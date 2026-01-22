#!/usr/bin/env python3
"""
FF7 German-to-English String Mapping via Multi-Anchor Pairs

Mission: Create a comprehensive mapping of ALL 767 touphScript strings from
English to their German equivalents using anchor-based regional search.

Approach:
1. Use known anchor pairs (EN text <-> DE text) to establish offset relationships
2. For each touphScript index, find the corresponding position in both EN and DE eStore exes
3. Extract German bytes and calculate offset deltas
4. Output comprehensive CSV with confidence ratings

Created: 2026-01-02 JST
Session: Agent 4 - German-to-English String Mapping
Context: Building comprehensive EN->DE mapping for FF7 menu text restoration
"""

import sys
import csv
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import IntEnum

sys.path.insert(0, str(Path(__file__).parent))
from generate_exe_hext import EN_OFFSETS, STRING_LENGTHS, STRING_TYPES

# =============================================================================
# FILE PATHS
# =============================================================================

STEAM_EN = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
ESTORE_EN = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe"
ESTORE_DE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

OUTPUT_CSV = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/data/german_string_mapping_complete.csv")

# =============================================================================
# SKIP REGIONS (cannot be mapped)
# =============================================================================

SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry (UNICODE) - 68 strings
SKIP_REGIONS.update(range(687, 712))   # Race ordinals (FFPADDED) - 25 strings
SKIP_REGIONS.update(range(712, 758))   # Chocobo names (ZEROTERM) - 46 strings

# =============================================================================
# ENCODING UTILITIES
# =============================================================================

def encode_ff7(text: str) -> bytes:
    """Encode ASCII text to FF7 bytes (ASCII - 0x20)."""
    result = []
    for c in text:
        if c == ' ':
            result.append(0x00)
        elif 0x21 <= ord(c) <= 0x7E:
            result.append(ord(c) - 0x20)
    return bytes(result)


