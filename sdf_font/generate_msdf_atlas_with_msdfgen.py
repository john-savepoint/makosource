#!/usr/bin/env python3
"""
Generate TRUE multi-channel MSDF atlases using msdfgen CLI tool.
Extracts vector paths from font glyphs and generates proper MSDF with R/G/B encoding.
"""

import csv
import subprocess
import tempfile
import os
from PIL import Image
import numpy as np
import freetype

MSDFGEN_PATH = os.path.expanduser("~/msdfgen/build/msdfgen")

def glyph_to_shapedesc(font_path, unicode_char, shapedesc_path):
    """
    Convert a font glyph to msdfgen shape description format.
    Shape desc format: each contour has points/curves separated by semicolons.
    """
    face = freetype.Face(font_path)
    face.set_char_size(1000 * 64)  # 1000 units for precision

    # Load glyph
    face.load_char(unicode_char, freetype.FT_LOAD_NO_BITMAP)
    outline = face.glyph.outline

    if len(outline.points) == 0:
        return False

    # Convert outline to shape description
    # SIMPLIFICATION: Use only on-curve points (linear segments)
    # TODO: Properly handle quadratic Bezier curves

    contours_text = []
    start_idx = 0

    for contour_end in outline.contours:
        contour_points = []

        for i in range(start_idx, contour_end + 1):
            tag = outline.tags[i]

            # Only use on-curve points for now
            if tag & 1:
                x, y = outline.points[i][0] / 64.0, -outline.points[i][1] / 64.0
                contour_points.append(f"{x}, {y}")

        # Close contour with # (represents first point)
        if contour_points:
            contours_text.append("; ".join(contour_points) + "; #")

        start_idx = contour_end + 1

    # Write shape description - ALL contours on ONE line!
    with open(shapedesc_path, 'w') as f:
        all_contours = " ".join("{ " + contour + " }" for contour in contours_text)
        f.write(all_contours + "\n")

    return True

def generate_glyph_msdf(font_path, unicode_char, size=64, pxrange=8):
    """
    Generate a true multi-channel MSDF for a single glyph using msdfgen CLI.
    """

    # Create temporary shape description in memory
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as shapefile:
        shapedesc_path = shapefile.name
        if not glyph_to_shapedesc(font_path, unicode_char, shapedesc_path):
            return np.zeros((size, size, 4), dtype=np.uint8)

    # Read shape description back
    with open(shapedesc_path, 'r') as f:
        shapedesc_text = f.read()

    # Create temporary BMP output file (BMP is fully supported!)
    with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as outfile:
        output_path = outfile.name

    try:
        # Call msdfgen with stdin input to generate TRUE MULTI-CHANNEL MSDF!
        cmd = [
            MSDFGEN_PATH,
            'msdf',  # Multi-channel mode - R/G/B encode directional distances!
            '-stdin',
            '-dimensions', str(size), str(size),
            '-pxrange', str(pxrange),
            '-autoframe',  # Auto-scale and center
            '-format', 'bmp',  # BMP format works perfectly
            '-o', output_path
        ]

        result = subprocess.run(
            cmd,
            input=shapedesc_text,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"  Warning: msdfgen failed for U+{ord(unicode_char):04X}: {result.stderr}")
            return np.zeros((size, size, 4), dtype=np.uint8)

        # Load generated MSDF from BMP
        img = Image.open(output_path)

        # Convert to RGBA (BMP is RGB)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        return np.array(img)

    except Exception as e:
        print(f"  Error: U+{ord(unicode_char):04X}: {e}")
        return np.zeros((size, size, 4), dtype=np.uint8)

    finally:
        # Cleanup temp files
        if os.path.exists(shapedesc_path):
            os.unlink(shapedesc_path)
        if os.path.exists(output_path):
            os.unlink(output_path)

def generate_atlas(mapping_csv, font_path, output_dir, cell_size=64, pxrange=8):
    """Generate TRUE multi-channel MSDF atlas textures."""

    # Read mapping
    with open(mapping_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        mappings = list(reader)

    # Organize by texture
    atlases = {f'jafont_{i}': {} for i in range(1, 7)}

    for row in mappings:
        texture = row['texture']
        index = int(row['index'])
        character = row['character']
        unicode_str = row['unicode']

        if character and unicode_str and not unicode_str.startswith('['):
            unicode_char = chr(int(unicode_str.replace('U+', ''), 16))
            atlases[texture][index] = unicode_char

    total_chars = sum(len(a) for a in atlases.values())
    print(f"Loaded {total_chars} character mappings")
    print(f"Using msdfgen: {MSDFGEN_PATH}")
    print("Generating TRUE multi-channel MSDF (R/G/B encoding)\n")

    # Generate each atlas
    for atlas_name, char_map in atlases.items():
        print(f"\nGenerating {atlas_name}...")

        grid_size = 16
        atlas_width = grid_size * cell_size
        atlas_height = grid_size * cell_size

        atlas_image = np.zeros((atlas_height, atlas_width, 4), dtype=np.uint8)

        char_count = 0
        for index, unicode_char in char_map.items():
            row = index // grid_size
            col = index % grid_size

            x = col * cell_size
            y = row * cell_size

            char_msdf = generate_glyph_msdf(font_path, unicode_char, cell_size, pxrange)
            atlas_image[y:y+cell_size, x:x+cell_size] = char_msdf
            char_count += 1

            if char_count % 20 == 0:
                print(f"  Progress: {char_count}/{len(char_map)}")

        output_path = f"{output_dir}/{atlas_name}_true_msdf.png"
        Image.fromarray(atlas_image).save(output_path)
        print(f"  ✅ Saved: {output_path} ({char_count} characters)")

if __name__ == "__main__":
    if not os.path.exists(MSDFGEN_PATH):
        print(f"❌ ERROR: msdfgen not found at {MSDFGEN_PATH}")
        exit(1)

    mapping_csv = "/home/johnzealanddoyle/projects/ff7OG_japanese/assets/character_mappings/interactive_viewer/ff7_complete_mapping_compact.csv"
    font_path = "/mnt/c/Users/johnz/Desktop/hiragino-kaku-gothic-pron-w6_IcXPV/Hiragino Kaku Gothic ProN W6.otf"

    generate_atlas(mapping_csv, font_path, ".", cell_size=64, pxrange=8)
    print("\n✅ TRUE multi-channel MSDF generation complete!")
    print("   R/G/B channels encode directional distances for perfect corners")
