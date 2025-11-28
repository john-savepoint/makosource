# Comparison: FF7_Kernel_Low_level_libraries.md vs 03_KERNEL.md

## File Sizes
- Individual file: 127 lines
- Major section: 1,641 lines
- Difference: 03_KERNEL.md is 12.9x larger

## Overview
The individual file `FF7_Kernel_Low_level_libraries.md` is a focused, condensed version covering low-level libraries and data formats. The major section `03_KERNEL.md` is a comprehensive guide covering the entire kernel system, including memory management, VRAM management, CD-ROM management, and detailed specifications of all kernel data structures. The individual file is essentially a subset of content found in the major section.

## Topics Covered in BOTH Files

### 1. PC to PSX Comparison
- **Individual file:** Lines 8-16 (brief overview of format differences)
- **Major section:** Lines 551-559 (identical content, slightly reformatted)
- **Note:** Both explain that PSX used Psy-Q development library with TIM files, while PC port converted to TEX files due to missing artwork

### 2. Data Archives Section
- **Individual file:** Lines 18-101 (complete archive format documentation)
- **Major section:** Lines 561-745 (extended archive format documentation with more detail)
- **Coverage:**
  - BIN Type Archives (uncompressed)
  - BIN-GZIP Type Archives (with detailed tables)
  - LZS Archives and LZS Compression algorithms
  - LGP Archives (file structure and format)

### 3. Textures
- **Individual file:** Lines 103-113 (brief texture format overview)
- **Major section:** Lines 746-865 (comprehensive texture specification)
- **Common content:**
  - TIM texture format for PSX (basic reference)
  - TEX texture format for PC (basic reference)

### 4. File Formats for 3D Models
- **Individual file:** Lines 115-127 (high-level overview)
- **Major section:** Lines 866-878 (brief statement about models being stored differently)
- **Common content:** Basic mention that models are handled differently between PSX and PC

## Content ONLY in Individual File (FF7_Kernel_Low_level_libraries.md)

**None identified.** All content in the individual file appears in the major section, though sometimes in expanded or reorganized form.

## Content ONLY in Major Section (03_KERNEL.md)

### 1. Kernel Overview & History (Lines 1-26)
- FF1 memory banking history
- Kernel as throwback to NES memory mapping systems (MMC1 controller)
- Kernel functionality overview
- Kernel as threaded multitasking program
- Architecture diagram showing User → Module → Kernel → Psy-Q libraries → PSX BIOS → Hardware
- Memory manager handling RAM and VRAM for all modules

### 2. Memory Management Section (Lines 27-73)
- **RAM Management (Lines 29-47)**
  - Save Map overview (4,340 bytes / 0x10F4)
  - 5 banks of field script memory
  - Field Script Banks 1-5 with memory offsets
  - Temporary field variables (256 bytes)
  - Save map structure details

- **VRAM Management (Lines 49-71)**
  - Detailed explanation of PSX VRAM as 2048x512 pixel surface
  - VRAM state during gameplay (double-buffering, texture cache)
  - VRAM schematic with detailed layout diagram
  - Double page buffer system
  - Blank areas for V-sync
  - Color Look Up Tables (CLUT) placement
  - Texture cache boundaries and volatility ordering
  - Game screen layout during different game states

- **PSX CD-ROM Management (Lines 73-77)**
  - Hardware access restrictions
  - Module preloading while executing current module
  - Quick mode CD-ROM access (8KB at a time)
  - Low-level BIOS calls for CD-ROM access without filename references

### 3. Game Resources Section (Lines 79-545)
- **KERNEL.BIN Overview (Lines 88-127)**
  - File format: BIN-GZIP with 6-byte header
  - 27 gzipped sections structure
  - Complete table of all 27 sections with offsets (Files 1-27)
  - Distinction between data sections (1-9) and text sections (10-27)

