#!/usr/bin/env python3
"""
Extract individual character SVGs from atlas and generate MSDF using msdf-atlas-gen

Created: 2026-01-28 10:30 JST
Session: 3a41c4e3-eac1-45e9-80bf-ce8631a0faad
Purpose: Convert vectorized SVG atlas to TRUE multi-channel MSDF atlas
"""

import xml.etree.ElementTree as ET
import subprocess
import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image

# Configuration
SVG_ATLAS_PATH = "/mnt/c/Users/johnz/Desktop/gemini-3-pro-image-preview-2k_a_I_want_you_to_remake.svg"
OUTPUT_DIR = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/extracted_svgs")
MSDFGEN_PATH = Path.home() / "msdf-atlas-gen/build/bin/msdf-atlas-gen"
TEMP_FONT_PATH = OUTPUT_DIR / "temp_font.otf"

# Atlas parameters
ATLAS_SIZE = 1024
GRID_SIZE = 16
CELL_SIZE = 64

def extract_cell_bounds(svg_path):
    """
    Parse SVG and extract bounding boxes for each character cell.
    Returns list of (cell_index, paths) tuples.
    """
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # SVG namespace
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    # Find all path elements
    paths = root.findall('.//svg:path', ns)
    if not paths:
        # Try without namespace
        paths = root.findall('.//path')

    print(f"Found {len(paths)} paths in SVG")

    # Group paths by cell based on their bounding boxes
    cells = {}
    for path in paths:
        d = path.get('d')
        if not d:
            continue

        # Parse path to get bounding box (simplified - just check first coordinate)
        coords = []
        parts = d.replace(',', ' ').split()
        for i, part in enumerate(parts):
            try:
                if part[0].isdigit() or part[0] == '-':
                    coords.append(float(part))
            except (ValueError, IndexError):
                continue

        if len(coords) < 2:
            continue

        # Get approximate position (first coordinate in path)
        x, y = coords[0], coords[1]

        # Determine which cell this belongs to
        col = int(x / CELL_SIZE)
        row = int(y / CELL_SIZE)

        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            cell_index = row * GRID_SIZE + col
            if cell_index not in cells:
                cells[cell_index] = []
            cells[cell_index].append(path)

    print(f"Grouped into {len(cells)} cells")
    return cells

