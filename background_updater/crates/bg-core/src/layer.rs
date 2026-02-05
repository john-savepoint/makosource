// FF7 Background Layer Sprites (52-byte structure)

/// FF7 BackgroundSprite structure (52 bytes)
/// Packed C structure representing a single tile/sprite in a background layer
#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct BackgroundSprite {
    pub zz1: i16,              // +0x00: Unknown (leave as 0)
    pub x: i16,                // +0x02: Destination X coordinate
    pub y: i16,                // +0x04: Destination Y coordinate
    pub zz2: [i16; 2],         // +0x06: Unknown (leave as 0)
    pub src_x: i16,            // +0x0A: Source X (0-255 within texture page)
    pub src_y: i16,            // +0x0C: Source Y (0-255 within texture page)
    pub zz3: [i16; 4],         // +0x0E: Unknown (leave as 0)
    pub pal: i16,              // +0x16: Palette index (which 256-color palette)
    pub flags: u16,            // +0x18: Blending/effects flags
    pub zz4: [i16; 3],         // +0x1A: Unknown (leave as 0)
    pub page: i16,             // +0x20: Texture page number (0-41)
    pub sfx: i16,              // +0x22: Special effects (0 = normal render)
    pub na: u32,               // +0x24: Unknown (leave as 0)
    pub zz5: i16,              // +0x28: Unknown (leave as 0)
    pub off_x: i32,            // +0x2A: Offset X (leave as 0)
    pub off_y: i32,            // +0x2E: Offset Y (leave as 0)
    pub zz6: i16,              // +0x32: Unknown (leave as 0)
}

impl BackgroundSprite {
    /// Create a new sprite with sensible defaults
    pub fn new(
        dest_x: i16,
        dest_y: i16,
        src_x: i16,
        src_y: i16,
        page: i16,
        palette: i16,
    ) -> Self {
        Self {
            zz1: 0,
            x: dest_x,
            y: dest_y,
            zz2: [0; 2],
            src_x,
            src_y,
            zz3: [0; 4],
            pal: palette,
            flags: 0,  // Normal blending
            zz4: [0; 3],
            page,
            sfx: 0,  // Normal rendering
            na: 0,
            zz5: 0,
            off_x: 0,
            off_y: 0,
            zz6: 0,
        }
    }

    /// Serialize to bytes
    pub fn to_bytes(&self) -> [u8; 52] {
        unsafe {
            // Cast the struct to a byte array
            std::ptr::read(self as *const Self as *const [u8; 52])
        }
    }

    /// Deserialize from bytes
    pub fn from_bytes(bytes: &[u8; 52]) -> Self {
        unsafe {
            std::ptr::read(bytes.as_ptr() as *const Self)
        }
    }
}

// Verify size at compile time
const _: () = assert!(std::mem::size_of::<BackgroundSprite>() == 52);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sprite_size() {
        assert_eq!(std::mem::size_of::<BackgroundSprite>(), 52);
    }

    #[test]
    fn test_sprite_creation() {
        let sprite = BackgroundSprite::new(100, 200, 32, 64, 5, 0);

        assert_eq!(sprite.x, 100);
        assert_eq!(sprite.y, 200);
        assert_eq!(sprite.src_x, 32);
        assert_eq!(sprite.src_y, 64);
        assert_eq!(sprite.page, 5);
        assert_eq!(sprite.pal, 0);
    }

    #[test]
    fn test_sprite_serialization() {
        let sprite = BackgroundSprite::new(100, 200, 32, 64, 5, 0);
        let bytes = sprite.to_bytes();

        assert_eq!(bytes.len(), 52);

        // Deserialize and verify
        let restored = BackgroundSprite::from_bytes(&bytes);
        assert_eq!(restored.x, sprite.x);
        assert_eq!(restored.y, sprite.y);
        assert_eq!(restored.page, sprite.page);
    }

    #[test]
    fn test_sprite_defaults() {
        let sprite = BackgroundSprite::new(0, 0, 0, 0, 0, 0);

        // Verify unknown fields are zeroed
        assert_eq!(sprite.zz1, 0);
        assert_eq!(sprite.zz2, [0; 2]);
        assert_eq!(sprite.zz3, [0; 4]);
        assert_eq!(sprite.zz4, [0; 3]);
        assert_eq!(sprite.na, 0);
        assert_eq!(sprite.zz5, 0);
        assert_eq!(sprite.zz6, 0);

        // Verify default flags
        assert_eq!(sprite.flags, 0);
        assert_eq!(sprite.sfx, 0);
        assert_eq!(sprite.off_x, 0);
        assert_eq!(sprite.off_y, 0);
    }
}
