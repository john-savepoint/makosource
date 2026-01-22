#!/usr/bin/env python3
"""
FF7 German String Extractor v2
==============================
Created: 2026-01-02
Session: 68888497-9f38-454c-8ee5-3953fa6c7625

Purpose: Extract ALL German text strings from ff7_de.exe for the FF7OG Japanese project.
This version correctly handles FF7's encoding: FF7_byte + 0x20 = ASCII_byte

FF7 Text Encoding (verified from binary analysis):
- FF7 byte 0x26 = ASCII 'F' (0x46) - e.g., &ENSTERFARBE = FENSTERFARBE
- FF7 byte 0x33 = ASCII 'S' (0x53) - e.g., 3OUND = SOUND
- FF7 byte 0x2B = ASCII 'K' (0x4B) - e.g., +ONTROLLER = KONTROLLER
- FF7 byte 0x00 = Space (0x20)
- String terminator = 0xFF or 0x00 in some contexts
- German special chars: ä=0x6A (needs verification), ö=0x7A, ü=0x7F, ß=0x7E
"""

import os
import sys
from collections import defaultdict

# FF7 to ASCII: add 0x20 to get ASCII
def ff7_to_ascii(ff7_byte):
    """Convert FF7 encoded byte to ASCII character."""
    if ff7_byte == 0xFF:
        return None  # String terminator

    # Standard FF7 encoding: add 0x20 to get ASCII
    ascii_val = ff7_byte + 0x20

    # German special characters (these may have special handling)
    german_special = {
        0x6A: 'ä',  # ä
        0x6B: 'Ä',  # Ä
        0x7A: 'ö',  # ö
        0x7B: 'Ö',  # Ö
        0x7F: 'ü',  # ü
        0x80: 'Ü',  # Ü
        0x7E: 'ß',  # ß
    }

    if ff7_byte in german_special:
        return german_special[ff7_byte]

    # Check if result is printable ASCII
    if 0x20 <= ascii_val <= 0x7E:
        return chr(ascii_val)

    # Handle space (0x00 in FF7 = 0x20 space in ASCII)
    if ff7_byte == 0x00:
        return ' '

    # Return placeholder for unknown bytes
    return f'[{ff7_byte:02X}]'


