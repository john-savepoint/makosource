// DDS texture loader using the ddsfile crate

use std::fs::File;
use std::path::Path;
use crate::{RgbaImage, Result, FormatError};

/// Load a DDS file into RGBA8 format
pub fn load(path: &Path) -> Result<RgbaImage> {
    let file = File::open(path)?;
    let dds = ddsfile::Dds::read(file)
        .map_err(|e| FormatError::DdsError(format!("Failed to read DDS: {}", e)))?;

    // Convert DDS data to RGBA8
    let rgba_image = dds_to_rgba(&dds)?;

    Ok(rgba_image)
}

/// Convert DDS texture data to RGBA8 format
fn dds_to_rgba(dds: &ddsfile::Dds) -> Result<RgbaImage> {
    let width = dds.get_width();
    let height = dds.get_height();

    // Get the main texture data (mipmap level 0)
    let data = dds.get_data(0)
        .map_err(|e| FormatError::DdsError(format!("Failed to get DDS data: {}", e)))?;

    // Handle different DDS formats
    let rgba_pixels = match dds.get_d3d_format() {
        Some(format) => {
            match format {
                // Uncompressed formats
                ddsfile::D3DFormat::A8R8G8B8 => convert_argb8_to_rgba8(data, width, height),
                ddsfile::D3DFormat::X8R8G8B8 => convert_xrgb8_to_rgba8(data, width, height),
                ddsfile::D3DFormat::A8B8G8R8 => convert_abgr8_to_rgba8(data, width, height),
                ddsfile::D3DFormat::R8G8B8 => convert_rgb8_to_rgba8(data, width, height),

                // Compressed formats (DXT)
                ddsfile::D3DFormat::DXT1 => {
                    return Err(FormatError::DdsError(
                        "DXT1 compression not yet supported. Please use uncompressed DDS.".to_string()
                    ));
                }
                ddsfile::D3DFormat::DXT3 | ddsfile::D3DFormat::DXT5 => {
                    return Err(FormatError::DdsError(
                        "DXT3/5 compression not yet supported. Please use uncompressed DDS.".to_string()
                    ));
                }

                _ => {
                    return Err(FormatError::DdsError(
                        format!("Unsupported DDS D3D format: {:?}", format)
                    ));
                }
            }
        }
        None => {
            // Try DXGI format (DX10+ header)
            if let Some(dxgi_format) = dds.get_dxgi_format() {
                match dxgi_format {
                    ddsfile::DxgiFormat::R8G8B8A8_UNorm => {
                        data.to_vec()
                    }
                    ddsfile::DxgiFormat::B8G8R8A8_UNorm => {
                        convert_bgra8_to_rgba8(data, width, height)
                    }
                    _ => {
                        return Err(FormatError::DdsError(
                            format!("Unsupported DXGI format: {:?}", dxgi_format)
                        ));
                    }
                }
            } else {
                return Err(FormatError::DdsError(
                    "DDS file has no recognized format".to_string()
                ));
            }
        }
    };

    Ok(RgbaImage {
        width,
        height,
        pixels: rgba_pixels,
    })
}

/// Convert ARGB8 (A8R8G8B8) to RGBA8
fn convert_argb8_to_rgba8(data: &[u8], width: u32, height: u32) -> Vec<u8> {
    let mut rgba = Vec::with_capacity((width * height * 4) as usize);

    for chunk in data.chunks_exact(4) {
        let a = chunk[0];
        let r = chunk[1];
        let g = chunk[2];
        let b = chunk[3];
        rgba.extend_from_slice(&[r, g, b, a]);
    }

    rgba
}

/// Convert XRGB8 (X8R8G8B8) to RGBA8 (opaque alpha)
fn convert_xrgb8_to_rgba8(data: &[u8], width: u32, height: u32) -> Vec<u8> {
    let mut rgba = Vec::with_capacity((width * height * 4) as usize);

    for chunk in data.chunks_exact(4) {
        let r = chunk[1];
        let g = chunk[2];
        let b = chunk[3];
        rgba.extend_from_slice(&[r, g, b, 255]);
    }

    rgba
}

/// Convert ABGR8 (A8B8G8R8) to RGBA8
fn convert_abgr8_to_rgba8(data: &[u8], width: u32, height: u32) -> Vec<u8> {
    let mut rgba = Vec::with_capacity((width * height * 4) as usize);

    for chunk in data.chunks_exact(4) {
        let a = chunk[0];
        let b = chunk[1];
        let g = chunk[2];
        let r = chunk[3];
        rgba.extend_from_slice(&[r, g, b, a]);
    }

    rgba
}

/// Convert RGB8 (R8G8B8) to RGBA8 (opaque alpha)
fn convert_rgb8_to_rgba8(data: &[u8], width: u32, height: u32) -> Vec<u8> {
    let mut rgba = Vec::with_capacity((width * height * 4) as usize);

    for chunk in data.chunks_exact(3) {
        rgba.extend_from_slice(&[chunk[0], chunk[1], chunk[2], 255]);
    }

    rgba
}

/// Convert BGRA8 (B8G8R8A8) to RGBA8
fn convert_bgra8_to_rgba8(data: &[u8], width: u32, height: u32) -> Vec<u8> {
    let mut rgba = Vec::with_capacity((width * height * 4) as usize);

    for chunk in data.chunks_exact(4) {
        let b = chunk[0];
        let g = chunk[1];
        let r = chunk[2];
        let a = chunk[3];
        rgba.extend_from_slice(&[r, g, b, a]);
    }

    rgba
}
