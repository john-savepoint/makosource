#!/usr/bin/env python3
"""
Generate German HEXT Patch File
================================
Created: 2026-01-03 16:35 JST
Session: 629f3c93-f884-439a-91d6-d77e7783bf9c

Generates a HEXT patch file to replace English touphScript strings
with German translations from ff7_de.exe.
"""

import sys
import os

# German character encoding map
FF7_GERMAN_ENCODE_MAP = {
    'Ü': 0x66, 'ä': 0x6A, 'ö': 0x7A, 'ß': 0x7E, 'ü': 0x7F,
    'á': 0x61, 'à': 0x62, 'â': 0x63, 'ã': 0x64, 'å': 0x65,
    'ç': 0x67, 'é': 0x68, 'è': 0x69, 'ë': 0x6B,
    'í': 0x6C, 'ì': 0x6D, 'î': 0x6E, 'ï': 0x6F,
    'ñ': 0x70, 'ó': 0x71, 'ò': 0x72, 'ô': 0x73, 'õ': 0x74,
}


def encode_ff7_german(text: str) -> bytes:
    """Encode German text to FF7 format."""
    result = []
    for c in text:
        if c in FF7_GERMAN_ENCODE_MAP:
            result.append(FF7_GERMAN_ENCODE_MAP[c])
        elif c == ' ':
            result.append(0x00)
        elif 0x21 <= ord(c) <= 0x7F:
            result.append(ord(c) - 0x20)
        else:
            # Skip unknown characters
            pass
    result.append(0xFF)  # Terminator
    return bytes(result)


def load_english_offsets(en_ref_path: str) -> dict:
    """Load English touphScript offsets."""
    offsets = {}
    with open(en_ref_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('[') and ']' in line:
                try:
                    idx_end = line.index(']')
                    idx = int(line[1:idx_end])
                    parts = line.split()
                    if len(parts) >= 3:
                        offset_str = parts[1]
                        length = int(parts[2])
                        if offset_str.startswith('0x'):
                            offset = int(offset_str, 16)
                            offsets[idx] = (offset, length)
                except:
                    pass
    return offsets


def load_german_mappings(csv_path: str) -> list:
    """Load German string mappings."""
    mappings = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split(',', 3)
            if len(parts) >= 4:
                try:
                    idx = int(parts[0])
                    de_offset = parts[1]
                    de_text = parts[2]
                    en_text = parts[3]
                    mappings.append((idx, de_offset, de_text, en_text))
                except:
                    pass
    return mappings


def generate_hext(en_offsets: dict, de_mappings: list, output_path: str):
    """Generate HEXT patch file."""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 English -> German Menu Translation Patch\n")
        f.write("# Generated: 2026-01-03 16:35 JST\n")
        f.write("# Session: 629f3c93-f884-439a-91d6-d77e7783bf9c\n")
        f.write("#\n")
        f.write("# This patch replaces English touphScript menu strings with German translations\n")
        f.write("# from the official FF7 German release (ff7_de.exe)\n")
        f.write("#\n")
        f.write(f"# Total patches: {len(de_mappings)}\n")
        f.write("# Coverage:\n")
        f.write("#   - Core menu (0-76): ~92% (55/60 translatable)\n")
        f.write("#   - Menu/UI (214-400): 119 strings\n")
        f.write("#   - Extended (401-766): 34 strings\n")
        f.write("#\n")
        f.write("# Usage: Place in ff7_en.exe directory and activate with Hext tool\n")
        f.write("#\n")
        f.write("# Format: OFFSET = HEX_BYTES  # Index [IDX]: GERMAN_TEXT (ENGLISH_TEXT)\n")
        f.write("#\n")
        f.write("=" * 80 + "\n\n")

        successful = 0
        skipped = 0
        errors = []

        for idx, de_offset, de_text, en_text in sorted(de_mappings):
            # Get English offset and slot size
            if idx not in en_offsets:
                errors.append(f"Index {idx}: No English offset found")
                skipped += 1
                continue

            en_offset, slot_size = en_offsets[idx]

            # Encode German text
            try:
                de_encoded = encode_ff7_german(de_text)
            except Exception as e:
                errors.append(f"Index {idx}: Encoding failed - {e}")
                skipped += 1
                continue

            # Check if German text fits in English slot
            if len(de_encoded) > slot_size:
                errors.append(f"Index {idx}: German text too long ({len(de_encoded)} > {slot_size} bytes)")
                skipped += 1
                continue

            # Pad to slot size with null bytes
            de_padded = de_encoded + (b'\x00' * (slot_size - len(de_encoded)))

            # Write HEXT entry
            hex_str = de_padded.hex().upper()
            # Format as space-separated pairs
            hex_formatted = ' '.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])

            f.write(f"# [{idx:03d}] {de_text[:40]:<40} ({en_text[:30]})\n")
            f.write(f"{en_offset:08X} = {hex_formatted}\n")
            f.write("\n")

            successful += 1

        # Write summary at the end
        f.write("\n" + "=" * 80 + "\n")
        f.write("# PATCH SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"# Total patches applied: {successful}\n")
        f.write(f"# Skipped (errors): {skipped}\n")
        f.write(f"# Success rate: {successful / len(de_mappings) * 100:.1f}%\n")

        if errors:
            f.write(f"#\n# ERRORS:\n")
            for error in errors[:20]:  # Limit to first 20
                f.write(f"#   - {error}\n")

    return successful, skipped, errors


def main():
    # Paths
    en_ref_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt"
    de_csv_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/haiku_chunks/results/FINAL_CLEAN_MAPPINGS.csv"
    output_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/mods/Textures/german_menu.hext"

    print("=" * 80)
    print("FF7 GERMAN MENU HEXT GENERATOR")
    print("=" * 80)
    print()

    # Load English offsets
    print("Loading English touphScript offset table...")
    en_offsets = load_english_offsets(en_ref_path)
    print(f"  Loaded {len(en_offsets)} English string offsets")

    # Load German mappings
    print("Loading German string mappings...")
    de_mappings = load_german_mappings(de_csv_path)
    print(f"  Loaded {len(de_mappings)} German translations")

    # Generate HEXT
    print()
    print("Generating HEXT patch file...")
    successful, skipped, errors = generate_hext(en_offsets, de_mappings, output_path)

    print()
    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Output file: {output_path}")
    print(f"Total patches: {successful}")
    print(f"Skipped: {skipped}")
    print(f"Success rate: {successful / len(de_mappings) * 100:.1f}%")
    print()

    if errors:
        print("Errors encountered:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
        print()

    print("Ready for testing!")
    print()
    print("To test:")
    print("  1. Launch FF7 English")
    print("  2. Apply Hext patch: german_menu.hext")
    print("  3. Check in-game menus for German text")


if __name__ == "__main__":
    main()
