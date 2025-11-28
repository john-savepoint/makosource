# Comparison: FF7_Kernel_Kernelbin.md vs 03_KERNEL.md

**Created:** 2025-11-28 JST
**Comparison Type:** Individual file vs Major section overlap analysis

## File Sizes

| Metric | Value |
|--------|-------|
| FF7_Kernel_Kernelbin.md | 57 lines |
| 03_KERNEL.md | 1,641 lines |
| **Ratio** | **1 : 28.8** (Major section is ~29x larger) |

## Overview

The individual file `FF7_Kernel_Kernelbin.md` is a **narrow, focused document** covering only KERNEL.BIN and KERNEL2.BIN file structure and architecture. The major section `03_KERNEL.md` is a **comprehensive treatment** that includes the same content plus extensive additional material covering kernel history, memory management, and low-level libraries.

## Content Comparison

### Topics Covered in BOTH Files

The following topics appear in both documents with largely identical information:

1. **Important Files Table**
   - Both list PSX version: `/INIT/KERNEL.BIN`
   - Both list PC version: `/DATA/KERNEL/KERNEL.BIN` and `/DATA/KERNEL/KERNEL2.BIN`
   - Content matches exactly (lines 12-15 in individual file; lines 83-86 in major section)

2. **KERNEL.BIN Overview**
   - Both describe BIN-GZIP format
   - Both state: "27 gziped sections concatenated together with a 6 byte header for each"
   - Both note: "same both on the PC and PSX versions"
   - Both explain: "holds all the static data and menu text for the game"
   - Both reference: "look up table at the beginning of the section" and sections 10-27 as FF Text files

3. **KERNEL.BIN Section Table**
   - Both include identical table of 27 sections with offsets (lines 23-51 in individual; lines 94-122 in major)
   - Offsets match exactly for all sections
   - Data descriptions match (with minor formatting variations)
   - **Note:** Section 3 is labeled "Battle and growth data" in individual file but "Unknown (Savemap?)" in major section

4. **KERNEL2.BIN Overview**
   - Both describe PC-only archive containing sections 10-27 (text data)
   - Both explain: "data was ungzipped from the original archive, concatenated together, and then LZSed"
   - Both mention: "4 byte header giving the length of the file"
   - Both state: "27KB (27648 bytes)" maximum storage space

## Content ONLY in Individual File (FF7_Kernel_Kernelbin.md)

**Minimal unique content:**

The individual file contains almost no unique material beyond the shared KERNEL.BIN/KERNEL2.BIN tables and descriptions.

- Slightly different wording in section descriptions (minor stylistic variations)
- Section 3 reference: Labels it as "Battle and growth data" vs "Unknown (Savemap?)"
- Slightly more concise language overall

## Content ONLY in Major Section (03_KERNEL.md)

The major section contains **extensive additional material** covering:

### Part I: Kernel Overview (Lines 3-26)
- **1.1 History:**
  - FF1 kernel architecture on NES
  - Memory mapper (MMC1) explanation
  - 16K sections and banking system
  - Evolution across FF series (FF VI PSX/PC port issues mentioned)
  - Historical context on module/kernel systems

- **1.2 Kernel Functionality:**
  - Threaded multitasking program description
  - Software-based memory manager for RAM and video memory
  - Psy-Q libraries explanation
  - PC port library replacements (SEQ→MIDI)
  - System hierarchy diagram

### Part II: Memory Management (Lines 27-77)
- **1.1 RAM Management:**
  - Save Map concept (4,340 bytes / 0x10F4)
  - 5 banks of field-accessible memory with offset tables
  - Bank 1-5 descriptions with memory addresses
  - Temporary field variables (256 bytes)
  - Cross-reference to Menu section for detailed Save Map

- **1.2 VRAM Management:**
  - PSX VRAM specifications (1MB, 2048x512 pixels)
  - VRAM representation as 1024x512 matrix
  - Color depth handling
  - Diagrams of typical VRAM layout during gameplay
  - Texture buffer, frame buffer, CLUT, and cache organization
  - Volatility and overwrite patterns

- **1.3 PSX CD-ROM Management:**
  - BIOS hardware access rules
  - Module preloading during transitions
  - "Quick mode" CD-ROM access limitations (8KB at a time)
  - Sector-based file referencing vs filename approach

### Part III: Low Level Libraries (Lines 549-1641, ~1,100 lines)
This is a **massive additional section** covering:

#### **1.1 DATA ARCHIVES** (Lines 561-591)
- BIN archive data format types:
  - **BIN Types:** Uncompressed archives with 4-byte header
  - **BIN-GZIP Types:** 6-byte header with gziped sections
  - Detailed structure tables with offsets and descriptions

#### **1.1.2 LZS Compressed Archive for PSX** (Lines 592+)
- Format specifications
- Compression algorithms
- Reference formats
- Examples and complications

