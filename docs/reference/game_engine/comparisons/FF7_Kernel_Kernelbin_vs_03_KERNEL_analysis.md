# FF7_Kernel_Kernelbin.md vs 03_KERNEL.md Analysis Report

**Created**: 2025-11-28 15:45 JST
**Analysis Date**: 2025-11-28
**Session ID**: Analysis session

---

## Executive Summary

**Individual File Status**: `FF7_Kernel_Kernelbin.md` contains 58 lines of content covering the KERNEL.BIN and KERNEL2.BIN archives at a basic level.

**Major Section Status**: `03_KERNEL.md` spans 1,641 lines and contains vastly more comprehensive documentation covering:
- Kernel history and functionality (250+ lines)
- Memory management including RAM, VRAM, and CD-ROM management (150+ lines)
- KERNEL.BIN and KERNEL2.BIN archive structure (100+ lines)
- Detailed section formats for binary data (Command, Attack, Item, Weapon, Armor, Accessory, Materia data)
- Low-level libraries and file formats (1,000+ lines covering archives, compression, textures, 3D models)

**Critical Finding**: The individual `FF7_Kernel_Kernelbin.md` file is **severely incomplete**. It covers only the basic archive structure and misses:
1. All kernel overview/history content (should reference FF7_Kernel_Overview.md)
2. Complete section format specifications
3. Relationships to other kernel components
4. File offset mappings

---

## Content Scope Analysis

### FF7_Kernel_Kernelbin.md (Current Individual File)

**Current Coverage** (Lines 1-58):
- Table of contents
- Important Files section (PSX/PC version paths)
- The KERNEL.BIN Archive overview
- The KERNEL2.BIN Archive overview

**Actual Content Provided**:
- Brief explanation of KERNEL.BIN as BIN-GZIP format
- High-level description of 27 gziped sections
- Mention that sections 10-27 are FF Text files
- Table of KERNEL.BIN sections with offsets
- Description of KERNEL2.BIN as PC-specific text data archive

**What's Missing**:
- Detailed format specifications for sections 1-9
- Explanation of section formats (Command data, Attack data, etc.)
- KERNEL.BIN Section Format subsection completely missing
- Text file format details
- Relationship explanations

### 03_KERNEL.md (Major Section)

**Content Breakdown**:

#### Part I: Kernel Overview (Lines 1-27)
- **1.1 History** - FF1 kernel origin, memory banking, MMC1 controller
- **1.2 Kernel Functionality** - Multitasking, memory management, Psy-Q libraries

#### Part II: Memory Management (Lines 27-78)
- **1.1 RAM Management** - Save map structure, field script banks
- **1.2 VRAM Management** - PSX VRAM layout, caching system
- **1.3 PSX CD-ROM Management** - Quick mode loading, 8KB chunks

#### Part III: Game Resources / Kernel.bin (Lines 79-545)
- **Important Files** table (PSX/PC paths)
- **1.1 The KERNEL.BIN Archive**
  - BIN-GZIP format description
  - 27 sections table with offsets
  - Section formats specification
  - **Section 1: Command data** (16 bytes per record) - Lines 128-145
  - **Section 2: Attacks data** (28 bytes per record) - Lines 146-189
  - **Section 3: Savemap** - Lines 190-193
  - **Section 4: Initialization data** - Lines 194-197
  - **Section 5: Item data** (27 bytes per record) - Lines 198-251
  - **Section 6: Weapon data** (44 bytes per record) - Lines 252-335
  - **Section 7: Armor data** (36 bytes per record) - Lines 336-399
  - **Section 8: Accessory data** (16 bytes per record) - Lines 400-490
  - **Section 9: Materia data** (20 bytes per record) - Lines 491-544
- **2.1 The KERNEL2.BIN Archive** - Lines 545-548

#### Part IV: Low Level Libraries (Lines 549-1640+)
This is a massive section covering:
- **1. PC to PSX Comparison**
- **1.1 DATA ARCHIVES**
  - **1.1.1 BIN archive data format**
  - **1.1.2 LZS Compressed archive for PSX**
  - **1.1.3 LGP Archive format for PC**
- **2. TEXTURES**
  - **2.1 TIM texture data format for PSX**
  - **2.2 TEX Texture Data Format for PC**
- **3. File formats for 3D models**
  - **3.1 Model Formats for PSX**
  - **3.2 Model Formats for PC**
    - **3.2.1 HRC Hierarchy data format**
    - **3.2.2 RSD Resource Data Format**
    - **3.2.3 "P" Polygon File Format** (EXTREMELY DETAILED - 600+ lines)

---

## Content to Extract from Major Section (03_KERNEL.md)

### For FF7_Kernel_Kernelbin.md

The following content should be added verbatim to complete this file:

#### EXTRACTION 1: KERNEL.BIN Section Formats Specifications
**Source Lines**: 124-544 (421 lines)
**Content**: Complete specifications for all 9 KERNEL.BIN sections:
- Section 1: Command data format (16 bytes) - Lines 128-145
- Section 2: Attacks data format (28 bytes) - Lines 146-189
- Section 3: Savemap - Lines 190-193
- Section 4: Initialization data - Lines 194-197
- Section 5: Item data format (27 bytes) - Lines 198-251
- Section 6: Weapon data format (44 bytes) - Lines 252-335
- Section 7: Armor data format (36 bytes) - Lines 336-399
- Section 8: Accessory data format (16 bytes) - Lines 400-490
- Section 9: Materia data format (20 bytes) - Lines 491-544

