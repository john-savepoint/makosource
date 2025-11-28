# Comparison: FF7_Kernel.md vs 03_KERNEL.md

## File Sizes and Structure

- **Individual file (FF7_Kernel.md)**: 10 lines
- **Major section (03_KERNEL.md)**: 1,641 lines
- **Size ratio**: Major section is ~164x larger

## Overview

The individual `FF7_Kernel.md` file is essentially a table of contents / stub document that links to external sections. The `03_KERNEL.md` file is the comprehensive, fully-detailed kernel documentation containing all the actual content referenced in the stub.

## Topics Covered in BOTH Files

1. **Kernel Overview**
2. **Memory Management**
3. **Kernel.bin** (Game resource data)
4. **Low Level Libraries**

## Content ONLY in Individual File (FF7_Kernel.md)

**None - this file contains only structural links**

The file (lines 1-10) consists of:
- A title header (`# FF7/Kernel`)
- A table of contents marker
- Four wikilinks pointing to external pages:
  - `FF7/Kernel/Overview`
  - `FF7/Kernel/Memory_management`
  - `FF7/Kernel/Kernel.bin`
  - `FF7/Kernel/Low_level_libraries`

This appears to be a converted wiki stub that originally linked to separate wiki pages.

## Comprehensive Content ONLY in Major Section (03_KERNEL.md)

### I. Kernel Overview (Lines 3-26)
- **1.1 History**: Detailed explanation of kernel concept from FF1 NES through FF7, memory banking history (MMC1 controller, 16K sections), original kernel design
- **1.2 Kernel Functionality**: Multitasking threaded program, software memory manager, Psy-Q libraries, module-to-module transitions, comparison with PSX BIOS

### II. Memory Management (Lines 27-78)
- **1.1 RAM Management** (lines 29-48):
  - Save Map structure (4,340 bytes / 0x10F4)
  - 5 banks of field-accessible memory
  - Field script banks 1-5 with offsets and 8-bit/16-bit field bank mappings
  - Temporary field variables (256 bytes)
  - Memory allocation table with specific offsets

- **1.2 VRAM Management** (lines 49-72):
  - PSX video memory model (2048x512 pixels)
  - Color depth visualization concepts
  - VRAM layout during gameplay with visual reference images
  - Detailed VRAM schematic with texture boundaries
  - Frame buffers, V-sync requirements
  - 24-bit movie mode VRAM usage
  - CLUT (Color Look Up Tables) storage and positioning
  - Texture cache hierarchy and volatility
  - Permanent menu textures and font storage

- **1.3 PSX CD-ROM Management** (lines 73-78):
  - BIOS hardware access restrictions
  - Module transition preloading strategy
  - CD-ROM quick mode access (8 KB at a time)
  - Sector-based file references

### III. Game Resources (Lines 79-548)

#### 1.1 The KERNEL.BIN Archive (Lines 88-543)
- **File location mapping**: PSX vs PC versions
- **Complete section table** (Lines 94-123): 27 sections with data types and byte offsets
  - Sections 1-9: Binary data (Command, Attack, Savemap, Stats, Item, Weapon, Armor, Accessory, Materia)
  - Sections 10-27: Text files (Descriptions, Names, Battle text, Summon attacks)

- **Section Formats & Specifications**:
  - **Section 1: Command data** (lines 128-145): 16-byte record format (empty table structure provided)
  - **Section 2: Attacks data** (lines 146-189): 28-byte record format with detailed field breakdown:
    - Casting cost (1 byte at 0x04)
    - Attack type (1 byte at 0x0A)
    - Attack attributes (2 bytes at 0x0B) with 20+ attribute types listed (Escape/Exit, Ribbon-Like, Enemy Skill, Restorative, Status-giving, Shield, Limit Break, Summon, Roulette, etc.)
    - ID Number, Restore data, Strength, Restore type (HP/MP/Ailment)
    - Times attacking, Statuses, Element
  - **Section 3: Savemap** (lines 190-192): Initial values and structure (0x0054 to 0x0fe7)
  - **Section 4: Initialization data** (lines 194-196): Starting stats for characters
  - **Section 5: Item data format** (lines 198-251): 27-byte record format with fields (incomplete, requires reading lines 198-251)
  - **Section 6: Weapon data format** (lines 252-335): Item type, rarity, attack power, attack accuracy, critical hit chance, physical damage formula, element attribute, bonus attributes, special abilities, model ID, various cost and stat modifiers
  - **Section 7: Armor data format** (lines 336-399): Defense value, magic defense, evade rate, magic evade, physical damage reduction, elemental properties, status immunity, growth boost, model ID
  - **Section 8: Accessory data format** (lines 400-490): Accessory-specific attributes and bonuses
  - **Section 9: Materia data format** (lines 491-544): Materia type, compatibility, stat changes, ability lists, growth rates

#### 2.1 The KERNEL2.BIN Archive (Lines 545-548)
- Location: PC version only (/DATA/KERNEL/KERNEL2.BIN)
- Brief reference, limited details

### IV. Low Level Libraries (Lines 549-1641)

#### 1. PC to PSX Comparison (Lines 551-560)
- Overview of platform differences

#### 1.1 DATA ARCHIVES (Lines 561-745)

- **1.1.1 BIN Archive Data Format** (Lines 565-591):
  - BIN Types: Standard BIN, GZIP BIN, LZS Compressed
  - BIN-GZIP Types: Four type variants with header structure and compression details
  - Header format specification

- **1.1.2 LZS Compressed Archive for PSX** (Lines 592-665):
  - Format specification
  - LZS compression algorithm details
  - Reference format with byte-level breakdown
  - Examples of compressed data with annotations
  - Complications and edge cases

