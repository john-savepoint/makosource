<!--
ANALYSIS REPORT: FF7_Chocobo_Breeding.md vs 08_MINI_GAMES.md
Created: 2025-11-29 03:15 JST
Author: Claude Code Analysis Agent
Task: Phase 1 Content Analysis for Merge Operation
Status: COMPLETE
-->

# FF7 Chocobo Breeding vs 08 Mini Games - Content Analysis Report

## Executive Summary

**File Sizes:**
- Individual file: `FF7_Chocobo_Breeding.md` - 541 lines
- Major section: `08_MINI_GAMES.md` - 552 lines
- Overlap scope: COMPLETE (entire individual file content exists in major section)

**Analysis Findings:**
- The individual `FF7_Chocobo_Breeding.md` file is **extremely sparse** - contains only metadata header with no actual content
- The major section `08_MINI_GAMES.md` contains the **FULL, AUTHORITATIVE Chocobo Breeding documentation** (lines 23-552)
- All Chocobo breeding mechanics, formulas, and tables exist ONLY in the major section
- The individual file is essentially a template awaiting content extraction
- **Action Required:** Extract ALL 529 lines of Chocobo Breeding content from major section into merged file

**Images Found:** 0 (no image references in this section)

**Content to Extract:** ~529 lines (lines 23-552 of major section)

**Extraction Priority:** CRITICAL - This is substantive, well-documented technical content

---

## Topic Scope Analysis

### Individual File Scope: `FF7_Chocobo_Breeding.md`

**Intended Coverage (based on filename):**
- Chocobo breeding mechanics
- Breeding nut types and effects
- Stat inheritance and calculation
- Color and rating determination
- Baby chocobo maturation

**Current Content:**
- METADATA ONLY (created 2025-11-29, pending review)
- File is essentially empty except header comment
- No substantive technical content

### Major Section Scope: `08_MINI_GAMES.md` (Lines 6854-7405)

**Actual Coverage:**
- Mini game overview (Lorem Ipsum placeholder - lines 3-19)
- Highway Battle (Lorem Ipsum placeholder)
- Chocobo Races (header only)
- Battle at Condor (Lorem Ipsum placeholder)
- Sub Battle (Lorem Ipsum placeholder)
- Snowboarding (header only)
- **Chocobo Breeding** (FULL CONTENT - lines 23-552)

**Key Observation:** The major section is mostly Lorem Ipsum placeholders EXCEPT for the comprehensive Chocobo Breeding guide by Terence Fergusson.

### Relationship to Other Files

**Related Files in Documentation:**
- No other individual files cover Chocobo breeding (confirmed via MAPPING.md)
- This is the ONLY source of Chocobo breeding documentation in the game engine docs
- The breeding mechanics are unique to FF7's mini-game system

---

## Content Already in Individual File

**Current Status:** ❌ EMPTY

The merged file at `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/merged_with_pdf_content/FF7_Chocobo_Breeding.md` contains only:

```markdown
<!--
MERGE METADATA
Created: 2025-11-29
Original: FF7_Chocobo_Breeding.md (541 lines)
Major section: 08_MINI_GAMES.md
Merge decision: NEEDS REVIEW
Reason: Chocobo mechanics documented in mini-games section
Status: Metadata-only - Full analysis pending
-->
```

**Conclusion:** The merged file is a template with no actual technical content. It awaits the extraction from the major section.

---

## CRITICAL: Content to Extract from Major Section

### Extraction Scope

**Source:** Lines 23-552 of `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/extracted_major_sections/08_MINI_GAMES.md`

**Total Lines to Extract:** 529 lines (full Chocobo Breeding guide by Terence Fergusson)

**Status:** READY FOR EXTRACTION (100% complete in major section)

### Content Structure (What Will Be Extracted)

1. **Editor's Note** (line 25)
   - Explains that Chocobo Breeding is written in Field Script
   - Notes relationship to Chocobo Racing

2. **1. STAT GLOSSARY** (lines 27-49)
   - Defines all Chocobo stats (Dash, Max Dash, Run, Max Run, Stamina, etc.)
   - 13 different stat types defined in table format

