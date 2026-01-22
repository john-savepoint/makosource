#!/usr/bin/env python3
"""
Extract ALL FF-Terminated Strings from German Exe
==================================================
Created: 2026-01-05 17:16 JST (Monday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Extract every single 0xFF-terminated string from the menu region,
no filtering, to get a complete picture of what's in there.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ff7_german_decoder import decode_ff7_german

def extract_all_ff_terminated(exe_path: str, start: int, end: int):
    """
    Extract EVERY 0xFF-terminated string from region.
    No filtering at all - keep everything.
    """
    with open(exe_path, 'rb') as f:
        f.seek(start)
        region = f.read(end - start)

    strings = []
    current_bytes = []
    string_start = 0

    for i, byte in enumerate(region):
        if byte == 0xFF:
            # Found terminator - save everything, even empty
            offset = start + string_start
            raw_bytes = bytes(current_bytes)
            decoded = decode_ff7_german(raw_bytes, show_unknown=False)

            # Include byte length and decoded length
            strings.append({
                'offset': offset,
                'raw_bytes': raw_bytes,
                'decoded': decoded,
                'byte_length': len(raw_bytes),
                'decoded_length': len(decoded)
            })

            # Reset for next string
            current_bytes = []
            string_start = i + 1
        else:
            if not current_bytes:
                string_start = i
            current_bytes.append(byte)

    return strings

def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

    # Menu region - wider range to catch everything
    start = 0x58FB00
    end = 0x5A0000

    print("=" * 80)
    print("Extracting ALL FF-Terminated Strings (No Filtering)")
    print("=" * 80)
    print(f"Source: {exe_path}")
    print(f"Region: 0x{start:06X} - 0x{end:06X}")
    print(f"Size: {end - start} bytes ({(end - start) / 1024:.1f} KB)")
    print()

    print("Extracting...")
    strings = extract_all_ff_terminated(exe_path, start, end)

    print(f"Found {len(strings)} FF-terminated strings")
    print()

    # Statistics
    non_empty = [s for s in strings if s['decoded_length'] > 0]
    short_strings = [s for s in strings if 0 < s['decoded_length'] <= 3]
    medium_strings = [s for s in strings if 4 <= s['decoded_length'] <= 20]
    long_strings = [s for s in strings if s['decoded_length'] > 20]

    print("Statistics:")
    print(f"  Total strings:     {len(strings)}")
    print(f"  Non-empty:         {len(non_empty)}")
    print(f"  Short (1-3 chars): {len(short_strings)}")
    print(f"  Medium (4-20):     {len(medium_strings)}")
    print(f"  Long (20+):        {len(long_strings)}")
    print()

    # Show first 100
    print("First 100 strings:")
    print("=" * 80)
    print(f"{'Idx':<6} {'Offset':<10} {'Bytes':<6} {'Len':<5} {'Text':<60}")
    print("-" * 80)

    for i, s in enumerate(strings[:100]):
        text = s['decoded'][:55] if s['decoded'] else "(empty)"
        print(f"{i:<6} 0x{s['offset']:06X} {s['byte_length']:<6} {s['decoded_length']:<5} {text}")

    if len(strings) > 100:
        print(f"\n... and {len(strings) - 100} more")

    # Save to file
    output_dir = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Text format
    txt_file = output_dir / "all_ff_terminated_strings.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("# ALL FF-Terminated Strings from German Exe\n")
        f.write(f"# Source: {exe_path}\n")
        f.write(f"# Region: 0x{start:06X} - 0x{end:06X}\n")
        f.write(f"# Total: {len(strings)}\n")
        f.write("# Format: [INDEX] OFFSET (BYTES:LEN) | TEXT\n")
        f.write("=" * 80 + "\n\n")

        for i, s in enumerate(strings):
            text = s['decoded'] if s['decoded'] else "(empty)"
            f.write(f"[{i:5d}] 0x{s['offset']:06X} ({s['byte_length']:3d}:{s['decoded_length']:3d}) | {text}\n")

    # CSV format
    csv_file = output_dir / "all_ff_terminated_strings.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("index,offset,byte_length,decoded_length,text,hex_bytes\n")
        for i, s in enumerate(strings):
            text = s['decoded'].replace('"', '""')
            hex_bytes = s['raw_bytes'].hex()
            f.write(f"{i},0x{s['offset']:06X},{s['byte_length']},{s['decoded_length']},\"{text}\",{hex_bytes}\n")

    print(f"\nText format saved to: {txt_file}")
    print(f"CSV format saved to:  {csv_file}")

if __name__ == '__main__':
    main()
