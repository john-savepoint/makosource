#!/usr/bin/env python3
"""
Generate Final German HEXT from Haiku-discovered offsets

Reads the German exe at the discovered DE offsets and generates
HEXT patches for the Steam EN exe.

Created: 2026-01-03 13:45 JST
Session: 8bc98f0a-abab-49e6-acdd-56dd38e9d149
"""

import csv
import re
from pathlib import Path
from datetime import datetime

# =============================================================================
# PATHS
# =============================================================================

GERMAN_EXE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe")
OUTPUT_DIR = Path(__file__).parent

# =============================================================================
# TOUPHSCRIPT STRING LENGTHS (for padding)
# =============================================================================

STRING_LENGTHS = [
    30, 30, 30, 4, 4, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 6, 6, 6, 25, 25,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
    50, 50, 50, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 12, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 16, 16, 8, 16, 4, 4, 4, 4, 4, 4, 4, 4, 4, 12, 12, 8, 12,
    12, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 12, 12, 12, 8, 12, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 8, 8, 8, 8, 8, 12, 8, 8, 8, 4, 8, 8, 8, 8, 8, 4, 4, 4, 4, 4, 8,
    8, 12, 4, 16, 12, 4, 8, 12, 8, 8, 4, 12, 12, 16, 12, 8, 8, 12, 8, 4, 8,
    8, 8, 4, 8, 12, 8, 8, 12, 12, 8, 12, 12, 12, 4, 8, 8, 8, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 8, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11,
    10, 10, 10, 10, 10, 10, 28, 4, 8, 16, 16, 24, 22, 22, 22, 32, 32, 32, 32,
    32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
    32, 32, 32, 34, 34, 34, 8, 38, 38, 38, 38, 38, 38, 22, 22, 22, 36, 36,
    36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 36, 36, 36,
    36, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34,
    34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 22, 22, 22, 22, 20, 20, 20,
    20, 20, 20, 20, 20, 46, 46, 46, 46, 46, 36, 36, 36, 36, 36, 36, 36, 36,
    36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
    36, 36, 36, 36, 36, 36, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 8, 16, 16, 16,
    16, 16, 8, 12, 8, 8, 8, 12, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 12, 8, 12, 8,
    8, 8, 8, 12, 12, 12, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 16,
    16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
]

EN_OFFSETS = [
    0x518370, 0x51838E, 0x5183AC, 0x5183D0, 0x5183D4, 0x5188A8, 0x5188D8, 0x518908,
    0x518938, 0x518968, 0x518998, 0x5189C8, 0x5189F8, 0x518A28, 0x518A58, 0x518A88,
    0x518AB8, 0x518C08, 0x518C38, 0x518C68, 0x518C98, 0x518CC8, 0x518CF8, 0x518D28,
    0x518D58, 0x518D88, 0x518DE8, 0x518E18, 0x518ED8, 0x518F08, 0x518F38, 0x518F68,
    0x518FC8, 0x519238, 0x51923E, 0x519244, 0x519288, 0x5192A1, 0x5192C0, 0x5192D4,
    0x5192E8, 0x5192FC, 0x519310, 0x519324, 0x519338, 0x51934C, 0x519360, 0x519374,
    0x519388, 0x51939C, 0x5193D8, 0x5193EC, 0x519400, 0x519414, 0x519428, 0x519450,
    0x519464, 0x519478, 0x5196B0, 0x5196E2, 0x519714, 0x519746, 0x519778, 0x5197AA,
    0x5197DC, 0x51980E, 0x519840, 0x519872, 0x5198A4, 0x5198D6, 0x519908, 0x51993A,
    0x51996C, 0x51999E, 0x5199D0, 0x519A02, 0x519A34,
]

# =============================================================================
# HAIKU-DISCOVERED MAPPINGS + KEYBOARD LABELS
# =============================================================================

