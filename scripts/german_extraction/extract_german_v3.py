#!/usr/bin/env python3
"""
FF7 German Comprehensive String Extractor v3
=============================================
Created: 2026-01-06 14:30 JST (Tuesday)
Session-ID: 85c271e2-f1ef-4bb6-b5dc-b212b2694001
Author: John Zealand-Doyle

This script extracts German strings from ff7_de.exe with STRICT classification:

1. clean_text/      - ONLY actual German menu text (verified human-readable)
2. character_names/ - Character name struct entries (Cloud, Barret, Tifa, etc.)
3. ui_data/         - UI coordinate tables and binary positioning data
4. asset_data/      - Texture filenames (.tim files)
5. developer/       - Developer markers
6. raw_all/         - Complete extraction with all categories for reference

Classification is based on:
- Byte pattern analysis (not just decoded text)
- High-byte (0x80+) ratio detection for binary data
- FF7 encoding validation (bytes 0x01-0x7F are valid text range)
- Known pattern matching (coordinate patterns, character names)
- German word verification using character frequency analysis

Key insight: The "garbage" bytes are meaningful data:
- 0x595B94+ region: UI coordinate tables (16-byte binary records with 0xFF padding)
- 0x5981E8+ region: Binary/compressed data (high-byte values)
- 0x598900+ region: Character name structs (header + FF7-encoded name)
- 0x58FC22+ region: Plain ASCII texture filenames (.tim)
"""

import os
import sys
import csv
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_GERMAN_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

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

