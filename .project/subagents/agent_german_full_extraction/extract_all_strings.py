#!/usr/bin/env python3
"""
FF7 German String Blind Extractor

Scans the entire menu text region of ff7_de.exe and extracts all valid
FF7-encoded strings with their exact offsets.

Created: 2026-01-03 13:28 JST
Session: 8bc98f0a-abab-49e6-acdd-56dd38e9d149
"""

import sys
import os

# ==============================================================================
# CONFIGURATION
# ==============================================================================
DE_EXE_PATH = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

# Menu text region - scan wider to be safe
START_OFFSET = 0x580000
END_OFFSET   = 0x5E0000

# Minimum length to be considered a "real" string
MIN_LENGTH = 2

# ==============================================================================
# DECODING LOGIC
# ==============================================================================
def decode_byte(val):
    """Decodes a single byte based on FF7 PC German encoding."""
    if val == 0x00: return ' '
    if val == 0xFF: return None  # Terminator - handled separately

    # German Special Characters
    if val == 0x6A: return 'ä'
    if val == 0x7A: return 'ö'
    if val == 0x7E: return 'ß'
    if val == 0x7F: return 'ü'

    # Capital umlauts (if they exist in this encoding)
    if val == 0x4A: return 'Ä'  # 0x4A + 0x20 = 'j', but might be Ä
    if val == 0x5A: return 'Ö'  # 0x5A + 0x20 = 'z', but might be Ö
    if val == 0x5F: return 'Ü'  # 0x5F + 0x20 = DEL, but might be Ü

    # Standard FF7 encoding: stored as (ASCII - 0x20)
    # 'A' (0x41) stored as 0x21, 'a' (0x61) stored as 0x41
    if 0x01 <= val <= 0x5E:
        ascii_val = val + 0x20
        if 32 <= ascii_val <= 126:
            return chr(ascii_val)

    # Extended range for lowercase
    if 0x41 <= val <= 0x79:
        ascii_val = val + 0x20
        if 97 <= ascii_val <= 122:  # a-z
            return chr(ascii_val)

    # Common punctuation/special chars
    if val == 0x0E: return '.'
    if val == 0x0F: return '/'
    if val == 0x1F: return '?'
    if val == 0x01: return '!'
    if val == 0x0C: return ','
    if val == 0x0D: return '-'
    if val == 0x1A: return ':'

    return None  # Invalid character

def is_valid_text_char(val):
    """Check if byte could be part of valid text."""
    if val == 0x00: return True  # Space
    if val == 0xFF: return False  # Terminator
    if decode_byte(val) is not None: return True
    return False

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    if not os.path.exists(DE_EXE_PATH):
        print(f"File not found: {DE_EXE_PATH}")
        return

    print(f"Scanning {DE_EXE_PATH}")
    print(f"Range: 0x{START_OFFSET:X} to 0x{END_OFFSET:X}")
    print(f"Size: {(END_OFFSET - START_OFFSET) / 1024:.1f} KB")
    print()

    with open(DE_EXE_PATH, "rb") as f:
        f.seek(START_OFFSET)
        data = f.read(END_OFFSET - START_OFFSET)

    current_string_bytes = []
    current_string_decoded = []
    current_start_offset = 0
    in_string = False

    extracted_strings = []

    for i, byte in enumerate(data):
        file_offset = START_OFFSET + i

        # Check for FF Terminator
        if byte == 0xFF:
            if in_string and len(current_string_decoded) >= MIN_LENGTH:
                decoded_text = "".join(current_string_decoded)
                # Filter: must have some non-space content
                if decoded_text.strip():
                    raw_hex = " ".join(f"{b:02X}" for b in current_string_bytes)
                    extracted_strings.append({
                        'offset': current_start_offset,
                        'text': decoded_text,
                        'raw': raw_hex,
                        'length': len(current_string_bytes) + 1  # +1 for FF terminator
                    })

            # Reset
            in_string = False
            current_string_bytes = []
            current_string_decoded = []
            continue

        # Check for valid char
        char = decode_byte(byte)

        if char is not None or byte == 0x00:
            if not in_string:
                in_string = True
                current_start_offset = file_offset
            current_string_bytes.append(byte)
            current_string_decoded.append(char if char else ' ')
        else:
            # Binary garbage - check if we had a valid string
            if in_string and len(current_string_decoded) >= MIN_LENGTH:
                decoded_text = "".join(current_string_decoded)
                if decoded_text.strip():
                    raw_hex = " ".join(f"{b:02X}" for b in current_string_bytes)
                    extracted_strings.append({
                        'offset': current_start_offset,
                        'text': decoded_text,
                        'raw': raw_hex,
                        'length': len(current_string_bytes)
                    })

            # Reset
            in_string = False
            current_string_bytes = []
            current_string_decoded = []

    # Sort by offset
    extracted_strings.sort(key=lambda x: x['offset'])

    # OUTPUT - Simple text dump for LLM analysis
    output_file = os.path.join(os.path.dirname(__file__), "de_strings_dump.txt")
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(f"# FF7 German EXE String Dump\n")
        out.write(f"# Range: 0x{START_OFFSET:X} to 0x{END_OFFSET:X}\n")
        out.write(f"# Total strings found: {len(extracted_strings)}\n")
        out.write(f"# Format: OFFSET | TEXT\n")
        out.write("# " + "=" * 80 + "\n\n")

        for s in extracted_strings:
            out.write(f"0x{s['offset']:06X} | {s['text']}\n")

    print(f"Extracted {len(extracted_strings)} strings")
    print(f"Saved to: {output_file}")

    # OUTPUT - Detailed with hex bytes
    output_file_detailed = os.path.join(os.path.dirname(__file__), "de_strings_detailed.txt")
    with open(output_file_detailed, "w", encoding="utf-8") as out:
        out.write(f"# FF7 German EXE String Dump (Detailed)\n")
        out.write(f"# Range: 0x{START_OFFSET:X} to 0x{END_OFFSET:X}\n")
        out.write(f"# Total strings found: {len(extracted_strings)}\n")
        out.write(f"# Format: OFFSET [LENGTH] | TEXT | RAW_HEX\n")
        out.write("# " + "=" * 100 + "\n\n")

        for s in extracted_strings:
            out.write(f"0x{s['offset']:06X} [{s['length']:3d}] | {s['text']} | {s['raw']}\n")

    print(f"Detailed output: {output_file_detailed}")

    # Also create chunks for LLM analysis
    chunk_size = 200  # strings per chunk
    chunk_dir = os.path.join(os.path.dirname(__file__), "chunks")
    os.makedirs(chunk_dir, exist_ok=True)

    for i in range(0, len(extracted_strings), chunk_size):
        chunk = extracted_strings[i:i+chunk_size]
        chunk_file = os.path.join(chunk_dir, f"chunk_{i//chunk_size:02d}.txt")
        with open(chunk_file, "w", encoding="utf-8") as out:
            out.write(f"# Chunk {i//chunk_size}: Strings {i} to {min(i+chunk_size, len(extracted_strings))-1}\n")
            out.write(f"# Offset range: 0x{chunk[0]['offset']:06X} to 0x{chunk[-1]['offset']:06X}\n\n")
            for s in chunk:
                out.write(f"0x{s['offset']:06X} | {s['text']}\n")
        print(f"Created: {chunk_file}")

    return extracted_strings

if __name__ == "__main__":
    main()
