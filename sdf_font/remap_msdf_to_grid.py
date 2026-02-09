#!/usr/bin/env python3
"""
Remap MSDF atlas from msdf-atlas-gen's packed layout to FF7's 16x16 grid layout

Created: 2026-01-28 10:50 JST
Session: 3a41c4e3-eac1-45e9-80bf-ce8631a0faad
Problem: msdf-atlas-gen packs glyphs efficiently, but FF7 expects fixed grid positions
Solution: Read JSON, extract each glyph, place in correct grid position
"""

import json
import numpy as np
from PIL import Image
from pathlib import Path

# Configuration
MSDF_JSON = "jafont_1_svg_msdf.json"
MSDF_PNG = "jafont_1_svg_TRUE_MSDF_RGBA.png"
OUTPUT_PNG = "jafont_1_svg_MSDF_GRID.png"

GRID_SIZE = 16
CELL_SIZE = 64
ATLAS_SIZE = 1024

def main():
    print("=" * 60)
    print("MSDF Atlas Grid Remapper")
    print("=" * 60)

    # Load JSON metadata
    with open(MSDF_JSON, 'r') as f:
        data = json.load(f)

    # Load MSDF atlas image
    msdf_img = Image.open(MSDF_PNG).convert('RGBA')
    msdf_array = np.array(msdf_img)

    print(f"Loaded MSDF atlas: {msdf_img.size}")
    print(f"Glyphs in JSON: {len(data['glyphs'])}")

    # Create new grid atlas (1024x1024 RGBA)
    grid_atlas = np.zeros((ATLAS_SIZE, ATLAS_SIZE, 4), dtype=np.uint8)

    # Process each glyph
    for glyph in data['glyphs']:
        unicode_val = glyph['unicode']

        # Calculate grid position from Unicode value
        # Glyphs are mapped to U+E000 - U+E0FF (Private Use Area)
        cell_index = unicode_val - 0xE000

        if cell_index < 0 or cell_index >= 256:
            print(f"WARNING: Glyph U+{unicode_val:04X} outside expected range")
            continue

        # Get atlas bounds from JSON (where msdf-atlas-gen placed it)
        bounds = glyph['atlasBounds']

        # Extract from packed atlas
        # Note: JSON uses bottom-left origin, need to flip Y
        atlas_height = data['atlas']['height']

        left = int(bounds['left'])
        right = int(bounds['right'])
        bottom = int(bounds['bottom'])
        top = int(bounds['top'])

        # Flip Y coordinate (JSON uses bottom-left, image uses top-left)
        bottom_flipped = atlas_height - top
        top_flipped = atlas_height - bottom

        # Validate bounds
        if bottom_flipped >= top_flipped or left >= right:
            print(f"WARNING: Invalid bounds for glyph {cell_index}, skipping")
            continue

        if bottom_flipped < 0 or top_flipped > atlas_height or left < 0 or right > atlas_height:
            print(f"WARNING: Out of bounds for glyph {cell_index}, skipping")
            continue

        # Extract glyph from packed atlas
        glyph_img = msdf_array[bottom_flipped:top_flipped, left:right]

        glyph_height, glyph_width = glyph_img.shape[:2]

        # Resize if larger than cell size
        if glyph_width > CELL_SIZE or glyph_height > CELL_SIZE:
            glyph_pil = Image.fromarray(glyph_img)
            glyph_pil = glyph_pil.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
            glyph_img = np.array(glyph_pil)
            glyph_height, glyph_width = CELL_SIZE, CELL_SIZE

        # Calculate target grid position
        row = cell_index // GRID_SIZE
        col = cell_index % GRID_SIZE

        # Calculate target cell bounds in grid atlas
        cell_y = row * CELL_SIZE
        cell_x = col * CELL_SIZE

        # Center the glyph in the cell
        offset_y = (CELL_SIZE - glyph_height) // 2
        offset_x = (CELL_SIZE - glyph_width) // 2

        target_y = cell_y + offset_y
        target_x = cell_x + offset_x

        # Place in grid atlas
        grid_atlas[target_y:target_y+glyph_height, target_x:target_x+glyph_width] = glyph_img

        if cell_index < 5 or cell_index % 50 == 0:
            print(f"  Cell {cell_index:03d} (U+{unicode_val:04X}): {glyph_width}x{glyph_height} -> grid[{row},{col}]")

    # Save grid atlas
    grid_img = Image.fromarray(grid_atlas)
    grid_img.save(OUTPUT_PNG)

    print(f"\nSUCCESS: Grid atlas saved to {OUTPUT_PNG}")
    print(f"Size: {ATLAS_SIZE}x{ATLAS_SIZE} RGBA")
    print(f"Layout: {GRID_SIZE}x{GRID_SIZE} grid, {CELL_SIZE}x{CELL_SIZE} cells")

if __name__ == '__main__':
    main()
