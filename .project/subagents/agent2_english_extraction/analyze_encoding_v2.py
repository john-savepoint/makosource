#!/usr/bin/env python3
"""
Analyze FF7 English strings to determine ASCII vs FF7 encoding
PROPERLY this time by checking if hex bytes match actual ASCII values
"""
import re

def determine_encoding(text, hex_bytes):
    """
    Check if hex bytes are direct ASCII by comparing to actual text.
    If hex bytes match ASCII values of the text, it's ASCII.
    Otherwise it's FF7 encoding.
    """
    bytes_list = [int(b, 16) for b in hex_bytes.strip().split() if b not in ['00', 'FF']]

    if not bytes_list or not text:
        return "FF7"

    # Remove any spaces from text for comparison
    clean_text = text.replace(' ', '')

    # Check if bytes match ASCII values
    if len(bytes_list) >= len(clean_text):
        matches = 0
        for i, char in enumerate(clean_text[:len(bytes_list)]):
            if i < len(bytes_list) and bytes_list[i] == ord(char):
                matches += 1

        # If >80% of characters match their ASCII values, it's ASCII
        if matches / len(clean_text) > 0.8:
            return "ASCII"

    return "FF7"

# Read input file
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt', 'r') as f:
    lines = f.readlines()

# Process and write output
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index_v2.txt', 'w') as out:
    # Update header
    out.write("# FF7 English Strings by touphScript Index - VERSION 2\n")
    out.write("# Generated: 2026-01-07 21:44:00 JST\n")
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
            # Parse the line
            match = re.match(r'(\[\d+\]\s+0x[0-9A-F]+\s+\d+)\s+(DEF|RGB|EXCLUDED)\s+\|\s+([^|]+)\|\s*(.+)', line)
            if match:
                prefix = match.group(1)
                old_type = match.group(2)
                text = match.group(3).strip()
                hex_part = match.group(4).strip()

                # Determine encoding
                if old_type == "EXCLUDED":
                    encoding = "FF7"
                elif old_type == "RGB":
                    encoding = "ASCII"
                else:  # DEF
                    encoding = determine_encoding(text, hex_part)

                # Write new format with aligned columns
                out.write(f"{prefix} {old_type:8} {encoding:5} | {text} | {hex_part}\n")
            else:
                out.write(line)
        else:
            out.write(line)

print("Created english_strings_by_index_v2.txt with encoding detection")
print("\nSample check:")
print("'Do you want to quit' with bytes '24 4F 00 59...' should be FF7 (24 != ASCII 'D')")
print("'ESCAPE' with bytes '45 53 43 41 50 45' should be ASCII (45 == ASCII 'E')")
