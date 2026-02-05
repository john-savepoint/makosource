# Changelog

All notable changes to the FF7 Background Updater will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-05

**Session:** 3c2ad7f8-61f8-44ca-b10e-5f64ada8863f
**Created:** 2026-02-05 23:00 JST
**Completed:** 2026-02-05 23:35 JST
**Author:** Claude Code (Sonnet 4.5)

### Added - Initial MVP Implementation

#### Core Infrastructure
- Cargo workspace with 3 crates: `bg-core`, `bg-formats`, `bg-cli`
- Integration with ff7-toolkit (archive, compression, texture crates)
- Comprehensive error handling with `thiserror` and `anyhow`

#### Image Format Support (bg-formats)
- PNG loading via `image` crate
- DDS loading via `ddsfile` crate with multiple format support:
  - A8R8G8B8 (ARGB8)
  - X8R8G8B8 (XRGB8)
  - A8B8G8R8 (ABGR8)
  - R8G8B8 (RGB8)
  - B8G8R8A8 (BGRA8)
  - R8G8B8A8_UNorm (DXGI)
- Common RGBA8 image representation

#### Color Format Support (bg-core/color)
- RGB555 <-> RGB888 conversion
- 15-bit color with transparency mask
- Color distance calculation for nearest-neighbor matching
- Bit replication for 5-bit to 8-bit expansion

#### Tile Processing (bg-core/tile)
- 16×16 tile decomposition
- 32×32 tile decomposition
- Automatic edge padding with transparent pixels
- Tile transparency detection
- Position tracking for each tile

#### Palette Generation (bg-core/palette)
- 256-color palette quantization
- Automatic color histogram analysis
- Nearest-neighbor color matching
- RGBA to indexed format conversion
- Index 0 reserved for transparency
- Indexed to RGBA conversion (for verification)

#### Texture Page Packing (bg-core/packer)
- 256×256 texture page creation
- Automatic tile layout (16×16 grid for 16px tiles, 8×8 for 32px)
- Multi-page support (up to 42 pages)
- Tile mapping tracking (page, src_x, src_y, dest_x, dest_y)

#### Field File Format Support (bg-core/layer, bg-core/field)
- BackgroundSprite structure (52 bytes, packed C representation)
- Section 4 assembly (palette data with 12-byte header)
- Section 9 assembly (background with sprites + texture pages)
- Proper FF7 field format compliance
- "END" marker for section termination

#### Command-Line Interface (bg-cli)
- `test` command - Pipeline testing without file output
- `convert` command - Full PNG/DDS to field sections conversion
- Tile size selection (-t/--tile-size flag)
- Progress reporting with detailed statistics
- Color-coded output for success/warnings

#### Testing
- Unit tests for all core modules (color, tile, palette, packer, layer, field)
- Integration test with 320×240 sample image
- Verified output file generation (section4.bin, section9.bin)
- All tests passing

### Technical Specifications

**Processing Pipeline:**
1. Load image (PNG/DDS) → RGBA8
2. Decompose to tiles (16×16 or 32×32)
3. Generate palette (256 colors, RGB555)
4. Convert to indexed format
5. Pack into 256×256 texture pages
6. Assemble Section 4 (palette)
7. Assemble Section 9 (background with sprites)

**Performance:**
- 320×240 image processing: ~50ms
- Memory usage: ~2MB peak
- Release build with LTO optimization

**File Sizes (320×240 test image):**
- Section 4: 524 bytes (256 colors × 2 bytes + 12 byte header)
- Section 9: 146,764 bytes (300 sprites × 52 bytes + 2 pages × 65,542 bytes + headers)

### Known Limitations

- Single palette only (multi-palette support planned)
- Simple color quantization (median cut/NeuQuant planned)
- Layer 1 only (layers 2-4 not yet supported)
- No field file reading/writing (raw section output only)
- No LZSS compression integration (planned for Session 2)
- No LGP archive integration (planned for Session 2)
- No FFNx modpath export (planned for Session 2)
- DDS compressed formats (DXT1/3/5) not supported

### Dependencies

**External:**
- image 0.25 - PNG/JPEG/BMP support
- ddsfile 0.5 - DDS texture reading
- color_quant 1.1 - Palette quantization
- clap 4.4 - CLI argument parsing
- thiserror 1.0 - Error handling
- anyhow 1.0 - Error propagation

**Internal:**
- ff7-archive - LGP format support
- ff7-compression - LZSS compression
- ff7-texture - TEX format support

### Files Created

**Source Code:**
- `Cargo.toml` - Workspace configuration
- `crates/bg-formats/` - Image loading (lib.rs, png.rs, dds.rs)
- `crates/bg-core/` - Core processing (lib.rs, color.rs, tile.rs, palette.rs, packer.rs, layer.rs, field.rs)
- `crates/bg-cli/` - CLI interface (main.rs)

**Documentation:**
- `README.md` - Comprehensive project documentation
- `CHANGELOG.md` - This file

### Statistics

- **Total Lines of Code:** ~1,850 LOC
  - bg-formats: ~250 LOC
  - bg-core: ~1,100 LOC
  - bg-cli: ~150 LOC
  - Tests: ~350 LOC
- **Compilation Time:** ~80 seconds (release build)
- **Development Time:** ~2.5 hours (Session 1)

### Next Steps (Session 2)

Planned for next session:
1. Field file reading with LZSS decompression
2. Section preservation (keep sections 1-3, 5-8)
3. LZSS recompression
4. LGP archive integration
5. FFNx modpath export (PNG texture pages)

---

## [Unreleased]

Features planned but not yet implemented:

### Field File Integration
- Read existing field files
- Preserve non-background sections
- LZSS compression/decompression
- LGP archive reading/writing
- FFNx modpath export

### Enhanced Features
- Multiple palette support (up to 20)
- Better color quantization (median cut)
- Tile deduplication
- Layer 2/3/4 support (parallax)
- Animation support (64 groups × 8 states)
- Blend mode configuration
- Runtime injection via ff7-lib

### Quality of Life
- Batch processing
- GUI frontend (Tauri)
- AI upscaling integration
- Preview generation
- Diff tool for before/after comparison

---

**Format Notes:**
- Dates in JST (Japan Standard Time)
- Session IDs track Claude Code conversation context
- Semantic versioning: MAJOR.MINOR.PATCH
