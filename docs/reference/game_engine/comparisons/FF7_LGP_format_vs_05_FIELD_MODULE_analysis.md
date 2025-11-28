# FF7_LGP_format.md vs 05_FIELD_MODULE.md - Content Analysis Report

**Created**: 2025-11-29 JST
**Analysis Type**: Two-phase content comparison and merge preparation
**Individual File**: FF7_LGP_format.md (102 lines)
**Major Section**: 05_FIELD_MODULE.md (2,645 lines)
**Status**: No substantive additions identified for extraction

---

## Executive Summary

### File Scope and Alignment

| Metric | Value |
|--------|-------|
| Individual file size | 102 lines |
| Major section size | 2,645 lines |
| Topical overlap | ~5-10 lines (mentions only) |
| Substantive LGP format content in major section | NONE |
| Images to extract | 0 |

### Key Finding

**The major section 05_FIELD_MODULE.md does NOT contain detailed information about the LGP archive format itself.** It only mentions that field files are located in FLEVEL.LGP and CHAR.LGP archives and that they are LZS compressed.

### Merge Decision

**NO EXTRACTION NEEDED** - The individual file FF7_LGP_format.md is complete and self-contained. The major section provides no additional technical specifications about LGP format that would enhance the individual file.

---

## Topic Scope Analysis

### FF7_LGP_format.md Scope

**Topics Covered**:
1. LGP Archive format structure (PC version)
   - File header with file creator and file count
   - Table of Contents (TOC) structure with 4 sections per entry
   - CRC validation code
   - Data section with file headers and data
   - File terminator

2. Technical Details
   - File creator string format ("SQUARESOFT" or "FICEDULA-LGP")
   - TOC entry structure (20-byte filename, 4-byte offset, 1-byte check code, 2-byte duplicate indicator)
   - CRC code specifications (typically 3602 bytes)
   - Data section file headers (20-byte filename, 4-byte file length, variable data)
   - Terminator strings ("FINAL FANTASY 7" or "LGP PATCH FILE")

