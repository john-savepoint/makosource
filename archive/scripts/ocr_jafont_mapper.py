#!/usr/bin/env python3
"""
FF7 Japanese Font Character Mapper using OCR
=============================================
Created: 2025-11-17 17:30:00 JST (Monday)
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

Purpose:
    Extract character mappings from FF7 Japanese font textures (jafont_1-6.png)
    using Tesseract OCR. Each texture is a 1024x1024 image with a 16x16 grid
    of 64x64 pixel glyphs.

Context:
    This script fills an 18-year gap in FF7 modding documentation. The community
    has been requesting a complete Japanese character table since 2007, but no
    one has created one. This uses OCR to bulk-process the font textures extracted
    in Session 8.

Usage:
    source .venv/bin/activate
    python scripts/ocr_jafont_mapper.py

Output:
    - character_map.json: Complete FF7 index to Unicode mapping
    - character_map.csv: Spreadsheet-friendly format
    - ocr_confidence.json: Confidence scores for manual review

Dependencies:
    - Pillow (pip install Pillow)
    - pytesseract (pip install pytesseract)
    - Tesseract with Japanese language pack (brew install tesseract-lang)
"""

import json
import csv
import os
from pathlib import Path

try:
    from PIL import Image, ImageOps, ImageEnhance
    import pytesseract
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install Pillow pytesseract")
    exit(1)

# Configuration
FONT_DIR = Path("extracted_fonts/png")
OUTPUT_DIR = Path("character_tables")
GRID_SIZE = 16  # 16x16 grid
CELL_SIZE = 64  # 64x64 pixels per glyph
TEXTURE_SIZE = 1024  # 1024x1024 total

# FF7 encoding pages
ENCODING_PAGES = {
    0: {"name": "jafont_1", "prefix": None, "description": "Base characters (single-byte)"},
    1: {"name": "jafont_2", "prefix": 0xFA, "description": "Kanji page 1"},
    2: {"name": "jafont_3", "prefix": 0xFB, "description": "Kanji page 2"},
    3: {"name": "jafont_4", "prefix": 0xFC, "description": "Kanji page 3"},
    4: {"name": "jafont_5", "prefix": 0xFD, "description": "Kanji page 4"},
    5: {"name": "jafont_6", "prefix": 0xFE, "description": "Kanji page 5"},
}


def preprocess_glyph(img):
    """
    Preprocess a single glyph image for better OCR accuracy.
    FF7 fonts are white text on black background.
    """
    # Convert to grayscale if needed
    if img.mode != 'L':
        img = img.convert('L')

    # Invert colors (OCR works better with black text on white background)
    img = ImageOps.invert(img)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # Add padding (helps OCR recognize single characters)
    padded = Image.new('L', (CELL_SIZE + 20, CELL_SIZE + 20), 255)
    padded.paste(img, (10, 10))

    # Scale up for better recognition
    scaled = padded.resize((padded.width * 2, padded.height * 2), Image.LANCZOS)

    return scaled


def extract_glyph(texture_img, grid_x, grid_y):
    """Extract a single glyph from the texture grid."""
    pixel_x = grid_x * CELL_SIZE
    pixel_y = grid_y * CELL_SIZE

    # Crop the glyph
    glyph = texture_img.crop((
        pixel_x, pixel_y,
        pixel_x + CELL_SIZE,
        pixel_y + CELL_SIZE
    ))

    return glyph


def is_empty_glyph(img):
    """Check if a glyph cell is empty (all black or mostly transparent)."""
    if img.mode == 'RGBA':
        # Check alpha channel
        pixels = list(img.getdata())
        non_transparent = sum(1 for p in pixels if p[3] > 10)
        return non_transparent < 50  # Less than 50 non-transparent pixels
    else:
        # Check brightness
        gray = img.convert('L')
        pixels = list(gray.getdata())
        bright_pixels = sum(1 for p in pixels if p > 30)
        return bright_pixels < 50


