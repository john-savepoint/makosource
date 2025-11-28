# Comparison: FF7_Kernel_Memory_management.md vs 03_KERNEL.md

**Created:** 2025-11-28 16:45 JST
**Document Version:** 1.0.0
**Analysis Focus:** Memory management documentation overlap and content distribution

---

## File Sizes

- **Individual file (FF7_Kernel_Memory_management.md):** 68 lines
- **Major section (03_KERNEL.md):** 1,641 lines
- **Size ratio:** 03_KERNEL.md is ~24x larger

---

## Topics Covered in BOTH Files

Both files cover the exact same three core memory management topics:

1. **RAM Management**
   - Savemap concept and size (4,340 bytes / 0x10F4 bytes)
   - Five banks of memory accessible by field scripting language
   - 8-bit and 16-bit access modes
   - Field Script Bank memory mapping table with offsets (0x0BA4 to 0x0FA4)
   - 256 bytes for temporary field variables
   - Reference to complete Savemap documentation in MENU section

2. **VRAM Management**
   - PSX 1 megabyte video RAM limitation
   - PSX "surface" representation as 2048x512 pixels
   - Visual diagram showing typical VRAM state during gameplay
   - Double buffering system with video buffers and back buffers
   - Field graphics cache positioning
   - CLUT (Color Look Up Tables) for texture palettes
   - Texture cache boundaries and volatility order
   - Support for multiple color depths

3. **PSX CD-ROM Management**
   - Direct hardware access prohibition and BIOS requirement
   - Module preloading during transitions (Map → Battle)
   - 8-kilobyte quick-load limitation in low-level BIOS mode
   - Sector-based file referencing rather than filename access

---

## Content ONLY in Individual File (FF7_Kernel_Memory_management.md)

**None identified.** The individual file contains no unique content not present in the major section.

The individual file is essentially a focused extraction of section **II. Memory management** from 03_KERNEL.md, with identical content and nearly identical formatting.

---

## Content ONLY in Major Section (03_KERNEL.md)

### Section I: Kernel Overview (lines 3-25)
- **1.1 History:** Evolution from NES MMC1 memory mapping through FF franchise history
- FF1 "Memory Manager Controller #1" (MMC1) architecture
- 16K bankable/16K static memory split on NES
- Architecture evolution through FF series (SNES, PSX ports, PC versions)
- Menu system behavior differences across platforms (electronic vs CD-ROM vs integrated)

### Section 1.2: Kernel Functionality (lines 15-25)
- Kernel as threaded multitasking program
- Software-based memory manager for RAM and video memory
- Psy-Q libraries integration
- PC port library replacements (SEQ player → MIDI player)
- Kernel system architecture diagram showing layering (Module → Kernel → Psy-Q → BIOS → Hardware)

### Section III: Game Resources (lines 79-544)
Complete technical specifications for KERNEL.BIN and KERNEL2.BIN files:

#### **Sections 1-9 Detailed Formats** (lines 88-544):
- **Section 1:** Command data format (16 bytes per record) - *structure not detailed in individual file*
- **Section 2:** Attacks/Magic data format (28 bytes per record) with full offset mappings, casting costs, attack types, attributes, and status effects
- **Section 3:** Savemap initialization data (0x0054 to 0x0fe7)
- **Section 4:** Character starting stats and game initialization data
- **Section 5:** Item data format (27 bytes per record) with restriction masks, target types, restore mechanics, and elemental properties
- **Section 6:** Weapon data format (44 bytes per record) with range types, special options, materia slots, stat bonuses, equip masks, and attack textures
- **Section 7:** Armor data format (36 bytes per record) with defense values, materia slots, element types, and restriction masks
- **Section 8:** Accessory data format (16 bytes per record) with stat bonuses, special effects, elemental properties, and status protections
- **Section 9:** Materia data format (20 bytes per record) with level-up AP limits and equip effects

#### **KERNEL2.BIN** (lines 545-548):
- Existence and differentiation from KERNEL.BIN noted
- PC/PSX version file path references

### Section IV: Low Level Libraries (lines 549-1641)
Extensive technical documentation on data formats and file structures (~1,100 lines):

#### **1. PC to PSX Comparison** (lines 551-560)
- Platform-specific differences in library implementations

#### **1.1 Data Archives** (lines 561-744):
- **BIN Archive Data Format:** Generic BIN type specifications
- **BIN-GZIP Types:** Compressed archive handling and decompression
- **LZS Compression:** PSX-specific compression by Ficedula
  - Format specifications
  - Compression algorithm details
  - Reference format and example data
- **LGP Archive Format:** PC-specific archive format by Ficedula
  - File header structure (Section 1)
  - CRC code handling (Section 2)
  - Actual data organization (Section 3)
  - Terminator specifications (Section 4)
  - Implementation notes

