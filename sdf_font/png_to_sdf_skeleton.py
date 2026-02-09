#!/usr/bin/env python3
"""
SDF generation with thin solid centerlines and dramatic halos.
Uses proper distance field that creates natural stroke skeletons.
"""

import numpy as np
from PIL import Image
import sys
from scipy.ndimage import distance_transform_edt

def bitmap_to_sdf_skeleton(image_path, output_path, distance_range=8):
    """
    Generate SDF where:
    - Maximum (255) only at stroke centerlines/skeleton
    - Smooth falloff creates dramatic gray halos
    - Anti-aliasing from source preserved at edges
    """
    # Load image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    img_array = np.array(img)
    
    # Extract alpha (0-1)
    alpha = img_array[:, :, 3].astype(float) / 255.0
    
    # Create mask - use medium threshold to get main body
    # Not too high (preserves thin strokes) not too low (avoids AA blur)
    mask = alpha > 0.6
    
    # Distance from INSIDE pixels to nearest EDGE
    # This creates maximum values at stroke centers (far from edges)
    dist_to_edge = distance_transform_edt(mask)
    
    # Distance from OUTSIDE pixels to nearest edge
    dist_outside = distance_transform_edt(~mask)
    
    # Combine: inside is positive, outside is negative
    sdf = dist_to_edge - dist_outside
    
    # Normalize with large range for dramatic halos
    # The key: don't clamp the inside too aggressively
    # Let the natural distance falloff create thin centerlines
    sdf_normalized = 0.5 + (sdf / (2.0 * distance_range))
    sdf_normalized = np.clip(sdf_normalized, 0.0, 1.0)
    
    # Where original has anti-aliasing, blend it subtly
    # This preserves smooth edges without destroying the distance field
    is_edge = (alpha > 0.1) & (alpha < 0.85)
    blend_weight = 0.2  # 20% original, 80% SDF
    
    sdf_final = sdf_normalized.copy()
    sdf_final[is_edge] = (
        blend_weight * alpha[is_edge] + 
        (1 - blend_weight) * sdf_normalized[is_edge]
    )
    
    sdf_final = np.clip(sdf_final, 0.0, 1.0)
    
    # Create RGB
    sdf_rgb = np.stack([sdf_final] * 3, axis=2)
    
    # Alpha: solid
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
    print(f"   Distance range: {distance_range}px")
    print(f"   Skeleton (250-255): {np.sum(gray >= 250):,} pixels (thin centerlines)")
    print(f"   Bright (200-250): {np.sum((gray >= 200) & (gray < 250)):,} pixels")
    print(f"   Gray halo (100-200): {np.sum((gray >= 100) & (gray < 200)):,} pixels")
    print(f"   Value range: {gray.min()}-{gray.max()}")
    
    return sdf_image

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python png_to_sdf_skeleton.py <input.png> <output.png> [distance_range]")
        sys.exit(1)
    
    bitmap_to_sdf_skeleton(sys.argv[1], sys.argv[2], 
                           int(sys.argv[3]) if len(sys.argv) > 3 else 8)
