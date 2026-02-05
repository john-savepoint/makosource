// Color format conversions (RGB888 <-> RGB555)

/// 15-bit RGB555 color format (FF7 native format)
/// 5 bits per channel + 1 bit mask (transparency flag)
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Color555 {
    pub r: u8,  // 5 bits (0-31)
    pub g: u8,  // 5 bits (0-31)
    pub b: u8,  // 5 bits (0-31)
    pub mask: u8,  // 1 bit (0 = transparent, 1 = opaque)
}

impl Color555 {
    /// Create transparent black
    pub fn transparent() -> Self {
        Self { r: 0, g: 0, b: 0, mask: 0 }
    }

    /// Create from 8-bit RGB values
    pub fn from_rgb8(r: u8, g: u8, b: u8) -> Self {
        Self {
            r: (r >> 3) & 0x1F,  // Convert 8-bit to 5-bit
            g: (g >> 3) & 0x1F,
            b: (b >> 3) & 0x1F,
            mask: 1,  // Opaque by default
        }
    }

    /// Create from RGB888
    pub fn from_color888(color: Color888) -> Self {
        Self::from_rgb8(color.r, color.g, color.b)
    }

    /// Convert to 16-bit value (FF7 format: ABBBBBGGGGGRRRRR)
    pub fn to_u16(&self) -> u16 {
        (self.r as u16)
            | ((self.g as u16) << 5)
            | ((self.b as u16) << 10)
            | ((self.mask as u16) << 15)
    }

    /// Create from 16-bit value
    pub fn from_u16(value: u16) -> Self {
        Self {
            r: (value & 0x1F) as u8,
            g: ((value >> 5) & 0x1F) as u8,
            b: ((value >> 10) & 0x1F) as u8,
            mask: ((value >> 15) & 0x1) as u8,
        }
    }

    /// Convert back to 8-bit RGB
    pub fn to_rgb8(&self) -> [u8; 3] {
        [
            (self.r << 3) | (self.r >> 2),  // Expand 5-bit to 8-bit
            (self.g << 3) | (self.g >> 2),
            (self.b << 3) | (self.b >> 2),
        ]
    }

    /// Calculate color distance squared (for nearest neighbor search)
    pub fn distance_squared(&self, other: &Self) -> u32 {
        let dr = (self.r as i32 - other.r as i32).abs();
        let dg = (self.g as i32 - other.g as i32).abs();
        let db = (self.b as i32 - other.b as i32).abs();
        (dr * dr + dg * dg + db * db) as u32
    }
}

/// 24-bit RGB888 color (standard 8-bit per channel)
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Color888 {
    pub r: u8,
    pub g: u8,
    pub b: u8,
}

impl Color888 {
    pub fn new(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b }
    }

    pub fn from_slice(rgb: &[u8]) -> Self {
        Self {
            r: rgb[0],
            g: rgb[1],
            b: rgb[2],
        }
    }

    /// Convert to Color555
    pub fn to_color555(&self) -> Color555 {
        Color555::from_rgb8(self.r, self.g, self.b)
    }
}

impl From<[u8; 3]> for Color888 {
    fn from(rgb: [u8; 3]) -> Self {
        Self::new(rgb[0], rgb[1], rgb[2])
    }
}

impl From<Color888> for [u8; 3] {
    fn from(color: Color888) -> Self {
        [color.r, color.g, color.b]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_color555_conversion() {
        let color = Color555::from_rgb8(255, 128, 64);
        assert_eq!(color.r, 31);  // 255 >> 3 = 31
        assert_eq!(color.g, 16);  // 128 >> 3 = 16
        assert_eq!(color.b, 8);   // 64 >> 3 = 8
        assert_eq!(color.mask, 1);
    }

    #[test]
    fn test_color555_roundtrip() {
        let original = Color555 { r: 31, g: 16, b: 8, mask: 1 };
        let u16_val = original.to_u16();
        let restored = Color555::from_u16(u16_val);
        assert_eq!(original, restored);
    }

    #[test]
    fn test_transparent_color() {
        let transparent = Color555::transparent();
        assert_eq!(transparent.mask, 0);
        assert_eq!(transparent.to_u16(), 0);
    }

    #[test]
    fn test_color_distance() {
        let c1 = Color555::from_rgb8(255, 0, 0);
        let c2 = Color555::from_rgb8(0, 255, 0);
        let c3 = Color555::from_rgb8(255, 0, 0);

        assert!(c1.distance_squared(&c2) > 0);
        assert_eq!(c1.distance_squared(&c3), 0);
    }
}
