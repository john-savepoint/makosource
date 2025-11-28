# Agent Comparison and Merge Guide

**Created**: 2025-11-28 20:10 JST
**Purpose**: Guide for agents performing content analysis and merge operations on FF7 game engine documentation
**Session**: e42ced1a-f85e-452f-89df-5d230ad50c41

---

## Overview

This guide provides the complete prompt and instructions for spawning Haiku agents to compare major section files against individual markdown files, then merge unique content while preserving all original information.

## Task Summary

**Goal**: Compare content between major sections (extracted from massive `ff7 game engine.md`) and individual markdown files, then create merged versions with ALL original content + extracted additions.

**Output Deliverables** (per file):
1. Analysis report in `comparisons/`
2. Merged file in `merged_with_pdf_content/`

**Safety Requirements**:
- ✅ Copy original files (never rewrite)
- ✅ Extract content verbatim (never paraphrase)
- ✅ Preserve ALL original content
- ✅ Add clear extraction markers
- ✅ **Handle images properly** (see Image Handling section below)

---

## File Structure Reference

### Source Files
- **Major sections**: `docs/reference/game_engine/extracted_major_sections/[SECTION_FILE].md`
- **Individual files**: `docs/reference/game_engine/markdown/[INDIVIDUAL_FILE].md`
- **Mapping guide**: `docs/reference/game_engine/extracted_major_sections/MAPPING.md`

### Output Locations
- **Analysis reports**: `docs/reference/game_engine/comparisons/[INDIVIDUAL_FILE]_vs_[SECTION_FILE]_analysis.md`
- **Merged files**: `docs/reference/game_engine/markdown/merged_with_pdf_content/[INDIVIDUAL_FILE]`

---

## Image Handling Protocol

### CRITICAL: Image Preservation

When extracting content from major sections, you **MUST** handle images properly:

#### Step 1: Identify Images in Major Section

Look for image references in formats:
- Markdown: `![alt text](path/to/image.png)`
- HTML: `<img src="path/to/image.png" />`
- Wiki syntax: `[[File:image.png]]`

#### Step 2: Verify Image Paths

Check if images exist at referenced locations:
```bash
# Major section images are typically in:
ls /Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/images/
```

#### Step 3: Update Image Paths in Merged Files

When copying content with images from major section to individual file:

**Original path in major section**:
```markdown
![Engine Parts](images/Engine_parts.jpg)
```

**Path in merged file** (adjust relative path):
```markdown
![Engine Parts](../../images/Engine_parts.jpg)
```

**Path calculation**:
- Major section location: `extracted_major_sections/`
- Individual file location: `markdown/merged_with_pdf_content/`
- Image location: `images/`
- Relative path from merged file: `../../images/[filename]`

#### Step 4: Document Image References

In your analysis report, list all images found:

```markdown
## Images in Extracted Content

- Engine_parts.jpg (major section line 123)
- Field_BackgroundVRAM.jpg (major section line 456)
- Gears_img_3.jpg (major section line 789)

**Image Path Adjustments**:
- Original: `images/Engine_parts.jpg`
- Updated: `../../images/Engine_parts.jpg`
```

#### Step 5: Verify Image Files Exist

Before completing merge, verify image files:
```bash
# Check each referenced image exists
ls -lh /Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/images/Engine_parts.jpg
```

---

## Complete Agent Prompt Template

Use this prompt when spawning agents with the Task tool. Replace placeholders in [BRACKETS] with actual values.

### Full Prompt (Copy This)

```
You are performing a TWO-PHASE content analysis and merge operation for FF7 game engine documentation.

## Context: The Documentation Structure

**Source**: A massive 8,167-line `ff7 game engine.md` file was broken into 12 major sections.

**Target**: 32+ individual markdown files that are the SOURCE OF TRUTH for documentation.

**Your Mission**:
1. Identify content in the major section that should be in the individual file but isn't
2. Create a merged version with ALL original content + extracted additions
3. **HANDLE IMAGES PROPERLY** - adjust paths and verify files exist

## Your Specific Task

**Major Section**: `[SECTION_FILE]`
**Individual File**: `[INDIVIDUAL_FILE]`

**Related Individual Files in This Domain**:
[LIST_OF_RELATED_FILES]

## File Paths

**Read completely**:
1. Major section: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/extracted_major_sections/[SECTION_FILE]`
2. Individual file: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/[INDIVIDUAL_FILE]`
3. Mapping context: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/extracted_major_sections/MAPPING.md`

