#!/usr/bin/env python3
"""
Debug Grid Overlay - Verify OCR is cutting glyphs correctly
Created: 2025-11-17 18:58:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

This script draws a red grid overlay on the jafont PNG to visually verify
that our 16x16 grid (64x64 pixels per cell) aligns with the actual characters.

If the grid lines DON'T align with character boundaries, then our OCR is
looking at the wrong areas!
"""

from PIL import Image, ImageDraw
from pathlib import Path

FONT_DIR = Path("extracted_fonts/png")
OUTPUT_DIR = Path("character_tables/debug")
GRID_SIZE = 16  # 16x16 grid
CELL_SIZE = 64  # 64x64 pixels per glyph

def create_grid_overlay(png_path, output_path):
    """Draw a red grid over the font texture to verify alignment."""

    img = Image.open(png_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Draw vertical lines
    for x in range(GRID_SIZE + 1):
        pixel_x = x * CELL_SIZE
        draw.line([(pixel_x, 0), (pixel_x, 1024)], fill='red', width=2)

    # Draw horizontal lines
    for y in range(GRID_SIZE + 1):
        pixel_y = y * CELL_SIZE
        draw.line([(0, pixel_y), (1024, pixel_y)], fill='red', width=2)

    # Add cell numbers to first row (0-15)
    for i in range(GRID_SIZE):
        x = i * CELL_SIZE + 5
        y = 5
        draw.text((x, y), f"{i:X}", fill='yellow')

    # Add row numbers to first column (0-F)
    for i in range(GRID_SIZE):
        x = 5
        y = i * CELL_SIZE + 5
        draw.text((x, y), f"{i:X}", fill='yellow')

    img.save(output_path)
    print(f"Saved grid overlay to {output_path}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Create overlays for all jafont textures
    for i in range(1, 7):
        png_path = FONT_DIR / f"jafont_{i}.png"
        if png_path.exists():
            output_path = OUTPUT_DIR / f"jafont_{i}_grid.png"
            create_grid_overlay(png_path, output_path)
        else:
            print(f"Warning: {png_path} not found")

    print("\nDone! Open the _grid.png files to check if grid aligns with characters.")
    print("If characters are NOT centered in grid cells, our OCR cuts are wrong!")


if __name__ == "__main__":
    main()
