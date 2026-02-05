// FF7 Background Updater CLI
// Created: 2026-02-05 23:10 JST
// Session: 3c2ad7f8-61f8-44ca-b10e-5f64ada8863f

use std::path::PathBuf;
use clap::{Parser, Subcommand};
use anyhow::Result;

#[derive(Parser)]
#[command(name = "bg-updater")]
#[command(version = "0.1.0")]
#[command(about = "FF7 Background Updater - Convert PNG/DDS to FF7 field backgrounds", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Convert PNG/DDS to field file sections
    Convert {
        /// Input image (PNG or DDS)
        #[arg(short, long)]
        input: PathBuf,

        /// Output directory for sections
        #[arg(short, long)]
        output: PathBuf,

        /// Tile size (16 or 32)
        #[arg(short, long, default_value = "16")]
        tile_size: u16,
    },

    /// Test the processing pipeline with a sample image
    Test {
        /// Input image (PNG or DDS)
        #[arg(short, long)]
        input: PathBuf,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Convert { input, output, tile_size } => {
            convert_image(&input, &output, tile_size)?;
        }
        Commands::Test { input } => {
            test_pipeline(&input)?;
        }
    }

    Ok(())
}

fn convert_image(input: &PathBuf, output: &PathBuf, tile_size: u16) -> Result<()> {
    println!("Converting {} to FF7 background...", input.display());
    println!("Tile size: {}x{}", tile_size, tile_size);

    // Load image
    println!("Loading image...");
    let image = bg_formats::load_image(input)?;
    println!("Loaded {}x{} image", image.width, image.height);

    // Decompose into tiles
    println!("Decomposing into {}x{} tiles...", tile_size, tile_size);
    let tile_size_enum = bg_core::tile::TileSize::from_u16(tile_size)?;
    let tiles = bg_core::decompose_to_tiles(&image, tile_size_enum)?;
    println!("Created {} tiles", tiles.len());

    // Generate palettes
    println!("Generating palette...");
    let (palettes, indexed_tiles) = bg_core::generate_palettes(&tiles, 1)?;
    println!("Generated {} palette(s)", palettes.len());

    // Pack into texture pages
    println!("Packing into texture pages...");
    let (pages, mappings) = bg_core::pack_tiles_to_pages(&indexed_tiles)?;
    println!("Created {} texture page(s)", pages.len());

    // Create Section 4 (palette)
    println!("Creating Section 4 (palette)...");
    let section4 = bg_core::create_section4_palette(&palettes)?;
    println!("Section 4 size: {} bytes", section4.len());

    // Create Section 9 (background)
    println!("Creating Section 9 (background)...");
    let section9 = bg_core::create_section9_background(&pages, &mappings)?;
    println!("Section 9 size: {} bytes", section9.len());

    // Write output files
    std::fs::create_dir_all(output)?;

    let section4_path = output.join("section4.bin");
    std::fs::write(&section4_path, section4)?;
    println!("Wrote {}", section4_path.display());

    let section9_path = output.join("section9.bin");
    std::fs::write(&section9_path, section9)?;
    println!("Wrote {}", section9_path.display());

    println!("\n✓ Conversion complete!");
    println!("  Section 4 (palette): {}", section4_path.display());
    println!("  Section 9 (background): {}", section9_path.display());

    Ok(())
}

fn test_pipeline(input: &PathBuf) -> Result<()> {
    println!("Testing processing pipeline with {}...", input.display());

    // Load image
    println!("\n[1/5] Loading image...");
    let image = bg_formats::load_image(input)?;
    println!("      ✓ Loaded {}x{} image ({} pixels)",
        image.width, image.height, image.pixel_count());

    // Decompose into tiles
    println!("\n[2/5] Decomposing into tiles...");
    let tiles = bg_core::decompose_to_tiles(&image, bg_core::tile::TileSize::Size16x16)?;
    println!("      ✓ Created {} tiles (16x16)", tiles.len());

    // Count transparent tiles
    let transparent_count = tiles.iter()
        .filter(|t| t.tile.is_transparent())
        .count();
    println!("      - {} transparent tiles", transparent_count);
    println!("      - {} opaque tiles", tiles.len() - transparent_count);

    // Generate palettes
    println!("\n[3/5] Generating palette...");
    let (palettes, indexed_tiles) = bg_core::generate_palettes(&tiles, 1)?;
    println!("      ✓ Generated palette with {} colors", palettes[0].colors.len());

    // Pack into texture pages
    println!("\n[4/5] Packing into texture pages...");
    let (pages, mappings) = bg_core::pack_tiles_to_pages(&indexed_tiles)?;
    println!("      ✓ Created {} texture page(s)", pages.len());
    println!("      - {} tile mappings", mappings.len());

    // Create field sections
    println!("\n[5/5] Creating field sections...");
    let section4 = bg_core::create_section4_palette(&palettes)?;
    let section9 = bg_core::create_section9_background(&pages, &mappings)?;
    println!("      ✓ Section 4: {} bytes", section4.len());
    println!("      ✓ Section 9: {} bytes", section9.len());

    println!("\n✓ All tests passed!");

    Ok(())
}
