#!/usr/bin/env python3
"""
Complete EN-DE Offset Mapper for FF7 PC

This script:
1. Extracts all 767 touphScript offset entries from documentation
2. Maps each offset from Steam EN to eStore EN (+0xC00)
3. Finds corresponding German offsets using regional delta analysis
4. Generates comprehensive CSV output

Created: 2026-01-02
Session: Agent 4 - EN-DE Offset Mapping
"""

import os
import re
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# File paths
STEAM_EN_EXE = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
ESTORE_EN_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe"
ESTORE_DE_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
TOUPH_DOC = "/home/johnzealanddoyle/projects/ff7OG_japanese/docs/TOUPHSCRIPT_OFFSET_TABLE_COMPLETE.md"

# Delta from Steam EN to eStore EN
STEAM_TO_ESTORE_DELTA = 0xC00

# Type name mapping
TYPE_NAMES = {
    0: "DEF",
    1: "NOFF_TERM",
    2: "RGB",
    3: "UNICODE",
    4: "FFPADDED",
    5: "ZEROTERM"
}

# Known DE string region mappings (eStore EN offset -> eStore DE offset)
# These are anchor points discovered through manual analysis
REGION_ANCHORS = {
    # Config screen region (strings around 0x519000)
    "config_screen": {
        "en_base": 0x5194A8,  # WINDOW COLOR in eStore EN
        "de_base": 0x5900F0,  # FENSTERFARBE in eStore DE
        "delta": 0x5900F0 - 0x5194A8,  # 0x76C48
        "en_range": (0x519000, 0x51A000),
    },
    # Menu items region
    "menu_items": {
        "en_base": 0x519EC0,  # ITEM in eStore EN
        "de_base": None,  # To be found
        "delta": None,
        "en_range": (0x5192C0, 0x5194A0),
    },
}


def read_bytes(filepath: str, offset: int, length: int) -> bytes:
    """Read bytes from file at given offset."""
    try:
        with open(filepath, 'rb') as f:
            f.seek(offset)
            return f.read(length)
    except Exception:
        return b''


def decode_ff7_text(data: bytes) -> str:
    """
    Decode FF7 text encoding to readable string.
    """
    result = []
    for byte in data:
        if byte == 0xFF:
            break
        elif byte == 0x00:
            result.append(' ')
        elif 0x21 <= byte <= 0x3A:
            result.append(chr(ord('A') + byte - 0x21))
        elif 0x3B <= byte <= 0x54:
            result.append(chr(ord('a') + byte - 0x3B))
        elif 0x01 <= byte <= 0x0A:
            if byte == 0x0A:
                result.append('0')
            else:
                result.append(str(byte))
        else:
            result.append(f'[{byte:02X}]')
    return ''.join(result)


def parse_touphscript_doc() -> List[Tuple[int, int, int, int]]:
    """
    Parse the touphScript documentation to extract all offset entries.
    Returns list of (index, offset, length, type)
    """
    entries = []

    with open(TOUPH_DOC, 'r') as f:
        content = f.read()

    # Pattern to match table rows: | 0 | 0x518370 | 30 | 0 | DEF |
    pattern = r'\|\s*(\d+)\s*\|\s*(0x[0-9A-Fa-f]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|'

    for match in re.finditer(pattern, content):
        idx = int(match.group(1))
        offset = int(match.group(2), 16)
        length = int(match.group(3))
        str_type = int(match.group(4))
        entries.append((idx, offset, length, str_type))

    return sorted(entries, key=lambda x: x[0])


def find_string_in_exe(exe_path: str, search_bytes: bytes, start: int = 0, end: int = 0) -> List[int]:
    """Find all occurrences of bytes in exe."""
    results = []
    try:
        with open(exe_path, 'rb') as f:
            if end == 0:
                data = f.read()
            else:
                f.seek(start)
                data = f.read(end - start)

        idx = 0
        while True:
            idx = data.find(search_bytes, idx)
            if idx == -1:
                break
            results.append(start + idx)
            idx += 1
    except Exception:
        pass
    return results