def ocr_single_character(img, lang='jpn'):
    """
    Run OCR on a single character image.
    Returns (character, confidence) tuple.
    """
    # Configure Tesseract for single character recognition
    config = '--psm 10 --oem 3'  # PSM 10 = single character mode

    try:
        # Get detailed data including confidence
        data = pytesseract.image_to_data(
            img, lang=lang, config=config, output_type=pytesseract.Output.DICT
        )

        # Find the recognized text
        text_items = [t.strip() for t in data['text'] if t.strip()]
        conf_items = [c for i, c in enumerate(data['conf']) if data['text'][i].strip()]

        if text_items:
            char = text_items[0]
            conf = conf_items[0] if conf_items else 0
            return char, float(conf)
        else:
            return "", 0.0

    except Exception as e:
        print(f"OCR error: {e}")
        return "", 0.0


def process_texture(texture_path, page_id):
    """
    Process a single texture file and extract all character mappings.
    Returns a list of (index, character, confidence) tuples.
    """
    results = []

    print(f"Processing {texture_path.name}...")

    try:
        img = Image.open(texture_path)
    except Exception as e:
        print(f"  Error loading image: {e}")
        return results

    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    total_cells = GRID_SIZE * GRID_SIZE
    processed = 0
    empty_count = 0

    for grid_y in range(GRID_SIZE):
        for grid_x in range(GRID_SIZE):
            index = grid_y * GRID_SIZE + grid_x

            # Extract glyph
            glyph = extract_glyph(img, grid_x, grid_y)

            # Check if empty
            if is_empty_glyph(glyph):
                results.append((index, "", 0.0))
                empty_count += 1
            else:
                # Preprocess for OCR
                preprocessed = preprocess_glyph(glyph)

                # Try Japanese first, then English for Latin characters
                char, conf = ocr_single_character(preprocessed, lang='jpn')

                # If low confidence and might be Latin/number, try English
                if conf < 50 and page_id == 0:  # Only for jafont_1 (base chars)
                    char_eng, conf_eng = ocr_single_character(preprocessed, lang='eng')
                    if conf_eng > conf:
                        char, conf = char_eng, conf_eng

                results.append((index, char, conf))

            processed += 1

            # Progress indicator
            if processed % 32 == 0:
                print(f"  Progress: {processed}/{total_cells} ({empty_count} empty)")

    print(f"  Completed: {processed} cells processed, {empty_count} empty")
    return results


def calculate_ff7_encoding(page_id, index):
    """
    Calculate the FF7 internal encoding for a character.
    Returns a tuple (encoding_bytes, encoding_hex_string).
    """
    if page_id == 0:
        # Single-byte encoding
        return bytes([index]), f"{index:02X}"
    else:
        # Two-byte encoding with page prefix
        prefix = ENCODING_PAGES[page_id]["prefix"]
        return bytes([prefix, index]), f"{prefix:02X} {index:02X}"


