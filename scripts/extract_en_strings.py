#!/usr/bin/env python3
"""
FF7 English String Extractor
=============================
Created: 2026-01-02
Purpose: Extract all FF7-encoded menu strings from ff7_en.exe
Context: Part of FF7 Japanese translation project - extracting EN strings
         for comparison and reference.

FF7 Text Encoding:
- byte + 0x20 = ASCII character (for printable chars)
- 0x00 = space
- 0xFF = string terminator
- Values 0x01-0x1F are special control characters

The script scans from 0x518000 to 0x5C0000 in the EN executable
looking for FF-terminated strings that decode to readable text.
"""

import json
import os
from pathlib import Path


def decode_ff7_string(raw_bytes: bytes) -> str:
    """
    Decode FF7 encoded bytes to readable text.

    FF7 encoding:
    - 0x00 = space
    - 0x01-0x1F = control chars (we'll represent as {XX})
    - 0x20-0xDF = byte + 0x20 = ASCII char (so 0x21 = 'A', etc.)
    - But actually: byte value maps directly to ASCII with offset
    - Real mapping: value + 0x20 for letters, 0x00 = space

    Let me re-examine: If 0x00 = space and chars start after that:
    - 0x21 should be 'A' (0x21 + 0x20 = 0x41 = 'A')
    - 0x01 would be '!' (0x01 + 0x20 = 0x21 = '!')
    """
    result = []
    for b in raw_bytes:
        if b == 0xFF:  # Terminator
            break
        elif b == 0x00:  # Space
            result.append(' ')
        elif b >= 0x01 and b <= 0xDF:
            # Add 0x20 to get ASCII value
            ascii_val = b + 0x20
            if 0x20 <= ascii_val <= 0x7E:  # Printable ASCII range
                result.append(chr(ascii_val))
            else:
                # Non-printable, show as hex
                result.append(f'{{0x{b:02X}}}')
        else:
            # Other values (0xE0-0xFE)
            result.append(f'{{0x{b:02X}}}')

    return ''.join(result)


def is_valid_ff7_string(raw_bytes: bytes, min_length: int = 2) -> bool:
    """
    Check if bytes look like a valid FF7 text string.
    Must end with 0xFF and contain mostly printable characters.
    """
    if len(raw_bytes) < min_length:
        return False

    if raw_bytes[-1] != 0xFF:
        return False

    # Check content (excluding terminator)
    content = raw_bytes[:-1]
    if len(content) == 0:
        return False

    printable_count = 0
    for b in content:
        if b == 0x00:  # Space is valid
            printable_count += 1
        elif b >= 0x01 and b <= 0xDF:
            ascii_val = b + 0x20
            if 0x20 <= ascii_val <= 0x7E:  # Printable ASCII
                printable_count += 1

    # At least 60% should be printable
    ratio = printable_count / len(content) if content else 0
    return ratio >= 0.6


def extract_strings_from_exe(exe_path: str, start_offset: int, end_offset: int) -> list:
    """
    Extract all FF-terminated strings from the executable.

    Returns list of tuples: (offset, raw_bytes_hex, decoded_text)
    """
    strings = []

    with open(exe_path, 'rb') as f:
        # Read the entire region
        f.seek(start_offset)
        data = f.read(end_offset - start_offset)

    print(f"Read {len(data)} bytes from 0x{start_offset:X} to 0x{end_offset:X}")

    # Scan for FF-terminated strings
    i = 0
    while i < len(data):
        # Look for 0xFF terminator
        ff_pos = data.find(b'\xFF', i)
        if ff_pos == -1:
            break

        # Try to find the start of the string (work backwards)
        # Look for previous 0xFF or start of region
        start = ff_pos
        while start > i:
            # Check if this could be a valid string character
            b = data[start - 1]
            if b == 0xFF:  # Previous terminator
                break
            elif b == 0x00:  # Space
                start -= 1
            elif b >= 0x01 and b <= 0xDF:
                ascii_val = b + 0x20
                if 0x20 <= ascii_val <= 0x7E:
                    start -= 1
                else:
                    break
            else:
                break

        # Extract the potential string (including terminator)
        raw_bytes = data[start:ff_pos + 1]

        if is_valid_ff7_string(raw_bytes, min_length=3):  # At least 2 chars + terminator
            absolute_offset = start_offset + start
            raw_hex = raw_bytes.hex().upper()
            decoded = decode_ff7_string(raw_bytes)

            # Filter out strings that are just whitespace or control chars
            cleaned = decoded.strip()
            if len(cleaned) >= 1:
                strings.append({
                    "offset": f"0x{absolute_offset:X}",
                    "offset_int": absolute_offset,
                    "raw_bytes": raw_hex,
                    "decoded": decoded,
                    "length": len(raw_bytes) - 1  # Exclude terminator
                })

        i = ff_pos + 1

    return strings


def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe"
    output_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/data/en_strings.json"

    # Scan range
    start_offset = 0x518000
    end_offset = 0x5C0000

    print(f"Extracting FF7 strings from: {exe_path}")
    print(f"Scan range: 0x{start_offset:X} - 0x{end_offset:X}")

    # Check file exists
    if not os.path.exists(exe_path):
        print(f"ERROR: File not found: {exe_path}")
        return

    # Extract strings
    strings = extract_strings_from_exe(exe_path, start_offset, end_offset)

    print(f"\nFound {len(strings)} strings")

    # Sort by offset
    strings.sort(key=lambda x: x["offset_int"])

    # Create output structure
    output = {
        "source_file": exe_path,
        "scan_range": {
            "start": f"0x{start_offset:X}",
            "end": f"0x{end_offset:X}"
        },
        "total_strings": len(strings),
        "extraction_date": "2026-01-02",
        "encoding_notes": "FF7 encoding: byte + 0x20 = ASCII, 0x00 = space, 0xFF = terminator",
        "strings": strings
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Output saved to: {output_path}")

    # Print sample of strings found
    print("\n--- Sample of extracted strings ---")
    for s in strings[:30]:
        print(f"  {s['offset']}: {s['decoded'][:60]}")

    if len(strings) > 30:
        print(f"  ... and {len(strings) - 30} more strings")


if __name__ == "__main__":
    main()
