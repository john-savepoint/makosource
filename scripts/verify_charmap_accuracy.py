#!/usr/bin/env python3
"""
Verify character mapping accuracy by rendering Unicode characters in matching grid.
Created: 2025-11-17 21:25:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

This script:
1. Loads the accurate character mapping CSV
2. Renders each Unicode character in a 16x16 grid (matching jafont layout)
3. Creates comparison images that can be overlaid with original jafont PNGs
4. Uses a Japanese font that supports all characters

The goal is visual verification - if our mapping is correct, the generated grid
should match the original jafont texture character-for-character.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import csv
import sys

# Paths
CHARMAP_CSV = Path("character_tables/character_map_accurate.csv")
OUTPUT_DIR = Path("character_tables/verification")
ORIGINAL_FONTS = Path("extracted_fonts/png")

# Grid parameters (matching jafont)
CELL_SIZE = 64
GRID_SIZE = 16  # 16x16 grid
IMAGE_SIZE = CELL_SIZE * GRID_SIZE  # 1024x1024


def find_japanese_font():
    """
    Find a suitable Japanese font on macOS.
    Returns path to a TrueType font file.
    """
    # Common macOS Japanese font paths
    font_paths = [
        # Hiragino (best quality, comes with macOS)
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Hiragino Sans GB W3.otf",
        # Yu Gothic (also good)
        "/System/Library/Fonts/YuGothic-Medium.otf",
        "/System/Library/Fonts/YuGothic.ttc",
        # Osaka
        "/System/Library/Fonts/Osaka.ttf",
        # Noto Sans CJK (if installed)
        "/Library/Fonts/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]

    for path in font_paths:
        if Path(path).exists():
            print(f"Found font: {path}")
            return path

    # Fallback: try to find ANY Japanese font
    system_fonts = Path("/System/Library/Fonts")
    if system_fonts.exists():
        for font_file in system_fonts.glob("*.ttc"):
            if "Hiragino" in str(font_file) or "Gothic" in str(font_file):
                print(f"Found font: {font_file}")
                return str(font_file)

    print("WARNING: No Japanese font found. Using default (may not render kanji)")
    return None


def load_charmap():
    """
    Load character mapping from CSV, organized by texture.
    Returns dict: texture_name -> list of (index, character) tuples
    """
    textures = {
        "jafont_1": [],
        "jafont_2": [],
        "jafont_3": [],
        "jafont_4": [],
        "jafont_5": [],
        "jafont_6": [],
    }

    with open(CHARMAP_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texture = row['Texture']
            index = int(row['Index'])
            char = row['Character']
            if texture in textures:
                textures[texture].append((index, char))

    # Sort by index
    for texture in textures:
        textures[texture].sort(key=lambda x: x[0])

    return textures


def render_verification_grid(chars_list, texture_name, font_path=None):
    """
    Render characters in a 16x16 grid matching jafont layout.

    Args:
        chars_list: List of (index, character) tuples
        texture_name: Name for output file
        font_path: Path to Japanese font

    Returns:
        PIL Image object
    """
    # Create image with dark background (like original jafont)
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load font
    font_size = 48  # Slightly smaller than cell to leave padding
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception as e:
        print(f"Font loading error: {e}")
        font = ImageFont.load_default()

    # Create lookup dict
    char_map = {idx: char for idx, char in chars_list}

    # Render each cell
    for grid_y in range(GRID_SIZE):
        for grid_x in range(GRID_SIZE):
            index = grid_y * GRID_SIZE + grid_x

            # Get character (or empty if not in map)
            char = char_map.get(index, "")

            if char:
                # Calculate pixel position
                # Center character in cell
                cell_x = grid_x * CELL_SIZE
                cell_y = grid_y * CELL_SIZE

                # Get text bounding box for centering
                try:
                    bbox = draw.textbbox((0, 0), char, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except:
                    text_width = font_size
                    text_height = font_size

                # Center in cell
                text_x = cell_x + (CELL_SIZE - text_width) // 2
                text_y = cell_y + (CELL_SIZE - text_height) // 2

                # Draw character in white (like original)
                draw.text((text_x, text_y), char, font=font, fill=(255, 255, 255))

            # Optionally draw grid lines (lighter than character)
            # Uncomment below if you want grid lines:
            # draw.rectangle([cell_x, cell_y, cell_x + CELL_SIZE - 1, cell_y + CELL_SIZE - 1],
            #                outline=(50, 50, 50))

    return img


def create_comparison_overlay(original_path, generated_img, output_path):
    """
    Create a comparison overlay: original in red, generated in green.
    Matching pixels appear yellow/white.
    """
    original = Image.open(original_path).convert('RGB')

    # Create comparison image
    comparison = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), color=(0, 0, 0))

    orig_pixels = original.load()
    gen_pixels = generated_img.load()
    comp_pixels = comparison.load()

    for y in range(IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            orig_brightness = sum(orig_pixels[x, y]) // 3
            gen_brightness = sum(gen_pixels[x, y]) // 3

            # Red channel: original
            # Green channel: generated
            # If both have ink, appears yellow; if match perfectly, appears bright
            comp_pixels[x, y] = (orig_brightness, gen_brightness, 0)

    comparison.save(output_path)
    return comparison


def create_side_by_side(original_path, generated_img, output_path):
    """
    Create side-by-side comparison for easy visual verification.
    """
    original = Image.open(original_path).convert('RGB')

    # Create wider image for side-by-side
    combined = Image.new('RGB', (IMAGE_SIZE * 2 + 20, IMAGE_SIZE), color=(50, 50, 50))

    # Paste original on left
    combined.paste(original, (0, 0))

    # Paste generated on right
    combined.paste(generated_img, (IMAGE_SIZE + 20, 0))

    # Add labels
    draw = ImageDraw.Draw(combined)
    try:
        label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        label_font = ImageFont.load_default()

    draw.text((10, 10), "ORIGINAL (jafont)", font=label_font, fill=(255, 100, 100))
    draw.text((IMAGE_SIZE + 30, 10), "GENERATED (Unicode)", font=label_font, fill=(100, 255, 100))

    combined.save(output_path)
    return combined


def main():
    print("=" * 60)
    print("FF7 Character Mapping Verification Tool")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Find Japanese font
    font_path = find_japanese_font()
    if not font_path:
        print("\nERROR: No Japanese font found!")
        print("Install a Japanese font or specify path manually.")
        sys.exit(1)

    # Load character mapping
    print(f"\nLoading character mapping from {CHARMAP_CSV}...")
    textures = load_charmap()

    for texture_name, chars_list in textures.items():
        print(f"\nProcessing {texture_name}...")
        print(f"  Characters: {len(chars_list)}")

        # Generate verification grid
        print("  Rendering Unicode grid...")
        gen_img = render_verification_grid(chars_list, texture_name, font_path)

        # Save generated grid
        gen_path = OUTPUT_DIR / f"{texture_name}_generated.png"
        gen_img.save(gen_path)
        print(f"  Saved: {gen_path}")

        # Create side-by-side comparison if original exists
        original_path = ORIGINAL_FONTS / f"{texture_name}.png"
        if original_path.exists():
            print("  Creating side-by-side comparison...")
            side_path = OUTPUT_DIR / f"{texture_name}_comparison.png"
            create_side_by_side(original_path, gen_img, side_path)
            print(f"  Saved: {side_path}")

            # Create color overlay
            print("  Creating overlay (red=original, green=generated)...")
            overlay_path = OUTPUT_DIR / f"{texture_name}_overlay.png"
            create_comparison_overlay(original_path, gen_img, overlay_path)
            print(f"  Saved: {overlay_path}")
        else:
            print(f"  WARNING: Original {original_path} not found, skipping comparison")

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("\nFiles created:")
    print("  *_generated.png   - Unicode characters in matching grid")
    print("  *_comparison.png  - Side-by-side original vs generated")
    print("  *_overlay.png     - Color overlay (red=orig, green=gen)")
    print("\nTo verify accuracy:")
    print("1. Open *_comparison.png to see side-by-side")
    print("2. Check that characters match position-by-position")
    print("3. Note: Font rendering will differ, but CHARACTER should match")
    print("\nIf characters don't match, the mapping needs correction!")


if __name__ == "__main__":
    main()
