# Required Modifications

**Extracted From**: FINDINGS.md
**Section Lines**: 1171-1267
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### Component Breakdown

Based on research, here are the specific components that need modification:

### 1. Character Encoding System

**Current State**:
- FF Text format: single-byte, ASCII offset 0x20
- 256 character maximum
- Control codes in 0xE0-0xFF range

**Required Changes**:
- Implement double-byte character support
- Character range: minimum 2,000 glyphs
- Maintain backward compatibility with English
- Escape sequence to toggle encoding mode

**Affected Files**:
- Game executable (decoding routines)
- All text files (new encoding format)
- Text editing tools (touphScript, etc.)

### 2. Font Texture System

**Current State**:
- Single font texture loaded from `menu_us.lgp`
- `usfont.png` + color variants
- Direct character → texture offset mapping

**Required Changes**:
- Load six font textures (`jafont_1.tex` through `jafont_6.tex`)
- Implement character → texture selection logic
- Character → offset within texture calculation
- Memory management for 6x texture data

**Affected Files**:
- Graphics driver (FFNx)
- `menu_ja.lgp` (new archive with 6 textures)
- Game executable (texture loading code)

### 3. Character Spacing System

**Current State**:
- Fixed-width assumed for most characters
- Spacing data in `window.bin`
- Single spacing table

**Required Changes**:
- Proportional font support (Japanese varies widely)
- Six spacing tables (one per texture)
- Width calculation for each glyph
- Kerning support (optional but recommended)

**Affected Files**:
- `window.bin` (expanded spacing data)
- Window sizing calculations in executable

### 4. Text File Formats

**Current State**:
- `flevel.lgp`: FF Text encoding
- `KERNEL.BIN`: FF Text encoding
- `kernel2.bin`: FF Text encoding
- `scene.bin`: FF Text encoding

**Required Changes**:
- Convert all text to new encoding
- Update text length calculations
- Modify compression (if needed for larger text)
- Update pointers/offsets

**Affected Files**:
- All source text files
- Game code that reads text files
- Text editing tools

### 5. Window Sizing System

**Current State**:
- Auto-sizing based on English character widths
- Fixed height calculations
- Assumes single-byte character = one glyph

**Required Changes**:
- Calculate width with proportional Japanese fonts
- Height calculation for vertical text (if applicable)
- Window parameter adjustments
- Line breaking for multi-byte characters

**Affected Files**:
- Field script window opcodes
- Game executable window rendering

---

