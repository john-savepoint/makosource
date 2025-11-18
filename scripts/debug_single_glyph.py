#!/usr/bin/env python3
"""
Debug Single Glyph - See exactly what OCR receives
Created: 2025-11-17 19:07:00 JST

Shows the preprocessing pipeline step-by-step for a single character.
"""

from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path

FONT_DIR = Path("extracted_fonts/png")
OUTPUT_DIR = Path("character_tables/debug")
CELL_SIZE = 64

def extract_and_debug_glyph(texture_path, grid_x, grid_y, offset_x=0, offset_y=0):
    """Extract a single glyph and show all preprocessing steps."""

    img = Image.open(texture_path)

    # Original extraction (current method)
    pixel_x = grid_x * CELL_SIZE
    pixel_y = grid_y * CELL_SIZE

    # Apply offset correction
    pixel_x += offset_x
    pixel_y += offset_y

    # Crop the glyph
    glyph = img.crop((pixel_x, pixel_y, pixel_x + CELL_SIZE, pixel_y + CELL_SIZE))
    glyph.save(OUTPUT_DIR / "step1_raw_glyph.png")
    print(f"Step 1: Raw glyph saved (offset: x={offset_x}, y={offset_y})")

    # Convert to grayscale
    gray = glyph.convert('L')
    gray.save(OUTPUT_DIR / "step2_grayscale.png")
    print("Step 2: Grayscale conversion")

    # Invert colors
    inverted = ImageOps.invert(gray)
    inverted.save(OUTPUT_DIR / "step3_inverted.png")
    print("Step 3: Inverted (now black on white)")

    # Boost contrast
    enhancer = ImageEnhance.Contrast(inverted)
    contrast = enhancer.enhance(2.0)
    contrast.save(OUTPUT_DIR / "step4_contrast.png")
    print("Step 4: Contrast enhanced")

    # Add padding
    padded = Image.new('L', (CELL_SIZE + 20, CELL_SIZE + 20), 255)
    padded.paste(contrast, (10, 10))
    padded.save(OUTPUT_DIR / "step5_padded.png")
    print("Step 5: Padding added")

    # Scale up
    scaled = padded.resize((padded.width * 2, padded.height * 2), Image.LANCZOS)
    scaled.save(OUTPUT_DIR / "step6_scaled.png")
    print("Step 6: Scaled 2x (this is what OCR sees)")

    # Try OCR on this
    try:
        import pytesseract
        config = '--psm 10 --oem 3'

        # Try with inverted (black on white)
        result_inverted = pytesseract.image_to_string(scaled, lang='jpn', config=config).strip()
        print(f"\nOCR result (inverted/black on white): '{result_inverted}'")

        # Also try WITHOUT inversion (white on black) - maybe Tesseract prefers this?
        gray_padded = Image.new('L', (CELL_SIZE + 20, CELL_SIZE + 20), 0)
        gray_padded.paste(gray, (10, 10))
        gray_scaled = gray_padded.resize((gray_padded.width * 2, gray_padded.height * 2), Image.LANCZOS)
        gray_scaled.save(OUTPUT_DIR / "step6_alt_no_invert.png")
        result_no_invert = pytesseract.image_to_string(gray_scaled, lang='jpn', config=config).strip()
        print(f"OCR result (white on black, no invert): '{result_no_invert}'")

    except Exception as e:
        print(f"OCR error: {e}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Test with grid position (9, 0) - the "四" kanji you mentioned
    # First without offset
    print("="*50)
    print("Testing grid (9, 0) WITHOUT offset correction:")
    print("="*50)
    extract_and_debug_glyph(FONT_DIR / "jafont_1.png", 9, 0, offset_x=0, offset_y=0)

    # Then with your suggested offset
    print("\n" + "="*50)
    print("Testing grid (9, 0) WITH offset correction (+5px left, +2px top):")
    print("="*50)
    extract_and_debug_glyph(FONT_DIR / "jafont_1.png", 9, 0, offset_x=5, offset_y=2)

    print("\n" + "="*50)
    print(f"Debug images saved to {OUTPUT_DIR}/")
    print("Open step1-6 PNGs to see the preprocessing pipeline")
    print("="*50)


if __name__ == "__main__":
    main()
