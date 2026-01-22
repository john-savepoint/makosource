#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator v3

Simpler approach:
1. Extract ALL FF-terminated strings from eStore EN menu region (ordered list)
2. Extract ALL FF-terminated strings from eStore DE menu region (ordered list)
3. They're in the same order, so index N in EN = index N in DE
4. For each touphScript Steam offset, find matching EN string, get same-index DE string
5. Write DE bytes to Steam VA

Created: 2026-01-02 16:45 JST
Session: 2e703ab4-4b5e-4772-8894-ba089b4f437c
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from generate_exe_hext import EN_OFFSETS, STRING_LENGTHS, STRING_TYPES

# File paths
STEAM_EN = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
ESTORE_EN = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe"
DE_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

# Skip regions (same as Japanese)
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry (UNICODE)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals
SKIP_REGIONS.update(range(712, 758))   # Chocobo names


def decode_ff7(data):
    """Decode FF7-encoded bytes to readable text."""
    result = []
    for b in data:
        if b == 0xFF: break
        if b == 0x00: result.append(' ')
        elif 0x01 <= b <= 0x9F: result.append(chr(b + 0x20))
        else: result.append(f'[{b:02X}]')
    return ''.join(result)


def extract_all_strings(data, start_offset, end_offset, min_len=2):
    """Extract all FF-terminated strings from a region.

    Returns list of (offset, bytes, decoded_text) tuples.
    """
    strings = []
    pos = start_offset

    while pos < end_offset:
        # Find next 0xFF terminator
        ff_pos = data.find(b'\xff', pos, end_offset)
        if ff_pos == -1:
            break

        # Extract string bytes (including terminator)
        string_bytes = data[pos:ff_pos + 1]

        # Skip if too short
        if len(string_bytes) >= min_len:
            decoded = decode_ff7(string_bytes)
            # Only keep if it has some printable content
            if any(c.isalnum() for c in decoded):
                strings.append((pos, string_bytes, decoded))

        # Move past terminator and any padding
        pos = ff_pos + 1
        while pos < end_offset and data[pos] == 0x00:
            pos += 1

    return strings


def file_offset_to_va(offset):
    """Convert file offset to Virtual Address for HEXT."""
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


def main():
    print("FF7 German HEXT Generator v3")
    print("=" * 60)

    # Load all exe files
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(ESTORE_EN, 'rb') as f:
        estore_data = f.read()
    with open(DE_EXE, 'rb') as f:
        de_data = f.read()

    print(f"Loaded: Steam EN ({len(steam_data):,}), eStore EN ({len(estore_data):,}), DE ({len(de_data):,})")

    # Extract all strings from eStore EN and DE menu regions
    # Menu strings are in the 0x518000-0x5C0000 range for eStore
    EN_START = 0x518000
    EN_END = 0x5C0000
    DE_START = 0x58F000  # DE strings start later due to exe differences
    DE_END = 0x5C0000

    print(f"\nExtracting strings from eStore EN (0x{EN_START:X}-0x{EN_END:X})...")
    en_strings = extract_all_strings(estore_data, EN_START, EN_END)
    print(f"  Found {len(en_strings)} strings")

    print(f"Extracting strings from eStore DE (0x{DE_START:X}-0x{DE_END:X})...")
    de_strings = extract_all_strings(de_data, DE_START, DE_END)
    print(f"  Found {len(de_strings)} strings")

    # Debug: show first 20 string pairs
    print("\nFirst 20 EN/DE string pairs:")
    for i in range(min(20, len(en_strings), len(de_strings))):
        en_off, en_bytes, en_text = en_strings[i]
        de_off, de_bytes, de_text = de_strings[i]
        print(f"  {i:3d}: EN[0x{en_off:06X}] '{en_text[:25]}' -> DE[0x{de_off:06X}] '{de_text[:25]}'")

    # Build mapping: eStore EN offset -> (index, DE bytes)
    en_offset_to_index = {}
    for i, (offset, _, _) in enumerate(en_strings):
        en_offset_to_index[offset] = i

    # Also build content-based lookup for strings (first 8 bytes -> index)
    en_content_to_index = {}
    for i, (_, en_bytes, _) in enumerate(en_strings):
        # Use first 6 bytes as key (before terminator)
        ff_pos = en_bytes.find(b'\xff')
        key_len = min(6, ff_pos if ff_pos != -1 else 6)
        key = en_bytes[:key_len]
        if len(key) >= 3:
            if key not in en_content_to_index:
                en_content_to_index[key] = i

    # Generate patches
    patches = []
    matched = 0
    unmatched = 0
    skipped = 0

    for i, steam_offset in enumerate(EN_OFFSETS):
        if i in SKIP_REGIONS:
            skipped += 1
            continue

        if i >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[i]
        steam_bytes = steam_data[steam_offset:steam_offset + length]

        # Get search key from Steam bytes
        ff_pos = steam_bytes.find(b'\xff')
        key_len = min(6, ff_pos if ff_pos != -1 else 6)
        search_key = steam_bytes[:key_len]

        if len(search_key) < 3:
            unmatched += 1
            continue

        # Find in eStore EN by content
        estore_pos = estore_data.find(search_key, EN_START, EN_END)

        idx = None
        if estore_pos != -1 and estore_pos in en_offset_to_index:
            idx = en_offset_to_index[estore_pos]
        elif search_key in en_content_to_index:
            idx = en_content_to_index[search_key]

        if idx is not None and idx < len(de_strings):
            de_off, de_bytes, de_text = de_strings[idx]

            va = file_offset_to_va(steam_offset)
            en_text = decode_ff7(steam_bytes)

            patches.append({
                'index': i,
                'va': va,
                'steam_offset': steam_offset,
                'length': length,
                'en_text': en_text,
                'de_text': de_text,
                'de_bytes': de_bytes
            })
            matched += 1
        else:
            # Debug unmatched
            if i < 100:  # Only show first 100 unmatched
                en_text = decode_ff7(steam_bytes)
                print(f"  UNMATCHED {i}: '{en_text[:30]}' (key: {search_key.hex()})")
            unmatched += 1

    print(f"\nMatched: {matched}, Unmatched: {unmatched}, Skipped: {skipped}")

    # Write HEXT file
    output_path = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext_v3.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("#\n\n")

        for p in patches:
            # Format bytes with padding to fill slot
            hex_bytes = ' '.join(f'{b:02X}' for b in p['de_bytes'])
            if len(p['de_bytes']) < p['length']:
                padding = ' '.join('00' for _ in range(p['length'] - len(p['de_bytes'])))
                hex_bytes += ' ' + padding

            f.write(f"# {p['index']}: '{p['en_text'][:30]}' -> '{p['de_text'][:30]}'\n")
            f.write(f"{p['va']:06X} = {hex_bytes}\n\n")

    print(f"\nWrote {len(patches)} patches to: {output_path}")


if __name__ == "__main__":
    main()