# From Haiku analysis and manual discovery - confirmed DE offsets for each EN index
HAIKU_MAPPINGS = [
    # Quit dialog (indices 0-4) - manually confirmed from dump
    (0, 0x58FBAF, "Möchten Sie Final"),
    (1, 0x58FBC3, "Fantasy VII verlassen und"),
    (2, 0x58FBE8, "zu Windows zurückkehren?"),
    (3, 0x58FC05, "Ja"),
    (4, 0x58FC13, "Nein"),

    # Config menu - from Haiku CSV
    (5, 0x5900EE, "Fensterfarbe"),
    (6, 0x5900FD, "Sound"),
    (7, 0x59012C, "Kontroller"),
    (8, 0x590167, "Cursor"),
    (9, 0x590199, "ATB"),
    (10, 0x5901CC, "Kampftempo"),
    (11, 0x590209, "Kampfmeldung"),
    (12, 0x590241, "Feldmeldung"),
    (13, 0x590276, "Kamerawinkel"),
    (14, 0x5902AD, "Auswählen"),
    (15, 0x5902E0, "Abbrechen"),
    (16, 0x590316, "Menü"),

    # More from Haiku
    (24, 0x590607, "Auto"),
    (25, 0x59063B, "Fest"),
    (29, 0x5907F2, "Heilung"),
    (30, 0x590824, "Angriff"),
    (31, 0x59085A, "Indirekt"),

    # Main menu
    (38, 0x590C68, "Objekt"),
    (39, 0x590C6F, "Zauber"),
    (40, 0x590C83, "Materia"),
    (41, 0x590C98, "Ausrüsten"),
    (44, 0x590CD2, "Limit"),
    (45, 0x590CE6, "Konfig"),
    (46, 0x590CFB, "PHS"),
    (47, 0x590D0C, "Speichern"),
    (48, 0x590D26, "Verlassen"),
    (49, 0x590D3A, "Anfänger"),
    (50, 0x590D77, "Zeit"),
    (51, 0x590D85, "Gil"),

    # Keyboard/Controller labels (indices 58-76) - found via screenshot/manual search
    (58, 0x591058, "Mit [ABBRECHEN] beenden."),
    (59, 0x5910A4, "[O.K.] um die Tastenbelegung zu konfigurieren."),
    (60, 0x5910F1, "Bitte neue Taste drücken"),
    (61, 0x591126, "[O.K.]"),
    (62, 0x591159, "[ABBRECHEN]"),
    (63, 0x591190, "[MENÜ]"),
    (64, 0x5911D2, "[UMSCHALTEN]"),
    (65, 0x591238, "[BILD HOCH]"),
    (66, 0x591274, "[BILD HERUNTER]"),
    (67, 0x5912B0, "[KAMERA]"),
    (68, 0x5912EC, "[ZIEL]"),
    (69, 0x591328, "[HILFE]"),
    (70, 0x591364, "[START]"),
    (71, 0x5913A0, "[HERAUF]"),
    (72, 0x5913DC, "[UNTEN]"),
    (73, 0x591418, "[LINKS]"),
    (74, 0x591454, "[RECHT]"),
    (75, 0x591490, "TASTATUR"),
    (76, 0x5914CC, "JOYSTICK"),
]


def file_offset_to_va(offset: int) -> int:
    """Convert Steam EN file offset to Virtual Address for HEXT."""
    return offset + 0x400800


def main():
    """Generate HEXT from discovered mappings."""

    print("Loading German exe...")
    with open(GERMAN_EXE, 'rb') as f:
        de_data = f.read()

    patches = []

    print(f"Processing {len(HAIKU_MAPPINGS)} discovered mappings...")

    for en_index, de_offset, de_text in HAIKU_MAPPINGS:
        if en_index >= len(EN_OFFSETS) or en_index >= len(STRING_LENGTHS):
            print(f"  Skipping index {en_index} - out of range")
            continue

        en_offset = EN_OFFSETS[en_index]
        slot_length = STRING_LENGTHS[en_index]

        # Read raw bytes from German exe
        raw_bytes = de_data[de_offset:de_offset + slot_length + 10]  # Read extra to find terminator

        # Find FF terminator
        term_pos = -1
        for i, b in enumerate(raw_bytes):
            if b == 0xFF:
                term_pos = i
                break

        if term_pos == -1:
            # No terminator found, use slot length
            actual_bytes = raw_bytes[:slot_length-1] + b'\xFF'
        else:
            actual_bytes = raw_bytes[:term_pos + 1]

        # Pad to slot length
        if len(actual_bytes) < slot_length:
            actual_bytes = actual_bytes + b'\x00' * (slot_length - len(actual_bytes))
        else:
            actual_bytes = actual_bytes[:slot_length]

        va = file_offset_to_va(en_offset)
        hex_str = ' '.join(f'{b:02X}' for b in actual_bytes)

        patches.append({
            'index': en_index,
            'en_offset': en_offset,
            'de_offset': de_offset,
            'va': va,
            'de_text': de_text,
            'hex': hex_str,
            'length': slot_length
        })

    # Sort by index
    patches.sort(key=lambda x: x['index'])

    # Write HEXT file
    output_file = OUTPUT_DIR / 'german_menu_final.txt'
    with open(output_file, 'w') as f:
        f.write("# =================================================================\n")
        f.write("# German Menu Text Patch for FF7 Steam English\n")
        f.write("# =================================================================\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Session: 8bc98f0a-abab-49e6-acdd-56dd38e9d149\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# VA = FileOffset + 0x400800\n")
        f.write("# German bytes extracted directly from ff7_de.exe\n")
        f.write("# " + "=" * 65 + "\n\n")

        for p in patches:
            f.write(f"# [{p['index']:03d}] \"{p['de_text']}\"\n")
            f.write(f"# EN: 0x{p['en_offset']:08X}, DE: 0x{p['de_offset']:08X}\n")
            f.write(f"{p['va']:06X} = {p['hex']}\n\n")

    print(f"\nWrote {len(patches)} patches to {output_file}")

    # Copy to game directory
    game_hext = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    print(f"Copying to {game_hext}...")

    import shutil
    shutil.copy(output_file, game_hext)
    print("Done!")


if __name__ == '__main__':
    main()
