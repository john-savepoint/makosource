# FF7 Kernel Memory Management - Content Analysis Report

**Analysis Date**: 2025-11-28
**Session ID**: Current Analysis Session
**Files Compared**:
- Source: `/docs/reference/game_engine/extracted_major_sections/03_KERNEL.md` (Lines 27-77)
- Target: `/docs/reference/game_engine/markdown/FF7_Kernel_Memory_management.md`

---

## Executive Summary

The `FF7_Kernel_Memory_management.md` individual file contains substantially similar content to the memory management section found in the major `03_KERNEL.md` file. However, there are **structural differences and some unique content in the major section** that should be extracted and integrated into the individual file.

**Key Finding**: The major section has **slightly different formatting, more detailed VRAM descriptions, and different explanatory text** that enhances understanding of the memory management systems.

---

## Topic Scope Analysis

### FF7_Kernel_Memory_management.md Coverage

The individual file covers three main memory topics:

1. **RAM Management** - Savemap structure, field script banks, temporary variables
2. **VRAM Management** - Video RAM allocation, caching, texture organization
3. **PSX CD-ROM Management** - Hardware access restrictions, module preloading

### Related Files in the Kernel Domain

**Files that should NOT receive this content**:
- `FF7_Kernel.md` - Navigation/index file only
- `FF7_Kernel_Overview.md` - History and kernel architecture (lines 1-46 of major section)
- `FF7_Kernel_Kernelbin.md` - KERNEL.BIN structure and format (lines 88+)
- `FF7_Kernel_Low_level_libraries.md` - Library documentation
- `FF7_Savemap.md` - Detailed savemap structure (this is referenced in memory management)

**Boundary Clarification**: While `FF7_Savemap.md` exists and contains much more detail (3,861 lines), the memory management section should maintain a reference to it while focusing on the high-level memory banking concept.

---

## Content Already in Individual File

The `FF7_Kernel_Memory_management.md` file already contains:

1. **RAM Management Section**
   - Explanation of Savemap (4,340 bytes / 0x10F4)
   - Five field script banks with memory addresses
   - Temporary field variables allocation
   - Reference table with offsets and descriptions

2. **VRAM Management Section**
   - Overview of 1MB PSX VRAM constraint
   - VRAM as 1024x512 pixel matrix
   - Description of video buffer and back buffer
   - Texture cache organization and volatility

3. **PSX CD-ROM Management Section**
   - Hardware access restrictions via BIOS
   - Module preloading during transitions
   - "Quick mode" loading mechanism (8KB chunks)
   - Sector-based referencing instead of filenames

4. **Images**
   - Reference to Gears_img_3.jpg (VRAM layout during gameplay)
   - Reference to Gears_img_4.jpg (VRAM schematic with texture boundaries)

---

## Content from Major Section to Extract

### Unique/Enhanced Content in 03_KERNEL.md

#### 1. Enhanced RAM Management Explanation (Lines 29-33)

**Major Section Text:**
```
No matter what module is banked into memory, there is a section of memory 4,340 bytes long (0x10F4 bytes) that is reserved for all the variables for the entire game. This entire image is called the "Save Map". When it's time to save a game, this section of memory is copied to non-volatile ram, such as a hard disk or memory card.

Within the save map there are 5 banks of memory that are directly accessible by the field scripting language. These can either be accessed 8 bits or 16 bits at a time depending on the field command argument. The following table is basic memory map of the banks and how they relate to the save map. There is also an allocation for 256 bytes for temporary field variables. These are not used between field files and are not saved.
```

**Status**: Individual file has nearly identical content (lines 10-14). The major section uses "Save Map" (capitalized) while individual uses "Savemap".

**Action**: Already present, no extraction needed. Note the capitalization variance.

---

#### 2. Enhanced Memory Map Table (Lines 35-45)

**CRITICAL DATA DISCREPANCY FOUND**:
- Major section Bank 5: 0x0FA4 | 0x7 (8-bit) | 0xF (16-bit)
- Individual file Bank 5: 0x0FA4 | 0xF (8-bit) | 0x7 (16-bit)

**This must be resolved before merging** - data accuracy is critical.

**Action**: REQUIRES VERIFICATION against original source before proceeding.

---

#### 3. Contextual Note About Menu Section (Line 47)

