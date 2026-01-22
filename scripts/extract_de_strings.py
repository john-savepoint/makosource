#!/usr/bin/env python3
"""
FF7 German String Extractor
Created: 2026-01-02
Context: Extract all FF7-encoded German strings from eStore DE executable
         for localization/translation analysis.

FF7 Encoding (confirmed):
- Regular characters: byte + 0x20 = ASCII char
- 0x00 = space
- 0xFF = string terminator
- Special German characters (raw bytes, NOT +0x20):
  - 0x7A = ö (replaces 'z' position - lowercase z uses different byte)
  - 0x7F = ü (replaces DEL position)
  - 0x6A = ä (replaces 'j' position - lowercase j uses different byte)
  - 0x7E = ß (replaces '~' position)

Note: The German font replaced certain character positions with umlauts.
This means some letters like 'z' and 'j' have alternate encodings.
"""

import json
import sys
from pathlib import Path


def decode_ff7_char(byte_val):
    """
    Decode a single FF7-encoded byte to a character.

    FF7 encoding: byte + 0x20 = ASCII character
    Special cases for German umlauts which replace certain positions.
    """
    if byte_val == 0x00:
        return ' '  # Space
    elif byte_val == 0xFF:
        return None  # Terminator

    # German umlauts - these are at specific byte positions
    # The German font replaced these character slots with umlauts
    elif byte_val == 0x7A:
        return 'ö'  # Replaces 'z' slot (0x7A + 0x20 = 0x9A, not standard ASCII)
    elif byte_val == 0x7F:
        return 'ü'  # At DEL position
    elif byte_val == 0x6A:
        return 'ä'  # Replaces 'j' slot
    elif byte_val == 0x7E:
        return 'ß'  # Eszett, replaces '~' slot
    else:
        # Standard FF7 encoding: byte + 0x20 = ASCII
        decoded = byte_val + 0x20
        if 0x20 <= decoded <= 0x7E:
            return chr(decoded)
        else:
            # Non-printable - return None to skip
            return None


def decode_ff7_string(data):
    """
    Decode a sequence of bytes using FF7 encoding until 0xFF terminator.
    Returns (decoded_string, bytes_consumed, has_invalid).
    """
    chars = []
    consumed = 0
    invalid_count = 0

    for byte_val in data:
        consumed += 1
        if byte_val == 0xFF:
            break
        char = decode_ff7_char(byte_val)
        if char is not None:
            chars.append(char)
        else:
            invalid_count += 1
            # If too many invalid chars, this is probably not a string
            if invalid_count > 3:
                return ''.join(chars), consumed, True

    return ''.join(chars), consumed, invalid_count > len(chars) // 3 if chars else True


def is_valid_menu_string(decoded):
    """
    Check if a decoded string looks like valid menu text.
    Filters out garbage/binary data.
    """
    if not decoded:
        return False

    # Strip and check length
    stripped = decoded.strip()
    if len(stripped) < 2:
        return False

    # Must have alphabetic characters
    alpha_count = sum(1 for c in stripped if c.isalpha())
    if alpha_count < 2:
        return False

    # Check for too many special chars
    special_chars = sum(1 for c in stripped if not c.isalnum() and c not in ' .,!?:-öüäß()/')
    if special_chars > len(stripped) // 3:
        return False

    # Should be mostly readable
    readable = sum(1 for c in stripped if c.isalnum() or c in ' .,!?:-öüäß()/')
    if len(stripped) > 0 and readable < len(stripped) * 0.7:
        return False

    return True


