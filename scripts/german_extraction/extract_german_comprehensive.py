#!/usr/bin/env python3
"""
FF7 German Comprehensive String Extractor v2
=============================================
Created: 2026-01-06 12:45 JST (Tuesday)
Session-ID: 85c271e2-f1ef-4bb6-b5dc-b212b2694001
Updated: Proper full extraction with categorization

This script extracts ALL German strings from ff7_de.exe and categorizes them into:
1. clean_strings/ - Pure German menu text (600+ strings)
2. asset_data/    - Texture filenames (.tim files)
3. menu_tables/   - UI table headers with embedded strings
4. developer_markers/ - Debug markers left by developers
5. raw_with_padding/ - Full extraction for reference

Usage:
    python extract_german_comprehensive.py
    python extract_german_comprehensive.py --exe /path/to/ff7_de.exe
"""

import os
import sys
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_GERMAN_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

# Full German string table range (from existing extraction)
STRING_TABLE_START = 0x58FBB0
STRING_TABLE_END = 0x59E000

# =============================================================================
# GERMAN DECODER
# =============================================================================

FF7_GERMAN_DECODE_MAP: Dict[int, str] = {
    0x66: 'Ü', 0x6A: 'ä', 0x7A: 'ö', 0x7E: 'ß', 0x7F: 'ü',
    0x61: 'á', 0x62: 'à', 0x63: 'â', 0x64: 'ã', 0x65: 'å',
    0x67: 'ç', 0x68: 'é', 0x69: 'è', 0x6B: 'ë',
    0x6C: 'í', 0x6D: 'ì', 0x6E: 'î', 0x6F: 'ï',
    0x70: 'ñ', 0x71: 'ó', 0x72: 'ò', 0x73: 'ô', 0x74: 'õ',
    0x76: '°', 0x77: '•', 0x78: '£',
}