**Major Section Text:**
```
A more complete and annotated save map is in the MENU section.
```

**Individual File**: Has no such reference.

**Action**: Extract this as a helpful reference/pointer to additional documentation.

---

#### 4. Enhanced VRAM Management Explanation (Lines 49-71)

The major section provides detailed textual explanations:

- Detailed VRAM layout descriptions (lines 59-71)
- Explanation of double-page buffering
- CLUT (Color Look Up Tables) explanation
- Texture cache boundaries and volatility patterns

**Status**: Individual file has very similar content.

**Action**: Text is nearly identical - no extraction needed unless standardizing language.

---

#### 5. PSX CD-ROM Management (Lines 73-77)

**Minor Differences**:
- Major: "direct hardware access is a prohibited"
- Individual: "that direct hardware access is a prohibited" (grammar variation)
- Major: "lowlevel" vs Individual: "low-level" (hyphenation)
- Major: "The in this mode" vs Individual: "In this mode"

**Status**: Content essentially identical, individual file has slightly better grammar.

**Action**: No extraction needed.

---

## Content Belonging to Other Files

The following content appears in 03_KERNEL.md but belongs in different individual files:

### Kernel Overview Content (Lines 1-26)
- History section
- Kernel Functionality section  
- Kernel architecture diagram
- **Belongs in**: `FF7_Kernel_Overview.md` (already present)

### KERNEL.BIN Content (Lines 79-122 and beyond)
- Important files references
- KERNEL.BIN archive structure
- Section descriptions
- **Belongs in**: `FF7_Kernel_Kernelbin.md` (already present)

---

## Gaps and Discrepancies

### 1. CRITICAL: Bank 5 Memory Values Differ

| Source | 8-Bit Bank | 16-Bit Bank |
|--------|-----------|------------|
| Major Section (03_KERNEL.md line 42) | 0x7 | 0xF |
| Individual File (FF7_Kernel_Memory_management.md line 23) | 0xF | 0x7 |

**This requires source code verification before finalizing merge.**

### 2. Capitalization: "Savemap" vs "Save Map"
- Major section: "Save Map" (two words)
- Individual file: "Savemap" (one word)
- **Recommendation**: Standardize across documentation

### 3. Grammar Variations
- Individual file is slightly more grammatically correct in CD-ROM section
- "low-level" vs "lowlevel" hyphenation

---

## Merge Plan

### Phase 1: Pre-Merge Validation (CRITICAL)

- **MUST VERIFY**: Bank 5 memory address values against original source before any merge
- Decide capitalization standard for "Savemap" / "Save Map"
- Confirm image file locations

### Phase 2: Merge Strategy

**Target for merging**: `FF7_Kernel_Memory_management.md` (individual file)

**Merge approach**:
1. Copy original file to `/markdown/merged_with_pdf_content/`
2. Add extraction markers showing content source
3. Include reference note about Menu section
4. Preserve ALL original content - nothing removed
5. Add metadata indicating merge source and date

### Phase 3: Content to Extract from 03_KERNEL.md

1. **Line 47**: Contextual reference to Menu section
2. **Line 29-45**: Memory map context (verify Bank 5 values first)
3. **Preserve all original explanatory text** from both sources

---

## Validation Checklist

- [x] Analyzed individual file (FF7_Kernel_Memory_management.md)
- [x] Analyzed major section (03_KERNEL.md lines 27-77)
- [x] Identified data discrepancies (Bank 5 - CRITICAL)
- [x] Identified unique content
- [x] Mapped all relevant line numbers
- [x] Identified content belonging to other files
- [ ] PENDING: Verify Bank 5 memory values from source
- [ ] Create merged file with extraction markers
- [ ] Add merge metadata
- [ ] Final validation

---

## Conclusion

Content in both files is **95% identical** with only minor differences:
- One CRITICAL data discrepancy (Bank 5 values)
- Grammar improvements available in individual file
- Capitalization inconsistencies

**The main value of merging is**:
1. Capturing cross-references (Menu section note)
2. Standardizing format and terminology
3. Preserving provenance with extraction markers

**BLOCKING ISSUE**: Bank 5 memory values must be verified against original source before finalizing merge. Cannot proceed with Phase 2 until this is resolved.
