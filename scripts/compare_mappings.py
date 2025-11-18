#!/usr/bin/env python3
"""
Compare manga-ocr results with Claude visual transcription.
Created: 2025-11-17 22:40:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

This script identifies discrepancies between the two mapping methods
to help determine which characters need manual verification.
"""

import csv
from pathlib import Path
from collections import defaultdict

CLAUDE_CSV = Path("character_tables/character_map_accurate.csv")
MANGAOCR_CSV = Path("character_tables/character_map_mangaocr.csv")
OUTPUT_DIR = Path("character_tables")


def load_mapping(csv_path):
    """Load character mapping from CSV into dict keyed by (texture, index)."""
    mapping = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['Texture'], int(row['Index']))
            mapping[key] = row['Character']
    return mapping


def compare_mappings():
    """Compare the two mappings and identify discrepancies."""

    print("Loading Claude visual transcription...")
    claude_map = load_mapping(CLAUDE_CSV)
    print(f"  Loaded {len(claude_map)} entries")

    print("Loading manga-ocr results...")
    mangaocr_map = load_mapping(MANGAOCR_CSV)
    print(f"  Loaded {len(mangaocr_map)} entries")

    # Find discrepancies
    discrepancies = []
    agreements = 0
    both_empty = 0
    claude_only = 0
    mangaocr_only = 0

    textures = ['jafont_1', 'jafont_2', 'jafont_3', 'jafont_4', 'jafont_5', 'jafont_6']

    for texture in textures:
        for index in range(256):
            key = (texture, index)
            claude_char = claude_map.get(key, "")
            mangaocr_char = mangaocr_map.get(key, "")

            if claude_char == mangaocr_char:
                if claude_char:
                    agreements += 1
                else:
                    both_empty += 1
            else:
                # Discrepancy found
                if not claude_char and mangaocr_char:
                    mangaocr_only += 1
                    discrepancies.append({
                        'texture': texture,
                        'index': index,
                        'grid_x': index % 16,
                        'grid_y': index // 16,
                        'claude': claude_char or "(empty)",
                        'mangaocr': mangaocr_char,
                        'type': 'MANGAOCR_ONLY'
                    })
                elif claude_char and not mangaocr_char:
                    claude_only += 1
                    discrepancies.append({
                        'texture': texture,
                        'index': index,
                        'grid_x': index % 16,
                        'grid_y': index // 16,
                        'claude': claude_char,
                        'mangaocr': "(empty)",
                        'type': 'CLAUDE_ONLY'
                    })
                else:
                    discrepancies.append({
                        'texture': texture,
                        'index': index,
                        'grid_x': index % 16,
                        'grid_y': index // 16,
                        'claude': claude_char,
                        'mangaocr': mangaocr_char,
                        'type': 'MISMATCH'
                    })

    # Statistics
    total = len(textures) * 256
    print(f"\n{'='*60}")
    print("COMPARISON RESULTS")
    print(f"{'='*60}")
    print(f"Total cells analyzed: {total}")
    print(f"Perfect agreements (both same char): {agreements}")
    print(f"Both empty: {both_empty}")
    print(f"Claude has char, manga-ocr empty: {claude_only}")
    print(f"Manga-ocr has char, Claude empty: {mangaocr_only}")
    print(f"Character mismatches: {len([d for d in discrepancies if d['type'] == 'MISMATCH'])}")
    print(f"Total discrepancies: {len(discrepancies)}")
    print(f"Agreement rate: {(agreements + both_empty) / total * 100:.1f}%")

    # Group discrepancies by texture
    by_texture = defaultdict(list)
    for d in discrepancies:
        by_texture[d['texture']].append(d)

    print(f"\n{'='*60}")
    print("DISCREPANCIES BY TEXTURE")
    print(f"{'='*60}")

    for texture in textures:
        disc_list = by_texture[texture]
        if disc_list:
            print(f"\n{texture}: {len(disc_list)} discrepancies")
            print("-" * 50)

            # Group by type
            mismatches = [d for d in disc_list if d['type'] == 'MISMATCH']
            claude_only = [d for d in disc_list if d['type'] == 'CLAUDE_ONLY']
            mangaocr_only = [d for d in disc_list if d['type'] == 'MANGAOCR_ONLY']

            if mismatches:
                print(f"\n  CHARACTER MISMATCHES ({len(mismatches)}):")
                for d in mismatches[:20]:  # Show first 20
                    print(f"    Index {d['index']:3d} ({d['grid_x']:2d},{d['grid_y']:2d}): "
                          f"Claude={d['claude']} vs manga-ocr={d['mangaocr']}")
                if len(mismatches) > 20:
                    print(f"    ... and {len(mismatches) - 20} more")

            if claude_only:
                print(f"\n  CLAUDE HAS, MANGA-OCR EMPTY ({len(claude_only)}):")
                chars = ''.join([d['claude'] for d in claude_only])
                print(f"    Characters: {chars[:50]}{'...' if len(chars) > 50 else ''}")

            if mangaocr_only:
                print(f"\n  MANGA-OCR HAS, CLAUDE EMPTY ({len(mangaocr_only)}):")
                chars = ''.join([d['mangaocr'] for d in mangaocr_only])
                print(f"    Characters: {chars[:50]}{'...' if len(chars) > 50 else ''}")

    # Save detailed discrepancies to CSV
    output_csv = OUTPUT_DIR / "mapping_discrepancies.csv"
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Texture', 'Index', 'Grid_X', 'Grid_Y',
            'Claude_Char', 'MangaOCR_Char', 'Type'
        ])
        writer.writeheader()
        for d in discrepancies:
            writer.writerow({
                'Texture': d['texture'],
                'Index': d['index'],
                'Grid_X': d['grid_x'],
                'Grid_Y': d['grid_y'],
                'Claude_Char': d['claude'],
                'MangaOCR_Char': d['mangaocr'],
                'Type': d['type']
            })

    print(f"\n{'='*60}")
    print(f"Detailed discrepancies saved to: {output_csv}")
    print(f"{'='*60}")

    # Highlight serious mismatches (different characters, not just empty)
    serious = [d for d in discrepancies if d['type'] == 'MISMATCH']
    print(f"\n⚠️  SERIOUS MISMATCHES (both have different chars): {len(serious)}")
    print("These need manual verification!")

    return discrepancies


if __name__ == "__main__":
    compare_mappings()
