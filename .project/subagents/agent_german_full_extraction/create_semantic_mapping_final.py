#!/usr/bin/env python3
"""
FINAL Production-Quality Semantic Mapping for FF7 English-German Strings
Handles all edge cases including composite keyboard mapping strings
"""

import re
import csv
from typing import List, Dict, Tuple, Optional, Set

# === COMPREHENSIVE KNOWN TRANSLATIONS ===

KNOWN_EXACT = {
    # Quit dialog (EN 0-4, DE 0-4)
    "Do you want to quit": "Möchten Sie Final",
    "playing Final Fantasy VII": "Fantasy VII verlassen und",
    "and return to Windows?": "zu Windows zurückkehren?",
    "Yes": "Ja",
    "No": "Nein",

    # Config menu (EN 5-31, DE 5-47)
    "Window color": "Fensterfarbe",
    "Sound": "Sound",
    "Controller": "Kontroller",
    "Cursor": "Cursor",
    "ATB": "ATB",
    "Battle speed": "Kampftempo",
    "Battle message": "Kampfmeldung",
    "Field message": "Feldmeldung",
    "Camera angle": "Kamerawinkel",
    "Select": "Auswählen",
    "Cancel": "Abbrechen",
    "Menu": "Menü",
    "Normal": "Normal",
    "Customize": "Benutzerdefiniert",
    "Initial": "Anfang",
    "Memory": "Speicher",
    "Active": "Aktiv",
    "Recommended": "Empfohlen",
    "Wait": "Warten",
    "Auto": "Auto",
    "Fixed": "Fest",
    "Slow": "Langs.",
    "Fast": "Schn.",
    "Magic order": "Zauberfolge",
    "restore": "Heilung",
    "attack": "Angriff",
    "indirect": "Indirekt",

    # Main menu (EN 38-48, DE 58-70)
    "Item": "Objekt",
    "Magic": "Zauber",
    "Materia": "Materia",
    "Equip": "Ausrüsten",
    "Status": "Werte",
    "Order": "Reihe",
    "Limit": "Limit",
    "Config": "Konfig",
    "PHS": "PHS",
    "Save": "Speichern",
    "Quit": "Verlassen",
    "Beginner": "Anfänger",

    # Stats and UI (EN 49-57)
    "Time": "Zeit",
    "Gil": "Gil",
    "next level": "Nächst. Lv",
    "Limit level": "Limit-Stufe",
    "Tutorial": "Anleitung",
    "LEVEL UP": "LV+1",
    "Fury": "Zorn",
    "Sadness": "Traurigk.",

    # Keyboard prompts (EN 61-76, DE 86-101)
    "[OK]": "[O.K.]",
    "[CANCEL]": "[ABBRECHEN]",
    "[MENU]": "[MENÜ]",
    "[SWITCH]": "[UMSCHALTEN]",
    "[PAGEUP]": "[BILD HOCH]",
    "[PAGEDOWN]": "[BILD HERUNTER]",
    "[CAMERA]": "[KAMERA]",
    "[TARGET]": "[ZIEL]",
    "[ASSIST]": "[HILFE]",
    "[START]": "[START]",
    "[UP]": "[HERAUF]",
    "[DOWN]": "[UNTEN]",
    "[LEFT]": "[LINKS]",
    "[RIGHT]": "[RECHT]",
    "KEYBOARD": "TASTATUR",
    "JOYSTICK": "JOYSTICK",

    # Status effects
    "Poison": "Gift",
    "Sleep": "Schlaf",
    "Confusion": "Verwirrung",
    "Silence": "Stummheit",
    "Haste": "Schnell",
    "Slow": "Langsam",
    "Stop": "Stop",
    "Petrify": "Versteinerung",
    "Regen": "regen",
    "Reflect": "Reflektieren",
    "Dual": "Doppel",
    "Shield": "Schild",
    "Death": "Toll",
    "Unique": "Einzigartig",
    "Paralyzed": "Lähmung",
    "Darkness": "Dunkelheit",

    # Common UI strings
    "Pause": "Pause",
    "Use": "Verwendung",
    "Forbidden": "Verboten",
    "Type": "Typ",
    "Mono": "Mono",
    "Stereo": "Stereo",
}

# Keyboard keys that are in composite string DE index 102
# English indices 77-191 map to content within this German blob
KEYBOARD_COMPOSITE_RANGE = (77, 191)