**Skim to understand boundaries**:
[LIST_OF_RELATED_FILE_PATHS]

## PHASE 1: Analysis Report (60 minutes)

### Step 1: Understand Topic Boundaries

Read MAPPING.md to understand:
- What is THIS individual file's topic scope?
- What do OTHER related files cover?
- Where are the boundaries between files?

Skim related individual files (TOC, headers, first/last sections):
- What content exists elsewhere?
- Where are the gaps?

### Step 2: Map Content in Major Section

Go through major section systematically, for EACH topic/section:
- Does it align with THIS individual file's scope?
- Does it align with a DIFFERENT individual file's scope?
- Is it NOT in ANY individual file?

### Step 3: Deep Content Comparison

For content aligning with THIS individual file:

**Compare at TOPIC level, not line-by-line**:
- Topic A: In individual file? Same detail? Missing formulas/tables/examples/images?
- Topic B: In individual file? [Repeat analysis]

**Identify substantive additions**:
- ✅ Additional formulas/algorithms
- ✅ Additional tables/data structures
- ✅ Additional technical specifications
- ✅ Additional examples/use cases
- ✅ Additional images/diagrams
- ✅ Clearer technical explanations

**Ignore superficial differences**:
- ❌ Formatting variations
- ❌ Section ordering
- ❌ Identical information with different wording

### Step 4: Identify Images

**Search for image references**:
```bash
grep -n "!\[.*\](" /path/to/major/section
grep -n "<img" /path/to/major/section
```

**Document all images found**:
- Image filename
- Line number in major section
- Alt text or description
- Whether it should be included in merged file

### Step 5: Create Analysis Report

**Write to**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/comparisons/[INDIVIDUAL_FILE]_vs_[SECTION_FILE]_analysis.md`

**Required sections**:
- Executive Summary (file sizes, alignment, items to extract, images count)
- Topic Scope Analysis
- Content Already in Individual File
- **CRITICAL**: Content to Extract (with line numbers and image lists)
- Images in Extracted Content (with path adjustments)
- Content for Other Files
- Gaps and Discrepancies
- Merge Plan Summary

## PHASE 2: Create Merged File

### Merging Rules (MANDATORY)

**Rule 1**: NEVER rewrite the original file - copy it exactly, then add to it
**Rule 2**: ALWAYS copy text verbatim - no paraphrasing or summarizing
**Rule 3**: ADJUST IMAGE PATHS - update relative paths and verify files exist
**Rule 4**: Add clear extraction markers
**Rule 5**: Preserve original structure - don't rearrange
**Rule 6**: If unsure, append at end

### Step 1: Copy Original File

```bash
cp "/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/[INDIVIDUAL_FILE]" "/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/merged_with_pdf_content/[INDIVIDUAL_FILE]"
```

### Step 2: Add Extracted Content

Use Edit tool to add content with markers:

```markdown
<!-- EXTRACTED FROM MAJOR SECTION: [SECTION_FILE] lines X-Y
     Images adjusted: images/file.jpg → ../../images/file.jpg
-->

[Exact copied text with adjusted image paths]

<!-- END EXTRACTION -->
```

### Step 3: Handle Images

For each image in extracted content:

1. Update path: `images/file.jpg` → `../../images/file.jpg`
2. Verify exists: `ls /path/to/images/file.jpg`
3. Document in extraction marker

### Step 4: Verify No Loss

- ✅ ALL original content preserved
- ✅ ALL extracted content added verbatim
- ✅ ALL images with corrected paths
- ✅ Clear extraction markers

### Step 5: Add Merge Metadata

At top of merged file:

```markdown
<!--
MERGE METADATA
Created: [DATE]
Original: [INDIVIDUAL_FILE] ([X] lines)
Major section: [SECTION_FILE]
Additions: [Y] items, ~[Z] lines
Images: [N] images with paths adjusted
Report: comparisons/[INDIVIDUAL_FILE]_vs_[SECTION_FILE]_analysis.md
-->
```

## Validation Checklist

**Analysis Report**:
- [ ] Read entire major section
- [ ] Read entire individual file
- [ ] Skimmed related files for context
- [ ] Identified content to extract (with line numbers)
- [ ] Identified all images
- [ ] Explained WHY each extraction belongs here
- [ ] Flagged discrepancies

**Merged File**:
- [ ] Copied original first (not rewritten)
- [ ] Content extracted verbatim (not paraphrased)
- [ ] Image paths updated correctly
- [ ] All images verified to exist
- [ ] Extraction markers added
- [ ] ALL original content preserved
- [ ] Merge metadata added

## Critical Warnings

**DO NOT**:
- Rewrite or paraphrase content
- Summarize extracted content
- Rearrange original file structure
- Remove anything from original
- Break image references with wrong paths

**DO**:
- Copy files and text verbatim
- Add clear markers
- Preserve everything
- Adjust image paths correctly
- Verify images exist
- Document what you added

## Deliverables

You must create BOTH:
1. Analysis report in `comparisons/` (with image inventory)
2. Merged file in `merged_with_pdf_content/` (with working images)
```

