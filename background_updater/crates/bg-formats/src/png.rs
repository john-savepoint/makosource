// PNG image loader using the image crate

use std::path::Path;
use crate::{RgbaImage, Result, FormatError};

/// Load a PNG file into RGBA8 format
pub fn load(path: &Path) -> Result<RgbaImage> {
    let img = image::open(path)
        .map_err(|e| FormatError::LoadError(format!("Failed to open PNG: {}", e)))?;

    let rgba = img.to_rgba8();

    Ok(RgbaImage {
        width: rgba.width(),
        height: rgba.height(),
        pixels: rgba.into_raw(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_png_loading() {
        // Create a simple 2x2 PNG for testing
        let img = image::RgbaImage::from_fn(2, 2, |x, y| {
            if (x + y) % 2 == 0 {
                image::Rgba([255, 0, 0, 255])
            } else {
                image::Rgba([0, 255, 0, 255])
            }
        });

        let temp_path = std::env::temp_dir().join("test.png");
        img.save(&temp_path).unwrap();

        let loaded = load(&temp_path).unwrap();
        assert_eq!(loaded.width, 2);
        assert_eq!(loaded.height, 2);

        std::fs::remove_file(temp_path).ok();
    }
}
