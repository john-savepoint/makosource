#!/usr/bin/env python3
"""
Verify character mapping with TOP-LEFT alignment (matching FF7 font style).
Created: 2025-11-17 23:14:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

Previous version centered characters. This version aligns them to top-left
to match how FF7 positions characters in their cells.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import csv

# Paths
MANGAOCR_CSV = Path("character_tables/character_map_mangaocr.csv")
OUTPUT_DIR = Path("character_tables/verification_topleft")
ORIGINAL_FONTS = Path("extracted_fonts/png")

# Grid parameters
CELL_SIZE = 64
GRID_SIZE = 16
IMAGE_SIZE = CELL_SIZE * GRID_SIZE  # 1024x1024


def find_japanese_font():
    """Find a suitable Japanese font on macOS."""
    font_paths = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/YuGothic-Medium.otf",
        "/System/Library/Fonts/Osaka.ttf",
    ]

    for path in font_paths:
        if Path(path).exists():
            return path
    return None


def load_mangaocr_mapping():
    """Load manga-ocr character mapping."""
    textures = {
        "jafont_1": [],
        "jafont_2": [],
        "jafont_3": [],
        "jafont_4": [],
        "jafont_5": [],
        "jafont_6": [],
    }

    with open(MANGAOCR_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texture = row['Texture']
            index = int(row['Index'])
            char = row['Character']
            if texture in textures:
                textures[texture].append((index, char))

    for texture in textures:
        textures[texture].sort(key=lambda x: x[0])

    return textures


def render_topleft_grid(chars_list, texture_name, font_path=None):
    """
    Render characters aligned to TOP-LEFT of each cell (like FF7).
    """
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Use larger font size to better match FF7's thick glyphs
    font_size = 52
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception as e:
        print(f"Font error: {e}")
        font = ImageFont.load_default()

    char_map = {idx: char for idx, char in chars_list}

    for grid_y in range(GRID_SIZE):
        for grid_x in range(GRID_SIZE):
            index = grid_y * GRID_SIZE + grid_x
            char = char_map.get(index, "")

            if char:
                cell_x = grid_x * CELL_SIZE
                cell_y = grid_y * CELL_SIZE

                # TOP-LEFT alignment with small padding
                # FF7 characters appear to have ~2-4px padding from edge
                text_x = cell_x + 4
                text_y = cell_y + 2

                draw.text((text_x, text_y), char, font=font, fill=(255, 255, 255))

    return img


def create_side_by_side(original_path, generated_img, output_path):
    """Create side-by-side comparison."""
    original = Image.open(original_path).convert('RGB')

    combined = Image.new('RGB', (IMAGE_SIZE * 2 + 20, IMAGE_SIZE), color=(50, 50, 50))
    combined.paste(original, (0, 0))
    combined.paste(generated_img, (IMAGE_SIZE + 20, 0))

    draw = ImageDraw.Draw(combined)
    try:
        label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        label_font = ImageFont.load_default()

    draw.text((10, 10), "ORIGINAL (jafont)", font=label_font, fill=(255, 100, 100))
    draw.text((IMAGE_SIZE + 30, 10), "MANGA-OCR (top-left)", font=label_font, fill=(100, 255, 100))

    combined.save(output_path)
    return combined


def main():
    print("Generating TOP-LEFT aligned verification images...")
    print("Using manga-ocr results (better for kanji)\n")

    OUTPUT_DIR.mkdir(exist_ok=True)

    font_path = find_japanese_font()
    if not font_path:
        print("ERROR: No Japanese font found!")
        return

    print(f"Using font: {font_path}")

    textures = load_mangaocr_mapping()

    for texture_name, chars_list in textures.items():
        print(f"\nProcessing {texture_name}...")

        # Generate top-left aligned grid
        gen_img = render_topleft_grid(chars_list, texture_name, font_path)
        gen_path = OUTPUT_DIR / f"{texture_name}_mangaocr_topleft.png"
        gen_img.save(gen_path)
        print(f"  Saved: {gen_path}")

        # Create comparison if original exists
        original_path = ORIGINAL_FONTS / f"{texture_name}.png"
        if original_path.exists():
            comp_path = OUTPUT_DIR / f"{texture_name}_comparison_topleft.png"
            create_side_by_side(original_path, gen_img, comp_path)
            print(f"  Saved: {comp_path}")

    print("\n" + "=" * 60)
    print("TOP-LEFT ALIGNED VERIFICATION COMPLETE")
    print("=" * 60)
    print(f"\nFiles saved to: {OUTPUT_DIR}")
    print("\nNow characters should align more closely with the original!")


if __name__ == "__main__":
    main()
