#!/usr/bin/env python3
"""
Extract German Strings - Clean Sequential Extraction
====================================================
Created: 2026-01-05 16:40 JST (Monday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Extract menu strings from German exe, filtering out binary noise
and matching 1:1 with English touphScript indices.

Strategy:
1. Extract strings by following 0xFF terminators
2. Filter out strings that are primarily binary/control chars
3. Map sequentially to English indices
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ff7_german_decoder import decode_ff7_german

def is_mostly_text(decoded_str: str, min_alpha_ratio: float = 0.3) -> bool:
    """
    Check if a string is mostly readable text (not binary noise).

    Args:
        decoded_str: Decoded string to check
        min_alpha_ratio: Minimum ratio of alphabetic characters required

    Returns:
        True if string appears to be text
    """
    if not decoded_str:
        return False

    # Count alphabetic characters
    alpha_count = sum(1 for c in decoded_str if c.isalpha())
    total_chars = len(decoded_str)

    # Must have at least some letters
    if alpha_count == 0:
        return False

    # Check ratio
    ratio = alpha_count / total_chars
    return ratio >= min_alpha_ratio

def extract_clean_sequential(exe_path: str, start_offset: int, max_strings: int = 800):
    """
    Extract strings sequentially, filtering out binary noise.

    Returns list of (offset, decoded_text) tuples
    """
    with open(exe_path, 'rb') as f:
        f.seek(start_offset)
        region = f.read(0x40000)  # Read 256KB region

    strings = []
    current_bytes = []
    string_start = 0

    for i, byte in enumerate(region):
        if byte == 0xFF:
            # Found terminator
            if current_bytes:
                # Decode the string
                decoded = decode_ff7_german(bytes(current_bytes), show_unknown=False)

                # Filter: must be mostly text
                if is_mostly_text(decoded):
                    offset = start_offset + string_start
                    # Clean up leading/trailing spaces
                    cleaned = decoded.strip()
                    if cleaned:  # Must have content after stripping
                        strings.append((offset, cleaned))

                    if len(strings) >= max_strings:
                        break

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

    print("=" * 80)
    print("FF7 German Clean Sequential Extraction")
    print("=" * 80)
    print(f"Source: {exe_path}")
    print(f"Start offset: 0x58FBB0 (first menu string)")
    print()

    # Extract clean strings
    strings = extract_clean_sequential(exe_path, 0x58FBB0, max_strings=800)

    print(f"Extracted {len(strings)} clean strings:")
    print()

    # Show first 80 for verification
    for i, (offset, text) in enumerate(strings[:80]):
        print(f"[{i:3d}] 0x{offset:06X} | {text[:70]}")

    if len(strings) > 80:
        print(f"\n... and {len(strings) - 80} more")

    # Save to file
    output_file = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_sequential.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Clean Sequential String Extraction\n")
        f.write(f"# Source: {exe_path}\n")
        f.write(f"# Start offset: 0x58FBB0\n")
        f.write(f"# Total extracted: {len(strings)}\n")
        f.write("# Format: [INDEX] OFFSET | TEXT\n")
        f.write("=" * 80 + "\n\n")

        for i, (offset, text) in enumerate(strings):
            f.write(f"[{i:3d}] 0x{offset:06X} | {text}\n")

    print(f"\nFull extraction saved to: {output_file}")

if __name__ == '__main__':
    main()
