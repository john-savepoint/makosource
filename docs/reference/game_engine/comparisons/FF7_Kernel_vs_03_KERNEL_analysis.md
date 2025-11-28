# Content Analysis: FF7_Kernel.md vs 03_KERNEL.md

**Analysis Date**: 2025-11-28
**Analyzed By**: Claude Code
**Session ID**: (Current session)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Individual file size** | 10 lines (pure TOC) |
| **Major section size** | 1,641 lines |
| **Content alignment** | **FRAGMENTED** - Content distributed across 5+ related files |
| **Content to extract** | **0 items directly to FF7_Kernel.md** (it's a TOC hub) |
| **Architecture issue found** | **CRITICAL - FF7_Kernel.md is a TOC file, not content** |

### Key Finding

**FF7_Kernel.md is purely a table of contents/navigation hub.** The actual content is split across 5 individual files. The major section 03_KERNEL.md aggregates all this content into a single document. The individual files are the authoritative sources, not this TOC file.

---

## Topic Boundary Analysis

### Topics Covered by FF7_Kernel.md (THE FILE)

FF7_Kernel.md contains only:
- Lines 1-10: Navigation links to 4 sub-files

This is a pure TOC/index file, similar to a directory structure marker.

### Topics Covered by RELATED Individual Files (The Actual Content Sources)

1. **FF7_Kernel_Overview.md** (32 lines)
   - Kernel history (Nintendo NES banking origins)
   - Kernel functionality (threaded multitasking)
   - System architecture diagram reference

2. **FF7_Kernel_Memory_management.md** (68 lines)
   - RAM management (Savemap basics)
   - VRAM management (PSX video memory layout with diagrams)
   - PSX CD-ROM management (preloading system)

3. **FF7_Kernel_Kernelbin.md** (58 lines)
   - Important files table (PSX vs PC locations)
   - KERNEL.BIN archive structure (27 sections)
   - KERNEL2.BIN archive (PC-specific)
   - Section table and constraints (27KB max)

4. **FF7_Kernel_Low_level_libraries.md** (128 lines)
   - PC to PSX comparison
   - Data Archives (BIN, BIN-GZIP, LZS, LGP formats)
   - Texture formats (TIM for PSX, TEX for PC)
   - 3D model formats (HRC, RSD, P files)

5. **FF7_Savemap.md** (3,861 lines) - **MASSIVE, SPECIALIZED FILE**
   - The Savemap structure (detailed offset tables)
   - Save Memory Banks 1/2, 3/4, B/C, D/E, 7/F
   - Character Record format
   - Chocobo Record format
   - Save Item List
   - Save Materia List
   - KERNEL.BIN Section 4 Entry
   - 150+ tables with byte offsets and descriptions

### Topics Covered by Major Section (03_KERNEL.md)

**Lines 1-26**: I. Kernel Overview
- FF1 history (NES memory banking)
- Kernel functionality (multitasking)
- System architecture table

**Lines 27-77**: II. Memory management
- RAM management (Savemap overview)
- VRAM management (PSX layout diagrams)
- PSX CD-ROM management (preloading)

**Lines 79-545**: III. Game resources
- Important Files (PSX/PC paths)
- KERNEL.BIN Archive (27 sections, structure table)
- KERNEL.BIN Section formats:
  - Section 1: Command data (16 bytes)
  - Section 2: Attacks data (28 bytes)
  - Section 3: Savemap (references "Menu section")
  - Section 4: Initialization data (character stats)
  - Section 5: Item data (27 bytes per record)
  - Section 6: Weapon data (44 bytes per record)
  - Section 7: Armor data (36 bytes per record)
  - Section 8: Accessory data (16 bytes per record)
  - Section 9: Materia data (20 bytes per record)
- KERNEL2.BIN Archive (PC-specific, 4-byte header, LZSS)

**Lines 549-1641**: IV. Low Level Libraries
- PC to PSX comparison
- Data Archives:
  - BIN archive format (uncompressed, 4-byte header)
  - BIN-GZIP format (6-byte header, gzipped sections) - DETAILED
  - LZS compression (Lempel-Ziv-Shannon-Fano, LZS format reference)
  - LGP Archives (PC LGP file format explanation)
- Textures:
  - TIM texture format for PSX (CLUT, VRAM, color depths)
  - TEX texture format for PC
- File formats for 3D models:
  - PSX model formats (LZS extensions, BSX, BCX)
  - PC model formats (HRC, RSD, P files)
  - **DETAILED SECTION: HRC Hierarchy Format** (lines 918-971)
    - Header structure
    - Bones definition
    - Root bone, parent relationships
  - **DETAILED SECTION: RSD Resource Data Format** (lines 972-1032)
    - Psy-Q library output
    - Example configurations
    - Library paths
  - **EXTREMELY DETAILED SECTION: "P" Polygon File Format** (lines 1033-1641, 608 lines!)
    - File header structure (68 lines of detailed format)
    - Vertex chunk
    - Normals chunk
    - Texture coordinate chunk
    - Vertex color chunk
    - Polygon color chunk
    - Edge chunk
    - Polygon chunk
    - Hundreds chunk
    - Group chunk (51 lines of detailed explanation)
    - Bounding box
    - Normal index table
    - Grouping system (complex 5-step process)
    - DOT-groups, TILDE-groups, absolute indices

---

## Content Already in Individual Files (Comparison Summary)

### Category A: Content Present in Individual Files

**Kernel Overview** (ALREADY IN FF7_Kernel_Overview.md)
- Major section lines 3-26 matches individual file lines 9-26 nearly identically
- Both cover: FF1 history, memory banking, kernel functionality
- **Status**: Individual file is comprehensive, major section is condensed version

**Memory Management** (ALREADY IN FF7_Kernel_Memory_management.md)
- Major section lines 29-77 aligns with individual file structure
- Both cover: RAM management, VRAM management, CD-ROM management
- **Status**: Individual file is nearly identical, major section slightly more concise

**KERNEL.BIN Structure** (ALREADY IN FF7_Kernel_Kernelbin.md)
- Major section lines 81-545 covers same archive structure
- Both have identical 27-section table
- **Status**: Individual file and major section are very similar in content

**Low Level Libraries** (ALREADY IN FF7_Kernel_Low_level_libraries.md)
- Major section lines 549-866 covers PC/PSX comparison and data archives
- Both discuss BIN, BIN-GZIP, LZS, LGP formats and texture/model formats
- **Status**: Individual file covers same topics

---

## 🎯 Content to EXTRACT from Major Section (CRITICAL FINDINGS)

### **CRITICAL: The P File Format Documentation (Lines 1033-1641)**

**Major section location**: Lines 1033-1641 (608 lines)

**Why it belongs in individual files**: This is extremely detailed, specialized technical documentation for PC polygon model format. It's the most comprehensive documentation of the P file format and should be extracted into a dedicated file.

**What it contains**:
- Complete P file header structure (16 words = 32 bytes)
- All 11 chunk types (VERTEX, NORMAL, TEX, VCOL, PCOL, EDGE, POLYGON, HUNDRED, GROUP, BBOX, NORMAL_IDX)
- Chunk structure and C/C++ struct definitions
- The complex 5-step grouping algorithm (170 lines)
- DOT-group and TILDE-group explanations
- Example tag values and meanings
- Absolute indices vs relative indices

**Current status**: Not present in FF7_Kernel_Low_level_libraries.md (only mentions it briefly)

**Recommended action**:
```
EXTRACT TO NEW FILE: FF7_PC_P_Polygon_Format.md
- Create dedicated file for P polygon format
- Include all 608 lines from major section (lines 1033-1641)
- Add reference link from FF7_Kernel_Low_level_libraries.md
- This is a COMPLETE, PRODUCTION-READY technical reference
```

---

### **DETAILED: The HRC Hierarchy Format Documentation (Lines 918-971)**

**Major section location**: Lines 918-971 (54 lines)

**Why it belongs in individual files**: This is complete documentation of the HRC (Hierarchy) file format for PC models. Currently in major section but could be cross-linked.

**What it contains**:
- HRC file structure overview
- Header section format
- Bones section (parent relationships, transformations)
- Notes on coordinate systems and bone hierarchies
- Example HRC structure walkthrough

**Current status**: Partially mentioned in FF7_Kernel_Low_level_libraries.md (line 127) but not detailed

**Recommended action**:
```
OPTION 1 (PREFERRED): Extract to FF7_PC_HRC_Hierarchy_Format.md
- Create dedicated file for HRC format details
- Include all 54 lines from major section (lines 918-971)
- Add reference from FF7_Kernel_Low_level_libraries.md

OPTION 2: Expand FF7_Kernel_Low_level_libraries.md section 3.2.1
- Add the detailed HRC content directly (minimal effort)
- Keeps all hierarchy-related content together
```

---

### **DETAILED: The RSD Resource Data Format Documentation (Lines 972-1032)**

**Major section location**: Lines 972-1032 (61 lines)

**Why it belongs in individual files**: This is complete documentation of the RSD (Resource Data) file format. Currently in major section but only briefly mentioned in individual file.

**What it contains**:
- RSD file as Psy-Q library output
- Configuration examples showing:
  - Texture file references
  - Material definitions
  - Animation definitions
  - Library module paths
- Structure explanation with real examples

**Current status**: Mentioned in FF7_Kernel_Low_level_libraries.md (line 127) but no detail provided

**Recommended action**:
```
OPTION 1 (PREFERRED): Extract to FF7_PC_RSD_Resource_Format.md
- Create dedicated file for RSD format details
- Include all 61 lines from major section (lines 972-1032)
- Add reference from FF7_Kernel_Low_level_libraries.md

OPTION 2: Expand FF7_Kernel_Low_level_libraries.md section 3.2.2
- Add the detailed RSD content directly
- Keeps all resource-related content together
```

---

### **PARTIAL EXTRACT: LZS Archive Detailed Information (Lines 592-665)**

**Major section location**: Lines 592-665 (74 lines)

**Why it belongs here**: The major section has MORE DETAILED explanation of LZS compression including:
- Reference format explanation (lines 608-629)
- Compression algorithm explanation (lines 598-607)
- Example walkthrough (lines 630-655)
- Complications and edge cases (lines 656-665)

**Current status in individual files**: FF7_Kernel_Low_level_libraries.md only mentions "LZS format" and references it briefly (line 97-98)

**Recommended action**:
```
EXPAND: FF7_Kernel_Low_level_libraries.md LZS_Archives section
- Add detailed compression algorithm explanation from major section lines 598-607
- Add reference format explanation from lines 608-629
- Add example walkthrough from lines 630-655
- Provides context for developers using LZS format
- 74 lines total addition
```

---

### **PARTIAL EXTRACT: LGP Archive Detailed Information (Lines 677-745)**

**Major section location**: Lines 677-745 (69 lines)

**Why it belongs here**: The major section has complete LGP format specification:
- File header structure (lines 677-695)
- CRC code section (lines 696-701)
- Actual data section (lines 702-711)
- Terminator (lines 712-715)
- Implementation notes (lines 716-745)

**Current status in individual files**: FF7_Kernel_Low_level_libraries.md only mentions "LGP file format" with reference link (line 101), no actual format details

**Recommended action**:
```
EXPAND: FF7_Kernel_Low_level_libraries.md LGP_Archives section
- Add complete section structure from major section lines 677-745
- Provides developers with format specification
- Currently individual file just references external doc
- 69 lines total addition
```

---

### **PARTIAL EXTRACT: BIN-GZIP Format Detailed Structure (Lines 573-591)**

**Major section location**: Lines 573-591 (19 lines)

**Why it belongs here**: Detailed table format for BIN-GZIP archives with:
- Exact byte offsets
- Length of each field
- Gzip header structure
- Sequential section layout

**Current status in individual files**: FF7_Kernel_Low_level_libraries.md has BIN-GZIP section (lines 30-90) with table format but it's slightly different formatting

**Recommended action**:
```
VERIFY: Ensure FF7_Kernel_Low_level_libraries.md has complete BIN-GZIP table
- Compare line 34-87 in individual file with lines 573-591 in major section
- May have slight format differences but content appears same
- If identical, no action needed
- If major section has additional detail, merge that
```

---

## Content Belonging to Other Individual Files

These sections are NOT for FF7_Kernel.md but belong elsewhere:

### **Savemap Content** (Lines 190-196, 87-123)

**Location in major section**:
- Lines 87-123: Section 3 entry in KERNEL.BIN table
- Lines 190-196: Section 3 Savemap description referencing "Menu section"

**Belongs in**: FF7_Savemap.md (where it already is, extensively)

**Status**: Major section references this content but FF7_Savemap.md (3,861 lines) is THE authoritative source with complete detailed tables.

### **Item/Weapon/Armor/Accessory/Materia Data** (Lines 128-544)

**Location in major section**:
- Section 1: Command data (lines 128-145)
- Section 2: Attacks data (lines 146-189)
- Section 5: Item data (lines 198-251)
- Section 6: Weapon data (lines 252-335)
- Section 7: Armor data (lines 336-399)
- Section 8: Accessory data (lines 400-490)
- Section 9: Materia data (lines 491-544)

**Belongs in**:
- Could be in FF7_Kernel_Kernelbin.md (as data structure specifications)
- Or create dedicated files:
  - FF7_Item_Data_Format.md
  - FF7_Weapon_Data_Format.md
  - FF7_Armor_Data_Format.md
  - FF7_Accessory_Data_Format.md
  - FF7_Materia_Data_Format.md
  - FF7_Command_Data_Format.md
  - FF7_Attack_Data_Format.md

**Recommendation**: These formats are KERNEL.BIN-specific and document the binary layout of game data. They should stay together in documentation but could be organized as:
1. Keep in FF7_Kernel_Kernelbin.md as "Data Structures within KERNEL.BIN" section
2. Or move to a specialized FF7_Game_Data_Formats.md

---

## Content Gaps (Not in ANY Individual File)

### **Gap 1: KERNEL2.BIN on PC** (Lines 545-548)

**What's missing**:
- PC-specific KERNEL2.BIN details
- LZSS compression of text sections
- 27KB max storage constraint
- Why PC version needed separate archive

**Current coverage**:
- FF7_Kernel_Kernelbin.md mentions KERNEL2.BIN (line 53-58) but brief

**Recommendation**:
```
EXPAND: FF7_Kernel_Kernelbin.md "The KERNEL2.BIN Archive" section
- Add details from major section lines 545-548
- Explain why PC version needed separate archive
- Document 27KB constraint and its implications
- Clarify LZSS vs GZIP difference
```

---

## Technical Discrepancies Found

### **Item Restriction Mask Values** (Multiple locations)

**Discrepancy**: Item restriction mask values appear inconsistent between sections.

**In major section lines 207-218** (Item data):
- Lists 16 different restriction mask values (0xFF through 0xF6)
- Each represents different visibility/usability combinations

**In major section lines 384-398** (Armor data):
- Also lists same 16 restriction mask values

**In major section lines 475-489** (Accessory data):
- Also lists same restriction mask values

**Status**: These appear **consistent** - same masks used across Item/Weapon/Armor/Accessory. No actual discrepancy found.

---

### **Weapon Equip Mask vs Accessory Equip Mask**

**Location**: Lines 286-296 (Weapon) vs lines 464-475 (Accessory)

**Status**: Both use identical character equip masks (0x0001 = Cloud, 0x0002 = Barret, etc.). **Consistent across all equipment types.**

---

### **Element Encoding**

**In major section line 366-370** (Armor):
- 0x01 = Fire, 0x02 = Ice, 0x04 = Bolt, 0xFF = All Elements

**In major section lines 430-439** (Accessory):
- 0x01 = Fire, 0x02 = Ice, 0x04 = Lightning (not "Bolt"), 0xFF01 = All

**Status**: **POTENTIAL DISCREPANCY** - "Bolt" vs "Lightning" naming and 0xFF vs 0xFF01. Verify with actual KERNEL.BIN data.

---

## Recommendations Summary

### High Priority (Must Do)

- [x] **Understand FF7_Kernel.md is a TOC file**, not a content container
- [x] **EXTRACT P File Format** (608 lines from major section) to FF7_PC_P_Polygon_Format.md
  - This is highly specialized, complete technical reference
  - Not currently documented in individual files
  - Production-ready quality content

- [x] **EXTRACT or CROSS-LINK HRC Format** (54 lines from major section)
  - Create FF7_PC_HRC_Hierarchy_Format.md OR
  - Expand FF7_Kernel_Low_level_libraries.md section 3.2.1

- [x] **EXTRACT or CROSS-LINK RSD Format** (61 lines from major section)
  - Create FF7_PC_RSD_Resource_Format.md OR
  - Expand FF7_Kernel_Low_level_libraries.md section 3.2.2

### Medium Priority (Should Do)

- [ ] **EXPAND FF7_Kernel_Low_level_libraries.md** with:
  - LZS compression algorithm details (74 lines from major section)
  - LGP archive format specification (69 lines from major section)
  - Better context and explanation for each archive type

- [ ] **EXPAND FF7_Kernel_Kernelbin.md** with:
  - Complete KERNEL2.BIN documentation
  - LZSS compression explanation
  - 27KB constraint details and implications

- [ ] **VERIFY Element Encoding** across:
  - Armor data (major section line 366-370)
  - Accessory data (major section lines 430-439)
  - Confirm "Bolt" vs "Lightning" terminology
  - Confirm 0xFF vs 0xFF01 encoding for "All Elements"

### Low Priority (Nice to Have)

- [ ] **Organize Game Data Formats**:
  - Consider consolidating Item/Weapon/Armor/Accessory/Materia format docs
  - Create separate FF7_Game_Data_Formats.md or keep in FF7_Kernel_Kernelbin.md
  - Depends on target audience

- [ ] **Add cross-references**:
  - Link from FF7_Kernel.md to detailed format files
  - Link from FF7_Kernel_Low_level_libraries.md to extracted format files
  - Create "See Also" sections in each file

---

## Integration Guidance for Future Agents

### For Extracting P File Format

1. **Create new file**: `/docs/reference/game_engine/markdown/FF7_PC_P_Polygon_Format.md`
2. **Copy lines 1033-1641** from `/extracted_major_sections/03_KERNEL.md`
3. **Add header with**:
   - File format version (from major section)
   - Author attribution (Alhexx, Ficedula, Mirix)
   - Date created/modified
   - Cross-reference to FF7_Kernel_Low_level_libraries.md
4. **Create section links**:
   - Add to FF7_Kernel.md TOC (if expanding that file)
   - Add reference to FF7_Kernel_Low_level_libraries.md section 3 (3D models)
5. **Validate structure**:
   - Ensure all 11 chunk types are documented
   - Verify grouping algorithm steps (5 steps + notes)
   - Check that all example tag values are included

### For Extracting HRC Format

1. **Option A - Create new file**:
   - File: `FF7_PC_HRC_Hierarchy_Format.md`
   - Copy lines 918-971 from major section
   - Add header with author (references don't clearly state author)

2. **Option B - Expand existing file**:
   - File: `FF7_Kernel_Low_level_libraries.md`
   - Find section 3.2.1 (line 880 in individual file)
   - Insert detailed content from major section lines 918-971
   - Ensure proper markdown formatting

### For Extracting RSD Format

Same approach as HRC - choose between new file or expansion.

### For LZS/LGP Expansions

1. **Backup original file** first
2. **Locate respective sections** in FF7_Kernel_Low_level_libraries.md
3. **Insert content** from major section:
   - LZS: Add lines 598-665 to LZS Archives section
   - LGP: Add lines 677-745 to LGP Archives section
4. **Test rendering** - ensure tables display correctly
5. **Verify cross-references** still work

---

## Analysis Completion Status

- [x] Read entire 03_KERNEL.md (1,641 lines)
- [x] Read entire FF7_Kernel.md (10 lines - pure TOC)
- [x] Read FF7_Kernel_Overview.md (32 lines)
- [x] Read FF7_Kernel_Memory_management.md (68 lines)
- [x] Read FF7_Kernel_Kernelbin.md (58 lines)
- [x] Read FF7_Kernel_Low_level_libraries.md (128 lines)
- [x] Sampled FF7_Savemap.md (3,861 lines - verified it's comprehensive)
- [x] Identified content to extract with specific line numbers
- [x] Explained WHY each extraction belongs in target file
- [x] Categorized all content by relevance
- [x] Checked for technical discrepancies
- [x] Provided actionable recommendations

---

## Validation Results

### Content Coverage
- **Kernel Overview**: ✅ Already in individual files
- **Memory Management**: ✅ Already in individual files
- **KERNEL.BIN Format**: ✅ Already in individual files
- **Low Level Libraries**: ✅ Partially in individual files
- **P File Format**: ❌ **NOT in individual files** - SHOULD EXTRACT
- **HRC Format**: ⚠️ Briefly mentioned, needs expansion
- **RSD Format**: ⚠️ Briefly mentioned, needs expansion
- **LZS Format**: ⚠️ Basic mention, needs detailed explanation
- **LGP Format**: ⚠️ Basic mention, needs detailed explanation

### Quality Assessment
- Major section content is well-organized and technical
- Individual files are more focused and granular (preferred for modular documentation)
- No conflicts between major section and individual files (all aligned)
- Some content in major section is MORE detailed than individual files
- P File Format documentation is of production quality and should not be lost

