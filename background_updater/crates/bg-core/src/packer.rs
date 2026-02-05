// Texture page packing: Pack indexed tiles into 256x256 texture pages

use crate::{Result, CoreError};
use crate::palette::IndexedTile;

/// A single 256x256 texture page
#[derive(Debug, Clone)]
pub struct TexturePage {
    pub data: Vec<u8>,  // 256x256 indexed pixel data
    pub page_index: u16,
}

impl TexturePage {
    /// Create a new empty texture page
    pub fn new(page_index: u16) -> Self {
        Self {
            data: vec![0u8; 256 * 256],
            page_index,
        }
    }

    /// Write a tile to the texture page at (x, y)
    pub fn write_tile(&mut self, tile: &IndexedTile, x: u16, y: u16) -> Result<()> {
        if x + tile.width > 256 || y + tile.height > 256 {
            return Err(CoreError::PackerError(format!(
                "Tile at ({}, {}) with size {}x{} exceeds page bounds",
                x, y, tile.width, tile.height
            )));
        }

        for dy in 0..tile.height {
            for dx in 0..tile.width {
                let src_idx = (dy * tile.width + dx) as usize;
                let dst_idx = ((y + dy) * 256 + (x + dx)) as usize;
                self.data[dst_idx] = tile.indices[src_idx];
            }
        }

        Ok(())
    }
}

/// Mapping of a tile to its location in a texture page
#[derive(Debug, Clone)]
pub struct TileMapping {
    pub tile_index: usize,    // Index in original tile list
    pub page_index: u16,      // Which texture page
    pub src_x: u16,           // X position within page (0-255)
    pub src_y: u16,           // Y position within page (0-255)
    pub dest_x: i16,          // Destination X in background
    pub dest_y: i16,          // Destination Y in background
    pub width: u16,           // Tile width
    pub height: u16,          // Tile height
}