3. Advanced Topics
   - Archive flexibility and game tolerance
   - Data gap handling
   - File pointer mechanics
   - Advanced editor techniques (Ficedula's LGP Editor)

4. Tools and Resources
   - LGP Tools (Advanced Editor)
   - Emerald (mass extraction)
   - Unmass (general extractor)

### 05_FIELD_MODULE.md Scope

**Topics Covered**:
1. Field Module Overview
   - Module responsibilities and structure
   - PSX vs PC version file organization
   - VRAM management and background assembly
   - Layer system and painter's algorithm

2. PC Field File Format (9 sections)
   - Section 1: Field Script and Dialog data
   - Section 2: Camera Matrix
   - Section 3: Unknown (Model Loader?)
   - Section 4: Palette
   - Section 5: Walkmesh
   - Section 6: Unknown
   - Section 7: Encounter data
   - Section 8: Unknown
   - Section 9: Background

3. PSX Field Format (3 separate files)
   - DAT files (field script data)
   - MIM files (background images)
   - BSX files (3D data)

4. Detailed Technical Specifications
   - Field file headers and section offsets
   - Script structures and entity definitions
   - Dialog parsing and string handling
   - Compression formats (LZS references)

---

## Content Already in Individual File

### Well-Covered Topics
- LGP archive format structure ✅
- File header specifications ✅
- Table of Contents format ✅
- CRC code information ✅
- Data section organization ✅
- Terminator format ✅
- Archive editing tools ✅
- Game flexibility with archives ✅

### No Gaps Identified
The individual file FF7_LGP_format.md provides a complete, self-contained explanation of the LGP archive format. It includes:
- All structural components
- Technical specifications
- Notes on archive flexibility
- References to editing tools
- Both standard and patched archive mentions

---

## Content to Extract from Major Section

### Result: NONE

**Analysis**:

1. **LGP Archive Format Details**: The major section does NOT discuss LGP archive format structure. It only mentions files are stored in FLEVEL.LGP.

2. **Specific References Found**:
   - Line 7: Table showing "/DATA/FIELD/FLEVEL.LGP" and "/DATA/FIELD/CHAR.LGP"
   - Line 41: "Field files are always found in FLEVEL.LGP. They are always LZS compressed"
   - Line 111: Brief mention of "ficedula lgp tools" in context of field file editing

3. **Assessment**: These are mere mentions/references to archives, not technical specifications about the archive format itself. The major section focuses on what's INSIDE the field files (the 9 sections), not the LGP container format.

4. **Appropriate Scope**: The field module section correctly delegates LGP format documentation to the specialized FF7_LGP_format.md file.

---

## Images in Extracted Content

### Result: NO IMAGES TO EXTRACT

**Analysis**:

The major section contains 13 images total (located at lines 27, 254, 462, 536, 673, 817, 1005, 1202, 1512, 1686, 1850, 2256, 2428):
- _page_73_Picture_13.jpeg - VRAM field background assembly (field module context)
- _page_80_Picture_0.jpeg - Walkmesh visualization (field module context)
- _page_85_Picture_5.jpeg - Background section (field module context)
- All others relate to field file sections, not LGP format

**Conclusion**: None of these images relate to LGP archive format. They all document the internal structure of field files or field module components.

---

## Content for Other Files

### Potential Cross-References

The major section mentions these related topics that belong in other individual files:

1. **FF7_LZSS_format.md**
   - Line 41 correctly references: "They are always LZS compressed (see my other documents/tools for details of LZS compression and tools to do it)"
   - Relationship: Field files are LZS compressed when stored in FLEVEL.LGP
   - Status: ✅ Correct delegation

2. **FF7_Field_Module.md** (if not already present)
   - The major section contains extensive field file format details
   - Status: This is the primary content for Field Module documentation

3. **FF7_TEX_format.md** (mentioned implicitly)
   - Background textures in field files use palette-based rendering
   - No explicit mention in major section

---

## Gaps and Discrepancies

### No Discrepancies Identified

**Assessment**:
- The individual FF7_LGP_format.md file and the major section 05_FIELD_MODULE.md have **complementary** scopes, not overlapping ones
- There are no conflicts or contradictions
- The scopes are appropriately separated:
  - FF7_LGP_format.md: Archive container format (HOW files are stored)
  - 05_FIELD_MODULE.md: Field file internal structure (WHAT is stored inside)
- Both work together: To access a field file, you first extract it from FLEVEL.LGP (LGP format), then parse its 9 sections (field file format)

### Cross-Reference Adequacy

The major section appropriately references related topics:
- ✅ References FLEVEL.LGP and CHAR.LGP archives
- ✅ References LZS compression separately
- ✅ Does not duplicate LGP format specification
- ✅ Focuses on field file internal structure (appropriate scope)

---

## Merge Plan Summary

### Recommendation: NO MERGE REQUIRED

**Rationale**:

1. **No Additional Content**: The major section contains zero new information about LGP archive format that would enhance FF7_LGP_format.md

2. **Appropriate Scope Separation**:
   - FF7_LGP_format.md covers: Archive container structure
   - 05_FIELD_MODULE.md covers: Field file internal structure
   - Both are necessary and complementary

3. **Cross-References Sufficient**: The major section adequately mentions FLEVEL.LGP and CHAR.LGP without duplicating format details

4. **Individual File Completeness**: FF7_LGP_format.md is a complete, self-contained document with all necessary technical specifications

### Alternative: Add Cross-Reference Link

**Optional Enhancement** (not required for data completeness):
- Consider adding a note in FF7_LGP_format.md mentioning that field files within LGP archives follow the structure documented in FF7_Field_Module.md
- Consider adding a note in 05_FIELD_MODULE.md cross-referencing FF7_LGP_format.md for archive structure details

---

## Related Individual Files

### Files in the Same Domain

1. **FF7_Field_Module.md** (293 lines)
   - Related: Documents field file internal structure
   - Relationship: Field files are stored in FLEVEL.LGP
   - Cross-reference opportunity: FLEVEL.LGP → FF7_LGP_format.md

2. **FF7_LZSS_format.md** (88 lines)
   - Related: LZS compression used for field files in FLEVEL.LGP
   - Relationship: Decompression required before parsing field files
   - Status: Already referenced in major section

3. **FF7_TEX_format.md** (364 lines)
   - Related: Texture format used in field backgrounds
   - Relationship: Background section of field files uses palette-based textures
   - Status: Not explicitly mentioned in major section

4. **PSX_TIM_format.md** (129 lines)
   - Related: PSX-specific image format for field backgrounds
   - Relationship: MIM files (PSX field backgrounds) use TIM format
   - Status: Not explicitly mentioned in major section

---

## Conclusion

### Final Status: ✅ NO ACTION REQUIRED

The analysis confirms that:

1. ✅ FF7_LGP_format.md is complete and comprehensive
2. ✅ 05_FIELD_MODULE.md appropriately delegates LGP format details
3. ✅ No new content needs to be extracted
4. ✅ No images need to be transferred
5. ✅ Scope boundaries are clear and well-respected
6. ✅ Cross-references are adequate

**Recommendation**: Do not merge. Both documents serve their intended purposes in the documentation structure.

---

**Report Complete**: 2025-11-29
**Prepared for**: Archive merge validation
**Status**: Analysis complete - no merge required