def decode_ff7_string(data):
    """Decode a sequence of FF7 bytes into a readable string."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        char = ff7_to_ascii(b)
        if char:
            result.append(char)
    return ''.join(result)


def is_valid_menu_string(data, decoded, min_printable=3):
    """Check if this looks like a valid menu string."""
    if len(decoded) < 2:
        return False

    # Count printable/readable characters (excluding placeholders)
    clean = ''.join(c for c in decoded if not c.startswith('['))
    printable = sum(1 for c in clean if c.isprintable())

    if printable < min_printable:
        return False

    # Check for too many control codes
    brackets = decoded.count('[')
    if brackets > len(decoded) // 3:
        return False

    return True


def find_strings_in_region(data, base_offset, pattern_start=None):
    """Find all FF7 text strings in a region of binary data."""
    strings = []
    i = 0

    while i < len(data) - 2:
        # Look for 0xFF terminated strings
        if i > 0 and data[i-1] == 0xFF:
            # Potential string start after terminator
            pass

        # Try to decode from this position
        end = i
        while end < len(data) and data[end] != 0xFF:
            end += 1

        if end > i and end < len(data):
            string_bytes = data[i:end]
            decoded = decode_ff7_string(string_bytes)

            if is_valid_menu_string(string_bytes, decoded):
                # Clean up the decoded string for display
                clean_decoded = decoded.strip()
                if clean_decoded and len(clean_decoded) >= 2:
                    strings.append({
                        'offset': base_offset + i,
                        'length': end - i + 1,  # +1 for terminator
                        'raw_bytes': bytes(string_bytes),
                        'raw_hex': ' '.join(f'{b:02X}' for b in string_bytes[:40]),
                        'decoded': clean_decoded
                    })
            i = end + 1
        else:
            i += 1

    return strings


def extract_fixed_width_strings(data, base_offset, width=48):
    """Extract strings from fixed-width record structures (common in FF7 menus)."""
    strings = []

    for i in range(0, len(data) - width, width):
        record = data[i:i+width]

        # Find string end (0xFF or first non-printable after printable content)
        string_end = 0
        for j, b in enumerate(record):
            if b == 0xFF:
                string_end = j
                break

        if string_end > 2:
            string_bytes = record[:string_end]
            decoded = decode_ff7_string(string_bytes)

            if is_valid_menu_string(string_bytes, decoded):
                clean = decoded.strip()
                if clean and len(clean) >= 2:
                    strings.append({
                        'offset': base_offset + i,
                        'length': string_end + 1,
                        'raw_bytes': bytes(string_bytes),
                        'raw_hex': ' '.join(f'{b:02X}' for b in string_bytes[:40]),
                        'decoded': clean
                    })

    return strings


def scan_menu_region(exe_data, start, end, name):
    """Scan a region for menu strings using multiple techniques."""
    region = exe_data[start:end]
    all_strings = []

    # Method 1: Look for 0xFF separated strings
    strings1 = find_strings_in_region(region, start)
    all_strings.extend(strings1)

    # Method 2: Try fixed-width extraction at various widths
    for width in [48, 32, 64, 24]:
        strings2 = extract_fixed_width_strings(region, start, width)
        for s in strings2:
            # Don't add duplicates
            if not any(abs(s['offset'] - existing['offset']) < 4 for existing in all_strings):
                all_strings.append(s)

    return all_strings


def categorize_string(text):
    """Categorize a string based on German keywords."""
    t = text.lower()

    # Config/Settings
    if any(w in t for w in ['fenster', 'sound', 'controller', 'cursor', 'tempo', 'meldung', 'kamera', 'speicher', 'laden', 'mono', 'stereo', 'config', 'einstellung']):
        return 'Config/Settings'

    # Battle
    if any(w in t for w in ['kampf', 'angriff', 'attack', 'magie', 'magic', 'limit', 'flucht', 'verteidigung', 'schlachthilfe']):
        return 'Battle'

    # Menu
    if any(w in t for w in ['menü', 'menu', 'item', 'status', 'equip', 'materia', 'phs', 'anfang', 'aktiv', 'warten']):
        return 'Menu'

    # Status
    if any(w in t for w in ['gift', 'schlaf', 'stumm', 'blind', 'tod', 'verwirr']):
        return 'Status Effects'

    # Shop
    if any(w in t for w in ['kaufen', 'verkauf', 'gil', 'preis']):
        return 'Shop'

    # Save/Load
    if any(w in t for w in ['speicher', 'laden', 'datei', 'slot']):
        return 'Save/Load'

    # Gold Saucer
    if any(w in t for w in ['saucer', 'spiel', 'arena', 'chocobo', 'rennen']):
        return 'Gold Saucer'

    # Items
    if any(w in t for w in ['trank', 'potion', 'elixir', 'äther', 'ether']):
        return 'Items'

    return 'Other'


def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    output_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent1_german_extraction"

    print(f"Reading {exe_path}...")
    with open(exe_path, 'rb') as f:
        exe_data = f.read()
    print(f"File size: {len(exe_data):,} bytes")

    # Focus on the main menu string region (0x590000 onwards based on analysis)
    regions = [
        (0x590000, 0x5A0000, 'Main Config Menu'),
        (0x5A0000, 0x5B0000, 'Extended Menu 1'),
        (0x5B0000, 0x5C0000, 'Extended Menu 2'),
        (0x5C0000, 0x5D0000, 'Extended Menu 3'),
        (0x56F000, 0x580000, 'Item/Equipment Names'),
        (0x594000, 0x598000, 'Status/Battle Messages'),
        (0x598000, 0x5A0000, 'Gold Saucer/Mini-games'),
    ]

    all_strings = []

    for start, end, name in regions:
        if start >= len(exe_data):
            continue
        actual_end = min(end, len(exe_data))
        print(f"\nScanning: {name} (0x{start:X}-0x{actual_end:X})...")

        strings = scan_menu_region(exe_data, start, actual_end, name)
        print(f"  Found {len(strings)} strings")
        all_strings.extend(strings)

    # Remove duplicates based on offset
    seen = set()
    unique = []
    for s in all_strings:
        key = s['offset']
        if key not in seen:
            seen.add(key)
            unique.append(s)

    unique.sort(key=lambda x: x['offset'])
    print(f"\nTotal unique strings: {len(unique)}")

    # Write complete strings file
    with open(os.path.join(output_dir, 'german_strings_complete.txt'), 'w', encoding='utf-8') as f:
        f.write("# FF7 German String Extraction (Complete)\n")
        f.write("# Source: ff7_de.exe\n")
        f.write(f"# Total strings: {len(unique)}\n")
        f.write("# Format: [OFFSET] [LEN] RAW_HEX | DECODED\n")
        f.write("=" * 100 + "\n\n")

        for s in unique:
            hex_preview = s['raw_hex'][:60]
            f.write(f"[0x{s['offset']:06X}] [{s['length']:3d}] {hex_preview:<60} | {s['decoded']}\n")

    # Categorize and write by category
    categories = defaultdict(list)
    for s in unique:
        cat = categorize_string(s['decoded'])
        categories[cat].append(s)

    with open(os.path.join(output_dir, 'german_strings_by_category.txt'), 'w', encoding='utf-8') as f:
        f.write("# FF7 German Strings by Category\n")
        f.write(f"# Total: {len(unique)} strings\n")
        f.write("=" * 80 + "\n")

        for cat in sorted(categories.keys()):
            strings = categories[cat]
            f.write(f"\n## {cat} ({len(strings)} strings)\n")
            f.write("-" * 60 + "\n")
            for s in strings:
                f.write(f"[0x{s['offset']:06X}] {s['decoded']}\n")

    # Print summary and samples
    print("\n" + "=" * 60)
    print("CATEGORY SUMMARY:")
    for cat in sorted(categories.keys()):
        print(f"  {cat}: {len(categories[cat])} strings")

    print("\nSAMPLE STRINGS (first 5 from each category):")
    for cat in sorted(categories.keys()):
        print(f"\n  {cat}:")
        for s in categories[cat][:5]:
            print(f"    [0x{s['offset']:06X}] {s['decoded'][:50]}")

    print(f"\nOutput written to: {output_dir}")


if __name__ == '__main__':
    main()