3. **2. BASE CHOCOBOS** (lines 50-152)
   - Rating system (Wonderful through Terrible)
   - Max Dash and Stamina table (8 variants per rating)
   - Dash calculation formulas
   - Run and Max Run calculations
   - Acceleration and Intelligence formulas
   - Performance determination

4. **3. FEEDING GREENS** (lines 154-172)
   - Green types and their effects
   - Gysahl, Krakka, Tantal, Pahsana, Curiel greens
   - Mimett, Reagan, Sylkis greens
   - Stat modifications per green type

5. **4. BREEDING DATA** (lines 174-552)
   - **Pepio Nut** (lines 188-230)
   - **Luchile Nut** (lines 232-270)
   - **Saraha Nut** (lines 271-303)
   - **Lasan Nut** (lines 304-336)
   - **Pram Nut** (lines 337-368)
   - **Porov Nut** (lines 369-402)
   - **Carob Nut** (lines 403-471)
   - **Zeio Nut** (lines 472-529)
   - **FINAL BREEDING NOTES** (lines 530-552)

### Why This Content Must Be Extracted

**Technical Value:**
- Extremely detailed breeding mechanics guide
- Written by Terence Fergusson (recognized authority)
- Complex formulas and probability calculations
- Critical for understanding FF7's breeding system

**Completeness:**
- Covers ALL 8 breeding nuts with detailed mechanics
- Includes stat calculation formulas
- Includes color/rating determination logic
- Includes performance variables and edge cases

**Uniqueness:**
- NOT available in any other documentation file
- NOT in individual file currently (only metadata)
- This is authoritative source material

**Practical Value:**
- Used by modders and FF7 enthusiasts
- Essential reference for creating breeding simulators
- Documents complex probability mechanics

---

## Images in Extracted Content

**Image Count:** 0

**Rationale:** The Chocobo Breeding section contains only text, tables, and mathematical formulas. No images are referenced or required.

**Image Paths:** N/A

---

## Content for Other Files

**Analysis:** None of the extracted content should go to other files.

**Rationale:**
- The breeding mechanics are self-contained
- They don't relate to field modules, battle systems, or other mini-games
- All content is specifically about Chocobo breeding
- The individual file `FF7_Chocobo_Breeding.md` is the correct destination

---

## Gaps and Discrepancies

### Intentional Placeholders in Major Section

The major section (`08_MINI_GAMES.md`) contains Lorem Ipsum placeholders for:
1. Mini Game Overview (lines 3-5) - placeholder text only
2. Highway Battle (lines 7-9) - placeholder text only
3. Chocobo Races (line 11) - header only, no content
4. Battle at Condor (lines 13-15) - placeholder text only
5. Sub Battle (lines 17-19) - placeholder text only
6. Snowboarding (line 21) - header only, no content

**Action Items:**
- These sections have no corresponding individual files in the markdown/ directory
- No extraction is planned for placeholder sections
- Focus remains on Chocobo Breeding (the only substantive content)

### Incompleteness in Source Documentation

**Editor's Note (Line 25):**
> "Editor's Note: Chocobo Breeding isn't a separate module like the others, but is written entirely in Field Script. It's connected to Chocobo racing in a way, but expansive enough to warrant it's own section."

This note indicates:
- Chocobo Breeding is implemented via Field Script (not a separate game module)
- It's technically part of the Field Module but documented separately
- This is a deliberate organizational choice

**Missing from Major Section:**
- No detailed performance variable explanation (mentioned but not exhaustively documented)
- Racing mechanics themselves are mentioned but not detailed
- Integration points with field script are not documented

These gaps don't affect extraction since all available content should be preserved.

---

## Merge Plan Summary

### Phase 1: Analysis (COMPLETE)
✅ Identified extraction scope: 529 lines (lines 23-552)
✅ Confirmed content uniqueness: Only exists in major section
✅ Verified no image processing needed
✅ Confirmed extraction destination: merged file only

