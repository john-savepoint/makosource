#!/usr/bin/env python3
"""
English to German String Mapper for FF7 HEXT Patch
Created: 2026-01-05
Session: Current session

Maps 767 English menu strings to their German equivalents by semantic content.
"""

import re
import csv
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class EnglishString:
    index: int
    offset: str
    length: int
    type: str
    text: str
    hex_bytes: str

@dataclass
class GermanString:
    index: int
    offset: str
    text: str
    padding_bytes: int
    text_bytes: int
    total_bytes: int

@dataclass
class Mapping:
    en_index: int
    en_offset: str
    en_text: str
    de_offset: str
    de_text: str
    confidence: str
    match_method: str

# Known translation pairs
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
    "Pause": "Pause",
    "Mono": "Mono",
    "Stereo": "Stereo",
    "Item": "Objekt",
    "Magic": "Zauber",
    "Materia": "Materia",
    "Equip": "Ausrüsten",
    "Status": "Werte",
    "Order": "Reihe",
    "Limit": "Limit",
    "Config": "Konfig",
    "Save": "Speichern",
    "Quit": "Verlassen",
    "Yes": "Ja",
    "No": "Nein",
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
    "PHS": "PHS",
    "Beginner": "Anfänger",
    "Time": "Zeit",
    "Gil": "Gil",
    "next level": "Nächst. Lv",
    "Limit level": "Limit-Stufe",
    "Tutorial": "Anleitung",
    "Fury": "Zorn",
    "Sadness": "Traurigk.",
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
    "Manipulate": "Einzigartig",
    "Berserk": "Toll",
    "Paralysis": "Lähmung",
    "Darkness": "Dunkelheit",
    "Toad": "Kröte",
    # Element/Effect terms
    "Element": "Element",
    "Effect": "Effekt",
    "Attack": "Angreifen",
    "Defend": "Verteidigen",
    "Halve": "Halbieren",
    "Invalid": "Ungültig",
    "Absorb": "Absorbieren",
    # Stats
    "Strength": "Stärke",
    "Dexterity": "Geschick",
    "Vitality": "Vitalität",
}

def parse_english_strings(filepath: str) -> List[EnglishString]:
    """Parse English strings from touphScript index file."""
    strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Match format: [000] 0x00518370  30 DEF        | Do you want to quit | HEX...
            match = re.match(r'\[(\d+)\]\s+(0x[0-9A-F]+)\s+(\d+)\s+(\w+)\s+\|\s+([^|]+)\s+\|', line)
            if match:
                index = int(match.group(1))
                offset = match.group(2)
                length = int(match.group(3))
                type_str = match.group(4)
                text = match.group(5).strip()
                # Extract hex bytes after second |
                hex_part = line.split('|')[2].strip() if len(line.split('|')) > 2 else ""

                strings.append(EnglishString(
                    index=index,
                    offset=offset,
                    length=length,
                    type=type_str,
                    text=text,
                    hex_bytes=hex_part
                ))
    return strings

def parse_german_strings(filepath: str) -> List[GermanString]:
    """Parse German strings from CSV file."""
    strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            strings.append(GermanString(
                index=int(row['index']),
                offset=row['offset'],
                text=row['text'],
                padding_bytes=int(row['padding_bytes']),
                text_bytes=int(row['text_bytes']),
                total_bytes=int(row['total_bytes'])
            ))
    return strings

def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    return text.lower().strip()

def find_exact_match(en_text: str, german_strings: List[GermanString], used: set) -> Optional[Tuple[GermanString, str]]:
    """Find exact text match."""
    en_norm = normalize_text(en_text)
    for gs in german_strings:
        if gs.offset in used:
            continue
        if normalize_text(gs.text) == en_norm:
            return (gs, "exact")
    return None

def find_translation_match(en_text: str, german_strings: List[GermanString], used: set) -> Optional[Tuple[GermanString, str]]:
    """Find known translation match."""
    if en_text in KNOWN_TRANSLATIONS:
        de_text = KNOWN_TRANSLATIONS[en_text]
        for gs in german_strings:
            if gs.offset in used:
                continue
            if normalize_text(gs.text) == normalize_text(de_text):
                return (gs, "translation")
    return None

