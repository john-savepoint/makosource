#!/usr/bin/env python3
"""
High-quality SDF generation with extended range for thickness control.
Uses larger distance field with proper anti-aliasing preservation.
"""

import numpy as np
from PIL import Image
import sys
from scipy.ndimage import distance_transform_edt, gaussian_filter

def bitmap_to_sdf_extended(image_path, output_path, distance_range=8):
    """
    Generate SDF with extended distance range for better boldness control.
    
    Key improvements:
    - Larger distance range (8px default vs 4px)
    - Uses actual alpha values, not binary threshold
    - Smooth gradients throughout
    - Solid white cores in character centers
    """
    # Load image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    img_array = np.array(img)
    
    # Extract alpha channel (0-1 range)
    alpha = img_array[:, :, 3].astype(float) / 255.0
    
    # Create a high-quality binary mask for distance calculation
    # Use multiple thresholds and average for smoother result
    masks = []
    for threshold in [0.3, 0.5, 0.7, 0.9]:
        masks.append((alpha > threshold).astype(float))
    
    # Average the masks for a smoother transition
    smooth_mask = np.mean(masks, axis=0) > 0.5
    
    # Compute distance transforms
    dist_inside = distance_transform_edt(smooth_mask)
    dist_outside = distance_transform_edt(~smooth_mask)
    
    # Signed distance field
    sdf = dist_inside - dist_outside
    
    # Normalize with extended range
    # This gives us more data for thickness adjustment
    sdf_normalized = 0.5 + (sdf / (2.0 * distance_range))
    sdf_normalized = np.clip(sdf_normalized, 0.0, 1.0)
    
    # Apply slight gaussian blur to smooth out any stepping
    sdf_smooth = gaussian_filter(sdf_normalized, sigma=0.5)
    
    # Where we have original anti-aliasing, blend it in
    # But only subtly - we want SDF to dominate for thickness control
    has_original_aa = (alpha > 0.05) & (alpha < 0.95)
    blend_factor = 0.3  # 30% original AA, 70% SDF
    
    sdf_final = sdf_smooth.copy()
    sdf_final[has_original_aa] = (
        blend_factor * alpha[has_original_aa] + 
        (1 - blend_factor) * sdf_smooth[has_original_aa]
    )
    
    sdf_final = np.clip(sdf_final, 0.0, 1.0)
    
    # Create RGB (all same - grayscale SDF)
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
    print(f"✅ SDF generated: {output_path}")
    print(f"   Input size: {width}×{height}")
    print(f"   Distance range: {distance_range} pixels (extended)")
    print(f"   Value range: {sdf_uint8[:,:,0].min()}-{sdf_uint8[:,:,0].max()}")
    print(f"   Dynamic range for thickness control: {sdf_uint8[:,:,0].max() - sdf_uint8[:,:,0].min()}")
    
    return sdf_image

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python png_to_sdf_v3.py <input.png> <output.png> [distance_range]")
        print("Default distance_range: 8 (larger = more thickness control)")
        sys.exit(1)
    
    bitmap_to_sdf_extended(sys.argv[1], sys.argv[2], 
                           int(sys.argv[3]) if len(sys.argv) > 3 else 8)
