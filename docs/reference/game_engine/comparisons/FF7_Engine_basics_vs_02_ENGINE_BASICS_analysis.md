# FF7_Engine_basics vs 02_ENGINE_BASICS Analysis Report

**Created:** 2025-11-29 12:00 JST
**Analysis Date:** 2025-11-29
**File Scope:** Engine basics (module architecture and program flow)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Major section size | 16 lines (1.3KB) |
| Original file size | 32 lines |
| Merged file current size | 11 lines (metadata only) |
| Content alignment | 95% - Near perfect match |
| Images to extract | 1 image with path adjustment |
| Substantive additions needed | 1 - Structured content from major section |

**Finding**: The major section contains the exact same technical content as the original markdown file, just without the document structure (TOC, section IDs). Content is ready to merge with proper formatting adjustments.

---

## Topic Scope Analysis

**FF7_Engine_basics.md scope:**
- FF7 engine architecture and module system
- Six-module design (kernel, field, menu, world map, battle, mini-game)
- Memory constraints on PSX
- Module data banking system
- Generic program flow between modules

**02_ENGINE_BASICS.md scope:**
- Identical topics as above
- Direct copy of core technical explanation
- Slightly different image reference source

**Boundary Assessment:**
- ✅ No content belongs in other files
- ✅ No other files cover this scope
- ✅ Clean, self-contained documentation

---

## Content Already in Individual File

### Existing in FF7_Engine_basics.md (Original)

**Section 1: Parts of the Engine**
- Module architecture explanation
- PSX resource constraints (1MB VRAM, 2MB system RAM)
- Six-module system listing
- Image reference: `Engine_parts.jpg`

**Section 2: Generic Program Flow**
- Module accessibility constraints
- Field module's central role
- Scripting system capabilities

**Status:** ✅ All content present in original file

---

## Content to Extract from Major Section

### Topic: Engine Parts Structure

**Lines 1-11 in major section:**
```markdown
# **Engine Basics**

## *I. Parts of the Engine*

The engine used to power Final Fantasy 7 is split into several modules. This allowed
the programming team to break apart into very distinct groups. It also created a very
diverse game playing environment. It also allowed the artists to only have to work
within their own module, keeping the artwork as dynamic as possible.

The module system allowed for a single point of entry into, and exit out of, each
distinct part of the game. The PSX, which the game was originally developed for, had
very limited resources. With only 1 megabyte of video ram and 2 megabytes of system
ram, data had to be banked in and out efficiently. Modules were a clean way to dump
whole parts of the engine to make way for other parts.

The core system is made up of six modules. They are called the kernel, field, menu,
world map, battle, and mini game. They are arranged in the following order

![](_page_8_Picture_5.jpeg)
```

**Extraction Decision:** ✅ EXTRACT
**Reason:** This is the canonical version from the major section, provides clearer formatting and structure than original file metadata version

**Image handling:**
- Source reference in major section: `_page_8_Picture_5.jpeg` (line 11)
- File verified to exist: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/_page_8_Picture_5.jpeg`
- Original file uses: `Engine_parts.jpg` - Same content, different source format
- **Merged file solution:** Use `Engine_parts.jpg` (already referenced in original, better naming)
- Path adjustment: `_page_8_Picture_5.jpeg` → `../../images/Engine_parts.jpg`

### Topic: Generic Program Flow

**Lines 13-15 in major section:**
```markdown
## *II. Generic Program Flow*

Not every module is accessible by every other module. There is a distinct flow
between them. For example, you can not access the menu from battle, much to the
chagrin of the poor user who had forgotten to equip some last minute item. The
field module, second only to the kernel, drives the game. It includes a powerful
scripting system that can call any module within the game.
```

**Extraction Decision:** ✅ EXTRACT
**Reason:** Identical content already in original file, but major section version provides clearer section formatting

---

## Images in Extracted Content

| Image Name | Current Path | Status | Verified | Purpose |
|------------|--------------|--------|----------|---------|
| Engine_parts.jpg | `/Volumes/DevSSD/.../images/Engine_parts.jpg` | ✅ Exists | ✅ Yes | Module architecture diagram |
| _page_8_Picture_5.jpeg | `/Volumes/DevSSD/.../game_engine/_page_8_Picture_5.jpeg` | ✅ Exists | ✅ Yes | Same as Engine_parts.jpg (alternate source) |

**Image handling decision:**
- Use `Engine_parts.jpg` (better naming, already in images/ directory)
- Adjust reference path in merged file to: `../../images/Engine_parts.jpg`

---

## Content for Other Files

**Assessment:** No content should be distributed to other files. All content is engine-specific overview material that belongs only in FF7_Engine_basics.md

---

## Gaps and Discrepancies

### Finding 1: Image Reference Inconsistency
- **Original file**: References `Engine_parts.jpg` from images/ directory
- **Major section**: References `_page_8_Picture_5.jpeg` from game_engine root directory
- **Resolution**: Use `Engine_parts.jpg` with path `../../images/Engine_parts.jpg`

### Finding 2: Formatting Differences
- **Original file**: Uses markdown section anchors/IDs (for wiki-style linking)
- **Major section**: Uses simpler markdown formatting
- **Resolution**: Preserve original section ID structure for consistency with other files

### Finding 3: Empty Merged File
- **Current state**: Only metadata, no content
- **Solution**: Fill with complete content from both sources (original structure + major section content where equivalent)

---

## Merge Plan Summary

### Step 1: Structure
- Keep original file's TOC and section ID structure (for consistency with documentation ecosystem)
- Use major section's cleaner explanatory text where superior

### Step 2: Content Assembly
```
1. Metadata header (update with merge details)
2. Title and TOC (from original file)
3. "Parts of the Engine" section (from major section, better formatting)
4. Image reference (using Engine_parts.jpg from images/)
5. "Generic Program Flow" section (from major section)
6. Image link at end (from original file's Images section)
```

### Step 3: Image Handling
- Reference: `../../images/Engine_parts.jpg`
- Verified to exist: ✅ Yes
- Path is relative from: `merged_with_pdf_content/FF7_Engine_basics.md`

### Step 4: Content Markers
- Add extraction markers noting content source
- Document image path adjustments
- Preserve all original information

---

## Validation Results

| Check | Status | Notes |
|-------|--------|-------|
| File exists in merged_with_pdf_content/ | ✅ Yes | Ready to edit |
| Major section readable | ✅ Yes | 16 lines, clear content |
| Original file readable | ✅ Yes | 32 lines, includes structure |
| Image exists in images/ directory | ✅ Yes | Engine_parts.jpg verified |
| No content for other files | ✅ Yes | All scope-appropriate |
| Content substantially complete | ✅ Yes | No material gaps |

---

## Recommended Actions

1. ✅ **Immediate**: Update merged file with extracted content from major section
2. ✅ **Image handling**: Use `../../images/Engine_parts.jpg` relative path
3. ✅ **Preservation**: Keep original section ID structure for wiki compatibility
4. ✅ **Documentation**: Add extraction markers noting source

---

**Prepared for merge operation**