def find_context_match(en_index: int, en_text: str, mappings: List[Mapping],
                       german_strings: List[GermanString], used: set,
                       window: int = 5) -> Optional[Tuple[GermanString, str]]:
    """Find match based on nearby already-mapped strings."""
    # Find closest mapped English strings
    closest_before = None
    closest_after = None

    for m in mappings:
        if m.en_index < en_index:
            if closest_before is None or m.en_index > closest_before.en_index:
                closest_before = m
        elif m.en_index > en_index:
            if closest_after is None or m.en_index < closest_after.en_index:
                closest_after = m

    if not closest_before and not closest_after:
        return None

    # Look for German strings in the vicinity
    target_de_offsets = []
    if closest_before:
        # Find German string after closest_before
        for gs in german_strings:
            if gs.offset == closest_before.de_offset:
                idx = german_strings.index(gs)
                for i in range(idx + 1, min(idx + window + 1, len(german_strings))):
                    if german_strings[i].offset not in used:
                        target_de_offsets.append(german_strings[i])
                break

    # Try to match by length similarity
    en_len = len(en_text)
    best_match = None
    best_score = float('inf')

    for gs in target_de_offsets:
        de_len = len(gs.text)
        len_diff = abs(en_len - de_len)
        if len_diff < best_score:
            best_score = len_diff
            best_match = gs

    if best_match:
        return (best_match, "context")

    return None

def manual_group_mappings(english_strings: List[EnglishString],
                         german_strings: List[GermanString],
                         used_german: set) -> List[Mapping]:
    """Manual mappings for known groups."""
    manual_mappings = []

    # Quit dialog group (indices 0-4)
    # English: "Do you want to quit", "playing Final Fantasy VII", "and return to Windows?", "Yes", "No"
    # German: "Möchten Sie Final", "Fantasy VII verlassen und", "zu Windows zurückkehren?", "Ja", "Nein"
    quit_mappings = [
        (0, 0),  # Do you want to quit -> Möchten Sie Final
        (1, 1),  # playing Final Fantasy VII -> Fantasy VII verlassen und
        (2, 2),  # and return to Windows? -> zu Windows zurückkehren?
        (3, 3),  # Yes -> Ja
        (4, 4),  # No -> Nein
    ]

    for en_idx, de_idx in quit_mappings:
        es = english_strings[en_idx]
        gs = german_strings[de_idx]
        manual_mappings.append(Mapping(
            en_index=es.index,
            en_offset=es.offset,
            en_text=es.text,
            de_offset=gs.offset,
            de_text=gs.text,
            confidence="high",
            match_method="manual_group"
        ))
        used_german.add(gs.offset)

    # Keyboard labels (English indices 61-77 map to German indices 86-101)
    # [OK], [CANCEL], [MENU], [SWITCH], [PAGEUP], [PAGEDOWN], [CAMERA], [TARGET], [ASSIST], [START], [UP], [DOWN], [LEFT], [RIGHT], KEYBOARD, JOYSTICK
    keyboard_mappings = [
        (61, 86),   # [OK] -> [O.K.]
        (62, 87),   # [CANCEL] -> [ABBRECHEN]
        (63, 88),   # [MENU] -> [MENÜ]
        (64, 89),   # [SWITCH] -> [UMSCHALTEN]
        (65, 90),   # [PAGEUP] -> [BILD HOCH]
        (66, 91),   # [PAGEDOWN] -> [BILD HERUNTER]
        (67, 92),   # [CAMERA] -> [KAMERA]
        (68, 93),   # [TARGET] -> [ZIEL]
        (69, 94),   # [ASSIST] -> [HILFE]
        (70, 95),   # [START] -> [START]
        (71, 96),   # [UP] -> [HERAUF]
        (72, 97),   # [DOWN] -> [UNTEN]
        (73, 98),   # [LEFT] -> [LINKS]
        (74, 99),   # [RIGHT] -> [RECHT]
        (75, 100),  # KEYBOARD -> TASTATUR
        (76, 101),  # JOYSTICK -> JOYSTICK
    ]

    for en_idx, de_idx in keyboard_mappings:
        if en_idx < len(english_strings) and de_idx < len(german_strings):
            es = english_strings[en_idx]
            gs = german_strings[de_idx]
            manual_mappings.append(Mapping(
                en_index=es.index,
                en_offset=es.offset,
                en_text=es.text,
                de_offset=gs.offset,
                de_text=gs.text,
                confidence="high",
                match_method="manual_group"
            ))
            used_german.add(gs.offset)

    # Press messages (English indices 58-60 map to German indices 82-85)
    press_mappings = [
        (58, 82),  # Press [CANCEL] to end. -> Mit [ABBRECHEN] beenden.
        (59, 83),  # Press [OK] to configure a key. -> Drücken Sie auf [O.K.] um die (split)
        (60, 85),  # Now press the new key. -> Bitte neue Taste drücken
    ]

    for en_idx, de_idx in press_mappings:
        if en_idx < len(english_strings) and de_idx < len(german_strings):
            es = english_strings[en_idx]
            gs = german_strings[de_idx]
            manual_mappings.append(Mapping(
                en_index=es.index,
                en_offset=es.offset,
                en_text=es.text,
                de_offset=gs.offset,
                de_text=gs.text,
                confidence="high",
                match_method="manual_group"
            ))
            used_german.add(gs.offset)

    # Keyboard/Joystick/Mouse key names (English indices 77-215 all map to German index 102 - packed binary structure)
    # German index 102 is a 3276-byte packed keyboard data structure containing all key/button names
    german_keyboard_block = german_strings[102]
    for en_idx in range(77, min(216, len(english_strings))):
        if en_idx < len(english_strings):
            es = english_strings[en_idx]
            manual_mappings.append(Mapping(
                en_index=es.index,
                en_offset=es.offset,
                en_text=es.text,
                de_offset=german_keyboard_block.offset,
                de_text=f"[KEYBOARD_DATA_BLOCK: {es.text}]",
                confidence="medium",
                match_method="keyboard_block"
            ))
    # Mark German keyboard block as used
    used_german.add(german_keyboard_block.offset)

    return manual_mappings

