# Content Analysis Report: FF7_Field_Module.md vs 05_FIELD_MODULE.md

**Analysis Date**: 2025-11-29
**Analyzed By**: Claude Code Analysis Agent
**Report Type**: Phase 1 - Content Comparison & Gap Analysis

---

## Executive Summary

This report documents a comprehensive comparison between the individual FF7_Field_Module.md file (293 lines) and the corresponding major section 05_FIELD_MODULE.md (2,645 lines) from the consolidated game engine documentation.

**Key Findings**:
- **Size Disparity**: Major section is 9x larger (2,645 vs 293 lines)
- **Content Coverage**: Substantial missing content in individual file
- **Scope Alignment**: Individual file covers ~10% of major section scope
- **Images**: 13 images in major section, all referenced files appear to be missing or have different naming
- **Content To Extract**: 2,300+ lines of substantive technical documentation
- **Status**: Individual file is severely incomplete and requires significant expansion

---

## Topic Scope Analysis

### Individual File (FF7_Field_Module.md) - Current Scope

**Topics Covered**:
1. Important Files (PSX/PC versions) - brief table
2. Field Overview - basic description
3. Field Format (PC) - PC file structure, header format (9 sections)
4. Field Format (PSX) - DAT/MIM/BSX/BCX formats (brief)
5. Event Scripting - overview
6. Script Commands - opcodes overview
7. Movies - movie handling
8. The 3D Overlay - section header only
9. Data Organization - section header only
10. "A" Field Animation Files - animation structure (36-byte header example)
11. Images - single VRAM background image

**Depth Level**: Shallow - mostly structural overview, lacks detailed specifications

### Major Section (05_FIELD_MODULE.md) - Comprehensive Scope

**Topics Covered**:
1. **Field Module Overview** - extended description of system architecture
2. **PC Field Format** - detailed header structure, 9 sections explained
3. **Field File Sections** (1-9):
   - Section 1: Dialog and Event Script (detailed header, subsections)
   - Section 2: Camera Matrix (vector operations, format specification)
   - Section 4: Palette (color format, 15-bit RGB, palette pages)
   - Section 5: Walkmesh (geometry, triangles, access information)
   - Section 7: Encounter Data (battle encounter system)
   - Section 9: Background (sprite format, image data layout, palette handling)
4. **PSX DAT Format** - compression, header structure
5. **PSX MIM Format** - truncated TIM format
6. **PSX BSX Format** - model data
7. **PSX BCX Format** - character models
8. **Debug Rooms** - STARTMAP and 10 developer test rooms
9. **Debug Room Characters** - detailed scripting for 10 developers' rooms (Kitase, Kyounen, Nojima, Kichioka, Toriyama, Akiyama, Matsuhara, Chiba, Tokita, Katou)
10. **Event Scripting System** - complete opcode matrix (0x00-0xF0, 256 commands)
11. **Movies** - movie playback system
12. **3D Overlay** - animation and model rendering
13. **Data Organization** - internal data structures

**Depth Level**: Very detailed - includes formulas, code snippets, tables, field coordinates

---

## Content Already in Individual File

The individual FF7_Field_Module.md contains these sections that align with the major section:

### ✅ Section 1: Important Files Table
- **Lines**: Individual file lines 9-16
- **Major Section Equivalent**: Lines 2-9
- **Assessment**: Nearly identical, minor format differences
- **Status**: COMPLETE - no expansion needed

### ✅ Section 2: Field Overview
- **Lines**: Individual file lines 18-50
- **Major Section Equivalent**: Lines 11-35
- **Assessment**: Individual file has ADDITIONAL content (VRAM snapshot discussion, layer obscuring explanation). Major section is condensed version.
- **Status**: ADEQUATE - individual file has unique content

### ✅ Section 3: Field Format (PC) - General Structure
- **Lines**: Individual file lines 53-159
- **Major Section Equivalent**: Lines 37-72
- **Assessment**: Individual file EXPANDS on major section with detailed table and pointer information. Contains link references to subsections (Field Script, Camera Matrix, etc.) that major section doesn't reference as cleanly.
- **Status**: PARTIAL - individual has some additional detail

