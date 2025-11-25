# FF7 Text System Architecture

**Extracted From**: FINDINGS.md
**Section Lines**: 657-728
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### FF Text Encoding Format

Full specification: https://qhimm-modding.fandom.com/wiki/FF7/FF_Text

**Character Mapping**:
```
Offset by 0x20 from ASCII
0x00-0x5F: Standard ASCII characters (space through ~)
0x60-0xBF: Extended Latin characters (àáâã etc.)
0xC0-0xD3: Special symbols and box-drawing characters
0xD4-0xDF: Produce graphical errors (unused)
0xE0-0xFF: Control codes and special functions
```

**Control Codes**:
- `{CLOUD}`, `{BARRET}`, etc. - Character name variables
- `{GRAY}`, `{BLUE}`, `{RED}`, etc. - Text colors
- `{CHOICE}` - Menu selection indent
- `{OK}` - Wait for confirmation
- `{NEW}` - Clear window and continue
- `{WAIT x}` - Delay by x frames
- `FE D2-DB` - Color function opcodes

### Text Storage Locations

**Field Scripts** (`flevel.lgp`):
- LZS compressed field files
- Section 1 contains script & dialog
- Text referenced by opcodes in field script
- Window parameters (x, y, width, height) stored with text

**Kernel Data** (`KERNEL.BIN`):
- BIN-GZIP archive format
- 27 sections total
- Sections 1-9: Binary data
- Sections 10-27: Text data (FF Text encoding)
- Full structure documented

**Battle Text** (`scene.bin`):
- 256 separate battle scene files
- Enemy names (3 per file)
- Attack names (32 per file)
- AI dialogue text
- Scene lookup table in KERNEL.BIN

**Menu Text** (`kernel2.bin` - PC only):
- LZS compressed
- Sections 10-27 from KERNEL.BIN ungzipped and concatenated
- Maximum size: 27KB (27,648 bytes) uncompressed
- Item names, descriptions, equipment text

### Font Rendering Pipeline

**Current English System**:
1. Text opcodes trigger text rendering
2. Engine looks up character in FF Text table
3. Single-byte value used as index into font texture
4. Character spacing read from `window.bin`
5. Glyph rendered from `usfont.png`

**Required Japanese System**:
1. Text opcodes trigger text rendering
2. Engine parses double-byte character value
3. Determine which of 6 font textures contains glyph
4. Calculate offset within that texture
5. Read spacing data (proportional fonts)
6. Render glyph from appropriate `jafont_X.tex`

---

