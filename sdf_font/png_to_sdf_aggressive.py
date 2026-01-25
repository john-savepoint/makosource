#!/usr/bin/env python3
"""
Aggressive SDF generation prioritizing solid cores and dramatic halos.
Designed specifically for bitmap fonts to maximize thickness control.
"""

import numpy as np
from PIL import Image
import sys
from scipy.ndimage import distance_transform_edt, maximum_filter, minimum_filter

def bitmap_to_sdf_aggressive(image_path, output_path, distance_range=12):
    """
    Generate SDF with:
    - Very large distance range (12px) for dramatic halos
    - Solid white cores throughout character strokes
    - Smooth gradients outside for anti-aliasing
    """
    # Load image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    img_array = np.array(img)
    
    # Extract alpha
    alpha = img_array[:, :, 3].astype(float) / 255.0
    
    # Create multiple masks at different thresholds
    # This helps maintain solid cores in thin strokes
    solid_core = alpha > 0.9     # Very opaque pixels
    main_body = alpha > 0.5      # Main character body
    soft_edge = alpha > 0.2      # Including anti-aliasing
    
    # Dilate the solid core slightly to ensure continuity
    from scipy.ndimage import binary_dilation
    solid_core_dilated = binary_dilation(solid_core, iterations=1)
    
    # Use the main body for distance calculation
    dist_inside = distance_transform_edt(main_body)
    dist_outside = distance_transform_edt(~main_body)
    
    # Signed distance field
    sdf = dist_inside - dist_outside
    
    # Normalize with LARGE distance range for dramatic effect
    sdf_normalized = 0.5 + (sdf / (2.0 * distance_range))
    sdf_normalized = np.clip(sdf_normalized, 0.0, 1.0)
    
    # Force solid cores where we know character strokes exist
    # This ensures white centers even in thin strokes
    sdf_final = sdf_normalized.copy()
    sdf_final[solid_core_dilated] = 1.0  # Force to white
    
    # Create RGB
    sdf_rgb = np.stack([sdf_final] * 3, axis=2)
    
    # Alpha: solid everywhere
    alpha_out = np.ones_like(sdf_final)
    
    # Combine
    sdf_rgba = np.dstack([sdf_rgb, alpha_out])
    
    # Convert to 8-bit
    sdf_uint8 = (sdf_rgba * 255).astype(np.uint8)
    
    # Save
    sdf_image = Image.fromarray(sdf_uint8, mode='RGBA')
    sdf_image.save(output_path)
    
    # Stats
    gray = sdf_uint8[:,:,0]
    print(f"✅ SDF generated: {output_path}")
    print(f"   Distance range: {distance_range}px (aggressive)")
    print(f"   Solid white (255): {np.sum(gray == 255):,} pixels")
    print(f"   Bright core (200-255): {np.sum(gray >= 200):,} pixels")
    print(f"   Gray halo (100-200): {np.sum((gray >= 100) & (gray < 200)):,} pixels")
    print(f"   Value range: {gray.min()}-{gray.max()}")
    
    return sdf_image

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python png_to_sdf_aggressive.py <input.png> <output.png> [distance_range]")
        print("Default distance_range: 12 (very large for maximum control)")
        sys.exit(1)
    
    bitmap_to_sdf_aggressive(sys.argv[1], sys.argv[2], 
                            int(sys.argv[3]) if len(sys.argv) > 3 else 12)
