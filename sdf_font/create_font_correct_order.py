#!/usr/bin/env python3
"""
Create OTF with glyphs in CORRECT order matching FF7 character mapping
"""

import fontforge
import csv

# Create font
font = fontforge.font()
font.fontname = "FF7Japanese"
font.familyname = "FF7 Japanese"
font.fullname = "FF7 Japanese Regular"
font.encoding = "UnicodeFull"
font.em = 1000
font.ascent = 800
font.descent = 200

# Read character mapping to get correct order
csv_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/assets/character_mappings/interactive_viewer/ff7_complete_mapping_compact.csv"
svg_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/extracted_svgs/"

cell_to_unicode = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['texture'] == 'jafont_1':
            cell_index = int(row['index'])
            unicode_str = row['unicode'].strip()
            if unicode_str and unicode_str.startswith('U+'):
                unicode_hex = unicode_str.replace('U+', '')
                unicode_val = int(unicode_hex, 16)
                cell_to_unicode[cell_index] = unicode_val

print(f"Loaded {len(cell_to_unicode)} character mappings")

# Import SVGs in the order they appear in the atlas grid
imported = 0
for cell_index in range(256):
    svg_file = f"cell_{cell_index:03d}.svg"
    svg_path = f"{svg_dir}{svg_file}"

    # Get the Unicode value for this cell position
    if cell_index in cell_to_unicode:
        unicode_val = cell_to_unicode[cell_index]
    else:
        # Empty cell - map to Private Use Area
        unicode_val = 0xE000 + cell_index

    try:
        glyph = font.createChar(unicode_val)
        glyph.importOutlines(svg_path)
        glyph.width = 640
        imported += 1
        if imported % 50 == 0:
            print(f"  Imported {imported} glyphs...")
    except Exception as e:
        if cell_index in cell_to_unicode:
            print(f"WARNING: Failed cell {cell_index} (U+{unicode_val:04X}): {e}")

# Generate fonts
font.generate("/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/ff7_japanese_CORRECT_ORDER.otf")
print(f"\nSUCCESS: {imported} glyphs with correct Unicode mapping")
