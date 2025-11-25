# FFNx Japanese Implementation - Verification Checklist

**Created**: 2025-11-24 17:32:00 JST (Monday)
**Last Modified**: 2025-11-24 23:08:00 JST (Monday)
**Version**: 2.0.0
**Author**: John Zealand-Doyle
**Session-ID**: 379a17a1-e73f-41b7-86b2-6c83f196e524
**Purpose**: Distinguish speculation from verified facts during implementation

---

## Overview

This document contains **critical questions that MUST be answered** by inspecting actual game files and FFNx source code. The Master Bible and research documentation contain assumptions that need verification before implementation begins.

---

## ⚠️ CRITICAL UPDATE - Session 11 Findings

**Date:** 2025-11-24 23:10:00 JST (Monday)
**Session:** 8f58819d-f9c4-4f04-8e95-4af04d782606
**Updated:** 2025-11-25 12:00:00 JST (Tuesday)

**✅ MAJOR CODEBASE ANALYSIS COMPLETED**

A comprehensive deep-dive analysis of the FFNx source code has been completed. **Many assumptions in the Master Bible have been verified or corrected.**

**📄 Note:** The original `VERIFICATION_FINDINGS_SESSION_11.md` document has been **archived** to `archive/` as its strategic recommendations were superseded by PR #737 discovery. Key valid findings were extracted to the Master Bible Section 14.5 (VREF/VRASS Macros).

