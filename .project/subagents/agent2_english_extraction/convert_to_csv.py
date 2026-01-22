#!/usr/bin/env python3
"""
Convert FF7 English strings to CSV with encoding detection
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

    for line in lines:
        if line.startswith('['):
            match = re.match(r'\[(\d+)\]\s+(0x[0-9A-F]+)\s+(\d+)\s+([A-Z_]+)\s+\|\s+([^|]+)\|\s*(.+)', line)
            if match:
                index = match.group(1)
                offset = match.group(2)
                length = match.group(3)
                type_val = match.group(4)
                text = match.group(5).strip()
                hex_bytes = match.group(6).strip()

                encoding = determine_encoding(text, hex_bytes, type_val)

                writer.writerow([index, offset, length, type_val, encoding, text, hex_bytes])

print("✓ Created english_strings_by_index_v2.csv")
print(f"  Columns: INDEX, OFFSET_HEX, LENGTH, TYPE, ENCODING, TEXT, HEX_BYTES")
