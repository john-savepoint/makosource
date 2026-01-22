#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator v7

The German eStore exe is 12KB larger than English - NO FIXED DELTA is possible.
We must use INDEX-BASED matching:

1. Extract ALL FF-terminated strings from eStore EN (0x518F70 - 0x5C0000)
2. Extract ALL FF-terminated strings from eStore DE (0x58FB90 - 0x5C0000)
3. They are in the SAME ORDER - match by index
4. For each touphScript offset, find matching eStore EN string by content
5. Use same index to get DE string
6. Write DE bytes (truncated to fit) to Steam VA

Created: 2026-01-02 17:30 JST
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

# Skip regions
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry (UNICODE)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals
SKIP_REGIONS.update(range(712, 758))   # Chocobo names
SKIP_REGIONS.update(range(77, 214))    # Keyboard region


def decode_ff7(data):
    """Decode FF7-encoded bytes to readable text."""
    result = []
    for b in data:
        if b == 0xFF: break
        if b == 0x00: result.append(' ')
        elif 0x01 <= b <= 0x9F: result.append(chr(b + 0x20))
        else: result.append('[%02X]' % b)
    return ''.join(result)


def extract_all_strings(data, start, end):
    """Extract ALL FF-terminated strings from a region.

    Returns list of (offset, bytes) tuples, in order of appearance.
    """
    strings = []
    pos = start

    while pos < end:
        # Find next FF terminator
        ff = data.find(b'\xff', pos, min(pos + 200, end))
        if ff == -1:
            # No terminator found in next 200 bytes - skip ahead
            pos += 1
            continue

        string_bytes = data[pos:ff + 1]

        # Keep if reasonable length and has content
        if 2 <= len(string_bytes) <= 150:
            # Check if it looks like text (at least some alphanumeric)
            text = decode_ff7(string_bytes)
            if any(c.isalnum() for c in text):
                strings.append((pos, string_bytes))

        # Move past terminator and padding
        pos = ff + 1
        while pos < end and data[pos] == 0x00:
            pos += 1

    return strings


def file_offset_to_va(offset):
    """Convert file offset to Virtual Address for HEXT."""
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


def main():
    print("FF7 German HEXT Generator v7")
    print("=" * 60)

    # Load all exe files
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(ESTORE_EN, 'rb') as f:
        estore_en_data = f.read()
    with open(ESTORE_DE, 'rb') as f:
        estore_de_data = f.read()

    print(f"Loaded: Steam EN ({len(steam_data):,}), eStore EN ({len(estore_en_data):,}), DE ({len(estore_de_data):,})")

    # Extract ALL strings from both eStore exes
    # These ranges cover the menu string regions
    EN_START = 0x518F70  # Start of quit dialog
    EN_END = 0x5C0000
    DE_START = 0x58FB90  # Start of quit dialog in DE
    DE_END = 0x5C0000

    print(f"\nExtracting ALL strings from eStore EN (0x{EN_START:X}-0x{EN_END:X})...")
    estore_en_strings = extract_all_strings(estore_en_data, EN_START, EN_END)
    print(f"  Found {len(estore_en_strings)} strings")

    print(f"Extracting ALL strings from eStore DE (0x{DE_START:X}-0x{DE_END:X})...")
    estore_de_strings = extract_all_strings(estore_de_data, DE_START, DE_END)
    print(f"  Found {len(estore_de_strings)} strings")

    # Build lookup: eStore EN offset -> index
    estore_en_offset_to_idx = {}
    for i, (offset, _) in enumerate(estore_en_strings):
        estore_en_offset_to_idx[offset] = i

    # Also build content-based lookup (first N bytes -> list of indices)
    estore_en_content_to_indices = {}
    for i, (_, bytes_data) in enumerate(estore_en_strings):
        ff_pos = bytes_data.find(b'\xff')
        key_len = min(8, ff_pos if ff_pos != -1 else 8)
        key = bytes_data[:key_len]
        if len(key) >= 3:
            if key not in estore_en_content_to_indices:
                estore_en_content_to_indices[key] = []
            estore_en_content_to_indices[key].append(i)

    # Verify alignment (first 20 strings)
    print("\nVerifying EN/DE alignment (first 20):")
    for i in range(min(20, len(estore_en_strings), len(estore_de_strings))):
        en_off, en_bytes = estore_en_strings[i]
        de_off, de_bytes = estore_de_strings[i]
        en_text = decode_ff7(en_bytes)[:20]
        de_text = decode_ff7(de_bytes)[:20]
        print(f"  {i:3d}: '{en_text}' -> '{de_text}'")

    # Generate patches
    patches = []
    matched = 0
    unmatched = 0
    skipped = 0
    unmatched_list = []

    # Delta from Steam to eStore EN
    STEAM_TO_ESTORE = 0xC00

    for touph_idx, steam_offset in enumerate(EN_OFFSETS):
        if touph_idx in SKIP_REGIONS:
            skipped += 1
            continue

        if touph_idx >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[touph_idx]
        steam_bytes = steam_data[steam_offset:steam_offset + length]
        en_text = decode_ff7(steam_bytes)

        # Calculate expected eStore EN offset
        estore_en_offset = steam_offset + STEAM_TO_ESTORE

        # Method 1: Direct offset match
        idx = estore_en_offset_to_idx.get(estore_en_offset)

        # Method 2: Content-based match if direct failed
        if idx is None:
            ff_pos = steam_bytes.find(b'\xff')
            key_len = min(8, ff_pos if ff_pos != -1 else 8)
            key = steam_bytes[:key_len]

            if len(key) >= 3 and key in estore_en_content_to_indices:
                # Take first match
                idx = estore_en_content_to_indices[key][0]

        # Get DE string if found
        if idx is not None and idx < len(estore_de_strings):
            de_off, de_bytes = estore_de_strings[idx]
            de_text = decode_ff7(de_bytes)

            patches.append({
                'touph_idx': touph_idx,
                'steam_offset': steam_offset,
                'length': length,
                'en_text': en_text,
                'de_text': de_text,
                'de_bytes': de_bytes,
            })
            matched += 1
        else:
            unmatched += 1
            if len(unmatched_list) < 50:
                unmatched_list.append((touph_idx, en_text[:30]))

    print(f"\n{'='*60}")
    print(f"Results: Matched={matched}, Unmatched={unmatched}, Skipped={skipped}")

    if unmatched_list:
        print(f"\nFirst {len(unmatched_list)} unmatched:")
        for idx, text in unmatched_list[:20]:
            print(f"  {idx:3d}: '{text}'")

    # Write HEXT file
    output_path = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext_v7.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# Method: Index-based matching from eStore EN/DE ordered string lists\n")
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
