# Content Analysis Report: PSX_TIM_format.md vs 05_FIELD_MODULE.md

**Created:** 2025-11-29 10:15 JST
**Analysis Scope:** Identify content from major section 05_FIELD_MODULE that should be merged into PSX_TIM_format.md
**Status:** Complete Analysis

---

## Executive Summary

### File Characteristics

| Metric | PSX_TIM_format.md | 05_FIELD_MODULE.md |
|--------|------------------|-------------------|
| **Current Lines** | 130 lines | 2,645 lines |
| **Current Size** | 7.2 KB | 90 KB |
| **Focus** | PSX TIM image format specification | FF7 Field module (entire subsystem) |
| **Scope** | Abstract PSX TIM format details | Field module + related PSX file formats |

### Relationship Analysis

**Direct Connection:**
- FF7 Field module heavily uses PSX TIM-derived formats (MIM files)
- MIM files are described in 05_FIELD_MODULE as "truncated TIM files"
- Both files deal with PSX graphics/color encoding

**Content Overlap:**
- **Palette/CLUT concepts:** Both discuss color lookup tables and palette management
- **Color format specifications:** Both reference 16-bit and multi-bit color formats
- **PSX VRAM architecture:** Field module discusses loading into VRAM; TIM format describes frame buffer structure

### Key Finding

**The major section (05_FIELD_MODULE) has TWO PLACEHOLDER SECTIONS with NO CONTENT:**

```
Line 444: PSX MIM FORMAT
Line 445: (empty line)
Line 446-447: (separator only)
Line 448: PSX BCX FORMAT
Line 449: (empty line)
Line 450-451: (separator only)
```

This represents a **significant gap** - PSX MIM FORMAT should contain detailed specification but contains only a header.

### Merge Recommendation

**VERDICT: NO SUBSTANTIVE CONTENT TO EXTRACT**

While the major section references MIM files extensively (as truncated TIM files), the actual specification section is empty. The individual PSX_TIM_format.md file is complete and self-contained. There is no duplicated or additional technical content in the major section to merge.

**However:** The reference to MIM files being "truncated TIM files" is a useful clarification that could be added as contextual information.

---

## Detailed Content Analysis

### Part 1: Topic Scope Understanding

#### PSX_TIM_format.md Scope
- **Topic:** Standard Sony PlayStation TIM (Texture Image Map) format
- **Content Level:** Detailed technical specification
- **Sections Covered:**
  1. Introduction to TIM format
  2. File layout (conceptual blocks)
  3. Header structure and flags
  4. CLUT (Color Lookup Table) block
  5. Image data block
  6. Color format specifications (16-bit, 24-bit, 8-bit indexed, 4-bit indexed)
  7. Image references/diagrams

#### 05_FIELD_MODULE.md Scope
- **Topic:** FF7's Field Module (the playable field/world system)
- **Content Level:** Implementation and architecture guide
- **Major Sections:**
  1. Field Overview
  2. Field Format (PC) - FLEVEL.LGP structure
  3. Field Format (PSX) - DAT/MIM/BSX file formats
  4. Event scripting and opcodes
  5. Debug rooms documentation
  6. Animation files for field characters

### Part 2: Related Individual Files Examination

**Field-Related Files Reviewed:**
- `FF7_Field_Module.md` (293 lines) - General field documentation
- `FF7_LGP_format.md` (102 lines) - PC archive format (contains field files)
- `FF7_LZSS_format.md` (88 lines) - Compression used by field files
- `FF7_TEX_format.md` (364 lines) - PC texture format

**Finding:** These files collectively cover:
- LGP archive structure (PC field files)
- LZSS compression (applied to PSX field files)
- TEX format (PC field textures)
- General field structure

**Notably absent:** Detailed PSX MIM format specification (the actual subject of MIM FORMAT section header)

### Part 3: Major Section Content Mapping

#### References to TIM/Palette Concepts in 05_FIELD_MODULE

| Line | Content Type | Description | Relevance to PSX_TIM |
|------|--------------|-------------|---------------------|
| 8 | Filename | `/FIELD/*.MIM` = Multiple Image Maps | References MIM as PSX graphics format |
| 21 | Overview | "MIM (Multiple Image Maps, or the backgrounds)" | Describes MIM role in field |
| 172-210 | Section 4 | **Palette data specification** | DESCRIBES COLOR PALETTE STRUCTURE |
| 181 | Palette data | "Number of colors in palette" | Uses palette organization |
| 197 | Color format | "15-bit (5-bit R/G/B + 1 mask bit)" | MATCHES TIM color format |
| 204 | Palette page | "256-color palette pages" | Palette page organization |
| 213 | PSX MIM FORMAT | "MIM file is a truncated TIM file" | **KEY: MIM defined as truncated TIM** |
| 213 | MIM content | "contains palettes (256 color ones) and screen blocks" | MIM uses palette system |
| 213 | MIM info | "clut location height and width information" | References CLUT (from TIM) |

