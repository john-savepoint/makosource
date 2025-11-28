# Analysis: FF7_Kernel_Overview.md vs 03_KERNEL.md Major Section

**Date**: 2025-11-28 15:45 JST
**Analysis Type**: Content comparison and extraction assessment
**Individual File**: `markdown/FF7_Kernel_Overview.md`
**Major Section**: `extracted_major_sections/03_KERNEL.md`

---

## Executive Summary

The individual file `FF7_Kernel_Overview.md` (34 lines) contains only a brief, high-level overview of the FF7 kernel concept and its history. The major section `03_KERNEL.md` (1,641 lines) is a comprehensive technical document that covers **six distinct knowledge domains**:

1. **Kernel Overview** (History, Functionality) - partially in individual file
2. **Memory Management** - NOT in individual file
3. **Game Resources (KERNEL.BIN/KERNEL2.BIN formats)** - NOT in individual file
4. **Low-Level Libraries** (BIN, GZIP, LZS, LGP, TIM, texture formats) - NOT in individual file
5. **3D Model Formats** (PSX battle model `.p` file format) - NOT in individual file
6. **Grouping and Model Structure** (Complex vertex/polygon/edge chunking) - NOT in individual file

**Assessment**: The individual file is incomplete. It covers the conceptual overview only. The major section should be systematically distributed across 6 separate individual files according to topic boundaries.

---

## Topic Scope Analysis

### FF7_Kernel_Overview.md Scope (Current)

**What it covers** (34 lines total):
- Kernel concept and history (throwback to FF1)
- Memory mapping on NES (MMC1 controller)
- Basic kernel functionality overview
- Table showing kernel's position relative to other systems (Psy-Q libraries, BIOS, Hardware)

**What it's designed for**:
- Conceptual introduction to the kernel concept
- Historical context (why the kernel architecture exists)
- High-level system architecture diagram

### Related Individual Files in Kernel Domain

| File | Lines | Purpose | Current Content |
|------|-------|---------|-----------------|
| `FF7_Kernel.md` | 11 | Index/hub file | Links to: Overview, Memory Management, Kernel.bin, Low-level Libraries |
| `FF7_Kernel_Overview.md` | 34 | **CURRENT FILE** | Kernel history and functionality overview |
| `FF7_Kernel_Kernelbin.md` | 58+ | Kernel.bin/Kernel2.bin details | Archive format, section structure |
| `FF7_Kernel_Memory_management.md` | ? | RAM/VRAM management | Save map, video memory layouts |
| `FF7_Kernel_Low_level_libraries.md` | ? | Archive/compression formats | BIN, GZIP, LZS, LGP formats |
| `FF7_Savemap.md` | 3,861 | Save data structure | Detailed save map breakdown |

---

## Content Already in Individual File

### Lines 1-34: FF7_Kernel_Overview.md (Current Content)

**Overlapping content found in 03_KERNEL.md**:

- **Lines 1-26 (Overview TOC)**
  Corresponds to: Major section lines 1-26
  Content: Title, TOC structure
  Status: Identical, structurally equivalent

- **Lines 9-20 (History section)**
  Corresponds to: Major section lines 5-13
  Content: Kernel history (FF1, MMC1, memory banking, FF6 PSX port lag issue, PC integration)
  Status: Substantially equivalent

- **Lines 21-26 (Kernel Functionality)**
  Corresponds to: Major section lines 15-25
  Content: Kernel as multitasking program, RAM/VRAM memory manager, Psy-Q libraries, PSX BIOS table
  Status: Functionally equivalent

- **Lines 30-33 (Images section)**
  Corresponds to: Major section lines 26
  Content: Reference to Kernel_table.png
  Status: Present in both

---

## Content to Extract from Major Section

### Domain 1: Memory Management (Lines 27-78)

**Location in 03_KERNEL.md**: Lines 27-78
**Section Header**: "## *II. Memory management*"

**Subsections**:

1. **1.1 RAM management** (Lines 29-47)
   - Save map concept (4,340 bytes / 0x10F4)
   - Field script banks (5 banks with specific memory offsets)
   - Temporary field variables (256 bytes)
   - Table mapping: Offset → 8-bit Bank → 16-bit Bank → Description

2. **1.2 VRAM management** (Lines 49-71)
   - PSX VRAM as 2048x512 pixel surface
   - Multiple color depth support
   - VRAM diagram with buffer layout
   - Schematic showing: frame buffers, blank V-sync areas, movie buffers, CLUT, texture caches
   - Cache volatility and organization

3. **1.3 PSX CD-ROM management** (Lines 73-77)
   - BIOS hardware access restrictions
   - Module preloading during transitions
   - 8KB quick-mode loading
   - Sector-based file reference

**Recommendation**: Extract to `FF7_Kernel_Memory_management.md`

