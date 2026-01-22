#!/usr/bin/env python3
"""
Delta Pattern Analysis: EN vs DE String Offsets
================================================
Created: 2026-01-03 16:25 JST
Session: 629f3c93-f884-439a-91d6-d77e7783bf9c

This script analyzes the relationship between English touphScript offsets
and German exe offsets to find potential patterns for programmatic extraction.

Key questions to answer:
1. Is there a constant delta between EN and DE offsets?
2. Are there regional deltas (different delta per string region)?
3. Can we use anchors to calculate offsets programmatically?
"""

import os
import sys
import json

# =============================================================================
# VERIFIED GERMAN CHARACTER ENCODING
# =============================================================================

FF7_GERMAN_DECODE_MAP = {
    0x66: 'Ü', 0x6A: 'ä', 0x7A: 'ö', 0x7E: 'ß', 0x7F: 'ü',
    0x61: 'á', 0x62: 'à', 0x63: 'â', 0x64: 'ã', 0x65: 'å',
    0x67: 'ç', 0x68: 'é', 0x69: 'è', 0x6B: 'ë',
    0x6C: 'í', 0x6D: 'ì', 0x6E: 'î', 0x6F: 'ï',
    0x70: 'ñ', 0x71: 'ó', 0x72: 'ò', 0x73: 'ô', 0x74: 'õ',
    0x76: '°', 0x77: '•', 0x78: '£',
}


