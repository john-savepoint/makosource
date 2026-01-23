#!/usr/bin/env python3
"""
Convert a PNG bitmap font character to a Signed Distance Field (SDF).

This script generates an MSDF-like texture from bitmap font images.
While not as sophisticated as true MSDF, it provides similar benefits.
"""

import numpy as np
from PIL import Image
import sys
from scipy.ndimage import distance_transform_edt

def bitmap_to_sdf(image_path, output_path, distance_range=4):
    """
    Convert a bitmap image to a signed distance field.

    Args:
        image_path: Path to input PNG image
        output_path: Path for output SDF image
        distance_range: Maximum distance in pixels (default: 4)
    """
    # Load image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size

    # Extract alpha channel as binary mask
    alpha = np.array(img)[:, :, 3].astype(float) / 255.0

    # Create binary mask (threshold at 0.5)
    mask = alpha > 0.5

    # Compute distance transforms
    # Distance to nearest solid pixel (inside)
    dist_inside = distance_transform_edt(mask)

    # Distance to nearest empty pixel (outside)
    dist_outside = distance_transform_edt(~mask)

    # Combine into signed distance field
    # Positive inside, negative outside
    sdf = dist_inside - dist_outside

    # Normalize to [0, 1] range with distance_range
    # 0.5 = edge, >0.5 = inside, <0.5 = outside
    sdf_normalized = 0.5 + (sdf / (2.0 * distance_range))
    sdf_normalized = np.clip(sdf_normalized, 0.0, 1.0)

    # For MSDF simulation, create 3-channel output
    # We'll use the same distance in all 3 channels
    # (True MSDF would compute different directions per channel)
    sdf_rgb = np.stack([sdf_normalized] * 3, axis=2)

    # Convert to 8-bit
    sdf_uint8 = (sdf_rgb * 255).astype(np.uint8)

    # Create output image
    sdf_image = Image.fromarray(sdf_uint8, mode='RGB')

    # Save
    sdf_image.save(output_path)

    print(f"✅ SDF generated: {output_path}")
    print(f"   Input size: {width}×{height}")
    print(f"   Distance range: {distance_range} pixels")
    print(f"   Output format: RGB (3-channel SDF)")

    return sdf_image

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python png_to_sdf.py <input.png> <output.png> [distance_range]")
        print("Example: python png_to_sdf.py test_char.png test_char_sdf.png 4")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    distance_range = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    bitmap_to_sdf(input_path, output_path, distance_range)