def create_individual_svg(paths, cell_index, output_path):
    """
    Create an individual SVG file for a single character cell.
    """
    # Calculate cell position
    row = cell_index // GRID_SIZE
    col = cell_index % GRID_SIZE
    cell_x = col * CELL_SIZE
    cell_y = row * CELL_SIZE

    # Create new SVG with just this cell's paths
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{CELL_SIZE}" height="{CELL_SIZE}" viewBox="{cell_x} {cell_y} {CELL_SIZE} {CELL_SIZE}" xmlns="http://www.w3.org/2000/svg">
'''

    for path in paths:
        # Copy path attributes
        d = path.get('d', '')
        fill = path.get('fill', '#000000')
        opacity = path.get('opacity', '1.0')

        svg_content += f'  <path d="{d}" fill="{fill}" opacity="{opacity}"/>\n'

    svg_content += '</svg>\n'

    with open(output_path, 'w') as f:
        f.write(svg_content)

def generate_msdf_from_svgs(svg_files, output_png):
    """
    Generate MSDF atlas from individual SVG files using msdf-atlas-gen.

    NOTE: msdf-atlas-gen requires font files, not SVGs.
    This is a limitation - we'll need to convert SVGs to a font first,
    or use msdfgen directly on each SVG.
    """
    print("ERROR: msdf-atlas-gen requires font files (OTF/TTF), not SVG files")
    print("We need to either:")
    print("1. Convert the SVG atlas to an OTF font file")
    print("2. Use msdfgen directly on each SVG (single-channel MSDF)")
    print("3. Use a different approach")
    return False

def generate_msdf_with_msdfgen(svg_file, output_png, size=64, pxrange=8):
    """
    Generate multi-channel MSDF from a single SVG using msdfgen directly.
    """
    msdfgen_path = Path.home() / "msdfgen/build/msdfgen"

    if not msdfgen_path.exists():
        print(f"ERROR: msdfgen not found at {msdfgen_path}")
        return None

    cmd = [
        str(msdfgen_path),
        'msdf',  # Multi-channel mode
        '-svg', str(svg_file),
        '-size', str(size), str(size),
        '-pxrange', str(pxrange),
        '-autoframe',
        '-o', str(output_png)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(output_png):
            return output_png
        else:
            print(f"msdfgen failed for {svg_file}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception running msdfgen: {e}")
        return None

def main():
    print("=" * 60)
    print("SVG Atlas to MSDF Converter")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Extract cells from SVG
    print(f"\nExtracting cells from {SVG_ATLAS_PATH}...")
    cells = extract_cell_bounds(SVG_ATLAS_PATH)

    if not cells:
        print("ERROR: No cells found in SVG")
        return 1

    # Create individual SVGs
    print(f"\nCreating individual SVG files...")
    svg_files = []
    for cell_index, paths in sorted(cells.items()):
        svg_path = OUTPUT_DIR / f"cell_{cell_index:03d}.svg"
        create_individual_svg(paths, cell_index, svg_path)
        svg_files.append((cell_index, svg_path))
        if cell_index < 5 or cell_index % 50 == 0:
            print(f"  Created {svg_path.name}")

    print(f"Created {len(svg_files)} individual SVG files")

    # Check if msdfgen supports SVG input
    msdfgen_path = Path.home() / "msdfgen/build/msdfgen"
    if not msdfgen_path.exists():
        print(f"\nERROR: msdfgen not found at {msdfgen_path}")
        print("Cannot proceed with MSDF generation")
        return 1

    # Test msdfgen with first cell
    print(f"\nTesting msdfgen with cell 0...")
    test_output = OUTPUT_DIR / "test_cell_0_msdf.png"
    result = generate_msdf_with_msdfgen(svg_files[0][1], test_output)

    if result:
        print(f"SUCCESS: Generated test MSDF at {test_output}")
        print("\nNow generating full MSDF atlas...")

        # Generate MSDF for each cell
        atlas = np.zeros((ATLAS_SIZE, ATLAS_SIZE, 4), dtype=np.uint8)

        for cell_index, svg_file in svg_files:
            output_png = OUTPUT_DIR / f"cell_{cell_index:03d}_msdf.png"

            msdf_file = generate_msdf_with_msdfgen(svg_file, output_png)
            if msdf_file:
                # Load MSDF image
                img = Image.open(msdf_file).convert('RGBA')
                img_array = np.array(img)

                # Place in atlas
                row = cell_index // GRID_SIZE
                col = cell_index % GRID_SIZE
                y_start = row * CELL_SIZE
                x_start = col * CELL_SIZE

                atlas[y_start:y_start+CELL_SIZE, x_start:x_start+CELL_SIZE] = img_array

                if cell_index % 10 == 0:
                    print(f"  Processed cell {cell_index}/255")

        # Save final atlas
        output_atlas = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/jafont_1_svg_msdf.png")
        Image.fromarray(atlas).save(output_atlas)
        print(f"\nSUCCESS: Generated MSDF atlas at {output_atlas}")
        print(f"Atlas size: {ATLAS_SIZE}x{ATLAS_SIZE} RGBA")
        print(f"Cells: {len(svg_files)}/{GRID_SIZE*GRID_SIZE}")

        return 0
    else:
        print("\nERROR: msdfgen test failed")
        print("Possible reasons:")
        print("1. msdfgen was built without SVG support")
        print("2. SVG file format is incompatible")
        print("3. Missing dependencies")
        return 1

if __name__ == '__main__':
    sys.exit(main())