# Sections with defined ranges
SECTIONS = [
    {'name': 'Quit Dialog', 'en': (0, 4), 'de': (0, 4), 'ordered': True},
    {'name': 'Config Menu', 'en': (5, 31), 'de': (5, 47), 'ordered': True},
    {'name': 'Special Tokens', 'en': (32, 37), 'de': (48, 57), 'ordered': False},
    {'name': 'Main Menu', 'en': (38, 48), 'de': (58, 70), 'ordered': True},
    {'name': 'Misc UI Labels', 'en': (49, 57), 'de': (71, 82), 'ordered': False},
    {'name': 'Keyboard Prompts', 'en': (58, 76), 'de': (83, 101), 'ordered': True},
    {'name': 'Keyboard Keys (Composite)', 'en': KEYBOARD_COMPOSITE_RANGE, 'de': (102, 102), 'ordered': False},
    {'name': 'Various Data', 'en': (192, 300), 'de': (103, 300), 'ordered': False},
    {'name': 'Game Content', 'en': (300, 767), 'de': (200, 895), 'ordered': False},
]

def parse_english_file(filepath: str) -> List[Dict]:
    """Parse English strings file"""
    strings = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            match = re.match(r'\[(\d+)\]\s+0x([0-9A-F]+)\s+\d+\s+\w+\s+\|\s+([^|]+)\s+\|', line)
            if match:
                index = int(match.group(1))
                offset = match.group(2)
                text = match.group(3).strip()
                strings.append({'index': index, 'offset': f'0x{offset}', 'text': text})
    return strings

def parse_german_file(filepath: str) -> List[Dict]:
    """Parse German CSV file"""
    strings = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            strings.append({
                'index': int(row['index']),
                'offset': row['offset'],
                'text': row['text']
            })
    return strings

def get_section_for_index(idx: int, is_english: bool) -> Optional[Dict]:
    """Get section info for given index"""
    key = 'en' if is_english else 'de'
    for section in SECTIONS:
        start, end = section[key]
        if start <= idx <= end:
            return section
    return None

def fuzzy_similarity(en_text: str, de_text: str) -> float:
    """Calculate similarity score between two strings"""
    if en_text == de_text:
        return 1.0

    en_lower = en_text.lower()
    de_lower = de_text.lower()

    # Number matching
    en_nums = re.findall(r'\d+', en_text)
    de_nums = re.findall(r'\d+', de_text)
    if en_nums and de_nums and en_nums == de_nums:
        return 0.9

    # Bracket format matching
    if en_text.startswith('[') and de_text.startswith('['):
        en_inner = en_text.strip('[]')
        de_inner = de_text.strip('[]')
        if en_inner.lower() in de_inner.lower() or de_inner.lower() in en_inner.lower():
            return 0.85

    # Length and word count similarity
    len_ratio = min(len(en_text), len(de_text)) / max(len(en_text), len(de_text), 1)
    en_words = en_text.split()
    de_words = de_text.split()
    word_ratio = min(len(en_words), len(de_words)) / max(len(en_words), len(de_words), 1)

    return len_ratio * 0.5 + word_ratio * 0.5