def discover_de_offset(estore_en_offset: int, length: int) -> Tuple[int, str, str]:
    """
    Try to discover the DE offset for a given EN offset.
    Returns (de_offset, confidence, method)
    """
    # Read EN bytes
    en_bytes = read_bytes(ESTORE_EN_EXE, estore_en_offset, length)
    if not en_bytes or en_bytes == b'\x00' * length:
        return 0, "NONE", "empty_string"

    # Check if string is mostly nulls/padding
    non_null = sum(1 for b in en_bytes if b != 0 and b != 0xFF)
    if non_null < 2:
        return 0, "NONE", "padding_only"

    # Method 1: Search for exact bytes in DE exe
    # This works for identical strings (SOUND, CURSOR, ATB, etc.)
    de_matches = find_string_in_exe(ESTORE_DE_EXE, en_bytes, 0x500000, 0x600000)
    if de_matches:
        # Found exact match
        return de_matches[0], "HIGH", "exact_match"

    # Method 2: Use regional delta
    # Config screen region delta
    config_delta = REGION_ANCHORS["config_screen"]["delta"]
    estimated_de = estore_en_offset + config_delta

    # Check if the estimated position has valid FF7 text
    de_bytes = read_bytes(ESTORE_DE_EXE, estimated_de, length)
    if de_bytes and de_bytes != b'\x00' * length:
        # Check for FF7 text terminator
        if 0xFF in de_bytes:
            return estimated_de, "MEDIUM", "regional_delta"

    # Method 3: Search nearby for any FF7 text
    # Look for 0xFF terminator in reasonable range
    for delta_offset in range(-0x1000, 0x1000, 0x10):
        test_offset = estimated_de + delta_offset
        test_bytes = read_bytes(ESTORE_DE_EXE, test_offset, length)
        if test_bytes and 0xFF in test_bytes[:min(len(test_bytes), 20)]:
            # Found potential text
            return test_offset, "LOW", "nearby_search"

    return 0, "NONE", "not_found"


