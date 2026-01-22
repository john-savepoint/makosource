#!/usr/bin/env python3
"""
FF7 German Localization Offset Finder

Analyzes Steam EN, eStore EN, and eStore DE executables to find
the correct offsets for German localization.

Created: 2025-01-02
Context: Finding German exe string offsets for FF7 localization work.
         The DE exe is 12KB larger than EN exe with no fixed delta.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Steam EN offset + 0xC00 = eStore EN offset (tested and confirmed)
STEAM_TO_ESTORE_DELTA = 0xC00

# Paths to executables
STEAM_EN_EXE = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe")
ESTORE_EN_EXE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe")
ESTORE_DE_EXE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe")

# From touphScript - Steam EN offsets (first 100 for initial analysis)
EN_OFFSETS = [
    0x518370, 0x51838E, 0x5183AC, 0x5183D0, 0x5183D4, 0x5188A8, 0x5188D8,
    0x518908, 0x518938, 0x518968, 0x518998, 0x5189C8, 0x5189F8, 0x518A28,
    0x518A58, 0x518A88, 0x518AB8, 0x518C08, 0x518C38, 0x518C68, 0x518C98,
    0x518CC8, 0x518CF8, 0x518D28, 0x518D58, 0x518D88, 0x518DE8, 0x518E18,
    0x518ED8, 0x518F08, 0x518F38, 0x518F68, 0x518FC8, 0x519238, 0x51923E,
    0x519244, 0x519288, 0x5192A1, 0x5192C0, 0x5192D4, 0x5192E8, 0x5192FC,
    0x519310, 0x519324, 0x519338, 0x51934C, 0x519360, 0x519374, 0x519388,
    0x51939C, 0x5193D8, 0x5193EC, 0x519400, 0x519414, 0x519428, 0x519450,
    0x519464, 0x519478, 0x5196B0, 0x5196E2, 0x519714, 0x519746, 0x519778,
    0x5197AA, 0x5197DC, 0x51980E, 0x519840, 0x519872, 0x5198A4, 0x5198D6,
    0x519908, 0x51993A, 0x51996C, 0x51999E, 0x5199D0, 0x519A02, 0x519A34,
    0x519FE0, 0x519FE8, 0x519FEC, 0x519FF0, 0x519FF4, 0x519FF8, 0x519FFC,
    0x51A000, 0x51A004, 0x51A008, 0x51A00C, 0x51A010, 0x51A018, 0x51A020,
    0x51A02C, 0x51A030, 0x51A034, 0x51A038, 0x51A03C, 0x51A040, 0x51A044,
    0x51A048, 0x51A04C,
]

# String lengths from touphScript (first 100)
STRING_LENGTHS = [
    30, 30, 30, 4, 4, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 6, 6, 6, 25, 25,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
    50, 50, 50, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 12, 4, 4, 4, 4, 4, 4,
    4, 4, 4,
]


def decode_ff7_english(data: bytes) -> str:
    """Decode English FF7 string."""
    result = []
    for byte in data:
        if byte == 0xFF:
            break
        if byte == 0x00:
            result.append(' ')
        elif 0x01 <= byte <= 0x5F:
            result.append(chr(byte + 0x20))
        else:
            result.append(f'[{byte:02X}]')
    return ''.join(result)


def find_bytes_in_file(f, search_bytes: bytes, start: int = 0, end: int = None) -> List[int]:
    """Find all occurrences of bytes in file."""
    if end is None:
        f.seek(0, 2)  # Seek to end
        end = f.tell()

    matches = []
    search_len = len(search_bytes)

    # Read file in chunks for efficiency
    chunk_size = 1024 * 1024  # 1MB chunks
    f.seek(start)

    pos = start
    overlap_buffer = b''

    while pos < end:
        read_size = min(chunk_size, end - pos)
        chunk = overlap_buffer + f.read(read_size)

        # Search in chunk
        search_pos = 0
        while True:
            found = chunk.find(search_bytes, search_pos)
            if found == -1:
                break
            actual_pos = pos - len(overlap_buffer) + found
            matches.append(actual_pos)
            search_pos = found + 1

        # Keep overlap for cross-boundary matches
        overlap_buffer = chunk[-(search_len-1):] if len(chunk) >= search_len else chunk
        pos += read_size

    return matches


def analyze_string(index: int, steam_offset: int, length: int,
                   steam_en_f, estore_en_f, estore_de_f) -> Dict:
    """Analyze a single string across all three executables."""

    result = {
        'index': index,
        'steam_en_offset': steam_offset,
        'estore_en_offset': steam_offset + STEAM_TO_ESTORE_DELTA,
        'de_offset': None,
        'length': length,
        'en_text': None,
        'de_text': None,
        'steam_en_bytes': None,
        'estore_en_bytes': None,
        'de_bytes': None,
        'de_matches': [],
        'status': 'unknown',
    }

    # Read Steam EN
    steam_en_f.seek(steam_offset)
    steam_en_bytes = steam_en_f.read(length)
    result['steam_en_bytes'] = steam_en_bytes
    result['en_text'] = decode_ff7_english(steam_en_bytes)

    # Read eStore EN (should be identical at +0xC00)
    estore_en_offset = steam_offset + STEAM_TO_ESTORE_DELTA
    estore_en_f.seek(estore_en_offset)
    estore_en_bytes = estore_en_f.read(length)
    result['estore_en_bytes'] = estore_en_bytes

    # Verify Steam EN and eStore EN match
    if steam_en_bytes != estore_en_bytes:
        result['status'] = 'en_mismatch'
        return result

    # Search for exact bytes in DE exe
    de_matches = find_bytes_in_file(estore_de_f, estore_en_bytes)
    result['de_matches'] = de_matches

    if len(de_matches) == 0:
        # No exact match - string is localized in DE
        # Try to find the string by searching in expected region
        # DE strings should be near the EN offset
        result['status'] = 'localized'

        # Read what's at the expected offset to see if it's valid German text
        # Try various delta values around the expected region
        for delta in [0xC00, 0xC00 + 0x1000, 0xC00 + 0x2000, 0xC00 + 0x3000]:
            test_offset = steam_offset + delta
            try:
                estore_de_f.seek(test_offset)
                de_bytes = estore_de_f.read(length)
                de_text = decode_ff7_english(de_bytes)
                # Check if it looks like valid text
                if de_bytes[0] != 0x00 and de_bytes[0] != 0xFF:
                    result['de_offset'] = test_offset
                    result['de_bytes'] = de_bytes
                    result['de_text'] = de_text
                    result['de_delta'] = delta
                    break
            except:
                continue

    elif len(de_matches) == 1:
        # Exactly one match - perfect!
        result['de_offset'] = de_matches[0]
        estore_de_f.seek(de_matches[0])
        result['de_bytes'] = estore_de_f.read(length)
        result['de_text'] = decode_ff7_english(result['de_bytes'])
        result['status'] = 'unique_match'

    else:
        # Multiple matches - need disambiguation
        result['status'] = 'multiple_matches'
        # Take the one closest to expected offset
        expected = steam_offset + STEAM_TO_ESTORE_DELTA
        closest = min(de_matches, key=lambda x: abs(x - expected))
        result['de_offset'] = closest
        estore_de_f.seek(closest)
        result['de_bytes'] = estore_de_f.read(length)
        result['de_text'] = decode_ff7_english(result['de_bytes'])

    return result


def main():
    print("FF7 German Localization Offset Finder")
    print("=" * 60)
    print()

    # Verify files exist
    for path, name in [(STEAM_EN_EXE, "Steam EN"), (ESTORE_EN_EXE, "eStore EN"), (ESTORE_DE_EXE, "eStore DE")]:
        if not path.exists():
            print(f"ERROR: {name} not found at {path}")
            sys.exit(1)
        print(f"{name}: {path} ({path.stat().st_size:,} bytes)")

    print()
    print(f"Analyzing first {len(EN_OFFSETS)} string offsets...")
    print()

    results = []

    with open(STEAM_EN_EXE, 'rb') as steam_en_f, \
         open(ESTORE_EN_EXE, 'rb') as estore_en_f, \
         open(ESTORE_DE_EXE, 'rb') as estore_de_f:

        for i, (offset, length) in enumerate(zip(EN_OFFSETS, STRING_LENGTHS)):
            result = analyze_string(i, offset, length, steam_en_f, estore_en_f, estore_de_f)
            results.append(result)

            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(EN_OFFSETS)} strings...")

    print()
    print("=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    # Categorize results
    unique = [r for r in results if r['status'] == 'unique_match']
    multiple = [r for r in results if r['status'] == 'multiple_matches']
    localized = [r for r in results if r['status'] == 'localized']
    mismatch = [r for r in results if r['status'] == 'en_mismatch']

    print(f"Unique matches:    {len(unique)}")
    print(f"Multiple matches:  {len(multiple)}")
    print(f"Localized (diff):  {len(localized)}")
    print(f"EN mismatch:       {len(mismatch)}")
    print()

    # Print detailed results
    print("DETAILED RESULTS (first 100)")
    print("-" * 80)

    for r in results:
        steam_hex = f"0x{r['steam_en_offset']:06X}"
        estore_hex = f"0x{r['estore_en_offset']:06X}"

        if r['de_offset']:
            de_hex = f"0x{r['de_offset']:06X}"
            delta = r['de_offset'] - r['estore_en_offset']
            delta_str = f"+0x{delta:X}" if delta >= 0 else f"-0x{-delta:X}"
        else:
            de_hex = "NOT FOUND"
            delta_str = "N/A"

        en_text = r['en_text'][:30] if r['en_text'] else ""
        de_text = r['de_text'][:30] if r['de_text'] else ""

        print(f"[{r['index']:3d}] Steam={steam_hex} eStore={estore_hex} DE={de_hex} ({delta_str})")
        print(f"      EN: {en_text!r}")
        print(f"      DE: {de_text!r}")
        print(f"      Status: {r['status']}, Len: {r['length']}")
        if r['status'] == 'multiple_matches':
            print(f"      Matches at: {[f'0x{m:06X}' for m in r['de_matches'][:5]]}")
        print()

    # Generate Python dictionary
    print()
    print("=" * 60)
    print("PYTHON DICTIONARY OUTPUT")
    print("=" * 60)
    print()
    print("DE_OFFSET_MAP = {")
    for r in results:
        if r['de_offset']:
            print(f"    {r['index']}: (0x{r['steam_en_offset']:06X}, 0x{r['estore_en_offset']:06X}, 0x{r['de_offset']:06X}, {r['en_text']!r}, {r['de_text']!r}),")
        else:
            print(f"    {r['index']}: (0x{r['steam_en_offset']:06X}, 0x{r['estore_en_offset']:06X}, None, {r['en_text']!r}, None),  # NOT FOUND")
    print("}")


if __name__ == '__main__':
    main()