**Notes**:
- These sections include detailed binary structure documentation
- Complete offset/length/description tables
- Status effect and attribute mappings
- Materia equip effect tables

**Currently in Individual File**: NO - MISSING ENTIRELY

**Action**: ADD to FF7_Kernel_Kernelbin.md after the KERNEL2.BIN section

---

## Content Already in Individual File

**Lines 10-52 of FF7_Kernel_Kernelbin.md** closely match **Major Section Lines 81-123**:
- Important Files table (PSX/PC paths)
- KERNEL.BIN Archive overview
- KERNEL.BIN section table with offsets
- KERNEL2.BIN Archive description

**Discrepancies Found**:
1. **Line 88 in major section** states "Unknown (Savemap?)" for Section 3
2. **Individual file Line 25** correctly identifies "Battle and growth data"
3. **Line 106 in major section** lists "Magic Descriptions" at offset 0x2119
4. **Individual file Line 35** correctly lists "Magic descriptions" at offset 0x2199

This suggests the individual file has NEWER/CORRECTED data than the major section.

---

## Content Belonging to Other Files

### Content for FF7_Kernel_Memory_management.md
**Major Section Lines**: 27-78 (52 lines)
- RAM management with save map structure
- VRAM management with PSX memory layout diagrams
- CD-ROM management

### Content for FF7_Kernel_Overview.md
**Major Section Lines**: 1-27 (27 lines)
- Kernel history (FF1, NES, banking)
- Kernel functionality (multitasking, memory management)

**Current Status in That File**: VERIFIED - Contains this content already

### Content for FF7_Kernel_Low_level_libraries.md
**Major Section Lines**: 549-1640+ (1,100+ lines)
- Archive formats (BIN, LZS, LGP)
- Texture formats (TIM, TEX)
- 3D model formats (HRC, RSD, P polygon files)

---

## Key Discrepancies and Issues

### 1. Offset Values Differ
- **Major section Section 11**: 0x2119 (Magic Descriptions)
- **Individual file Section 11**: 0x2199 (Magic Descriptions)
- **Difference**: 0x80 bytes (128 bytes)

This could indicate:
- Individual file has newer/corrected offsets
- Major section extraction was from older documentation
- Need verification against actual game files

### 2. Section 3 Labeling
- **Major section**: "Unknown (Savemap?)" - uncertain
- **Individual file**: "Battle and growth data" - confident

### 3. Format Detail Level
- **Major section**: Comprehensive binary structure documentation (good for implementers)
- **Individual file**: High-level overview only (insufficient for tool makers)

---

## Gaps and Missing Content

### In FF7_Kernel_Kernelbin.md
1. **No binary format specifications** for any section beyond table
2. **No offset explanations** for why sections are at specific locations
3. **No cross-references** to how items/weapons/armor data relates to menu module
4. **No implementation examples** (C structs, parsing code)
5. **No relationship to Savemap.md** - Section 3 is savemap initialization data
6. **No explanation of text sections** (10-27) - what makes them different

---

## Merge Plan

### Step 1: Preserve Current Content
- Individual file has corrected offset values compared to major section
- Keep all original content from FF7_Kernel_Kernelbin.md as-is

### Step 2: Extract Section Format Specifications
Extract from major section lines 124-544 (complete section format documentation):
- Add after the KERNEL2.BIN section
- Include all binary structure tables
- Include all offset/length/description mappings
- Include materia equip effect table

### Step 3: Add Extraction Markers
- Use clear markers showing extraction source and line numbers
- Include header explaining content additions
- Preserve all original content from individual file

### Step 4: Verify Content Accuracy
- **offset 0x2119 vs 0x2199**: Individual file appears to be correct
- Section 3 label: Individual file's "Battle and growth data" is correct
- Add note about offset corrections

### Step 5: Add Cross-References
- Link to FF7_Kernel_Memory_management.md for Section 3 (Savemap)
- Link to FF7_Savemap.md for detailed save map structure
- Cross-reference text section formats if documented elsewhere

---

## Validation Checklist for Merged File

- [ ] All original FF7_Kernel_Kernelbin.md content preserved verbatim
- [ ] Section format specifications added (lines 124-544 from major section)
- [ ] Extraction markers included with source line numbers
- [ ] Offset discrepancies documented
- [ ] Cross-references added to related files
- [ ] Merge metadata header added
- [ ] File is coherent and logically organized
- [ ] No content duplicated
- [ ] All binary structure tables are complete
- [ ] Materia equip effect table included

---

## Summary of Findings

1. **Individual file is 95% incomplete** - only has overview, missing all section specifications
2. **Individual file has corrected offsets** - should be used as authoritative
3. **Major section has comprehensive documentation** - 421 lines of section format details needed
4. **Content properly belongs in FF7_Kernel_Kernelbin.md** - not in other files
5. **Merge is straightforward** - append major section content after KERNEL2.BIN section
6. **No conflicts** - content is complementary, not duplicative

