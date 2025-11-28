# FF7_Kernel.md vs 03_KERNEL.md - Detailed Comparison Analysis

**Analysis Date**: 2025-11-28 14:30 JST
**Analyst**: Claude Code
**Purpose**: Identify content gaps between major section and individual file for merge operation

---

## Executive Summary

The `03_KERNEL.md` major section (1,641 lines, covering lines 216-1856 of the original 8,167-line file) aggregates content from **6 individual markdown files**. When compared to the primary individual file `FF7_Kernel.md`, there is **substantial content coverage in the major section that either doesn't exist in the individual file or is significantly less detailed**.

**Key Finding**: The individual `FF7_Kernel.md` is essentially a **navigation stub** (11 lines) containing only headings and links to related files, while the major section `03_KERNEL.md` contains **full technical documentation** on kernel functionality, memory management, game resources, and low-level libraries.

**Recommended Action**: Merge most of `03_KERNEL.md` into the individual file structure, distributing content appropriately across 6 related files.

---

## Topic Scope Analysis

### What FF7_Kernel.md Currently Contains
- TOC reference: 11 lines total
- Four linked file references:
  1. FF7/Kernel/Overview
  2. FF7/Kernel/Memory_management
  3. FF7/Kernel/Kernel.bin
  4. FF7/Kernel/Low_level_libraries
- No substantive content

### What 03_KERNEL.md Contains (1,641 lines)
- Kernel history and evolution (FF1 through FF7)
- Kernel functionality and architecture
- RAM and VRAM management systems
- PSX CD-ROM management
- Game resources and file structures
- KERNEL.BIN archive format and sections (27 detailed sections)
- KERNEL2.BIN archive specifications
- Low-level library comparisons (PSX vs PC)
- Data archive formats (BIN, LZS, LGP)
- Texture formats (TIM for PSX, TEX for PC)
- 3D model formats and structures
- HRC/RSD/P file format documentation
- Compression algorithms (LZS/LZSS detailed)

---

## Content Mapping to Individual Files

### Related Individual Files in Kernel Domain
1. **FF7_Kernel_Overview.md** (33 lines)
   - Contains: History, Kernel Functionality
   - Source in major: Lines 3-28 in 03_KERNEL.md (section I)

2. **FF7_Kernel_Memory_management.md** (69 lines)
   - Contains: RAM, VRAM, PSX CD-ROM management
   - Source in major: Lines 27-77 in 03_KERNEL.md (section II)

3. **FF7_Kernel_Kernelbin.md** (58 lines)
   - Contains: KERNEL.BIN and KERNEL2.BIN overview
   - Source in major: Lines 79-192 in 03_KERNEL.md (Game resources)

4. **FF7_Kernel_Low_level_libraries.md** (128 lines)
   - Contains: PC/PSX comparison, archive formats overview
   - Source in major: Lines 549-664 in 03_KERNEL.md (Section IV, partial)

5. **FF7_Savemap.md** (3,861 lines)
   - Contains: Detailed save data structures
   - **MINIMAL overlap** with major section (major only has brief reference)

### Individual File Sizes vs Content in Major Section

| File | Individual Size | Content in Major | Coverage | Status |
|------|-----------------|------------------|----------|--------|
| FF7_Kernel_Overview.md | 33 lines | ~40 lines | ~30% | Major section richer |
| FF7_Kernel_Memory_management.md | 69 lines | ~50 lines | ~70% | Similar coverage |
| FF7_Kernel_Kernelbin.md | 58 lines | ~115 lines | ~50% | Major section has more |
| FF7_Kernel_Low_level_libraries.md | 128 lines | ~115 lines (partial) | ~65% | Partial match |
| FF7_Savemap.md | 3,861 lines | ~1 line reference | <1% | Individual is much richer |

---

## Critical Gaps Identified

### Gap 1: KERNEL.BIN Detailed Section Formats
**Severity**: CRITICAL
**Location**: Lines 128-544 in 03_KERNEL.md
**Content Missing from FF7_Kernel_Kernelbin.md**: 
- Section 1: Command data format
- Section 2: Attacks data format
- Section 3: Savemap initialization
- Section 4: Initialization data
- Section 5: Item data format
- Section 6: Weapon data format
- Section 7: Armor data format
- Section 8: Accessory data format
- Section 9: Materia data format

**Line Count**: ~417 lines
**Impact**: Cannot parse KERNEL.BIN structure without this

### Gap 2: LZS Compression Algorithm Details
**Severity**: HIGH
**Location**: Lines 598-664 in 03_KERNEL.md
**Content Missing**: Detailed algorithm explanation, reference format, examples
**Line Count**: ~67 lines
**Impact**: Cannot implement LZS decompression correctly

### Gap 3: LGP Archive Format
**Severity**: HIGH
**Location**: Lines 666-737 in 03_KERNEL.md
**Content Missing**: Complete LGP structure (4 sections with details)
**Line Count**: ~72 lines
**Impact**: Cannot work with PC version LGP archives

### Gap 4: Texture Format Specifications
**Severity**: MEDIUM-HIGH
**Location**: Lines 746-865 in 03_KERNEL.md
**Content Missing**: TIM/TEX format tables and detailed specifications
**Line Count**: ~120 lines
**Impact**: Cannot parse texture files correctly

### Gap 5: 3D Model Format Documentation
**Severity**: MEDIUM
**Location**: Lines 866-1201 in 03_KERNEL.md
**Content Missing**: HRC, RSD, and P file format specifications
**Line Count**: ~336 lines
**Impact**: Limited ability to work with 3D models

---

## Extraction Summary Table

| Content | Lines | Start | End | Extract? |
|---------|-------|-------|-----|----------|
| KERNEL.BIN Sections 1-9 | 417 | 128 | 544 | YES |
| LZS Compression Detail | 67 | 598 | 664 | YES |
| LGP Archive Format | 72 | 666 | 737 | YES |
| Texture Formats | 120 | 746 | 865 | YES |
| 3D Model Formats | 336 | 866 | 1201 | YES |
| **TOTAL TO EXTRACT** | **982** | - | - | - |

---

## Files to Modify

1. **FF7_Kernel_Kernelbin.md** - Add KERNEL.BIN section format details (417 lines)
2. **FF7_Kernel_Low_level_libraries.md** - Add compression, archive, texture, and 3D formats (545+ lines)

---

## Conclusion

The major section `03_KERNEL.md` contains approximately **982 lines of substantive technical content** not present in the individual markdown files. This represents critical documentation that should be integrated to maintain comprehensive documentation.

