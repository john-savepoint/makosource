#!/usr/bin/env python3
"""
OCR FF7 Japanese font textures using manga-ocr.
Created: 2025-11-17 22:34:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

manga-ocr is specifically trained on stylized Japanese text from manga/anime/games,
making it far better suited for FF7's pixel art fonts than traditional OCR.

Key differences from Tesseract approach:
- Uses transformer model trained on stylized Japanese
- No need for complex preprocessing
- Handles thick pixel fonts better
"""

from PIL import Image, ImageOps
from pathlib import Path
from manga_ocr import MangaOcr
import json
import csv
import sys

# Paths
FONT_DIR = Path("extracted_fonts/png")
OUTPUT_DIR = Path("character_tables")

# Grid parameters
CELL_SIZE = 64
GRID_SIZE = 16  # 16x16 grid = 256 cells per texture


def extract_single_glyph(img, grid_x, grid_y):
    """Extract a single character cell from the texture."""
    pixel_x = grid_x * CELL_SIZE
    pixel_y = grid_y * CELL_SIZE

    glyph = img.crop((pixel_x, pixel_y, pixel_x + CELL_SIZE, pixel_y + CELL_SIZE))
    return glyph


def preprocess_for_manga_ocr(glyph):
    """
    Preprocess glyph for manga-ocr.
    manga-ocr works best with black text on white background.
    """
    # Convert to grayscale
    gray = glyph.convert('L')

    # Invert colors (white-on-black -> black-on-white)
    inverted = ImageOps.invert(gray)

    # Convert back to RGB (manga-ocr expects RGB)
    rgb = inverted.convert('RGB')

    return rgb


def is_empty_cell(glyph):
    """Check if a cell is empty (all black or nearly black)."""
    gray = glyph.convert('L')
    pixels = list(gray.getdata())

    # Count bright pixels
    bright_pixels = sum(1 for p in pixels if p > 30)

    # If less than 1% bright pixels, consider it empty
    return bright_pixels < (CELL_SIZE * CELL_SIZE * 0.01)


def process_texture(mocr, img_path, texture_name, prefix_byte=None):
    """
    Process a single texture file and OCR all characters.

    Args:
        mocr: MangaOcr instance
        img_path: Path to PNG file
        texture_name: Name like 'jafont_1'
        prefix_byte: For extended pages (FA=250, FB=251, etc.)

    Returns:
        List of dicts with character data
    """
    print(f"\nProcessing {texture_name}...")

    img = Image.open(img_path)
    results = []

    total_cells = GRID_SIZE * GRID_SIZE
    empty_count = 0
    recognized_count = 0

    for grid_y in range(GRID_SIZE):
        row_chars = []
        for grid_x in range(GRID_SIZE):
            index = grid_y * GRID_SIZE + grid_x

            # Extract glyph
            glyph = extract_single_glyph(img, grid_x, grid_y)

            # Check if empty
            if is_empty_cell(glyph):
                character = ""
                empty_count += 1
            else:
                # Preprocess and OCR
                processed = preprocess_for_manga_ocr(glyph)

                try:
                    # manga-ocr returns the recognized text
                    character = mocr(processed)

                    # manga-ocr might return multiple characters or spaces
                    # Take only first character if multiple returned
                    if character:
                        character = character.strip()
                        if len(character) > 1:
                            # For single-character cells, take first char
                            character = character[0]
                        recognized_count += 1
                    else:
                        character = ""
                except Exception as e:
                    print(f"    Error at ({grid_x}, {grid_y}): {e}")
                    character = ""

            row_chars.append(character)

            # Build encoding string
            if prefix_byte is None:
                encoding_hex = f"{index:02X}"
            else:
                encoding_hex = f"{prefix_byte:02X} {index:02X}"

            # Store result
            result = {
                "ff7_encoding": encoding_hex,
                "texture": texture_name,
                "index": index,
                "grid_x": grid_x,
                "grid_y": grid_y,
                "character": character,
                "unicode_hex": f"0x{ord(character):04x}" if character else ""
            }
            results.append(result)

        # Show progress
        print(f"  Row {grid_y}: {''.join(row_chars)}")

    print(f"  Recognized: {recognized_count}/{total_cells}")
    print(f"  Empty: {empty_count}/{total_cells}")

    return results


def main():
    print("=" * 60)
    print("FF7 Japanese Font OCR using manga-ocr")
    print("=" * 60)

    # Initialize manga-ocr (downloads model on first run)
    print("\nInitializing manga-ocr model...")
    print("(This may take a moment on first run as it downloads the model)")
    mocr = MangaOcr()
    print("Model loaded!")

    # Define textures and their prefix bytes
    textures = [
        ("jafont_1.png", "jafont_1", None),      # Single-byte (00-FF)
        ("jafont_2.png", "jafont_2", 0xFA),      # FA XX
        ("jafont_3.png", "jafont_3", 0xFB),      # FB XX
        ("jafont_4.png", "jafont_4", 0xFC),      # FC XX
        ("jafont_5.png", "jafont_5", 0xFD),      # FD XX
        ("jafont_6.png", "jafont_6", 0xFE),      # FE XX
    ]

    all_results = []

    for filename, texture_name, prefix in textures:
        img_path = FONT_DIR / filename
        if not img_path.exists():
            print(f"WARNING: {img_path} not found, skipping")
            continue

        results = process_texture(mocr, img_path, texture_name, prefix)
        all_results.extend(results)

    # Save results
    print("\n" + "=" * 60)
    print("Saving results...")

    # JSON output
    json_path = OUTPUT_DIR / "character_map_mangaocr.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON: {json_path}")

    # CSV output
    csv_path = OUTPUT_DIR / "character_map_mangaocr.csv"
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "FF7_Encoding", "Texture", "Index", "Grid_X", "Grid_Y",
            "Character", "Unicode"
        ])
        writer.writeheader()
        for result in all_results:
            writer.writerow({
                "FF7_Encoding": result["ff7_encoding"],
                "Texture": result["texture"],
                "Index": result["index"],
                "Grid_X": result["grid_x"],
                "Grid_Y": result["grid_y"],
                "Character": result["character"],
                "Unicode": result["unicode_hex"]
            })
    print(f"Saved CSV: {csv_path}")

    # Statistics
    total = len(all_results)
    recognized = sum(1 for r in all_results if r["character"])
    empty = sum(1 for r in all_results if not r["character"])

    print(f"\nTotal cells: {total}")
    print(f"Recognized: {recognized}")
    print(f"Empty/Failed: {empty}")
    print(f"Recognition rate: {recognized/total*100:.1f}%")

    print("\n" + "=" * 60)
    print("OCR COMPLETE!")
    print("=" * 60)
    print(f"\nFiles created:")
    print(f"  {json_path}")
    print(f"  {csv_path}")
    print("\nNext step: Compare with previous mapping to identify corrections needed.")


if __name__ == "__main__":
    main()
