# Analysis: FF7_Battle_Battle_Mechanics.md vs 06_BATTLE_MODULE.md

**Analysis Date**: 2025-11-28
**Files Compared**:
- Source: `/docs/reference/game_engine/extracted_major_sections/06_BATTLE_MODULE.md` (1,764 lines)
- Target: `/docs/reference/game_engine/markdown/FF7_Battle_Battle_Mechanics.md` (660 lines)

---

## Executive Summary

### Content Alignment Overview

The major section `06_BATTLE_MODULE.md` contains **Terence Fergusson's comprehensive FF7 Battle Mechanics Guide** (lines 5-1097 in major section, covering ~1,000 lines), which is a completely distinct and **UNIQUE** document that does NOT appear in the individual file `FF7_Battle_Battle_Mechanics.md`.

The individual file focuses on **memory structures and data layout** (command defaults, queued actions, AI structure, active character data, actor battle data), while the major section is **Terence Fergusson's Battle Mechanics documentation** covering game balance formulas, damage calculations, status effects, and gameplay mechanics.

**Key Finding**: These are complementary documents covering different aspects of the battle system:
- Major section: Game mechanics, formulas, balance
- Individual file: Memory structures, data organization

### Content Statistics

| Metric | Value |
|--------|-------|
| Major section total lines | 1,764 |
| Individual file lines | 660 |
| Terence Fergusson content in major section | ~1,093 lines (lines 5-1097) |
| Scene.bin documentation in major section | ~355 lines (lines 1098-1453) |
| PC/PSX model documentation in major section | ~310 lines (lines 1504-1765) |
| **Content unique to major section** | ~1,658 lines |
| **Content to extract for individual file** | YES - all Terence Fergusson guide |
| **Images in extracted content** | 0 |

---

## Topic Scope Analysis

### Individual File Scope: FF7_Battle_Battle_Mechanics.md

**Current Coverage**:
- Command Defaults (3 items)
- Queued Actions (6 fields)
- AI Structure (14 memory locations)
- Active Character Data (48 memory locations + subtable for magic/summons/skills)
- Actor Battle Data (50+ memory locations with detailed breakdown)

**Topic**: Memory layout and in-game data structures related to battle mechanics

**Boundaries**: Strictly focused on **how battle data is organized in memory** - NOT on game balance, formulas, or effect calculations.

### Major Section Content Distribution

The major section (`06_BATTLE_MODULE.md`) contains content from multiple sources:

1. **Terence Fergusson's Battle Mechanics Guide** (lines 5-1097, ~1,093 lines)
   - Foreword and version history
   - Component guides overview
   - Definitions and terminology
   - Basic damage formulas
   - Battle damage calculation (19-step process)
   - Status effects (31 types, detailed descriptions)
   - Game Over conditions
   - Credits

2. **Enemy Battle Scenes (scene.bin)** (lines 1098-1453, ~355 lines)
   - Scene.bin file format documentation
   - By Fremen
   - Block structure and data file specifications
   - Battle setup, formations, enemy data, attack data
   - Enemy AI offsets

3. **PSX 3D Battle Scenes** (lines 1458-1662, ~205 lines)
   - By Micky
   - Background model format
   - Vertex, triangle, and quad data structures

4. **PSX Battle Models Structure** (lines 1504-1662, ~159 lines)
   - By Cyberman
   - Model format specifications
   - Bone structure, animation data
   - Section types and identification

5. **PC Battle Models Structure** (lines 1663-1765, ~103 lines)
   - By Mirex
   - File naming conventions
   - File structure info (.AA, .DA, .AM-.CJ formats)
   - Skeleton and animation specifications

---

## Content Already in Individual File

### Coverage Areas (Confirmed Present in FF7_Battle_Battle_Mechanics.md)

**✓ Memory Structures**:
- Command Defaults table (3 rows)
- Queued Actions structure (6 fields)
- AI Structure (14 memory locations)
- Active Character Data (48+ locations with sub-structures)
- Actor Battle Data (50+ locations with detailed breakdown)

**✓ Coverage**: 100% of currently documented memory structures

**Note**: These memory structures are NOT covered in the major section's Terence Fergusson guide.