- **KERNEL.BIN Section Formats (Lines 128-544)**

  **Section 1: Command Data (16 bytes per record)**
  - Menu command structure (incomplete table in document)

  **Section 2: Attacks Data (28 bytes per record)**
  - Offset 0x00: Unknown (4 bytes)
  - Offset 0x04: Casting cost (1 byte)
  - Offset 0x0A: Attack type (1 byte)
  - Offset 0x0B: Attack attribute (2 bytes) with 13 specific values including:
    - Escape/Exit-Type (0x0000)
    - Ribbon-Like (0x0001)
    - Enemy Skill (multiple values)
    - Restorative/Protective (0x000D)
    - Status-giving/Elemental (0x000F)
    - Shield (0x0011)
    - Limit Break (0x0013)
    - Cait Sith Limit Break (0x0015)
    - Summon (0x0017)
    - Roulette (0x00C7)
    - Multiple Strike Limit breaks (0x0097)
    - Phoenix Down (0xFF01)
    - X-needles attack (0xFF03)
    - Final Limit break (0xFF17)
  - Offset 0x0D: ID Number (1 byte)
  - Offset 0x0E: Restore Apply (1 byte)
  - Offset 0x0F: Strength (1 byte)
  - Offset 0x10: Restore type (1 byte) - HP/MP/Ailment/None
  - Offset 0x11: Unknown (2 bytes)
  - Offset 0x13: Times attacking (1 byte)
  - Offset 0x14: Statuses (4 bytes)
  - Offset 0x18: Element (2 bytes)
  - Offset 0x20: Unknown (2 bytes)

  **Section 3: Savemap (Lines 190-192)**
  - Initial values and structure for Savemap
  - Copied to RAM on initialization
  - Data range: 0x0054 to 0x0fe7

  **Section 4: Initialization Data (Lines 194-196)**
  - Starting stats for characters
  - Related game states on New Game
  - Data range: 0x0054 to 0x0BAF

  **Section 5: Item Data (27 bytes per record, Lines 198-250)**
  - Offset 0x00: Unknown (8 bytes, always 0xFFFFFFFF)
  - Offset 0x08: Unknown (2 bytes)
  - Offset 0x0A: Restriction Mask (1 byte) with 8 specific values
  - Offset 0x0B: Attack Target (2 bytes) - specific targeting modes
  - Offset 0x0D: Item ID (1 byte)
  - Offset 0x0E: Restore Apply (1 byte) - 8 specific values
  - Offset 0x0F: Amount Multiplier (1 byte)
  - Offset 0x10: Restore Type (1 byte)
  - Offset 0x11: Unknown (3 bytes)
  - Offset 0x14: Status effects (4 bytes)
  - Offset 0x18: Element (2 bytes)
  - Offset 0x1A: Unknown (2 bytes)

  **Section 6: Weapon Data (44 bytes per record, Lines 252-334)**
  - Extensive weapon attributes including:
    - Offset 0x00: Weapon Range (Long Range 0x03 / Normal Range 0x23)
    - Offset 0x02: Special Options with attack modifiers (9 specific values including Tifa-specific formulas)
    - Offset 0x04: Weapon Attack (1 byte)
    - Offset 0x06: Materia growth rate (1 byte)
    - Offset 0x08: Weapon attack percentage (1 byte)
    - Offset 0x09: Weapon Model ID (3 bytes)
    - Offset 0x0E: Equip Mask (2 bytes) - 10 character equip flags
    - Offset 0x10: Attack Type (2 bytes) - Cut/Hit/Punch values
    - Offset 0x14: Increase Stat Type (4 bytes) - STR/VIT/MAG/SPI/DEX/LUC
    - Offset 0x18: Stat Amount Increased (4 bytes)
    - Offset 0x1C: Materia Slots (8 bytes) - 4 different slot types
    - Offset 0x27: Attack texture graphic (1 byte)
    - Offset 0x2A: Restriction Mask (1 byte) - 9 specific values

  **Section 7: Armor Data (36 bytes per record, Lines 336-398)**
  - Offset 0x01: Unknown (1 byte)
  - Offset 0x02: Damage Type (1 byte) - Normal/Absorb/No Damage/Half
  - Offset 0x03: Defense (1 byte)
  - Offset 0x04: Magic Defense (1 byte)
  - Offset 0x05: Defense % (1 byte)
  - Offset 0x06: Magic Defense % (1 byte)
  - Offset 0x08: Materia Slots (8 bytes)
  - Offset 0x12: Materia Growth (1 byte)
  - Offset 0x13: Equip Mask (1 byte)
  - Offset 0x15: Element (1 byte)
  - Offset 0x19: Stat Bonus (2 bytes)
  - Offset 0x1D: Stat increase (2 bytes)
  - Offset 0x21: Restriction Mask (1 byte) - 9 specific values

  **Section 8: Accessory Data (16 bytes per record, Lines 400-489)**
  - Offset 0x00: Stat Bonus (2 bytes)
  - Offset 0x02: Bonus Amount (2 bytes)
  - 1 byte: Elemental Strength (Drains/Nullifies)
  - 1 byte: Special Effect (Haste/Fury/Curse Ring Effect/Reflect/Stealing/Manipulation/Barrier/MBarrier)
  - 2 bytes: Elemental Type (Fire/Ice/Lightning/Earth/Poison/Gravity/Water/Wind/Holy/All)
  - 4 bytes: Status Protect (17 specific status values and combinations)
  - Offset 0x0C: Equip Mask (2 bytes) - 10 character equip flags
  - Offset 0x0E: Restriction Mask (1 byte) - 8 specific values

  **Section 9: Materia Data (20 bytes per record, Lines 491-544)**
  - Offset 0x00: Level-up AP limits (8 bytes, multiples of 100)
  - Offset 0x08: Equip Effect (1 byte) - detailed table of STR/VIT/MAG/MDEF/MAXHP/MAXMP/LUCK/DEX modifiers
  - Offset 0x09: Status Bitmask (3 bytes)
  - Offset 0x0C: Element (1 byte)
  - Offset 0x0D: Materia Type (1 byte) with 11 specific values:
    - Unknown (0x00)
    - Master Command (0x08)
    - Master Magic (0x0A)
    - Master Summon (0x0C)
    - Command (0x12, 0x16)
    - Magic (0x19)
    - Booster% (0x20)
    - Unknown (0x21, 0x25, 0x30, 0x35)
    - W-Command (0x33)
    - Summon (0x3B)
    - Enemy Skill (0x57)
  - Offset 0x0E-0x13: Materia attributes (6 bytes)
  - Comprehensive Equip Effects table with 18 byte values and stat modifications

