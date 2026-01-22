#!/usr/bin/env python3
"""
Create semantic mapping between English and German FF7 menu strings
Analyzes both files to match strings based on semantic meaning, position, and context
"""

import re
import csv
from typing import List, Dict, Tuple, Optional

# Known exact translations
KNOWN_TRANSLATIONS = {
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
    "Yes": "Ja",
    "No": "Nein",
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
}

# Identical strings across languages
IDENTICAL_STRINGS = {"ATB", "Mono", "Stereo", "Normal", "Auto", "PHS", "Materia", "Gil"}

def parse_english_file(filepath: str) -> List[Dict]:
    """Parse English strings file into structured data"""
    strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Match pattern: [INDEX] OFFSET LENGTH TYPE | TEXT | HEX
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

def calculate_similarity(en_text: str, de_text: str) -> float:
    """Calculate basic similarity score between two strings"""
    # Exact match
    if en_text == de_text:
        return 1.0

    # Length similarity
    len_ratio = min(len(en_text), len(de_text)) / max(len(en_text), len(de_text))

    # Word count similarity
    en_words = en_text.split()
    de_words = de_text.split()
    word_ratio = min(len(en_words), len(de_words)) / max(len(en_words), len(de_words))

    return (len_ratio + word_ratio) / 2

def find_best_match(en_string: Dict, de_strings: List[Dict], used_indices: set, context: Dict) -> Tuple[Optional[Dict], str, str]:
    """
    Find best German match for an English string
    Returns: (german_match, confidence_level, notes)
    """
    en_text = en_string['text']
    en_idx = en_string['index']

    # Check known translations first
    if en_text in KNOWN_TRANSLATIONS:
        target_de = KNOWN_TRANSLATIONS[en_text]
        for de in de_strings:
            if de['text'] == target_de and de['index'] not in used_indices:
                return (de, 'exact', 'Known translation match')

    # Check identical strings
    if en_text in IDENTICAL_STRINGS:
        for de in de_strings:
            if de['text'] == en_text and de['index'] not in used_indices:
                return (de, 'exact', 'Identical string')

    # Semantic section-based matching
    candidates = []

    # Define section boundaries based on known structure
    section_ranges = [
        (0, 4, "Quit dialog"),
        (5, 31, "Config menu"),
        (38, 48, "Main menu"),
        (49, 57, "Misc labels"),
        (58, 76, "Keyboard labels"),
    ]

    current_section = None
    for start, end, name in section_ranges:
        if start <= en_idx <= end:
            current_section = name
            break

    # Look for matches within similar position range
    search_start = max(0, en_idx - 10)
    search_end = min(len(de_strings), en_idx + 20)

    for i in range(search_start, search_end):
        if i >= len(de_strings):
            break
        de = de_strings[i]
        if de['index'] in used_indices:
            continue

        similarity = calculate_similarity(en_text, de['text'])
        candidates.append((de, similarity, i))

    if candidates:
        # Sort by similarity, prefer closer positions
        candidates.sort(key=lambda x: (x[1], -abs(x[2] - en_idx)), reverse=True)
        best = candidates[0]

        if best[1] > 0.7:
            return (best[0], 'high', f'Semantic match in section: {current_section}')
        elif best[1] > 0.5:
            return (best[0], 'medium', f'Possible match, similarity: {best[1]:.2f}')
        else:
            return (best[0], 'low', f'Weak match, needs review')

    return (None, 'none', 'No suitable match found')

def create_mapping(en_strings: List[Dict], de_strings: List[Dict]) -> List[Dict]:
    """Create comprehensive mapping between English and German strings"""
    mappings = []
    used_de_indices = set()
    context = {}

    for en_string in en_strings:
        de_match, confidence, notes = find_best_match(en_string, de_strings, used_de_indices, context)

        if de_match:
            used_de_indices.add(de_match['index'])
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

    print("Creating semantic mapping...")
    mappings = create_mapping(en_strings, de_strings)

    print(f"Writing {len(mappings)} mappings to {output_file}")
    write_mapping_csv(mappings, output_file)

    # Print statistics
    confidence_counts = {}
    for m in mappings:
        conf = m['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1

    print("\nMapping Statistics:")
    for conf, count in sorted(confidence_counts.items()):
        print(f"  {conf}: {count}")

    print(f"\nMapping complete! Output: {output_file}")

if __name__ == '__main__':
    main()
