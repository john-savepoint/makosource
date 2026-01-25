#!/usr/bin/env python3
"""
Clean font texture for SDF generation - PRESERVES anti-aliasing quality.
Only removes drop shadows (dark pixels), keeps all bright anti-aliased edges.
"""

import sys
from PIL import Image
import numpy as np

def clean_font_texture(input_path, output_path):
    """Remove drop shadows while preserving anti-aliasing gradients."""
    
    # Load the image
    img = Image.open(input_path).convert('RGBA')
    img_array = np.array(img, dtype=np.float32)
    
    # Separate channels
    r, g, b, a = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2], img_array[:,:,3]
    
    # Calculate brightness (0-255)
    brightness = (r + g + b) / 3.0
    
    # Identify drop shadow: dark pixels with opacity
    # Drop shadows are typically brightness < 100, main glyphs are > 150
    is_drop_shadow = (brightness < 100) & (a > 0)
    
    # Keep everything that's NOT a drop shadow
    # This preserves all anti-aliasing gradients on the main glyph
    keep_mask = ~is_drop_shadow & (a > 0)
    
    # For pixels we keep, normalize to white but preserve alpha gradients
    clean = np.zeros_like(img_array)
    
    # Where we have content, make it white but keep the alpha gradient
    clean[:,:,0] = np.where(keep_mask, 255, 0)  # R = white
    clean[:,:,1] = np.where(keep_mask, 255, 0)  # G = white
    clean[:,:,2] = np.where(keep_mask, 255, 0)  # B = white
    
    # Preserve original alpha where we're keeping content
    # This maintains all the beautiful anti-aliasing
    clean[:,:,3] = np.where(keep_mask, a, 0)
    
    # Save
    clean_img = Image.fromarray(clean.astype(np.uint8), mode='RGBA')
    clean_img.save(output_path)
    
    # Stats
    total_pixels = img_array.shape[0] * img_array.shape[1]
    shadow_pixels = np.sum(is_drop_shadow)
    kept_pixels = np.sum(keep_mask)
    
    print(f"✅ Cleaned font texture: {output_path}")
    print(f"   Removed {shadow_pixels} shadow pixels ({shadow_pixels/total_pixels*100:.1f}%)")
    print(f"   Kept {kept_pixels} glyph pixels ({kept_pixels/total_pixels*100:.1f}%)")
    print(f"   Preserved anti-aliasing gradients")
    
    return clean_img

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_font_for_sdf_v2.py <input.png> <output.png>")
        sys.exit(1)
    
    clean_font_texture(sys.argv[1], sys.argv[2])