### 4. KERNEL2.BIN Archive (Lines 545-547)
- PC version only archive containing sections 10-27 (text data)
- Data processing: ungzipped, concatenated, then LZSed
- 4-byte header with file length

### 5. Advanced Archive Format Details (Lines 592-665)
- **LZS Compression Deep Dive:**
  - Control byte scheme (1=literal, 0=reference)
  - Literal data processing
  - Reference format with offset and length calculations
  - 12-bit offset and 4-bit length encoding
  - Length minimum of 3 bytes
  - 4K circular buffer reference window
  - Complex offset formula: `real_offset = tail - ((tail - 18 - raw_offset) mod 4096)`
  - Detailed example with positions 1000, offset 339, length 5
  - Edge case handling:
    - Negative offsets (reading before file start - write nulls)
    - Repeated runs (reading past output end - loop output)
  - FF7 uses both edge case tricks

### 6. Detailed Texture Format Specifications (Lines 746-865)
- **TIM Format (PSX):**
  - Basic terms: CLUT, VRAM Location, CLUT Location
  - 4 Bits Per Pixel format (table with offsets and structure)
  - 8 Bits Per Pixel format (table with detailed structure)
  - 16 Bits Per Pixel format (BGR with mask bit)

- **TEX Format (PC):**
  - Header structure (56 bytes unknown + specific fields)
  - Bit depth options: 4, 8, 16
  - Image Width/Height fields
  - Palette entries structure (BGRA format)
  - Bitmap data storage variations by bit depth
  - Optional RGB555 16-bit format

### 7. Advanced 3D Model Format Information (Lines 868-999)
- **HRC Hierarchy Data Format (Lines 880-970)**
  - File structure: Plain text format
  - Header block identification
  - Skeleton naming
  - Bones count and structure
  - Bone definition with 4-line format:
    - Bone name
    - Parent bone name
    - Bone length
    - RSD file associations
  - Note: HRC files contain hierarchy, not skeleton (no bone angles, only lengths)
  - Animation data in .a files

