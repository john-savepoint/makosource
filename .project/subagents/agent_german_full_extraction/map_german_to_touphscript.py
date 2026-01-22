#!/usr/bin/env python3
"""
German FF7 Menu Strings → touphScript Index Mapper

Maps German menu strings (indices 38-48) to their English touphScript equivalents
for hext patch generation.

Created: 2026-01-03 16:35 JST
Session: e4b8c9f0-8bc9-4e6a-9d12-3f4a5b6c7d8e
Purpose: Create definitive mapping between German offsets and English indices
"""

import csv
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class MenuString:
    """Represents a menu string with its offsets and translations."""
    touphscript_index: int
    en_text: str
    de_text: str
    de_file_offset: int
    en_file_offset: int
    de_hex_bytes: str
    notes: str = ""

    @property
    def de_virtual_addr(self) -> int:
        """Calculate German virtual address (VA = FileOffset + 0x400800)."""
        return self.de_file_offset + 0x400800

    @property
    def en_virtual_addr(self) -> int:
        """Calculate English virtual address."""
        return self.en_file_offset + 0x400800

    @property
    def offset_delta(self) -> int:
        """Calculate offset difference between German and English."""
        return self.de_file_offset - self.en_file_offset


# English touphScript offsets for menu items (indices 38-48)
EN_MENU_OFFSETS = {
    38: 0x5192C0,  # Item
    39: 0x5192D4,  # Magic
    40: 0x5192E8,  # Materia
    41: 0x5192FC,  # Equip
    42: 0x519310,  # Status
    43: 0x519324,  # Order
    44: 0x519338,  # Limit
    45: 0x51934C,  # Config
    46: 0x519360,  # PHS
    47: 0x519374,  # Save
    48: 0x519388,  # Quit
}

# German menu strings with their offsets and hex bytes
DE_MENU_STRINGS = [
    MenuString(
        touphscript_index=38,
        en_text="Item",
        de_text="Objekt",
        de_file_offset=0x590C68,
        en_file_offset=EN_MENU_OFFSETS[38],
        de_hex_bytes="2F 42 4A 45 4B 54",
        notes="German 'Objekt' = English 'Item'"
    ),
    MenuString(
        touphscript_index=39,
        en_text="Magic",
        de_text="Zauber",
        de_file_offset=0x590C6F,
        en_file_offset=EN_MENU_OFFSETS[39],
        de_hex_bytes="3A 41 55 42 45 52",
        notes="German 'Zauber' = English 'Magic'"
    ),
    MenuString(
        touphscript_index=40,
        en_text="Materia",
        de_text="Materia",
        de_file_offset=0x590C83,
        en_file_offset=EN_MENU_OFFSETS[40],
        de_hex_bytes="2D 41 54 45 52 49 41",
        notes="Same in both languages"
    ),
    MenuString(
        touphscript_index=41,
        en_text="Equip",
        de_text="Ausrüsten",
        de_file_offset=0x590C98,
        en_file_offset=EN_MENU_OFFSETS[41],
        de_hex_bytes="21 55 53 52 7F 53 54 45 4E",
        notes="Contains ü-umlaut (0x7F)"
    ),
    MenuString(
        touphscript_index=42,
        en_text="Status",
        de_text="Werte",
        de_file_offset=0x590CAE,
        en_file_offset=EN_MENU_OFFSETS[42],
        de_hex_bytes="37 45 52 54 45",
        notes="German uses 'Werte' (values) instead of 'Status'"
    ),
    MenuString(
        touphscript_index=43,
        en_text="Order",
        de_text="Reihe",
        de_file_offset=0x590CBE,
        en_file_offset=EN_MENU_OFFSETS[43],
        de_hex_bytes="32 45 49 48 45",
        notes="German 'Reihe' (row/sequence)"
    ),
    MenuString(
        touphscript_index=44,
        en_text="Limit",
        de_text="Limit",
        de_file_offset=0x590CD2,
        en_file_offset=EN_MENU_OFFSETS[44],
        de_hex_bytes="2C 49 4D 49 54",
        notes="Same in both languages"
    ),
    MenuString(
        touphscript_index=45,
        en_text="Config",
        de_text="Konfig",
        de_file_offset=0x590CE6,
        en_file_offset=EN_MENU_OFFSETS[45],
        de_hex_bytes="2B 4F 4E 46 49 47",
        notes="German abbreviation of 'Konfiguration'"
    ),
    MenuString(
        touphscript_index=46,
        en_text="PHS",
        de_text="PHS",
        de_file_offset=0x590CFB,
        en_file_offset=EN_MENU_OFFSETS[46],
        de_hex_bytes="30 28 33",
        notes="Acronym, same in both languages"
    ),
    MenuString(
        touphscript_index=47,
        en_text="Save",
        de_text="Speichern",
        de_file_offset=0x590D0C,
        en_file_offset=EN_MENU_OFFSETS[47],
        de_hex_bytes="33 50 45 49 43 48 45 52 4E",
        notes="German infinitive 'to save'"
    ),
    MenuString(
        touphscript_index=48,
        en_text="Quit",
        de_text="Verlassen",
        de_file_offset=0x590D26,
        en_file_offset=EN_MENU_OFFSETS[48],
        de_hex_bytes="36 45 52 4C 41 53 53 45 4E",
        notes="German infinitive 'to leave/quit'"
    ),
]