### ✅ Section 4: Field Format (PSX) - DAT/MIM/BSX/BCX
- **Lines**: Individual file lines 161-221
- **Major Section Equivalent**: Lines 432-449 (PSX DAT/MIM/BSX/BCX format sections)
- **Assessment**: Major section has more detailed explanation of DAT format (lines 75-106 cover Section 1 in detail). Individual file is summary only.
- **Status**: INCOMPLETE - major section has expanded DAT format details

### ✅ Section 5: Event Scripting
- **Lines**: Individual file lines 223-237
- **Major Section Equivalent**: Lines 2508-2580 (Event Scripting / Script Commands)
- **Assessment**: Individual file has brief overview. Major section has complete OPCODE MATRIX with 256 commands listed.
- **Status**: CRITICALLY INCOMPLETE - opcode matrix missing from individual file

### ✅ Section 6: Script Commands
- **Lines**: Individual file lines 227-229
- **Major Section Equivalent**: Lines 2510-2580
- **Assessment**: Individual file references opcodes but provides no actual opcode specifications.
- **Status**: CRITICALLY INCOMPLETE - massive gap

### ✅ Section 7: Movies
- **Lines**: Individual file lines 231-237
- **Major Section Equivalent**: Lines 2582-2644 (Movie handling, FMV/AVI formats)
- **Assessment**: Individual file covers basic movie triggering. Major section explains FMV compression formats, disc modes, timing.
- **Status**: INCOMPLETE

### ✅ Section 8: The 3D Overlay
- **Lines**: Individual file line 239 (header only)
- **Major Section Equivalent**: Lines 2584-2598 (Lorem Ipsum placeholder + data structures list)
- **Assessment**: Both sections are placeholders/incomplete
- **Status**: PLACEHOLDER

### ✅ Section 9: Data Organization
- **Lines**: Individual file line 241 (header only)
- **Major Section Equivalent**: Lines 2588-2598 (Lorem Ipsum placeholder + textures/polygons/animation list)
- **Assessment**: Both sections are placeholders
- **Status**: PLACEHOLDER

### ✅ Section 10: "A" Field Animation Files
- **Lines**: Individual file lines 243-287
- **Major Section Equivalent**: Lines 2599-2642
- **Assessment**: **SIGNIFICANT DIFFERENCES**:
  - Individual file: 36-byte header (version, frames_count, bones_count, rotation_order, 5 runtime_data values)
  - Major section: 24-byte header (x1, frames_count, bones_count, x2/x3/x4) + 12 unknown bytes after
  - Individual file provides rotation order info; major section doesn't
  - Major section frame format different: "6 floats + rotations" vs "root rotation (3 floats) + root translation (3 floats) + rotations"
- **Status**: CONFLICTING SPECIFICATIONS - major section may be more recent/accurate (24-byte header vs 36-byte)

---

## Critical Content Gaps - Items to Extract

### 🔴 CRITICAL EXTRACTION 1: Section 1 - Dialog and Event Script Format
- **Lines**: 74-106 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Technical specification with code structure
- **Importance**: HIGH - defines scripting data structure
- **Includes**:
  - Section 1 Header structure (u16, char, u16, u16, u16, u16 array, char array fields)
  - Event Script Subsection format
  - Dialog Subsection format
  - Pointer table layout
  - Code block for FF7SCRIPTHEADER struct

### 🔴 CRITICAL EXTRACTION 2: Section 2 - Camera Matrix
- **Lines**: 109-168 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Technical specification with vector math
- **Importance**: HIGH - essential for 3D rendering
- **Includes**:
  - Description of section 2 (camera matrix definition)
  - Vector and position information
  - Left-handed coordinate system explanation
  - Section 2 Format table (camera vectors, position, zoom)
  - Vector loading procedure
  - Fixed-point arithmetic explanation (multiply constant 4096)
  - Orthonormal vector explanation with formulas
  - Camera matrix center calculation formula (code snippet)

