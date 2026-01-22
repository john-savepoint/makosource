#!/usr/bin/env python3
"""
Enhanced semantic mapping between English and German FF7 menu strings
Uses section-aware matching, known translations, and context analysis
"""

import re
import csv
from typing import List, Dict, Tuple, Optional

# Complete known translations dictionary
KNOWN_TRANSLATIONS = {
    # Quit dialog
    "Do you want to quit": "Möchten Sie Final",
    "playing Final Fantasy VII": "Fantasy VII verlassen und",
    "and return to Windows?": "zu Windows zurückkehren?",
    "Yes": "Ja",
    "No": "Nein",

    # Config menu
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

    # Main menu
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

    # Other common strings
    "Time": "Zeit",
    "Gil": "Gil",
    "next level": "Nächst. Lv",
    "Limit level": "Limit-Stufe",
    "Tutorial": "Anleitung",
    "Fury": "Zorn",
    "Sadness": "Traurigk.",
    "Beginner": "Anfänger",
    "Mono": "Mono",
    "Stereo": "Stereo",
    "Pause": "Pause",
    "LEVEL UP": "LV+1",

    # Keyboard labels
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
    "Sadness": "Traurigkeit",
    "Fury": "Zorn",
    "Confusion": "Verwirrung",
    "Silence": "Stummheit",
    "Haste": "Schnell",
    "Slow": "Langsam",
    "Stop": "Stop",
    "Petrify": "Versteinerung",
    "Regen": "regen",
    "Barrier": "Reflektieren",
    "MBarrier": "Doppel",
    "Reflect": "Schild",
    "Death": "Toll",
    "Dual": "Einzigartig",
    "Paralyzed": "Lähmung",
    "Darkness": "Dunkelheit",
    "Sleep": "Schlaf",

    # Elements
    "Fire": "Feuer",
    "Ice": "Eis",
    "Lightning": "Blitz",
    "Earth": "Erde",
    "Water": "Wasser",
    "Wind": "Wind",
    "Holy": "Heilig",
    "Poison": "Gift",

    # Stats
    "Strength": "Stärke",
    "Vitality": "Vitalität",
    "Magic": "Magie",
    "Spirit": "Geist",
    "Dexterity": "Geschick",
    "Luck": "Glück",

    # Common UI
    "Continue?": "Weiter?",
    "Use": "Verwendung",
    "Forbidden": "Verboten",
    "Type": "Typ",
}

# Section definitions with expected German index ranges
SECTIONS = [
    {
        'name': 'Quit Dialog',
        'en_range': (0, 4),
        'de_range': (0, 4),
        'ordered': True
    },
    {
        'name': 'Config Menu',
        'en_range': (5, 31),
        'de_range': (5, 47),
        'ordered': True
    },
    {
        'name': 'Main Menu',
        'en_range': (38, 48),
        'de_range': (58, 70),
        'ordered': True
    },
    {
        'name': 'Misc Labels',
        'en_range': (49, 57),
        'de_range': (69, 82),
        'ordered': False
    },
    {
        'name': 'Keyboard Prompts',
        'en_range': (58, 76),
        'de_range': (82, 102),
        'ordered': True
    },
]

def parse_english_file(filepath: str) -> List[Dict]:
    """Parse English strings file into structured data"""
    strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            match = re.match(r'\[(\d+)\]\s+0x([0-9A-F]+)\s+\d+\s+\w+\s+\|\s+([^|]+)\s+\|', line)
            if match:
                index = int(match.group(1))
                offset = match.group(2)
                text = match.group(3).strip()
                strings.append({
                    'index': index,
                    'offset': f'0x{offset}',
                    'text': text
                })
    return strings

def parse_german_file(filepath: str) -> List[Dict]:
    """Parse German CSV file into structured data"""
    strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            strings.append({
                'index': int(row['index']),
                'offset': row['offset'],
                'text': row['text']
            })
    return strings

def get_section(index: int, is_english: bool) -> Optional[Dict]:
    """Get the section for a given index"""
    for section in SECTIONS:
        range_key = 'en_range' if is_english else 'de_range'
        start, end = section[range_key]
        if start <= index <= end:
            return section
    return None

def fuzzy_match(en_text: str, de_text: str) -> float:
    """Calculate fuzzy match score between strings"""
    en_lower = en_text.lower()
    de_lower = de_text.lower()

    # Exact match
    if en_text == de_text:
        return 1.0

    # Check for common patterns
    # Numbers match
    en_nums = re.findall(r'\d+', en_text)
    de_nums = re.findall(r'\d+', de_text)
    if en_nums and de_nums and en_nums == de_nums:
        return 0.9

    # Bracket patterns match
    if en_text.startswith('[') and de_text.startswith('['):
        return 0.85

    # Length similarity
    len_ratio = min(len(en_text), len(de_text)) / max(len(en_text), len(de_text)) if max(len(en_text), len(de_text)) > 0 else 0

    # Word count similarity
    en_words = en_text.split()
    de_words = de_text.split()
    word_ratio = min(len(en_words), len(de_words)) / max(len(en_words), len(de_words)) if max(len(en_words), len(de_words)) > 0 else 0

    return (len_ratio * 0.6 + word_ratio * 0.4)

