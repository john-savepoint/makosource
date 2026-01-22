#!/usr/bin/env python3
"""
FF7 German String Extractor - Complete Version
===============================================
Created: 2026-01-02
Session: 68888497-9f38-454c-8ee5-3953fa6c7625

VERIFIED STRUCTURE from hex analysis:
- Menu strings at 0x590000+ in 48-byte fixed records
- Each record starts with padding (0x00 bytes), then string, then 0xFF terminator
- Encoding: raw_byte + 0x20 = ASCII
  Example: 0x26 + 0x20 = 0x46 = 'F' → &ENSTERFARBE = FENSTERFARBE

German special characters (override the +0x20 rule):
- 0x6A = ä (not 0x8A)
- 0x7F = ü (not 0x9F)
- 0x7E = ß (not 0x9E)
"""

import os
from collections import defaultdict

# Special character overrides
GERMAN_SPECIALS = {
    0x6A: 'ä', 0x6B: 'Ä',
    0x7A: 'ö', 0x7B: 'Ö',
    0x7F: 'ü', 0x80: 'Ü',
    0x7E: 'ß',
}


def decode_ff7_byte(b):
    """Decode single FF7 byte to character."""
    if b == 0xFF:
        return None
    if b in GERMAN_SPECIALS:
        return GERMAN_SPECIALS[b]
    if b == 0x00:
        return ' '
    ascii_val = b + 0x20
    if 0x20 <= ascii_val <= 0x7E:
        return chr(ascii_val)
    return None


