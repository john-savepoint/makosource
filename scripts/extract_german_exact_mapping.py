#!/usr/bin/env python3
"""
Extract German Strings - Exact 1:1 Mapping to English Indices
==============================================================
Created: 2026-01-05 16:45 JST (Monday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Extract ALL strings from German exe following 0xFF terminators,
then map 1:1 to English touphScript indices.

Key insight: German and English have same string order, just different
offsets due to length differences. We extract sequentially and map
by position, NOT by semantic matching.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ff7_german_decoder import decode_ff7_german

def extract_all_sequential(exe_path: str, start_offset: int, end_offset: int):
    """
    Extract ALL strings sequentially by following 0xFF terminators.
    No filtering - keep everything to maintain exact alignment.

    Returns list of (offset, decoded_text, raw_bytes) tuples
    """
    with open(exe_path, 'rb') as f:
        f.seek(start_offset)
        region = f.read(end_offset - start_offset)

    strings = []
    current_bytes = []
    string_start = 0

    for i, byte in enumerate(region):
        if byte == 0xFF:
            # Found terminator - save string even if empty
            offset = start_offset + string_start
            decoded = decode_ff7_german(bytes(current_bytes), show_unknown=False).strip()

            # Keep ALL strings including empty/garbage to maintain alignment
            strings.append((offset, decoded, bytes(current_bytes)))

            # Reset for next string
            current_bytes = []
            string_start = i + 1
        else:
            if not current_bytes:
                string_start = i
            current_bytes.append(byte)

    return strings

def load_english_indices(filepath: str):
    """Load English touphScript indices and offsets."""
    indices = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Parse format: [INDEX] OFFSET LENGTH TYPE | TEXT | HEX
            if line.startswith('['):
                try:
                    parts = line.split('|')
                    header = parts[0].strip()

                    # Extract index and offset
                    header_parts = header.split()
                    index_str = header_parts[0][1:-1]  # Remove brackets
                    offset_str = header_parts[1]

                    index = int(index_str)
                    en_offset = int(offset_str, 16)
                    en_text = parts[1].strip() if len(parts) > 1 else ""

                    indices.append((index, en_offset, en_text))
                except:
                    continue

    return indices

def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    english_ref = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt"

    print("=" * 80)
    print("FF7 German 1:1 Mapping to English Indices")
    print("=" * 80)
    print()

    # Load English reference
    print("Loading English reference...")
    english_indices = load_english_indices(english_ref)
    print(f"Loaded {len(english_indices)} English indices")
    print()

    # Extract German strings
    print("Extracting German strings from 0x58FBB0 to 0x5A0000...")
    german_strings = extract_all_sequential(exe_path, 0x58FBB0, 0x5A0000)
    print(f"Extracted {len(german_strings)} German strings")
    print()

    # Map German to English indices
    print("=" * 80)
    print("MAPPING VERIFICATION (first 80 indices)")
    print("=" * 80)
    print(f"{'Idx':<5} {'EN Offset':<12} {'DE Offset':<12} {'English Text':<35} | {'German Text':<35}")
    print("=" * 80)

    mappings = []
    for i in range(min(80, len(english_indices), len(german_strings))):
        en_idx, en_offset, en_text = english_indices[i]
        de_offset, de_text, de_raw = german_strings[i]

        # Sanity check: index should match position
        if en_idx != i:
            print(f"WARNING: Index mismatch at position {i}: expected {i}, got {en_idx}")

        print(f"{i:<5} 0x{en_offset:08X}  0x{de_offset:06X}  {en_text:<35} | {de_text:<35}")

        mappings.append({
            'index': i,
            'en_offset': en_offset,
            'de_offset': de_offset,
            'en_text': en_text,
            'de_text': de_text,
            'de_raw': de_raw
        })

    # Save full mapping
    output_file = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_english_1to1_mapping.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("index,en_offset,de_offset,en_text,de_text\n")

        for mapping in mappings:
            # Escape quotes in text
            en_text = mapping['en_text'].replace('"', '""')
            de_text = mapping['de_text'].replace('"', '""')

            f.write(f"{mapping['index']},0x{mapping['en_offset']:08X},0x{mapping['de_offset']:06X},\"{en_text}\",\"{de_text}\"\n")

    print(f"\nFull mapping saved to: {output_file}")
    print(f"Total mappings: {len(mappings)}")

if __name__ == '__main__':
    main()