def decode_ff7_german(data: bytes, show_unknown: bool = False) -> str:
    """Decode FF7 German encoded bytes to readable text."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        elif b in FF7_GERMAN_DECODE_MAP:
            result.append(FF7_GERMAN_DECODE_MAP[b])
        elif b == 0x00:
            result.append(' ')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))
        else:
            if show_unknown:
                result.append(f'[{b:02X}]')
    return ''.join(result)

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class ExtractedEntry:
    """Represents an extracted entry with full metadata."""
    index: int
    raw_offset: int      # Where the raw data starts (including padding)
    text_offset: int     # Where the actual text starts
    text: str
    raw_bytes: bytes
    padding_bytes: int
    total_bytes: int
    category: str        # 'clean', 'asset', 'menu_table', 'developer', 'unknown'

# =============================================================================
# CATEGORIZATION FUNCTIONS
# =============================================================================

def categorize_entry(raw_bytes: bytes, decoded_text: str) -> str:
    """Categorize an entry based on its content."""

    # Check for developer markers
    if b'START OF MENU' in raw_bytes or b'END OF MENU' in raw_bytes:
        return 'developer'
    if 'START OF MENU' in decoded_text or 'END OF MENU' in decoded_text:
        return 'developer'

    # Check for asset filenames (.tim in raw bytes = plain ASCII)
    if b'.tim' in raw_bytes:
        return 'asset'

    # Check for decoded .tim patterns (Nõèì = .tim decoded wrong)
    if 'Nõèì' in decoded_text or '.tim' in decoded_text.lower():
        return 'asset'

    # Check for menu table headers (UI coordinates before strings)
    # These have high bytes (0x80+) in first few positions AND embedded strings
    if len(raw_bytes) > 50:
        # Count high bytes in first 50 bytes
        high_byte_count = sum(1 for b in raw_bytes[:50] if b > 0x7F)
        if high_byte_count > 10:
            # Check if there are embedded FF-terminated strings
            if raw_bytes.count(b'\xFF') > 3:
                return 'menu_table'

    # Check for oversized garbage (coordinate tables, etc.)
    if len(decoded_text) > 200:
        # Check for patterns indicating non-text data
        special_chars = decoded_text.count('_') + decoded_text.count('`') + decoded_text.count('@')
        if special_chars > 20:
            return 'unknown'

    # If it's reasonably sized and has actual text, it's clean
    if len(decoded_text) > 0 and len(decoded_text) < 200:
        # Check it has some actual letters
        letter_count = sum(1 for c in decoded_text if c.isalpha())
        text_stripped = decoded_text.strip()

        # Accept if:
        # - Has at least 30% letters, OR
        # - Is short (<20 chars) and has at least 2 letters, OR
        # - Contains game terms like HP, MP, LV, etc.
        if letter_count > len(decoded_text) * 0.3:
            return 'clean'
        if len(text_stripped) < 20 and letter_count >= 2:
            return 'clean'
        if any(term in decoded_text.upper() for term in ['HP', 'MP', 'LV', 'PTS', 'GIL']):
            return 'clean'

    return 'unknown'

def find_text_start(raw_bytes: bytes) -> int:
    """Find where actual FF7-encoded text starts (skip leading 0x00 padding)."""
    for i, b in enumerate(raw_bytes):
        if b != 0x00:
            return i
    return len(raw_bytes)

def extract_embedded_strings(raw_bytes: bytes) -> List[Tuple[int, str]]:
    """Extract FF-terminated strings embedded within a data block."""
    strings = []
    current = []
    start = 0

    for i, b in enumerate(raw_bytes):
        if b == 0xFF:
            if current:
                decoded = decode_ff7_german(bytes(current))
                if len(decoded.strip()) > 1 and any(c.isalpha() for c in decoded):
                    strings.append((start, decoded.strip()))
            current = []
            start = i + 1
        else:
            if not current:
                start = i
            current.append(b)

    return strings

# =============================================================================
# MAIN EXTRACTION
# =============================================================================

def extract_all_entries(exe_path: str) -> List[ExtractedEntry]:
    """Extract all FF-terminated entries from the German string table."""

    with open(exe_path, 'rb') as f:
        f.seek(STRING_TABLE_START)
        data = f.read(STRING_TABLE_END - STRING_TABLE_START)

    entries = []
    current = []
    entry_start = 0
    index = 0

    for i, b in enumerate(data):
        if b == 0xFF:
            if current:
                raw_bytes = bytes(current) + b'\xFF'
                raw_offset = STRING_TABLE_START + entry_start

                # Find where text actually starts
                text_start = find_text_start(raw_bytes)
                text_offset = raw_offset + text_start

                # Decode the text
                decoded = decode_ff7_german(raw_bytes[text_start:]).strip()

                # Categorize
                category = categorize_entry(raw_bytes, decoded)

                entries.append(ExtractedEntry(
                    index=index,
                    raw_offset=raw_offset,
                    text_offset=text_offset,
                    text=decoded,
                    raw_bytes=raw_bytes,
                    padding_bytes=text_start,
                    total_bytes=len(raw_bytes),
                    category=category
                ))
                index += 1

            current = []
            entry_start = i + 1
        else:
            if not current:
                entry_start = i
            current.append(b)

    return entries

# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def write_clean_strings(entries: List[ExtractedEntry], output_dir: Path):
    """Write only clean German menu strings."""
    clean_dir = output_dir / "clean_strings"
    clean_dir.mkdir(exist_ok=True)

    clean = [e for e in entries if e.category == 'clean']

    # CSV with corrected offsets
    csv_path = clean_dir / "menu_strings.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'offset', 'text', 'length'])
        for e in clean:
            writer.writerow([e.index, f'0x{e.text_offset:06X}', e.text, len(e.text)])

    # Human-readable
    txt_path = clean_dir / "menu_strings.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Menu Strings (Clean)\n")
        f.write(f"# Total: {len(clean)} strings\n")
        f.write("# Format: [INDEX] OFFSET | TEXT\n")
        f.write("=" * 80 + "\n\n")
        for e in clean:
            f.write(f"[{e.index:03d}] 0x{e.text_offset:06X} | {e.text}\n")

    print(f"Wrote {len(clean)} clean strings to {csv_path}")
    return len(clean)

def write_asset_data(entries: List[ExtractedEntry], output_dir: Path):
    """Write asset filename entries."""
    asset_dir = output_dir / "asset_data"
    asset_dir.mkdir(exist_ok=True)

    assets = [e for e in entries if e.category == 'asset']

    csv_path = asset_dir / "asset_entries.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'offset', 'decoded_text', 'contains_tim_files'])
        for e in assets:
            # Extract actual .tim filenames from raw bytes
            tim_files = []
            raw_str = e.raw_bytes.decode('latin-1', errors='ignore')
            import re
            tim_files = re.findall(r'[\w_]+\.tim', raw_str, re.IGNORECASE)
            writer.writerow([e.index, f'0x{e.raw_offset:06X}', e.text[:100], ', '.join(tim_files)])

    # Also extract all .tim filenames found
    all_tim = []
    for e in assets:
        raw_str = e.raw_bytes.decode('latin-1', errors='ignore')
        import re
        for tim in re.findall(r'[\w_]+\.tim', raw_str, re.IGNORECASE):
            all_tim.append((e.raw_offset, tim))

    tim_path = asset_dir / "texture_filenames.csv"
    with open(tim_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['found_in_offset', 'filename'])
        for offset, filename in sorted(set(all_tim), key=lambda x: x[1]):
            writer.writerow([f'0x{offset:06X}', filename])

    print(f"Wrote {len(assets)} asset entries to {csv_path}")
    print(f"Found {len(set(all_tim))} unique .tim filenames")
    return len(assets)

def write_menu_tables(entries: List[ExtractedEntry], output_dir: Path):
    """Write menu table headers with their embedded strings."""
    table_dir = output_dir / "menu_tables"
    table_dir.mkdir(exist_ok=True)

    tables = [e for e in entries if e.category == 'menu_table']

    csv_path = table_dir / "menu_tables.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'offset', 'total_bytes', 'embedded_strings'])
        for e in tables:
            embedded = extract_embedded_strings(e.raw_bytes)
            embedded_text = ' | '.join([s[1] for s in embedded[:10]])
            writer.writerow([e.index, f'0x{e.raw_offset:06X}', e.total_bytes, embedded_text])

    # Detailed breakdown
    detail_path = table_dir / "menu_tables_detail.txt"
    with open(detail_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Menu Table Structures\n")
        f.write("# These entries contain UI coordinates AND embedded menu strings\n")
        f.write("=" * 80 + "\n\n")

        for e in tables:
            f.write(f"=== Index {e.index} at 0x{e.raw_offset:06X} ({e.total_bytes} bytes) ===\n")
            embedded = extract_embedded_strings(e.raw_bytes)
            f.write(f"Embedded strings found: {len(embedded)}\n")
            for offset, text in embedded:
                f.write(f"  +0x{offset:02X}: {text}\n")
            f.write("\n")

    print(f"Wrote {len(tables)} menu table entries to {csv_path}")
    return len(tables)

def write_developer_markers(entries: List[ExtractedEntry], output_dir: Path):
    """Write developer debug markers."""
    dev_dir = output_dir / "developer_markers"
    dev_dir.mkdir(exist_ok=True)

    devs = [e for e in entries if e.category == 'developer']

    txt_path = dev_dir / "developer_markers.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Developer Markers\n")
        f.write("# Debug text left in executable by developers\n")
        f.write("=" * 80 + "\n\n")

        for e in devs:
            f.write(f"Index {e.index} at 0x{e.raw_offset:06X}:\n")
            # Show raw ASCII where possible
            raw_ascii = e.raw_bytes.decode('latin-1', errors='ignore')
            f.write(f"  Raw: {raw_ascii[:200]}\n")
            f.write(f"  Decoded: {e.text[:200]}\n\n")

    print(f"Wrote {len(devs)} developer marker entries")
    return len(devs)

def write_raw_extraction(entries: List[ExtractedEntry], output_dir: Path):
    """Write full raw extraction for reference."""
    raw_dir = output_dir / "raw_with_padding"
    raw_dir.mkdir(exist_ok=True)

    csv_path = raw_dir / "all_entries_raw.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'raw_offset', 'text_offset', 'category', 'padding_bytes',
                        'total_bytes', 'text_preview'])
        for e in entries:
            writer.writerow([
                e.index,
                f'0x{e.raw_offset:06X}',
                f'0x{e.text_offset:06X}',
                e.category,
                e.padding_bytes,
                e.total_bytes,
                e.text[:80]
            ])

    # Category summary
    summary_path = raw_dir / "category_summary.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German String Extraction Summary\n")
        f.write("=" * 80 + "\n\n")

        categories = {}
        for e in entries:
            if e.category not in categories:
                categories[e.category] = []
            categories[e.category].append(e)

        for cat, cat_entries in sorted(categories.items()):
            f.write(f"{cat}: {len(cat_entries)} entries\n")

        f.write(f"\nTotal: {len(entries)} entries\n")

    print(f"Wrote {len(entries)} total entries to {csv_path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='FF7 German Comprehensive String Extractor v2')
    parser.add_argument('--exe', default=DEFAULT_GERMAN_EXE, help='Path to ff7_de.exe')
    parser.add_argument('--output', default=None, help='Output directory')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    output_dir = Path(args.output) if args.output else script_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("FF7 German Comprehensive String Extractor v2")
    print("=" * 80)
    print(f"Input:  {args.exe}")
    print(f"Output: {output_dir}")
    print(f"Range:  0x{STRING_TABLE_START:06X} - 0x{STRING_TABLE_END:06X}")
    print()

    if not os.path.exists(args.exe):
        print(f"ERROR: Executable not found: {args.exe}")
        sys.exit(1)

    # Extract all entries
    print("Extracting entries...")
    entries = extract_all_entries(args.exe)
    print(f"Found {len(entries)} total entries")
    print()

    # Categorize summary
    categories = {}
    for e in entries:
        if e.category not in categories:
            categories[e.category] = 0
        categories[e.category] += 1

    print("Categories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    print()

    # Write outputs
    print("Writing outputs...")
    write_clean_strings(entries, output_dir)
    write_asset_data(entries, output_dir)
    write_menu_tables(entries, output_dir)
    write_developer_markers(entries, output_dir)
    write_raw_extraction(entries, output_dir)

    print()
    print("=" * 80)
    print("Extraction complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
