#!/usr/bin/env python3
"""
Create clean OTF font from extracted SVG cells using FontForge

Created: 2026-01-28 14:05 JST
Session: 3a41c4e3-eac1-45e9-80bf-ce8631a0faad
Purpose: Fix corrupted OTF by creating from scratch with proper settings
"""

import fontforge
import os

# Create new font
font = fontforge.font()
font.fontname = "FF7Japanese"
font.familyname = "FF7 Japanese"
font.fullname = "FF7 Japanese Regular"
font.encoding = "UnicodeFull"

# Set metrics (important for proper rendering)
font.em = 1000
font.ascent = 800
font.descent = 200

# Import SVGs
svg_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/extracted_svgs/"
svg_files = sorted([f for f in os.listdir(svg_dir) if f.startswith('cell_') and f.endswith('.svg')])

print(f"Found {len(svg_files)} SVG files")

# Map to Unicode Private Use Area (U+E000 onwards)
codepoint = 0xE000
imported = 0

for svg_file in svg_files:
    svg_path = os.path.join(svg_dir, svg_file)
    try:
        glyph = font.createChar(codepoint)
        glyph.importOutlines(svg_path)
        glyph.width = 640  # 64% of em (proportional to 64px cell in 1000 EM units)
        imported += 1
        if imported % 50 == 0:
            print(f"  Imported {imported} glyphs...")
        codepoint += 1
    except Exception as e:
        print(f"WARNING: Failed to import {svg_file}: {e}")
        codepoint += 1

# Generate fonts
output_otf = "/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/ff7_japanese_CLEAN.otf"
output_ttf = "/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/ff7_japanese_CLEAN.ttf"

print(f"\nGenerating OTF...")
font.generate(output_otf)
print(f"Generated: {output_otf}")

print(f"Generating TTF...")
font.generate(output_ttf)
print(f"Generated: {output_ttf}")

print(f"\nSUCCESS: Created fonts with {imported} glyphs")
print(f"Unicode range: U+E000 - U+{codepoint-1:04X}")