def decode_ff7(data: bytes) -> str:
    """Decode FF7 bytes to readable text."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        if b == 0x00:
            result.append(' ')
        elif b == 0x6A:
            result.append('ä')
        elif b == 0x7A:
            result.append('ö')
        elif b == 0x7E:
            result.append('ß')
        elif b == 0x7F:
            result.append('ü')
        elif 0x01 <= b <= 0x9F:
            result.append(chr(b + 0x20))
        else:
            result.append(f'[{b:02X}]')
    return ''.join(result).strip()


def file_offset_to_va(offset: int) -> int:
    """Convert file offset to Virtual Address for HEXT."""
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


# =============================================================================
# ANCHOR DEFINITIONS
# Key insight: Both eStore EN and DE have strings in the same relative order,
# but at different base offsets. Finding anchors lets us calculate the delta.
# =============================================================================

@dataclass
class AnchorPair:
    """Defines an anchor pair for regional string mapping."""
    name: str
    en_text: str
    de_text: str
    search_start: int  # Start of search range in exes
    search_end: int    # End of search range
    expected_count: int  # Expected number of strings after this anchor


# Comprehensive anchor list - expanded from v2 generator
ANCHOR_PAIRS = [
    # Quit dialog (indices 0-4)
    AnchorPair("quit_dialog", "Yes", "Ja", 0x518000, 0x520000, 5),
    AnchorPair("quit_dialog_2", "Do you want to quit", "Möchten Sie Final", 0x518000, 0x5A0000, 5),

    # Config menu (indices 5-57)
    AnchorPair("config_menu", "Window color", "Fensterfarbe", 0x518000, 0x5A0000, 80),
    AnchorPair("config_sound", "Sound", "Sound", 0x518000, 0x5A0000, 50),
    AnchorPair("config_controller", "Controller", "Kontroller", 0x518000, 0x5A0000, 30),
    AnchorPair("config_battle_speed", "Battle speed", "Kampftempo", 0x518000, 0x5A0000, 40),

    # Keyboard config (indices 58-76)
    AnchorPair("keyboard_end", "Press [CANCEL] to end", "Mit [ABBRECHEN] beenden", 0x519000, 0x5A0000, 20),

    # Main menu (indices 38-57)
    AnchorPair("main_menu_item", "Item", "Objekt", 0x519000, 0x5A0000, 25),
    AnchorPair("main_menu_magic", "Magic", "Magie", 0x518000, 0x5A0000, 30),
    AnchorPair("main_menu_materia", "Materia", "Materia", 0x518000, 0x5A0000, 20),
    AnchorPair("main_menu_equip", "Equip", "Ausrüsten", 0x518000, 0x5A0000, 20),
    AnchorPair("main_menu_status", "Status", "Werte", 0x518000, 0x5A0000, 30),
    AnchorPair("main_menu_save", "Save", "Speichern", 0x518000, 0x5A0000, 30),
    AnchorPair("main_menu_config", "Config", "Konfig", 0x518000, 0x5A0000, 20),

    # Stats (indices 87-150)
    AnchorPair("stats_strength", "Strength", "Stärke", 0x51A000, 0x5A0000, 50),
    AnchorPair("stats_attack", "Attack", "Angriff", 0x51A000, 0x5A0000, 60),
    AnchorPair("stats_defense", "Defense", "Verteidigung", 0x51A000, 0x5A0000, 40),
    AnchorPair("stats_vitality", "Vitality", "Vitalität", 0x51A000, 0x5A0000, 30),

    # Equipment (indices 160-180)
    AnchorPair("equip_weapon", "Weapon", "Waffe", 0x51A000, 0x5A0000, 50),
    AnchorPair("equip_armor", "Armor", "Rüstung", 0x51A000, 0x5A0000, 30),
    AnchorPair("equip_accessory", "Accessory", "Accessoire", 0x51A000, 0x5A0000, 20),

    # Elements (indices 295-315)
    AnchorPair("element_fire", "Fire", "Feuer", 0x51D000, 0x5A0000, 30),
    AnchorPair("element_ice", "Ice", "Kälte", 0x51D000, 0x5A0000, 25),
    AnchorPair("element_lightning", "Lightning", "Blitz", 0x51D000, 0x5A0000, 25),
    AnchorPair("element_poison", "Poison", "Gift", 0x51D000, 0x5A0000, 25),

    # Status effects (indices 316-360)
    AnchorPair("status_death", "Death", "Tod", 0x51D000, 0x5A0000, 40),
    AnchorPair("status_sleep", "Sleep", "Schlaf", 0x51D000, 0x5A0000, 30),
    AnchorPair("status_confusion", "Confusion", "Verwirrung", 0x51D000, 0x5A0000, 25),
    AnchorPair("status_silence", "Silence", "Stummheit", 0x51D000, 0x5A0000, 20),
    AnchorPair("status_haste", "Haste", "Schnell", 0x51D000, 0x5A0000, 20),
    AnchorPair("status_barrier", "Barrier", "Barriere", 0x51D000, 0x5A0000, 20),

    # Battle commands (indices 380-420)
    AnchorPair("battle_change", "Change", "Wechseln", 0x51E000, 0x5A0000, 40),
    AnchorPair("battle_defend", "Defend", "Verteidigen", 0x51E000, 0x5A0000, 30),
    AnchorPair("battle_steal", "Steal", "Stehlen", 0x51E000, 0x5A0000, 25),
    AnchorPair("battle_throw", "Throw", "Werfen", 0x51E000, 0x5A0000, 20),
    AnchorPair("battle_escape", "Escape", "Fliehen", 0x51E000, 0x5A0000, 20),

    # Battle messages (indices 440-460)
    AnchorPair("battle_minimum", "Minimum", "Minimum", 0x51F000, 0x5A0000, 30),
    AnchorPair("battle_maximum", "Maximum", "Maximum", 0x51F000, 0x5A0000, 25),
    AnchorPair("battle_miss", "Missed", "Verfehlt", 0x51F000, 0x5A0000, 20),
    AnchorPair("battle_critical", "Critical", "Kritisch", 0x51F000, 0x5A0000, 20),

    # Shop menu (indices 560-590)
    AnchorPair("shop_welcome", "Welcome!", "Willkommen!", 0x555000, 0x5A0000, 20),
    AnchorPair("shop_buy", "Buy", "Kaufen", 0x555000, 0x5A0000, 60),
    AnchorPair("shop_sell", "Sell", "Verkaufen", 0x555000, 0x5A0000, 30),
    AnchorPair("shop_exit", "Exit", "Verlassen", 0x555000, 0x5A0000, 25),
    AnchorPair("shop_owned", "Owned:", "Im Besitz:", 0x555000, 0x5A0000, 15),

    # Materia menu (indices 400-440)
    AnchorPair("materia_check", "Check", "Prüfen", 0x520000, 0x5A0000, 30),
    AnchorPair("materia_exchange", "Exchange", "Tauschen", 0x520000, 0x5A0000, 25),
    AnchorPair("materia_summon", "Summon", "Herbeiruf", 0x520000, 0x5A0000, 30),
    AnchorPair("materia_command", "Command", "Kommando", 0x520000, 0x5A0000, 25),
    AnchorPair("materia_support", "Support", "Unterstützung", 0x520000, 0x5A0000, 20),
    AnchorPair("materia_master", "MASTER", "MEISTER", 0x520000, 0x5A0000, 15),

    # Limit break (indices 330-350)
    AnchorPair("limit_set", "Set", "Einrichten", 0x51F000, 0x5A0000, 25),
    AnchorPair("limit_level1", "LEVEL 1", "STUFE 1", 0x51F000, 0x5A0000, 20),

    # Item menu (indices 530-560)
    AnchorPair("item_use", "Use", "Verwenden", 0x555000, 0x5A0000, 30),
    AnchorPair("item_arrange", "Arrange", "Ordnen", 0x555000, 0x5A0000, 25),
    AnchorPair("item_key_items", "Key Items", "Schlüsselobjekte", 0x555000, 0x5A0000, 20),

    # Save/Load (indices 640-670)
    AnchorPair("save_select", "Select a save data file", "Speicherdatei auswählen", 0x570000, 0x5A0000, 25),
    AnchorPair("save_1", "Save 1", "Speicher 1", 0x57B000, 0x5C0000, 20),
    AnchorPair("save_new_game", "New Game", "Neues Spiel", 0x57B000, 0x5C0000, 15),
    AnchorPair("save_continue", "Continue", "Fortsetzen", 0x57B000, 0x5C0000, 15),

    # Gold Saucer / Battle Arena (indices 600-640)
    AnchorPair("gs_raise", "How much will you raise", "Wieviel setzen Sie", 0x550000, 0x5A0000, 20),
    AnchorPair("gs_battle_points", "Battle Points", "Kampfpunkte", 0x550000, 0x5A0000, 15),

    # Chocobo related (after skip region)
    AnchorPair("chocobo_racing", "GP", "GP", 0x57B000, 0x5C0000, 10),
]

# =============================================================================
# STRING EXTRACTION AND MATCHING
# =============================================================================

def extract_strings_from_anchor(data: bytes, anchor_bytes: bytes,
                                search_start: int, search_end: int,
                                max_strings: int = 300) -> List[Tuple[int, bytes, str]]:
    """Extract consecutive strings starting from an anchor position."""

    # Find anchor in search range
    anchor_pos = data.find(anchor_bytes, search_start, search_end)
    if anchor_pos == -1:
        return []

    strings = []
    pos = anchor_pos

    while len(strings) < max_strings and pos < min(search_end, len(data) - 2):
        # Find next FF terminator
        next_ff = data.find(b'\xff', pos, min(pos + 200, search_end))
        if next_ff == -1:
            break

        string_bytes = data[pos:next_ff + 1]
        if len(string_bytes) >= 2:
            decoded = decode_ff7(string_bytes)
            strings.append((pos, string_bytes, decoded))

        # Skip to next string (past any padding zeros)
        pos = next_ff + 1
        while pos < search_end and data[pos] == 0x00:
            pos += 1

    return strings


def build_estore_to_de_mapping(estore_data: bytes, de_data: bytes,
                                anchor: AnchorPair) -> Dict[int, Tuple[int, bytes, str]]:
    """Build mapping from eStore EN offset to DE offset and bytes."""

    # Encode anchor texts to FF7 bytes
    # Handle German special characters for DE anchor
    en_anchor_bytes = encode_ff7(anchor.en_text)

    # For DE text, we need to handle umlauts
    de_anchor = anchor.de_text
    de_bytes = []
    for c in de_anchor:
        if c == ' ':
            de_bytes.append(0x00)
        elif c == 'ä':
            de_bytes.append(0x6A)
        elif c == 'ö':
            de_bytes.append(0x7A)
        elif c == 'ü':
            de_bytes.append(0x7F)
        elif c == 'ß':
            de_bytes.append(0x7E)
        elif 0x21 <= ord(c) <= 0x7E:
            de_bytes.append(ord(c) - 0x20)
    de_anchor_bytes = bytes(de_bytes)

    # Extract strings from both exes starting at anchor
    en_strings = extract_strings_from_anchor(
        estore_data, en_anchor_bytes,
        anchor.search_start, anchor.search_end,
        anchor.expected_count
    )

    de_strings = extract_strings_from_anchor(
        de_data, de_anchor_bytes,
        anchor.search_start, anchor.search_end,
        anchor.expected_count
    )

    if not en_strings or not de_strings:
        return {}

    # Create mapping: eStore EN offset -> (DE offset, DE bytes, DE text)
    mapping = {}
    for i in range(min(len(en_strings), len(de_strings))):
        en_offset, en_bytes, en_text = en_strings[i]
        de_offset, de_bytes, de_text = de_strings[i]
        mapping[en_offset] = (de_offset, de_bytes, de_text)

    return mapping


# =============================================================================
# MAIN MAPPING LOGIC
# =============================================================================

@dataclass
class MappingResult:
    """Result of mapping a single touphScript string."""
    idx: int
    steam_offset: int
    steam_va: int
    estore_en_offset: Optional[int]
    estore_de_offset: Optional[int]
    en_text: str
    de_text: str
    de_bytes: Optional[bytes]
    anchor_used: str
    confidence: str
    string_type: int
    length: int
    status: str  # MAPPED, SKIPPED, UNMAPPED, IDENTICAL


def create_comprehensive_mapping() -> List[MappingResult]:
    """Create complete mapping for all 767 touphScript strings."""

    print("=" * 70)
    print("FF7 German-to-English String Mapper")
    print("=" * 70)

    # Load exe files
    print("\nLoading exe files...")
    try:
        with open(STEAM_EN, 'rb') as f:
            steam_data = f.read()
        with open(ESTORE_EN, 'rb') as f:
            estore_data = f.read()
        with open(ESTORE_DE, 'rb') as f:
            de_data = f.read()
    except FileNotFoundError as e:
        print(f"ERROR: Could not load exe file: {e}")
        sys.exit(1)

    print(f"  Steam EN: {len(steam_data):,} bytes")
    print(f"  eStore EN: {len(estore_data):,} bytes")
    print(f"  eStore DE: {len(de_data):,} bytes")

    # Build combined mapping from all anchor pairs
    print(f"\nBuilding mapping from {len(ANCHOR_PAIRS)} anchor pairs...")
    estore_to_de: Dict[int, Tuple[int, bytes, str, str]] = {}  # offset -> (de_offset, de_bytes, de_text, anchor_name)

    for anchor in ANCHOR_PAIRS:
        mapping = build_estore_to_de_mapping(estore_data, de_data, anchor)
        if mapping:
            for estore_off, (de_off, de_bytes, de_text) in mapping.items():
                if estore_off not in estore_to_de:  # Don't overwrite existing
                    estore_to_de[estore_off] = (de_off, de_bytes, de_text, anchor.name)
            print(f"  [{anchor.name}] '{anchor.en_text}' -> '{anchor.de_text}': {len(mapping)} strings")
        else:
            print(f"  [{anchor.name}] '{anchor.en_text}' -> '{anchor.de_text}': NOT FOUND")

    print(f"\nTotal unique eStore positions mapped: {len(estore_to_de)}")

    # Now map each touphScript index
    print(f"\nMapping {len(EN_OFFSETS)} touphScript strings...")
    results: List[MappingResult] = []

    stats = {
        'mapped': 0,
        'skipped': 0,
        'unmapped': 0,
        'identical': 0,
        'short': 0
    }

    for idx, steam_offset in enumerate(EN_OFFSETS):
        if idx >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[idx]
        string_type = STRING_TYPES[idx] if idx < len(STRING_TYPES) else 0
        steam_va = file_offset_to_va(steam_offset)

        # Read Steam EN string
        steam_bytes = steam_data[steam_offset:steam_offset + length]
        en_text = decode_ff7(steam_bytes)

        # Check if in skip region
        if idx in SKIP_REGIONS:
            results.append(MappingResult(
                idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                estore_en_offset=None, estore_de_offset=None,
                en_text=en_text, de_text="", de_bytes=None,
                anchor_used="", confidence="N/A",
                string_type=string_type, length=length, status="SKIPPED"
            ))
            stats['skipped'] += 1
            continue

        # Skip very short strings
        if length <= 1 or len(en_text.strip()) == 0:
            results.append(MappingResult(
                idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                estore_en_offset=None, estore_de_offset=None,
                en_text=en_text, de_text="", de_bytes=None,
                anchor_used="", confidence="N/A",
                string_type=string_type, length=length, status="SHORT"
            ))
            stats['short'] += 1
            continue

        # Find this string in eStore EN
        # Use first N bytes before FF terminator as search pattern
        ff_pos = steam_bytes.find(b'\xff')
        search_len = min(10, ff_pos if ff_pos != -1 else 10)
        search_bytes = steam_bytes[:search_len]

        # Search for exact match in eStore menu region
        estore_pos = estore_data.find(search_bytes, 0x510000, 0x5C0000)

        if estore_pos != -1 and estore_pos in estore_to_de:
            de_off, de_bytes, de_text, anchor_name = estore_to_de[estore_pos]

            # Check if EN and DE are identical
            if de_text.strip() == en_text.strip():
                results.append(MappingResult(
                    idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                    estore_en_offset=estore_pos, estore_de_offset=de_off,
                    en_text=en_text, de_text=de_text, de_bytes=de_bytes,
                    anchor_used=anchor_name, confidence="HIGH",
                    string_type=string_type, length=length, status="IDENTICAL"
                ))
                stats['identical'] += 1
            else:
                results.append(MappingResult(
                    idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                    estore_en_offset=estore_pos, estore_de_offset=de_off,
                    en_text=en_text, de_text=de_text, de_bytes=de_bytes,
                    anchor_used=anchor_name, confidence="HIGH",
                    string_type=string_type, length=length, status="MAPPED"
                ))
                stats['mapped'] += 1
        else:
            # Not found in mapping - try direct search in DE exe
            # This is a fallback with lower confidence
            de_pos = de_data.find(search_bytes, 0x580000, 0x5C0000)

            if de_pos != -1:
                # Found at different position - extract string
                next_ff = de_data.find(b'\xff', de_pos, de_pos + 200)
                if next_ff != -1:
                    de_bytes = de_data[de_pos:next_ff + 1]
                    de_text = decode_ff7(de_bytes)

                    results.append(MappingResult(
                        idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                        estore_en_offset=estore_pos if estore_pos != -1 else None,
                        estore_de_offset=de_pos,
                        en_text=en_text, de_text=de_text, de_bytes=de_bytes,
                        anchor_used="direct_search", confidence="LOW",
                        string_type=string_type, length=length, status="MAPPED"
                    ))
                    stats['mapped'] += 1
                else:
                    results.append(MappingResult(
                        idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                        estore_en_offset=estore_pos if estore_pos != -1 else None,
                        estore_de_offset=None,
                        en_text=en_text, de_text="", de_bytes=None,
                        anchor_used="", confidence="N/A",
                        string_type=string_type, length=length, status="UNMAPPED"
                    ))
                    stats['unmapped'] += 1
            else:
                results.append(MappingResult(
                    idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                    estore_en_offset=estore_pos if estore_pos != -1 else None,
                    estore_de_offset=None,
                    en_text=en_text, de_text="", de_bytes=None,
                    anchor_used="", confidence="N/A",
                    string_type=string_type, length=length, status="UNMAPPED"
                ))
                stats['unmapped'] += 1

    # Print summary
    print("\n" + "=" * 70)
    print("MAPPING SUMMARY")
    print("=" * 70)
    print(f"  Total strings: {len(EN_OFFSETS)}")
    print(f"  Mapped (translated): {stats['mapped']}")
    print(f"  Identical (EN=DE): {stats['identical']}")
    print(f"  Skipped (UNICODE/etc): {stats['skipped']}")
    print(f"  Short/Empty: {stats['short']}")
    print(f"  Unmapped: {stats['unmapped']}")
    print(f"  Success rate: {(stats['mapped'] + stats['identical']) / len(EN_OFFSETS) * 100:.1f}%")

    return results


def write_csv(results: List[MappingResult], output_path: Path):
    """Write mapping results to CSV file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'idx', 'steam_offset', 'steam_va', 'estore_en_offset', 'estore_de_offset',
            'en_text', 'de_text', 'de_bytes_hex', 'anchor_used', 'confidence',
            'string_type', 'length', 'status'
        ])

        for r in results:
            de_bytes_hex = r.de_bytes.hex() if r.de_bytes else ""
            writer.writerow([
                r.idx,
                f"0x{r.steam_offset:X}",
                f"0x{r.steam_va:X}",
                f"0x{r.estore_en_offset:X}" if r.estore_en_offset else "",
                f"0x{r.estore_de_offset:X}" if r.estore_de_offset else "",
                r.en_text,
                r.de_text,
                de_bytes_hex,
                r.anchor_used,
                r.confidence,
                r.string_type,
                r.length,
                r.status
            ])

    print(f"\nWrote {len(results)} entries to: {output_path}")