---

## Domain-Specific Related Files

### Kernel Domain (03_KERNEL.md)
- FF7_Kernel.md
- FF7_Kernel_Overview.md
- FF7_Kernel_Kernelbin.md
- FF7_Kernel_Memory_management.md
- FF7_Kernel_Low_level_libraries.md
- FF7_Savemap.md

### Battle Domain (06_BATTLE_MODULE.md)
- FF7_Battle_Battle_Mechanics.md
- FF7_Battle_Battle_Scenes.md
- FF7_Battle_Battle_Scenes_Battle_Script.md
- FF7_Battle_Battle_Animation_PC.md
- FF7_Battle_Battle_Field.md
- FF7_Playstation_Battle_Model_Format.md

### World Map Domain (07_WORLD_MAP.md)
- FF7_WorldMap_Module.md
- FF7_WorldMap_Module_Script.md
- FF7_World_Map_BSZ.md
- FF7_World_Map_TXZ.md

### Field Domain (05_FIELD_MODULE.md)
- FF7_Field_Module.md
- FF7_LGP_format.md
- FF7_LZSS_format.md
- FF7_TEX_format.md
- PSX_TIM_format.md

---

## Example Task Tool Invocation

To spawn agents in parallel, use a single message with multiple Task tool calls:

**Placeholder values to replace**:
- `[SECTION_FILE]` - e.g., `03_KERNEL.md`
- `[INDIVIDUAL_FILE]` - e.g., `FF7_Kernel_Memory_management.md`
- `[LIST_OF_RELATED_FILES]` - Bullet list from Domain-Specific section above
- `[LIST_OF_RELATED_FILE_PATHS]` - Full absolute paths to related files

**Model**: Use `haiku` for cost efficiency - this task is well-defined

**Description**: Brief 3-5 word description, e.g., "Analyze and merge FF7_Kernel.md"

---

## Batch Processing Guide

### Recommended Batches

**Batch 1: Kernel (6 files)** - ✅ COMPLETE
**Batch 2: Battle (6 files)** - Pending
**Batch 3: World Map (4 files)** - Pending
**Batch 4: Field + Formats (5 files)** - Pending
**Batch 5: Sound (4 files)** - Pending
**Batch 6: Miscellaneous (7 files)** - Pending

### Running a Batch

1. Create task invocations for all files in batch
2. Send in SINGLE message for parallel execution
3. Wait for all agents to complete
4. Review analysis reports
5. Verify merged files
6. Commit before next batch

---

## Post-Processing

After agents complete:

### 1. Review Analysis Reports
- Check for critical findings
- Note technical discrepancies
- Identify gaps

### 2. Verify Merged Files
- Spot-check content preservation
- Verify image paths work
- Check extraction markers present

### 3. Test Image References
```bash
# From merged file directory, verify images load
cd docs/reference/game_engine/markdown/merged_with_pdf_content/
# Check image paths in files
grep -r "!\[.*\](../../images/" .
# Verify files exist
ls ../../images/
```

### 4. Commit Work
```bash
git add comparisons/ merged_with_pdf_content/
git commit -m "docs(game-engine): batch N comparison and merge results"
```

---

## Troubleshooting

### Images Not Found
- Check `docs/reference/game_engine/images/` directory exists
- Verify image filenames match (case-sensitive)
- Ensure relative path calculation is correct

### Agent Timeouts
- Large files may need more time
- Consider breaking very large files into sub-tasks
- Haiku should handle most files efficiently

### Content Not Extracted
- Check topic alignment in analysis report
- Verify content truly belongs in this file vs another
- Agent may correctly determine no extraction needed

---

## Success Metrics

After each batch:
- ✅ All analysis reports complete with specific line numbers
- ✅ All merged files preserve 100% of original content
- ✅ All images have working paths
- ✅ No information loss
- ✅ Clear traceability via extraction markers
- ✅ Technical discrepancies flagged for follow-up