#### **1.1.3 LGP Archive Format for PC** (Lines 666+)
- File header structure
- CRC code section
- Actual data section
- Terminator section
- Detailed notes on implementation

#### **2. TEXTURES** (Lines 746+)
- **2.1 TIM Texture Data Format for PSX:**
  - CLUT (Color Look-Up Table) definitions
  - VRAM location specifications
  - TIM file format details
  - 4-bit, 8-bit, and 16-bit per pixel formats with technical specifications

- **2.2 TEX Texture Data Format for PC**
  - PC-specific texture format documentation

#### **3. File Formats for 3D Models** (Lines 866+)
- **3.1 Model Formats for PSX**
- **3.2 Model Formats for PC:**
  - **3.2.1 HRC Hierarchy Data Format:**
    - Bone/skeleton system
    - Header structure
    - Bone definitions

  - **3.2.2 RSD Resource Data Format:**
    - Resource data structures
    - SGI RSD fileset library format

  - **3.2.3 "P" Polygon File Format:**
    - Comprehensive polygon file structure
    - File headers
    - Vertex, normal, texture coordinate chunks
    - Vertex color, polygon color, edge chunks
    - Polygon chunk definitions
    - Hundred chunk, group chunk, bounding box
    - Normal index table
    - Complex grouping algorithm (5-step process)
    - DOT-Group, TILDE-Group, and absolute indices explanations

## Significant Differences in Detail Level

| Aspect | Individual File | Major Section |
|--------|-----------------|---|
| **KERNEL.BIN description** | ~35 lines | ~60 lines (more context) |
| **KERNEL2.BIN description** | ~4 lines | ~4 lines (identical) |
| **Kernel history/context** | None | ~25 lines |
| **Memory management** | None | ~50 lines with diagrams |
| **File formats coverage** | None | ~1,100 lines |
| **Texture formats** | None | ~200 lines |
| **3D model formats** | None | ~800 lines |
| **Technical depth** | Overview only | Comprehensive specification |

## Section-by-Section Mapping

### FF7_Kernel_Kernelbin.md Structure:
1. **Lines 3-6:** TOC
2. **Lines 10-15:** Important Files
3. **Lines 17-51:** The KERNEL.BIN Archive (overview + section table)
4. **Lines 53-57:** The KERNEL2.BIN Archive

### 03_KERNEL.md Structure:
1. **Lines 1-26:** Part I - Kernel Overview (History & Functionality)
2. **Lines 27-77:** Part II - Memory Management (RAM, VRAM, CD-ROM)
3. **Lines 79-87:** Game Resources - Important Files *(OVERLAP)*
4. **Lines 88-122:** The KERNEL.BIN Archive *(OVERLAP)*
5. **Lines 124-543:** KERNEL.BIN Section Formats (9 sections detailed)
6. **Lines 545-547:** The KERNEL2.BIN Archive *(OVERLAP)*
7. **Lines 549-1641:** Part IV - Low Level Libraries (1,100 lines of additional technical content)

## Overlapping Content Precision

**Exact Matches:**
- Important Files table: 100% identical
- KERNEL.BIN section offsets: 100% identical
- KERNEL2.BIN description: ~99% identical (minor wording variation)

**Minor Differences:**
- Section 3 naming: "Battle and growth data" vs "Unknown (Savemap?)"
  - Major section uses question mark, suggesting uncertainty
  - Individual file uses definitive naming

**Structural Differences:**
- Individual file lacks internal section format specifications (e.g., "Section 1: Command data format", "Section 2: Attacks data format", etc.)
- Major section includes detailed specifications for all 9 binary sections (124-543) which are completely absent from individual file

## Recommendations

- [x] **Individual file serves as quick reference:** FF7_Kernel_Kernelbin.md is optimal for readers needing just KERNEL.BIN/KERNEL2.BIN file structure
- [ ] **Investigate Section 3 naming discrepancy:** Clarify whether section 3 is "Battle and growth data" or contains Savemap initialization data (or both)
- [ ] **Consider consolidation:** Individual file is essentially a condensed excerpt of 03_KERNEL.md lines 79-547
- [ ] **Preserve individual file if:** It serves as a focused quick-reference in a larger documentation system
- [ ] **Deprecate individual file if:** Documentation organization prefers single canonical source in major sections
- [ ] **Add cross-references:** If both files are retained, add links noting they cover the same KERNEL.BIN/KERNEL2.BIN content
- [ ] **Document the ~1,100 line gap:** Major section includes low-level library specifications (archives, textures, 3D models) that are critical for implementation but completely absent from individual file

## Summary

- **Overlap Percentage:** ~15% (52 of 57 lines in individual file overlap with major section)
- **Unique to Individual:** ~5% (minor wording variations, non-essential)
- **Unique to Major:** ~85% (1,589 lines of extended kernel, memory, and library documentation)
- **Content Relationship:** Individual file is a strict subset of major section
- **Recommendation:** Keep both if fast-access quick reference is valuable; consolidate if single canonical source is preferred
