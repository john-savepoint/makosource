// Palette generation: Convert RGBA tiles to indexed color with 256-color palettes

use std::collections::HashMap;
use crate::{Color555, Result, CoreError};
use crate::tile::{Tile, TileWithPosition};

/// FF7 palette: 256 colors in RGB555 format
#[derive(Debug, Clone)]
pub struct Palette {
    pub colors: Vec<Color555>,
}

impl Palette {
    /// Create an empty palette
    pub fn new() -> Self {
        Self {
            colors: Vec::with_capacity(256),
        }
    }

    /// Create palette with transparent black at index 0
    pub fn with_transparent() -> Self {
        let mut palette = Self::new();
        palette.colors.push(Color555::transparent());
        palette
    }

    /// Find nearest palette index for a given color
    pub fn find_nearest(&self, color: Color555) -> u8 {
        self.colors
            .iter()
            .enumerate()
            .min_by_key(|(_, pal_color)| color.distance_squared(pal_color))
            .map(|(idx, _)| idx as u8)
            .unwrap_or(0)
    }

    /// Pad palette to 256 colors with transparent black
    pub fn pad_to_256(&mut self) {
        while self.colors.len() < 256 {
            self.colors.push(Color555::transparent());
        }
    }
}

impl Default for Palette {
    fn default() -> Self {
        Self::new()
    }
}

/// Indexed tile: tile converted to palette indices
#[derive(Debug, Clone)]
pub struct IndexedTile {
    pub indices: Vec<u8>,  // Palette indices (1 byte per pixel)
    pub width: u16,
    pub height: u16,
    pub dest_x: i16,
    pub dest_y: i16,
}

/// Generate palettes and convert tiles to indexed format
pub fn generate_palettes(
    tiles: &[TileWithPosition],
    _max_palettes: usize,
) -> Result<(Vec<Palette>, Vec<IndexedTile>)> {
    // For MVP: single 256-color palette
    // Future: support multiple palettes for better color accuracy

    // Step 1: Collect all unique colors across all tiles
    let mut color_histogram: HashMap<Color555, usize> = HashMap::new();

    for tile_pos in tiles {
        for rgba in tile_pos.tile.pixels.chunks_exact(4) {
            // Skip fully transparent pixels
            if rgba[3] == 0 {
                continue;
            }

            let color = Color555::from_rgb8(rgba[0], rgba[1], rgba[2]);
            *color_histogram.entry(color).or_insert(0) += 1;
        }
    }

    // Step 2: Quantize to 256 colors (reserve index 0 for transparency)
    let palette_colors = if color_histogram.len() <= 255 {
        // If we have 255 or fewer unique colors, use them directly
        color_histogram.into_keys().collect()
    } else {
        // Use color quantization to reduce to 255 colors
        quantize_colors(&color_histogram, 255)?
    };

    // Step 3: Build palette (index 0 = transparent)
    let mut palette = Palette::with_transparent();
    palette.colors.extend(palette_colors);
    palette.pad_to_256();

    // Step 4: Convert tiles to indexed format
    let indexed_tiles = tiles
        .iter()
        .map(|tile_pos| rgba_to_indexed(&tile_pos.tile, &palette, tile_pos.dest_x, tile_pos.dest_y))
        .collect();

    Ok((vec![palette], indexed_tiles))
}

/// Quantize colors using median cut or NeuQuant algorithm
fn quantize_colors(
    histogram: &HashMap<Color555, usize>,
    num_colors: usize,
) -> Result<Vec<Color555>> {
    // Convert histogram to weighted color list
    let mut colors: Vec<_> = histogram
        .iter()
        .map(|(color, &count)| (*color, count))
        .collect();

    // Sort by frequency (most common first)
    colors.sort_by(|a, b| b.1.cmp(&a.1));

    // Simple approach for MVP: take the N most common colors
    // Future enhancement: use proper median cut or NeuQuant
    let quantized: Vec<Color555> = colors
        .into_iter()
        .take(num_colors)
        .map(|(color, _)| color)
        .collect();

    if quantized.is_empty() {
        return Err(CoreError::PaletteError("No colors to quantize".to_string()));
    }

    Ok(quantized)
}