#### **2. Textures** (lines 746-866):
- **TIM Texture Format (PSX)** by native PSX tooling
  - CLUT (Color Look Up Table) specifications
  - VRAM location concepts
  - CLUT location specifications
  - 4-bit, 8-bit, and 16-bit per pixel formats with detailed specifications
- **TEX Texture Format (PC)** by Mirix
  - Format specifications for PC texture handling

#### **3. File Formats for 3D Models** (lines 866-1641):
- **PSX Model Formats:** Native PSX 3D data structures
- **PC Model Formats:**
  - **HRC Hierarchy Format** by Alhexx: Bone/skeleton data, hierarchy definitions, header structure
  - **RSD Resource Format** by Alhexx: Resource organization and texture file references
  - **P Polygon Format** by Alhexx (with Ficedula and Mirex): Comprehensive polygon data
    - Header specifications
    - Vertex chunk format
    - Normals chunk
    - Texture coordinate chunk
    - Vertex color chunk
    - Polygon color chunk
    - Edge chunk
    - Polygon chunk with detailed tag specifications
    - Hundreds/LOD chunk
    - Group chunk with bounding boxes
    - Normal index tables
  - **Grouping and Group Construction:** 5-step process for polygon grouping, DOT-groups, TILDE-groups, absolute indices

---

## Significant Differences

### Content Depth
- **Individual file:** Provides high-level overview of three memory management systems
- **Major section:** Provides comprehensive technical reference with detailed binary format specifications for 20+ data structures

### Scope and Focus
- **Individual file:** Narrowly focused on memory management only
- **Major section:** Comprehensive kernel documentation including history, architecture, memory management, game resources, file formats, texture specs, and 3D model specifications

### Structure Organization
- **Individual file:** Single focused topic (Memory management) with 3 subsections
- **Major section:** Four major sections with extensive subsections covering evolution, functionality, detailed data formats, and technical specifications

### Technical Detail Level
The individual file provides foundational concepts; the major section provides implementation-level details:
- Memory management: Both cover identical concepts, but 03_KERNEL.md references further documentation ("A more complete and annotated save map is in the MENU section")
- VRAM management: Identical descriptions with image references
- CD-ROM management: Identical descriptions
- 03_KERNEL.md additionally specifies exact byte offsets, data types, and values for all game data structures

### Historical Context
- **Individual file:** No historical context provided
- **Major section:** Includes kernel evolution from NES (FF1) through modern platforms, explaining architectural decisions

### Authorship Attribution
- **Individual file:** No author attribution
- **Major section:** Credits contributors by name (Ficedula, Mirix, Alhexx) for specific technical contributions

---

## Recommendations

- [ ] **Evaluate purpose of individual file:** FF7_Kernel_Memory_management.md appears to be a direct extraction of Section II from 03_KERNEL.md. Determine if it should be:
  - Retained as a focused reference document for memory management only
  - Merged back into 03_KERNEL.md with cross-references
  - Removed as redundant if 03_KERNEL.md serves as primary documentation

- [ ] **Update cross-references:** If individual file is retained, add clear references to:
  - Section II in 03_KERNEL.md for complete context
  - MENU section documentation for detailed Savemap format

- [ ] **Consolidate image assets:** Both files reference memory layout diagrams (Gears_img_3.jpg, Gears_img_4.jpg). Verify:
  - Image file paths are correct in both locations
  - Image assets exist and are not duplicated unnecessarily
  - References use consistent path conventions

- [ ] **Maintain documentation synchronization:** If updates are made to memory management sections:
  - Determine single source of truth (recommend 03_KERNEL.md as comprehensive reference)
  - Establish process to prevent divergent versions
  - Consider whether individual file should auto-generate from primary source

- [ ] **Consider documentation hierarchy:** Create clear documentation structure:
  - 03_KERNEL.md as comprehensive technical reference
  - Individual file as optional quick-reference or learning path
  - Savemap.md as detailed Savemap specification (already referenced)
  - Cross-link all related documents

- [ ] **CRITICAL: Resolve Field Script Bank 5 mapping discrepancy:**
  - Individual file (line 23): `| 0x0FA4 | 0xF | 0x7 | Field Script Bank 5 |`
  - 03_KERNEL.md (line 42): `| 0x0FA4 | 0x7 | 0xF | Field Script Bank 5 |`
  - **Values are reversed between files** - the 8-bit bank and 16-bit bank values are swapped
  - **Priority:** High - This affects field scripting memory access patterns
  - **Action:** Determine correct mapping from primary source documentation and update both files

---

## Summary

The individual file FF7_Kernel_Memory_management.md is a nearly identical subset of 03_KERNEL.md, containing only Section II (Memory management). The major section document is comprehensive reference material covering kernel architecture, history, memory management, detailed file format specifications, and 3D model formats (~24x larger). No new or unique content exists in the individual file; all three memory management topics are identically documented in both sources.

**Recommendation:** Consolidate documentation by establishing 03_KERNEL.md as primary reference and determining the specific purpose of the individual file before retaining it.