### 🔴 CRITICAL EXTRACTION 3: Section 4 - Palette Format
- **Lines**: 170-204 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Technical specification with binary format detail
- **Importance**: MEDIUM-HIGH - color data handling
- **Includes**:
  - Section 4 Palette Format table
  - 15-bit color format explanation (5-bit RGB + 1-bit mask)
  - Palette page explanation (256-color pages)
  - Palette entry bit layout diagram

### 🔴 CRITICAL EXTRACTION 4: Section 5 - Walkmesh Structure
- **Lines**: 206-254 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Technical specification with geometry data
- **Importance**: CRITICAL - character movement system
- **Includes**:
  - Walkmesh header structure (NoS - Number of sectors)
  - Sector pool format (triangles with vertices)
  - vertex_3s structure definition
  - sect_t structure definition
  - Access pool format (neighbor polygon IDs)
  - Access table explanation (crossing edges)
  - Walkmesh diagram image (_page_80_Picture_0.jpeg)

### 🔴 CRITICAL EXTRACTION 5: Section 7 - Encounter Data
- **Lines**: 256-277 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Technical specification
- **Importance**: MEDIUM - battle encounter system
- **Includes**:
  - Encounter section structure (48 bytes fixed)
  - Offset breakdown for encounter data
  - Primary vs secondary encounters
  - Encounter chance calculation
  - Notes on encounter rates

### 🔴 CRITICAL EXTRACTION 6: Section 9 - Background and Sprite Format
- **Lines**: 280-429 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Technical specification with extensive binary format details
- **Importance**: CRITICAL - visual rendering
- **Includes**:
  - Section 9 Background format overview
  - Background paradigm explanation
  - 16x16 pixel block sprite system
  - Palette pages and color mapping
  - Background sprite data structure (TFF7BgSprite record with 14 fields)
  - Image data offset calculation formulas (shifts vs multiplication)
  - Destination coordinate system (0,0 at image center)
  - Pixel copying and palette filtering procedure
  - Color conversion from FF7 to Windows format (code snippet)
  - Multi-layer rendering explanation
  - Variable conventions for data types

### 🔴 CRITICAL EXTRACTION 7: Debug Rooms (STARTMAP)
- **Lines**: 452-500 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Procedural documentation / Developer reference
- **Importance**: LOW-MEDIUM - development artifacts
- **Includes**:
  - Debug room overview
  - STARTMAP room description
  - Japanese character list (8 developers + 2 others)
  - Developer name mappings (北=Kitase, 京=Kyounen, 野=Nojima, etc.)
  - Character script interactions
  - Room image (_page_85_Picture_5.jpeg)

### 🔴 CRITICAL EXTRACTION 8: Kitase's Room Debug Events
- **Lines**: 532-588 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Procedural documentation / Event testing
- **Importance**: LOW - development artifacts
- **Includes**:
  - Kitase's room overview with image (_page_87_Picture_19.jpeg)
  - 5 character scripts (Aerith, Tifa, Cid, President Shinra, Shinra Employee)
  - Event names and descriptions
  - Lighting effects information
  - Debug test procedures

### 🔴 CRITICAL EXTRACTION 9: Kyounen's Room through Tokita's Room
- **Lines**: 669-2399 in major section
- **Current Status**: NOT IN individual file at all
- **Content Type**: Extensive procedural documentation
- **Importance**: LOW - development artifacts
- **Includes**:
  - 8 additional developer debug rooms
  - ~1,700 lines of event testing procedures
  - Character interactions and menu testing
  - Location mapping for debug testing
  - 9 additional images
  - Notes on broken JUMPMAP commands and stuck locations

