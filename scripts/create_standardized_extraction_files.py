#!/usr/bin/env python3
"""
Create Standardized Extraction Files
=====================================
Created: 2026-01-06 10:45 JST (Tuesday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Convert English and German extractions to standardized CSV format
for easy comparison and semantic matching.

Standard format:
index,offset,text,hex_bytes,byte_length,text_length,type_info

Where:
- index: Sequential index (0-based)
- offset: File offset (hex format 0xXXXXXX)
- text: Decoded string
- hex_bytes: Raw hex bytes (space-separated)
- byte_length: Total bytes (including padding/terminators)
- text_length: Decoded text length
- type_info: Additional metadata (EN: touphScript type, DE: padding info)
"""

import re
import csv
from pathlib import Path

def parse_english_file(filepath):
    """Parse English touphScript format."""
    strings = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('='):
                continue

            # Format: [INDEX] OFFSET LENGTH TYPE | TEXT | HEX_BYTES
            match = re.match(r'\[(\d+)\]\s+(\S+)\s+(\d+)\s+(\S+)\s+\|\s+([^|]+)\s+\|\s+(.+)', line)
            if match:
                index = int(match.group(1))
                offset = match.group(2)  # Already in hex format
                byte_length = int(match.group(3))
                type_info = match.group(4)
                text = match.group(5).strip()
                hex_bytes = match.group(6).strip()

                strings.append({
                    'index': index,
                    'offset': offset,
                    'text': text,
                    'hex_bytes': hex_bytes,
                    'byte_length': byte_length,
                    'text_length': len(text),
                    'type_info': type_info
                })

    return strings

def parse_german_file(filepath):
    """Parse German clean offsets CSV format."""
    strings = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert to standardized format
            # Note: German CSV doesn't have hex_bytes, we'll mark as N/A
            strings.append({
                'index': int(row['index']),
                'offset': row['offset'],  # Already in hex format
                'text': row['text'],
                'hex_bytes': 'N/A',  # Not in German CSV
                'byte_length': int(row['total_bytes']),
                'text_length': int(row['text_bytes']),
                'type_info': f"padding:{row['padding_bytes']}"
            })

    return strings

def write_standardized_csv(strings, output_path, language):
    """Write strings to standardized CSV format."""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(['index', 'offset', 'text', 'hex_bytes', 'byte_length', 'text_length', 'type_info'])

        # Data
        for s in strings:
            writer.writerow([
                s['index'],
                s['offset'],
                s['text'],
                s['hex_bytes'],
                s['byte_length'],
                s['text_length'],
                s['type_info']
            ])

    print(f"{language} CSV written: {output_path}")
    print(f"  Total strings: {len(strings)}")

def write_standardized_txt(strings, output_path, language):
    """Write strings to standardized TXT format (human-readable)."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# FF7 {language} Strings - Standardized Format\n")
        f.write(f"# Generated: 2026-01-06 10:45 JST (Tuesday)\n")
        f.write(f"# Session: c5687d3e-90a9-47e8-829a-a0c6e70cd98e\n")
        f.write(f"# Total strings: {len(strings)}\n")
        f.write("#\n")
        f.write("# Format: [INDEX] OFFSET (BYTES:TEXT_LEN) | TEXT\n")
        f.write("# " + "=" * 75 + "\n\n")

        for s in strings:
            f.write(f"[{s['index']:5d}] {s['offset']} ({s['byte_length']:4d}:{s['text_length']:3d}) | {s['text']}\n")

    print(f"{language} TXT written: {output_path}")

def main():
    print("=" * 80)
    print("Creating Standardized Extraction Files")
    print("=" * 80)
    print()

    # Paths
    english_in = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt"
    german_in = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_offsets.csv"

    output_dir = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/data/standardized_extractions")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse files
    print("Parsing English...")
    english_strings = parse_english_file(english_in)
    print(f"  Parsed {len(english_strings)} English strings")

    print("\nParsing German...")
    german_strings = parse_german_file(german_in)
    print(f"  Parsed {len(german_strings)} German strings")

    # Write standardized outputs
    print("\n" + "=" * 80)
    print("Writing Standardized Files")
    print("=" * 80)
    print()

    # English
    write_standardized_csv(english_strings, output_dir / "english_strings_standardized.csv", "English")
    write_standardized_txt(english_strings, output_dir / "english_strings_standardized.txt", "English")

    # German
    write_standardized_csv(german_strings, output_dir / "german_strings_standardized.csv", "German")
    write_standardized_txt(german_strings, output_dir / "german_strings_standardized.txt", "German")

    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"English: {len(english_strings)} strings")
    print(f"German:  {len(german_strings)} strings")
    print(f"\nOutput directory: {output_dir}")
    print("\nFiles created:")
    print("  - english_strings_standardized.csv (machine-readable)")
    print("  - english_strings_standardized.txt (human-readable)")
    print("  - german_strings_standardized.csv (machine-readable)")
    print("  - german_strings_standardized.txt (human-readable)")

if __name__ == '__main__':
    main()
