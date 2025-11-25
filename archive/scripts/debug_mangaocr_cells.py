#!/usr/bin/env python3
"""
Debug manga-ocr by showing exactly what cells are being extracted.
Created: 2025-11-17 23:08:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

This will extract specific problematic cells and save them so you can
see exactly what manga-ocr is receiving as input.
"""

from PIL import Image, ImageOps, ImageDraw, ImageFont
from pathlib import Path

FONT_DIR = Path("extracted_fonts/png")
OUTPUT_DIR = Path("character_tables/debug_cells")
CELL_SIZE = 64


def extract_and_save_cell(texture_name, index):
    """Extract a single cell and save it with metadata."""

    img_path = FONT_DIR / f"{texture_name}.png"
    img = Image.open(img_path)

    grid_x = index % 16
    grid_y = index // 16

    # Extract cell
    pixel_x = grid_x * CELL_SIZE
    pixel_y = grid_y * CELL_SIZE
    cell = img.crop((pixel_x, pixel_y, pixel_x + CELL_SIZE, pixel_y + CELL_SIZE))

    # Also create inverted version (what manga-ocr sees)
    gray = cell.convert('L')
    inverted = ImageOps.invert(gray)

    return cell, inverted, grid_x, grid_y


def create_debug_panel(samples):
    """Create a panel showing multiple samples for comparison."""

    # Calculate panel size
    samples_per_row = 4
    num_rows = (len(samples) + samples_per_row - 1) // samples_per_row

    # Each sample: 64px cell + 64px inverted + labels = ~150px wide, ~100px tall
    sample_width = 180
    sample_height = 120
    panel_width = samples_per_row * sample_width
    panel_height = num_rows * sample_height

    panel = Image.new('RGB', (panel_width, panel_height), color=(30, 30, 30))
    draw = ImageDraw.Draw(panel)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except:
        font = ImageFont.load_default()

    for i, sample in enumerate(samples):
        row = i // samples_per_row
        col = i % samples_per_row

        x_offset = col * sample_width + 10
        y_offset = row * sample_height + 10

        # Paste original cell
        panel.paste(sample['original'], (x_offset, y_offset + 20))

        # Paste inverted cell (what OCR sees)
        panel.paste(sample['inverted'].convert('RGB'), (x_offset + 70, y_offset + 20))

        # Add labels
        label = f"{sample['texture']} idx:{sample['index']}"
        draw.text((x_offset, y_offset), label, font=font, fill=(200, 200, 200))

        info = f"({sample['grid_x']},{sample['grid_y']})"
        draw.text((x_offset, y_offset + 88), info, font=font, fill=(150, 150, 150))

    return panel


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Sample some problematic cells from our comparison
    # Focus on jafont_3 which had massive errors
    problem_samples = [
        # jafont_1 - small kana issues
        ("jafont_1", 6, "ベ vs べ"),
        ("jafont_1", 158, "ャ vs ヤ"),
        ("jafont_1", 164, "ァ vs ア"),
        ("jafont_1", 116, "ニ vs 二"),

        # jafont_2 - kanji issues
        ("jafont_2", 4, "獄 vs 状"),
        ("jafont_2", 7, "戦 vs 裁"),
        ("jafont_2", 31, "自 vs 白"),

        # jafont_3 - massive off-by-one?
        ("jafont_3", 0, "安"),
        ("jafont_3", 1, "香"),
        ("jafont_3", 5, "蟹 vs 蜂"),
        ("jafont_3", 6, "蝕 vs 蜜"),
        ("jafont_3", 16, "品 vs 商"),
        ("jafont_3", 17, "最 vs 品"),

        # jafont_4 edge cases
        ("jafont_4", 224, "a"),
        ("jafont_4", 225, "b"),
        ("jafont_4", 226, "c"),
    ]

    samples = []
    for texture, index, note in problem_samples:
        original, inverted, gx, gy = extract_and_save_cell(texture, index)

        # Save individual cell
        filename = f"{texture}_idx{index:03d}_gxy{gx}_{gy}.png"
        original.save(OUTPUT_DIR / f"orig_{filename}")
        inverted.save(OUTPUT_DIR / f"inv_{filename}")

        samples.append({
            'texture': texture,
            'index': index,
            'grid_x': gx,
            'grid_y': gy,
            'note': note,
            'original': original,
            'inverted': inverted
        })

        print(f"Saved: {texture} index {index} at ({gx}, {gy}) - {note}")

    # Create comparison panel
    panel = create_debug_panel(samples)
    panel.save(OUTPUT_DIR / "problem_cells_panel.png")
    print(f"\nSaved panel: {OUTPUT_DIR / 'problem_cells_panel.png'}")

    # Also extract first 4x4 grid from jafont_3 to see alignment
    print("\nExtracting jafont_3 first 16 cells (row 0) for alignment check...")
    row_samples = []
    for idx in range(16):
        original, inverted, gx, gy = extract_and_save_cell("jafont_3", idx)
        row_samples.append({
            'texture': 'jafont_3',
            'index': idx,
            'grid_x': gx,
            'grid_y': gy,
            'note': '',
            'original': original,
            'inverted': inverted
        })

    row_panel = create_debug_panel(row_samples)
    row_panel.save(OUTPUT_DIR / "jafont3_row0_cells.png")
    print(f"Saved: {OUTPUT_DIR / 'jafont3_row0_cells.png'}")


if __name__ == "__main__":
    main()