def decode_ff7(data: bytes) -> str:
    """Decode FF7 encoded bytes."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        elif b in FF7_GERMAN_DECODE_MAP:
            result.append(FF7_GERMAN_DECODE_MAP[b])
        elif b == 0x00:
            result.append(' ')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))
    return ''.join(result).strip()


def encode_ff7_search(text: str) -> bytes:
    """Encode text for searching in exe."""
    CHAR_TO_BYTE = {
        'Ü': 0x66, 'ä': 0x6A, 'ö': 0x7A, 'ß': 0x7E, 'ü': 0x7F,
    }
    result = []
    for c in text:
        if c in CHAR_TO_BYTE:
            result.append(CHAR_TO_BYTE[c])
        elif c == ' ':
            result.append(0x00)
        elif 0x21 <= ord(c) <= 0x7F:
            result.append(ord(c) - 0x20)
    return bytes(result)


def load_english_offsets(filepath: str):
    """Load English touphScript offset table."""
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('[') and ']' in line:
                try:
                    idx_end = line.index(']')
                    idx = int(line[1:idx_end])
                    # Extract offset
                    parts = line.split()
                    if len(parts) >= 2:
                        offset_str = parts[1]
                        if offset_str.startswith('0x'):
                            offset = int(offset_str, 16)
                            # Extract text
                            if '|' in line:
                                text = line.split('|')[1].strip()
                                entries.append({
                                    'index': idx,
                                    'en_offset': offset,
                                    'en_text': text
                                })
                except:
                    pass
    return entries


def search_german_string(data: bytes, text: str, region_start: int = 0x580000, region_end: int = 0x5E0000):
    """Search for a German string in the exe and return all matches."""
    # Try to encode for search
    try:
        search_bytes = encode_ff7_search(text)
        if len(search_bytes) < 3:
            return []

        matches = []
        region = data[region_start:region_end]
        pos = 0
        while True:
            pos = region.find(search_bytes, pos)
            if pos == -1:
                break
            matches.append(region_start + pos)
            pos += 1
        return matches
    except:
        return []


def main():
    # Paths
    de_exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    en_ref_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt"
    output_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction"

    print("=" * 80)
    print("DELTA PATTERN ANALYSIS: EN vs DE OFFSETS")
    print("=" * 80)
    print()

    # Read German exe
    print("Loading German exe...")
    with open(de_exe_path, 'rb') as f:
        de_data = f.read()

    # Load English offsets
    print("Loading English offset table...")
    english = load_english_offsets(en_ref_path)
    print(f"  Loaded {len(english)} English entries")

    # Known German translations for key strings
    # These are VERIFIED translations from FF7 German
    known_translations = {
        0: ("Do you want to quit", "Möchten Sie Final"),
        3: ("Yes", "Ja"),
        4: ("No", "Nein"),
        5: ("Window color", "Fensterfarbe"),
        6: ("Sound", "Sound"),
        7: ("Controller", "Kontroller"),
        8: ("Cursor", "Cursor"),
        9: ("ATB", "ATB"),
        10: ("Battle speed", "Kampftempo"),
        11: ("Battle message", "Kampfmeldung"),
        12: ("Field message", "Feldmeldung"),
        13: ("Camera angle", "Kamerawinkel"),
        14: ("Select", "Auswählen"),
        15: ("Cancel", "Abbrechen"),
        16: ("Menu", "Menü"),
        29: ("restore", "Heilung"),
        30: ("attack", "Angriff"),
        31: ("indirect", "Indirekt"),
        38: ("Item", "Objekt"),
        39: ("Magic", "Zauber"),
        40: ("Materia", "Materia"),
        41: ("Equip", "Ausrüsten"),
        42: ("Status", "Status"),
        43: ("Order", "Anordnung"),
        44: ("Limit", "Limit"),
        45: ("Config", "Konfig"),
        47: ("Save", "Speichern"),
        48: ("Quit", "Verlassen"),
        75: ("KEYBOARD", "TASTATUR"),
        76: ("JOYSTICK", "JOYSTICK"),
    }

    # Find deltas for known translations
    print()
    print("=" * 80)
    print("SEARCHING FOR KNOWN GERMAN STRINGS")
    print("=" * 80)
    print()

    delta_data = []

    for idx, (en_text, de_text) in known_translations.items():
        # Find English entry
        en_entry = next((e for e in english if e['index'] == idx), None)
        if not en_entry:
            continue

        en_offset = en_entry['en_offset']

        # Search for German string
        matches = search_german_string(de_data, de_text)

        if matches:
            # Calculate deltas for each match
            for de_offset in matches:
                delta = de_offset - en_offset
                delta_data.append({
                    'index': idx,
                    'en_offset': en_offset,
                    'de_offset': de_offset,
                    'delta': delta,
                    'en_text': en_text,
                    'de_text': de_text
                })

            # Print first match
            de_offset = matches[0]
            delta = de_offset - en_offset
            print(f"[{idx:03d}] EN: 0x{en_offset:06X} -> DE: 0x{de_offset:06X}  Delta: {delta:+8d} (0x{delta:+06X})")
            print(f"       EN: '{en_text[:30]}' -> DE: '{de_text[:30]}'")
            if len(matches) > 1:
                print(f"       ({len(matches)} matches found)")
            print()
        else:
            print(f"[{idx:03d}] NOT FOUND: '{de_text}'")
            print()

    # Analyze delta patterns
    print("=" * 80)
    print("DELTA PATTERN ANALYSIS")
    print("=" * 80)
    print()

    if delta_data:
        deltas = [d['delta'] for d in delta_data]
        unique_deltas = list(set(deltas))

        print(f"Total matches found: {len(delta_data)}")
        print(f"Unique delta values: {len(unique_deltas)}")
        print()

        # Count frequency of each delta
        from collections import Counter
        delta_counts = Counter(deltas)
        print("Delta value frequency:")
        for delta, count in delta_counts.most_common(10):
            print(f"  Delta {delta:+8d} (0x{delta & 0xFFFFFFFF:08X}): {count} occurrences")

        print()

        # Check for regional patterns
        print("Regional analysis:")
        regions = {}
        for d in delta_data:
            region = d['en_offset'] & 0xFFF000  # Group by 4KB region
            if region not in regions:
                regions[region] = []
            regions[region].append(d['delta'])

        for region in sorted(regions.keys()):
            region_deltas = regions[region]
            if len(region_deltas) > 1:
                min_d = min(region_deltas)
                max_d = max(region_deltas)
                avg_d = sum(region_deltas) / len(region_deltas)
                variance = max_d - min_d
                print(f"  Region 0x{region:06X}: {len(region_deltas)} strings, delta range [{min_d:+d} to {max_d:+d}], variance: {variance}")

        # Save results
        output_file = os.path.join(output_dir, "delta_analysis_results.json")
        with open(output_file, 'w') as f:
            json.dump({
                'delta_data': delta_data,
                'unique_deltas': unique_deltas,
                'delta_frequency': dict(delta_counts),
            }, f, indent=2)
        print()
        print(f"Results saved to: {output_file}")

        # Conclusion
        print()
        print("=" * 80)
        print("CONCLUSION")
        print("=" * 80)
        print()

        if len(unique_deltas) == 1:
            print(f"CONSTANT DELTA FOUND: {unique_deltas[0]:+d} (0x{unique_deltas[0] & 0xFFFFFFFF:08X})")
            print("This means we CAN use programmatic extraction!")
        elif len(unique_deltas) <= 5:
            print(f"LIMITED DELTA VARIATION: {len(unique_deltas)} unique values")
            print("May be able to use regional deltas for extraction.")
            print(f"Most common delta: {delta_counts.most_common(1)[0][0]:+d}")
        else:
            print(f"VARIABLE DELTAS: {len(unique_deltas)} unique values")
            print("Deltas vary significantly - LLM extraction is the correct approach.")
            print("The delta drift issue identified in previous sessions is confirmed.")

    else:
        print("No matches found - check search patterns")


if __name__ == "__main__":
    main()