/// Convert RGBA tile to indexed format using palette
fn rgba_to_indexed(tile: &Tile, palette: &Palette, dest_x: i16, dest_y: i16) -> IndexedTile {
    let indices: Vec<u8> = tile
        .pixels
        .chunks_exact(4)
        .map(|rgba| {
            if rgba[3] == 0 {
                // Fully transparent = index 0
                0
            } else {
                let color = Color555::from_rgb8(rgba[0], rgba[1], rgba[2]);
                palette.find_nearest(color)
            }
        })
        .collect();

    IndexedTile {
        indices,
        width: tile.width,
        height: tile.height,
        dest_x,
        dest_y,
    }
}

/// Convert indexed tile back to RGBA (for verification/export)
pub fn indexed_to_rgba(indexed: &IndexedTile, palette: &Palette) -> Vec<u8> {
    let mut rgba = Vec::with_capacity(indexed.indices.len() * 4);
    let transparent = Color555::transparent();

    for &idx in &indexed.indices {
        let color = palette.colors.get(idx as usize)
            .unwrap_or(&transparent);

        if color.mask == 0 {
            // Transparent
            rgba.extend_from_slice(&[0, 0, 0, 0]);
        } else {
            let rgb = color.to_rgb8();
            rgba.extend_from_slice(&[rgb[0], rgb[1], rgb[2], 255]);
        }
    }

    rgba
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_palette_creation() {
        let palette = Palette::with_transparent();
        assert_eq!(palette.colors.len(), 1);
        assert_eq!(palette.colors[0].mask, 0);
    }

    #[test]
    fn test_palette_padding() {
        let mut palette = Palette::with_transparent();
        palette.colors.push(Color555::from_rgb8(255, 0, 0));
        palette.pad_to_256();
        assert_eq!(palette.colors.len(), 256);
    }

    #[test]
    fn test_find_nearest_color() {
        let mut palette = Palette::with_transparent();
        palette.colors.push(Color555::from_rgb8(255, 0, 0)); // Red
        palette.colors.push(Color555::from_rgb8(0, 255, 0)); // Green
        palette.colors.push(Color555::from_rgb8(0, 0, 255)); // Blue

        let red = Color555::from_rgb8(255, 0, 0);
        let near_red = Color555::from_rgb8(250, 10, 10);

        assert_eq!(palette.find_nearest(red), 1);
        assert_eq!(palette.find_nearest(near_red), 1);
    }

    #[test]
    fn test_rgba_to_indexed() {
        let mut tile = Tile::new(2, 2);
        // Set 4 pixels: transparent, red, green, blue
        tile.pixels = vec![
            0, 0, 0, 0,       // Transparent
            255, 0, 0, 255,   // Red
            0, 255, 0, 255,   // Green
            0, 0, 255, 255,   // Blue
        ];

        let mut palette = Palette::with_transparent();
        palette.colors.push(Color555::from_rgb8(255, 0, 0));
        palette.colors.push(Color555::from_rgb8(0, 255, 0));
        palette.colors.push(Color555::from_rgb8(0, 0, 255));

        let indexed = rgba_to_indexed(&tile, &palette, 0, 0);
        assert_eq!(indexed.indices.len(), 4);
        assert_eq!(indexed.indices[0], 0);  // Transparent
        assert_eq!(indexed.indices[1], 1);  // Red
        assert_eq!(indexed.indices[2], 2);  // Green
        assert_eq!(indexed.indices[3], 3);  // Blue
    }

    #[test]
    fn test_indexed_to_rgba_roundtrip() {
        let mut palette = Palette::with_transparent();
        palette.colors.push(Color555::from_rgb8(255, 0, 0));

        let indexed = IndexedTile {
            indices: vec![0, 1, 0, 1],
            width: 2,
            height: 2,
            dest_x: 0,
            dest_y: 0,
        };

        let rgba = indexed_to_rgba(&indexed, &palette);
        assert_eq!(rgba.len(), 16);  // 4 pixels * 4 bytes
        assert_eq!(rgba[0..4], [0, 0, 0, 0]);  // Transparent
        assert_eq!(rgba[7], 255);  // Opaque alpha for red pixel
    }
}
