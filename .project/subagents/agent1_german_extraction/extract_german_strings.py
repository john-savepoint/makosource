#!/usr/bin/env python3
"""
FF7 German String Extractor
===========================
Created: 2026-01-02
Session: 68888497-9f38-454c-8ee5-3953fa6c7625

Purpose: Extract ALL German text strings from ff7_de.exe for the FF7OG Japanese project.
This script handles FF7's custom text encoding including German umlauts.

FF7 Text Encoding:
- ASCII characters stored as (ASCII_value - 0x20)
- Space = 0x00
- String terminator = 0xFF
- German special chars: ä=0x6A, ö=0x7A, ü=0x7F, ß=0x7E
"""

import os
import sys
from collections import defaultdict

# FF7 Character decoding table
# Standard ASCII range is shifted by 0x20
# Special German characters have specific mappings
FF7_CHAR_MAP = {}

# Build standard ASCII mapping (0x20-0x7E range becomes 0x00-0x5E)
for i in range(0x20, 0x7F):
    ff7_byte = i - 0x20
    FF7_CHAR_MAP[ff7_byte] = chr(i)

# Override with German special characters
GERMAN_SPECIAL_CHARS = {
    0x6A: 'ä',
    0x6B: 'Ä',
    0x7A: 'ö',
    0x7B: 'Ö',
    0x7F: 'ü',
    0x80: 'Ü',
    0x7E: 'ß',
    # Additional FF7 control/special codes
    0xE0: '{CLOUD}',
    0xE1: '{BARRET}',
    0xE2: '{TIFA}',
    0xE3: '{AERITH}',
    0xE4: '{RED XIII}',
    0xE5: '{YUFFIE}',
    0xE6: '{CAIT SITH}',
    0xE7: '{VINCENT}',
    0xE8: '{CID}',
    0xEA: '{PARTY1}',
    0xEB: '{PARTY2}',
    0xEC: '{PARTY3}',
    0xFE: '{NEWLINE}',
}

# Merge special chars into main map
FF7_CHAR_MAP.update(GERMAN_SPECIAL_CHARS)


def decode_ff7_byte(byte_val):
    """Decode a single FF7 byte to its character representation."""
    if byte_val in FF7_CHAR_MAP:
        return FF7_CHAR_MAP[byte_val]
    elif byte_val == 0xFF:
        return None  # String terminator
    elif byte_val >= 0x5F and byte_val < 0x6A:
        # Extended printable range - map to some chars
        return f'[0x{byte_val:02X}]'
    else:
        return f'[0x{byte_val:02X}]'