def decode_ff7_string(data):
    """Decode FF7 byte sequence to string, stopping at 0xFF."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        ch = decode_ff7_byte(b)
        if ch:
            result.append(ch)
    return ''.join(result).strip()


def extract_fixed_records(data, base_offset, record_size=48):
    """Extract strings from fixed-size record structure."""
    strings = []
    num_records = len(data) // record_size

    for i in range(num_records):
        start = i * record_size
        record = data[start:start + record_size]

        # Find first non-zero byte (start of actual string)
        str_start = 0
        while str_start < len(record) and record[str_start] == 0x00:
            str_start += 1

        if str_start >= len(record) - 1:
            continue

        # Find terminator
        str_end = str_start
        while str_end < len(record) and record[str_end] != 0xFF:
            str_end += 1

        if str_end <= str_start:
            continue

        raw = record[str_start:str_end]
        decoded = decode_ff7_string(raw)

        if decoded and len(decoded) >= 2:
            strings.append({
                'offset': base_offset + start + str_start,
                'record_offset': base_offset + start,
                'length': str_end - str_start + 1,
                'raw_hex': ' '.join(f'{b:02X}' for b in raw),
                'decoded': decoded
            })

    return strings


def extract_sequential_strings(data, base_offset, min_len=2):
    """Extract 0xFF-terminated strings sequentially."""
    strings = []
    i = 0

    while i < len(data) - min_len:
        # Skip leading zeros/padding
        while i < len(data) and data[i] == 0x00:
            i += 1

        if i >= len(data) - min_len:
            break

        # Find terminator
        end = i
        while end < len(data) and data[end] != 0xFF:
            end += 1

        if end > i and end < len(data):
            raw = data[i:end]
            decoded = decode_ff7_string(raw)

            if decoded and len(decoded) >= min_len:
                strings.append({
                    'offset': base_offset + i,
                    'record_offset': base_offset + i,
                    'length': end - i + 1,
                    'raw_hex': ' '.join(f'{b:02X}' for b in raw[:40]),
                    'decoded': decoded
                })
            i = end + 1
        else:
            i += 1

    return strings


def categorize_string(text):
    """Categorize based on German keywords."""
    t = text.lower()

    categories = [
        ('Config/Settings', ['fenster', 'farbe', 'sound', 'controller', 'cursor', 'tempo',
                            'meldung', 'kamera', 'einstellung', 'mono', 'stereo', 'breit',
                            'normal', 'benutzerdefiniert', 'empfohlen', 'winkel']),
        ('Battle/Combat', ['kampf', 'angriff', 'magie', 'limit', 'flucht', 'verteidigung',
                          'schlachthilfe', 'schutz', 'schlag', 'aktiv', 'warten']),
        ('Menu/Navigation', ['menü', 'auswählen', 'abbrechen', 'anfang', 'speicher', 'phs',
                            'item', 'status', 'equip', 'materia', 'beenden']),
        ('Save/Load', ['speicher', 'laden', 'datei', 'spielstand', 'slot', 'block']),
        ('Status Effects', ['gift', 'schlaf', 'stumm', 'blind', 'tod', 'verwirrung',
                           'versteinert', 'frosch', 'klein', 'raserei', 'stummheit']),
        ('Shop/Money', ['kaufen', 'verkauf', 'gil', 'preis', 'hand', 'bezahlen']),
        ('Gold Saucer', ['saucer', 'spiel', 'arena', 'chocobo', 'rennen', 'gp',
                        'wette', 'gewinn']),
        ('Items', ['trank', 'elixir', 'äther', 'phönix', 'antidot', 'augentropfen',
                  'heldentrank', 'feder', 'zelt', 'schlüssel']),
        ('Equipment', ['waffe', 'rüstung', 'zubehör', 'schwert', 'stab', 'handschuh',
                      'gewehr', 'speer', 'shuriken', 'megafon', 'würfel', 'panzer']),
        ('Time/Date', ['stunde', 'minute', 'uhr', 'zeit', 'tag']),
    ]

    for cat_name, keywords in categories:
        if any(kw in t for kw in keywords):
            return cat_name

    return 'Other'


def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    output_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent1_german_extraction"

    print("FF7 German String Extraction - Complete")
    print("=" * 50)

    with open(exe_path, 'rb') as f:
        data = f.read()
    print(f"Loaded: {len(data):,} bytes")

    # Define regions based on hex analysis
    regions = [
        # Main config menu (48-byte records)
        (0x5900F0, 0x590C00, 48, 'Config Menu'),
        # Sound settings
        (0x590BC0, 0x590E00, 48, 'Sound Settings'),
        # Main menu options
        (0x590C00, 0x591000, 48, 'Main Menu'),
        # Item names region
        (0x56F800, 0x570800, 0, 'Item Names'),
        # Status messages
        (0x594C00, 0x595800, 0, 'Status Messages'),
        # Shop/prices
        (0x594E00, 0x595200, 0, 'Shop Messages'),
        # Gold Saucer region
        (0x597600, 0x599000, 0, 'Gold Saucer A'),
        (0x599000, 0x59A000, 0, 'Gold Saucer B'),
        # Save/Load
        (0x59C400, 0x59E000, 0, 'Save/Load'),
        # Extended regions
        (0x591000, 0x594C00, 0, 'Extended A'),
        (0x595200, 0x597600, 0, 'Extended B'),
        (0x59A000, 0x59C400, 0, 'Extended C'),
        (0x59E000, 0x5A2000, 0, 'Extended D'),
    ]

    all_strings = []

    for start, end, record_size, name in regions:
        if start >= len(data):
            continue
        end = min(end, len(data))
        region_data = data[start:end]

        print(f"\n{name} (0x{start:06X}-0x{end:06X})...")

        if record_size > 0:
            strings = extract_fixed_records(region_data, start, record_size)
        else:
            strings = extract_sequential_strings(region_data, start)

        print(f"  → {len(strings)} strings")
        all_strings.extend(strings)

    # Deduplicate
    seen = {}
    unique = []
    for s in all_strings:
        text = s['decoded']
        if text not in seen:
            seen[text] = s['offset']
            unique.append(s)

    unique.sort(key=lambda x: x['offset'])

    print(f"\n{'='*50}")
    print(f"Total unique strings: {len(unique)}")

    # Categorize
    categories = defaultdict(list)
    for s in unique:
        cat = categorize_string(s['decoded'])
        categories[cat].append(s)

    # Write complete output
    complete_path = os.path.join(output_dir, 'german_strings_complete.txt')
    with open(complete_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German String Extraction - Complete\n")
        f.write("# Source: ff7_de.exe\n")
        f.write("# Date: 2026-01-02\n")
        f.write(f"# Total: {len(unique)} unique strings\n")
        f.write("#\n")
        f.write("# Format: [OFFSET] [LEN] RAW_HEX | DECODED_TEXT\n")
        f.write("# Encoding: raw_byte + 0x20 = ASCII (with German special char overrides)\n")
        f.write("=" * 100 + "\n\n")

        for s in unique:
            f.write(f"[0x{s['offset']:06X}] [{s['length']:3d}] {s['raw_hex']:<50} | {s['decoded']}\n")

    # Write by category
    cat_path = os.path.join(output_dir, 'german_strings_by_category.txt')
    with open(cat_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Strings by Category\n")
        f.write(f"# Total: {len(unique)} strings\n")
        f.write("# Date: 2026-01-02\n\n")

        for cat in sorted(categories.keys()):
            strings = categories[cat]
            f.write(f"\n{'='*60}\n")
            f.write(f"## {cat} ({len(strings)} strings)\n")
            f.write(f"{'='*60}\n\n")
            for s in strings:
                f.write(f"[0x{s['offset']:06X}] {s['decoded']}\n")

    # Summary
    print("\nCATEGORY BREAKDOWN:")
    for cat in sorted(categories.keys()):
        print(f"  {cat}: {len(categories[cat])}")

    print("\nSAMPLE STRINGS (first 10 each):")
    for cat in ['Config/Settings', 'Battle/Combat', 'Menu/Navigation', 'Items', 'Status Effects']:
        if cat in categories:
            print(f"\n  {cat}:")
            for s in categories[cat][:10]:
                print(f"    [{s['offset']:06X}] {s['decoded']}")

    print(f"\nOutput: {output_dir}")


if __name__ == '__main__':
    main()