def print_unmapped_analysis(results: List[MappingResult]):
    """Analyze and print unmapped regions for debugging."""

    print("\n" + "=" * 70)
    print("UNMAPPED STRINGS ANALYSIS")
    print("=" * 70)

    unmapped = [r for r in results if r.status == "UNMAPPED"]

    if not unmapped:
        print("All mappable strings have been mapped!")
        return

    # Group by index ranges
    ranges = []
    start = unmapped[0].idx
    prev = start

    for r in unmapped[1:]:
        if r.idx == prev + 1:
            prev = r.idx
        else:
            ranges.append((start, prev))
            start = r.idx
            prev = start
    ranges.append((start, prev))

    print(f"\nUnmapped index ranges ({len(unmapped)} total):")
    for start, end in ranges[:20]:  # Show first 20 ranges
        count = end - start + 1
        sample = next((r for r in unmapped if r.idx == start), None)
        if sample:
            print(f"  [{start}-{end}] ({count} strings): '{sample.en_text[:40]}...'")

    if len(ranges) > 20:
        print(f"  ... and {len(ranges) - 20} more ranges")


# =============================================================================
# MAIN
# =============================================================================

def main():
    results = create_comprehensive_mapping()
    write_csv(results, OUTPUT_CSV)
    print_unmapped_analysis(results)

    # Summary of what needs more anchors
    high_conf = len([r for r in results if r.confidence == "HIGH"])
    low_conf = len([r for r in results if r.confidence == "LOW"])
    unmapped = len([r for r in results if r.status == "UNMAPPED"])

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print(f"  HIGH confidence mappings: {high_conf}")
    print(f"  LOW confidence mappings: {low_conf}")
    print(f"  Unmapped (need new anchors): {unmapped}")

    if unmapped > 0:
        print("\nTo improve coverage, add anchor pairs for unmapped regions.")
        print("Check the CSV for patterns in unmapped string indices.")


if __name__ == "__main__":
    main()
