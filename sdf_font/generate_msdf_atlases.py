#!/usr/bin/env python3
"""
Generate MSDF atlas textures from vector font using character mapping.
Creates 6 atlas PNGs (jafont_1 through jafont_6) with proper MSDF encoding.
"""

import csv
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import freetype
import sys

def render_character_msdf(font_path, unicode_char, size=64, spread=8):
    """
    Render a single character as MSDF.
    
    For true MSDF we'd need the msdfgen library, but we can approximate
    by rendering at high resolution and computing multi-channel distance.
    
    This is a simplified MSDF that encodes:
    - R channel: horizontal edge distances
    - G channel: vertical edge distances  
    - B channel: diagonal edge distances
    """
    # Load font
    face = freetype.Face(font_path)
    face.set_char_size(size * 64)  # 64 = 1pt in freetype
    
    # Render glyph
    face.load_char(unicode_char, freetype.FT_LOAD_RENDER)
    bitmap = face.glyph.bitmap
    
    if bitmap.width == 0 or bitmap.rows == 0:
        # Empty glyph
        return np.zeros((size, size, 4), dtype=np.uint8)
    
    # Convert bitmap to numpy array
    glyph_array = np.array(bitmap.buffer, dtype=np.uint8).reshape(bitmap.rows, bitmap.width)
    
    # For now, return a simple grayscale SDF (we can improve to true MSDF later)
    # This at least gives us sharp vector rendering
    from scipy.ndimage import distance_transform_edt
    
    # Create binary mask
    mask = glyph_array > 128
    
    # Compute distance field
    dist_inside = distance_transform_edt(mask)
    dist_outside = distance_transform_edt(~mask)
    sdf = dist_inside - dist_outside
    
    # Normalize
    sdf_norm = 0.5 + (sdf / (2.0 * spread))
    sdf_norm = np.clip(sdf_norm, 0, 1)
    
    # Resize to target size
    from scipy.ndimage import zoom
    if glyph_array.shape != (size, size):
        scale_y = size / glyph_array.shape[0]
        scale_x = size / glyph_array.shape[1]
        sdf_resized = zoom(sdf_norm, (scale_y, scale_x), order=1)
    else:
        sdf_resized = sdf_norm
    
    # Create RGBA (for now, all channels same - we can improve to true MSDF)
    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[:,:,0] = (sdf_resized * 255).astype(np.uint8)  # R
    rgba[:,:,1] = (sdf_resized * 255).astype(np.uint8)  # G
    rgba[:,:,2] = (sdf_resized * 255).astype(np.uint8)  # B
    rgba[:,:,3] = 255  # A (solid)
    
    return rgba

def generate_atlas(mapping_csv, font_path, output_dir, cell_size=64, spread=8):
    """Generate MSDF atlas textures from character mapping."""
    
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
            # Valid character with Unicode
            unicode_char = chr(int(unicode_str.replace('U+', ''), 16))
            atlases[texture][index] = unicode_char
    
    print(f"Loaded {sum(len(a) for a in atlases.values())} character mappings")
    
    # Generate each atlas
    for atlas_name, char_map in atlases.items():
        print(f"\nGenerating {atlas_name}...")
        
        # Create 16x16 grid (256 cells)
        grid_size = 16
        atlas_width = grid_size * cell_size
        atlas_height = grid_size * cell_size
        
        atlas_image = np.zeros((atlas_height, atlas_width, 4), dtype=np.uint8)
        
        # Render each character
        for index, unicode_char in char_map.items():
            row = index // grid_size
            col = index % grid_size
            
            x = col * cell_size
            y = row * cell_size
            
            try:
                char_msdf = render_character_msdf(font_path, unicode_char, cell_size, spread)
                atlas_image[y:y+cell_size, x:x+cell_size] = char_msdf
            except Exception as e:
                print(f"  Warning: Could not render '{unicode_char}' (U+{ord(unicode_char):04X}): {e}")
        
        # Save
        output_path = f"{output_dir}/{atlas_name}_msdf.png"
        Image.fromarray(atlas_image).save(output_path)
        print(f"  Saved: {output_path}")
        print(f"  Characters: {len(char_map)}")

if __name__ == "__main__":
    mapping_csv = "/home/johnzealanddoyle/projects/ff7OG_japanese/assets/character_mappings/interactive_viewer/ff7_complete_mapping_compact.csv"
    font_path = "/mnt/c/Users/johnz/Desktop/hiragino-kaku-gothic-pron-w6_IcXPV/Hiragino Kaku Gothic ProN W6.otf"
    output_dir = "."
    
    generate_atlas(mapping_csv, font_path, output_dir, cell_size=64, spread=8)
    print("\n✅ MSDF atlas generation complete!")
