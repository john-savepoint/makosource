#!/usr/bin/env python3
"""
Generate optimized SDF atlas by processing each character individually.
Allows larger spread values since we process glyphs separately before recombining.
"""

import sys
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

def bitmap_to_sdf_single(img_array, distance_range):
    """Generate SDF for a single character"""
    # Ensure binary mask
    mask = img_array > 128
    
    # Distance from background to foreground (inside)
    dist_inside = distance_transform_edt(mask)
    
    # Distance from foreground to background (outside)
    dist_outside = distance_transform_edt(~mask)
    
    # Combine
    sdf = dist_inside - dist_outside
    
    # Normalize to [0, 1] with distance range
    sdf_normalized = 0.5 + (sdf / (2.0 * distance_range))
    sdf_normalized = np.clip(sdf_normalized, 0.0, 1.0)
    
    return sdf_normalized

def process_atlas_to_sdf(input_path, output_path, char_width=16, char_height=16, distance_range=8):
    """
    Process font atlas to SDF atlas by generating SDF per character.
    
    Args:
        input_path: Clean font atlas PNG
        output_path: Output SDF atlas PNG
        char_width: Width of each character cell (default 16 for 64x64 chars in 1024x1024)
        char_height: Height of each character cell
        distance_range: SDF spread in pixels (can be larger since we process per-char)
    """
    # Load clean atlas
    img = Image.open(input_path).convert('RGBA')
    img_array = np.array(img)
    
    width, height = img.size
    
    # Calculate grid dimensions
    cols = width // char_width
    rows = height // char_height
    
    print(f"Processing {cols}x{rows} = {cols*rows} characters...")
    print(f"Character size: {char_width}x{char_height}")
    print(f"SDF spread: {distance_range} pixels")
    
    # Create output array
    sdf_atlas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Process each character cell
    for row in range(rows):
        for col in range(cols):
            # Extract character cell
            x1 = col * char_width
            y1 = row * char_height
            x2 = x1 + char_width
            y2 = y1 + char_height
            
            char_cell = img_array[y1:y2, x1:x2]
            
            # Check if cell has content
            if char_cell[:,:,3].max() > 0:
                # Generate SDF for this character's alpha channel
                alpha = char_cell[:,:,3]
                sdf_normalized = bitmap_to_sdf_single(alpha, distance_range)
                
                # Create RGB SDF (same value in all channels for simplicity)
                sdf_rgb = np.stack([sdf_normalized] * 3, axis=2)
                
                # Alpha: opaque where there's content
                sdf_alpha = (sdf_normalized > 0.5).astype(np.float32)
                
                # Combine RGBA
                sdf_rgba = np.dstack([sdf_rgb, sdf_alpha])
                sdf_uint8 = (sdf_rgba * 255).astype(np.uint8)
                
                # Place back in atlas
                sdf_atlas[y1:y2, x1:x2] = sdf_uint8
            
            # Progress indicator
            if (row * cols + col + 1) % 100 == 0:
                print(f"  Processed {row * cols + col + 1}/{cols*rows} characters...")
    
    # Save
    sdf_image = Image.fromarray(sdf_atlas, mode='RGBA')
    sdf_image.save(output_path)
    
    print(f"✅ SDF atlas generated: {output_path}")
    print(f"   Distance range: {distance_range} pixels")
    print(f"   Output format: RGBA (3-channel SDF + alpha)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python atlas_to_sdf_optimized.py <clean_atlas.png> <output_sdf.png> [distance_range] [char_size]")
        print("Example: python atlas_to_sdf_optimized.py jafont_1_00_clean.png jafont_1_00_sdf.png 8 16")
        print("")
        print("Arguments:")
        print("  distance_range: SDF spread in pixels (default: 8, can go higher)")
        print("  char_size: Character cell size in pixels (default: 16 for 64x64 grid)")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    distance_range = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    char_size = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    
    process_atlas_to_sdf(input_path, output_path, char_size, char_size, distance_range)
