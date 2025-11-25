#!/usr/bin/env python3
"""
Measure actual glyph size by analyzing the character boundaries
Created: 2025-11-17 19:15:00 JST

Maybe the glyphs are NOT 64x64? Let's find out.
"""

from PIL import Image
from pathlib import Path

FONT_DIR = Path("extracted_fonts/png")
OUTPUT_DIR = Path("character_tables/debug")

def measure_glyph_spacing(img_path):
    """
    Look at the first row and measure the actual distance between character centers.
    """

    img = Image.open(img_path).convert('L')
    pixels = img.load()
    width = img.size[0]

    # Find vertical lines of mostly black (spaces between characters)
    # Scan the first row (y=0 to y=64) and look for vertical gaps

    print(f"Analyzing {img_path.name}...")
    print(f"Image dimensions: {img.size}")

    # For each x position, count how many pixels in first 64 rows are ink
    ink_density = []
    for x in range(width):
        ink_count = sum(1 for y in range(min(64, img.size[1])) if pixels[x, y] > 30)
        ink_density.append(ink_count)

    # Find the pattern - where does ink density drop significantly?
    # This should happen between characters

    print("\nInk density pattern (first 200 pixels):")
    print("Looking for gaps (low density = space between chars)...")

    # Find transition points (high to low density)
    gaps = []
    in_gap = False
    gap_start = 0

    for x in range(1, min(200, width)):
        if ink_density[x] < 5 and not in_gap:
            in_gap = True
            gap_start = x
        elif ink_density[x] >= 5 and in_gap:
            in_gap = False
            gap_center = (gap_start + x) // 2
            gaps.append(gap_center)
            print(f"  Gap found at x={gap_start}-{x} (center: {gap_center})")

    if len(gaps) >= 2:
        spacing = gaps[1] - gaps[0]
        print(f"\nMeasured character spacing: {spacing} pixels")
        print(f"(Compare to our assumed 64 pixels)")

    # Alternative: look for the repeating pattern
    print("\nManual inspection of first 128 pixels:")
    for x in range(0, 128, 8):
        density_block = sum(ink_density[x:x+8])
        bar = '#' * (density_block // 10)
        print(f"  x={x:3d}-{x+7:3d}: {density_block:3d} {bar}")


def extract_larger_sample(img_path):
    """Extract a larger area to see multiple characters."""

    img = Image.open(img_path)
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Extract first 3x3 characters (assuming 64px each = 192x192)
    sample = img.crop((0, 0, 256, 256))
    sample.save(OUTPUT_DIR / "first_256x256.png")
    print(f"\nSaved first 256x256 pixels to first_256x256.png")
    print("This should show ~4x4 characters if grid is 64px")
    print("Or ~5x5 if grid is smaller")


def main():
    measure_glyph_spacing(FONT_DIR / "jafont_1.png")
    extract_larger_sample(FONT_DIR / "jafont_1.png")


if __name__ == "__main__":
    main()