- **RSD Resource Data Format (Lines 972-999)**
  - Plain text format
  - Header ID (@RSD940102, date January 2, 1994)
  - PLY references (polygon data)
  - MAT references (materials)
  - GRP references (polygon groups)
  - NTEX count and TEX file references
  - Comment lines beginning with #

### 8. LGP Archive Deep Technical Details (Lines 666-737)
- Four-section structure:
  1. File header/Table of contents
  2. CRC code (3602 bytes typically)
  3. Actual data with nested file headers
  4. File terminator

- File header: 12-byte creator string ("SQUARESOFT" or "FICEDULA-LGP" for patches)
- File count (4-byte integer)
- TOC entries: 20-byte filename + 4-byte offset + 1-byte check code + 2-byte duplicate handling
- CRC validation (based on file count and filenames)
- Data section file header: 20-byte filename + 4-byte length + file data
- File terminator: "FINAL FANTASY 7" or "LGP PATCH FILE"
- Game flexibility notes:
  - TOC and actual filenames can mismatch
  - Can point multiple TOC entries to same data
  - Data gaps allowed if not referenced
  - 4-byte skip offset for size mismatches
  - Links to LGP tools (LGP Tools, Emerald, Unmass)

## Significant Differences

### 1. Scope and Purpose
- **Individual file:** Narrow focus on low-level libraries and data archive formats only
- **Major section:** Comprehensive kernel system documentation including architecture, memory management, VRAM layout, CD-ROM management, and detailed binary format specifications

### 2. Detail Level
- **Individual file:** Surface-level overview suitable for understanding archive structure concepts
- **Major section:** Exhaustive technical documentation with:
  - Complete binary offset specifications for all KERNEL.BIN sections
  - Formula-based attack modifier calculations
  - Character-specific weapon mechanics (Tifa formulas)
  - Comprehensive status effect and elemental system details
  - Complex compression algorithm explanations with worked examples

### 3. Data Structure Coverage
- **Individual file:** Mentions texture formats exist but no binary specifications
- **Major section:** Complete binary specifications for:
  - TIM format at 4/8/16 bits per pixel with precise offset tables
  - TEX format with header structure and palette organization
  - HRC hierarchy format with bone structure details
  - RSD resource format with cross-reference details

### 4. Architecture and System Design
- **Individual file:** No coverage
- **Major section:** Extensive coverage including:
  - Kernel history dating back to NES FF1
  - Memory banking concepts
  - Multitasking architecture
  - VRAM layout and caching strategies
  - CD-ROM access optimization techniques

### 5. Missing Experimental Sections
- **Major section:** Contains "Lorem ipsum" placeholder text in Section 3.1 (Model Formats for PSX, lines 874), indicating incomplete or placeholder documentation for PSX model formats

## Document Quality Issues

### Major Section Issues
1. **Incomplete Command Data table** (Section 1, lines 130-144): Table header shown but no data rows
2. **Lorem ipsum placeholder** (Section 3.1, line 874): Entire PSX model format section is dummy text
3. **Incomplete Materia Attributes** (Section 9, lines 514-525): Lists attribute values but structure unclear

### Individual File Issues
- None identified; content is clean and complete within its scope

## Recommendations

- [x] **Merge consideration:** The individual file is redundant; all content exists in 03_KERNEL.md in expanded form
- [ ] **Complete missing tables:** Fill in the empty Command Data table in 03_KERNEL.md Section 1
- [ ] **Replace placeholder text:** Replace Lorem ipsum in Section 3.1 with actual PSX model format documentation or move reference to separate document
- [ ] **Clarify Materia Attributes:** Provide complete structure explanation for materia attribute bytes in Section 9
- [ ] **Consolidate documentation:** If maintaining both files, clearly define the individual file as an "overview" or "quick reference" vs the major section as "authoritative reference"
- [ ] **Add cross-references:** Link between files to reduce confusion about which document is canonical
- [ ] **Version information:** Add version numbers or dates to clarify which document is most current
