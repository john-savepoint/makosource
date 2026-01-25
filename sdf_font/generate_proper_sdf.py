#!/usr/bin/env python3
"""
Generate PROPER multi-channel SDF (MSDF) from font atlas.
The output should look like a gray cloud - not like the sharp original!
"""

import sys
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

def generate_sdf_for_char(alpha_channel, spread):
    """
    Generate a proper SDF with smooth gradients.
    
    The output should be GRAY/CLOUDY, not sharp!
    """
    # Convert to binary mask
    mask = alpha_channel > 128
    
    # Distance transform - distance from each pixel to nearest edge
    # Inside pixels: positive distance to edge
    # Outside pixels: negative distance to edge
    
    if mask.any():
        # Distance from inside to edge
        dist_inside = distance_transform_edt(mask)
        # Distance from outside to edge  
        dist_outside = distance_transform_edt(~mask)
        
        # Signed distance: positive inside, negative outside
        sdf = dist_inside - dist_outside
    else:
        # Empty cell
        sdf = np.full_like(alpha_channel, -spread, dtype=float)
    
    # Normalize to 0-1 range
    # 0.5 = exactly on the edge
    # 0.0 = far outside (spread distance away)
    # 1.0 = far inside (spread distance away)
    sdf_normalized = 0.5 + (sdf / spread)
    sdf_normalized = np.clip(sdf_normalized, 0.0, 1.0)
    
    return sdf_normalized

def process_atlas(input_path, output_path, char_size=16, spread=4):
    """
    Process entire atlas to SDF.
    """
    print(f"Loading: {input_path}")
    img = Image.open(input_path).convert('RGBA')
    img_array = np.array(img)
    
    width, height = img.size
    cols = width // char_size
    rows = height // char_size
    
    print(f"Processing {cols}x{rows} grid, char size: {char_size}x{char_size}")
    print(f"Spread: {spread} pixels")
    print(f"Output should look CLOUDY/GRAY, not sharp!")
    
    # Output array - will be grayscale SDF
    sdf_output = np.zeros((height, width, 4), dtype=np.uint8)
    
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * char_size, row * char_size
            x2, y2 = x1 + char_size, y1 + char_size
            
            # Extract character alpha
            char_alpha = img_array[y1:y2, x1:x2, 3]
            
            # Generate SDF
            sdf = generate_sdf_for_char(char_alpha, spread)
            
            # For MSDF (multi-channel SDF), we put the same value in RGB
            # In a true MSDF, each channel would encode different corner directions
            # For simplicity, we'll use single-channel approach
            sdf_uint8 = (sdf * 255).astype(np.uint8)
            
            # Put SDF value in all RGB channels (grayscale)
            sdf_output[y1:y2, x1:x2, 0] = sdf_uint8  # R
            sdf_output[y1:y2, x1:x2, 1] = sdf_uint8  # G  
            sdf_output[y1:y2, x1:x2, 2] = sdf_uint8  # B
            
            # Alpha: full opacity everywhere (we encode distance in RGB)
            sdf_output[y1:y2, x1:x2, 3] = 255
            
            if (row * cols + col + 1) % 500 == 0:
                print(f"  Processed {row * cols + col + 1}/{cols * rows}...")
    
    # Save
    sdf_img = Image.fromarray(sdf_output, mode='RGBA')
    sdf_img.save(output_path)
    
    print(f"\n✅ Proper SDF generated: {output_path}")
    print(f"   The image should look GRAY/CLOUDY")
    print(f"   Characters should have gray halos around them")
    print(f"   NOT sharp like the original!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_proper_sdf.py <input.png> <output.png> [spread] [char_size]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    spread = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    char_size = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    
    process_atlas(input_path, output_path, char_size, spread)