GERMAN_LETTERS = set('äöüÜßABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

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
    raw_offset: int
    text_offset: int
    text: str
    raw_bytes: bytes
    padding_bytes: int
    total_bytes: int
    category: str
    confidence: int
    reason: str

# =============================================================================
# CLASSIFICATION FUNCTIONS
# =============================================================================

# Known character name encodings for detection
CHARACTER_NAMES = {
    'CLOUD': b'\x23\x4C\x4F\x55\x44',
    'BARRET': b'\x22\x41\x52\x52\x45\x54',
    'TIFA': b'\x34\x49\x46\x41',
    'AERITH': b'\x21\x45\x52\x49\x54\x48',
    'AERIS': b'\x21\x45\x52\x49\x53',
    'RED': b'\x32\x45\x44',
    'YUFFIE': b'\x39\x55\x46\x46\x49\x45',
    'CAIT': b'\x23\x41\x49\x54',
    'VINCENT': b'\x36\x49\x4E\x43\x45\x4E\x54',
    'CID': b'\x23\x49\x44',
    'SEPHIROTH': b'\x33\x45\x50\x48\x49\x52\x4F\x54\x48',
    'CHOCO': b'\x23\x48\x4F\x43\x4F',
}

# Known German words/phrases that indicate valid menu text
GERMAN_INDICATORS = [
    'Auswähl', 'Fenster', 'Speicher', 'Kampf', 'Zauber', 'Objekt',
    'Materia', 'Ausrüst', 'Werte', 'Reihe', 'Limit', 'Konfig',
    'Verlassen', 'Möchten', 'Windows', 'Fantasy', 'Kontroll',
    'Cursor', 'Tempo', 'Meldung', 'Kamera', 'Hilfe', 'Taste',
    'drück', 'wählen', 'Angriff', 'Verteidig', 'Element', 'Effekt',
    'Stärke', 'Geschick', 'Vitalität', 'Glück', 'Moral',
    'Hitze', 'Kälte', 'Gewitter', 'Erde', 'Gift', 'Wasser', 'Wind',
    'Heilig', 'Tod', 'Gefahr', 'Schlaf', 'Trauer', 'Zorn',
    'Kaufen', 'Verkaufen', 'Beenden', 'Besitz', 'Gesamt',
    'Spielstand', 'Speichern', 'Laden', 'Formatier',
    'bitte', 'Bitte', 'nicht', 'Nicht', 'genug', 'mehr',
    'STUFE', 'Stufe', 'MASTER', 'Ebene',
]

def classify_entry(raw_bytes: bytes, decoded_text: str, raw_offset: int = 0) -> Tuple[str, int, str]:
    """
    Classify an entry based on byte patterns and decoded content.
    Returns: (category, confidence 0-100, reason)
    """
    if len(raw_bytes) == 0:
        return ('empty', 100, 'no data')

    text = decoded_text.strip()

    # =========================================================================
    # PRIORITY 1: Asset filenames (plain ASCII with .tim extension)
    # =========================================================================
    if b'.tim' in raw_bytes or b'.TIM' in raw_bytes:
        return ('asset', 100, 'contains .tim extension')
    if b'.tex' in raw_bytes or b'.TEX' in raw_bytes:
        return ('asset', 100, 'contains .tex extension')

    # =========================================================================
    # PRIORITY 2: Developer markers
    # =========================================================================
    if b'START OF MENU' in raw_bytes or b'END OF MENU' in raw_bytes:
        return ('developer', 100, 'developer marker')
    if b'SYSTEM' in raw_bytes and b'!!!' in raw_bytes:
        return ('developer', 95, 'developer marker pattern')

    # =========================================================================
    # PRIORITY 3: Character name structs
    # =========================================================================
    for name, encoded in CHARACTER_NAMES.items():
        if encoded in raw_bytes:
            return ('character_name', 95, f'contains {name}')

    # =========================================================================
    # PRIORITY 4: Binary data (high-byte ratio)
    # =========================================================================
    non_padding = bytes([b for b in raw_bytes if b != 0x00 and b != 0xFF])
    if len(non_padding) > 0:
        high_byte_count = sum(1 for b in non_padding if b >= 0x80)
        high_byte_ratio = high_byte_count / len(non_padding)

        # >30% high bytes = binary data
        if high_byte_ratio > 0.30:
            return ('binary_data', 90, f'high byte ratio: {high_byte_ratio:.2%}')

    # =========================================================================
    # PRIORITY 5: UI coordinate/table patterns
    # =========================================================================
    # Pattern: "X X 3Y1Z" where X is letter, Y/Z are digits/chars
    if re.match(r'^[A-Za-zäöüÜß] [A-Za-zäöüÜß] \d', text):
        return ('ui_table', 90, 'coordinate pattern: letter space letter space digit')

    # Pattern: "X X X" - repeated single letters with spaces
    if re.match(r'^[A-Za-zäöüÜß] [A-Za-zäöüÜß] [A-Za-zäöüÜß]', text) and len(text) < 15:
        return ('ui_table', 90, 'coordinate pattern: repeated letters with spaces')

    # Pattern: "x x  YZ" - single letters with double space then letters
    if re.match(r'^[A-Za-zäöüÜß] [A-Za-zäöüÜß]  [A-Z]{1,2}$', text):
        return ('ui_table', 90, 'coordinate pattern: letters with double space')

    # Pattern: short entries ending with digit-letter-digit
    if re.search(r'\d[A-Z]\d[A-Z]?$', text) and len(text) < 12:
        return ('ui_table', 85, 'coordinate pattern: ends with digit-letter pattern')

    # Known UI coordinate table region (0x595B94 - 0x596400)
    if STRING_TABLE_START <= raw_offset <= 0x596400:
        # If we're in the known coordinate region and text is short with letters+digits
        if 0x595B94 <= raw_offset <= 0x596400:
            if len(text) < 15 and re.search(r'[0-9]', text):
                return ('ui_table', 85, 'in known UI coordinate region with digits')

    # Multiple 0xFF terminators in short entry = UI table data
    ff_count = raw_bytes.count(0xFF)
    if len(raw_bytes) > 0 and len(raw_bytes) < 50 and ff_count > 3:
        return ('ui_table', 85, f'multiple 0xFF in short entry: {ff_count}')

    # =========================================================================
    # PRIORITY 6: Fragment detection (too short to be menu text)
    # =========================================================================
    if len(text) <= 2:
        # Allow specific 2-char German words: Ja, HP, MP, AP, LV
        if text.upper() in ['JA', 'HP', 'MP', 'AP', 'LV', 'OK', 'GIL']:
            pass  # Continue to clean_text check
        else:
            return ('fragment', 80, 'too short for menu text')

    # =========================================================================
    # PRIORITY 7: Check for actual German text
    # =========================================================================
    if len(text) > 0:
        # Count actual German letters
        german_letter_count = sum(1 for c in text if c in GERMAN_LETTERS)
        german_ratio = german_letter_count / len(text)

        # Check for known German indicators
        has_german_word = any(ind in text for ind in GERMAN_INDICATORS)

        # Check FF7 encoding validity (should be mostly 0x01-0x7F)
        valid_ff7 = sum(1 for b in non_padding if 0x01 <= b <= 0x7F)
        ff7_ratio = valid_ff7 / len(non_padding) if len(non_padding) > 0 else 0

        # Check for suspicious patterns that indicate non-text
        has_suspicious_pattern = any([
            '  3' in text and '1' in text,  # Coordinate pattern variant
            '!!' in text and len(text) > 20,  # Multiple bangs in long string (usually struct data)
            re.search(r'\[\w+\]', decoded_text),  # Has [XX] unknown byte markers
            text.count('[') > 3,  # Too many unknown bytes
            '°' in text and text.count('°') > 2,  # Multiple degree symbols (unlikely in menu)
            re.match(r'^[A-Za-z] [A-Za-z] \d', text),  # Coordinate pattern at start
            re.match(r'^\d[A-Za-z]\d', text),  # Numeric pattern at start
            bool(re.search(r'[!#$%&]{3,}', text)),  # Multiple special chars in sequence
            text.startswith('!') and len(text) > 5,  # Starts with ! and is long
        ])

        # Check for garbage prefix patterns (text starts with non-word characters)
        # This catches entries like "!S   S "S..."
        garbage_prefix = re.match(r'^[^A-Za-zäöüÜßÄÖ]{5,}', text)
        if garbage_prefix:
            has_suspicious_pattern = True

        # Check for keyboard layout patterns
        keyboard_pattern = re.search(r'[A-Z]{10,}', text)  # Long uppercase sequences
        if keyboard_pattern:
            # Unless it's a common German word in caps
            caps_section = keyboard_pattern.group()
            if caps_section not in ['MASTER', 'STUFE', 'BLOCK', 'STECKPLATZ']:
                has_suspicious_pattern = True

        # Strong indicators of valid German text - BUT only if no suspicious patterns
        if has_german_word and not has_suspicious_pattern:
            return ('clean_text', 95, f'contains German indicator word')

        # High German letter ratio + high FF7 validity = likely good text
        if german_ratio > 0.5 and ff7_ratio > 0.9 and not has_suspicious_pattern:
            return ('clean_text', 85, f'german_ratio={german_ratio:.2%}, ff7_valid={ff7_ratio:.2%}')

        # Medium confidence: decent ratios but no indicator word
        if german_ratio > 0.4 and ff7_ratio > 0.85 and not has_suspicious_pattern:
            if len(text) >= 3:  # At least 3 chars
                return ('clean_text', 75, f'german_ratio={german_ratio:.2%}, ff7_valid={ff7_ratio:.2%}')

    # =========================================================================
    # DEFAULT: Unknown
    # =========================================================================
    return ('unknown', 50, 'no pattern matched')

def find_text_start(raw_bytes: bytes) -> int:
    """Find where actual FF7-encoded text starts (skip leading 0x00 padding)."""
    for i, b in enumerate(raw_bytes):
        if b != 0x00:
            return i
    return len(raw_bytes)

def extract_character_name(raw_bytes: bytes) -> Optional[str]:
    """Extract the actual character name from a struct entry."""
    for name, encoded in CHARACTER_NAMES.items():
        pos = raw_bytes.find(encoded)
        if pos != -1:
            # Find the FF terminator after the name
            end_pos = raw_bytes.find(b'\xFF', pos)
            if end_pos != -1:
                name_bytes = raw_bytes[pos:end_pos]
                return decode_ff7_german(name_bytes).strip()
    return None

def parse_character_struct(raw_bytes: bytes, offset: int) -> dict:
    """
    Parse a 132-byte character name struct.

    Structure:
    - Bytes 0-3: Character ID (uint32 LE)
    - Byte 4: Slot index (01=Barret, 02=Tifa, etc.)
    - Byte 5: Flag (usually 0x01)
    - Bytes 6-11: Base stats (STR, VIT, MAG, SPR, DEX, LCK)
    - Bytes 12-17: Padding
    - Byte 18: Prefix marker (0x01)
    - Byte 19: Position/modifier code
    - Bytes 20+: FF7-encoded name + FF terminator
    """
    result = {
        'offset': f'0x{offset:06X}',
        'char_id': int.from_bytes(raw_bytes[0:4], 'little') if len(raw_bytes) >= 4 else 0,
        'slot_index': raw_bytes[4] if len(raw_bytes) > 4 else 0,
        'stats': {
            'STR': raw_bytes[6] if len(raw_bytes) > 6 else 0,
            'VIT': raw_bytes[7] if len(raw_bytes) > 7 else 0,
            'MAG': raw_bytes[8] if len(raw_bytes) > 8 else 0,
            'SPR': raw_bytes[9] if len(raw_bytes) > 9 else 0,
            'DEX': raw_bytes[10] if len(raw_bytes) > 10 else 0,
            'LCK': raw_bytes[11] if len(raw_bytes) > 11 else 0,
        },
        'name': None,
        'name_offset': None,
    }

    # Find the name (starts at byte 20, encoded)
    if len(raw_bytes) >= 20:
        name_bytes = raw_bytes[20:]
        # Find FF terminator
        ff_pos = name_bytes.find(b'\xFF')
        if ff_pos > 0:
            name_encoded = name_bytes[:ff_pos]
            result['name'] = decode_ff7_german(name_encoded).strip()
            result['name_offset'] = f'0x{offset + 20:06X}'

    return result

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
                raw_bytes = bytes(current)  # Don't include FF
                raw_offset = STRING_TABLE_START + entry_start

                text_start = find_text_start(raw_bytes)
                text_offset = raw_offset + text_start

                decoded = decode_ff7_german(raw_bytes[text_start:]).strip()
                category, confidence, reason = classify_entry(raw_bytes, decoded, raw_offset)

                entries.append(ExtractedEntry(
                    index=index,
                    raw_offset=raw_offset,
                    text_offset=text_offset,
                    text=decoded,
                    raw_bytes=raw_bytes,
                    padding_bytes=text_start,
                    total_bytes=len(raw_bytes),
                    category=category,
                    confidence=confidence,
                    reason=reason,
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

def write_clean_text(entries: List[ExtractedEntry], output_dir: Path):
    """Write only verified clean German menu strings."""
    clean_dir = output_dir / "clean_text"
    clean_dir.mkdir(exist_ok=True)

    # Filter: category=clean_text AND confidence >= 75
    clean = [e for e in entries if e.category == 'clean_text' and e.confidence >= 75]

    csv_path = clean_dir / "german_menu_strings.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'offset', 'text', 'length', 'confidence', 'reason'])
        for e in clean:
            writer.writerow([e.index, f'0x{e.text_offset:06X}', e.text, len(e.text),
                           e.confidence, e.reason])

    txt_path = clean_dir / "german_menu_strings.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Menu Strings - Clean Extraction v3\n")
        f.write(f"# Total: {len(clean)} verified strings\n")
        f.write(f"# Confidence threshold: 75%\n")
        f.write("# Format: [INDEX] OFFSET | TEXT\n")
        f.write("=" * 80 + "\n\n")
        for e in clean:
            f.write(f"[{e.index:04d}] 0x{e.text_offset:06X} | {e.text}\n")

    print(f"  clean_text: {len(clean)} entries -> {csv_path}")
    return len(clean)

def write_character_names(entries: List[ExtractedEntry], output_dir: Path):
    """Write character name struct entries with extracted names."""
    char_dir = output_dir / "character_names"
    char_dir.mkdir(exist_ok=True)

    names = [e for e in entries if e.category == 'character_name']

    csv_path = char_dir / "character_names.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'struct_offset', 'raw_text', 'extracted_name', 'struct_size'])
        for e in names:
            extracted = extract_character_name(e.raw_bytes)
            writer.writerow([e.index, f'0x{e.raw_offset:06X}', e.text[:50],
                           extracted or 'UNKNOWN', e.total_bytes])

    txt_path = char_dir / "character_names.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Character Name Structs\n")
        f.write("# These entries contain binary struct headers + FF7-encoded names\n")
        f.write("=" * 80 + "\n\n")
        for e in names:
            extracted = extract_character_name(e.raw_bytes)
            f.write(f"Index {e.index} at 0x{e.raw_offset:06X}:\n")
            f.write(f"  Struct size: {e.total_bytes} bytes\n")
            f.write(f"  Extracted name: {extracted or 'UNKNOWN'}\n")
            f.write(f"  Raw decoded: {e.text[:60]}...\n\n")

    print(f"  character_names: {len(names)} entries -> {csv_path}")
    return len(names)

def write_ui_data(entries: List[ExtractedEntry], output_dir: Path):
    """Write UI table/coordinate data entries."""
    ui_dir = output_dir / "ui_data"
    ui_dir.mkdir(exist_ok=True)

    # Include ui_table, binary_data, fragments
    ui = [e for e in entries if e.category in ('ui_table', 'binary_data', 'fragment')]

    csv_path = ui_dir / "ui_binary_data.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'offset', 'category', 'size', 'hex_preview', 'decoded_preview'])
        for e in ui:
            hex_preview = e.raw_bytes[:20].hex()
            writer.writerow([e.index, f'0x{e.raw_offset:06X}', e.category,
                           e.total_bytes, hex_preview, e.text[:30]])

    print(f"  ui_data: {len(ui)} entries -> {csv_path}")
    return len(ui)

def write_asset_data(entries: List[ExtractedEntry], output_dir: Path):
    """Write asset filename entries."""
    asset_dir = output_dir / "asset_data"
    asset_dir.mkdir(exist_ok=True)

    assets = [e for e in entries if e.category == 'asset']

    # Extract all .tim filenames
    all_tim = []
    for e in assets:
        raw_str = e.raw_bytes.decode('latin-1', errors='ignore')
        tim_files = re.findall(r'[\w_]+\.tim', raw_str, re.IGNORECASE)
        for tim in tim_files:
            all_tim.append((e.raw_offset, tim))

    csv_path = asset_dir / "texture_filenames.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['offset', 'filename'])
        for offset, filename in sorted(set(all_tim), key=lambda x: x[1]):
            writer.writerow([f'0x{offset:06X}', filename])

    print(f"  asset_data: {len(set(all_tim))} unique .tim files -> {csv_path}")
    return len(assets)

def write_developer_markers(entries: List[ExtractedEntry], output_dir: Path):
    """Write developer debug markers."""
    dev_dir = output_dir / "developer"
    dev_dir.mkdir(exist_ok=True)

    devs = [e for e in entries if e.category == 'developer']

    txt_path = dev_dir / "developer_markers.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Developer Markers\n")
        f.write("=" * 80 + "\n\n")
        for e in devs:
            raw_ascii = e.raw_bytes.decode('latin-1', errors='ignore')
            f.write(f"Index {e.index} at 0x{e.raw_offset:06X}:\n")
            f.write(f"  Raw ASCII: {raw_ascii[:100]}\n")
            f.write(f"  FF7 Decoded: {e.text[:100]}\n\n")

    print(f"  developer: {len(devs)} entries -> {txt_path}")
    return len(devs)

