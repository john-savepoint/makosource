#!/usr/bin/env python3
"""
Analyze German Menu String Structure
=====================================
Created: 2026-01-05 16:30 JST (Monday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Purpose: Examine the German executable's menu string region to find
consistent spacing patterns that would allow sequential extraction.

Key Questions:
1. Is there a consistent offset between consecutive menu strings?
2. Are strings organized sequentially like in English?
3. Can we extract by following 0xFF terminators?
"""

import sys
from pathlib import Path

# Add the scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from ff7_german_decoder import decode_ff7_german, encode_ff7_german

# Known anchor points from previous sessions
KNOWN_ANCHORS = [
    (0x58FBB0, "Möchten Sie Final"),        # Index 0
    (0x58FBE8, "Fantasy VII verlassen und"),  # Index 1
    (0x58FC25, "zu Windows zurückkehren?"),   # Index 2
    (0x58FC48, "Ja"),                       # Index 3
    (0x58FC56, "Nein"),                     # Index 4
    (0x5900EE, "Fensterfarbe"),             # Index 5 (config menu start)
]

def extract_menu_strings_sequential(exe_path: str, start_offset: int, max_strings: int = 100):
    """
    Extract strings sequentially by following 0xFF terminators.

    Returns list of (offset, decoded_text) tuples
    """
    with open(exe_path, 'rb') as f:
        f.seek(start_offset)
        region = f.read(0x20000)  # Read 128KB region

    strings = []
    current_pos = 0
    current_string_start = 0
    current_bytes = []

    for i, byte in enumerate(region):
        if byte == 0xFF:
            # Found terminator
            if current_bytes:
                # Decode the string
                decoded = decode_ff7_german(bytes(current_bytes), show_unknown=False)
                # Filter: must have at least one letter
                if any(c.isalpha() for c in decoded):
                    offset = start_offset + current_string_start
                    strings.append((offset, decoded))

                    if len(strings) >= max_strings:
                        break

            # Reset for next string
            current_bytes = []
            current_string_start = i + 1
        else:
            if not current_bytes:
                current_string_start = i
            current_bytes.append(byte)

    return strings

def analyze_spacing(strings_with_offsets):
    """Analyze spacing between consecutive strings."""
    print("=" * 80)
    print("SPACING ANALYSIS")
    print("=" * 80)

    deltas = []
    for i in range(len(strings_with_offsets) - 1):
        offset1, text1 = strings_with_offsets[i]
        offset2, text2 = strings_with_offsets[i + 1]

        delta = offset2 - offset1
        text1_len = len(text1.encode('utf-8', errors='ignore'))

        deltas.append(delta)

        print(f"[{i:3d}→{i+1:3d}] Δ={delta:5d} bytes | '{text1[:40]}'")

    print("\n" + "=" * 80)
    print("DELTA STATISTICS")
    print("=" * 80)

    from collections import Counter
    delta_counts = Counter(deltas)

    print(f"Total strings analyzed: {len(strings_with_offsets)}")
    print(f"Unique delta values: {len(delta_counts)}")
    print(f"\nMost common deltas:")
    for delta, count in delta_counts.most_common(10):
        print(f"  Δ={delta:5d} bytes: {count:3d} occurrences ({count/len(deltas)*100:.1f}%)")

    print(f"\nDelta range: {min(deltas)} to {max(deltas)} bytes")
    print(f"Average delta: {sum(deltas)/len(deltas):.1f} bytes")

    # Look for regional patterns
    print("\n" + "=" * 80)
    print("REGIONAL PATTERN DETECTION")
    print("=" * 80)

    # Find large gaps (likely region boundaries)
    large_gaps = [(i, deltas[i]) for i in range(len(deltas)) if deltas[i] > 500]

    if large_gaps:
        print(f"Found {len(large_gaps)} large gaps (>500 bytes):")
        for idx, delta in large_gaps:
            offset1, text1 = strings_with_offsets[idx]
            offset2, text2 = strings_with_offsets[idx + 1]
            print(f"  [{idx}→{idx+1}] Gap of {delta} bytes")
            print(f"    Before: 0x{offset1:06X} '{text1[:40]}'")
            print(f"    After:  0x{offset2:06X} '{text2[:40]}'")

def verify_known_anchors(exe_path: str):
    """Verify known anchor points and measure spacing."""
    print("=" * 80)
    print("KNOWN ANCHOR VERIFICATION")
    print("=" * 80)

    with open(exe_path, 'rb') as f:
        for offset, expected_text in KNOWN_ANCHORS:
            f.seek(offset)
            raw = f.read(100)

            # Find terminator
            term_pos = raw.find(b'\xff')
            if term_pos != -1:
                raw = raw[:term_pos]

            decoded = decode_ff7_german(raw, show_unknown=False)

            match = "✓" if expected_text in decoded else "✗"
            print(f"{match} 0x{offset:06X}: {decoded[:50]}")

    # Calculate spacing between known anchors
    print("\nSpacing between known anchors:")
    for i in range(len(KNOWN_ANCHORS) - 1):
        offset1, text1 = KNOWN_ANCHORS[i]
        offset2, text2 = KNOWN_ANCHORS[i + 1]
        delta = offset2 - offset1

        print(f"  [{i}→{i+1}] Δ={delta:5d} bytes: '{text1[:30]}' → '{text2[:30]}'")

def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

    print("FF7 German Menu Structure Analysis")
    print("=" * 80)
    print(f"Analyzing: {exe_path}")
    print()

    # First verify our known anchor points
    verify_known_anchors(exe_path)
    print()

    # Extract strings starting from the first menu string
    print("=" * 80)
    print("SEQUENTIAL EXTRACTION FROM MENU START (0x58FBB0)")
    print("=" * 80)

    strings = extract_menu_strings_sequential(exe_path, 0x58FBB0, max_strings=100)

    print(f"Extracted {len(strings)} strings:")
    for i, (offset, text) in enumerate(strings[:20]):
        print(f"[{i:3d}] 0x{offset:06X}: {text[:60]}")

    if len(strings) > 20:
        print(f"... and {len(strings) - 20} more")

    print()

    # Analyze spacing patterns
    analyze_spacing(strings)

    # Save full extraction to file
    output_file = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/sequential_extraction_analysis.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("FF7 German Sequential String Extraction\n")
        f.write("=" * 80 + "\n")
        f.write(f"Start offset: 0x58FBB0\n")
        f.write(f"Total extracted: {len(strings)}\n")
        f.write("\n")

        for i, (offset, text) in enumerate(strings):
            f.write(f"[{i:3d}] 0x{offset:06X} | {text}\n")

    print(f"\nFull extraction saved to: {output_file}")

if __name__ == '__main__':
    main()