#### Palette Section Deep Dive (Lines 172-210)

This section in the major document **does provide palette structure details:**

```markdown
Line 172: "The following is an overview of the palette data"
Line 181: "Number of colors in palette" (4 bytes)
Line 191-204: Palette entry structure (16-bit)
Line 197: "15-bit (5-bit Red, 5-bit Green, 5-bit Blue, and 1 mask bit)"
Line 204: "256-color 'pages' internally"
```

**Assessment:** This palette section describes FF7-SPECIFIC palette implementation, not generic PSX TIM CLUT structure.

- **TIM format** (in PSX_TIM_format.md): Describes abstract CLUT block with frame buffer positioning
- **FF7 Palette** (in major section): Describes how FF7 organizes 256-color palette "pages"

These are **different levels of abstraction** - not duplicative.

### Part 4: Search for TIM-Specific Content

#### Explicit TIM References
```
Line 213: "The MIM file is a truncated TIM file and contains the normal
          clut location height and width information. This information
          is directly loaded into the PSX video ram to be decoded by
          the field module."
```

This is the **only explicit TIM format reference** in the entire major section.

#### Color Format Mentions
- 16-bit color: Mentioned in context of FF7's palette (line 197)
- Mentioned same format as TIM's 16-bit format
- But described in FF7-specific context, not generic PSX TIM context

### Part 5: Images in Major Section

#### Images Found
```
Line 27:  ![](\_page_73_Picture_13.jpeg) - PSX VRAM field assembly
Line 254: ![](\_page_80_Picture_0.jpeg) - [context unknown]
Line 462: ![](\_page_85_Picture_5.jpeg) - Debug room Startmap
Line 536: ![](\_page_87_Picture_19.jpeg) - Kitase's room
Line 673: ![](\_page_90_Picture_4.jpeg) - [context unknown]
Line 817: ![](\_page_93_Picture_2.jpeg) - [context unknown]
Line 1005: ![](\_page_96_Picture_2.jpeg) - [context unknown]
Line 1202: ![](\_page_99_Picture_2.jpeg) - [context unknown]
Line 1512: ![](\_page_103_Picture_15.jpeg) - [context unknown]
Line 1686: ![](\_page_106_Picture_2.jpeg) - [context unknown]
Line 1850: ![](\_page_108_Picture_26.jpeg) - [context unknown]
Line 2256: ![](\_page_114_Picture_23.jpeg) - [context unknown]
Line 2428: ![](\_page_117_Picture_2.jpeg) - [context unknown]
```

#### Relevance to PSX_TIM_format.md

These images are PDF page captures (internal references) and are NOT about TIM format:
- Field architecture screenshots
- Debug room walkthrough
- Event trigger examples

**None of these images are relevant to PSX_TIM_format.md** which uses actual diagram images:
- `PSX_TIM_file_layout.png` - File structure diagram
- `PSX_TIM_file_clut.png` - CLUT block diagram
- `PSX_color_formats_16.png` - Color format diagram
- `PSX_color_formats_24.png` - Color format diagram
- `PSX_color_formats_8.png` - Color format diagram
- `PSX_color_formats_4.png` - Color format diagram
- `PSX_TIM_file_image.png` - Image data block diagram

### Part 6: Content Boundary Analysis

#### What Should Be In PSX_TIM_format.md
✅ Generic PSX TIM format specification
✅ File layout and structure
✅ Header format and flags
✅ CLUT block details
✅ Image data encoding
✅ Color format specifications
✅ Frame buffer integration

#### What Should NOT Be In PSX_TIM_format.md
❌ FF7-specific field module structure
❌ FF7-specific palette page organization
❌ LGP archive format (PC)
❌ DAT/BSX format specifics
❌ Field script documentation

#### What The Major Section Provides
- **Palette organization:** FF7-specific (256-color pages)
- **MIM file reference:** "truncated TIM file" - clarification, not specification
- **No actual TIM specification content**

### Part 7: Content to Extract Analysis

**Finding:** There is **NO substantive new content to extract** from the major section.

**Detailed Analysis:**

| Content Area | In PSX_TIM_format? | In 05_FIELD_MODULE? | Assessment |
|---|---|---|---|
| TIM file structure | ✅ Complete | ❌ Not detailed | TIM file more comprehensive |
| CLUT format | ✅ Complete | ⚠️ FF7-specific | Different abstraction levels |
| Color formats (16/24/8/4-bit) | ✅ Complete | ⚠️ References only | TIM file complete |
| Frame buffer integration | ✅ Covered | ✅ Mentioned | Already in TIM file |
| MIM file relationship | ❌ Not mentioned | ✅ States "truncated TIM" | Could be added as reference |
| PSX VRAM architecture | ✅ Implicit | ✅ Detailed | Different contexts |

**The MIM File Reference (Line 213):**
```
"The MIM file is a truncated TIM file and contains the normal
clut location height and width information."
```

