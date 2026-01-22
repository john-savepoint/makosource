#!/usr/bin/env python3
"""
Analyze Inter-String Spacing in German Exe
===========================================
Created: 2026-01-03 16:25 JST

Check if German strings follow a consistent spacing/stride pattern
like English does (48 bytes per slot).

If they do, we can extract sequentially and map 1:1 to English indices.
"""

import sys

FF7_GERMAN_DECODE_MAP = {
    0x66: 'Ü', 0x6A: 'ä', 0x7A: 'ö', 0x7E: 'ß', 0x7F: 'ü',
    0x61: 'á', 0x62: 'à', 0x63: 'â', 0x64: 'ã', 0x65: 'å',
    0x67: 'ç', 0x68: 'é', 0x69: 'è', 0x6B: 'ë',
    0x6C: 'í', 0x6D: 'ì', 0x6E: 'î', 0x6F: 'ï',
    0x70: 'ñ', 0x71: 'ó', 0x72: 'ò', 0x73: 'ô', 0x74: 'õ',
    0x76: '°', 0x77: '•', 0x78: '£',
}


def decode_ff7(data: bytes) -> str:
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
    return ''.join(result).strip()


def analyze_sequential_spacing(de_exe_path, start_offset, slot_size, num_slots):
    """
    Read sequential slots and check if strings are laid out with consistent spacing.
    """
    with open(de_exe_path, 'rb') as f:
        f.seek(start_offset)

        strings = []
        for i in range(num_slots):
            offset = start_offset + (i * slot_size)
            f.seek(offset)
            slot_data = f.read(slot_size)
            decoded = decode_ff7(slot_data)
            strings.append((offset, decoded, slot_data))

        return strings


def main():
    de_exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

    print("=" * 80)
    print("ANALYZING GERMAN STRING SPACING PATTERNS")
    print("=" * 80)
    print()

    # Known German string locations from previous analysis:
    # Index 0 (quit dialog): 0x58FBB0
    # Index 3 (Yes): 0x58FC05
    # Index 4 (No): 0x58FC13
    # Index 5 (Window color): 0x5900F0

    # Calculate spacing between known indices
    known_offsets = [
        (0, 0x58FBB0, "Möchten Sie Final"),
        (3, 0x58FC05, "Ja"),
        (4, 0x58FC13, "Nein"),
        (5, 0x5900F0, "Fensterfarbe"),
    ]

    print("Known offsets:")
    for idx, offset, text in known_offsets:
        print(f"  Index {idx:03d}: 0x{offset:06X} - {text}")
    print()

    # Calculate deltas between consecutive indices
    print("Inter-string spacing analysis:")
    print()

    # Between index 0 and 3 (gap of 3 indices)
    delta_0_3 = 0x58FC05 - 0x58FBB0
    bytes_per_slot_0_3 = delta_0_3 / 3
    print(f"Index 0->3: {delta_0_3} bytes / 3 slots = {bytes_per_slot_0_3:.1f} bytes/slot")

    # Between index 3 and 4 (gap of 1)
    delta_3_4 = 0x58FC13 - 0x58FC05
    print(f"Index 3->4: {delta_3_4} bytes / 1 slot = {delta_3_4} bytes/slot")

    # Between index 4 and 5 (gap of 1, but note there's likely padding)
    delta_4_5 = 0x5900F0 - 0x58FC13
    print(f"Index 4->5: {delta_4_5} bytes / 1 slot = {delta_4_5} bytes/slot")
    print()

    # Try reading with different slot sizes
    test_slot_sizes = [14, 20, 48]  # 48 is what English uses

    for slot_size in test_slot_sizes:
        print(f"\nTesting with slot size: {slot_size} bytes")
        print("-" * 60)

        # Start from quit dialog (index 0)
        start = 0x58FBB0
        strings = analyze_sequential_spacing(de_exe_path, start, slot_size, 10)

        for i, (offset, decoded, raw) in enumerate(strings):
            # Show first 20 bytes hex
            hex_preview = raw[:20].hex()
            print(f"  Slot {i:02d} @ 0x{offset:06X}: {decoded[:40]:<40} | {hex_preview}")

    # Load English reference to compare structure
    print()
    print("=" * 80)
    print("ENGLISH REFERENCE STRUCTURE")
    print("=" * 80)

    en_ref_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt"

    # Parse first 10 English entries to see spacing
    with open(en_ref_path, 'r') as f:
        en_offsets = []
        for line in f:
            if line.startswith('[') and ']' in line:
                try:
                    parts = line.split()
                    if len(parts) >= 3:
                        idx = int(line[1:line.index(']')])
                        offset = int(parts[1], 16)
                        length = int(parts[2])
                        en_offsets.append((idx, offset, length))
                        if len(en_offsets) >= 10:
                            break
                except:
                    pass

    print("\nFirst 10 English entries:")
    for idx, offset, length in en_offsets:
        print(f"  Index {idx:03d}: 0x{offset:06X}, Length: {length} bytes")

    print("\nEnglish inter-slot spacing:")
    for i in range(len(en_offsets) - 1):
        idx1, off1, len1 = en_offsets[i]
        idx2, off2, len2 = en_offsets[i+1]
        delta = off2 - off1
        print(f"  Index {idx1} -> {idx2}: {delta} bytes")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()

    # The answer to the user's question
    print("English uses FIXED 48-byte slots (seen in indices 0-2).")
    print("But indices 4->5 have varying spacing, suggesting gaps/regions.")
    print()
    print("For German, we see:")
    print(f"  - Index 3->4 delta: {delta_3_4} bytes (very small - consecutive strings)")
    print(f"  - Index 4->5 delta: {delta_4_5} bytes (large gap - different region)")
    print()
    print("If German strings ARE sequential with small consistent spacing:")
    print("  => We can extract them in order and map 1:1 to English indices")
    print()
    print("If spacing is irregular:")
    print("  => We need the LLM approach (which we're already doing)")


if __name__ == "__main__":
    main()
