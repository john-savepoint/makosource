#!/usr/bin/env python3
"""
Clean font texture for SDF generation by removing drop shadows and colors.
Converts all non-transparent pixels to pure white.
"""

import sys
from PIL import Image
import numpy as np

def clean_font_texture(input_path, output_path):
    """Remove colors and drop shadows, keeping only white glyphs."""
    
    # Load the image
    img = Image.open(input_path).convert('RGBA')
    img_array = np.array(img)
    
    # Separate channels
    r, g, b, a = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2], img_array[:,:,3]
    
    # Create clean version: white where there's any opacity, transparent elsewhere
    # Use a threshold to determine what counts as "content"
    content_mask = a > 128  # Pixels with >50% opacity are considered content
    
    # Create new image: pure white with original alpha
    clean = np.zeros_like(img_array)
    clean[:,:,0] = np.where(content_mask, 255, 0)  # R
    clean[:,:,1] = np.where(content_mask, 255, 0)  # G
    clean[:,:,2] = np.where(content_mask, 255, 0)  # B
    clean[:,:,3] = np.where(content_mask, 255, 0)  # A - full opacity where there's content
    
    # Save
    clean_img = Image.fromarray(clean.astype(np.uint8), mode='RGBA')
    clean_img.save(output_path)
    
    print(f"✅ Cleaned font texture: {output_path}")
    print(f"   Input: {input_path}")
    print(f"   Output format: Pure white glyphs, transparent background")
    
    return clean_img

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_font_for_sdf.py <input.png> <output.png>")
        print("Example: python clean_font_for_sdf.py jafont_1_00.png jafont_1_00_clean.png")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    clean_font_texture(input_path, output_path)
