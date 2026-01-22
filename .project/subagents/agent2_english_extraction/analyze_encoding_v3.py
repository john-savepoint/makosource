#!/usr/bin/env python3
"""
Analyze FF7 English strings to determine ASCII vs FF7 encoding - ALL TYPES
"""
import re

def determine_encoding(text, hex_bytes, original_type):
    """
    Determine encoding based on type and hex bytes
    """
    # Types that are always ASCII
    if original_type in ['RGB', 'ASCII_FIX']:
        return "ASCII"

    # Types that are always FF7
    if original_type in ['EXCLUDED', 'FF7_CHAR', 'FF7_CTRL']:
        return "FF7"

    # For other types (DEF, DEF_FIXED, FFPADDED, ZEROTERM), check the bytes
    bytes_list = [int(b, 16) for b in hex_bytes.strip().split() if b not in ['00', 'FF']]

    if not bytes_list or not text:
        return "FF7"

    # Remove spaces from text
    clean_text = text.replace(' ', '').replace('[', '').replace(']', '')

    if len(bytes_list) >= len(clean_text):
        matches = 0
        for i, char in enumerate(clean_text[:len(bytes_list)]):
            if i < len(bytes_list) and bytes_list[i] == ord(char):
                matches += 1

        # If >80% match ASCII, it's ASCII
        if len(clean_text) > 0 and matches / len(clean_text) > 0.8:
            return "ASCII"

    return "FF7"

# Read input file
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt', 'r') as f:
    lines = f.readlines()

# Process and write output
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index_v2.txt', 'w') as out:
    # Update header
    out.write("# FF7 English Strings by touphScript Index - VERSION 2\n")
    out.write("# Generated: 2026-01-07 21:47:30 JST\n")
    out.write("# Session: d55a34dc-1851-44b8-98a5-782ad55fb17c\n")
    out.write("# Source: /mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe\n")
    out.write("# Total strings: 767\n")
    out.write("#\n")
    out.write("# Format: [INDEX] [OFFSET_HEX] [LENGTH] [TYPE] [ENCODING] | DECODED_EN_TEXT | RAW_HEX_BYTES\n")
    out.write("# ENCODING: ASCII = direct ASCII bytes, FF7 = FF7 character encoding\n")
    out.write("# ====================================================================================================\n")
    out.write("\n")

    skip_header = True
    for line in lines:
        if skip_header:
            if line.startswith('['):
                skip_header = False
            else:
                continue

        if line.startswith('['):
            # Parse with flexible TYPE matching
            match = re.match(r'(\[\d+\]\s+0x[0-9A-F]+\s+\d+)\s+([A-Z_]+)\s+\|\s+([^|]+)\|\s*(.+)', line)
            if match:
                prefix = match.group(1)
                original_type = match.group(2)
                text = match.group(3).strip()
                hex_part = match.group(4).strip()

                # Determine encoding
                encoding = determine_encoding(text, hex_part, original_type)

                # Write with aligned columns
                out.write(f"{prefix} {original_type:12} {encoding:5} | {text} | {hex_part}\n")
            else:
                # Couldn't parse - write as-is
                out.write(line)
        else:
            out.write(line)

print("Created english_strings_by_index_v2.txt with ALL encoding types detected")
