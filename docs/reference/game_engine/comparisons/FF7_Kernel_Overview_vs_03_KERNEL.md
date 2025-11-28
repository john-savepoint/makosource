# Comparison: FF7_Kernel_Overview.md vs 03_KERNEL.md

## File Sizes

- **Individual file:** FF7_Kernel_Overview.md = 33 lines
- **Major section:** 03_KERNEL.md = 1641 lines
- **Size ratio:** 03_KERNEL.md is ~50x larger

---

## Topics Covered in BOTH Files

These sections appear in identical or nearly identical form in both files:

1. **History** (Lines 9-19 in FF7_Kernel_Overview.md / Lines 5-13 in 03_KERNEL.md)
   - Origin as throwback to FF1 NES kernel concept
   - Memory mapper and banking system explanation
   - MMC1 controller details (16K sections, 256K max)
   - FF1 kernel in bottom 16K of memory
   - Main program loop functions
   - Evolution across Final Fantasy franchise
   - FF6 → PSX → PC port examples

2. **Kernel Functionality** (Lines 21-33 in FF7_Kernel_Overview.md / Lines 15-25 in 03_KERNEL.md)
   - Kernel as threaded multitasking program
   - Memory manager for RAM and video memory
   - Psy-Q libraries integration
   - PC port equivalents (SEQ to MIDI replacement)
   - Kernel hierarchy diagram (User → Module → Kernel → Psy-Q → BIOS → Hardware)

---

## Content ONLY in Individual File (FF7_Kernel_Overview.md)

The individual file is an extremely condensed overview containing:

1. **Table of Contents** (Lines 3-5)
   - Simple anchor links to main sections

2. **Kernel table diagram reference** (Line 25)
   - Image reference: `Kernel_table.png`
   - Associated embedded image in "Images" section (Line 32)

3. **Minimal scope**
   - Only covers the two main sections: History and Kernel Functionality
   - No technical data formats, no archive specifications, no deep implementation details
   - Functions as a high-level introduction/overview only

---

## Content ONLY in Major Section (03_KERNEL.md)

The major section file contains extensive technical documentation organized into major sections:

### **II. Memory Management** (Lines 27-77)

1. **RAM Management** (Lines 29-47)
   - Save Map structure (4,340 bytes / 0x10F4)
   - 5 banks of field script memory (8-bit and 16-bit accessible)
   - Offset mappings for banks 0x1-0xF
   - Temporary field variables (256 bytes)
   - Detailed memory map table

2. **VRAM Management** (Lines 49-71)
   - PSX VRAM characteristics (1 megabyte, 2048x512 pixels)
   - VRAM visualization as 1024x512 matrix
   - Video buffer and back buffer layout
   - Field graphics caching
   - CLUT (Color Look Up Table) positioning
   - Permanent and semi-permanent texture storage
   - V-sync blank areas
   - Texture cache boundaries and volatility ordering

3. **PSX CD-ROM Management** (Lines 73-77)
   - Direct hardware access prohibition
   - Preloading strategy during module transitions
   - BIOS call limitations
   - Quick mode CD-ROM access (8KB blocks)
   - Sector-based file referencing

### **III. Game Resources** (Lines 79-544)

1. **KERNEL.BIN Archive** (Lines 88-192)
   - 27 gzip-compressed sections concatenated
   - 6-byte header format
   - 27 file sections with complete offset and content documentation:
     - Sections 1-9: Command, Attack, Savemap, Character stats, Item, Weapon, Armor, Accessory, Materia data
     - Sections 10-27: Text descriptions and names for all game objects
   - Detailed table of all section offsets