def write_raw_all(entries: List[ExtractedEntry], output_dir: Path):
    """Write complete extraction with all categories."""
    raw_dir = output_dir / "raw_all"
    raw_dir.mkdir(exist_ok=True)

    csv_path = raw_dir / "all_entries.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'raw_offset', 'text_offset', 'category', 'confidence',
                        'padding', 'total_bytes', 'text_preview', 'reason'])
        for e in entries:
            writer.writerow([
                e.index,
                f'0x{e.raw_offset:06X}',
                f'0x{e.text_offset:06X}',
                e.category,
                e.confidence,
                e.padding_bytes,
                e.total_bytes,
                e.text[:60],
                e.reason
            ])

    # Summary file
    summary_path = raw_dir / "category_summary.txt"
    categories = {}
    for e in entries:
        if e.category not in categories:
            categories[e.category] = 0
        categories[e.category] += 1

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German String Extraction Summary v3\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total entries: {len(entries)}\n\n")
        f.write("By category:\n")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            f.write(f"  {cat:20s}: {count:4d}\n")

    print(f"  raw_all: {len(entries)} entries -> {csv_path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='FF7 German Comprehensive String Extractor v3')
    parser.add_argument('--exe', default=DEFAULT_GERMAN_EXE, help='Path to ff7_de.exe')
    parser.add_argument('--output', default=None, help='Output directory')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    output_dir = Path(args.output) if args.output else script_dir / "output_v3"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("FF7 German Comprehensive String Extractor v3")
    print("=" * 80)
    print(f"Input:  {args.exe}")
    print(f"Output: {output_dir}")
    print(f"Range:  0x{STRING_TABLE_START:06X} - 0x{STRING_TABLE_END:06X}")
    print()

    if not os.path.exists(args.exe):
        print(f"ERROR: Executable not found: {args.exe}")
        sys.exit(1)

    # Extract
    print("Extracting entries...")
    entries = extract_all_entries(args.exe)
    print(f"Found {len(entries)} total entries")
    print()

    # Summary
    print("Category breakdown:")
    categories = {}
    for e in entries:
        if e.category not in categories:
            categories[e.category] = 0
        categories[e.category] += 1
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat:20s}: {count:4d}")
    print()

    # Write outputs
    print("Writing outputs:")
    write_clean_text(entries, output_dir)
    write_character_names(entries, output_dir)
    write_ui_data(entries, output_dir)
    write_asset_data(entries, output_dir)
    write_developer_markers(entries, output_dir)
    write_raw_all(entries, output_dir)

    print()
    print("=" * 80)
    print("Extraction complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
