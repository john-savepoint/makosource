#!/usr/bin/env python3
"""
Convert SVG atlas to OTF font file for MSDF generation

Created: 2026-01-28 10:30 JST
Session: 3a41c4e3-eac1-45e9-80bf-ce8631a0faad
Purpose: Convert vectorized SVG atlas to OTF so msdf-atlas-gen can generate MSDF
"""

import fontforge
import sys
from pathlib import Path

# Configuration
SVG_ATLAS_PATH = "/mnt/c/Users/johnz/Desktop/gemini-3-pro-image-preview-2k_a_I_want_you_to_remake.svg"
EXTRACTED_SVGS_DIR = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/extracted_svgs")
OUTPUT_OTF = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/jafont_1_from_svg.otf")

# Atlas parameters
GRID_SIZE = 16
TOTAL_CELLS = 256

def create_font_from_svg_cells():
    """
    Create an OTF font from extracted SVG cells.
    Each cell becomes a glyph mapped to a Unicode codepoint.
    """
    print("Creating new font...")

    # Create new font
    font = fontforge.font()
    font.fontname = "JAFont1SVG"
    font.familyname = "JA Font 1 SVG"
    font.fullname = "JA Font 1 from SVG"
    font.encoding = "UnicodeFull"
    font.em = 1000  # Units per em

    # Set font metrics
    font.ascent = 800
    font.descent = 200

    # Check which SVG cells exist
    svg_files = sorted(EXTRACTED_SVGS_DIR.glob("cell_*.svg"))
    print(f"Found {len(svg_files)} SVG cell files")

    if not svg_files:
        print(f"ERROR: No SVG files found in {EXTRACTED_SVGS_DIR}")
        print("Make sure extraction script has been run first")
        return None

    # Import each SVG as a glyph
    # Map to Unicode private use area starting at U+E000
    base_codepoint = 0xE000

    glyphs_created = 0
    for svg_file in svg_files:
        # Extract cell index from filename (e.g., cell_045.svg -> 45)
        cell_index = int(svg_file.stem.split('_')[1])

        # Map to Unicode codepoint
        codepoint = base_codepoint + cell_index

        try:
            # Create glyph at this codepoint
            glyph = font.createChar(codepoint)

            # Import SVG into glyph
            glyph.importOutlines(str(svg_file))

            # Set glyph width (square characters)
            glyph.width = 640  # 64% of em (640 out of 1000)

            glyphs_created += 1

            if glyphs_created % 50 == 0:
                print(f"  Imported {glyphs_created} glyphs...")

        except Exception as e:
            print(f"WARNING: Failed to import {svg_file.name}: {e}")
            continue

    print(f"\nCreated {glyphs_created} glyphs in font")

    # Generate OTF file
    print(f"Generating OTF font at {OUTPUT_OTF}...")
    font.generate(str(OUTPUT_OTF))

    print(f"SUCCESS: OTF font created with {glyphs_created} glyphs")
    return OUTPUT_OTF

def main():
    print("=" * 60)
    print("SVG Atlas to OTF Font Converter")
    print("=" * 60)

    # Create output directory
    OUTPUT_OTF.parent.mkdir(parents=True, exist_ok=True)

    # Create font from SVG cells
    otf_file = create_font_from_svg_cells()

    if otf_file:
        print(f"\nOTF file ready at: {otf_file}")
        print(f"Glyphs mapped to Unicode range: U+E000 - U+E0FF (Private Use Area)")
        print(f"\nNext step: Use msdf-atlas-gen with this OTF file")
        return 0
    else:
        print("\nERROR: Failed to create OTF font")
        return 1

if __name__ == '__main__':
    sys.exit(main())