---

## CRITICAL: Content to Extract

### Terence Fergusson's Complete Battle Mechanics Guide

**Source**: Major section lines 5-1097 (approximately 1,093 lines)

**Rationale for Extraction**:
1. Unique content not in individual file
2. Foundational game mechanics documentation
3. Essential reference for understanding battle system balance
4. Complements memory structures with game behavior explanations
5. Already signed/copyrighted material (should remain intact)

**Content Breakdown** (to be extracted verbatim):

| Section | Lines | Content |
|---------|-------|---------|
| Title & Version History | 1-31 | Title, version, copyright notice |
| Foreword | 13-31 | Author's context and intent |
| Component Guides Intro | 33-49 | Overview of three planned guides |
| Table of Contents | 51-65 | Detailed outline (20 items) |
| 1. Definitions | 67-241 | Character stats, terminology, attack types, target types, equipment modifiers |
| 2. Basic Damage Formulae | 258-276 | Physical and magical base damage formulas |
| 3. Battle Damage | 278-572 | 19-step damage calculation process with detailed formulas and conditions |
| 4. Statuses | 574-1031 | 31 status effects with detailed descriptions, mechanics, and interaction tables |
| 5. Game Over | 1046-1067 | Game over conditions and mechanics |
| 6. Credits | 1068-1088 | Author credits and acknowledgments |

**Key Formulas & Content** (samples to illustrate extraction):
- Base Damage Physical: `Base Damage = Att + [(Att + Lvl) / 32] * [(Att * Lvl) / 32]`
- Base Damage Magical: `Base Damage = 6 * (MAt + Lvl)`
- Damage calculation 19-step process (Defense, Berserk, Critical, Frog Check, MP Turbo, Back Row, Barrier/MBarrier, Sadness, Random Variation, Added Damage Effects, Elemental Damage, Sanity Checks, Negative Damage flag)
- Complete table of 31 status effects with: Visuals, Effects, Duration, Protection, Cure methods
- Status removal interaction tables (Esuna, Remedy, DeBarrier, DeSpell, White Wind, Angel Whisper)
- Magic and skills that can/cannot be reflected

**Why This Content Belongs in This File**:
- Completes the "Battle Mechanics" topic
- Memory structures + Game mechanics = Complete battle system documentation
- Provides context for how memory structures are used during damage calculation
- Authors other related battle files need these formulas as reference

### Scene.bin Documentation

**Source**: Major section lines 1098-1453 (~355 lines)

**Rationale**:
- Belongs to separate file: `FF7_Battle_Battle_Scenes.md` (already exists, verified)
- Should NOT be extracted to Battle Mechanics file
- Scene.bin is enemy configuration, not battle mechanics formulas

### Model Documentation (PSX/PC)

**Source**: Major section lines 1458-1765 (~307 lines)

**Rationale**:
- PSX models belong to: `FF7_Playstation_Battle_Model_Format.md` (exists, 10,833 lines - extremely detailed)
- PC models belong to: `FF7_Battle_Battle_Animation_PC.md` (exists, 912 lines)
- These should NOT be extracted to Battle Mechanics file
- Model formats are distinct from mechanics formulas

---

## Images in Extracted Content

### Image Inventory

**Total images to extract**: 0

The Terence Fergusson Battle Mechanics guide contains:
- Tables (formatted with markdown `|` pipes)
- Mathematical formulas (using markdown `$$` for LaTeX)
- Structured lists
- NO image files or image references

**Image Path Adjustments**: Not applicable

---

## Content Distribution Map

### What goes to FF7_Battle_Battle_Mechanics.md (THIS FILE)
✓ Terence Fergusson's complete Battle Mechanics Guide (lines 5-1097)

### What stays in FF7_Battle_Battle_Scenes.md
✓ Enemy Battle Scenes / scene.bin documentation (already there per MAPPING.md line 115)

### What stays in FF7_Playstation_Battle_Model_Format.md
✓ PSX battle models documentation (already there, 10,833 lines)

### What stays in FF7_Battle_Battle_Animation_PC.md
✓ PC animation file format (already there, 912 lines)

---