**Key Discoveries (Still Valid):**
- ❌ `src/ff7/font.cpp` does NOT exist (PR #737 created `japanese_text.cpp` instead)
- ✅ Font width table confirmed at `0x99DDA8` (US 1.02)
- ✅ Multi-texture support exists (via palette system, can adapt)
- ❌ NO `font_language` config option (PR #737 adds `ff7_japanese_edition`)
- ✅ Texture path confirmed: `mods/Textures/`
- ✅ BGFX multi-backend (DirectX 11/12, Vulkan, OpenGL)
- ✅ Mid-frame texture switching FULLY supported
- ⚠️ Windows-only build (cannot build on macOS)

**Status Updates Below:**

- Many questions in Sections 4, 8 are now **ANSWERED** by PR #737's actual code (see Section 16)
- **NEW Section 17** added for Phase 1.5 bug investigation questions

---

**Status Legend:**
- ❓ **Unverified** - Assumption from documentation, needs confirmation
- ✅ **Verified** - Confirmed by inspecting actual files/code
- ❌ **False** - Documentation was incorrect
- ⚠️ **Partial** - Partially true, needs clarification

---

## SECTION 1: kernel.bin File Format Verification

### 1.1 Character Encoding in kernel.bin Text Sections

**Current Assumption** (from Session 7/8 findings):
> `lang-ja/kernel/KERNEL.BIN` stores "Gzip compressed Shift-JIS encoded text"

**Questions to Answer:**

- [ ] ❓ **Q1.1.1**: Open `lang-ja/kernel/KERNEL.BIN` with hex editor. Are sections 10-27 actually Shift-JIS encoded?
  - **How to verify**: Extract sections 10-27, decompress gzip, look at raw bytes
  - **Expected if Shift-JIS**: Double-byte sequences like `82 A0` (あ), `82 A2` (い)
  - **Expected if Custom**: Single-byte 0x00-0xE6 or two-byte FA XX, FB XX sequences
  - **Tool**: `unbingz` from ff7tools, or hex editor (HexFiend, 010 Editor)

- [ ] ❓ **Q1.1.2**: Do kernel.bin text sections contain FA-FE page markers, or is that a runtime-only construct?
  - **How to verify**: Search for byte sequences starting with 0xFA, 0xFB, 0xFC, 0xFD, 0xFE
  - **Expected if FA-FE in file**: Sequences like `FA 00 FA 01` for multi-character words
  - **Expected if Shift-JIS in file**: No FA-FE markers present
  - **Tool**: Hex editor + grep for FA-FE patterns

- [ ] ❓ **Q1.1.3**: Compare English vs Japanese kernel.bin text sections - are they encoded differently?
  - **How to verify**: Extract same section (e.g., section 10) from both `lang-en/kernel/KERNEL.BIN` and `lang-ja/kernel/KERNEL.BIN`
  - **Expected**: English uses single-byte ASCII-like, Japanese uses... (to be determined)
  - **Tool**: `unbingz`, diff tool

### 1.2 kernel.bin Structure Verification

- [ ] ❓ **Q1.2.1**: Confirm kernel.bin has exactly 27 sections
  - **How to verify**: Count gzip headers (0x1F 0x8B) in file
  - **Tool**: Hex editor, or `unbingz -l KERNEL.BIN`

- [ ] ❓ **Q1.2.2**: Verify sections 1-9 are binary data, 10-27 are text
  - **How to verify**: Extract all 27 sections, inspect content type
  - **Expected**: Sections 1-9 have structured binary, 10-27 have text-like data
  - **Tool**: `unbingz`, hex editor

- [ ] ❓ **Q1.2.3**: Confirm 6-byte header format (gzip length + ungzip length + file type)
  - **How to verify**: Inspect header of each section
  - **Tool**: Hex editor at offsets documented in findings

### 1.3 kernel2.bin (PC Version)

- [ ] ❓ **Q1.3.1**: Does kernel2.bin exist in the game files you have access to?
  - **How to verify**: Check `/data/kernel/kernel2.bin` path
  - **Note**: May be PC Steam version only

- [ ] ❓ **Q1.3.2**: Is kernel2.bin actually LZSS compressed, or just concatenated?
  - **How to verify**: Check first 4 bytes for LZSS signature, try `unlzss` tool
  - **Tool**: `unlzss kernel2.bin kernel2_decompressed.bin`

- [ ] ❓ **Q1.3.3**: Verify kernel2.bin max size is 27KB uncompressed
  - **How to verify**: Decompress, check file size
  - **Tool**: `ls -lh kernel2_decompressed.bin`

- [ ] ❓ **Q1.3.4**: Confirm kernel2.bin contains ONLY sections 10-27 from KERNEL.BIN
  - **How to verify**: Compare decompressed kernel2.bin with extracted KERNEL.BIN sections 10-27
  - **Tool**: diff, hex comparison

---

## SECTION 2: Character Encoding Runtime Behavior

### 2.1 FA-FE Extended Page System

**Current Assumption** (from Session 8):
> FF7 uses FA-FE two-byte encoding at runtime where:
> - FA XX = jafont_2
> - FB XX = jafont_3
> - FC XX = jafont_4
> - FD XX = jafont_5
> - FE XX = jafont_6

**Questions to Answer:**

- [ ] ❓ **Q2.1.1**: Where does the Shift-JIS → FA-FE conversion happen?
  - **How to verify**: Search FFNx source for encoding conversion functions
  - **Search terms**: `MultiByteToWideChar`, `Shift-JIS`, `FA`, `FB`, character encoding
  - **Files to check**: `src/ff7/font.cpp`, `src/ff7/text.cpp`, `src/saveload.cpp`

- [ ] ❓ **Q2.1.2**: Does FF7.exe (original game) or FFNx handle the FA-FE system?
  - **How to verify**: Disassemble FF7.exe text rendering functions
  - **Alternative**: Check if FFNx source has text decoder
  - **Tool**: IDA Pro, Ghidra, or grep FFNx source

- [ ] ❓ **Q2.1.3**: Is there a lookup table converting Shift-JIS → FA-FE indices?
  - **How to verify**: Search for arrays/maps in FFNx or game memory
  - **Expected**: Array of 2808+ entries mapping Unicode/Shift-JIS to texture position
  - **Files to check**: FFNx config files, embedded data structures

### 2.2 Character Width Table

**Current Assumption** (from Bible):
> Width table at memory address `0x99DDA8` (256 bytes) for US 1.02

**Questions to Answer:**

- [ ] ❓ **Q2.2.1**: What is the actual memory address of the width table?
  - **How to verify**: Use Cheat Engine / memory scanner to find the table
  - **Search pattern**: Array of 256 bytes with values 0-64 (character widths)
  - **Note**: Address will differ per game version

- [ ] ❓ **Q2.2.2**: Does the width table cover all 6 jafont textures (1536 chars) or just one page (256 chars)?
  - **How to verify**: Check table size in memory
  - **Expected if 1 page**: 256 bytes
  - **Expected if 6 pages**: 1536 bytes
  - **Tool**: Memory inspector

- [ ] ❓ **Q2.2.3**: Is the width table loaded from a file or hardcoded?
  - **How to verify**: Search FFNx source for width table loading
  - **Files to check**: `src/ff7/font.cpp`, config parsers
  - **Expected**: Loaded from `window.bin` or similar

- [ ] ❓ **Q2.2.4**: Do Japanese fonts use proportional or fixed-width spacing?
  - **How to verify**: Inspect jafont width values in table
  - **Expected**: All same value (fixed) or varying values (proportional)
  - **Tool**: Memory dump analysis

---

## SECTION 3: Font Texture File Format

### 3.1 jafont_*.tex Format

**Current Assumption** (from Session 8):
> - TEX header: 236 bytes (0xEC)
> - Dimensions: 1024×1024 pixels
> - Format: 32-bit RGBA, BGRA byte order
> - Grid: 16×16 (256 glyphs)
> - Glyph size: 64×64 pixels

**Questions to Answer:**

- [ ] ❓ **Q3.1.1**: Verify TEX file header structure
  - **How to verify**: Open `jafont_1.tex` with hex editor, check first 236 bytes
  - **Expected fields**: Width, height, bit depth, color format at known offsets
  - **Tool**: Hex editor, TEX format spec from wiki

- [ ] ❓ **Q3.1.2**: Confirm pixel data starts at offset 0xEC (236 bytes)
  - **How to verify**: Extract pixel data from offset 236, render as raw image
  - **Tool**: ImageMagick, Python PIL script

- [ ] ❓ **Q3.1.3**: Verify BGRA byte order vs RGBA
  - **How to verify**: Check if blue/red channels are swapped in current extraction
  - **Test**: Convert TEX → PNG, check if colors look correct
  - **Tool**: Your existing TEX converter script

- [ ] ❓ **Q3.1.4**: Are all 6 jafont textures exactly the same format?
  - **How to verify**: Compare headers of all 6 .tex files byte-by-byte
  - **Tool**: `diff`, hex editor

### 3.2 Font Texture Grid Layout

- [ ] ❓ **Q3.2.1**: Confirm 16×16 grid with 64×64 glyphs (no padding/spacing)
  - **How to verify**: Visual inspection of extracted PNGs
  - **Expected**: Characters aligned perfectly to 64-pixel boundaries
  - **Tool**: Image viewer with grid overlay

- [ ] ❓ **Q3.2.2**: Are glyphs centered within 64×64 cells, or do they vary?
  - **How to verify**: Measure actual glyph pixels in multiple cells
  - **Expected**: Smaller glyphs (e.g., punctuation) centered, kanji fills cell
  - **Tool**: Photoshop/GIMP pixel ruler

- [ ] ❓ **Q3.2.3**: Verify index calculation formula: `pixel_x = (index % 16) * 64`
  - **How to verify**: Manually locate known characters by index
  - **Test**: Index 0 = (0,0), Index 1 = (64,0), Index 16 = (0,64)
  - **Tool**: Visual inspection of PNG

---

## SECTION 4: FFNx Codebase Architecture

### 4.1 Font System Implementation

**Current Assumption** (from Bible Section 5):
> FFNx has a font subsystem in `src/ff7/font.cpp`

**Questions to Answer:**

- [ ] ❓ **Q4.1.1**: Does `src/ff7/font.cpp` actually exist in FFNx repo?
  - **How to verify**: Clone FFNx repo, check file structure
  - **Repo**: https://github.com/julianxhokaxhiu/FFNx
  - **Tool**: `ls -la src/ff7/`

- [ ] ❓ **Q4.1.2**: What functions handle text rendering in FFNx?
  - **How to verify**: Search source for text/font rendering functions
  - **Search terms**: `DrawText`, `RenderGlyph`, `TextOutput`
  - **Tool**: grep, ripgrep

- [ ] ❓ **Q4.1.3**: How does FFNx currently load font textures?
  - **How to verify**: Find texture loading code for English fonts
  - **Files to check**: `src/saveload.cpp`, `src/gl/gl.cpp`
  - **Expected**: PNG loading from `mods/Textures/` path

- [ ] ❓ **Q4.1.4**: Is there existing multi-texture support for fonts?
  - **How to verify**: Check if FFNx already loads multiple font pages
  - **Search terms**: `font_page`, `texture_set`, multiple texture handles
  - **Tool**: Code search in FFNx repo

### 4.2 Configuration System

- [ ] ❓ **Q4.2.1**: Does FFNx.toml support `font_language` setting?
  - **How to verify**: Check FFNx config parser and example config
  - **Files to check**: `src/cfg.cpp`, `FFNx.toml.example`
  - **Tool**: grep for `font_language`

- [ ] ❓ **Q4.2.2**: What config options already exist for fonts?
  - **How to verify**: List all `font_*` config keys
  - **Tool**: grep `^font_` in config files

- [ ] ❓ **Q4.2.3**: Where does FFNx look for texture override files?
  - **How to verify**: Find path resolution code
  - **Expected**: `mods/Textures/menu/` or similar
  - **Tool**: Search for "mods/Textures" in source

### 4.3 Renderer Integration

- [ ] ❓ **Q4.3.1**: Which rendering backend does FFNx use? (OpenGL/D3D11/Vulkan)
  - **How to verify**: Check renderer abstraction layer
  - **Files to check**: `src/gl/gl.cpp`, `src/renderer.cpp`
  - **Expected**: BGFX multi-backend

- [ ] ❓ **Q4.3.2**: How does FFNx handle texture binding during rendering?
  - **How to verify**: Find texture bind/switch functions
  - **Search terms**: `BindTexture`, `SetTexture`, texture slot management
  - **Tool**: Code search

- [ ] ❓ **Q4.3.3**: Can FFNx switch textures mid-frame (needed for FA-FE page switching)?
  - **How to verify**: Check rendering pipeline, look for texture state changes
  - **Expected**: Yes, but may need optimization
  - **Tool**: Code review of rendering loop

---

## SECTION 5: Game File Structure Verification

### 5.1 Directory Layout

**Current Assumption** (from Session 7):
> Japanese assets are in `lang-ja/` subdirectories

**Questions to Answer:**

- [ ] ❓ **Q5.1.1**: Confirm actual directory structure of your game files
  - **How to verify**: Run `tree -L 3` on game installation directory
  - **Expected paths**:
    - `lang-ja/kernel/KERNEL.BIN`
    - `lang-ja/menu_ja.lgp`
    - `lang-ja/jfleve.lgp` (or `flevel_ja.lgp`?)
    - `lang-ja/world_ja.lgp`
  - **Tool**: File browser, terminal

- [ ] ❓ **Q5.1.2**: Are Japanese fonts in `menu_ja.lgp` or separate files?
  - **How to verify**: Extract `menu_ja.lgp`, list contents
  - **Expected**: Contains `jafont_1.tex` through `jafont_6.tex`
  - **Tool**: LGP extractor (ff7tools, Elena, or custom script)

- [ ] ❓ **Q5.1.3**: Does `jfleve.lgp` vs `flevel_ja.lgp` typo actually exist?
  - **How to verify**: Check actual filename in `lang-ja/` directory
  - **Note**: Bible mentions "JFLEVE typo" but may be speculation
  - **Tool**: `ls lang-ja/*.lgp`

### 5.2 File Sizes and Versions

- [ ] ❓ **Q5.2.1**: What version of FF7 do you have access to?
  - **How to verify**: Check `FF7.exe` or game launcher version
  - **Expected**: Steam version, Japanese re-release, or original 1998?
  - **Tool**: File properties, version info

- [ ] ❓ **Q5.2.2**: Are lang-ja assets complete or modified by previous mods?
  - **How to verify**: Compare file checksums with known clean versions
  - **Note**: Important for ensuring baseline correctness
  - **Tool**: `sha256sum`, compare with community checksums

---

## SECTION 6: AF3DN.P Driver Behavior

### 6.1 Driver Purpose and Functionality

**Current Assumption** (from Session 8):
> AF3DN.P is a DirectX 9 wrapper created by DotEmu

**Questions to Answer:**

- [ ] ❓ **Q6.1.1**: Is AF3DN.P actually present in your game installation?
  - **How to verify**: Check for `AF3DN.P` file in game directory
  - **Expected location**: Root game folder or `/drivers/`
  - **Tool**: File search

- [ ] ❓ **Q6.1.2**: What functions does AF3DN.P export?
  - **How to verify**: Run `objdump -x AF3DN.P | grep "Export"` or use PE viewer
  - **Expected**: `new_dll_graphics_driver` and dotemu registry functions
  - **Tool**: objdump, Dependency Walker, PE Explorer

- [ ] ❓ **Q6.1.3**: Does AF3DN.P contain any character encoding logic?
  - **How to verify**: Search binary for Shift-JIS → Unicode conversion calls
  - **Search**: Look for `MultiByteToWideChar` calls with CP_SHIFT_JIS (932)
  - **Tool**: IDA Pro, Ghidra, strings command

- [ ] ❓ **Q6.1.4**: Is AF3DN.P actually used when FFNx is installed?
  - **How to verify**: Check FFNx documentation/code for AF3DN.P replacement
  - **Expected**: FFNx replaces AF3DN.P entirely
  - **Tool**: FFNx documentation, config files

### 6.2 Registry Virtualization

- [ ] ❓ **Q6.2.1**: Do the `dotemuRegXxx` functions actually intercept Windows registry?
  - **How to verify**: Reverse engineer those functions in AF3DN.P
  - **Alternative**: Test with/without AF3DN.P, see if registry behavior changes
  - **Tool**: Disassembler, Process Monitor

---

## SECTION 7: Character Mapping Verification

### 7.1 Your Existing character_tables/ Data

**Current Status**: You have OCR-extracted character mappings

**Questions to Answer:**

- [ ] ❓ **Q7.1.1**: Do your character_tables/*.json mappings align with actual game text?
  - **How to verify**: Extract known dialogue from game files, decode using your mappings
  - **Test**: Find a simple menu item (e.g., "アイテム" / Items), verify encoding matches
  - **Tool**: Compare extracted bytes with your JSON mappings

- [ ] ❓ **Q7.1.2**: Are there characters in game files NOT in your OCR mappings?
  - **How to verify**: Extract all unique character codes from kernel.bin sections 10-27
  - **Tool**: Python script to parse and collect unique byte sequences

- [ ] ❓ **Q7.1.3**: Are glyphs actually at the positions your mappings indicate?
  - **How to verify**: Visual comparison of jafont PNG position vs mapping JSON
  - **Test**: Pick 10 random characters, verify position matches texture
  - **Tool**: Manual inspection with image viewer

### 7.2 Unicode Mapping Accuracy

- [ ] ❓ **Q7.2.1**: Did MangaOCR correctly identify all kanji?
  - **How to verify**: Manually verify ~50 random kanji from jafont_2 through jafont_6
  - **Expected accuracy**: 90%+ for common kanji, lower for rare/old forms
  - **Tool**: Human verification against jafont PNGs

- [ ] ❓ **Q7.2.2**: Are katakana/hiragana mappings 100% correct?
  - **How to verify**: These should be perfect - verify against jafont_1.png
  - **Tool**: Visual inspection, compare with Unicode kana chart

---

## SECTION 8: FFNx Modification Feasibility

### 8.1 Code Modification Points

**Current Assumption** (from Bible Section 7):
> Need to modify:
> - `src/cfg.h` / `src/cfg.cpp` (config)
> - `src/common.cpp` (detection & texture allocation)
> - `src/saveload.cpp` (multi-page loader)
> - `src/redirect.cpp` (file redirection)
> - `src/ff7/font.cpp` (width table)

**Questions to Answer:**

- [ ] ❓ **Q8.1.1**: Do these files actually exist in FFNx repo?
  - **How to verify**: Clone repo, check file paths
  - **Tool**: `ls -la src/` and subdirectories

- [ ] ❓ **Q8.1.2**: What is FFNx's code style and contribution guidelines?
  - **How to verify**: Read `CONTRIBUTING.md`, check existing code patterns
  - **Expected**: Consistent naming, comment style, formatting
  - **Tool**: GitHub repo documentation

- [ ] ❓ **Q8.1.3**: Does FFNx have a plugin/extension system, or must we modify core?
  - **How to verify**: Check for plugin API, mod hooks
  - **Preferred**: Plugin system (less invasive)
  - **Fallback**: Core modifications (fork required)
  - **Tool**: Documentation, code review

### 8.2 Build System and Dependencies

- [ ] ❓ **Q8.2.1**: What build system does FFNx use? (CMake, Visual Studio, Make?)
  - **How to verify**: Check for `CMakeLists.txt`, `.sln`, `Makefile`
  - **Tool**: Root directory inspection

- [ ] ❓ **Q8.2.2**: What dependencies does FFNx require?
  - **How to verify**: Read build documentation, check dependency list
  - **Expected**: BGFX, FFmpeg, possibly DirectX SDK
  - **Tool**: `README.md`, build docs

- [ ] ❓ **Q8.2.3**: Can FFNx be built on macOS for development/testing?
  - **How to verify**: Check CI/CD configs, platform support docs
  - **Preferred**: Yes (for your dev environment)
  - **Tool**: GitHub Actions workflows, build docs

---

## SECTION 9: Testing Infrastructure

### 9.1 Test Game Instance

- [ ] ❓ **Q9.1.1**: Do you have a working FF7 installation to test against?
  - **How to verify**: Launch game, confirm it runs
  - **Required**: Clean baseline installation

- [ ] ❓ **Q9.1.2**: Can you run FFNx with your current game installation?
  - **How to verify**: Install FFNx, test if game launches
  - **Tool**: FFNx installation guide

- [ ] ❓ **Q9.1.3**: Is there a debug/dev mode in FFNx for logging?
  - **How to verify**: Check FFNx.toml for `trace_all` or debug settings
  - **Tool**: Config file inspection

### 9.2 Testing Tools

- [ ] ❓ **Q9.2.1**: What tools can monitor FF7 memory in real-time?
  - **How to verify**: Test Cheat Engine or similar tools
  - **Purpose**: Watch character width table, texture handles, etc.
  - **Tool**: Cheat Engine, x64dbg

- [ ] ❓ **Q9.2.2**: Can you capture frame-by-frame rendering output?
  - **How to verify**: Check if FFNx or OBS can dump frames
  - **Purpose**: Verify correct texture selection per character
  - **Tool**: FFNx save_textures setting, OBS

---

## SECTION 10: Critical Unknowns (Priority Questions)

These are the **MOST IMPORTANT** questions to answer first:

### 🔴 Priority 1: Encoding Format

**Question**: Does kernel.bin store Shift-JIS text, or does it already use FA-FE encoding?

**Why Critical**: Determines if you need to build a converter or just load textures

**How to Answer**: Extract kernel.bin section 10, look at raw bytes

---

### 🔴 Priority 2: FA-FE System Location

**Question**: Does FA-FE encoding exist in game files, in runtime memory, or is it FFNx-specific?

**Why Critical**: Determines where to hook conversion logic

**How to Answer**: Search FFNx source for FA/FB/FC/FD/FE constants

---

### 🔴 Priority 3: Width Table Coverage

**Question**: Is there ONE width table (256 entries) or SIX tables (1536 entries)?

**Why Critical**: Determines data structure design

**How to Answer**: Memory scan for width data structure size

---

### 🔴 Priority 4: FFNx Font System

**Question**: How does FFNx currently load and render fonts?

**Why Critical**: Determines modification strategy (extend vs. replace)

**How to Answer**: Read FFNx font loading code

---

### 🔴 Priority 5: Texture Format Compatibility

**Question**: Can FFNx load 1024×1024 RGBA PNGs directly, or does it need TEX format?

**Why Critical**: Determines asset preparation workflow

**How to Answer**: Test texture replacement with dummy PNG

---

## Implementation Strategy

Once these questions are answered:

1. **Document all findings** in a new `VERIFICATION_RESULTS.md` file
2. **Update Master Bible** with corrections where assumptions were wrong
3. **Create implementation plan** based on verified architecture
4. **Prioritize changes** by risk (low-risk texture replacement first, high-risk assembly hooks last)

---

## Notes

- **Keep Master Bible as reference** but treat as "hypothesis to verify"
- **This checklist is living document** - add questions as you discover new unknowns
- **Mark verification date** when completing each item
- **Include evidence** (screenshots, code snippets, hex dumps) for each verified item

---

## SECTION 11: AF3DN.P Reverse Engineering (NEW - HIGH PRIORITY)

### 11.1 AF3DN.P As Reference Implementation

**Context** (from IMPLEMENTATION_READINESS_ASSESSMENT.md):
> You have access to AF3DN.P (317KB custom driver) and ff7_ja.exe (Japanese executable). This is a working reference implementation by Square Enix/DotEmu.

**Questions to Answer:**

- [ ] ❓ **Q11.1.1**: What exported functions does AF3DN.P provide?
  - **How to verify**: Load in Ghidra, check Export Table
  - **Expected**: DirectX 9 wrapper functions, potentially custom text rendering
  - **Tool**: Ghidra, IDA Pro, or `objdump -x`

- [ ] ❓ **Q11.1.2**: How does AF3DN.P allocate texture slots for 6 font pages?
  - **How to verify**: Find `CreateTexture` or `D3DXCreateTexture` calls in disassembly
  - **Search for**: Loops allocating 6 textures instead of 1
  - **Tool**: Ghidra with DirectX 9 type library loaded

- [ ] ❓ **Q11.1.3**: Where does AF3DN.P hook the text rendering pipeline?
  - **How to verify**: Find function that processes FA-FE byte sequences
  - **Expected**: Hook in text parser before character rendering
  - **Tool**: Dynamic analysis with x64dbg + breakpoints

- [ ] ❓ **Q11.1.4**: Does AF3DN.P patch the width table, or use a separate table?
  - **How to verify**: Search for memory writes to 256-byte arrays
  - **Expected**: Either VirtualProtect + memcpy, or shadow table
  - **Tool**: x64dbg memory breakpoints

- [ ] ❓ **Q11.1.5**: How does AF3DN.P switch texture pages during rendering?
  - **How to verify**: Trace `SetTexture` calls during dialogue display
  - **Expected**: Texture bind call per character or per FA-FE marker
  - **Tool**: x64dbg with DirectX 9 API tracing

### 11.2 Dynamic Analysis Workflow

**Recommended Process:**

1. **Setup:**
   - Launch ff7_ja.exe (uses AF3DN.P)
   - Attach x64dbg to process
   - Set breakpoints on AF3DN.P exports

2. **Trigger Dialogue:**
   - Start new game
   - Reach first dialogue (opening scene)
   - Step through execution

3. **Capture Data:**
   - Dump texture allocation calls
   - Record memory addresses of width table
   - Trace FA-FE byte processing
   - Screenshot call stacks

4. **Document Findings:**
   - Create `AF3DN_REVERSE_ENGINEERING_RESULTS.md`
   - Include memory addresses with screenshots
   - Provide call graphs for key functions

**Priority:** 🔴 **CRITICAL** - This gives you the actual implementation instead of guessing

---

## SECTION 12: Build Environment Verification (NEW - CRITICAL)

### 12.1 Windows Build Prerequisites

**Context**: You have FFNx codebase on Windows machine

**Questions to Answer:**

- [ ] ❓ **Q12.1.1**: Which Visual Studio version does FFNx require?
  - **How to verify**: Check `.sln` file or `CMakeLists.txt` minimum version
  - **Expected**: VS 2019 or 2022
  - **Tool**: Text editor, read solution file header

- [ ] ❓ **Q12.1.2**: What CMake version is required?
  - **How to verify**: Check `cmake_minimum_required()` in CMakeLists.txt
  - **Tool**: Text editor, search for version requirement

- [ ] ❓ **Q12.1.3**: What Windows SDK version is needed?
  - **How to verify**: Check project properties or CMake config
  - **Expected**: Windows 10 SDK or later
  - **Tool**: Visual Studio installer, SDK list

- [ ] ❓ **Q12.1.4**: Are there any Git submodules to initialize?
  - **How to verify**: Check for `.gitmodules` file, run `git submodule status`
  - **Expected**: BGFX, possibly FFmpeg or other dependencies
  - **Tool**: `git submodule status`, file browser

### 12.2 Build Success Verification

- [ ] ❓ **Q12.2.1**: Can you build Debug configuration successfully?
  - **How to verify**: Run CMake + MSBuild, check for errors
  - **Command**: `cmake --build build --config Debug`
  - **Expected**: `FFNx.dll` produced in `build/Debug/`

- [ ] ❓ **Q12.2.2**: Can you build Release configuration successfully?
  - **How to verify**: Run CMake + MSBuild with Release config
  - **Command**: `cmake --build build --config Release`
  - **Expected**: Optimized `FFNx.dll` in `build/Release/`

- [ ] ❓ **Q12.2.3**: Does Debug build produce .pdb files for debugging?
  - **How to verify**: Check build output directory
  - **Expected**: `FFNx.pdb` alongside `FFNx.dll`
  - **Purpose**: Required for Visual Studio debugger attachment

**Priority:** 🔴 **CRITICAL** - Can't implement without ability to build

---

## SECTION 13: Test Environment Requirements (NEW - HIGH PRIORITY)

### 13.1 Isolated Test Installation

**Context**: User has "never done something like that before"

**Questions to Answer:**

- [ ] ❓ **Q13.1.1**: Where should the test FF7 installation be located?
  - **How to verify**: Choose path that won't conflict with main game
  - **Recommendation**: `C:\FF7_Test\` or similar
  - **Purpose**: Allows breaking things without affecting main install

- [ ] ❓ **Q13.1.2**: Can you copy your FF7 installation to a separate directory?
  - **How to verify**: Copy entire game folder, test if it runs
  - **Note**: May need to update registry keys or config files
  - **Tool**: xcopy, robocopy

- [ ] ❓ **Q13.1.3**: How do you switch between stock FFNx and dev build?
  - **How to verify**: Document DLL swap procedure
  - **Method**: Rename `FFNx.dll` → `FFNx.dll.backup`, copy dev build
  - **Rollback**: Restore backup if dev build crashes

### 13.2 Test Data Preparation

- [ ] ❓ **Q13.2.1**: How do you create test dialogue with FA-FE encoding?
  - **How to verify**: Write Python script to encode test strings
  - **Example**: "テスト" → FA XX FB YY (lookup in character_map.csv)
  - **Tool**: Custom encoding script

- [ ] ❓ **Q13.2.2**: Where do you inject test dialogue into the game?
  - **How to verify**: Find smallest dialogue file to modify (e.g., menu text)
  - **Recommendation**: Modify a single menu entry as proof-of-concept
  - **Tool**: kernel.bin editor, LGP repacker

- [ ] ❓ **Q13.2.3**: How do you capture baseline behavior (English mode)?
  - **How to verify**: Screenshot all menus, dump textures with FFNx
  - **Purpose**: Regression testing - ensure English still works
  - **Tool**: FFNx texture dumping, manual screenshots

**Priority:** 🔴 **CRITICAL** - Needed before Phase 1 implementation

---

## SECTION 14: Tool Chain Validation (NEW - MEDIUM PRIORITY)

### 14.1 Texture Conversion Tools

**Context** (from TOOL_GUIDE.md): Multiple tool options available

**Questions to Answer:**

- [ ] ❓ **Q14.1.1**: Which TEX converter do you have installed?
  - **Options**: Image2TEX (needs compilation), Tex Tools v1.0.4.7 (pre-compiled)
  - **Recommendation**: Use Tex Tools v1.0.4.7 (easier)
  - **How to verify**: Download, test TEX → PNG conversion

- [ ] ❓ **Q14.1.2**: Can Tex Tools handle 1024×1024 textures?
  - **How to verify**: Convert jafont_1.tex → PNG, check output dimensions
  - **Expected**: Should preserve full resolution
  - **Tool**: Tex Tools v1.0.4.7

- [ ] ❓ **Q14.1.3**: Does alpha channel survive TEX → PNG → TEX round-trip?
  - **How to verify**: Convert, re-convert, diff original with result
  - **Purpose**: Ensure no data loss in conversion process
  - **Tool**: Tex Tools + ImageMagick compare

### 14.2 Disassembly Tools

- [ ] ❓ **Q14.2.1**: Do you have Ghidra installed for AF3DN.P analysis?
  - **How to verify**: Download from https://ghidra-sre.org/
  - **Version**: Latest stable (10.x or 11.x)
  - **Tool**: Ghidra

- [ ] ❓ **Q14.2.2**: Do you have x64dbg for dynamic analysis?
  - **How to verify**: Download from https://x64dbg.com/
  - **Purpose**: Runtime tracing of AF3DN.P and ff7_ja.exe
  - **Tool**: x64dbg

**Priority:** ⚠️ **MEDIUM** - Needed for Phase 0, not Phase 1

---

## SECTION 15: Language Switching Architecture (NEW - PHASE 4)

### 15.1 Save/Load Persistence

**Context** (from user clarification):
> "I don't know how save load would affect the language state."

**Recommendation**: Store language preference globally, not in save files

**Questions to Answer:**

- [ ] ❓ **Q15.1.1**: Where does FFNx store persistent configuration?
  - **Options**: Registry, FFNx.toml, separate config file
  - **How to verify**: Check FFNx config saving code
  - **Tool**: Code search for file writes, registry writes

- [ ] ❓ **Q15.1.2**: Should language switch require game restart?
  - **MVP Answer**: Yes (simpler implementation)
  - **Future Answer**: No (hot-swap)
  - **How to verify**: Design decision, document trade-offs

- [ ] ❓ **Q15.1.3**: What happens if user loads save with different language?
  - **Expected Behavior**: Use global language setting, ignore save file
  - **How to verify**: Test scenario with saves from different languages
  - **Tool**: Manual testing

### 15.2 Mid-Dialogue Switching

**Context** (from user clarification):
> "If we switch languages, it just changes to the next language and starts rendering from the start again."

**Questions to Answer:**

- [ ] ❓ **Q15.2.1**: Can rendering be interrupted cleanly?
  - **How to verify**: Check FF7 text rendering state machine
  - **Expected**: Yes, dialogue can be cancelled/restarted
  - **Tool**: Code review of text rendering loop

- [ ] ❓ **Q15.2.2**: How do you reload text data without restarting game?
  - **How to verify**: Design file cache invalidation system
  - **Expected**: Clear cache, reload KERNEL_*.BIN from new language
  - **Tool**: Implementation design

**Priority:** 📋 **LOW** - Phase 4 feature, not MVP

---

## UPDATED: Priority Questions

### REVISED Priority Order (Based on New Information)

**🔴 Phase 0 Blockers (Must Answer First):**

1. **Build Environment** (Section 12) - Can't implement without builds
2. **AF3DN.P Analysis** (Section 11) - Provides all memory addresses + approach
3. **Test Environment** (Section 13) - Needed for validation
4. **Tool Chain** (Section 14) - Required for asset preparation

**🔴 Phase 1 Blockers (Answer Before Implementation):**

5. **Encoding Format** (Section 1, Priority 1) - Shift-JIS vs FA-FE
6. **FFNx Font System** (Section 4, Priority 4) - Current architecture
7. **Texture Format** (Section 3, Priority 5) - PNG vs TEX

**⚠️ Phase 2-3 (Answer During Implementation):**

8. **Width Table** (Section 2, Priority 3) - 256 vs 1536 entries
9. **FA-FE System Location** (Section 2, Priority 2) - File vs runtime
10. **Character Mapping** (Section 7) - Verify accuracy

**📋 Phase 4+ (Answer Later):**

11. **Language Switching** (Section 15) - Hot-swap architecture
12. **Edge Cases** - Battle text, minigames, FMV subtitles

---

**Next Action**:
1. Set up build environment on Windows machine (Section 12)
2. Reverse-engineer AF3DN.P (Section 11)
3. Create isolated test environment (Section 13)
4. Validate tool chain (Section 14)
5. Then start Section 1 questions

---

## SECTION 16: PR #737 Baseline Verification (CRITICAL UPDATE)

**Date Added:** 2025-11-25 01:30:00 JST (Tuesday)
**Session:** 37952f94-430d-46c5-8bed-8068cf9a7a62
**Status:** ✅ **ANALYSIS COMPLETE**

### 16.1 PR #737 Implementation Discovery

**Context:** Community member CosmosXIII created [PR #737](https://github.com/julianxhokaxhiu/FFNx/pull/737) implementing Japanese text rendering in FFNx.

**Status:** PR is OPEN (not merged) with 95% functionality complete

**Files Changed:** 17 files, +2,868 additions, -22 deletions

**Key Implementation File:** `src/ff7/japanese_text.cpp` (2,386 lines)

**What PR #737 Implements:**

- ✅ **FA-FE encoding system** - Identical to our Master Bible spec
- ✅ **Multi-page texture loading** - All 6 jafont textures loaded at init
- ✅ **Character width tables** - 1,536 values (6 pages × 256 chars) hardcoded
- ✅ **Function pointer hooking** - C++ hooks, no assembly required
- ✅ **Dynamic texture switching** - Mid-frame page selection works
- ✅ **Text box resizing** - Adjusts UI to fit Japanese characters
- ✅ **Compatible with ff7_ja.exe** - Auto-detects Japanese version

**What's Broken:**

- ❌ **Colored text rendering** - `[セーブ]` shows malformed (14 months unresolved)
- ❌ **Character name input screen** - Garbage in last 2 rows, missing tabs
- ❌ **Cursor alignment** - Hand doesn't align with text in menus

**References:**
- `PR737_ANALYSIS.md` - Complete code analysis (42,000 tokens)
- `ARCHITECTURAL_RETROSPECTIVE.md` - Why PR #737's approach is superior

---

### 16.2 Questions Answered by PR #737

Many verification questions are now **ANSWERED** by analyzing PR #737's code:

#### Section 2.1 - FA-FE Extended Page System

- ✅ **Q2.1.1**: FA-FE conversion happens in `field_submit_draw_text_640x480_6E706D_jp()` at line ~1010-1080
  - **Code:** C++ switch statement on `*buffer_text`
  - **Location:** `src/ff7/japanese_text.cpp:1024-1066`
  - **Evidence:** 
    ```cpp
    switch (*buffer_text) {
        case 0xFAu:
            graphics_object = ff7_externals.menu_jafont_2_graphics_object;
            charWidth = charWidthData[1][*buffer_text];
            break;
    }
    ```

- ✅ **Q2.1.2**: FFNx handles FA-FE, not original FF7.exe
  - **Method:** Pure C++ function pointer interception
  - **No assembly hooks required**
  - **Evidence:** PR #737 changes `draw_graphics_object` from `uint32_t` to function pointer

- ✅ **Q2.1.3**: Lookup table is `charWidthData[6][256]` at line 309-477
  - **Format:** Hardcoded C++ array
  - **Size:** 1,536 int values
  - **Evidence:** Visible in PR diff lines 309-477

#### Section 2.2 - Character Width Table

- ✅ **Q2.2.2**: SIX width tables (1,536 entries total)
  - **Structure:** `int charWidthData[6][256]`
  - **Evidence:** Array declaration in japanese_text.cpp

- ✅ **Q2.2.3**: Width table is hardcoded in C++, NOT loaded from file
  - **Reason:** Simplicity, no file I/O, immediate availability
  - **Trade-off:** Must recompile to change widths (but works)

- ✅ **Q2.2.4**: Proportional spacing (widths vary 20-32 pixels)
  - **Evidence:** 
    ```cpp
    { 30, 30, 28, 31, 30, 30, 29, 29, ... }  // Varying values
    ```

#### Section 3.1 - jafont_*.tex Format

- ✅ **Q3.1.X**: PR #737 loads **TIM format**, not TEX
  - **Files:** `jafont_1.tim` through `jafont_6.tim`
  - **Loader:** `engine_load_graphics_object_6710AC()`
  - **Evidence:** PR diff line 593-633

#### Section 4.1 - Font System Implementation

- ✅ **Q4.1.1**: `src/ff7/font.cpp` does NOT exist
  - **Alternative:** Created `src/ff7/japanese_text.cpp` instead
  - **Reason:** Self-contained Japanese-specific module

- ✅ **Q4.1.2**: Text rendering handled by `field_submit_draw_text_640x480_6E706D_jp()`
  - **Function signature:** `__int16 field_submit_draw_text_640x480_6E706D_jp(__int16 character_x, __int16 character_y, ...)`
  - **Location:** `src/ff7/japanese_text.cpp:515+`

- ✅ **Q4.1.3**: Texture loading via `engine_load_graphics_object_6710AC()`
  - **Parameters:** `(int type, int size, struc_3* config, const char* filename, int dx_context)`
  - **Evidence:** PR diff shows 6 sequential calls loading jafont_1-6.tim

- ✅ **Q4.1.4**: Multi-texture support via 6 global pointers
  - **Variables:**
    ```cpp
    ff7_externals.menu_jafont_1_graphics_object
    ff7_externals.menu_jafont_2_graphics_object
    // ... through jafont_6
    ```
  - **Selection:** C++ switch statement selects correct pointer

#### Section 4.2 - Configuration System

- ✅ **Q4.2.1**: `ff7_japanese_edition` config flag exists
  - **File:** `misc/FFNx.toml` line 697
  - **Auto-detection:** Enabled when `ff7_ja.exe` detected
  - **Evidence:** 
    ```toml
    ff7_japanese_edition = false  # Auto-enabled for Japanese exe
    ```

- ⚠️ **Q4.2.2**: Font config options remain limited
  - **Existing:** Only `ff7_japanese_edition` flag
  - **Missing:** No `font_language`, `font_path`, etc.
  - **Future need:** Multi-language support requires config expansion

- ✅ **Q4.2.3**: Texture override path is `mods/Textures/`
  - **Confirmed:** Standard FFNx texture replacement path
  - **Evidence:** Session 11 verification findings

#### Section 4.3 - Renderer Integration

- ✅ **Q4.3.1**: BGFX multi-backend (verified in Session 11)
  - **Backends:** DirectX 11/12, Vulkan, OpenGL
  - **Evidence:** Session 11 findings document

- ✅ **Q4.3.2**: Texture binding via `graphics_object` pointer assignment
  - **Method:** 
    ```cpp
    graphics_object = ff7_externals.menu_jafont_N_graphics_object;
    // Then draw call uses graphics_object automatically
    ```

- ✅ **Q4.3.3**: Mid-frame texture switching **WORKS** (already implemented)
  - **Evidence:** PR #737 switches texture per FA-FE marker
  - **Performance:** No issues reported in 14 months of testing

---

### 16.3 Remaining Questions (NOT Answered by PR #737)

#### Critical for Phase 1.5 (Bug Fixes)

- [ ] ❓ **Q16.3.1**: Why is colored text rendering broken?
  - **Hypothesis A:** Colored texture variants (jafont_1_red.tim) missing
  - **Hypothesis B:** Color tinting logic doesn't work with non-white base
  - **How to verify:** Inspect `get_character_color()` function logic
  - **Tool:** Debugger attached to Japanese game

- [ ] ❓ **Q16.3.2**: Why is character name input screen corrupted?
  - **Symptom:** Last 2 rows show garbage, missing Katakana/Romaji tabs
  - **How to verify:** Debug character selection rendering code
  - **Tool:** Visual Studio debugger + name input screen

- [ ] ❓ **Q16.3.3**: What causes cursor alignment offset?
  - **Hypothesis:** Cursor code assumes fixed 16px width
  - **How to verify:** Find cursor position calculation, check if uses `charWidthData`
  - **Tool:** Code search for cursor rendering

#### Critical for Phase 2 (Multi-Language)

- [ ] ❓ **Q16.3.4**: Where are FR/DE/ES fonts stored in Japanese eStore version?
  - **Expected paths:**
    - `lang-fr/menu_fr.lgp` → frfont_1-6.tim
    - `lang-de/menu_de.lgp` → defont_1-6.tim
    - `lang-es/menu_es.lgp` → esfont_1-6.tim
  - **How to verify:** Extract LGP files, list contents
  - **Tool:** LGP extractor

- [ ] ❓ **Q16.3.5**: Do FR/DE/ES use same FA-FE encoding or different?
  - **How to verify:** Analyze FR/DE/ES kernel.bin text sections
  - **Tool:** Hex editor, compare byte patterns

- [ ] ❓ **Q16.3.6**: How to add language toggle hotkey to FFNx?
  - **How to verify:** Find keyboard input handler in FFNx source
  - **Search for:** `VK_F9`, keyboard event processing
  - **Tool:** Code search in FFNx repo

#### Critical for Phase 3 (Furigana)

- [ ] ❓ **Q16.3.7**: Can text rendering handle dual-layer (kanji + furigana)?
  - **How to verify:** Analyze text rendering architecture for multi-pass support
  - **Tool:** Code review of rendering pipeline

- [ ] ❓ **Q16.3.8**: How to adjust line heights for furigana space?
  - **How to verify:** Find line height calculation in dialogue rendering
  - **Tool:** Code search for line spacing, vertical positioning

---

### 16.4 PR #737 Architecture Analysis Summary

**Comparison: Our Original Spec vs PR #737**

| Component | Our Spec (Master Bible) | PR #737 (Actual) | Assessment |
|-----------|-------------------------|------------------|------------|
| **FA-FE Encoding** | ✅ Specified | ✅ Implemented | IDENTICAL - validates our spec |
| **Texture Loading** | Multi-page (6 textures) | Multi-page (6 textures) | IDENTICAL |
| **Hook Method** | Assembly via Hext | C++ function pointers | PR #737 BETTER - maintainable |
| **Width Tables** | Memory patch @ 0x99DDA8 | Hardcoded arrays | PR #737 SIMPLER - safer |
| **Texture Format** | PNG/TEX | TIM | MINOR - both work |
| **Page Selection** | `g_currentFontPage` global | `graphics_object` pointer | PR #737 CLEANER - direct |

**Key Insights:**

1. **We were RIGHT about FA-FE encoding** - PR #737 validates this approach
2. **We were WRONG about assembly hooks** - C++ function pointers are superior
3. **We were WRONG about memory patching** - hardcoded arrays are simpler/safer
4. **Our research wasn't wasted** - it VALIDATED PR #737's architecture

**Strategic Conclusion:**

- ✅ **Use PR #737 as baseline** - 95% complete, battle-tested
- ✅ **Fix PR #737's bugs** - colored text, input screen, cursor (Phase 1.5)
- ✅ **Extend PR #737** - add multi-language, furigana (Phases 2-3)
- ✅ **Preserve our research** - character mapping enables translation tools

---

### 16.5 Updated Priority Order

**REVISED Priority Questions (Post-PR #737 Discovery):**

### 🔴 Phase 1.5 Blockers (MUST Answer to Fix Bugs)

1. **Colored Text Root Cause** (Q16.3.1)
   - Where are colored texture variants?
   - Why does `get_character_color()` fail?

2. **Character Input Bug** (Q16.3.2)
   - Why are last 2 rows garbage?
   - Where is character selection rendering code?

3. **Cursor Alignment** (Q16.3.3)
   - Where is cursor position calculated?
   - Does it use fixed 16px assumption?

### 🔴 Phase 2 Blockers (MUST Answer for Multi-Language)

4. **FR/DE/ES Font Locations** (Q16.3.4)
5. **Multi-Language Encoding** (Q16.3.5)
6. **Hotkey System Integration** (Q16.3.6)

### ⚠️ Phase 3 (Can Answer During Implementation)

7. **Dual-Layer Text Rendering** (Q16.3.7)
8. **Line Height Adjustment** (Q16.3.8)

### 📋 Lower Priority (Answer Later)

9. **Character Mapping Validation** (Section 7)
10. **AF3DN.P Reverse Engineering** (Section 11) - Less critical now
11. **Edge Cases** - Battle text, minigames, FMV subtitles

---

## Implementation Strategy Update

**Old Strategy (Pre-PR #737):**
1. Reverse-engineer AF3DN.P
2. Implement FA-FE system from scratch
3. Create assembly hooks via Hext
4. Patch memory width table
5. Test everything

**Estimated Time:** 5-8 months

---

**New Strategy (Post-PR #737):**
1. **Phase 1.5:** Fix PR #737 bugs (3-4 weeks)
2. **Phase 2:** Extend to multi-language (2-3 weeks)
3. **Phase 3:** Add furigana (3-6 weeks)
4. **Phase 5:** Polish and release (3-4 weeks)

**Estimated Time:** 2.5-4 months (50-60% time savings)

---

## Success Criteria (Updated)

### Phase 1.5 Complete When:
- [ ] Colored text renders correctly (screenshots prove it)
- [ ] Character name input shows correct glyphs
- [ ] Cursor aligns with text in all menus
- [ ] PR #737 approved and merged by FFNx maintainer

### Phase 2 Complete When:
- [ ] Can toggle between EN/JA/FR/DE/ES during gameplay
- [ ] All 5 languages render without errors
- [ ] Language preference persists across game restarts

### Phase 3 Complete When:
- [ ] Furigana displays above kanji
- [ ] Toggle on/off works seamlessly
- [ ] No text overflow or layout breaks

---

**Next Actions:**

1. ☐ Set up PR #737 fork locally
2. ☐ Build PR #737 branch
3. ☐ Launch Japanese game with PR #737 build
4. ☐ Reproduce colored text bug
5. ☐ Debug `get_character_color()` to find root cause
6. ☐ Implement fix
7. ☐ Submit patch to PR #737

---

## SECTION 17: PR #737 Bug Investigation (PHASE 1.5)

**Date Added:** 2025-11-25 12:00:00 JST (Tuesday)
**Session:** 451ac988-eb41-4d5b-aa56-6c2d6127f213
**Purpose:** Detailed investigation questions for fixing PR #737's known bugs

---

### 17.1 Colored Text Rendering Bug

**Symptom:** `[セーブ]` and other colored menu text renders incorrectly/malformed

- [ ] ❓ **Q17.1.1**: What does `get_character_color()` return for Japanese text?
  - **File:** `src/ff7/japanese_text.cpp`
  - **How to verify:** Add `ffnx_trace()` logging, capture return values during colored text display
  - **Expected values:** BGRA color struct for each n_shape value

- [ ] ❓ **Q17.1.2**: Are colored texture variants (jafont_X_red.tim, jafont_X_blue.tim) expected to exist?
  - **How to verify:** Check original Japanese game files in `menu_ja.lgp`
  - **Alternative hypothesis:** English uses white base + tint, Japanese has pre-colored glyphs

- [ ] ❓ **Q17.1.3**: Is the color tinting approach multiplying RGB against non-white base?
  - **Hypothesis:** Japanese fonts have embedded colors (not white), so tinting produces wrong result
  - **How to verify:** Inspect jafont_*.tim pixel values - are glyphs white or colored?
  - **Tool:** Debugger + texture memory inspection, or export TIM to PNG and check

---

### 17.2 Character Name Input Screen Bug

**Symptom:** Last 2 rows show garbage characters, Katakana/Romaji tabs missing

- [ ] ❓ **Q17.2.1**: Which function renders the character selection grid?
  - **How to verify:** Set breakpoints in PR #737 code, trigger name input screen
  - **Search:** "name", "character", "input", "select" in `japanese_text.cpp`

- [ ] ❓ **Q17.2.2**: Why are only the last 2 rows corrupted?
  - **Hypothesis A:** Array bounds issue (loop goes 0-13 rows, but only 12 exist)
  - **Hypothesis B:** Page marker decoding fails for certain character ranges
  - **How to verify:** Memory inspection during rendering, check loop bounds

- [ ] ❓ **Q17.2.3**: Where are Katakana/Romaji tab graphics defined?
  - **How to verify:** Find UI element definitions, check if hardcoded or loaded from assets
  - **Related:** Tabs may use different texture or rendering path than main grid

---

### 17.3 Cursor Alignment Bug

**Symptom:** Hand cursor doesn't align with menu text (offset to left/right)

- [ ] ❓ **Q17.3.1**: Where is cursor X position calculated?
  - **Search:** "cursor", "hand", "selection", "menu_x" in FFNx source
  - **Expected:** Some function computes cursor_x = base_x + (char_width * char_count)

- [ ] ❓ **Q17.3.2**: Does cursor code use `charWidthData[]` or assume fixed 16px?
  - **How to verify:** Code review of cursor positioning logic
  - **Hypothesis:** Original English code assumed fixed 16px width, Japanese varies 20-32px

- [ ] ❓ **Q17.3.3**: Is this a per-character accumulation error or constant offset?
  - **How to verify:** Test cursor alignment on short vs long menu items
  - **If accumulation:** Error grows with text length
  - **If constant:** Same offset regardless of text length

---

### 17.4 Investigation Workflow

**Recommended Debug Approach:**

1. **Set Up Environment:**
   - Clone PR #737 branch
   - Build Debug configuration (with .pdb symbols)
   - Attach Visual Studio debugger to ff7_ja.exe

2. **For Each Bug:**
   - Reproduce the issue
   - Add logging (`ffnx_trace()`) to suspected functions
   - Set breakpoints at key decision points
   - Capture variable values at time of failure
   - Document findings in this checklist

3. **Document Findings:**
   - Mark questions as ✅ Verified with evidence
   - Update hypotheses based on discoveries
   - Add new questions if investigation reveals new unknowns

---

**End of Section 17**
