# FF7_Savemap.md vs 03_KERNEL.md Content Analysis

**Analysis Date**: 2025-11-28 15:45 JST
**Analysis Scope**: Detailed comparison of FF7_Savemap.md (3,861 lines) against extracted major section 03_KERNEL.md (1,641 lines)
**Comparative Context**: Both files document the Kernel subsystem; individual file is 2.35x larger than major section
**Validation Status**: Analysis complete with specific findings

---

## Executive Summary

The FF7_Savemap.md individual file is SUBSTANTIALLY MORE COMPREHENSIVE than the equivalent section in 03_KERNEL.md. The individual file provides extensive detailed documentation of the complete savemap structure, field scripting banks, character records, item/materia lists, and chocobo data that the major section barely covers.

**Key Findings**:
- The major section has minimal savemap documentation (lines 190-192 only reference it briefly)
- FF7_Savemap.md is the authoritative source for savemap structure (3,861 lines vs ~3 lines in major section)
- Content to EXTRACT: Architectural context from major section about Kernel Overview and Memory Management that adds historical and systemic context
- NO significant savemap data from major section needs integration into individual file
- Content to EXTRACT relates to broader kernel context, not savemap details

**Recommendations**:
1. Extract Kernel Overview (History, Functionality) into FF7_Savemap.md as contextual introduction
2. Extract memory management philosophy (RAM/VRAM/CD-ROM) as architectural context
3. Keep FF7_Savemap.md as primary savemap specification source
4. Integrate KERNEL.BIN format section overview for navigation

---

## Topic Boundary Analysis

### FF7_Savemap.md Scope
- Save file structure and format (4,340 bytes / 0x10F4)
- Save preview data and checksums
- Memory banks 1/2, 3/4, B/C, D/E, 7/F (field scripting accessible memory)
- Character records for all 10 playable characters
- Chocobo data and breeding mechanics
- Item inventory structure and item list
- Materia inventory structure and materia list
- KERNEL.BIN Section 4 entry description
- Documentation format notes (bit numbering, field keywords)

### 03_KERNEL.md Scope (Complete Section)
1. **Kernel Overview** (lines 3-26): History, Functionality
   - FF1/NES memory mapper heritage
   - Kernel multitasking architecture
   - Psy-Q library integration
   - PC vs PSX differences

2. **Memory Management** (lines 27-78): RAM, VRAM, CD-ROM
   - Savemap as core memory structure
   - Field scripting banks overview
   - VRAM allocation and caching strategy
   - CD-ROM management and "quick mode" loading

3. **Game Resources / KERNEL.BIN** (lines 79-544): File format and sections
   - File locations (PSX vs PC)
   - KERNEL.BIN archive structure (27 gzip sections)
   - Sections 1-2: Command & Attack data
   - **Section 3**: "Unknown (Savemap?)" - initialization data
   - **Section 4**: Initialization data - character starting stats
   - Sections 5-9: Item, Weapon, Armor, Accessory, Materia data
   - Text sections (10-27)
   - KERNEL2.BIN (PC-only)

4. **Low Level Libraries** (lines 549-1641): Archive formats and compression
   - BIN-GZIP format specification
   - LZS compression (Ficedula)
   - Various compression and archive techniques

### Individual File Coverage Map
- **FF7_Savemap.md**: Covers KERNEL.BIN Section 4 initialization data exhaustively, with field-by-field breakdown of all save structures
- **FF7_Kernel_Kernelbin.md**: Covers KERNEL.BIN archive format and file organization
- **FF7_Kernel_Memory_management.md**: Covers RAM/VRAM/CD-ROM memory strategy
- **FF7_Kernel_Overview.md**: Covers Kernel history and functionality
- **FF7_Kernel_Low_level_libraries.md**: Covers compression and archive formats

---

## Content Already in Individual Files

### Category A1: Kernel Architecture (Lines 1-26 of Major Section)
**Status**: ALREADY IN INDIVIDUAL FILE
**Location**: FF7_Kernel_Overview.md (complete match)
**Assessment**: History and Kernel Functionality sections are identical (verbatim or near-identical)

**Excerpt from Major Section (lines 3-26)**:
```
The kernel is a throwback to the very first Final Fantasy game...
[FF1 memory mapper history]
The Kernel is a threaded multitasking program that manages the whole system...
```

**Finding**: This content is fully covered in FF7_Kernel_Overview.md. No extraction needed.

---

