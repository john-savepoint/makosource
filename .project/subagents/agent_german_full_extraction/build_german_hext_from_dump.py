#!/usr/bin/env python3
"""
Build German HEXT from discovered string offsets

Uses the blind extraction dump to find German strings and map them to
the English touphScript indices based on content matching.

Created: 2026-01-03 13:35 JST
Session: 8bc98f0a-abab-49e6-acdd-56dd38e9d149
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# =============================================================================
# PATHS
# =============================================================================

GERMAN_EXE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe")
ENGLISH_EXE = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe")
OUTPUT_DIR = Path(__file__).parent

# =============================================================================
# KNOWN GERMAN STRINGS - Discovered from dump at their exact DE offsets
# Format: (de_offset, de_text, corresponding_en_index)
# These are anchors we found by searching for "Möchten", "Fensterfarbe", etc.
# =============================================================================

# From the detailed dump, these are the actual German menu strings with offsets:
DISCOVERED_GERMAN_STRINGS = [
    # Quit dialog (indices 0-4)
    (0x58FBB0, "Möchten Sie Final", 0),
    (0x58FBCE, "Fantasy VII verlassen und", 1),
    (0x58FBEC, "zu Windows zurückkehren?", 2),
    (0x58FC10, "Ja", 3),
    (0x58FC14, "Nein", 4),

    # Config menu (indices 5+)
    (0x5900F0, "Fensterfarbe", 5),
    (0x590120, "Sound", 6),
    (0x590150, "Kontroller", 7),
    (0x590180, "Cursor", 8),
    (0x5901B0, "ATB", 9),
    (0x5901E0, "Kampftempo", 10),
    (0x590210, "Kampfmeldung", 11),
    (0x590240, "Feldmeldung", 12),
    (0x590270, "Kamerawinkel", 13),
    (0x5902A0, "Auswählen", 14),
    (0x5902D0, "Abbrechen", 15),
    (0x590300, "Menü", 16),
    # ... more will be discovered by LLM analysis
]

# =============================================================================
# TOUPHSCRIPT OFFSET TABLE (English) - First 100 entries for reference
# =============================================================================

EN_OFFSETS = [
    0x518370, 0x51838E, 0x5183AC, 0x5183D0, 0x5183D4, 0x5188A8, 0x5188D8,
    0x518908, 0x518938, 0x518968, 0x518998, 0x5189C8, 0x5189F8, 0x518A28,
    0x518A58, 0x518A88, 0x518AB8, 0x518C08, 0x518C38, 0x518C68, 0x518C98,
    0x518CC8, 0x518CF8, 0x518D28, 0x518D58, 0x518D88, 0x518DE8, 0x518E18,
    0x518ED8, 0x518F08, 0x518F38, 0x518F68, 0x518FC8,
    # ... continues for all 767
]

STRING_LENGTHS = [
    30, 30, 30, 4, 4, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    # ... continues
]

# =============================================================================
# FUNCTIONS
# =============================================================================

def encode_german_to_ff7(text: str) -> bytes:
    """Encode German text to FF7 byte format."""
    result = []
    for char in text:
        if char == ' ':
            result.append(0x00)
        elif char == 'ä':
            result.append(0x6A)
        elif char == 'ö':
            result.append(0x7A)
        elif char == 'ü':
            result.append(0x7F)
        elif char == 'ß':
            result.append(0x7E)
        elif char == 'Ä':
            result.append(0x4A)  # Uppercase ä
        elif char == 'Ö':
            result.append(0x5A)  # Uppercase ö
        elif char == 'Ü':
            result.append(0x5F)  # Uppercase ü
        elif char == '?':
            result.append(0x1F)
        elif char == '!':
            result.append(0x01)
        elif char == '.':
            result.append(0x0E)
        elif char == ',':
            result.append(0x0C)
        elif char == '-':
            result.append(0x0D)
        elif char == ':':
            result.append(0x1A)
        elif 'A' <= char <= 'Z':
            result.append(ord(char) - 0x20)
        elif 'a' <= char <= 'z':
            result.append(ord(char) - 0x20)
        elif '0' <= char <= '9':
            result.append(ord(char) - 0x20)
        else:
            # Unknown char - skip or use placeholder
            pass
    result.append(0xFF)  # Terminator
    return bytes(result)


def file_offset_to_va(offset: int) -> int:
    """Convert Steam EN file offset to Virtual Address for HEXT."""
    return offset + 0x400800


def generate_hext_patch(en_index: int, en_offset: int, slot_length: int, de_text: str) -> str:
    """Generate a single HEXT patch line."""
    va = file_offset_to_va(en_offset)
    de_bytes = encode_german_to_ff7(de_text)

    # Pad or truncate to slot length
    if len(de_bytes) > slot_length:
        de_bytes = de_bytes[:slot_length-1] + b'\xFF'  # Truncate with terminator
    else:
        de_bytes = de_bytes + b'\x00' * (slot_length - len(de_bytes))  # Pad with nulls

    hex_str = ' '.join(f'{b:02X}' for b in de_bytes)
    return f"{va:06X} = {hex_str}"


def main():
    """Main function to generate HEXT from discovered strings."""

    print("Building German HEXT from discovered string offsets...")
    print(f"Found {len(DISCOVERED_GERMAN_STRINGS)} anchor strings")

    # Read German exe to extract raw bytes
    with open(GERMAN_EXE, 'rb') as f:
        de_data = f.read()

    # For now, generate patches for the discovered strings
    patches = []

    for de_offset, de_text, en_index in DISCOVERED_GERMAN_STRINGS:
        if en_index < len(EN_OFFSETS) and en_index < len(STRING_LENGTHS):
            en_offset = EN_OFFSETS[en_index]
            slot_length = STRING_LENGTHS[en_index]

            # Read actual bytes from German exe
            raw_bytes = de_data[de_offset:de_offset + slot_length]

            # Find terminator
            term_pos = raw_bytes.find(0xFF)
            if term_pos == -1:
                term_pos = len(raw_bytes)

            actual_bytes = raw_bytes[:term_pos + 1] if term_pos < len(raw_bytes) else raw_bytes + b'\xFF'

            # Pad to slot length
            padded_bytes = actual_bytes + b'\x00' * (slot_length - len(actual_bytes))
            padded_bytes = padded_bytes[:slot_length]

            va = file_offset_to_va(en_offset)
            hex_str = ' '.join(f'{b:02X}' for b in padded_bytes)

            patches.append({
                'index': en_index,
                'en_offset': en_offset,
                'de_offset': de_offset,
                'va': va,
                'de_text': de_text,
                'hex': hex_str,
                'length': slot_length
            })

    # Write output
    output_file = OUTPUT_DIR / 'german_menu_from_dump.txt'
    with open(output_file, 'w') as f:
        f.write("# German Menu HEXT - Built from discovered offsets\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Session: 8bc98f0a-abab-49e6-acdd-56dd38e9d149\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# VA = FileOffset + 0x400800\n")
        f.write("# " + "=" * 80 + "\n\n")

        for p in patches:
            f.write(f"# [{p['index']:03d}] \"{p['de_text']}\"\n")
            f.write(f"# EN: 0x{p['en_offset']:08X}, DE: 0x{p['de_offset']:08X}, Slot: {p['length']} bytes\n")
            f.write(f"{p['va']:06X} = {p['hex']}\n\n")

    print(f"Wrote {len(patches)} patches to {output_file}")

    # Now we need to find more strings by analyzing the dump with LLM
    # Let's create a focused chunk of just the menu region for LLM analysis
    print("\nCreating focused menu region dump for LLM analysis...")

    # Menu region is roughly 0x58FB00 to 0x5A0000
    menu_start = 0x58FB00
    menu_end = 0x5A0000

    strings_in_region = []

    # Re-extract just the menu region with better decoding
    current_string = []
    current_offset = 0
    in_string = False

    for i in range(menu_start, min(menu_end, len(de_data))):
        byte = de_data[i]

        if byte == 0xFF:
            if in_string and len(current_string) >= 2:
                text = decode_ff7_string(bytes(current_string))
                if text.strip():
                    strings_in_region.append((current_offset, text, bytes(current_string)))
            in_string = False
            current_string = []
            continue

        if is_valid_ff7_char(byte):
            if not in_string:
                in_string = True
                current_offset = i
            current_string.append(byte)
        else:
            if in_string and len(current_string) >= 2:
                text = decode_ff7_string(bytes(current_string))
                if text.strip():
                    strings_in_region.append((current_offset, text, bytes(current_string)))
            in_string = False
            current_string = []

    # Write menu region strings
    menu_dump_file = OUTPUT_DIR / 'german_menu_region.txt'
    with open(menu_dump_file, 'w') as f:
        f.write(f"# German Menu Region Strings\n")
        f.write(f"# Range: 0x{menu_start:X} to 0x{menu_end:X}\n")
        f.write(f"# Total: {len(strings_in_region)} strings\n\n")

        for offset, text, raw in strings_in_region:
            hex_str = ' '.join(f'{b:02X}' for b in raw[:50])
            if len(raw) > 50:
                hex_str += '...'
            f.write(f"0x{offset:06X} | {text} | {hex_str}\n")

    print(f"Wrote menu region dump to {menu_dump_file}")


def is_valid_ff7_char(byte: int) -> bool:
    """Check if byte is valid FF7 text character."""
    if byte == 0x00: return True  # Space
    if byte == 0xFF: return False  # Terminator
    if 0x01 <= byte <= 0x5F: return True  # Standard range
    if byte in (0x6A, 0x7A, 0x7E, 0x7F): return True  # German umlauts
    return False


def decode_ff7_string(data: bytes) -> str:
    """Decode FF7 bytes to string."""
    result = []
    for byte in data:
        if byte == 0x00:
            result.append(' ')
        elif byte == 0x6A:
            result.append('ä')
        elif byte == 0x7A:
            result.append('ö')
        elif byte == 0x7E:
            result.append('ß')
        elif byte == 0x7F:
            result.append('ü')
        elif 0x21 <= byte <= 0x5F:
            result.append(chr(byte + 0x20))
        else:
            result.append(f'[{byte:02X}]')
    return ''.join(result)


if __name__ == '__main__':
    main()