/// Pack indexed tiles into 256x256 texture pages
pub fn pack_tiles_to_pages(
    tiles: &[IndexedTile],
) -> Result<(Vec<TexturePage>, Vec<TileMapping>)> {
    if tiles.is_empty() {
        return Ok((Vec::new(), Vec::new()));
    }

    // Determine tile size (assume all tiles are same size)
    let tile_size = tiles[0].width;

    // Validate all tiles are same size
    for tile in tiles {
        if tile.width != tile_size || tile.height != tile_size {
            return Err(CoreError::PackerError(format!(
                "All tiles must be same size. Expected {}x{}, got {}x{}",
                tile_size, tile_size, tile.width, tile.height
            )));
        }
    }

    // Calculate how many tiles fit per page
    let tiles_per_row = 256 / tile_size;
    let tiles_per_page = tiles_per_row * tiles_per_row;

    // Calculate number of pages needed
    let num_pages = (tiles.len() + tiles_per_page as usize - 1) / tiles_per_page as usize;

    let mut pages = Vec::with_capacity(num_pages);
    let mut mappings = Vec::with_capacity(tiles.len());

    for page_idx in 0..num_pages {
        let mut page = TexturePage::new(page_idx as u16);

        // Pack tiles into this page
        let start_tile = page_idx * tiles_per_page as usize;
        let end_tile = ((page_idx + 1) * tiles_per_page as usize).min(tiles.len());

        for (tile_offset, tile_idx) in (start_tile..end_tile).enumerate() {
            let tile = &tiles[tile_idx];

            // Calculate position within page
            let tile_x = (tile_offset % tiles_per_row as usize) as u16;
            let tile_y = (tile_offset / tiles_per_row as usize) as u16;

            let src_x = tile_x * tile_size;
            let src_y = tile_y * tile_size;

            // Write tile to page
            page.write_tile(tile, src_x, src_y)?;

            // Record mapping
            mappings.push(TileMapping {
                tile_index: tile_idx,
                page_index: page_idx as u16,
                src_x,
                src_y,
                dest_x: tile.dest_x,
                dest_y: tile.dest_y,
                width: tile.width,
                height: tile.height,
            });
        }

        pages.push(page);
    }

    Ok((pages, mappings))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_test_tile(size: u16, dest_x: i16, dest_y: i16) -> IndexedTile {
        IndexedTile {
            indices: vec![0u8; (size * size) as usize],
            width: size,
            height: size,
            dest_x,
            dest_y,
        }
    }

    #[test]
    fn test_texture_page_creation() {
        let page = TexturePage::new(0);
        assert_eq!(page.data.len(), 256 * 256);
        assert_eq!(page.page_index, 0);
    }

    #[test]
    fn test_write_tile_to_page() {
        let mut page = TexturePage::new(0);
        let tile = IndexedTile {
            indices: vec![42u8; 16 * 16],
            width: 16,
            height: 16,
            dest_x: 0,
            dest_y: 0,
        };

        page.write_tile(&tile, 0, 0).unwrap();

        // Verify tile was written
        for y in 0..16 {
            for x in 0..16 {
                let idx = (y * 256 + x) as usize;
                assert_eq!(page.data[idx], 42);
            }
        }
    }

    #[test]
    fn test_pack_16x16_tiles() {
        // Create 16 tiles (16x16 each) = exactly 1 page worth (16x16 = 256 tiles)
        let tiles: Vec<IndexedTile> = (0..16)
            .map(|i| create_test_tile(16, i * 16, 0))
            .collect();

        let (pages, mappings) = pack_tiles_to_pages(&tiles).unwrap();

        assert_eq!(pages.len(), 1);
        assert_eq!(mappings.len(), 16);

        // Check first mapping
        assert_eq!(mappings[0].page_index, 0);
        assert_eq!(mappings[0].src_x, 0);
        assert_eq!(mappings[0].src_y, 0);

        // Check second mapping (next tile in same row)
        assert_eq!(mappings[1].src_x, 16);
        assert_eq!(mappings[1].src_y, 0);
    }

    #[test]
    fn test_pack_multiple_pages() {
        // Create 300 tiles (16x16) = needs 2 pages (256 + 44)
        let tiles: Vec<IndexedTile> = (0..300)
            .map(|i| create_test_tile(16, (i % 40) * 16, (i / 40) * 16))
            .collect();

        let (pages, mappings) = pack_tiles_to_pages(&tiles).unwrap();

        assert_eq!(pages.len(), 2);
        assert_eq!(mappings.len(), 300);

        // First 256 tiles should be on page 0
        assert_eq!(mappings[255].page_index, 0);

        // Remaining tiles on page 1
        assert_eq!(mappings[256].page_index, 1);
        assert_eq!(mappings[256].src_x, 0);  // Reset to top-left of new page
        assert_eq!(mappings[256].src_y, 0);
    }

    #[test]
    fn test_pack_32x32_tiles() {
        // 32x32 tiles: 8x8 = 64 tiles per page
        let tiles: Vec<IndexedTile> = (0..100)
            .map(|i| create_test_tile(32, (i % 10) * 32, (i / 10) * 32))
            .collect();

        let (pages, mappings) = pack_tiles_to_pages(&tiles).unwrap();

        // 100 tiles / 64 per page = 2 pages
        assert_eq!(pages.len(), 2);
        assert_eq!(mappings.len(), 100);

        // Check tile spacing (should be 32 pixels apart)
        assert_eq!(mappings[1].src_x, 32);
        assert_eq!(mappings[8].src_x, 0);  // Wrap to next row
        assert_eq!(mappings[8].src_y, 32);
    }

    #[test]
    fn test_mixed_tile_sizes_error() {
        let tiles = vec![
            create_test_tile(16, 0, 0),
            create_test_tile(32, 0, 0),  // Different size!
        ];

        let result = pack_tiles_to_pages(&tiles);
        assert!(result.is_err());
    }

    #[test]
    fn test_empty_tiles() {
        let tiles: Vec<IndexedTile> = Vec::new();
        let (pages, mappings) = pack_tiles_to_pages(&tiles).unwrap();
        assert!(pages.is_empty());
        assert!(mappings.is_empty());
    }
}