- **1.1.3 LGP Archive Format for PC by Ficedula** (Lines 666-745):
  - Complete file structure specification
  - Section 1: File header (27 bytes with field breakdown)
  - Section 2: CRC Code
  - Section 3: Actual data
  - Section 4: Terminator
  - Detailed notes on implementation

#### 2. TEXTURES (Lines 746-865)

- **2.1 TIM Texture Data Format for PSX** (Lines 750-846):
  - **2.1.1 Basic Terms** (lines 756-769):
    - CLUT (Color Look Up Table) definition
    - VRAM Location concepts
    - CLUT Location positioning
  - **2.1.2 TIM File Format** (lines 770-846):
    - 4 Bits Per Pixel (4bpp) format details
    - 8 Bits Per Pixel (8bpp) format details
    - 16 Bits Per Pixel (16bpp) format details
    - Header structures and data layouts for each color depth

- **2.2 TEX Texture Data Format for PC by Mirix** (Lines 847-865):
  - PC texture format specification

#### 3. File Formats for 3D Models (Lines 866-1641)

- **3.1 Model Formats for PSX** (Lines 872-875)
  - Reference to PSX model specifications

- **3.2 Model Formats for PC** (Lines 876-1641):

  - **3.2.1 HRC Hierarchy Data Format** (Lines 880-971):
    - Hierarchy file structure for skeletal/bone data
    - Format sections: Preamble, Header, Bones, Notes
    - Header structure details
    - Bone hierarchy specification with animation support
    - Implementation notes

  - **3.2.2 RSD Resource Data Format** (Lines 972-1032):
    - SGI RSD fileset library reference
    - Texture file references
    - Output file specifications

  - **3.2.3 "P" Polygon File Format** (Lines 1033-1641):
    - Comprehensive 3D model polygon format by Alhexx
    - **1.1 .P File Header** (lines 1080-1137):
      - Header fields and their meanings
      - 12-byte header structure with field descriptions

    - **P File Construction** (lines 1141-1480):
      - **1.2 Vertex Chunk**: Vertex position data specification
      - **1.3 Normals Chunk**: Surface normal data
      - **1.4 Texture Coordinate Chunk**: UV mapping data with C/C++ struct
      - **1.5 Vertex Color Chunk**: Per-vertex color information
      - **1.6 Polygon Color Chunk**: Per-polygon color attributes
      - **1.7 Edge Chunk**: Edge visibility/properties with C/C++ struct
      - **1.8 Polygon Chunk**: Polygon face definitions with tag information
      - **1.9 Hundrets Chunk**: Hundred-polygon grouping (lines 1268-1320)
      - **1.10 Group Chunk**: Polygon grouping specifications (lines 1321-1430)
      - **1.11 BoundingBox**: Bounding volume specification
      - **1.12 Normal Index Table**: Normal-to-vertex mapping

    - **2. GROUPING** (lines 1482-1641):
      - **2.1 General grouping concepts** (lines 1488-1567)
      - Detailed step-by-step process:
        - STEP 1: Initial grouping setup (lines 1494-1522)
        - STEP 2: Group definition (lines 1523-1541)
        - STEP 3: Further grouping (lines 1542-1559)
        - STEP 4: Group types with DOT-Group, TILDE-Group, and ABSOLUTE INDICES (lines 1560-1617)
        - STEP 5: Final grouping steps (lines 1618-1629)
      - Implementation notes and important considerations (lines 1630-1641)

## Significant Differences

### Content Depth
- **Individual file**: 10 lines - structure only (wikilinks with no content)
- **Major section**: 1,641 lines - fully detailed specifications, formulas, binary data layouts, tables

### Knowledge Transfer
- **Individual file**: Presupposes reader has access to external wiki pages
- **Major section**: Completely self-contained reference documentation

### Technical Detail Level
- **Individual file**: None (stub document)
- **Major section**:
  - Byte-level specifications with offset and length tables
  - C/C++ struct definitions
  - Hexadecimal values and encoding examples
  - Visual diagrams (VRAM layout, structure visualizations)
  - Step-by-step algorithm explanations
  - Compression algorithm details

### Scope
- **Individual file**: High-level topic listing only
- **Major section**:
  - Complete kernel architecture
  - Memory models (RAM, VRAM, CD-ROM)
  - All 27 sections of KERNEL.BIN with full specifications
  - Archive format specifications (BIN, LZS, LGP)
  - Texture formats (TIM, TEX) with color depth variations
  - 3D model formats (HRC, RSD, P) with detailed chunk specifications

## Recommendations

- [ ] **Archive obsolete stub file**: FF7_Kernel.md appears to be a converted wiki index. Consider archiving or removing it, as it serves no purpose now that the comprehensive 03_KERNEL.md exists
- [ ] **Update internal links**: Search the codebase for any references to the old wikilinks (e.g., `FF7/Kernel/Overview`) and update them to point to sections in 03_KERNEL.md
- [ ] **Consider consolidation**: 03_KERNEL.md is the authoritative source for all kernel-related documentation
- [ ] **Add table of contents**: Consider adding a markdown table of contents to 03_KERNEL.md to improve navigation given its 1,641 line length
- [ ] **Version control**: The stub file may have been accidentally committed from the wiki conversion process. Check git history to determine if this is intentional
- [ ] **Cross-reference cleanup**: Verify all KERNEL2.BIN references are properly documented or flag as incomplete (lines 545-548 show minimal detail)

## Summary

**FF7_Kernel.md is a structural stub** linking to four main topics. **03_KERNEL.md is the complete, comprehensive source documentation** containing all technical details for those four topics. There is no content duplication or conflict—the stub file is simply superseded by the major section file. The individual file appears to be a legacy artifact from wiki conversion and should be consolidated with or removed in favor of the complete 03_KERNEL.md.
