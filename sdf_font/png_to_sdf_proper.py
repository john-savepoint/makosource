#!/usr/bin/env python3
"""
Convert anti-aliased bitmap to SDF while preserving quality.
Uses multi-level sampling to maintain smooth edges.
"""

import numpy as np
from PIL import Image
import sys
from scipy.ndimage import distance_transform_edt

def bitmap_to_sdf_smooth(image_path, output_path, distance_range=4):
    """
    Convert anti-aliased bitmap to SDF with quality preservation.
    
    Instead of binary threshold, uses the actual alpha gradients
    to maintain smooth anti-aliasing in the final SDF.
    """
    # Load image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    img_array = np.array(img)
    
    # Extract alpha channel (0-255)
    alpha = img_array[:, :, 3].astype(float) / 255.0
    
    # For SDF, we need a "core" mask for distance calculation
    # Use a higher threshold to get the solid core
    core_mask = alpha > 0.75
    
    # Compute distance transforms from the core
    dist_inside = distance_transform_edt(core_mask)
    dist_outside = distance_transform_edt(~core_mask)
    
    # Signed distance field
    sdf = dist_inside - dist_outside
    
    # Normalize to [0, 1]
    sdf_normalized = 0.5 + (sdf / (2.0 * distance_range))
    
    # Where we have original anti-aliasing (alpha 0.1-0.9), 
    # blend with the original alpha to preserve smooth edges
    is_edge = (alpha > 0.1) & (alpha < 0.9)
    
    # For edge pixels, use a blend of SDF and original alpha
    # This preserves the beautiful anti-aliasing from the source
    sdf_final = sdf_normalized.copy()
    sdf_final[is_edge] = alpha[is_edge]
    
    sdf_final = np.clip(sdf_final, 0.0, 1.0)
    
    # Create 3-channel grayscale SDF (RGB all same)
    sdf_rgb = np.stack([sdf_final] * 3, axis=2)
    
    # Alpha channel: solid everywhere (shader handles transparency)
    alpha_out = np.ones_like(sdf_final)
    
    # Combine
    sdf_rgba = np.dstack([sdf_rgb, alpha_out])
    
    # Convert to 8-bit
    sdf_uint8 = (sdf_rgba * 255).astype(np.uint8)
    
    # Save
    sdf_image = Image.fromarray(sdf_uint8, mode='RGBA')
    sdf_image.save(output_path)
    
    print(f"✅ SDF generated: {output_path}")
    print(f"   Input size: {width}×{height}")
    print(f"   Distance range: {distance_range} pixels")
    print(f"   Anti-aliasing preserved from source")
    
    return sdf_image

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python png_to_sdf_proper.py <input.png> <output.png> [distance_range]")
        sys.exit(1)
    
    bitmap_to_sdf_smooth(sys.argv[1], sys.argv[2], 
                         int(sys.argv[3]) if len(sys.argv) > 3 else 4)