2. **KERNEL.BIN Section Formats** (Lines 124-544)
   - **Section 1: Command Data** - 16 bytes per record
   - **Section 2: Attack Data** - 28 bytes per record with detailed field mapping:
     - Casting cost, Attack type, Attack attribute flags (0x0000-0xFF17)
     - Restoration type, Status effects, Elements, Duration
   - **Section 3: Savemap** - Initial values and structure (0x0054 to 0x0fe7)
   - **Section 4: Character Starting Stats** - Character initialization data
   - **Section 5: Item Data** - 27 bytes per record
     - Restriction mask (0xFF-0xF9 variants)
     - Attack target types (0x01, 0x03, 0x05, 0x07, 0x10)
     - Restoration types and multipliers
     - Status effects and elements
   - **Section 6: Weapon Data** - 44 bytes per weapon record
     - Weapon range, attack modifiers, special options
     - 8 special option types (0x11, 0xA0-0xA8) with complex formulas
     - Attack percentages, Materia growth rates, Weapon model IDs
     - Equip masks for 10 characters
     - Attack types, Stat increases, Materia slot configurations
     - Restriction masks
   - **Section 7: Armor Data** - 36 bytes per armor record
     - Damage type (Absorb, No Damage, Half)
     - Defense, Magic Defense, percentage modifiers
     - Materia slots, Growth rates
     - Equip masks (Everyone, All Females, All Males)
     - Element protection, Stat bonuses
     - Restriction masks
   - **Section 8: Accessory Data** - 16 bytes per accessory record
     - Stat bonuses (STR, VIT, MAG, SPR, DEX, LCK)
     - Bonus amount, Elemental effects
     - Special effects (Haste, Fury, Curse Ring, Reflect, etc.)
     - Elemental immunity (8 types + Holy)
     - Status protection (Death, Near Death, Sleep, Poison, etc.)
     - Equip masks (10 characters)
     - Restriction masks
   - **Section 9: Materia Data** - 20 bytes per materia record
     - Level-up AP limits (4x WORD)
     - Equip effects with stat modification table
     - Status bitmasks, Element type
     - Materia type (0x00-0x57) with 13 different type codes
     - Materia attributes for spell/command availability

3. **KERNEL2.BIN Archive** (Lines 545-547)
   - Secondary kernel archive for PC version only
   - Sections 10-27 (text data) only
   - Ungzipped, concatenated, then LZS compressed
   - 4-byte header with file length

### **IV. Low Level Libraries** (Lines 549-1641)

1. **PC to PSX Comparison** (Lines 551-559)
   - Original PSX FF7 using Psy-Q development library
   - TIM files (PSX) vs TEX files (PC)
   - Conversion challenges (artwork availability)
   - Archive format differences

2. **Data Archives** (Lines 561-733)
   - **BIN Archive Types:**
     - Uncompressed: 4-byte header + data
     - BIN-GZIP: 6-byte header + multiple gzipped sections
     - Header structure details (length, unknown, file number)
   - **LZS Compression** (Lines 592-664)
     - Modified LZSS compression algorithm
     - Control byte scheme
     - Literal data and reference structure
     - 12-bit offset and 4-bit length encoding
     - Reference calculation formula
     - Detailed example (offset/length calculation from position 1000)
     - Edge cases (negative offsets, repeated runs)
   - **LGP Archive Format** (Lines 666-736)
     - 4 sections: File header/TOC, CRC code, Data, Terminator
     - Creator string (12 bytes, "SQUARESOFT")
     - File count integer
     - TOC entries: 20-byte filename, 4-byte offset, 1 byte attributes, 2-byte duplicate indicator
     - CRC validation (3602 bytes, based on file count)
     - Data section with embedded file headers
     - Terminator string ("FINAL FANTASY 7")
     - Flexibility and quirks (filename mismatch, data linking, unused data)
     - LGP Editor tools and workarounds

3. **Textures** (Lines 746-865)
   - **TIM Format (PSX)** (Lines 750-845)
     - Native Psy-Q format, clean VRAM loading
     - CLUT (Color Look Up Table) concept
     - VRAM location positioning
     - 4-bit per pixel format (16 colors) with full structure
     - 8-bit per pixel format (256 colors) with full structure
     - 16-bit per pixel format (BGR with mask bit, RGB555)
   - **TEX Format (PC)** (Lines 847-864)
     - 56-byte header unknown section
     - Bit depth (4, 8, or 16)
     - Image dimensions
     - Palette entries (20-byte unknown, 144-byte unknown sections)
     - BGRA color palette (4 bytes per color)
     - Bitmap data (varies by bit depth)