def create_mappings(english_strings: List[EnglishString],
                   german_strings: List[GermanString]) -> List[Mapping]:
    """Create complete mapping of English to German strings."""
    mappings = []
    used_german = set()

    # Statistics
    stats = {
        "exact": 0,
        "translation": 0,
        "context": 0,
        "manual_group": 0,
        "keyboard_block": 0,
        "none": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    print("Starting mapping process...")
    print(f"English strings: {len(english_strings)}")
    print(f"German strings: {len(german_strings)}")

    # Pass 0: Manual group mappings
    print("\nPass 0: Manual group mappings...")
    manual_maps = manual_group_mappings(english_strings, german_strings, used_german)

    # Count keyboard_block separately
    keyboard_count = sum(1 for m in manual_maps if m.match_method == "keyboard_block")
    manual_group_count = len(manual_maps) - keyboard_count

    mappings.extend(manual_maps)
    stats["manual_group"] = manual_group_count
    stats["keyboard_block"] = keyboard_count
    stats["high"] += manual_group_count
    stats["medium"] += keyboard_count
    print(f"Found {manual_group_count} manual group mappings")
    print(f"Found {keyboard_count} keyboard block mappings")

    # Pass 1: Exact matches
    print("\nPass 1: Exact matches...")
    for es in english_strings:
        # Skip if already mapped
        if any(m.en_index == es.index for m in mappings):
            continue

        result = find_exact_match(es.text, german_strings, used_german)
        if result:
            gs, method = result
            confidence = "exact"
            mappings.append(Mapping(
                en_index=es.index,
                en_offset=es.offset,
                en_text=es.text,
                de_offset=gs.offset,
                de_text=gs.text,
                confidence=confidence,
                match_method=method
            ))
            used_german.add(gs.offset)
            stats["exact"] += 1
            stats[confidence] += 1

    print(f"Found {stats['exact']} exact matches")

    # Pass 2: Known translations
    print("\nPass 2: Known translations...")
    for es in english_strings:
        # Skip if already mapped
        if any(m.en_index == es.index for m in mappings):
            continue

        result = find_translation_match(es.text, german_strings, used_german)
        if result:
            gs, method = result
            confidence = "high"
            mappings.append(Mapping(
                en_index=es.index,
                en_offset=es.offset,
                en_text=es.text,
                de_offset=gs.offset,
                de_text=gs.text,
                confidence=confidence,
                match_method=method
            ))
            used_german.add(gs.offset)
            stats["translation"] += 1
            stats[confidence] += 1

    print(f"Found {stats['translation']} translation matches")

    # Pass 3: Context-based matching
    print("\nPass 3: Context-based matching...")
    iterations = 0
    max_iterations = 10

    while iterations < max_iterations:
        found_any = False
        for es in english_strings:
            # Skip if already mapped
            if any(m.en_index == es.index for m in mappings):
                continue

            result = find_context_match(es.index, es.text, mappings, german_strings, used_german)
            if result:
                gs, method = result
                confidence = "medium"
                mappings.append(Mapping(
                    en_index=es.index,
                    en_offset=es.offset,
                    en_text=es.text,
                    de_offset=gs.offset,
                    de_text=gs.text,
                    confidence=confidence,
                    match_method=method
                ))
                used_german.add(gs.offset)
                stats["context"] += 1
                stats[confidence] += 1
                found_any = True

        iterations += 1
        if not found_any:
            break

    print(f"Found {stats['context']} context matches")

    # Pass 4: Fill remaining with "none"
    print("\nPass 4: Filling unmapped strings...")
    for es in english_strings:
        if not any(m.en_index == es.index for m in mappings):
            mappings.append(Mapping(
                en_index=es.index,
                en_offset=es.offset,
                en_text=es.text,
                de_offset="",
                de_text="",
                confidence="none",
                match_method="none"
            ))
            stats["none"] += 1

    # Sort by English index
    mappings.sort(key=lambda m: m.en_index)

    # Print statistics
    print("\n" + "="*60)
    print("MAPPING STATISTICS")
    print("="*60)
    print(f"Total mappings created: {len(mappings)}/{len(english_strings)}")
    print(f"Manual group mappings: {stats['manual_group']}")
    print(f"Keyboard block mappings: {stats['keyboard_block']}")
    print(f"Exact matches: {stats['exact']}")
    print(f"Translation matches: {stats['translation']}")
    print(f"Context matches: {stats['context']}")
    print(f"No match: {stats['none']}")
    print(f"\nConfidence distribution:")
    print(f"  Exact: {stats['exact']}")
    print(f"  High: {stats['translation'] + stats['manual_group']}")
    print(f"  Medium: {stats['context'] + stats['keyboard_block']}")
    print(f"  None: {stats['none']}")

    # Show unmapped English strings
    unmapped = [m for m in mappings if m.confidence == "none"]
    if unmapped:
        print(f"\n{len(unmapped)} unmapped English strings:")
        for m in unmapped[:20]:  # Show first 20
            print(f"  [{m.en_index}] {m.en_offset} | {m.en_text}")
        if len(unmapped) > 20:
            print(f"  ... and {len(unmapped) - 20} more")

    return mappings

def write_mappings(mappings: List[Mapping], output_path: str):
    """Write mappings to CSV file."""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['en_index', 'en_offset', 'en_text', 'de_offset', 'de_text', 'confidence', 'match_method'])
        for m in mappings:
            writer.writerow([m.en_index, m.en_offset, m.en_text, m.de_offset, m.de_text, m.confidence, m.match_method])

    print(f"\nMappings written to: {output_path}")

def main():
    # File paths
    english_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt"
    german_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_offsets.csv"
    output_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/mappings/english_german_mapping.csv"

    # Parse input files
    print("Parsing input files...")
    english_strings = parse_english_strings(english_path)
    german_strings = parse_german_strings(german_path)

    # Create mappings
    mappings = create_mappings(english_strings, german_strings)

    # Write output
    write_mappings(mappings, output_path)

if __name__ == "__main__":
    main()
