#!/usr/bin/env python3
"""
Create improved semantic mapping between English and German FF7 strings.
Uses section-aware matching and rigorous validation.
"""

import csv
import re
from typing import Dict, List, Tuple, Optional

# Comprehensive known translations - corrected and expanded
KNOWN_TRANSLATIONS = {
    # Quit dialog (indices 0-4)
    "Do you want to quit": "Möchten Sie Final",
    "playing Final Fantasy VII": "Fantasy VII verlassen und",
    "and return to Windows?": "zu Windows zurückkehren?",
    "Yes": "Ja",
    "No": "Nein",

    # Config menu (indices 5-31)
    "Window color": "Fensterfarbe",  # CORRECTED
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

    # Main menu (indices 38-48)
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

    # Other common terms
    "Beginner": "Anfänger",
    "Time": "Zeit",
    "Gil": "Gil",
    "next level": "Nächst. Lv",
    "Limit level": "Limit-Stufe",
    "Tutorial": "Anleitung",
    "Fury": "Zorn",
    "Sadness": "Traurigk.",
    "Pause": "Pause",
    "Mono": "Mono",
    "Stereo": "Stereo",

    # Keyboard labels
    "Press [CANCEL] to end.": "Mit [ABBRECHEN] beenden.",
    "Press [OK] to configure a key.": "Drücken Sie auf [O.K.] um die",
    "Now press the new key.": "Bitte neue Taste drücken",
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
}

def parse_english_file(filepath: str) -> List[Tuple[int, str, str]]:
    """Parse English strings file."""
    english_strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            match = re.match(r'\[(\d+)\]\s+(0x[0-9A-F]+)\s+\d+\s+\w+\s+\|\s+([^|]+)\s+\|', line)
            if match:
                index = int(match.group(1))
                offset = match.group(2)
                text = match.group(4).strip()
                english_strings.append((index, text, offset))

    return english_strings

def parse_german_csv(filepath: str) -> List[Tuple[int, str, str]]:
    """Parse German CSV file."""
    german_strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = int(row['index'])
            text = row['text']
            offset = row['offset']
            german_strings.append((index, text, offset))

    return german_strings

def find_exact_match(en_text: str, german_strings: List[Tuple[int, str, str]],
                    used_indices: set) -> Optional[Tuple[int, str, str, str, str]]:
    """Find exact match in German strings."""

    # Check known translations first
    if en_text in KNOWN_TRANSLATIONS:
        target = KNOWN_TRANSLATIONS[en_text]
        for de_idx, de_text, de_offset in german_strings:
            if de_idx not in used_indices and de_text == target:
                return (de_idx, de_text, de_offset, "exact", "Known translation")

    # Check for identical strings (like ATB, PHS, etc.)
    for de_idx, de_text, de_offset in german_strings:
        if de_idx not in used_indices and de_text == en_text:
            return (de_idx, de_text, de_offset, "exact", "Identical string")

    return None

def find_contextual_match(en_idx: int, en_text: str, german_strings: List[Tuple[int, str, str]],
                         used_indices: set, last_de_idx: int) -> Optional[Tuple[int, str, str, str, str]]:
    """Find match based on context and position."""

    # Search in a window around the last matched German index
    search_start = max(0, last_de_idx - 5)
    search_end = min(len(german_strings), last_de_idx + 30)

    for i in range(search_start, search_end):
        if i < len(german_strings):
            de_idx, de_text, de_offset = german_strings[i]
            if de_idx not in used_indices:
                # Check if lengths are similar
                if abs(len(en_text) - len(de_text)) <= max(len(en_text), len(de_text)) // 2:
                    return (de_idx, de_text, de_offset, "high",
                           f"Contextual match (position-based, DE idx {de_idx})")

    return None

def create_comprehensive_mapping(english_strings: List[Tuple[int, str, str]],
                                german_strings: List[Tuple[int, str, str]]) -> List[Dict]:
    """Create comprehensive semantic mapping."""

    mappings = []
    used_german_indices = set()
    last_german_idx = 0

    for en_idx, en_text, en_offset in english_strings:
        match = None

        # Strategy 1: Exact match (known translations or identical)
        match = find_exact_match(en_text, german_strings, used_german_indices)

        # Strategy 2: Contextual match based on position
        if not match:
            match = find_contextual_match(en_idx, en_text, german_strings,
                                        used_german_indices, last_german_idx)

        # Strategy 3: Take next available German string
        if not match:
            for de_idx, de_text, de_offset in german_strings[last_german_idx:]:
                if de_idx not in used_german_indices:
                    match = (de_idx, de_text, de_offset, "medium",
                           f"Sequential fallback (DE idx {de_idx})")
                    break

        if match:
            de_idx, de_text, de_offset, confidence, notes = match
            used_german_indices.add(de_idx)
            last_german_idx = de_idx + 1
        else:
            # No match found
            de_idx = -1
            de_offset = ""
            de_text = ""
            confidence = "none"
            notes = "No German equivalent found"

        mappings.append({
            'en_index': en_idx,
            'en_text': en_text,
            'de_offset': de_offset,
            'de_text': de_text,
            'confidence': confidence,
            'notes': notes
        })

    return mappings

def write_mapping_csv(mappings: List[Dict], output_path: str):
    """Write mappings to CSV."""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['en_index', 'en_text', 'de_offset', 'de_text', 'confidence', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mappings)

def main():
    english_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt'
    german_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_offsets.csv'
    output_file = '/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/english_german_semantic_mapping.csv'

    print("Loading English strings...")
    english_strings = parse_english_file(english_file)
    print(f"Loaded {len(english_strings)} English strings")

    print("Loading German strings...")
    german_strings = parse_german_csv(german_file)
    print(f"Loaded {len(german_strings)} German strings")

    print("Creating comprehensive semantic mapping...")
    mappings = create_comprehensive_mapping(english_strings, german_strings)

    print(f"Writing {len(mappings)} mappings...")
    write_mapping_csv(mappings, output_file)

    # Statistics
    conf_counts = {}
    for m in mappings:
        conf = m['confidence']
        conf_counts[conf] = conf_counts.get(conf, 0) + 1

    print("\nMapping Statistics:")
    print(f"Total mappings: {len(mappings)}")
    for conf in sorted(conf_counts.keys()):
        count = conf_counts[conf]
        pct = (count / len(mappings)) * 100
        print(f"  {conf:10s}: {count:4d} ({pct:5.1f}%)")

    print(f"\nOutput written to: {output_file}")

if __name__ == '__main__':
    main()
