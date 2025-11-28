# FF7_LZSS_format vs 05_FIELD_MODULE Content Analysis Report

**Created:** 2025-11-29 13:45 JST (Friday)
**Analysis Type:** Merge Validation & Gap Identification
**Session ID:** claude-code-session-analysis

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Individual File Size | 88 lines, 7.0 KB |
| Major Section Size | 2,645 lines, 90 KB |
| Content Overlap | **MINIMAL** - only 2 brief mentions of LZS compression |
| Images to Extract | **NONE** - No images in LZSS-related content |
| Content to Merge | **NONE** - No substantive additions found |
| Merge Complexity | **LOW** - Individual file is complete as-is |

---

## Topic Scope Analysis

### FF7_LZSS_format.md Scope
**Purpose:** Comprehensive technical reference for LZSS compression algorithm used in FF7 files

**Topics Covered:**
1. Format overview (header structure)
2. LZSS compression algorithm (control byte scheme)
3. Reference format (offset and length encoding)
4. Offset calculation (12-bit offset with modulo arithmetic)
5. Length calculations (4-bit length + 3)
6. Worked example (decompression walkthrough)
7. Complications (negative offsets, repeated runs, circular buffers)

**Audience:** Developers implementing LZSS decompression for FF7 file formats

### 05_FIELD_MODULE.md Scope
**Purpose:** Complete reference for the Field Module system in FF7 game engine

**Major Topics:**
- Field overview and architecture
- Field file format (PC version) - 9 sections
- Field script and dialog system
- Camera matrix structures
- Walkmesh/collision system
- Background sprite system
- PSX format variations (DAT, MIM, BSX files)
- Debug rooms (STARTMAP)

---

## Content Already in Individual File

The FF7_LZSS_format.md file is a **self-contained technical specification**. It comprehensively covers:

✅ Full LZSS algorithm explanation
✅ Reference format with bit-level details
✅ Offset calculation with complex modulo arithmetic
✅ Length encoding explained
✅ Practical example with step-by-step walkthrough
✅ Edge cases and complications (negative offsets, circular buffers)
✅ Implementation guidance for decompression

**Assessment:** The individual file is **complete and thorough** for its specific scope.

---

## CRITICAL FINDINGS: Content in Major Section vs Individual File

### Finding 1: Minimal Cross-Reference (Line 41)
**Location in 05_FIELD_MODULE.md:** Line 41

```markdown
Field files are always found in FLEVEL.LGP. They are always LZS compressed
(see my other documents/tools for details of LZS compression and tools to do it).
```

**Analysis:**
- This is a **brief mention** of LZS compression, not a detailed explanation
- It **delegates to separate documentation** (i.e., FF7_LZSS_format.md)
- The sentence is complete as-is; it does NOT provide technical details

**Merge Decision:** **NO CONTENT TO EXTRACT** - This reference is correctly pointing to a separate technical document for compression details. Including LZSS compression algorithm details in the Field Module document would bloat it unnecessarily.

### Finding 2: PSX DAT Format Reference (Line 434)
**Location in 05_FIELD_MODULE.md:** Line 434

```markdown
#### PSX DAT FORMAT

The PSX script is contained in the DAT file, it is compressed with LZS compression.
After it's decompressed, here is the header format for that..
```

**Analysis:**
- This mentions LZS compression for PSX DAT files
- Again, it's a **brief mention** without technical details
- Immediately follows with PSX DAT header format (not compression algorithm)
- The PSX DAT format section (lines 432-440) describes what happens **after decompression**

**Merge Decision:** **NO CONTENT TO EXTRACT** - This correctly identifies the compression method and then moves on to describing the decompressed structure. The technical details of HOW to decompress are appropriately left to FF7_LZSS_format.md.

---

## Image Inventory

**Images found in LZSS-related content:** **NONE**

The two references to LZS compression in the major section are brief textual mentions with no accompanying diagrams, charts, or images.

---

## Content for Other Files

### FF7_LGP_format.md Potential Addition
The FF7_LGP_format.md file (102 lines) describes the LGP archive format that contains these LZSS-compressed field files. The boundary is clear:
- **FF7_LGP_format.md scope:** How files are stored in LGP archives
- **FF7_LZSS_format.md scope:** How to decompress individual LZS-compressed files within those archives

**Boundary Status:** ✅ **CLEAR** - No overlap, complementary documents

### FF7_Field_Module.md Relationship
The FF7_Field_Module.md (293 lines) describes field structure but references compression through the delegation pattern already present in the major section.

**Boundary Status:** ✅ **CLEAR** - Field module describes structure, LZSS format describes decompression

---

## Gaps and Discrepancies

### Gap 1: No Cross-Reference in FF7_LZSS_format.md
**Observation:** The FF7_LZSS_format.md file does not mention field files or LGP archives as use cases

**Impact:** **MINIMAL** - The document clearly states it's for FF7 files generally; the specific use cases (field files, DAT files) are documented elsewhere

**Recommendation:** No change needed - the separation of concerns is intentional and appropriate

### Gap 2: PSX DAT Format Section Incomplete
**Observation:** The PSX DAT FORMAT section (lines 432-440) in the major section appears unfinished
- Line 434: Describes LZS compression
- Line 440: "(Follow PC Version)" - suggests forwarding to different section
- Lines 444-448: "PSX MIM FORMAT" and "PSX BCX FORMAT" are just placeholders

**Impact:** **NOT RELATED TO LZSS** - This is a gap in PSX format documentation, not in LZSS compression documentation

**Recommendation:** No action for this merge task

---

## Merge Plan Summary

### Recommendation: **NO MERGE REQUIRED**

**Justification:**

1. **Complete Document:** FF7_LZSS_format.md is a comprehensive, self-contained technical specification
2. **Appropriate References:** The major section correctly references (delegates to) this document rather than duplicating content
3. **Clean Boundaries:** The separation between:
   - LZS compression algorithm (FF7_LZSS_format.md)
   - Field module structure (FF7_Field_Module.md)
   - LGP archive format (FF7_LGP_format.md)

   ...is clear and appropriate

4. **No Missing Content:** The major section does NOT contain additional LZSS compression details that should be in the individual file

5. **No Images:** No images to integrate or path-adjust

### Alternative Consideration: Cross-Reference Enrichment
**If desired**, the FF7_LZSS_format.md could be **enhanced** (not merged) with contextual notes about usage:

```markdown
<!-- USAGE CONTEXTS -->

This compression format is used extensively in FF7 files:
- **Field files:** Stored in FLEVEL.LGP (PC version)
- **PSX DAT files:** Field script data on PlayStation version
- **Other archives:** Various LGP-packaged resources

See FF7_LGP_format.md and FF7_Field_Module.md for file format details.
```

However, this would be an **enhancement**, not a **merge** from the major section.

---

## Conclusion

**Merge Status:** ✅ **NO MERGE REQUIRED**

The FF7_LZSS_format.md individual file is **complete and appropriately scoped**. The major section (05_FIELD_MODULE.md) correctly treats LZSS compression as an external detail, delegating to this comprehensive technical document.

The documentation structure is optimal:
- **FF7_LZSS_format.md:** Algorithm and technical implementation
- **FF7_Field_Module.md:** Field structure and file organization
- **FF7_LGP_format.md:** Archive container format
- **05_FIELD_MODULE.md (major):** Comprehensive field system overview

No content extraction, path adjustments, or image integration needed.

---

**Report Complete**
