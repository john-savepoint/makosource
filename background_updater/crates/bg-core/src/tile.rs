// Tile decomposition: Break images into 16x16 or 32x32 tiles

use bg_formats::RgbaImage;
use crate::{Result, CoreError};

/// Tile size options
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TileSize {
    Size16x16,
    Size32x32,
}

impl TileSize {
    pub fn as_u16(&self) -> u16 {
        match self {
            TileSize::Size16x16 => 16,
            TileSize::Size32x32 => 32,
        }
    }

    pub fn from_u16(size: u16) -> Result<Self> {
        match size {
            16 => Ok(TileSize::Size16x16),
            32 => Ok(TileSize::Size32x32),
            _ => Err(CoreError::TileError(format!("Invalid tile size: {}. Must be 16 or 32.", size))),
        }
    }
}

/// A single tile with RGBA8 pixel data
#[derive(Debug, Clone)]
pub struct Tile {
    pub pixels: Vec<u8>,   // RGBA8 format (4 bytes per pixel)
    pub width: u16,
    pub height: u16,
}

impl Tile {
    /// Create a new empty tile
    pub fn new(width: u16, height: u16) -> Self {
        Self {
            pixels: vec![0u8; (width as usize * height as usize * 4)],
            width,
            height,
        }
    }

    /// Get pixel count
    pub fn pixel_count(&self) -> usize {
        (self.width as usize * self.height as usize)
    }

    /// Get pixel at (x, y) as RGBA tuple
    pub fn get_pixel(&self, x: u16, y: u16) -> Option<[u8; 4]> {
        if x >= self.width || y >= self.height {
            return None;
        }

        let offset = ((y as usize * self.width as usize + x as usize) * 4);
        Some([
            self.pixels[offset],
            self.pixels[offset + 1],
            self.pixels[offset + 2],
            self.pixels[offset + 3],
        ])
    }

    /// Check if tile is fully transparent
    pub fn is_transparent(&self) -> bool {
        self.pixels.chunks_exact(4).all(|rgba| rgba[3] == 0)
    }
}

/// Tile with destination coordinates
#[derive(Debug, Clone)]
pub struct TileWithPosition {
    pub tile: Tile,
    pub dest_x: i16,
    pub dest_y: i16,
}

/// Decompose an RGBA image into tiles
pub fn decompose_to_tiles(
    image: &RgbaImage,
    tile_size: TileSize,
) -> Result<Vec<TileWithPosition>> {
    let tile_dim = tile_size.as_u16();
    let tiles_x = (image.width + tile_dim as u32 - 1) / tile_dim as u32;
    let tiles_y = (image.height + tile_dim as u32 - 1) / tile_dim as u32;

    let mut tiles = Vec::new();

    for ty in 0..tiles_y {
        for tx in 0..tiles_x {
            let tile_data = extract_tile_rgba(
                &image.pixels,
                image.width,
                image.height,
                tx * tile_dim as u32,
                ty * tile_dim as u32,
                tile_dim,
            );

            let dest_x = (tx * tile_dim as u32) as i16;
            let dest_y = (ty * tile_dim as u32) as i16;

            tiles.push(TileWithPosition {
                tile: tile_data,
                dest_x,
                dest_y,
            });
        }
    }

    Ok(tiles)
}

/// Extract a single tile from RGBA image data
fn extract_tile_rgba(
    pixels: &[u8],
    image_width: u32,
    image_height: u32,
    start_x: u32,
    start_y: u32,
    tile_size: u16,
) -> Tile {
    let mut tile_pixels = Vec::with_capacity((tile_size as usize * tile_size as usize * 4));

    for dy in 0..tile_size {
        for dx in 0..tile_size {
            let px = start_x + dx as u32;
            let py = start_y + dy as u32;

            if px < image_width && py < image_height {
                // Copy pixel from source image
                let offset = ((py * image_width + px) * 4) as usize;
                tile_pixels.push(pixels[offset]);     // R
                tile_pixels.push(pixels[offset + 1]); // G
                tile_pixels.push(pixels[offset + 2]); // B
                tile_pixels.push(pixels[offset + 3]); // A
            } else {
                // Fill with transparent black (padding for edges)
                tile_pixels.extend_from_slice(&[0, 0, 0, 0]);
            }
        }
    }

    Tile {
        pixels: tile_pixels,
        width: tile_size,
        height: tile_size,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tile_creation() {
        let tile = Tile::new(16, 16);
        assert_eq!(tile.width, 16);
        assert_eq!(tile.height, 16);
        assert_eq!(tile.pixels.len(), 16 * 16 * 4);
    }

    #[test]
    fn test_tile_size_conversion() {
        assert_eq!(TileSize::Size16x16.as_u16(), 16);
        assert_eq!(TileSize::Size32x32.as_u16(), 32);
        assert_eq!(TileSize::from_u16(16).unwrap(), TileSize::Size16x16);
    }

    #[test]
    fn test_decompose_exact_size() {
        // Create a 32x32 test image
        let image = RgbaImage {
            width: 32,
            height: 32,
            pixels: vec![0u8; 32 * 32 * 4],
        };

        let tiles = decompose_to_tiles(&image, TileSize::Size16x16).unwrap();

        // Should create 2x2 grid = 4 tiles
        assert_eq!(tiles.len(), 4);

        // Check positions
        assert_eq!(tiles[0].dest_x, 0);
        assert_eq!(tiles[0].dest_y, 0);
        assert_eq!(tiles[1].dest_x, 16);
        assert_eq!(tiles[1].dest_y, 0);
        assert_eq!(tiles[2].dest_x, 0);
        assert_eq!(tiles[2].dest_y, 16);
        assert_eq!(tiles[3].dest_x, 16);
        assert_eq!(tiles[3].dest_y, 16);
    }

    #[test]
    fn test_decompose_partial_tile() {
        // Create a 20x20 test image (not evenly divisible by 16)
        let image = RgbaImage {
            width: 20,
            height: 20,
            pixels: vec![255u8; 20 * 20 * 4],
        };

        let tiles = decompose_to_tiles(&image, TileSize::Size16x16).unwrap();

        // Should create 2x2 grid = 4 tiles (with padding)
        assert_eq!(tiles.len(), 4);

        // Edge tiles should have some transparent padding
        let bottom_right_tile = &tiles[3];
        assert_eq!(bottom_right_tile.tile.width, 16);
        assert_eq!(bottom_right_tile.tile.height, 16);
    }

    #[test]
    fn test_transparent_check() {
        let mut tile = Tile::new(4, 4);
        assert!(tile.is_transparent());

        // Set one pixel to opaque
        tile.pixels[3] = 255;  // Alpha channel of first pixel
        assert!(!tile.is_transparent());
    }
}