### Phase 2: Merge Execution (PENDING)

**Target File:** `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/merged_with_pdf_content/FF7_Chocobo_Breeding.md`

**Merge Process:**

1. Read current merged file (metadata only)
2. Extract lines 23-552 from major section
3. Add extraction markers with source references
4. Update metadata header with merge information
5. Verify all 529 lines copied verbatim
6. Commit changes with proper attribution

**Text Extraction Method:**
```
Copy verbatim from major section lines 23-552
No paraphrasing
No summarization
Preserve exact formatting including tables and code blocks
```

**Extraction Markers:**
```markdown
<!-- EXTRACTED FROM MAJOR SECTION: 08_MINI_GAMES.md lines 23-552
     Content: Complete Chocobo Breeding Guide
     Author: Terence Fergusson
     No images in this section
-->

[FULL CONTENT COPIED VERBATIM]

<!-- END EXTRACTION from 08_MINI_GAMES.md -->
```

**Metadata Update:**
```markdown
<!--
MERGE METADATA
Created: 2025-11-29
Original: FF7_Chocobo_Breeding.md (541 lines initially)
Major section: 08_MINI_GAMES.md (552 lines total)
Additions: 529 lines (lines 23-552 from major section)
Final size: ~1,070 lines after merge
Images: 0 images to adjust
Extraction marker: Yes
Report: comparisons/FF7_Chocobo_Breeding_vs_08_MINI_GAMES_analysis.md
-->
```

---

## Validation Checklist for Phase 2

**Before Edit:**
- [ ] Confirm merged file exists and is readable
- [ ] Confirm original file in markdown/ has 541 lines (unchanged)
- [ ] Backup current merged file metadata

**During Edit:**
- [ ] Read merged file completely
- [ ] Add extraction marker at beginning
- [ ] Copy lines 23-552 verbatim (no modifications)
- [ ] Preserve all formatting (tables, code blocks, formulas)
- [ ] Add closing extraction marker
- [ ] Update metadata header

**After Edit:**
- [ ] Verify no lines were lost from original metadata
- [ ] Verify all 529 lines were added
- [ ] Verify original file in markdown/ is unchanged
- [ ] Count lines in merged file (~1,070 expected)
- [ ] Commit with proper attribution

---

## Technical Notes for Implementation Agent

### Character Encoding
The content contains special characters that should be preserved:
- Greek letters (α, β, etc.) - **NOT USED in this section**
- Mathematical operators (÷, ×, etc.) - **NOT USED in this section**
- Special notation (\*italics\*, \~strikethrough\~) - Used sparingly
- Tables with pipes and hyphens - Multiple tables present

### Formula Handling
Multiple mathematical formulas present using Markdown code blocks:
```
Dash = [Max Dash / 10] * Rnd(5..8)
```

These should be copied exactly as-is, including the bracket notation and parenthetical definitions.

### Table Preservation
Multiple complex tables with:
- Multi-row headers
- Merged cells (indicated by empty columns)
- Probability notations (e.g., "7/16", "50/256")
- Mathematical expressions in cells

All table formatting should be preserved exactly.

### LaTeX Math
One LaTeX formula present (line 539):
```
$$x = 100 * Rnd(3..10)$$
```

Should be copied exactly as-is.

---

## Conclusion

The Chocobo Breeding section in `08_MINI_GAMES.md` is a **complete, authoritative, and substantive documentation** that must be fully extracted into the individual `FF7_Chocobo_Breeding.md` file.

**Key Facts:**
- Current individual file is empty (metadata only)
- Major section contains 529 lines of comprehensive breeding mechanics
- No images require processing
- Content is unique to this location
- Text should be copied verbatim with no modifications

**Readiness:** ✅ READY FOR PHASE 2 MERGE

The extraction is straightforward: copy all 529 lines verbatim from major section into the merged file, add proper markers and metadata, and commit.

---

**Report Created:** 2025-11-29 03:15 JST
**Next Phase:** Merge Execution (Phase 2)
**Estimated Merge Time:** 15-20 minutes
