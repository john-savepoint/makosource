#!/usr/bin/env python3
"""
Find correct grid offset by detecting where characters actually start
Created: 2025-11-17 19:13:00 JST

The texture likely has padding at the edges. We need to find the actual
starting point of the character grid.
"""

from PIL import Image
from pathlib import Path

FONT_DIR = Path("extracted_fonts/png")
OUTPUT_DIR = Path("character_tables/debug")

def find_first_ink_pixel(img):
    """Find the top-left corner where actual character ink starts."""

    # Convert to grayscale
    gray = img.convert('L')
    pixels = gray.load()
    width, height = gray.size

    # Scan from left to find first non-black column
    first_x = None
    for x in range(width):
        for y in range(height):
            if pixels[x, y] > 30:  # Non-black pixel (ink)
                first_x = x
                break
        if first_x is not None:
            break

    # Scan from top to find first non-black row
    first_y = None
    for y in range(height):
        for x in range(width):
            if pixels[x, y] > 30:
                first_y = y
                break
        if first_y is not None:
            break

    return first_x, first_y


def test_different_offsets(img_path):
    """Try different offsets and show what we get."""

    img = Image.open(img_path)

    print(f"Image size: {img.size}")

    # Find first ink
    first_x, first_y = find_first_ink_pixel(img)
    print(f"First ink pixel found at: ({first_x}, {first_y})")

    # The offset should be such that first_x and first_y become centered in cell
    # If cell is 64px and character is ~40px wide, center would be at ~12px from edge
    # So if ink starts at pixel 7, offset should be... let's calculate

    # Actually, let's just try multiple offsets and extract the same character
    # to see which one looks right

    OUTPUT_DIR.mkdir(exist_ok=True)

    offsets_to_try = [
        (0, 0),    # Current (bad)
        (5, 2),    # Your suggestion
        (7, 2),    # First ink position
        (8, 4),    # Slightly more
        (10, 4),   # Even more
    ]

    grid_x, grid_y = 9, 0  # The "bo" character

    print(f"\nExtracting grid ({grid_x}, {grid_y}) with different offsets:")
    print("="*50)

    for offset_x, offset_y in offsets_to_try:
        pixel_x = grid_x * 64 + offset_x
        pixel_y = grid_y * 64 + offset_y

        glyph = img.crop((pixel_x, pixel_y, pixel_x + 64, pixel_y + 64))

        filename = f"offset_{offset_x}_{offset_y}.png"
        glyph.save(OUTPUT_DIR / filename)

        # Check if the glyph looks centered (no ink at very edges)
        gray = glyph.convert('L')
        pixels = gray.load()

        # Check left edge
        left_edge_ink = any(pixels[0, y] > 30 for y in range(64))
        # Check top edge
        top_edge_ink = any(pixels[x, 0] > 30 for x in range(64))
        # Check right edge
        right_edge_ink = any(pixels[63, y] > 30 for y in range(64))

        status = ""
        if left_edge_ink:
            status += " [LEFT EDGE CROPPED]"
        if top_edge_ink:
            status += " [TOP EDGE CROPPED]"
        if right_edge_ink:
            status += " [RIGHT EDGE HAS INK]"
        if not status:
            status = " [GOOD - No edge cropping!]"

        print(f"  Offset ({offset_x:2d}, {offset_y:2d}): {filename}{status}")

    print(f"\nOpen the offset_*.png files to see which one centers the character correctly.")


def main():
    test_different_offsets(FONT_DIR / "jafont_1.png")


if __name__ == "__main__":
    main()