### 🔴 CRITICAL EXTRACTION 10: Complete Opcode Matrix
- **Lines**: 2514-2542 in major section
- **Current Status**: PARTIALLY in individual file (opcodes section header only)
- **Content Type**: Technical reference
- **Importance**: CRITICAL - script command system
- **Includes**:
  - Complete opcode matrix table (0x00-0xF0, 256 commands organized in 16x16 grid)
  - Command names: RET, REQ, REQSW, REQEW, PREQ, PRQSW, etc.
  - Opcode definitions with arguments
  - Description tables for each opcode

### 🟡 EXTRACTION 11: Final Movie Handling (Lines 2644-2645)
- **Lines**: 2644-2645 in major section
- **Status**: Empty section (just "## **Movies**" header)
- **Assessment**: No additional content

---

## Images in Extracted Content

All images referenced in major section use relative path format `![](filename.jpeg)` with filenames like `_page_73_Picture_13.jpeg`. These files appear to be extracted from PDF pages and **do not exist in the current images/ directory**.

### Image Inventory:

| Line | Image Name | Section | Found | Path Notes |
|------|-----------|---------|-------|-----------|
| 27 | _page_73_Picture_13.jpeg | Field Overview VRAM | ❌ NO | Need to find or recreate |
| 254 | _page_80_Picture_0.jpeg | Walkmesh Diagram | ❌ NO | Shows walkmesh polygon access |
| 462 | _page_85_Picture_5.jpeg | STARTMAP Layout | ❌ NO | Debug room layout |
| 536 | _page_87_Picture_19.jpeg | Kitase's Room | ❌ NO | Developer room layout |
| 673 | _page_90_Picture_4.jpeg | Kyounen's Room | ❌ NO | Developer room layout |
| 817 | _page_93_Picture_2.jpeg | Nojima's Room | ❌ NO | Developer room layout |
| 1005 | _page_96_Picture_2.jpeg | Kichioka's Room | ❌ NO | Developer room layout |
| 1202 | _page_99_Picture_2.jpeg | Toriyama's Room | ❌ NO | Developer room layout |
| 1512 | _page_103_Picture_15.jpeg | Akiyama's Room | ❌ NO | Developer room layout |
| 1686 | _page_106_Picture_2.jpeg | Matsuhara's Room | ❌ NO | Developer room layout |
| 1850 | _page_108_Picture_26.jpeg | Chiba's Room | ❌ NO | Developer room layout |
| 2256 | _page_114_Picture_23.jpeg | Tokita's Room | ❌ NO | Developer room layout |
| 2428 | _page_117_Picture_2.jpeg | Katou's Room | ❌ NO | Developer room layout |

**Image Handling Note**: The individual file at line 292 references `../images/Field_BackgroundVRAM.jpg` which EXISTS in the images directory. When extracting content, image references should be adjusted from `_page_XX_Picture_YY.jpeg` to `../../images/field_module_image_XX.jpg` format and flagged for verification.

---

## Content for Related Individual Files

Some extracted content may belong in other individual files:

### For FF7_LGP_format.md:
- Field files are stored in FLEVEL.LGP (mentioned in major section line 41)
- Archive container format should reference field file structure

### For FF7_LZSS_format.md:
- LZS compression is used for field files (lines 41, 165, 213, 217)
- Decompression procedures should be cross-referenced

### For FF7_TEX_format.md:
- Field textures referenced in FIELD.TDB (line 217)
- Background sprite format uses palettized data (lines 310-429)
- Palette system uses 16-bit color (5-bit RGB + mask bit)

### For PSX_TIM_format.md:
- MIM files are "truncated TIM files" (line 213)
- Cross-reference with TIM format documentation

---

## Discrepancies and Conflicts

### 1. Animation File Header Format (CONFLICT)
- **Individual File** (lines 264-272): 36-byte header with named fields (version, frames_count, bones_count, rotation_order[3], unused, runtime_data[5])
- **Major Section** (lines 2625-2633): 24-byte header (x1, frames_count, bones_count, x2, x3, x4) plus 12 unknown bytes after
- **Status**: **CONFLICTING** - requires investigation into which is correct
- **Recommendation**: Verify against actual FF7 game files

