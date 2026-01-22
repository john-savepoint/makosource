#!/usr/bin/env python3
"""
FF7 German String Extractor - Final Version
============================================
Created: 2026-01-02
Session: 68888497-9f38-454c-8ee5-3953fa6c7625

This is the definitive extraction script for German menu strings from ff7_de.exe.
Focuses on clean extraction with proper deduplication and categorization.

Encoding: FF7_byte + 0x20 = ASCII_byte
Example: 0x26 ('&' in raw) + 0x20 = 0x46 ('F') → &ENSTERFARBE = FENSTERFARBE
"""

import os
from collections import defaultdict
import re

# German special character overrides for bytes that don't follow standard +0x20 rule
GERMAN_SPECIAL = {
    0x6A: 'ä',
    0x6B: 'Ä',
    0x7A: 'ö',
    0x7B: 'Ö',
    0x7F: 'ü',
    0x80: 'Ü',
    0x7E: 'ß',
}


def ff7_decode(data):
    """Decode FF7 bytes to string."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        if b in GERMAN_SPECIAL:
            result.append(GERMAN_SPECIAL[b])
        elif b == 0x00:
            result.append(' ')
        else:
            ascii_val = b + 0x20
            if 0x20 <= ascii_val <= 0x7E:
                result.append(chr(ascii_val))
            else:
                result.append(f'[{b:02X}]')
    return ''.join(result)


def find_ff7_strings(data, base_offset, min_len=3):
    """Extract 0xFF-terminated strings from binary data."""
    strings = []
    i = 0

    while i < len(data) - min_len:
        # Check if this could be start of a string (printable FF7 byte)
        first_byte = data[i]
        ascii_val = first_byte + 0x20

        is_printable_start = (
            first_byte in GERMAN_SPECIAL or
            first_byte == 0x00 or
            (0x20 <= ascii_val <= 0x7E)
        )

        if not is_printable_start:
            i += 1
            continue

        # Find terminator
        end = i
        while end < len(data) and data[end] != 0xFF:
            end += 1

        if end >= len(data):
            i += 1
            continue

        # Extract and decode
        raw = data[i:end]
        if len(raw) < min_len:
            i = end + 1
            continue

        decoded = ff7_decode(raw)

        # Quality checks
        clean = re.sub(r'\[[0-9A-Fa-f]{2}\]', '', decoded).strip()

        # Must have enough clean text
        if len(clean) < min_len:
            i = end + 1
            continue

        # Must be mostly printable
        printable_ratio = len(clean) / len(decoded) if decoded else 0
        if printable_ratio < 0.5:
            i = end + 1
            continue

        # Skip if it's just numbers or punctuation
        if re.match(r'^[\d\s.,;:!?-]+$', clean):
            i = end + 1
            continue

        strings.append({
            'offset': base_offset + i,
            'length': end - i + 1,
            'raw_hex': ' '.join(f'{b:02X}' for b in raw[:32]),
            'decoded': decoded.strip(),
            'clean': clean
        })

        i = end + 1

    return strings


def categorize(text):
    """Categorize string by content keywords."""
    t = text.lower()

    categories = {
        'Config/Settings': ['fenster', 'farbe', 'sound', 'controller', 'cursor', 'tempo',
                           'meldung', 'kamera', 'mono', 'stereo', 'einstellung', 'config',
                           'normal', 'benutzerdefiniert', 'breit', 'empfohlen'],
        'Battle': ['kampf', 'angriff', 'magie', 'limit', 'flucht', 'verteidigung',
                   'schlachthilfe', 'warten', 'aktiv', 'schlag', 'schutz'],
        'Menu': ['menü', 'item', 'status', 'equip', 'materia', 'phs', 'anfang',
                 'abbrechen', 'auswählen'],
        'Save/Load': ['speicher', 'laden', 'datei', 'spielstand', 'slot'],
        'Status Effects': ['gift', 'schlaf', 'stumm', 'blind', 'tod', 'verwirr',
                          'versteinert', 'frosch', 'klein', 'raserei'],
        'Shop': ['kaufen', 'verkauf', 'gil', 'preis', 'hand'],
        'Gold Saucer': ['saucer', 'spiel', 'arena', 'chocobo', 'rennen', 'gp'],
        'Items': ['trank', 'elixir', 'äther', 'phönix', 'antidot', 'augentropfen',
                  'wecker', 'heiltrank', 'heldentrank'],
        'Equipment': ['waffe', 'rüstung', 'zubehör', 'schwert', 'stab', 'handschuh',
                      'gewehr', 'speer', 'shuriken', 'megafon', 'würfel'],
    }

    for cat, keywords in categories.items():
        if any(kw in t for kw in keywords):
            return cat

    return 'Other'


def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    output_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent1_german_extraction"

    print(f"Loading {exe_path}...")
    with open(exe_path, 'rb') as f:
        data = f.read()
    print(f"Size: {len(data):,} bytes")

    # Key menu regions based on hex analysis
    regions = [
        # Config menu area (verified from xxd output)
        (0x5900F0, 0x592000, 'Config Menu Strings'),
        # Item/Materia names
        (0x56F800, 0x570800, 'Item Names'),
        # Status messages
        (0x594C00, 0x595800, 'Status Messages'),
        # Shop/Gold Saucer
        (0x597600, 0x59A000, 'Shop/Gold Saucer'),
        # Save/Load area
        (0x59C400, 0x59E000, 'Save/Load Strings'),
        # Battle messages
        (0x590000, 0x5900F0, 'Battle/System'),
        # Extended regions
        (0x592000, 0x594C00, 'Extended Menu A'),
        (0x595800, 0x597600, 'Extended Menu B'),
        (0x59A000, 0x59C400, 'Extended Menu C'),
        (0x59E000, 0x5A2000, 'Extended Menu D'),
    ]

    all_strings = []
    region_stats = []

    for start, end, name in regions:
        if start >= len(data):
            continue
        end = min(end, len(data))

        print(f"\nScanning {name} (0x{start:06X}-0x{end:06X})...")
        strings = find_ff7_strings(data[start:end], start)

        region_stats.append({
            'name': name,
            'start': start,
            'end': end,
            'count': len(strings)
        })

        print(f"  → {len(strings)} strings found")
        all_strings.extend(strings)

    # Deduplicate by decoded text AND offset
    seen_text = {}
    unique = []
    for s in all_strings:
        key = s['clean']
        # Keep the first occurrence of each unique text
        if key not in seen_text:
            seen_text[key] = s['offset']
            unique.append(s)
        # Or keep if significantly different offset (might be different context)
        elif abs(s['offset'] - seen_text[key]) > 0x1000:
            unique.append(s)

    unique.sort(key=lambda x: x['offset'])

    print(f"\n{'='*60}")
    print(f"Total unique strings: {len(unique)}")

    # Write complete output
    complete_path = os.path.join(output_dir, 'german_strings_complete.txt')
    with open(complete_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German String Extraction - Complete\n")
        f.write("# Source: ff7_de.exe\n")
        f.write(f"# Extracted: 2026-01-02\n")
        f.write(f"# Total: {len(unique)} strings\n")
        f.write("# Format: [OFFSET] [LEN] HEX_PREVIEW | DECODED_TEXT\n")
        f.write("=" * 100 + "\n\n")

        for s in unique:
            f.write(f"[0x{s['offset']:06X}] [{s['length']:3d}] {s['raw_hex']:<48} | {s['decoded']}\n")

    # Categorize
    categories = defaultdict(list)
    for s in unique:
        cat = categorize(s['decoded'])
        categories[cat].append(s)

    # Write categorized output
    cat_path = os.path.join(output_dir, 'german_strings_by_category.txt')
    with open(cat_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Strings by Category\n")
        f.write(f"# Total: {len(unique)} strings\n\n")

        for cat in sorted(categories.keys()):
            items = categories[cat]
            f.write(f"\n{'='*60}\n")
            f.write(f"## {cat} ({len(items)} strings)\n")
            f.write(f"{'='*60}\n\n")

            for s in items:
                f.write(f"[0x{s['offset']:06X}] {s['decoded']}\n")

    # Print summary
    print("\nCATEGORY BREAKDOWN:")
    for cat in sorted(categories.keys()):
        count = len(categories[cat])
        print(f"  {cat}: {count}")

    print("\nSAMPLES FROM KEY CATEGORIES:")
    key_cats = ['Config/Settings', 'Battle', 'Menu', 'Items', 'Status Effects']
    for cat in key_cats:
        if cat in categories:
            print(f"\n  {cat}:")
            for s in categories[cat][:8]:
                print(f"    [0x{s['offset']:06X}] {s['decoded']}")

    print(f"\nOutput: {output_dir}")
    return unique, categories, region_stats


if __name__ == '__main__':
    main()
