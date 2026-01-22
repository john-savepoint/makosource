#!/usr/bin/env python3
"""
Extract German Strings - Clean Offsets (No Padding)
====================================================
Created: 2026-01-05 18:42 JST (Monday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Extract strings with offsets pointing to where TEXT starts (after padding),
and strip empty strings.

Two-pass approach:
1. Strip leading 0x00 padding, adjust offset to text start
2. Remove empty strings entirely
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ff7_german_decoder import decode_ff7_german

def extract_clean_with_correct_offsets(exe_path: str, start: int, end: int):
    """
    Extract strings with offsets pointing to actual text start.

    Returns list of (text_offset, decoded_text, total_bytes) tuples
    Only includes non-empty strings.
    """
    with open(exe_path, 'rb') as f:
        f.seek(start)
        region = f.read(end - start)

    strings = []
    current_bytes = []
    string_start = 0

    for i, byte in enumerate(region):
        if byte == 0xFF:
            # Found terminator
            if current_bytes:
                # Count leading 0x00 bytes (padding)
                padding_count = 0
                for b in current_bytes:
                    if b == 0x00:
                        padding_count += 1
                    else:
                        break  # Hit first non-0x00 byte

                # Decode the full string (including padding)
                decoded_full = decode_ff7_german(bytes(current_bytes), show_unknown=False)
                decoded_stripped = decoded_full.strip()

                # Only include non-empty strings
                if decoded_stripped:
                    # Offset points to where text ACTUALLY starts (after padding)
                    text_offset = start + string_start + padding_count
                    total_bytes = len(current_bytes)

                    strings.append({
                        'offset': text_offset,
                        'text': decoded_stripped,
                        'total_bytes': total_bytes,
                        'padding_bytes': padding_count,
                        'text_bytes': total_bytes - padding_count
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
    start = 0x58FBB0  # Correct start (first menu string)
    end = 0x5A0000

    print("=" * 80)
    print("Extracting German Strings - Clean Offsets & No Empties")
    print("=" * 80)
    print(f"Source: {exe_path}")
    print(f"Region: 0x{start:06X} - 0x{end:06X}")
    print()

    print("Extracting...")
    strings = extract_clean_with_correct_offsets(exe_path, start, end)

    print(f"Found {len(strings)} non-empty strings (after removing empties)")
    print()

    # Statistics
    padded = [s for s in strings if s['padding_bytes'] > 0]
    no_padding = [s for s in strings if s['padding_bytes'] == 0]

    print("Statistics:")
    print(f"  Total non-empty strings: {len(strings)}")
    print(f"  Strings with padding:    {len(padded)} ({len(padded)/len(strings)*100:.1f}%)")
    print(f"  Strings without padding: {len(no_padding)} ({len(no_padding)/len(strings)*100:.1f}%)")
    print()

    # Show first 50
    print("First 50 strings (offset = text start, not padding start):")
    print("=" * 80)
    print(f"{'Idx':<6} {'Offset':<10} {'Pad':<5} {'Text':<60}")
    print("-" * 80)

    for i, s in enumerate(strings[:50]):
        pad_info = f"{s['padding_bytes']:3d}" if s['padding_bytes'] > 0 else "  -"
        text_preview = s['text'][:55]
        print(f"{i:<6} 0x{s['offset']:06X} {pad_info:<5} {text_preview}")

    if len(strings) > 50:
        print(f"\n... and {len(strings) - 50} more")

    # Save to files
    output_dir = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Text format
    txt_file = output_dir / "german_strings_clean_offsets.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("# German Strings - Clean Offsets (Text Start, No Empties)\n")
        f.write(f"# Source: {exe_path}\n")
        f.write(f"# Region: 0x{start:06X} - 0x{end:06X}\n")
        f.write(f"# Total: {len(strings)} non-empty strings\n")
        f.write("# Offset points to where TEXT starts (after padding)\n")
        f.write("# Format: [INDEX] OFFSET (PAD_BYTES) | TEXT\n")
        f.write("=" * 80 + "\n\n")

        for i, s in enumerate(strings):
            pad_info = f"(pad:{s['padding_bytes']:3d})" if s['padding_bytes'] > 0 else "(no pad) "
            f.write(f"[{i:5d}] 0x{s['offset']:06X} {pad_info} | {s['text']}\n")

    # CSV format
    csv_file = output_dir / "german_strings_clean_offsets.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("index,offset,text,padding_bytes,text_bytes,total_bytes\n")
        for i, s in enumerate(strings):
            text_escaped = s['text'].replace('"', '""')
            f.write(f"{i},0x{s['offset']:06X},\"{text_escaped}\",{s['padding_bytes']},{s['text_bytes']},{s['total_bytes']}\n")

    print(f"\nText format saved to: {txt_file}")
    print(f"CSV format saved to:  {csv_file}")

    # Verification examples
    print("\n" + "=" * 80)
    print("VERIFICATION - First 5 strings:")
    print("=" * 80)

    for i in range(min(5, len(strings))):
        s = strings[i]
        print(f"\n[{i}] Offset: 0x{s['offset']:06X}")
        print(f"    Text: '{s['text']}'")
        print(f"    Padding: {s['padding_bytes']} bytes")

        # Verify by reading from exe at that offset
        with open(exe_path, 'rb') as f:
            f.seek(s['offset'])
            verify_bytes = f.read(s['text_bytes'])
            verify_decoded = decode_ff7_german(verify_bytes, show_unknown=False).strip()

            match = "✓" if verify_decoded == s['text'] else "✗"
            print(f"    Verify: {match} '{verify_decoded}'")

if __name__ == '__main__':
    main()