4. **3D Model Formats** (Lines 866-1641+)
   - **General 3D Model Overview** (Lines 866-870)
   - **PSX Model Formats** (Lines 872-874) - Lorem ipsum placeholder
   - **PC Model Formats** (Lines 876-878)
   - **HRC Hierarchy Data Format** (Lines 880-970)
     - Plain text skeleton definition files
     - Header block identification
     - Skeleton name declaration
     - Bone count and listing
     - Bone structure: name, parent, length, RSD file count
   - **RSD Resource Data Format** (Lines 972-1031)
     - Plain text resource definition
     - ID line (@RSD940102)
     - Comments (# prefix ignored)
     - Polygon file (PLY), Material file (MAT), Group file (GRP)
     - Texture count (NTEX) and listing with TIM→TEX conversion
   - **P Polygon File Format** (Lines 1033-1498+)
     - Comprehensive 11-section file structure
     - 128-byte header with 16+ field specifications
     - Vertex chunk (NumVerts * 12 bytes, XYZ floats)
     - Normal chunk (NumNormals * 12 bytes)
     - Texture coordinate chunk (NumTexCs * 8 bytes, XY floats)
     - Vertex color chunk (NumVerts * 4 bytes, BGRA)
     - Polygon color chunk (NumPolys * 4 bytes, BGRA)
     - Edge chunk (NumEdges * 4 bytes, wireframe data)
     - Polygon chunk (NumPolys * 24 bytes with tag/vertex/normal/edge data)
     - Hundrets chunk (mirex-h * 100 bytes, texture-related)
     - Group chunk (NumGroups * 56 bytes, model subdivision)
     - Bounding box (24 bytes, min/max XYZ)
     - Normal index table (NumNormInds * 4 bytes)
     - Group type specification (non-textured, textured with/without normals)
     - Detailed group structure with polygon/vertex/edge/texture mappings
     - Field character grouping methodology (steps 1-n)

---

## Significant Differences

### Depth and Detail Level

1. **FF7_Kernel_Overview.md** is a **conceptual overview**
   - Serves as entry point documentation
   - High-level understanding of kernel architecture
   - No implementation-specific data or binary formats
   - Suitable for architectural understanding

2. **03_KERNEL.md** is **comprehensive technical reference**
   - Complete binary file format specifications
   - Byte-level offset and length documentation
   - Encoding schemes and compression algorithms
   - Data structure tables with all possible values
   - Implementation details for tool developers

### Content Organization

1. **FF7_Kernel_Overview.md**
   - Single narrative flow
   - Only 2 main sections
   - Single image reference
   - ~34 lines total

2. **03_KERNEL.md**
   - 4 major sections (I-IV) with ~30+ subsections
   - Hierarchical structure suitable for reference lookup
   - Complex nested tables
   - Multiple data format specifications
   - ~1641 lines total

### Target Audience

1. **FF7_Kernel_Overview.md**
   - Game developers seeking architectural overview
   - Modders wanting to understand system organization
   - General reference for kernel concept history

2. **03_KERNEL.md**
   - Tool developers building extraction/modding utilities
   - ROM hackers needing precise format specifications
   - Archive and texture editors
   - 3D model converters

---

## Recommendations

- [ ] **Consolidate related documentation**: Consider creating a "Kernel Architecture" parent document with FF7_Kernel_Overview.md as summary and 03_KERNEL.md as complete reference
- [ ] **Add cross-references**: Link from Overview to detailed sections in major file for users who need deeper dives
- [ ] **Update table of contents**: 03_KERNEL.md lacks a comprehensive TOC despite 1641 lines - recommend adding structured heading navigation
- [ ] **Separate by function**: Consider splitting 03_KERNEL.md into subsections:
  - Kernel_Core.md (History + Functionality)
  - Kernel_Memory.md (RAM/VRAM/CD-ROM)
  - Kernel_Archives.md (KERNEL.BIN, LZS, LGP)
  - Kernel_Formats.md (Textures, Models)
- [ ] **Verify overview completeness**: FF7_Kernel_Overview.md appears complete for its intended scope (conceptual overview), but confirm no user-facing sections were intended to be added
- [ ] **Address Lorem ipsum**: Section 3.1 (PSX Model Formats) contains Lorem ipsum placeholder text - needs actual content or removal
- [ ] **Update date metadata**: Both files lack creation/modification dates - recommend adding timestamps per project standards