def find_ff_terminated_strings(data, base_offset, min_length=2):
    """
    Scan binary data for FF-terminated strings.
    """
    results = []
    pos = 0

    while pos < len(data) - 1:
        # Skip padding bytes
        if data[pos] == 0x00:
            pos += 1
            continue

        if data[pos] == 0xFF:
            pos += 1
            continue

        # Try to decode a string from here
        remaining = data[pos:]

        # Find the next 0xFF terminator
        term_pos = -1
        for i, b in enumerate(remaining):
            if b == 0xFF:
                term_pos = i
                break

        if term_pos == -1 or term_pos > 300:  # No terminator within reasonable distance
            pos += 1
            continue

        if term_pos < min_length:
            pos += 1
            continue

        # Extract and decode
        string_bytes = remaining[:term_pos + 1]  # Include terminator
        decoded, _, has_invalid = decode_ff7_string(string_bytes)

        if has_invalid:
            pos += 1
            continue

        decoded_stripped = decoded.strip()
        if len(decoded_stripped) >= min_length and is_valid_menu_string(decoded_stripped):
            absolute_offset = base_offset + pos
            results.append({
                'offset': f'0x{absolute_offset:06X}',
                'offset_dec': absolute_offset,
                'raw_bytes': string_bytes.hex().upper(),
                'decoded': decoded_stripped,
                'length': len(decoded_stripped)
            })
            pos += term_pos + 1
        else:
            pos += 1

    return results


def extract_ff7_strings(exe_path, start_offset, end_offset):
    """
    Extract all FF7-encoded strings from a region of the executable.
    """
    with open(exe_path, 'rb') as f:
        f.seek(start_offset)
        data = f.read(end_offset - start_offset)

    print(f"Read {len(data)} bytes from 0x{start_offset:06X} to 0x{end_offset:06X}")

    # Find all FF-terminated strings
    strings = find_ff_terminated_strings(data, start_offset)

    # Remove duplicates based on offset
    seen_offsets = set()
    unique_strings = []
    for s in strings:
        if s['offset'] not in seen_offsets:
            seen_offsets.add(s['offset'])
            unique_strings.append(s)

    # Sort by offset
    unique_strings.sort(key=lambda x: x['offset_dec'])

    return unique_strings


def main():
    exe_path = Path('/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe')
    output_path = Path('/home/johnzealanddoyle/projects/ff7OG_japanese/data/de_strings.json')

    if not exe_path.exists():
        print(f"Error: File not found: {exe_path}", file=sys.stderr)
        sys.exit(1)

    # Region to scan: 0x58F000 to 0x5C0000
    start_offset = 0x58F000
    end_offset = 0x5C0000

    print(f"Extracting German strings from FF7 DE executable")
    print(f"File: {exe_path}")
    print(f"Scan range: 0x{start_offset:06X} to 0x{end_offset:06X}")
    print()

    strings = extract_ff7_strings(exe_path, start_offset, end_offset)

    print(f"Found {len(strings)} valid strings")

    # Create output data structure
    output_data = {
        'metadata': {
            'source_file': str(exe_path),
            'scan_start': f'0x{start_offset:06X}',
            'scan_end': f'0x{end_offset:06X}',
            'total_strings': len(strings),
            'extraction_date': '2026-01-02',
            'encoding_notes': {
                'description': 'FF7 custom text encoding',
                'standard': 'byte + 0x20 = ASCII char',
                'space': '0x00',
                'terminator': '0xFF',
                'german_umlauts': {
                    '0x6A': 'ä (replaces j slot)',
                    '0x7A': 'ö (replaces z slot)',
                    '0x7E': 'ß (replaces ~ slot)',
                    '0x7F': 'ü (at DEL slot)'
                },
                'notes': [
                    'German font replaced certain character positions with umlauts',
                    'Letters j and z may have alternate encodings in German version'
                ]
            }
        },
        'strings': strings
    }

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nOutput saved to: {output_path}")

    # Print all found strings for review
    print("\n" + "=" * 80)
    print("EXTRACTED GERMAN STRINGS")
    print("=" * 80)

    for s in strings:
        print(f"{s['offset']}: {s['decoded']}")

    print("\n" + "=" * 80)
    print(f"Total: {len(strings)} strings extracted")


if __name__ == '__main__':
    main()