def print_mapping_table():
    """Print a comprehensive mapping table."""
    print("=" * 120)
    print("FF7 German Menu Strings → touphScript Index Mapping")
    print("=" * 120)
    print()

    # Header
    print(f"{'Idx':<5} {'EN Text':<12} {'DE Text':<12} {'DE Offset':<12} {'EN Offset':<12} {'DE VA':<12} {'EN VA':<12} {'Delta':<12}")
    print("-" * 120)

    for item in DE_MENU_STRINGS:
        print(f"{item.touphscript_index:<5} "
              f"{item.en_text:<12} "
              f"{item.de_text:<12} "
              f"0x{item.de_file_offset:08X}  "
              f"0x{item.en_file_offset:08X}  "
              f"0x{item.de_virtual_addr:08X}  "
              f"0x{item.en_virtual_addr:08X}  "
              f"+0x{item.offset_delta:05X}")

    print()
    print("=" * 120)


def print_hex_bytes_table():
    """Print hex bytes for each string."""
    print()
    print("=" * 100)
    print("Hex Byte Representation")
    print("=" * 100)
    print()

    for item in DE_MENU_STRINGS:
        print(f"[{item.touphscript_index:02d}] {item.de_text:<12} | {item.de_hex_bytes}")
        print(f"     {item.notes}")
        print()


def export_to_csv(output_path: Path):
    """Export mapping to CSV file."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'touphscript_index',
            'en_text',
            'de_text',
            'de_file_offset',
            'en_file_offset',
            'de_virtual_addr',
            'en_virtual_addr',
            'offset_delta',
            'de_hex_bytes',
            'notes'
        ])

        for item in DE_MENU_STRINGS:
            writer.writerow([
                item.touphscript_index,
                item.en_text,
                item.de_text,
                f"0x{item.de_file_offset:08X}",
                f"0x{item.en_file_offset:08X}",
                f"0x{item.de_virtual_addr:08X}",
                f"0x{item.en_virtual_addr:08X}",
                f"+0x{item.offset_delta:05X}",
                item.de_hex_bytes,
                item.notes
            ])

    print(f"Exported mapping to: {output_path}")


def generate_hext_patch(output_path: Path):
    """Generate hext patch to replace English menu with German."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# =================================================================\n")
        f.write("# German Menu Text Patch for FF7 Steam English\n")
        f.write("# =================================================================\n")
        f.write("# Generated: 2026-01-03 16:35 JST\n")
        f.write("# Session: e4b8c9f0-8bc9-4e6a-9d12-3f4a5b6c7d8e\n")
        f.write("# Replaces English menu items (indices 38-48) with German text\n")
        f.write("#\n")
        f.write("# VA = FileOffset + 0x400800\n")
        f.write("# =================================================================\n\n")

        for item in DE_MENU_STRINGS:
            f.write(f"# [{item.touphscript_index:02d}] {item.de_text} ({item.en_text})\n")
            f.write(f"# DE: 0x{item.de_file_offset:08X}, EN: 0x{item.en_file_offset:08X}\n")

            # Calculate how many bytes to write at English VA
            hex_bytes = item.de_hex_bytes.replace(' ', '')
            bytes_list = [hex_bytes[i:i+2] for i in range(0, len(hex_bytes), 2)]

            # Add FF terminator
            bytes_list.append('FF')

            # Pad to 20 bytes (touphScript standard length for menu items)
            while len(bytes_list) < 20:
                bytes_list.append('00')

            bytes_str = ' '.join(bytes_list)

            f.write(f"{item.en_virtual_addr:06X} = {bytes_str}\n")
            f.write(f"# {item.notes}\n\n")

    print(f"Generated hext patch: {output_path}")


def main():
    output_dir = Path(__file__).parent

    # Print tables
    print_mapping_table()
    print_hex_bytes_table()

    # Export to CSV
    csv_path = output_dir / 'german_menu_touphscript_mapping.csv'
    export_to_csv(csv_path)

    # Generate hext patch
    hext_path = output_dir / 'german_menu_items.hext'
    generate_hext_patch(hext_path)

    print()
    print("=" * 100)
    print("MAPPING COMPLETE")
    print("=" * 100)
    print()
    print("Files generated:")
    print(f"  1. {csv_path.name}")
    print(f"  2. {hext_path.name}")
    print(f"  3. GERMAN_MENU_TOUPHSCRIPT_MAPPING.md (already created)")
    print()


if __name__ == '__main__':
    main()