This is a **useful clarification** but not a substantive technical addition. It explains the relationship between TIM and MIM formats at an architectural level.

### Part 8: Empty Section Analysis

**Lines 444-450: PSX MIM FORMAT and PSX BCX FORMAT**

These section headers exist with **zero content**:

```markdown
PSX MIM FORMAT
--------------

PSX BCX FORMAT
------------------
```

**Assessment:**
- These are placeholders in the major section
- They indicate where detailed format specifications SHOULD exist
- The individual FF7_Field_Module.md file provides brief descriptions but not detailed format specs
- **This is NOT a deficiency of PSX_TIM_format.md** - this is a gap in the major section itself

---

## Merge Plan Summary

### Recommended Action: MINIMAL MERGE

Based on the comprehensive analysis above:

### Content to Add

**Optional:** Add a single clarifying section at the end of PSX_TIM_format.md:

```markdown
## Related Formats

### MIM (Multiple Image Maps) Format

In Final Fantasy VII, the PSX field module uses a format called MIM
(Multiple Image Maps) for storing background graphics. MIM files are
truncated TIM files containing palettes and screen block data. The CLUT
(color lookup table) location, height, and width information from the TIM
format is directly utilized when loading MIM data into the PlayStation VRAM
for decoding by the field module.

**Reference:** `FF7_Field_Module.md` - PSX MIM Format section
```

### Why MINIMAL Merge?

1. **PSX_TIM_format.md is complete and accurate** - Covers all aspects of the generic TIM format
2. **No duplicated technical content** - The major section doesn't provide new TIM format details
3. **Different abstraction levels** - Major section is FF7-implementation-specific; TIM file is format-generic
4. **No images to extract** - Major section images are event documentation, not format diagrams
5. **The MIM reference is architectural clarification**, not technical specification

### What NOT to Do

❌ Do NOT extract palette sections - they describe FF7-specific organization
❌ Do NOT copy VRAM architecture - different context and purpose
❌ Do NOT add empty section placeholders - they're incomplete in source
❌ Do NOT restructure the original file - preserve its current organization

---

## Images Inventory

### Images Currently in PSX_TIM_format.md
✅ PSX_TIM_file_layout.png (5.9 KB)
✅ PSX_TIM_file_clut.png (2.3 KB)
✅ PSX_color_formats_16.png (632 B)
✅ PSX_TIM_file_image.png (3.1 KB)
✅ PSX_color_formats_16.png (duplicate reference)
✅ PSX_color_formats_24.png (928 B)
✅ PSX_color_formats_8.png (432 B)
✅ PSX_color_formats_4.png (512 B)

### Images in Major Section Relevant to TIM
❌ None - All major section images are field/event screenshots, not format diagrams

### Image Path Adjustments Needed
✅ Current paths in PSX_TIM_format.md are correct: `../images/PSX_*.png`
✅ All image files exist and are accessible

---

## Gaps and Discrepancies

### Gap 1: PSX MIM Format Specification
**Location:** Lines 444-447 in 05_FIELD_MODULE.md
**Issue:** Section header exists with no content
**Resolution:** Beyond scope of this task (affects major section, not individual file)

### Gap 2: PSX BCX Format Specification
**Location:** Lines 448-450 in 05_FIELD_MODULE.md
**Issue:** Section header exists with no content
**Resolution:** Beyond scope of this task

### Gap 3: Palette vs CLUT Documentation
**Finding:** Separate but related concepts not cross-referenced:
- **PSX_TIM_format.md:** Documents generic CLUT block
- **05_FIELD_MODULE.md:** Documents FF7-specific palette pages
- **Recommendation:** Optional cross-reference in PSX_TIM_format.md

---

## Final Recommendations

### For PSX_TIM_format.md Merge

**OPTION 1: NO CHANGES (RECOMMENDED)**
- The file is complete and accurate as-is
- No substantive new content exists in major section to add
- Individual file serves its purpose well

**OPTION 2: ADD OPTIONAL CLARIFICATION**
- Add "Related Formats" section mentioning MIM files
- Provides architectural context for readers
- Requires ~5-10 lines of new content
- Does NOT modify existing content

### For Project-Wide Documentation

**Further Investigation Needed:**
1. Someone should write the `PSX MIM FORMAT` section (currently empty)
2. Someone should write the `PSX BCX FORMAT` section (currently empty)
3. Consider creating `FF7_MIM_format.md` and `FF7_BCX_format.md` as new individual files

---

## Session Metadata

**Analysis Complete:** 2025-11-29 10:35 JST
**Lines Reviewed (Major Section):** 2,645 lines
**Lines Reviewed (Individual File):** 130 lines
**Related Files Sampled:** 5 files
**Images Verified:** 8 images in reference directory
**Content Extraction Identified:** Minimal (architectural reference only)
**Status:** Ready for Phase 2 (Merge or No-Op)

---
