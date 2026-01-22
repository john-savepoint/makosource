#!/usr/bin/env python3
"""
Extract German from Known Clean Regions
========================================
Created: 2026-01-05 17:07 JST (Monday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Extract strings from regions we KNOW contain menu text:
- Quit dialog region: 0x58FBB0-0x58FC20
- Config menu region: 0x5900F0-0x590C00
- Main menu region: 0x590C68-0x591500
- Battle/status text: 0x594C00-0x596500
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ff7_german_decoder import decode_ff7_german

def extract_from_region(exe_path: str, start: int, end: int, region_name: str):
    """Extract all strings from a specific region."""
    with open(exe_path, 'rb') as f:
        f.seek(start)
        region = f.read(end - start)

    strings = []
    current_bytes = []
    string_start = 0

    for i, byte in enumerate(region):
        if byte == 0xFF:
            if current_bytes:
                offset = start + string_start
                decoded = decode_ff7_german(bytes(current_bytes), show_unknown=False).strip()
                if decoded and len(decoded) > 0:
                    strings.append((offset, decoded, region_name))
            current_bytes = []
            string_start = i + 1
        else:
            if not current_bytes:
                string_start = i
            current_bytes.append(byte)

    return strings

def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

    # Define known clean regions
    regions = [
        (0x58FBB0, 0x58FC20, "Quit Dialog"),
        (0x5900F0, 0x590C00, "Config Menu"),
        (0x590C68, 0x591500, "Main Menu"),
        (0x591058, 0x5914D0, "Keyboard Labels"),
        (0x594C00, 0x596500, "Battle/Status"),
    ]

    print("=" * 80)
    print("Extracting German Strings from Known Clean Regions")
    print("=" * 80)

    all_strings = []
    for start, end, name in regions:
        print(f"\nRegion: {name} (0x{start:06X} - 0x{end:06X})")
        strings = extract_from_region(exe_path, start, end, name)
        print(f"  Found {len(strings)} strings")
        all_strings.extend(strings)

    print(f"\n{'=' * 80}")
    print(f"Total strings extracted: {len(all_strings)}")
    print(f"{'=' * 80}")

    # Show first 100
    print("\nFirst 100 strings:")
    for i, (offset, text, region) in enumerate(all_strings[:100]):
        print(f"[{i:4d}] 0x{offset:06X} [{region:20s}] | {text[:60]}")

    if len(all_strings) > 100:
        print(f"\n... and {len(all_strings) - 100} more")

    # Save to file
    output_file = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_known_regions.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Strings from Known Clean Regions\n")
        f.write(f"# Source: {exe_path}\n")
        f.write(f"# Total strings: {len(all_strings)}\n")
        f.write("# Format: [INDEX] OFFSET [REGION] | TEXT\n")
        f.write("=" * 80 + "\n\n")

        for i, (offset, text, region) in enumerate(all_strings):
            f.write(f"[{i:4d}] 0x{offset:06X} [{region:20s}] | {text}\n")

    print(f"\nFull list saved to: {output_file}")

    # Save as CSV
    csv_file = output_file.with_suffix('.csv')
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("index,offset,region,text\n")
        for i, (offset, text, region) in enumerate(all_strings):
            escaped_text = text.replace('"', '""')
            f.write(f"{i},0x{offset:06X},{region},\"{escaped_text}\"\n")

    print(f"CSV format saved to: {csv_file}")

if __name__ == '__main__':
    main()