def decode_ff7_string(data):
    """Decode a sequence of FF7 bytes into a string."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        char = decode_ff7_byte(b)
        if char:
            result.append(char)
    return ''.join(result)


def is_valid_ff7_string(data, min_length=2):
    """Check if a byte sequence looks like a valid FF7 string."""
    if len(data) < min_length:
        return False

    printable_count = 0
    total_count = 0

    for b in data:
        if b == 0xFF:
            break
        total_count += 1
        # Check if byte maps to a printable character
        if b in FF7_CHAR_MAP or b == 0x00:  # 0x00 is space
            char = FF7_CHAR_MAP.get(b, ' ')
            if isinstance(char, str) and (char.isprintable() or char == ' ' or char.startswith('{')):
                printable_count += 1

    if total_count == 0:
        return False

    # Require at least 70% printable characters
    return (printable_count / total_count) >= 0.7


def extract_strings_from_region(data, start_offset, min_length=3):
    """Extract all strings from a binary data region."""
    strings = []
    i = 0

    while i < len(data):
        # Look for potential string start
        # A string typically starts with a printable character
        if data[i] in FF7_CHAR_MAP or data[i] == 0x00:
            # Find the end of the string (0xFF terminator)
            end = i
            while end < len(data) and data[end] != 0xFF:
                end += 1

            if end < len(data):  # Found terminator
                string_data = data[i:end]

                if len(string_data) >= min_length and is_valid_ff7_string(string_data):
                    decoded = decode_ff7_string(string_data)

                    # Filter out strings that are just control codes or garbage
                    clean_decoded = decoded.replace('[', '').replace(']', '')
                    if len(clean_decoded) >= min_length:
                        strings.append({
                            'offset': start_offset + i,
                            'length': len(string_data) + 1,  # +1 for terminator
                            'raw_hex': ' '.join(f'{b:02X}' for b in string_data) + ' FF',
                            'decoded': decoded
                        })

                i = end + 1
            else:
                i += 1
        else:
            i += 1

    return strings


def scan_for_string_tables(data, start_offset):
    """Scan for potential string table structures."""
    # FF7 often has strings stored consecutively, separated by 0xFF
    tables = []
    current_table_start = None
    consecutive_strings = 0

    i = 0
    while i < len(data) - 4:
        # Look for string terminator followed by potential new string
        if data[i] == 0xFF:
            next_bytes = data[i+1:i+5] if i+5 < len(data) else data[i+1:]

            # Check if next bytes look like a string start
            if len(next_bytes) > 0 and (next_bytes[0] in FF7_CHAR_MAP or next_bytes[0] == 0x00):
                if current_table_start is None:
                    current_table_start = i + 1
                    consecutive_strings = 1
                else:
                    consecutive_strings += 1
            else:
                if consecutive_strings >= 3:
                    tables.append({
                        'start': start_offset + current_table_start,
                        'end': start_offset + i,
                        'string_count': consecutive_strings
                    })
                current_table_start = None
                consecutive_strings = 0
        i += 1

    return tables


def categorize_string(decoded_text):
    """Attempt to categorize a string based on its content."""
    text_lower = decoded_text.lower()

    # Config/Settings
    if any(word in text_lower for word in ['config', 'einstellung', 'option', 'speicher', 'laden', 'save', 'load']):
        return 'Config/Save'

    # Battle
    if any(word in text_lower for word in ['angriff', 'attack', 'magie', 'magic', 'verteidigung', 'defense', 'hp', 'mp', 'limit', 'flucht', 'escape']):
        return 'Battle'

    # Items/Equipment
    if any(word in text_lower for word in ['trank', 'potion', 'elixir', 'waffe', 'weapon', 'rüstung', 'armor', 'zubehör', 'accessory', 'materia']):
        return 'Items/Equipment'

    # Status
    if any(word in text_lower for word in ['gift', 'poison', 'schlaf', 'sleep', 'verwirr', 'confuse', 'stumm', 'silence', 'blind', 'tod', 'death']):
        return 'Status Effects'

    # Shop
    if any(word in text_lower for word in ['kaufen', 'buy', 'verkauf', 'sell', 'gil', 'preis', 'price']):
        return 'Shop'

    # Character names
    if any(word in text_lower for word in ['cloud', 'barret', 'tifa', 'aerith', 'red', 'yuffie', 'cait', 'vincent', 'cid']):
        return 'Character Names'

    # Gold Saucer
    if any(word in text_lower for word in ['saucer', 'gp', 'spiel', 'game', 'arena', 'chocobo']):
        return 'Gold Saucer'

    # Menu
    if any(word in text_lower for word in ['menü', 'menu', 'status', 'item', 'equip', 'materia', 'phs']):
        return 'Menu'

    return 'Uncategorized'


def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    output_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent1_german_extraction"

    print(f"Reading {exe_path}...")

    with open(exe_path, 'rb') as f:
        exe_data = f.read()

    print(f"File size: {len(exe_data):,} bytes")

    # Define search regions (based on known FF7 string locations)
    regions = [
        (0x580000, 0x5C0000, 'Main Menu Strings'),
        (0x400000, 0x480000, 'Early Region'),
        (0x4E0000, 0x580000, 'Mid Region'),
        (0x5C0000, 0x700000, 'Extended Region'),
    ]

    all_strings = []
    region_stats = {}

    for start, end, name in regions:
        if start >= len(exe_data):
            print(f"Region {name} (0x{start:X}-0x{end:X}) is beyond file size, skipping")
            continue

        actual_end = min(end, len(exe_data))
        print(f"\nScanning region: {name} (0x{start:X}-0x{actual_end:X})...")

        region_data = exe_data[start:actual_end]
        strings = extract_strings_from_region(region_data, start, min_length=2)

        region_stats[name] = {
            'start': start,
            'end': actual_end,
            'strings_found': len(strings)
        }

        print(f"  Found {len(strings)} strings")
        all_strings.extend(strings)

    # Remove duplicates based on offset
    seen_offsets = set()
    unique_strings = []
    for s in all_strings:
        if s['offset'] not in seen_offsets:
            seen_offsets.add(s['offset'])
            unique_strings.append(s)

    # Sort by offset
    unique_strings.sort(key=lambda x: x['offset'])

    print(f"\n{'='*60}")
    print(f"Total unique strings extracted: {len(unique_strings)}")

    # Write complete strings file
    complete_path = os.path.join(output_dir, 'german_strings_complete.txt')
    with open(complete_path, 'w', encoding='utf-8') as f:
        f.write(f"# FF7 German String Extraction\n")
        f.write(f"# Extracted from: ff7_de.exe\n")
        f.write(f"# Total strings: {len(unique_strings)}\n")
        f.write(f"# Format: [OFFSET_HEX] [LENGTH] [RAW_HEX_BYTES] | DECODED_TEXT\n")
        f.write(f"{'='*80}\n\n")

        for s in unique_strings:
            f.write(f"[0x{s['offset']:06X}] [{s['length']:3d}] {s['raw_hex'][:60]:<60} | {s['decoded']}\n")

    print(f"Written: {complete_path}")

    # Categorize strings
    categories = defaultdict(list)
    for s in unique_strings:
        cat = categorize_string(s['decoded'])
        categories[cat].append(s)

    # Write categorized strings file
    cat_path = os.path.join(output_dir, 'german_strings_by_category.txt')
    with open(cat_path, 'w', encoding='utf-8') as f:
        f.write(f"# FF7 German Strings by Category\n")
        f.write(f"# Total strings: {len(unique_strings)}\n")
        f.write(f"{'='*80}\n\n")

        for cat_name in sorted(categories.keys()):
            strings_in_cat = categories[cat_name]
            f.write(f"\n{'='*60}\n")
            f.write(f"## {cat_name} ({len(strings_in_cat)} strings)\n")
            f.write(f"{'='*60}\n\n")

            for s in strings_in_cat:
                f.write(f"[0x{s['offset']:06X}] {s['decoded']}\n")

    print(f"Written: {cat_path}")

    # Print category summary
    print("\nCategory Summary:")
    for cat_name in sorted(categories.keys()):
        print(f"  {cat_name}: {len(categories[cat_name])} strings")

    # Print sample strings from each category
    print("\nSample strings from each category:")
    for cat_name in sorted(categories.keys()):
        strings_in_cat = categories[cat_name]
        print(f"\n  {cat_name}:")
        for s in strings_in_cat[:5]:
            print(f"    [{s['offset']:06X}] {s['decoded'][:50]}")


if __name__ == '__main__':
    main()
