#!/usr/bin/env python3
"""
Convert FF7 English strings to CSV - Simple split approach
"""
import re
import csv

def determine_encoding(text, hex_bytes, original_type):
    """Determine encoding"""
    if original_type in ['RGB', 'ASCII_FIX']:
        return "ASCII"
    if original_type in ['EXCLUDED', 'FF7_CHAR', 'FF7_CTRL']:
        return "FF7"

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

# Process to CSV
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index_v2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Header
    writer.writerow(['INDEX', 'OFFSET_HEX', 'LENGTH', 'TYPE', 'ENCODING', 'TEXT', 'HEX_BYTES'])

    count = 0
    for line in lines:
        if line.startswith('['):
            # Split on pipes
            parts = line.split('|')
            if len(parts) == 3:
                # Part 0: [INDEX] OFFSET LENGTH TYPE
                # Part 1: TEXT
                # Part 2: HEX_BYTES

                prefix = parts[0].strip()
                text = parts[1].strip()
                hex_bytes = parts[2].strip()

                # Parse prefix: [INDEX] OFFSET LENGTH TYPE
                prefix_match = re.match(r'\[(\d+)\]\s+(0x[0-9A-F]+)\s+(\d+)\s+([A-Z_]+)', prefix)
                if prefix_match:
                    index = prefix_match.group(1)
                    offset = prefix_match.group(2)
                    length = prefix_match.group(3)
                    type_val = prefix_match.group(4)

                    encoding = determine_encoding(text, hex_bytes, type_val)

                    writer.writerow([index, offset, length, type_val, encoding, text, hex_bytes])
                    count += 1

print(f"✓ Created english_strings_by_index_v2.csv")
print(f"  Total entries: {count}")
