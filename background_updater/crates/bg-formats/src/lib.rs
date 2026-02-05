// FF7 Background Updater - Image Format Support
// Created: 2026-02-05 23:00 JST
// Session: 3c2ad7f8-61f8-44ca-b10e-5f64ada8863f
//
// Handles loading PNG and DDS images into a common RGBA8 format.

use std::path::Path;
use thiserror::Error;

pub mod png;
pub mod dds;

#[derive(Error, Debug)]
pub enum FormatError {
    #[error("Unsupported image format: {0}")]
    UnsupportedFormat(String),

    #[error("Failed to load image: {0}")]
    LoadError(String),

    #[error("Failed to decode DDS: {0}")]
    DdsError(String),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, FormatError>;

/// Detected image format
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ImageFormat {
    Png,
    Dds,
}

/// Common RGBA8 image representation
#[derive(Debug, Clone)]
pub struct RgbaImage {
    pub width: u32,
    pub height: u32,
    pub pixels: Vec<u8>,  // RGBA8 format (4 bytes per pixel)
}

impl RgbaImage {
    /// Create a new RGBA image with given dimensions
    pub fn new(width: u32, height: u32) -> Self {
        Self {
            width,
            height,
            pixels: vec![0u8; (width * height * 4) as usize],
        }
    }

    /// Get pixel count
    pub fn pixel_count(&self) -> usize {
        (self.width * self.height) as usize
    }

    /// Get pixel at (x, y) as RGBA tuple
    pub fn get_pixel(&self, x: u32, y: u32) -> Option<[u8; 4]> {
        if x >= self.width || y >= self.height {
            return None;
        }

        let offset = ((y * self.width + x) * 4) as usize;
        Some([
            self.pixels[offset],
            self.pixels[offset + 1],
            self.pixels[offset + 2],
            self.pixels[offset + 3],
        ])
    }

    /// Set pixel at (x, y)
    pub fn set_pixel(&mut self, x: u32, y: u32, rgba: [u8; 4]) {
        if x >= self.width || y >= self.height {
            return;
        }

        let offset = ((y * self.width + x) * 4) as usize;
        self.pixels[offset..offset + 4].copy_from_slice(&rgba);
    }
}

/// Detect image format from file extension
pub fn detect_format(path: &Path) -> Result<ImageFormat> {
    let ext = path
        .extension()
        .and_then(|e| e.to_str())
        .ok_or_else(|| FormatError::UnsupportedFormat("No file extension".to_string()))?;

    match ext.to_lowercase().as_str() {
        "png" => Ok(ImageFormat::Png),
        "dds" => Ok(ImageFormat::Dds),
        _ => Err(FormatError::UnsupportedFormat(ext.to_string())),
    }
}

/// Load an image from file (auto-detect format)
pub fn load_image(path: &Path) -> Result<RgbaImage> {
    let format = detect_format(path)?;

    match format {
        ImageFormat::Png => png::load(path),
        ImageFormat::Dds => dds::load(path),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rgba_image_creation() {
        let img = RgbaImage::new(16, 16);
        assert_eq!(img.width, 16);
        assert_eq!(img.height, 16);
        assert_eq!(img.pixels.len(), 16 * 16 * 4);
    }

    #[test]
    fn test_pixel_access() {
        let mut img = RgbaImage::new(4, 4);
        img.set_pixel(2, 2, [255, 128, 64, 255]);

        let pixel = img.get_pixel(2, 2).unwrap();
        assert_eq!(pixel, [255, 128, 64, 255]);
    }

    #[test]
    fn test_format_detection() {
        assert_eq!(detect_format(Path::new("test.png")).unwrap(), ImageFormat::Png);
        assert_eq!(detect_format(Path::new("test.dds")).unwrap(), ImageFormat::Dds);
        assert!(detect_format(Path::new("test.jpg")).is_err());
    }
}
