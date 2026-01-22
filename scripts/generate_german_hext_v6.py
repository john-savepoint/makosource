#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator v6

CORRECT APPROACH:
1. eStore EN and DE have strings in the SAME ORDER but at different offsets
2. Extract ordered string lists from both eStore exes
3. Steam EN offset + 0xC00 = eStore EN offset
4. Find which INDEX that eStore EN string is at
5. Get DE string at same INDEX
6. Write DE bytes to Steam VA (with proper truncation)

Created: 2026-01-02 17:10 JST
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
ESTORE_DE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

# Fixed delta: Steam EN + 0xC00 = eStore EN
STEAM_TO_ESTORE_DELTA = 0xC00

# Skip regions (same as Japanese)
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry (UNICODE)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals
SKIP_REGIONS.update(range(712, 758))   # Chocobo names

# Keyboard region - skip for now
SKIP_REGIONS.update(range(77, 214))


def decode_ff7(data):
    """Decode FF7-encoded bytes to readable text."""
    result = []
    for b in data:
        if b == 0xFF: break
        if b == 0x00: result.append(' ')
        elif 0x01 <= b <= 0x9F: result.append(chr(b + 0x20))
        else: result.append('[%02X]' % b)
    return ''.join(result)


def extract_strings_from_offset(data, start, max_count=1000):
    """Extract FF-terminated strings sequentially from a starting offset.

    Returns list of (offset, bytes) tuples.
    """
    strings = []
    pos = start

    while len(strings) < max_count and pos < len(data) - 2:
        # Find next FF terminator
        ff = data.find(b'\xff', pos, pos + 300)
        if ff == -1:
            break

        string_bytes = data[pos:ff + 1]

        # Only keep if it has content
        if len(string_bytes) >= 2:
            strings.append((pos, string_bytes))

        # Move past terminator and padding
        pos = ff + 1
        while pos < len(data) and data[pos] == 0x00:
            pos += 1

    return strings


def file_offset_to_va(offset):
    """Convert file offset to Virtual Address for HEXT."""
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


def main():
    print("FF7 German HEXT Generator v6")
    print("=" * 60)

    # Load all exe files
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(ESTORE_EN, 'rb') as f:
        estore_en_data = f.read()
    with open(ESTORE_DE, 'rb') as f:
        estore_de_data = f.read()

    print(f"Loaded: Steam EN ({len(steam_data):,}), eStore EN ({len(estore_en_data):,}), DE ({len(estore_de_data):,})")

    # Extract strings from eStore EN and DE starting from known anchors
    # These are the menu string regions
    ESTORE_EN_START = 0x5194A8  # "Window Color"
    ESTORE_DE_START = 0x5900F0  # "Fensterfarbe"

    print(f"\nExtracting eStore EN strings from 0x{ESTORE_EN_START:X}...")
    estore_en_strings = extract_strings_from_offset(estore_en_data, ESTORE_EN_START, 800)
    print(f"  Found {len(estore_en_strings)} strings")

    print(f"Extracting eStore DE strings from 0x{ESTORE_DE_START:X}...")
    estore_de_strings = extract_strings_from_offset(estore_de_data, ESTORE_DE_START, 800)
    print(f"  Found {len(estore_de_strings)} strings")

    # Build lookup: eStore EN offset -> index
    estore_en_offset_to_idx = {}
    for i, (offset, _) in enumerate(estore_en_strings):
        estore_en_offset_to_idx[offset] = i

    # Verify alignment with first 10
    print("\nVerifying EN/DE alignment:")
    for i in range(min(10, len(estore_en_strings), len(estore_de_strings))):
        en_off, en_bytes = estore_en_strings[i]
        de_off, de_bytes = estore_de_strings[i]
        en_text = decode_ff7(en_bytes)[:20]
        de_text = decode_ff7(de_bytes)[:20]
        print(f"  {i:2d}: '{en_text}' -> '{de_text}'")

    # Generate patches
    patches = []
    matched = 0
    unmatched = 0
    skipped = 0

    for touph_idx, steam_offset in enumerate(EN_OFFSETS):
        if touph_idx in SKIP_REGIONS:
            skipped += 1
            continue

        if touph_idx >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[touph_idx]

        # Calculate eStore EN offset
        estore_en_offset = steam_offset + STEAM_TO_ESTORE_DELTA

        # Find which index this is in eStore EN
        idx = estore_en_offset_to_idx.get(estore_en_offset)

        if idx is not None and idx < len(estore_de_strings):
            # Get DE string at same index
            de_off, de_bytes = estore_de_strings[idx]
            de_text = decode_ff7(de_bytes)

            # Get EN text for comment
            steam_bytes = steam_data[steam_offset:steam_offset + length]
            en_text = decode_ff7(steam_bytes)

            patches.append({
                'touph_idx': touph_idx,
                'steam_offset': steam_offset,
                'length': length,
                'en_text': en_text,
                'de_text': de_text,
                'de_bytes': de_bytes,
                'estore_idx': idx
            })
            matched += 1
        else:
            # Try to find by content match as fallback
            steam_bytes = steam_data[steam_offset:steam_offset + length]
            en_text = decode_ff7(steam_bytes)

            # Search in eStore EN for this content
            ff_pos = steam_bytes.find(b'\xff')
            search_key = steam_bytes[:ff_pos] if ff_pos != -1 else steam_bytes[:8]

            if len(search_key) >= 3:
                found_pos = estore_en_data.find(search_key, ESTORE_EN_START, ESTORE_EN_START + 0x80000)
                if found_pos != -1 and found_pos in estore_en_offset_to_idx:
                    idx = estore_en_offset_to_idx[found_pos]
                    if idx < len(estore_de_strings):
                        de_off, de_bytes = estore_de_strings[idx]
                        de_text = decode_ff7(de_bytes)

                        patches.append({
                            'touph_idx': touph_idx,
                            'steam_offset': steam_offset,
                            'length': length,
                            'en_text': en_text,
                            'de_text': de_text,
                            'de_bytes': de_bytes,
                            'estore_idx': idx
                        })
                        matched += 1
                        continue

            unmatched += 1

    print(f"\n{'='*60}")
    print(f"Results: Matched={matched}, Unmatched={unmatched}, Skipped={skipped}")

    # Write HEXT file
    output_path = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext_v6.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# Method: Index-based mapping from eStore EN/DE ordered string lists\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("#\n\n")

        for p in patches:
            de_bytes = p['de_bytes']
            slot_len = p['length']
            va = file_offset_to_va(p['steam_offset'])

            # CRITICAL: Truncate if DE string is longer than slot
            truncated = False
            if len(de_bytes) > slot_len:
                de_bytes = de_bytes[:slot_len - 1] + b'\xff'
                truncated = True

            # Format DE bytes with padding if shorter
            hex_bytes = ' '.join('%02X' % b for b in de_bytes)
            if len(de_bytes) < slot_len:
                padding = ' '.join('00' for _ in range(slot_len - len(de_bytes)))
                hex_bytes += ' ' + padding

            comment = f"# {p['touph_idx']}: '{p['en_text'][:25]}' -> '{p['de_text'][:25]}'"
            if truncated:
                comment += " [TRUNCATED]"
            f.write(comment + "\n")
            f.write(f"{va:06X} = {hex_bytes}\n\n")

    print(f"\nWrote {len(patches)} patches to: {output_path}")


if __name__ == "__main__":
    main()