## Content Comparison at Topic Level

### Topic: Damage Calculation

**Individual File Coverage**:
- Memory structures only (offsets in Actor Battle Data)
- Example: offset 0x40h = "Damage Calculation", offset 0x44h = "Action's Element"

**Major Section Coverage** (Terence Fergusson):
- Complete 19-step damage calculation process (lines 278-572)
- All intermediate calculations with formulas
- Random variation, critical strikes, berserk, frog, barrier/mbarrier, elemental, status effects
- Detailed examples and mathematical notation

**Assessment**: MAJOR SUPPLEMENT - Extract all damage calculation content (lines 278-572, ~294 lines)

### Topic: Status Effects

**Individual File Coverage**:
- Memory offset references only
- Example: offset 0x048h = "Immune Statuses", offset 0x080h = "Inflicting Status(es)"

**Major Section Coverage** (Terence Fergusson):
- Complete documentation of all 31 status effects (lines 576-1031, ~456 lines)
- Each status includes: Visuals, Effects, Duration, Protected by, Cured by
- Status incompatibilities table (lines 951-968)
- Status removal methods table (lines 969-1007)
- Magic/skills that can/cannot be reflected (lines 1012-1045)

**Assessment**: MAJOR SUPPLEMENT - Extract all status documentation (lines 576-1031, ~456 lines)

### Topic: Character Stats

**Individual File Coverage**:
- Memory layout of stat storage in Active Character Data structure
- No explanations of what stats mean or how they're calculated

**Major Section Coverage** (Terence Fergusson):
- Section 1.1: Character Stats definitions (lines 69-106)
- Primary stats vs derived stats explanations
- Formula for each derived stat
- Bug note about armor magic defense

**Assessment**: MINOR SUPPLEMENT - Extract stats definitions (lines 69-106, ~38 lines)

### Topic: Attack Types

**Individual File Coverage**:
- None - only memory layout for storing attack properties

**Major Section Coverage** (Terence Fergusson):
- Section 1.2.2: Complete type definitions (Physical, Magical, Piercing, Attack, Absorb, LR, Restore, Recovery, Change Status, Misc)
- Lines 177-201

**Assessment**: EXTRACTION NEEDED - Extract attack types documentation (lines 177-201, ~24 lines)

### Topic: Target Types

**Individual File Coverage**:
- None - only memory offsets for target masks

**Major Section Coverage** (Terence Fergusson):
- Section 1.2.3: Target type definitions (1 Tar, <n> Tar, All Tar, All Tar (NS), Area, Random)
- Lines 203-234

**Assessment**: EXTRACTION NEEDED - Extract target types documentation (lines 203-234, ~31 lines)

### Topic: Elements

**Individual File Coverage**:
- None - only memory locations for element affinity tracking

**Major Section Coverage** (Terence Fergusson):
- Section 1.2.1 (Elements section): 11 common elements, 5 physical-only elements, 1 hidden element
- Descriptions of each element
- Lines 142-175

**Assessment**: EXTRACTION NEEDED - Extract element documentation (lines 142-175, ~33 lines)

---

## Merge Plan Summary

### Phase 1: Copy Original File
```bash
cp /docs/reference/game_engine/markdown/FF7_Battle_Battle_Mechanics.md \
   /docs/reference/game_engine/markdown/merged_with_pdf_content/FF7_Battle_Battle_Mechanics.md
```

### Phase 2: Identify Insertion Points

**Best insertion point**: After "Actor Battle Data" section (after line 661 in original file)

**Reason**: Memory structures documented first, then supplement with game mechanics that explain HOW those structures are used

### Phase 3: Extract Terence Fergusson Content

**Extract in this order** (to flow naturally):

1. **Definitions Section** (lines 67-241 from major, ~175 lines)
   - Explains all the terminology used later
   - Character stats, attack types, target types, equipment modifiers

2. **Basic Damage Formulae** (lines 258-276 from major, ~18 lines)
   - Foundation for understanding damage calculations

3. **Battle Damage (19-Step Process)** (lines 278-572 from major, ~294 lines)
   - Shows how memory structures are used in practice