def find_match(en_entry: Dict, de_strings: List[Dict], used: Set[int], last_de_idx: int) -> Tuple[Optional[Dict], str, str]:
    """
    Find best German match for English entry
    Returns: (german_entry, confidence, notes)
    """
    en_text = en_entry['text']
    en_idx = en_entry['index']

    # Check known translations
    if en_text in KNOWN_EXACT:
        target = KNOWN_EXACT[en_text]
        for de in de_strings:
            if de['text'] == target and de['index'] not in used:
                return (de, 'exact', 'Known translation')

    # Handle keyboard composite section (EN 77-191 -> DE 102)
    if KEYBOARD_COMPOSITE_RANGE[0] <= en_idx <= KEYBOARD_COMPOSITE_RANGE[1]:
        # These English entries are individual keyboard keys
        # German has them in one composite blob at index 102
        for de in de_strings:
            if de['index'] == 102:
                return (de, 'high', 'Keyboard composite - part of DE index 102')

    # Get section
    section = get_section_for_index(en_idx, is_english=True)

    # Determine search range
    if not section:
        search_start, search_end = 0, len(de_strings)
    else:
        de_start, de_end = section['de']
        if section['ordered']:
            # Stay close to previous match for ordered sections
            search_start = max(de_start, last_de_idx - 3)
            search_end = min(de_end + 1, last_de_idx + 20)
        else:
            # Search entire section for unordered
            search_start = de_start
            search_end = min(de_end + 1, len(de_strings))

    # Find candidates
    candidates = []
    for i in range(search_start, search_end):
        if i >= len(de_strings):
            break
        de = de_strings[i]
        if de['index'] in used:
            continue

        score = fuzzy_similarity(en_text, de['text'])

        # Boost for same section
        if section:
            de_sect = get_section_for_index(de['index'], is_english=False)
            if de_sect and de_sect['name'] == section['name']:
                score += 0.15

        # Boost for proximity in ordered sections
        if section and section['ordered']:
            distance = abs(de['index'] - last_de_idx)
            if distance <= 3:
                score += (3 - distance) * 0.05

        candidates.append((de, score, de['index']))

    if not candidates:
        return (None, 'none', 'No candidates in expected range')

    # Get best
    candidates.sort(key=lambda x: (x[1], -abs(x[2] - last_de_idx)), reverse=True)
    best_de, best_score, best_idx = candidates[0]

    section_name = section['name'] if section else 'General'

    if best_score >= 0.95:
        return (best_de, 'exact', f'{section_name}')
    elif best_score >= 0.75:
        return (best_de, 'high', f'{section_name}, score: {best_score:.2f}')
    elif best_score >= 0.55:
        return (best_de, 'medium', f'{section_name}, score: {best_score:.2f}')
    else:
        return (best_de, 'low', f'{section_name}, score: {best_score:.2f}, review needed')

def create_mapping(en_strings: List[Dict], de_strings: List[Dict]) -> List[Dict]:
    """Create comprehensive English-German mapping"""
    mappings = []
    used_de = set()
    last_de_idx = 0

    for en_entry in en_strings:
        de_match, conf, notes = find_match(en_entry, de_strings, used_de, last_de_idx)

        if de_match:
            used_de.add(de_match['index'])
            last_de_idx = de_match['index']

            mappings.append({
                'en_index': en_entry['index'],
                'en_text': en_entry['text'],
                'de_offset': de_match['offset'],
                'de_text': de_match['text'],
                'confidence': conf,
                'notes': notes
            })
        else:
            mappings.append({
                'en_index': en_entry['index'],
                'en_text': en_entry['text'],
                'de_offset': '',
                'de_text': '',
                'confidence': 'none',
                'notes': notes
            })

    return mappings

def write_output(mappings: List[Dict], output_path: str):
    """Write mappings to CSV"""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['en_index', 'en_text', 'de_offset', 'de_text', 'confidence', 'notes'])
        writer.writeheader()
        writer.writerows(mappings)

def print_stats(mappings: List[Dict]):
    """Print mapping statistics"""
    counts = {}
    for m in mappings:
        conf = m['confidence']
        counts[conf] = counts.get(conf, 0) + 1

    total = len(mappings)
    print("\n" + "="*60)
    print("  FINAL MAPPING STATISTICS")
    print("="*60)

    for conf in ['exact', 'high', 'medium', 'low', 'none']:
        count = counts.get(conf, 0)
        pct = (count / total * 100) if total else 0
        bar = '█' * int(pct / 2)
        print(f"  {conf:8s}: {count:4d} ({pct:5.1f}%) {bar}")

    print("="*60)
    print(f"  TOTAL: {total} mappings")
    print("="*60)

def main():
    en_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt'
    de_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_offsets.csv'
    output_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/english_german_semantic_mapping.csv'

    print("\n🔍 Parsing English strings...")
    en_strings = parse_english_file(en_file)
    print(f"   Found {len(en_strings)} English strings")

    print("\n🔍 Parsing German strings...")
    de_strings = parse_german_file(de_file)
    print(f"   Found {len(de_strings)} German strings")

    print("\n🔄 Creating semantic mappings...")
    print("   Using section-aware matching with known translations")
    mappings = create_mapping(en_strings, de_strings)

    print(f"\n💾 Writing output to CSV...")
    write_output(mappings, output_file)

    print_stats(mappings)

    print(f"\n✅ SUCCESS!")
    print(f"   Output file: {output_file}")

if __name__ == '__main__':
    main()