---

### Domain 2: KERNEL.BIN and KERNEL2.BIN Files (Lines 79-548)

**Location in 03_KERNEL.md**: Lines 79-548
**Section Header**: "## *III. Game resources*"

**Content includes**:
- KERNEL.BIN/KERNEL2.BIN file paths
- 27-section archive breakdown with offsets
- Detailed format specifications for:
  - Command data (16 bytes/record)
  - Attack data (28 bytes/record)
  - Savemap reference
  - Character initialization data
  - Item data (27 bytes/record)
  - Weapon data (44 bytes/record)
  - Armor data (36 bytes/record)
  - Accessory data (16 bytes/record)
  - Materia data (20 bytes/record)

**Recommendation**: Extract to expand `FF7_Kernel_Kernelbin.md`

---

### Domain 3: Low-Level Libraries (Lines 549-799+)

**Location in 03_KERNEL.md**: Lines 549-799+
**Section Header**: "## *IV. Low Level Libraries*"

**Content includes**:
- PC to PSX format comparison
- BIN archive types (uncompressed and GZIP)
- LZS compression algorithm with detailed example
- LGP archive format (all 4 sections, CRC, notes)
- TIM texture format (4bpp variant)

**Recommendation**: Extract to expand `FF7_Kernel_Low_level_libraries.md`

---

### Domain 4: 3D Model Formats (Lines 800-1200+)

**Location in 03_KERNEL.md**: Lines 800-1200+
**Content**: Detailed PSX 3D model format structure with chunks

**Note**: Cross-reference with `FF7_Playstation_Battle_Model_Format.md` (10,833 lines)

---

### Domain 5: Model Grouping and Structure (Lines 1257-1600+)

**Location in 03_KERNEL.md**: Lines 1257-1600+
**Content**: Complex explanation of model grouping with detailed diagrams

---

## Gaps and Discrepancies

| Gap | Severity | Impact | Solution |
|-----|----------|--------|----------|
| No memory management documentation | **HIGH** | Users can't understand Save Map or memory allocation | Extract lines 27-78 |
| No KERNEL.BIN/KERNEL2.BIN details | **HIGH** | Users can't understand file format | Extract lines 79-548 |
| No low-level library formats | **HIGH** | Users can't understand archive compression | Extract lines 549-799+ |
| No 3D model format documentation | **MEDIUM** | Users looking at model files confused | Cross-reference with PSX_Battle_Model |

---

## Specific Line Numbers for Extraction

### For FF7_Kernel_Overview.md (Current File)

**Content Already Present**: Lines 1-34 contain equivalent to major section lines 1-26

**Recommendation**: Keep as-is (minor refinements optional)

---

### For FF7_Kernel_Memory_management.md

**Extract from 03_KERNEL.md**:
- **Lines 27-47**: RAM management (Save Map, field script banks)
- **Lines 49-71**: VRAM management (PSX layout, texture caching)
- **Lines 73-77**: CD-ROM management

---

### For FF7_Kernel_Kernelbin.md

**Extract from 03_KERNEL.md**:
- **Lines 79-86**: Important Files table
- **Lines 88-123**: KERNEL.BIN overview and section table
- **Lines 124-544**: All section format details (Sections 1-9)
- **Lines 545-548**: KERNEL2.BIN archive specification

---

### For FF7_Kernel_Low_level_libraries.md

**Extract from 03_KERNEL.md**:
- **Lines 551-559**: PC to PSX comparison
- **Lines 561-591**: BIN archive types
- **Lines 592-654**: LZS compression (format, reference, example)
- **Lines 656-664**: LZS complications (negative offset, repeated run)
- **Lines 666-744**: LGP archive format (all 4 sections, notes, tools)
- **Lines 746-798**: TIM texture format (basic terms, 4bpp format)

---

## Merge Plan for FF7_Kernel_Overview.md

### Action: Create Merged Version

**Scope**: Update `FF7_Kernel_Overview.md` to include any unique overview content from major section

**Procedure**:
1. Copy original file
2. Add extraction markers for sections that should move to other files
3. Keep all original content intact
4. Add metadata about merge

**Expected Result**: Same content as original, with clear documentation of structure

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Major section total lines | 1,641 |
| Individual file current lines | 34 |
| Lines of overlap/equivalent content | ~26 |
| Lines of unique content to extract | ~1,600 |
| Number of domains covered | 6 |
| Related individual files in kernel domain | 6 |
| Files needing extraction | 4 |

---

## Next Steps

1. **Phase 1** (Current Task): Merge FF7_Kernel_Overview.md
2. **Phase 2**: Extract memory management content
3. **Phase 3**: Extract KERNEL.BIN content
4. **Phase 4**: Extract low-level libraries content
5. **Phase 5**: Review and extract 3D model content
