#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator v2

Generates HEXT patches by:
1. Finding anchor strings in both eStore EN and DE exes
2. Extracting consecutive strings from each anchor
3. Matching Steam offsets to eStore positions by content
4. Writing German bytes to Steam VAs

Created: 2026-01-01 20:50 JST
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
    result = []
    for b in data:
        if b == 0xFF: break
        if b == 0x00: result.append(' ')
        elif 0x01 <= b <= 0x9F: result.append(chr(b + 0x20))
        else: result.append(f'[{b:02X}]')
    return ''.join(result)


def extract_strings_from_position(data, start_pos, max_count=300):
    strings = []
    pos = start_pos
    while len(strings) < max_count and pos < len(data) - 2:
        next_ff = data.find(b'\xff', pos)
        if next_ff == -1 or next_ff > pos + 200:
            break
        string_bytes = data[pos:next_ff + 1]
        if len(string_bytes) >= 2:
            strings.append((pos, string_bytes))
        pos = next_ff + 1
        while pos < len(data) and data[pos] == 0x00:
            pos += 1
    return strings


def file_offset_to_va(offset):
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


def build_region_mapping(estore_data, de_data, en_anchor_bytes, de_anchor_bytes, search_start, search_end, max_strings=300):
    """Build eStore offset -> DE bytes mapping for a region."""

    # Search broader range for both
    en_start = estore_data.find(en_anchor_bytes, 0x510000, 0x5C0000)
    de_start = de_data.find(de_anchor_bytes, 0x580000, 0x5C0000)

    if en_start == -1 or de_start == -1:
        return {}

    en_strings = extract_strings_from_position(estore_data, en_start, max_strings)
    de_strings = extract_strings_from_position(de_data, de_start, max_strings)

    mapping = {}
    for i in range(min(len(en_strings), len(de_strings))):
        en_off, en_bytes = en_strings[i]
        de_off, de_bytes = de_strings[i]
        mapping[en_off] = (de_off, de_bytes)

    return mapping


def main():
    print("FF7 German HEXT Generator v2")
    print("=" * 60)

    # Load all exe files
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(ESTORE_EN, 'rb') as f:
        estore_data = f.read()
    with open(DE_EXE, 'rb') as f:
        de_data = f.read()

    print(f"Loaded: Steam EN ({len(steam_data):,}), eStore EN ({len(estore_data):,}), DE ({len(de_data):,})")

    # Define anchor pairs for each major region
    # Format: (EN anchor text, DE anchor text, search_start, search_end)
    anchors = [
        # Quit dialog (indices 0-4)
        (b"Yes", b"Ja", 0x580000, 0x5A0000),
        # Config menu region (indices 5-76)
        (b"Window color", b"Fensterfarbe", 0x510000, 0x5A0000),
        # Battle menu
        (b"Attack", b"Angriff", 0x510000, 0x5A0000),
        # Status screen
        (b"Sadness", b"Trauer", 0x510000, 0x5A0000),
        # Equipment
        (b"Weapon", b"Waffe", 0x510000, 0x5A0000),
        # Battle messages (indices 250+)
        (b"Minimum", b"Minimum", 0x590000, 0x5A0000),
        # Item menu (indices 420+)
        (b"Arrange", b"Ordnen", 0x590000, 0x5A0000),
        # Shop (indices 590+)
        (b"Welcome!", b"Willkommen!", 0x590000, 0x5A0000),
        (b"Buy", b"Kaufen", 0x590000, 0x5A0000),
        # Save slots (indices 650+)
        (b"Save", b"Speichern", 0x590000, 0x5A0000),
        # Pause message (index 214)
        (b"Pause", b"Pause", 0x580000, 0x5A0000),
        # Materia (index 400+)
        (b"EXP.UP", b"EXP.UP", 0x590000, 0x5A0000),
        # Limit break screen
        (b"Limit", b"Limit", 0x580000, 0x5A0000),
        # Status ailments
        (b"Poison", b"Gift", 0x580000, 0x5A0000),
        # Main menu
        (b"Status", b"Status", 0x580000, 0x5A0000),
        (b"Equip", b"Ausr", 0x580000, 0x5A0000),
        (b"Materia", b"Materia", 0x580000, 0x5A0000),
        (b"Magic", b"Magie", 0x580000, 0x5A0000),
        # Equipment slots
        (b"Accessory", b"Accessoire", 0x580000, 0x5A0000),
    ]

    # Build combined mapping from all anchors
    estore_to_de = {}

    for en_text, de_text, start, end in anchors:
        en_bytes = bytes([c - 0x20 for c in en_text])
        de_bytes = bytes([c - 0x20 for c in de_text])

        mapping = build_region_mapping(estore_data, de_data, en_bytes, de_bytes, start, end)
        if mapping:
            print(f"  Anchor '{en_text.decode()}' -> '{de_text.decode()}': {len(mapping)} strings")
            estore_to_de.update(mapping)

    print(f"\nTotal mapped strings: {len(estore_to_de)}")

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

        # Find search pattern (first 8 non-FF bytes)
        ff_pos = steam_bytes.find(b'\xff')
        search_len = min(8, ff_pos if ff_pos != -1 else 8)
        search_bytes = steam_bytes[:search_len]

        if len(search_bytes) < 2:
            unmatched += 1
            continue

        # Find in eStore
        estore_pos = estore_data.find(search_bytes, 0x510000, 0x5C0000)

        if estore_pos != -1 and estore_pos in estore_to_de:
            de_off, de_bytes = estore_to_de[estore_pos]

            va = file_offset_to_va(steam_offset)
            en_text = decode_ff7(steam_bytes)
            de_text = decode_ff7(de_bytes)

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
            unmatched += 1

    print(f"\nMatched: {matched}, Unmatched: {unmatched}, Skipped: {skipped}")

    # Write HEXT file
    output_path = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext_v2.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("#\n\n")

        for p in patches:
            # Format bytes with padding
            hex_bytes = ' '.join(f'{b:02X}' for b in p['de_bytes'])
            if len(p['de_bytes']) < p['length']:
                padding = ' '.join('00' for _ in range(p['length'] - len(p['de_bytes'])))
                hex_bytes += ' ' + padding

            f.write(f"# {p['index']}: '{p['en_text'][:30]}' -> '{p['de_text'][:30]}'\n")
            f.write(f"{p['va']:06X} = {hex_bytes}\n\n")

    print(f"\nWrote {len(patches)} patches to: {output_path}")


if __name__ == "__main__":
    main()