def save_results(all_results):
    """Save the character mapping results to various formats."""

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Prepare data structures
    character_map = {}
    confidence_map = {}
    csv_rows = []

    # Statistics
    total_chars = 0
    high_conf_chars = 0
    low_conf_chars = 0
    empty_slots = 0

    for page_id, results in all_results.items():
        page_info = ENCODING_PAGES[page_id]

        for index, char, conf in results:
            encoding_bytes, encoding_hex = calculate_ff7_encoding(page_id, index)

            # Calculate grid position
            grid_x = index % GRID_SIZE
            grid_y = index // GRID_SIZE

            # Build key for JSON
            if page_id == 0:
                key = f"{index:02X}"
            else:
                key = f"{page_info['prefix']:02X}_{index:02X}"

            # Store mapping
            # Handle multi-character OCR results (take first char only)
            single_char = char[0] if char and len(char) >= 1 else ""
            character_map[key] = {
                "character": single_char,
                "unicode": hex(ord(single_char)) if single_char else "",
                "page": page_info["name"],
                "grid_position": f"({grid_x}, {grid_y})",
                "encoding_hex": encoding_hex,
                "ocr_raw": char if char != single_char else ""  # Keep original if different
            }

            confidence_map[key] = {
                "character": char,
                "confidence": conf,
                "needs_review": conf < 70 and char != ""
            }

            # CSV row
            csv_rows.append([
                encoding_hex,
                page_info["name"],
                index,
                grid_x,
                grid_y,
                single_char,
                hex(ord(single_char)) if single_char else "",
                f"{conf:.1f}",
                "Yes" if (conf < 70 and single_char != "") else "No"
            ])

            # Statistics
            if char:
                total_chars += 1
                if conf >= 70:
                    high_conf_chars += 1
                else:
                    low_conf_chars += 1
            else:
                empty_slots += 1

    # Save JSON character map
    json_path = OUTPUT_DIR / "character_map.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(character_map, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"Saved character map to {json_path}")

    # Save confidence data
    conf_path = OUTPUT_DIR / "ocr_confidence.json"
    with open(conf_path, 'w', encoding='utf-8') as f:
        json.dump(confidence_map, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"Saved confidence data to {conf_path}")

    # Save CSV
    csv_path = OUTPUT_DIR / "character_map.csv"
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "FF7_Encoding", "Texture", "Index", "Grid_X", "Grid_Y",
            "Character", "Unicode", "Confidence", "Needs_Review"
        ])
        writer.writerows(csv_rows)
    print(f"Saved CSV to {csv_path}")

    # Print statistics
    print("\n" + "="*50)
    print("OCR MAPPING STATISTICS")
    print("="*50)
    print(f"Total character slots:     {total_chars + empty_slots}")
    print(f"Characters recognized:     {total_chars}")
    print(f"  - High confidence (≥70): {high_conf_chars}")
    print(f"  - Low confidence (<70):  {low_conf_chars}")
    print(f"Empty slots:               {empty_slots}")
    print(f"Accuracy estimate:         {high_conf_chars / max(total_chars, 1) * 100:.1f}%")
    print("="*50)

    # Identify characters needing review
    review_needed = sum(1 for k, v in confidence_map.items() if v.get("needs_review"))
    if review_needed > 0:
        print(f"\nWARNING: {review_needed} characters need manual review (confidence < 70%)")
        print(f"Check {conf_path} for details")


def main():
    print("="*60)
    print("FF7 Japanese Font Character Mapper")
    print("="*60)
    print(f"Grid size: {GRID_SIZE}x{GRID_SIZE} = {GRID_SIZE*GRID_SIZE} cells per texture")
    print(f"Cell size: {CELL_SIZE}x{CELL_SIZE} pixels")
    print(f"Total textures: {len(ENCODING_PAGES)}")
    print(f"Maximum characters: {GRID_SIZE*GRID_SIZE*len(ENCODING_PAGES)}")
    print("="*60 + "\n")

    # Check for pytesseract
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
    except Exception as e:
        print(f"Error: Tesseract not found. {e}")
        print("Install with: brew install tesseract tesseract-lang")
        exit(1)

    # Check if Japanese language is available
    langs = pytesseract.get_languages()
    if 'jpn' not in langs:
        print("Error: Japanese language pack not installed")
        print("Install with: brew install tesseract-lang")
        exit(1)
    print(f"Available languages: {', '.join(langs)}\n")

    # Process each texture
    all_results = {}

    for page_id, page_info in ENCODING_PAGES.items():
        texture_path = FONT_DIR / f"{page_info['name']}.png"

        if not texture_path.exists():
            print(f"Warning: {texture_path} not found, skipping...")
            continue

        print(f"\n--- Page {page_id}: {page_info['name']} ---")
        print(f"Description: {page_info['description']}")
        if page_info['prefix']:
            print(f"Encoding prefix: 0x{page_info['prefix']:02X}")

        results = process_texture(texture_path, page_id)
        all_results[page_id] = results

    # Save all results
    print("\n" + "="*60)
    print("SAVING RESULTS")
    print("="*60)
    save_results(all_results)

    print("\nDone! Character mapping complete.")
    print("Next steps:")
    print("1. Review low-confidence characters in character_tables/ocr_confidence.json")
    print("2. Cross-reference with known game strings for validation")
    print("3. Manually correct any OCR errors in character_tables/character_map.json")


if __name__ == "__main__":
    main()
