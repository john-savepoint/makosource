#!/usr/bin/env python3
"""
Analyze FF7 English strings - FIXED column alignment
"""
import re

def determine_encoding(text, hex_bytes, original_type):
    """Determine encoding based on type and hex bytes"""
    # Always ASCII
    if original_type in ['RGB', 'ASCII_FIX']:
        return "ASCII"
    # Always FF7
    if original_type in ['EXCLUDED', 'FF7_CHAR', 'FF7_CTRL']:
        return "FF7"

    # Check bytes for others
    bytes_list = [int(b, 16) for b in hex_bytes.strip().split() if b not in ['00', 'FF']]
    if not bytes_list or not text:
        return "FF7"

    clean_text = text.replace(' ', '').replace('[', '').replace(']', '')
    if len(bytes_list) >= len(clean_text) and len(clean_text) > 0:
        matches = sum(1 for i, char in enumerate(clean_text[:len(bytes_list)])
                     if i < len(bytes_list) and bytes_list[i] == ord(char))
        if matches / len(clean_text) > 0.8:
            return "ASCII"
    return "FF7"

# Read input
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt', 'r') as f:
    lines = f.readlines()

# Process
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index_v2.txt', 'w') as out:
    out.write("# FF7 English Strings by touphScript Index - VERSION 2\n")
    out.write("# Generated: 2026-01-07 21:48:30 JST\n")
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
            # Match: [INDEX] OFFSET LENGTH TYPE | text | hex
            match = re.match(r'(\[\d+\]\s+0x[0-9A-F]+\s+\d+)\s+([A-Z_]+)\s+\|\s+([^|]+)\|\s*(.+)', line)
            if match:
                prefix = match.group(1)
                original_type = match.group(2)
                text = match.group(3).strip()
                hex_part = match.group(4).strip()

                encoding = determine_encoding(text, hex_part, original_type)

                # Fixed width columns: TYPE=12 chars, ENCODING=5 chars
                out.write(f"{prefix} {original_type:12} {encoding:5} | {text} | {hex_part}\n")
            else:
                out.write(line)
        else:
            out.write(line)

print("✓ Created english_strings_by_index_v2.txt with proper column alignment")