4. **Statuses** (lines 574-1031 from major, ~457 lines)
   - Complete reference for status effects
   - Interaction tables essential for understanding status mechanics

5. **Game Over** (lines 1046-1067 from major, ~21 lines)
   - Completes mechanics documentation

### Phase 4: Add Extraction Markers

Use clear markers to show content origin:
```markdown
<!-- EXTRACTED FROM MAJOR SECTION: 06_BATTLE_MODULE.md (Lines X-Y)
     Source: Terence Fergusson's The Final Fantasy 7 Battle Mechanics (v0.8)
     Copyright: Terence Fergusson
     Original file paths preserved. No images. -->
```

### Phase 5: Verify No Loss

**Pre-merge integrity check**:
- Original file: 661 lines
- Extraction: ~965 lines
- Final merged file: ~1,626 lines

**Post-merge validation**:
- All original content preserved exactly
- All extraction content added verbatim
- No images to verify
- No path adjustments needed (no image references)

---

## Discrepancies & Notes

### Minor: Placeholder Content in Major Section

**Location**: Lines 1090-1094 (FF7 Party Mechanics section)
- Contains: Lorem ipsum placeholder
- Status: NOT to be extracted (placeholder content)
- Reason: Individual file should not include Lorem ipsum placeholders

**Location**: Lines 1454-1456 (Magic Scripting section)
- Contains: Lorem ipsum placeholder
- Status: NOT to be extracted
- Reason: Placeholder content

### Note: Copyright Attribution

**Content Source**:
- Lines 5-1088: Terence Fergusson's The Final Fantasy 7 Battle Mechanics (v0.8, March 23, 2002)
- Copyright notice at line 1088: "The FF7 Battle Mechanics, copyright 2001-2003 Terence Fergusson"

**Handling**:
- Preserve entire copyright notice when extracting
- Include author attribution in extraction marker
- This is copyrighted work properly attributed in original

### Note: Cross-References

**Links in Terence Fergusson content**:
- No URLs or external links in the content
- References to "Party Mechanics" and "Enemy Mechanics" guides are contextual (those aren't included in major section)
- Internal cross-references are minimal

---

## Recommendations for Merge Implementation

### 1. Ordering Strategy
Place extracted content AFTER the memory structure sections to maintain logical flow:
1. Memory structures (existing content)
2. Terence Fergusson's game mechanics guide (new extraction)
3. Bonus: Keep reference links to related documentation at end

### 2. Section Headers
The Terence Fergusson guide has clear internal headers that should be preserved:
- "1. DEFINITIONS"
- "2. BASIC DAMAGE FORMULAE"
- "3. BATTLE DAMAGE"
- "4. STATUSES"
- "5. GAME OVER"

These section headers should remain at their original heading level (H4 or H3).

### 3. Table Preservation
All tables in the Terence Fergusson content use markdown format and should be copied exactly:
- Character stats tables
- Attack type tables
- Status interaction tables (6 different ones)
- Skill reflection tables

### 4. Formula Preservation
Mathematical formulas use LaTeX notation in `$$..$$` blocks. Preserve exactly as-is.

### 5. No Content Reordering
Maintain Terence Fergusson's original structure and flow. This is signed work and should not be rearranged.

---

## Quality Checklist

- [x] Read entire major section (06_BATTLE_MODULE.md)
- [x] Read entire individual file (FF7_Battle_Battle_Mechanics.md)
- [x] Identified content scope for this file
- [x] Identified related files and their scope
- [x] Mapped content to appropriate files
- [x] Identified all unique content in major section
- [x] Counted lines and formulas to extract
- [x] Searched for images (found 0)
- [x] Verified copyright attribution
- [x] Created extraction plan with line numbers
- [x] Documented insertion point
- [x] Explained why each extraction belongs in this file

---

## Files Ready for Merge

**Individual file to merge into**:
`/docs/reference/game_engine/markdown/merged_with_pdf_content/FF7_Battle_Battle_Mechanics.md`

**Total extraction**: ~965 lines from lines 5-1088 of major section (Terence Fergusson's Battle Mechanics Guide)

**Extraction is READY** - all content identified, line numbers marked, rationale documented.
