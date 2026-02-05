// FF7 Background Updater - Core Processing Logic
// Created: 2026-02-05 23:05 JST
// Session: 3c2ad7f8-61f8-44ca-b10e-5f64ada8863f
//
// Core background processing: tile decomposition, palette generation, and field file assembly.

use thiserror::Error;

pub mod color;
pub mod tile;
pub mod palette;
pub mod packer;
pub mod layer;
pub mod field;

#[derive(Error, Debug)]
pub enum CoreError {
    #[error("Tile decomposition failed: {0}")]
    TileError(String),

    #[error("Palette generation failed: {0}")]
    PaletteError(String),

    #[error("Texture packing failed: {0}")]
    PackerError(String),

    #[error("Field file error: {0}")]
    FieldError(String),

    #[error("Image format error: {0}")]
    FormatError(#[from] bg_formats::FormatError),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, CoreError>;

// Re-export commonly used types
pub use color::{Color555, Color888};
pub use tile::{Tile, TileSize, decompose_to_tiles};
pub use palette::{Palette, generate_palettes};
pub use packer::{TexturePage, pack_tiles_to_pages};
pub use layer::BackgroundSprite;
pub use field::{create_section4_palette, create_section9_background};
