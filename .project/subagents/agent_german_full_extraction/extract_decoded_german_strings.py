#!/usr/bin/env python3
"""
FF7 German String Extraction with Correct Decoding
===================================================
Created: 2026-01-03 16:15 JST
Session: 629f3c93-f884-439a-91d6-d77e7783bf9c

This script extracts ALL strings from the German FF7 executable using the
VERIFIED character encoding map. Output will be used for Haiku LLM analysis.

The decoder handles:
- Standard ASCII range (0x00-0x5F): byte + 0x20 = character
- German special characters: ä(0x6A), ö(0x7A), ü(0x7F), Ü(0x66), ß(0x7E)
- String terminator: 0xFF
"""

import os
import sys

# =============================================================================
# VERIFIED GERMAN CHARACTER ENCODING
# =============================================================================

FF7_GERMAN_DECODE_MAP = {
    # German special characters (VERIFIED from ff7_de.exe)
    0x66: 'Ü',  # uppercase U-umlaut
    0x6A: 'ä',  # lowercase a-umlaut
    0x7A: 'ö',  # lowercase o-umlaut
    0x7E: 'ß',  # eszett
    0x7F: 'ü',  # lowercase u-umlaut

    # Extended Latin
    0x61: 'á', 0x62: 'à', 0x63: 'â', 0x64: 'ã', 0x65: 'å',
    0x67: 'ç', 0x68: 'é', 0x69: 'è', 0x6B: 'ë',
    0x6C: 'í', 0x6D: 'ì', 0x6E: 'î', 0x6F: 'ï',
    0x70: 'ñ', 0x71: 'ó', 0x72: 'ò', 0x73: 'ô', 0x74: 'õ',
    0x76: '°', 0x77: '•', 0x78: '£',
}


def decode_ff7_german(data: bytes, show_unknown: bool = False) -> str:
    """Decode FF7 German encoded bytes to readable text."""
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
        else:
            if show_unknown:
                result.append(f'[{b:02X}]')
    return ''.join(result)


def extract_strings_from_region(data: bytes, start: int, end: int, min_length: int = 2):
    """
    Extract all FF-terminated strings from a region.
    Returns list of (offset, raw_bytes, decoded_text)
    """
    strings = []
    region = data[start:end]

    current_string = []
    string_start = 0

    for i, b in enumerate(region):
        if b == 0xFF:
            if current_string:
                raw = bytes(current_string)
                decoded = decode_ff7_german(raw)
                # Filter: must have letters and minimum length
                if len(decoded.strip()) >= min_length and any(c.isalpha() for c in decoded):
                    strings.append((start + string_start, raw, decoded))
                current_string = []
            string_start = i + 1
        else:
            if not current_string:
                string_start = i
            current_string.append(b)

    return strings


def main():
    # Paths
    de_exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    output_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction"

    print("=" * 80)
    print("FF7 GERMAN STRING EXTRACTION - CORRECT DECODING")
    print("=" * 80)
    print()

    # Read German exe
    print(f"Reading {de_exe_path}...")
    with open(de_exe_path, 'rb') as f:
        data = f.read()
    print(f"  Size: {len(data):,} bytes")
    print()

    # Define regions to scan (based on previous analysis)
    # Main menu region: 0x58FB00 - 0x5A0000
    # Extended region: 0x580000 - 0x5E0000 (broader scan)
    regions = [
        (0x580000, 0x5E0000, "Full string region"),
    ]

    all_strings = []

    for start, end, desc in regions:
        print(f"Scanning {desc} (0x{start:06X} - 0x{end:06X})...")
        strings = extract_strings_from_region(data, start, end, min_length=2)
        print(f"  Found {len(strings)} strings")
        all_strings.extend(strings)

    # Remove duplicates (same offset)
    seen_offsets = set()
    unique_strings = []
    for offset, raw, decoded in all_strings:
        if offset not in seen_offsets:
            seen_offsets.add(offset)
            unique_strings.append((offset, raw, decoded))

    # Sort by offset
    unique_strings.sort(key=lambda x: x[0])

    print()
    print(f"Total unique strings: {len(unique_strings)}")
    print()

    # Write full dump with correct decoding
    dump_file = os.path.join(output_dir, "de_strings_decoded.txt")
    print(f"Writing {dump_file}...")

    with open(dump_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 German EXE String Dump - CORRECTLY DECODED\n")
        f.write(f"# Source: {de_exe_path}\n")
        f.write(f"# Total strings: {len(unique_strings)}\n")
        f.write("# Encoding: Verified German FF7 character map\n")
        f.write("# Format: OFFSET | HEX_BYTES | DECODED_TEXT\n")
        f.write("# " + "=" * 77 + "\n\n")

        for offset, raw, decoded in unique_strings:
            hex_bytes = raw[:30].hex()
            if len(raw) > 30:
                hex_bytes += "..."
            f.write(f"0x{offset:06X} | {hex_bytes:<65} | {decoded}\n")

    print(f"  Written {len(unique_strings)} strings")

    # Write detailed dump with full hex
    detailed_file = os.path.join(output_dir, "de_strings_decoded_detailed.txt")
    print(f"Writing {detailed_file}...")

    with open(detailed_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 German EXE String Dump - DETAILED\n")
        f.write(f"# Total strings: {len(unique_strings)}\n")
        f.write("# " + "=" * 77 + "\n\n")

        for offset, raw, decoded in unique_strings:
            f.write(f"[0x{offset:06X}]\n")
            f.write(f"  HEX: {raw.hex()}\n")
            f.write(f"  LEN: {len(raw)} bytes\n")
            f.write(f"  TXT: {decoded}\n")
            f.write("\n")

    # Create chunks for Haiku analysis (200 strings per chunk)
    chunks_dir = os.path.join(output_dir, "chunks_decoded")
    os.makedirs(chunks_dir, exist_ok=True)

    print(f"Creating chunks in {chunks_dir}...")

    chunk_size = 200
    num_chunks = (len(unique_strings) + chunk_size - 1) // chunk_size

    for i in range(num_chunks):
        chunk_start = i * chunk_size
        chunk_end = min((i + 1) * chunk_size, len(unique_strings))
        chunk_strings = unique_strings[chunk_start:chunk_end]

        chunk_file = os.path.join(chunks_dir, f"chunk_{i:03d}.txt")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(f"# Chunk {i:03d} - Strings {chunk_start} to {chunk_end-1}\n")
            f.write(f"# Total in chunk: {len(chunk_strings)}\n")
            f.write("# Format: OFFSET | DECODED_TEXT\n\n")

            for offset, raw, decoded in chunk_strings:
                f.write(f"0x{offset:06X} | {decoded}\n")

    print(f"  Created {num_chunks} chunks")

    # Summary statistics
    print()
    print("=" * 80)
    print("EXTRACTION COMPLETE")
    print("=" * 80)
    print()
    print(f"Total strings extracted: {len(unique_strings)}")
    print(f"Chunks created: {num_chunks}")
    print()
    print("Output files:")
    print(f"  - {dump_file}")
    print(f"  - {detailed_file}")
    print(f"  - {chunks_dir}/chunk_XXX.txt")
    print()

    # Show sample of decoded strings
    print("Sample decoded strings (first 20 with German characters):")
    print("-" * 60)
    german_chars = ['ä', 'ö', 'ü', 'Ü', 'ß']
    count = 0
    for offset, raw, decoded in unique_strings:
        if any(c in decoded for c in german_chars):
            print(f"0x{offset:06X}: {decoded[:50]}")
            count += 1
            if count >= 20:
                break


if __name__ == "__main__":
    main()