def main():
    """Main function."""
    output_dir = Path(__file__).parent

    print("FF7 EN-DE Comprehensive Offset Mapper")
    print("=" * 70)

    # Check files exist
    for name, path in [("Steam EN", STEAM_EN_EXE), ("eStore EN", ESTORE_EN_EXE),
                       ("eStore DE", ESTORE_DE_EXE), ("TouphDoc", TOUPH_DOC)]:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  {name}: {path}")
            print(f"         Size: {size:,} bytes")
        else:
            print(f"  {name}: NOT FOUND - {path}")
            return

    print()

    # Parse touphScript documentation
    print("Parsing touphScript offset table...")
    entries = parse_touphscript_doc()
    print(f"  Found {len(entries)} entries")

    # Process each entry
    print("\nProcessing entries...")
    results = []
    stats = defaultdict(int)

    for idx, steam_offset, length, str_type in entries:
        estore_en_offset = steam_offset + STEAM_TO_ESTORE_DELTA

        # Read EN text
        en_bytes = read_bytes(ESTORE_EN_EXE, estore_en_offset, length)
        en_text = decode_ff7_text(en_bytes) if en_bytes else ""

        # Find DE offset
        de_offset, confidence, method = discover_de_offset(estore_en_offset, length)

        # Read DE text
        de_bytes = b''
        de_text = ""
        if de_offset > 0:
            de_bytes = read_bytes(ESTORE_DE_EXE, de_offset, length)
            de_text = decode_ff7_text(de_bytes) if de_bytes else ""

        # Calculate delta
        delta = de_offset - estore_en_offset if de_offset > 0 else 0

        results.append({
            'index': idx,
            'steam_en_offset': f"0x{steam_offset:06X}",
            'steam_en_va': f"0x{steam_offset + 0x17600:06X}",
            'estore_en_offset': f"0x{estore_en_offset:06X}",
            'estore_de_offset': f"0x{de_offset:06X}" if de_offset > 0 else "",
            'en_text': en_text[:40].replace(',', ';'),
            'de_text': de_text[:40].replace(',', ';'),
            'de_bytes_hex': de_bytes.hex().upper()[:60] if de_bytes else "",
            'confidence': confidence,
            'method': method,
            'delta': f"0x{delta:X}" if delta > 0 else "",
            'length': length,
            'type': TYPE_NAMES.get(str_type, str(str_type))
        })

        stats[confidence] += 1

        if idx % 100 == 0:
            print(f"  Processed {idx}/{len(entries)}...")

    # Write CSV
    csv_path = output_dir / "en_de_offset_mapping.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['index', 'steam_en_offset', 'steam_en_va', 'estore_en_offset',
                     'estore_de_offset', 'en_text', 'de_text', 'de_bytes_hex',
                     'confidence', 'method', 'delta', 'length', 'type']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nWrote {len(results)} entries to: {csv_path}")

    # Print statistics
    print("\n" + "=" * 70)
    print("CONFIDENCE STATISTICS")
    print("=" * 70)
    for conf, count in sorted(stats.items()):
        pct = 100.0 * count / len(results)
        print(f"  {conf:10s}: {count:4d} ({pct:5.1f}%)")

    # Write analysis report
    report_path = output_dir / "offset_delta_analysis.md"
    with open(report_path, 'w') as f:
        f.write("# EN-DE Offset Delta Analysis\n\n")
        f.write(f"**Generated:** 2026-01-02\n")
        f.write(f"**Total Entries:** {len(results)}\n\n")

        f.write("## Confidence Summary\n\n")
        f.write("| Confidence | Count | Percentage |\n")
        f.write("|------------|-------|------------|\n")
        for conf, count in sorted(stats.items()):
            pct = 100.0 * count / len(results)
            f.write(f"| {conf} | {count} | {pct:.1f}% |\n")

        f.write("\n## Key Findings\n\n")
        f.write("### Delta Pattern Analysis\n\n")
        f.write("1. **Steam EN to eStore EN**: Constant delta of `0xC00` (3072 bytes)\n")
        f.write("2. **eStore EN to eStore DE**: Variable delta depending on region\n")
        f.write(f"   - Config screen region: ~`0x{REGION_ANCHORS['config_screen']['delta']:X}`\n")
        f.write("\n### Why Deltas Vary\n\n")
        f.write("German translations are often longer than English, which shifts subsequent strings.\n")
        f.write("Examples:\n")
        f.write("- 'BATTLE SPEED' -> 'KAMPFTEMPO' (same length)\n")
        f.write("- 'WINDOW COLOR' -> 'FENSTERFARBE' (12 chars vs 12 chars)\n")
        f.write("- 'FIELD MESSAGE' -> 'FELDMELDUNG' (shorter in German!)\n")

        f.write("\n## Regional Delta Map\n\n")
        f.write("```\n")
        for region_name, region_data in REGION_ANCHORS.items():
            if region_data["delta"]:
                f.write(f"Region: {region_name}\n")
                f.write(f"  EN Range: 0x{region_data['en_range'][0]:06X} - 0x{region_data['en_range'][1]:06X}\n")
                f.write(f"  Delta: 0x{region_data['delta']:X} ({region_data['delta']} bytes)\n\n")
        f.write("```\n")

    print(f"Wrote analysis to: {report_path}")

    # Write anchor pairs documentation
    anchor_path = output_dir / "anchor_pair_mapping.txt"
    with open(anchor_path, 'w') as f:
        f.write("# Anchor Pair Mapping\n")
        f.write("# Format: [EN_TEXT] -> [DE_TEXT] at EN_OFFSET -> DE_OFFSET (delta=XXXX)\n\n")

        # Extract high-confidence matches as anchors
        anchors = [(r['en_text'], r['de_text'], r['estore_en_offset'], r['estore_de_offset'], r['delta'])
                   for r in results if r['confidence'] == 'HIGH' and r['en_text'] and r['de_text']]

        for en_text, de_text, en_off, de_off, delta in anchors[:50]:  # Top 50
            f.write(f"{en_text:30s} -> {de_text:30s} at {en_off} -> {de_off} (delta={delta})\n")

    print(f"Wrote anchor pairs to: {anchor_path}")

    # Write problem regions documentation
    problem_path = output_dir / "problem_regions.md"
    with open(problem_path, 'w') as f:
        f.write("# Problem Regions\n\n")
        f.write("Regions where EN-DE mapping was difficult or failed.\n\n")

        f.write("## Strings Not Found in DE\n\n")
        not_found = [(r['index'], r['en_text'], r['steam_en_offset'])
                     for r in results if r['confidence'] == 'NONE' and r['en_text']]
        for idx, text, offset in not_found[:30]:
            f.write(f"- [{idx}] `{text}` at {offset}\n")

        f.write("\n## Low Confidence Mappings\n\n")
        low_conf = [(r['index'], r['en_text'], r['de_text'], r['steam_en_offset'])
                    for r in results if r['confidence'] == 'LOW']
        for idx, en_text, de_text, offset in low_conf[:30]:
            f.write(f"- [{idx}] `{en_text}` -> `{de_text}` at {offset}\n")

    print(f"Wrote problem regions to: {problem_path}")

    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