### 2. Animation Frame Format (CONFLICT)
- **Individual File** (lines 254-261): "root rotation + root translation + rotations for each bone"
- **Major Section** (lines 2615-2623): "unknown 24 bytes = 6 floats + rotations"
- **Status**: **CONFLICTING** - description differs
- **Recommendation**: Verify against binary format specifications

---

## Gaps and Missing Content Analysis

### 🔴 Severely Underrepresented Topics:

1. **Field Script Data (Section 1)**: 0 lines in individual, 33 lines in major
2. **Camera Matrix (Section 2)**: 0 lines in individual, 60 lines in major
3. **Palette System (Section 4)**: 0 lines in individual, 35 lines in major
4. **Walkmesh Geometry (Section 5)**: 0 lines in individual, 49 lines in major
5. **Encounter System (Section 7)**: 0 lines in individual, 22 lines in major
6. **Background Rendering (Section 9)**: 0 lines in individual, 150 lines in major
7. **Debug Rooms**: 0 lines in individual, 1,800+ lines in major
8. **Opcode Matrix**: Brief reference in individual, 30+ lines in major

### Coverage Summary:
- **Current Individual File Coverage**: ~10-15% of major section content
- **Missing Coverage**: ~85-90% of technical specifications and debug room documentation
- **Severity**: CRITICAL - most subsections have zero documentation in individual file

---

## Merge Plan Summary

### Phase 2 Merge Strategy:

1. **Preserve existing content** in FF7_Field_Module.md (lines 1-293)

2. **Append extracted sections** from major section in this order:
   - Section 1 Dialog/Event details (lines 74-106)
   - Section 2 Camera Matrix (lines 109-168)
   - Section 4 Palette (lines 170-204)
   - Section 5 Walkmesh (lines 206-254)
   - Section 7 Encounter (lines 256-277)
   - Section 9 Background/Sprites (lines 280-429)
   - Event Scripting Opcode Matrix (lines 2514-2542)
   - Optional: Debug Room Documentation (lines 452-2462, 1,800+ lines)

3. **Image path adjustments**:
   - Replace `![](filename.jpeg)` with `![](../../images/filename.jpg)`
   - Verify all images exist or flag for sourcing
   - Current VRAM image path is already correct

4. **Clear extraction markers** to show source and line numbers

5. **Maintain reference links** to related individual files (LGP, LZSS, TEX, TIM formats)

---

## Recommendations for Implementation Team

1. **Priority 1 - Technical Specifications**:
   - Extract Sections 1-5, 7, 9 (field data structures)
   - Extract Opcode Matrix
   - Resolve animation format conflicts

2. **Priority 2 - Image Resolution**:
   - Locate or recreate 13 missing images
   - Update image paths to working locations
   - Consider renaming to more semantic names (field_vram_background.jpg vs _page_73_Picture_13.jpeg)

3. **Priority 3 - Debug Room Documentation**:
   - Decide if debug room content belongs in main field documentation
   - Consider separate file (FF7_Field_Debug_Rooms.md) for 1,800+ lines

4. **Priority 4 - Cross-File References**:
   - Link to format files (LGP, LZSS, TEX, TIM) where appropriate
   - Add inverse links from format files back to field module

5. **Conflict Resolution**:
   - Verify animation header format against actual binary specifications
   - Document which version is authoritative
   - Add technical notes explaining discrepancies

---

## Report Metadata

- **Individual File**: FF7_Field_Module.md (293 lines, 15KB)
- **Major Section**: 05_FIELD_MODULE.md (2,645 lines, 90KB)
- **Size Ratio**: 1:9 (individual to major)
- **Extraction Candidates**: 2,300+ lines
- **Critical Gaps**: 7 major sections completely missing
- **Images**: 13 referenced, 0 found in current directory
- **Conflicts**: 2 (animation header format, frame format)
- **Estimated Merge Time**: 2-3 hours (including image sourcing)

---

**End of Analysis Report**