def find_best_match(en_string: Dict, de_strings: List[Dict], used_indices: set, prev_de_index: int) -> Tuple[Optional[Dict], str, str]:
    """
    Find best German match for English string using section-aware matching
    """
    en_text = en_string['text']
    en_idx = en_string['index']

    # Check known translations first
    if en_text in KNOWN_TRANSLATIONS:
        target_de = KNOWN_TRANSLATIONS[en_text]
        for de in de_strings:
            if de['text'] == target_de and de['index'] not in used_indices:
                return (de, 'exact', 'Known translation')

    # Get section context
    section = get_section(en_idx, is_english=True)

    if not section:
        # No section - do broad search
        search_start = 0
        search_end = len(de_strings)
    else:
        # Search within expected German range for this section
        de_start, de_end = section['de_range']

        if section['ordered']:
            # For ordered sections, stay close to previous match
            search_start = max(de_start, prev_de_index - 5)
            search_end = min(de_end + 1, prev_de_index + 15)
        else:
            # For unordered sections, search entire section
            search_start = de_start
            search_end = de_end + 1

    candidates = []

    for i in range(search_start, search_end):
        if i >= len(de_strings):
            break

        de = de_strings[i]
        if de['index'] in used_indices:
            continue

        score = fuzzy_match(en_text, de['text'])

        # Boost score if in same section
        if section:
            de_sect = get_section(de['index'], is_english=False)
            if de_sect and de_sect['name'] == section['name']:
                score += 0.1

        # Boost score for proximity in ordered sections
        if section and section['ordered']:
            distance = abs(de['index'] - prev_de_index)
            if distance <= 5:
                score += (5 - distance) * 0.02

        candidates.append((de, score, de['index']))

    if not candidates:
        return (None, 'none', 'No match found in expected range')

    # Sort by score
    candidates.sort(key=lambda x: x[1], reverse=True)
    best = candidates[0]

    section_note = f"Section: {section['name']}" if section else "No section"

    if best[1] >= 0.9:
        return (best[0], 'exact', section_note)
    elif best[1] >= 0.7:
        return (best[0], 'high', f"{section_note}, score: {best[1]:.2f}")
    elif best[1] >= 0.5:
        return (best[0], 'medium', f"{section_note}, score: {best[1]:.2f}")
    else:
        return (best[0], 'low', f"{section_note}, score: {best[1]:.2f}, needs review")

def create_mapping(en_strings: List[Dict], de_strings: List[Dict]) -> List[Dict]:
    """Create comprehensive mapping between English and German strings"""
    mappings = []
    used_de_indices = set()
    prev_de_index = 0

    for en_string in en_strings:
        de_match, confidence, notes = find_best_match(en_string, de_strings, used_de_indices, prev_de_index)

        if de_match:
            used_de_indices.add(de_match['index'])
            prev_de_index = de_match['index']

            mappings.append({
                'en_index': en_string['index'],
                'en_text': en_string['text'],
                'de_offset': de_match['offset'],
                'de_text': de_match['text'],
                'confidence': confidence,
                'notes': notes
            })
        else:
            mappings.append({
                'en_index': en_string['index'],
                'en_text': en_string['text'],
                'de_offset': '',
                'de_text': '',
                'confidence': 'none',
                'notes': notes
            })

    return mappings

def write_mapping_csv(mappings: List[Dict], output_path: str):
    """Write mapping to CSV file"""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['en_index', 'en_text', 'de_offset', 'de_text', 'confidence', 'notes'])
        writer.writeheader()
        writer.writerows(mappings)

def main():
    en_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt'
    de_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_offsets.csv'
    output_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/english_german_semantic_mapping.csv'

    print("Parsing English strings...")
    en_strings = parse_english_file(en_file)
    print(f"Found {len(en_strings)} English strings")

    print("Parsing German strings...")
    de_strings = parse_german_file(de_file)
    print(f"Found {len(de_strings)} German strings")

    print("Creating enhanced semantic mapping...")
    mappings = create_mapping(en_strings, de_strings)

    print(f"Writing {len(mappings)} mappings to output file")
    write_mapping_csv(mappings, output_file)

    # Statistics
    confidence_counts = {}
    for m in mappings:
        conf = m['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1

    print("\n=== Mapping Statistics ===")
    for conf in ['exact', 'high', 'medium', 'low', 'none']:
        count = confidence_counts.get(conf, 0)
        pct = (count / len(mappings) * 100) if mappings else 0
        print(f"  {conf:8s}: {count:4d} ({pct:5.1f}%)")

    print(f"\n✓ Mapping complete!")
    print(f"  Output: {output_file}")
    print(f"  Total mappings: {len(mappings)}")

if __name__ == '__main__':
    main()