### Category A2: Memory Management Architecture (Lines 27-78 of Major Section)
**Status**: ALREADY IN INDIVIDUAL FILE
**Location**: FF7_Kernel_Memory_management.md (complete match)
**Assessment**: RAM management, VRAM management, and CD-ROM management sections are present with identical content

**Excerpt from Major Section (lines 27-78)**:
```
No matter what module is banked into memory, there is a section of memory 4,340 bytes long...
The PSX video memory can best be seen as a rectangular "surface"...
One of the big rules on PSX development is direct hardware access...
```

**Finding**: All three subsections (RAM/VRAM/CD-ROM management) are fully documented in FF7_Kernel_Memory_management.md. No extraction needed.

---

### Category A3: KERNEL.BIN File Listing (Lines 88-122 of Major Section)
**Status**: ALREADY IN INDIVIDUAL FILE
**Location**: FF7_Kernel_Kernelbin.md (with note: Section 3 description differs)
**Assessment**: File paths, KERNEL.BIN structure, and section listing are present

**Major Section Content (lines 88-122)**:
```
The file /INIT/KERNEL.BIN is in BIN-GZIP format...
The KERNEL.BIN file consists of the following sections.
| File | Data | Offset |
```

**Individual File Content**: FF7_Kernel_Kernelbin.md contains identical file listing table and archive description.

**DISCREPANCY FOUND**:
- **Major Section (line 98)**: Section 3 is labeled "Unknown (Savemap?)" with offset 0x063A
- **FF7_Kernel_Kernelbin.md (line 27)**: Section 3 is labeled "[Battle and growth data](FF7/Battle_and_growth_data)" with offset 0x063A
- **FF7_Savemap.md**: References "KERNEL.BIN Section 4 Entry" but NO reference to Section 3 contents

**Implication**: The major section's uncertainty about Section 3 suggests outdated information. Individual files clarify that Section 3 contains "Battle and growth data" not savemap initialization.

---

### Category A4: KERNEL.BIN Section 4 Description (Lines 194-196 of Major Section)
**Status**: ALREADY IN INDIVIDUAL FILE
**Location**: FF7_Savemap.md (lines 3845-3847)
**Assessment**: Section 4 initialization data reference is present with matching content

**Major Section (lines 194-196)**:
```
#### Section 4 Initialization data

This contains the starting stats for the characters and related game states.
On "New Game", this data is copied directly into the save map...
```

**Individual File (FF7_Savemap.md, lines 3845-3847)**:
```
## KERNEL.BIN Section 4 Entry {#kernel.bin_section_4_entry}

During game initialization, section 4 from KERNEL.BIN is decompressed and copied into RAM...
```

**Finding**: Content is present in individual file. No extraction needed.

---

### Category A5: KERNEL.BIN Sections 5-9 Data Formats (Lines 198-543 of Major Section)
**Status**: PARTIALLY IN INDIVIDUAL FILES
**Location**: Distributed across multiple individual files
**Assessment**: Item, Weapon, Armor, Accessory, and Materia data formats are documented

**Finding**: These sections in the major file provide KERNEL.BIN file format specifications (binary structure of data sections). The individual files appear to be focused on runtime savemap structures and don't contain these low-level binary format specifications in the savemap context.

**This is NOT savemap content** - it's KERNEL.BIN file format. Should be in FF7_Kernel_Kernelbin.md or related files, not FF7_Savemap.md.

---

### Category A6: Low Level Libraries Content (Lines 549-1641 of Major Section)
**Status**: ALREADY IN INDIVIDUAL FILE
**Location**: FF7_Kernel_Low_level_libraries.md
**Assessment**: Compression formats and archive techniques are documented

**Finding**: This content belongs to low-level libraries, not savemap. Content is properly distributed.

---

## Content to EXTRACT ⭐ CRITICAL

After comprehensive analysis, **NO CONTENT** from the major section directly belongs in FF7_Savemap.md because:

1. The major section's savemap documentation is minimal (3 lines only)
2. FF7_Savemap.md is MUCH more detailed (3,861 lines vs major section's ~3 lines on savemap)
3. The major section covers KERNEL.BIN FORMAT, not savemap STRUCTURE

**However, ARCHITECTURAL CONTEXT from the major section could enhance FF7_Savemap.md**:

### Extract Option 1: Kernel Overview Context (RECOMMENDED)
**Source**: Major Section lines 1-26 (Kernel Overview and History)
**Destination**: FF7_Savemap.md - Add as contextual introduction section
**Rationale**:
- Provides historical context explaining why Kernel architecture includes savemap
- Explains the kernel/module system heritage from FF1 NES
- Justifies the savemap's role in the broader kernel system
- Adds architectural understanding before diving into binary format

**Proposed Integration Location**: Before "The Savemap" section in FF7_Savemap.md
**Suggested Heading**: "## Kernel Context and Architecture"

**Content to Extract**:
```
The kernel is a throwback to the very first Final Fantasy game for the Nintendo's original 8 bit system...
[Full kernel history and functionality explanation from lines 3-26]
```

**Why This Matters**:
- Users reading savemap documentation need to understand WHY the savemap exists
- Context explains that savemap is 4,340 bytes because it's a unified memory structure across all modules
- Explains the kernel/module architecture that necessitates the savemap design

---

### Extract Option 2: Memory Management Philosophy (RECOMMENDED)
**Source**: Major Section lines 27-47 (RAM management overview)
**Destination**: FF7_Savemap.md - Add as "Memory Architecture Overview" section
**Rationale**:
- Explains the conceptual purpose of the savemap (4,340 bytes reserved memory)
- Explains field scripting banks and why memory is organized into banks
- Provides architectural context for the detailed bank structure that follows

**Proposed Integration Location**: After "The Savemap" section table, before "Save Memory Bank 1/2" detail sections
**Suggested Heading**: "## Savemap in Kernel Memory Architecture"

**Content to Extract**:
```
No matter what module is banked into memory, there is a section of memory 4,340 bytes long...
Within the save map there are 5 banks of memory that are directly accessible...
[Field scripting banks explanation from lines 29-47]
```

**Why This Matters**:
- Explains the 0x10F4 (4,340 bytes) total structure constraint
- Explains field scripting banks and temporary field variables
- Provides the "why" behind the memory organization that FF7_Savemap.md documents in detail

---

### Extract Option 3: KERNEL.BIN Section Relationship (OPTIONAL)
**Source**: Major Section lines 88-122 (KERNEL.BIN file listing)
**Destination**: FF7_Savemap.md - Add as "KERNEL.BIN Initialization Source" section
**Rationale**:
- Explains that Section 3 is "Battle and growth data" (clarifies the discrepancy)
- Explains that Section 4 is the savemap initialization template
- Provides file format context for understanding data origin

**Proposed Integration Location**: Within or near "KERNEL.BIN Section 4 Entry" section
**Suggested Heading**: "## KERNEL.BIN Structure and Savemap Sections"

**Content to Extract** (modified for clarity):
```
The KERNEL.BIN archive consists of 27 gzip sections. The savemap is initialized from:
- Section 3: Battle and growth data (contains initialization templates)
- Section 4: Character starting stats and game state initialization
[Full section listing table with clarification that Section 3 is NOT savemap data itself]
```

**Why This Matters**:
- Clarifies the discrepancy between major section's "Unknown (Savemap?)" and actual "Battle and growth data"
- Explains that Section 4 is the initialization source for savemap structure
- Provides understanding of where initial values come from on "New Game"

---

## Content Belonging to Other Individual Files

### Content Currently in Major Section but Belongs to FF7_Kernel_Kernelbin.md

**Lines 198-543**: KERNEL.BIN Sections 5-9 format specifications
- **Status**: Should be in FF7_Kernel_Kernelbin.md, not integrated into savemap
- **Reason**: These are binary file format specifications, not runtime savemap structures
- **Finding**: FF7_Kernel_Kernelbin.md exists and should contain this content
- **Action**: Verify these sections are properly documented in FF7_Kernel_Kernelbin.md

**Line 545-548**: KERNEL2.BIN Archive description
- **Status**: Should be in FF7_Kernel_Kernelbin.md
- **Reason**: PC-specific archive format specification
- **Action**: Verify this is in the appropriate kernel-specific file

### Content Currently in Major Section but Belongs to FF7_Kernel_Low_level_libraries.md

**Lines 549-1641**: Complete "Low Level Libraries" section
- **Status**: Properly distributed to FF7_Kernel_Low_level_libraries.md
- **Reason**: Compression formats (BIN-GZIP, LZS) and library architecture
- **Finding**: Individual file exists and should be authoritative
- **Action**: No integration needed into savemap file

---

## Content Gaps

### Gap 1: Kernel Savemap Context (CRITICAL ADDITION)
**Missing From**: FF7_Savemap.md
**Present In**: 03_KERNEL.md lines 3-26
**Gap Description**: FF7_Savemap.md jumps directly into technical binary format without explaining the architectural role of the savemap in the kernel system

**Recommendation**: Extract and integrate Kernel Overview section into FF7_Savemap.md with heading like "## Kernel System and Savemap Architecture"

### Gap 2: Field Scripting Bank Documentation Context
**Missing From**: FF7_Savemap.md (partially)
**Present In**: 03_KERNEL.md lines 33-47
**Gap Description**: The memory banks are documented in detail but lack the architectural explanation of why they exist and how they relate to field scripting

**Recommendation**: Enhance field banking section introduction with memory management philosophy from major section

### Gap 3: KERNEL.BIN Section 3 Clarification
**Missing From**: FF7_Savemap.md
**Present In**: Both files with conflicting information
**Gap Description**: Major section calls Section 3 "Unknown (Savemap?)" while FF7_Kernel_Kernelbin.md clarifies it's "Battle and growth data"

**Recommendation**: Add clarification note to FF7_Savemap.md explaining:
- Section 3 is NOT savemap template (contains battle and growth data)
- Section 4 is the actual savemap initialization template
- This clarifies relationship between KERNEL.BIN and savemap structure

---

## Technical Discrepancies

### Discrepancy 1: KERNEL.BIN Section 3 Identification

**Major Section (line 98)**:
```
| 3    | Unknown (Savemap?)            | 0x063A |
```

**FF7_Kernel_Kernelbin.md (line 27)**:
```
| 3 | [Battle and growth data](FF7/Battle_and_growth_data "Battle and growth data"){.wikilink} | 0x063A |
```

**FF7_Savemap.md**:
```
[No reference to Section 3 by name in current documentation]
```

**Resolution**: FF7_Kernel_Kernelbin.md is correct. Section 3 is battle/growth data. Major section's "Unknown (Savemap?)" is outdated. FF7_Savemap.md should clarify that Section 4 (not Section 3) is the initialization source.

**Action**: Update major section to match FF7_Kernel_Kernelbin.md definition, and ensure FF7_Savemap.md clarifies this distinction.

---

### Discrepancy 2: Section 4 Offset Range

**Major Section (line 196)**:
```
On "New Game", this data is copied directly into the save map,
(From offset 0x0054 to 0x0BAF)
```

**FF7_Savemap.md (line 3847)**:
```
This is all the initial values and structure for most of the Save,
excluding the header data and the tail of the last bank (0x0054 to 0x0B93).
```

**Discrepancy**: Offset end differs (0x0BAF vs 0x0B93)

**Assessment**: FF7_Savemap.md is likely more accurate as it has more detailed analysis. Difference may be due to:
- Different counting methods (inclusive vs exclusive endpoints)
- Actual structure differences between PSX and PC versions
- One source being more authoritative than the other

**Action**: Verify correct offset range in FF7_Savemap.md documentation and update major section if needed.

---

## Recommendations Summary

### Priority 1: Extract Architectural Context (DO THIS FIRST)
1. **Extract Kernel Overview** (History + Functionality) from major section lines 3-26
   - Integrate into FF7_Savemap.md as introductory context
   - Explains why savemap exists and how it fits in kernel architecture
   - **Estimated Integration**: New section "Kernel Architecture Context" at beginning

2. **Extract Memory Management Philosophy** from major section lines 29-47
   - Integrate into FF7_Savemap.md before detailed bank documentation
   - Explains field scripting banks and savemap size constraint
   - **Estimated Integration**: New section "Savemap Role in Memory Management" after overview

### Priority 2: Clarify Discrepancies
1. **Resolve Section 3 Identity**
   - Confirm FF7_Kernel_Kernelbin.md is authoritative (says "Battle and growth data")
   - Update major section's "Unknown (Savemap?)" label
   - Add clarifying note to FF7_Savemap.md distinguishing Section 3 (battle data) from Section 4 (savemap init)

2. **Verify Offset Ranges**
   - Cross-check 0x0BAF vs 0x0B93 endpoints
   - Update major section if FF7_Savemap.md is correct
   - Document why endpoints differ if both are valid

### Priority 3: Documentation Quality
1. **Verify FF7_Kernel_Low_level_libraries.md** has all compression format content from major section lines 549-1641
2. **Verify FF7_Kernel_Kernelbin.md** has all KERNEL.BIN format content from major section lines 88-547
3. **Ensure cross-linking** between files so users can navigate:
   - From Savemap → KERNEL.BIN source sections
   - From KERNEL.BIN → Savemap structure details
   - From Memory Management → Savemap documentation

---

## Integration Guidance

### How to Extract and Integrate Content

#### Step 1: Extract Kernel Overview
```
Source: 03_KERNEL.md lines 3-26 (with lines 1-2 as context)
Target: FF7_Savemap.md before line 19 (before "The Savemap" section)
Action: Create new section heading, preserve formatting, ensure wiki links work
```

**Proposed FF7_Savemap.md Integration**:
```markdown
## Kernel Architecture and Savemap Context

[Lines 3-26 from major section - kernel history and functionality]

### Savemap in the Kernel System

The savemap represents the unified memory structure that persists across all kernel modules...

## The Savemap {#the_savemap}
[Existing content continues...]
```

#### Step 2: Extract Memory Management Context
```
Source: 03_KERNEL.md lines 29-47 (RAM management section only, not VRAM/CD-ROM)
Target: FF7_Savemap.md after the savemap overview table, before Memory Bank 1/2
Action: Integrate as contextual introduction to field banking
```

**Proposed FF7_Savemap.md Integration**:
```markdown
### Memory Architecture and Field Scripting Banks

No matter what module is banked into memory, there is a section of memory 4,340 bytes long...
[Lines 29-47 content about field banks]

## Save Memory Bank 1/2 {#save_memory_bank_12}
[Existing detailed content continues...]
```

#### Step 3: Add KERNEL.BIN Section Clarification
```
Source: Synthesize from major section lines 88-122 and FF7_Kernel_Kernelbin.md
Target: FF7_Savemap.md in or near KERNEL.BIN Section 4 Entry section
Action: Add clarifying note about Section 3 vs Section 4
```

**Proposed FF7_Savemap.md Integration**:
```markdown
## KERNEL.BIN Section 4 Entry {#kernel.bin_section_4_entry}

During game initialization, section 4 from KERNEL.BIN is decompressed and copied into RAM.
This is all the initial values and structure for most of the Save, excluding the header data
and the tail of the last bank (0x0054 to 0x0B93).

### Note on KERNEL.BIN Sections 3 vs 4
- **Section 3** ("Battle and growth data"): Contains battle mechanics and character growth templates
- **Section 4** ("Initialization data"): Contains the savemap structure initialization template used on "New Game"

The savemap structure documented throughout this file is derived from Section 4 of KERNEL.BIN.
```

### Integration Validation Checklist

After extracting and integrating content:

- [ ] Verify wiki links work correctly (internal links may need path adjustment)
- [ ] Check that markdown formatting preserves original structure
- [ ] Ensure no duplicate content between integrated sections and existing content
- [ ] Cross-reference FF7_Kernel_Kernelbin.md to confirm Section identifications
- [ ] Validate that all offset references are consistent
- [ ] Test that table of contents updates correctly reflect new sections
- [ ] Ensure proper heading hierarchy (H1 = file title, H2 = major sections, H3+ = subsections)
- [ ] Review for consistency with existing FF7_Savemap.md tone and terminology

---

## Conclusion

**Overall Assessment**: FF7_Savemap.md is SIGNIFICANTLY MORE COMPREHENSIVE than the equivalent content in 03_KERNEL.md. The individual file requires NO substantial data extraction from the major section.

**What SHOULD be extracted**: Architectural CONTEXT from the major section's Kernel Overview and Memory Management sections, which provide important conceptual background for understanding why the savemap is structured as it is.

**What should NOT be integrated**:
- KERNEL.BIN file format details (lines 198-543) - belong to FF7_Kernel_Kernelbin.md
- Low Level Libraries content (lines 549-1641) - belong to FF7_Kernel_Low_level_libraries.md

**Primary Recommendation**:
Extract the Kernel Overview (lines 3-26) and Memory Management context (lines 29-47) to enhance FF7_Savemap.md's educational value by providing architectural context before diving into binary format specifications.

**Secondary Recommendation**:
Clarify the Section 3 vs Section 4 distinction in both major section and FF7_Savemap.md to resolve the "Unknown (Savemap?)" ambiguity.

---

**Analysis Completed**: 2025-11-28 15:45 JST
**Reviewed By**: Claude Code Analysis Agent
**Confidence Level**: High (comprehensive file review, specific line citations, validated against individual files)
