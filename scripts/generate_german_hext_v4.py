#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator v4

Strategy:
1. Scan eStore EN exe for FF-terminated strings starting from known menu region
2. Scan eStore DE exe for FF-terminated strings starting from known menu region
3. Both have strings in SAME ORDER - index N in EN = index N in DE
4. For each touphScript offset in Steam exe, find the matching string by content
5. Look up the corresponding DE string and write to Steam VA

Key insight: eStore EN and DE have same string ORDER but different slot sizes/offsets.
We extract both ordered lists, then match Steam strings to eStore EN to find DE equivalent.

Created: 2026-01-02 17:05 JST
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


def extract_strings_ordered(data, start_offset, end_offset):
    """Extract FF-terminated strings in order from a region.

    Returns list of (offset, raw_bytes, decoded_text) tuples.
    Handles variable-length strings with padding.
    """
    strings = []
    pos = start_offset

    while pos < end_offset:
        # Find next FF terminator
        ff_pos = data.find(b'\xff', pos, min(pos + 300, end_offset))
        if ff_pos == -1:
            break

        # Extract string (including terminator)
        string_bytes = data[pos:ff_pos + 1]
        decoded = decode_ff7(string_bytes)

        # Only keep if it looks like text (has alphanumeric content)
        if len(string_bytes) >= 2 and any(c.isalnum() for c in decoded):
            strings.append((pos, string_bytes, decoded))

        # Move past terminator
        pos = ff_pos + 1

        # Skip padding (0x00 bytes)
        while pos < end_offset and data[pos] == 0x00:
            pos += 1

    return strings


def file_offset_to_va(offset):
    """Convert file offset to Virtual Address for HEXT."""
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


def main():
    print("FF7 German HEXT Generator v4")
    print("=" * 60)

    # Load all exe files
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(ESTORE_EN, 'rb') as f:
        estore_data = f.read()
    with open(DE_EXE, 'rb') as f:
        de_data = f.read()

    print(f"Loaded: Steam EN ({len(steam_data):,}), eStore EN ({len(estore_data):,}), DE ({len(de_data):,})")

    # Known starting points for menu string region
    # These were found by searching for "Window Color" / "Fensterfarbe"
    EN_MENU_START = 0x5194A8  # "Window Color" in eStore EN
    EN_MENU_END = 0x5C0000
    DE_MENU_START = 0x5900F0  # "Fensterfarbe" in eStore DE
    DE_MENU_END = 0x5C0000

    print(f"\nExtracting eStore EN strings from 0x{EN_MENU_START:X}...")
    en_strings = extract_strings_ordered(estore_data, EN_MENU_START, EN_MENU_END)
    print(f"  Found {len(en_strings)} strings")

    print(f"Extracting eStore DE strings from 0x{DE_MENU_START:X}...")
    de_strings = extract_strings_ordered(de_data, DE_MENU_START, DE_MENU_END)
    print(f"  Found {len(de_strings)} strings")

    # Show first 20 pairs to verify alignment
    print("\nFirst 20 EN/DE pairs (verifying alignment):")
    for i in range(min(20, len(en_strings), len(de_strings))):
        en_off, en_bytes, en_text = en_strings[i]
        de_off, de_bytes, de_text = de_strings[i]
        en_short = en_text[:20].ljust(20)
        de_short = de_text[:20].ljust(20)
        print(f"  {i:3d}: '{en_short}' -> '{de_short}'")

    # Build lookup: eStore EN offset -> index
    en_offset_to_idx = {offset: i for i, (offset, _, _) in enumerate(en_strings)}

    # Build content lookup: first N bytes -> index (for matching Steam to eStore)
    en_content_to_idx = {}
    for i, (_, en_bytes, _) in enumerate(en_strings):
        # Use content before FF as key
        ff_pos = en_bytes.find(b'\xff')
        content = en_bytes[:ff_pos] if ff_pos != -1 else en_bytes
        if len(content) >= 3:
            # Store first occurrence only
            if content not in en_content_to_idx:
                en_content_to_idx[content] = i

    # Generate patches
    patches = []
    matched = 0
    unmatched = 0
    skipped = 0
    unmatched_list = []

    for touph_idx, steam_offset in enumerate(EN_OFFSETS):
        if touph_idx in SKIP_REGIONS:
            skipped += 1
            continue

        if touph_idx >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[touph_idx]
        steam_bytes = steam_data[steam_offset:steam_offset + length]

        # Extract content (before FF terminator)
        ff_pos = steam_bytes.find(b'\xff')
        content = steam_bytes[:ff_pos] if ff_pos != -1 else steam_bytes.rstrip(b'\x00')

        if len(content) < 2:
            unmatched += 1
            continue

        # Try to find in eStore EN by content
        idx = None

        # First try exact match
        if content in en_content_to_idx:
            idx = en_content_to_idx[content]
        else:
            # Try finding in eStore data directly
            estore_pos = estore_data.find(content, EN_MENU_START, EN_MENU_END)
            if estore_pos != -1:
                # Find which string this belongs to
                for i, (off, _, _) in enumerate(en_strings):
                    if off <= estore_pos < off + 100:  # Within reasonable range
                        idx = i
                        break

        if idx is not None and idx < len(de_strings):
            de_off, de_bytes, de_text = de_strings[idx]
            en_text = decode_ff7(steam_bytes)

            va = file_offset_to_va(steam_offset)

            patches.append({
                'touph_index': touph_idx,
                'va': va,
                'steam_offset': steam_offset,
                'length': length,
                'en_text': en_text,
                'de_text': de_text,
                'de_bytes': de_bytes,
                'estore_idx': idx
            })
            matched += 1
        else:
            unmatched += 1
            if len(unmatched_list) < 50:
                en_text = decode_ff7(steam_bytes)
                unmatched_list.append((touph_idx, en_text, content.hex()))

    print(f"\n{'='*60}")
    print(f"Results: Matched={matched}, Unmatched={unmatched}, Skipped={skipped}")

    if unmatched_list:
        print(f"\nFirst {len(unmatched_list)} unmatched strings:")
        for idx, text, hexkey in unmatched_list:
            print(f"  {idx:3d}: '{text[:30]}'")

    # Write HEXT file
    output_path = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext_v4.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("#\n\n")

        for p in patches:
            # Format DE bytes with padding to fill Steam slot
            hex_bytes = ' '.join(f'{b:02X}' for b in p['de_bytes'])
            if len(p['de_bytes']) < p['length']:
                padding = ' '.join('00' for _ in range(p['length'] - len(p['de_bytes'])))
                hex_bytes += ' ' + padding

            f.write(f"# {p['touph_index']}: '{p['en_text'][:25]}' -> '{p['de_text'][:25]}'\n")
            f.write(f"{p['va']:06X} = {hex_bytes}\n\n")

    print(f"\nWrote {len(patches)} patches to: {output_path}")


if __name__ == "__main__":
    main()
