// FF7 Field file assembly: Create Section 4 (palette) and Section 9 (background)

use crate::{Result, CoreError};
use crate::palette::Palette;
use crate::packer::{TexturePage, TileMapping};
use crate::layer::BackgroundSprite;

/// Create Section 4 data (palette section)
pub fn create_section4_palette(palettes: &[Palette]) -> Result<Vec<u8>> {
    if palettes.is_empty() {
        return Err(CoreError::FieldError("No palettes provided".to_string()));
    }

    let mut data = Vec::new();

    // Total number of colors across all palettes
    let num_colors = 256 * palettes.len();

    // Section 4 header (12 bytes)
    data.extend_from_slice(&(num_colors as u32).to_le_bytes());  // +0x00: Total colors
    data.extend_from_slice(&0u16.to_le_bytes());                 // +0x04: Unknown
    data.push(0);                                                 // +0x06: Unknown byte
    data.extend_from_slice(&(num_colors as u32).to_le_bytes());  // +0x07: Total colors (repeat)
    data.push(0);                                                 // +0x0B: Unknown byte

    // Write palette data (15-bit RGB555 colors, 2 bytes each)
    for palette in palettes {
        for color in &palette.colors {
            data.extend_from_slice(&color.to_u16().to_le_bytes());
        }
    }

    Ok(data)
}

/// Create Section 9 data (background section)
pub fn create_section9_background(
    pages: &[TexturePage],
    mappings: &[TileMapping],
) -> Result<Vec<u8>> {
    let mut data = Vec::new();

    // Calculate background dimensions
    let max_x = mappings.iter()
        .map(|m| m.dest_x + m.width as i16)
        .max()
        .unwrap_or(640);
    let max_y = mappings.iter()
        .map(|m| m.dest_y + m.height as i16)
        .max()
        .unwrap_or(480);

    // Background header (46 bytes before sprite data)
    // First 40 bytes: unknown/reserved
    data.extend_from_slice(&[0u8; 40]);

    // Offset 0x28: Width (2 bytes)
    data.extend_from_slice(&(max_x as u16).to_le_bytes());

    // Offset 0x2A: Height (2 bytes)
    data.extend_from_slice(&(max_y as u16).to_le_bytes());

    // Offset 0x2C: Number of sprites in layer 1 (2 bytes)
    let num_sprites = mappings.len() as u16;
    data.extend_from_slice(&num_sprites.to_le_bytes());

    // Offset 0x2E: Unknown padding (4 bytes)
    data.extend_from_slice(&[0u8; 4]);

    // Layer 1 sprite data (52 bytes each)
    for mapping in mappings {
        let sprite = BackgroundSprite::new(
            mapping.dest_x,
            mapping.dest_y,
            mapping.src_x as i16,
            mapping.src_y as i16,
            mapping.page_index as i16,
            0,  // Palette index (always 0 for single palette)
        );

        data.extend_from_slice(&sprite.to_bytes());
    }

    // Layer 2 header (no sprites for MVP)
    data.extend_from_slice(&[0u8; 7]);   // Unknown
    data.extend_from_slice(&0u16.to_le_bytes());  // 0 sprites
    data.extend_from_slice(&[0u8; 18]);  // Unknown padding

    // Texture page data
    for page in pages {
        // Each page has a 6-byte header
        data.extend_from_slice(&[0u8; 6]);

        // Followed by 256x256 indexed pixel data
        data.extend_from_slice(&page.data);
    }

    // End marker
    data.extend_from_slice(b"END");

    Ok(data)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::Color555;

    #[test]
    fn test_section4_creation() {
        let mut palette = Palette::new();
        palette.colors.push(Color555::transparent());
        palette.colors.push(Color555::from_rgb8(255, 0, 0));
        palette.pad_to_256();

        let section4 = create_section4_palette(&[palette]).unwrap();

        // Header is 12 bytes
        assert!(section4.len() >= 12);

        // Total size should be 12 + (256 * 2) = 524 bytes
        assert_eq!(section4.len(), 12 + 256 * 2);

        // Verify header
        let num_colors = u32::from_le_bytes([section4[0], section4[1], section4[2], section4[3]]);
        assert_eq!(num_colors, 256);
    }

    #[test]
    fn test_section9_creation() {
        let mut page = TexturePage::new(0);
        // Fill with test pattern
        for i in 0..256 * 256 {
            page.data[i] = (i % 256) as u8;
        }

        let mappings = vec![
            TileMapping {
                tile_index: 0,
                page_index: 0,
                src_x: 0,
                src_y: 0,
                dest_x: 0,
                dest_y: 0,
                width: 16,
                height: 16,
            },
            TileMapping {
                tile_index: 1,
                page_index: 0,
                src_x: 16,
                src_y: 0,
                dest_x: 16,
                dest_y: 0,
                width: 16,
                height: 16,
            },
        ];

        let section9 = create_section9_background(&[page], &mappings).unwrap();

        // Header is 46 bytes
        assert!(section9.len() >= 46);

        // Verify sprite count at offset 0x2C
        let sprite_count = u16::from_le_bytes([section9[44], section9[45]]);
        assert_eq!(sprite_count, 2);

        // Verify width/height at offset 0x28
        let width = u16::from_le_bytes([section9[40], section9[41]]);
        let height = u16::from_le_bytes([section9[42], section9[43]]);
        assert_eq!(width, 32);  // 16 + 16
        assert_eq!(height, 16);

        // Verify END marker is present
        let end_pos = section9.len() - 3;
        assert_eq!(&section9[end_pos..], b"END");
    }

    #[test]
    fn test_section4_multiple_palettes() {
        let palette1 = Palette::with_transparent();
        let mut palette2 = Palette::with_transparent();
        palette2.colors[1] = Color555::from_rgb8(255, 0, 0);

        let section4 = create_section4_palette(&[palette1, palette2]).unwrap();

        // Total colors = 256 * 2 = 512
        // Size = 12 + (512 * 2) = 1036 bytes
        assert_eq!(section4.len(), 12 + 512 * 2);

        let num_colors = u32::from_le_bytes([section4[0], section4[1], section4[2], section4[3]]);
        assert_eq!(num_colors, 512);
    }

    #[test]
    fn test_empty_palettes_error() {
        let result = create_section4_palette(&[]);
        assert!(result.is_err());
    }

    #[test]
    fn test_section9_with_multiple_pages() {
        let page1 = TexturePage::new(0);
        let page2 = TexturePage::new(1);

        let mappings = vec![
            TileMapping {
                tile_index: 0,
                page_index: 0,
                src_x: 0,
                src_y: 0,
                dest_x: 0,
                dest_y: 0,
                width: 16,
                height: 16,
            },
            TileMapping {
                tile_index: 1,
                page_index: 1,
                src_x: 0,
                src_y: 0,
                dest_x: 16,
                dest_y: 0,
                width: 16,
                height: 16,
            },
        ];

        let section9 = create_section9_background(&[page1, page2], &mappings).unwrap();

        // Should contain 2 pages worth of data
        // Header + sprites + layer2 header + (6 + 256*256) * 2 + END
        let expected_page_data = (6 + 256 * 256) * 2;
        assert!(section9.len() >= expected_page_data);
    }
}
