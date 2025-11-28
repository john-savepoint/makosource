# Analysis: FF7_Battle_Battle_Scenes_Battle_Script.md vs 06_BATTLE_MODULE.md

**Created**: 2025-11-28 14:32 JST
**Analyzed**: Battle AI Opcode Documentation
**Status**: NO CONTENT OVERLAP - NO MERGE REQUIRED

---

## Executive Summary

This analysis compared the individual file `FF7_Battle_Battle_Scenes_Battle_Script.md` against the major section `06_BATTLE_MODULE.md` to identify content that should be merged.

**Key Finding: ZERO CONTENT OVERLAP**

| Metric | Value |
|--------|-------|
| Individual file size | 421 lines |
| Major section size | 1,764 lines |
| Topic alignment | ORTHOGONAL (completely different topics) |
| Content to extract | NONE |
| Images to merge | NONE |
| Merge required | NO |
| Recommendation | KEEP FILES AS-IS |

---

## Topic Scope Analysis

### FF7_Battle_Battle_Scenes_Battle_Script.md (Individual File)

**Primary Focus**: Battle AI Script Opcodes and Stack-based Virtual Machine

**Content Topics**:
- Battle AI script stack-based architecture
- Stack data types (Value, Address, Multiple Values)
- Opcode reference tables:
  - Push Values (0Xh)
  - Push Addresses (1Xh)
  - Mathematical & Bit-wise Operators (30h-37h)
  - Logical Operators (40h-45h)
  - Logical Comparisons (50h-52h)
  - Push Constants (60h-62h)
  - Script Jumps (70h-75h)
  - Bit Operations (80h-87h)
  - Commands (90h-A1h)
- Detailed notes on command behavior (90h-96h, A0h-A1h)
- MP cost calculation formulas (86h code notes)
- Command execution types (92h code notes)

**File Type**: Technical Reference - Low-level programming documentation

### 06_BATTLE_MODULE.md (Major Section)

**Primary Focus**: Battle Mechanics, Formulas, and System Design

**Content Topics**:
- Terence Fergusson's Battle Mechanics Guide (v0.8, 23/03/02)
- Character stats and derived stats
- Damage calculation formulas (17-step damage pipeline)
- Status effects and immunities
- Attack types and target types
- Equipment modifiers
- Battle mechanics terminology
- Enemy scene.bin file format
- PSX 3D battle models and bone structure
- PC battle models (battle.lpg file structure)
- Animation data format and rotation calculation

**File Type**: Systems Design & Implementation Guide

---

## Content Comparison Results

### CRITICAL FINDING: NO OVERLAP

After systematic analysis of the major section:

1. **Searched for opcode references**: No results
   - Patterns searched: "opcode", "command 90h", "push values", "stack", "AI script"
   - Result: Zero matches in major section

2. **Content verification**:
   - Major section lines 5004-6767: Terence Fergusson mechanics guide (damage formulas)
   - Major section lines 1663-1758: PC/PSX battle models and animation formats
   - Major section remainder: Scene.bin format, 3D bone structures
   - **No mention of**: AI scripting, opcodes, stack-based execution, battle AI

3. **Confirmation by structure**:
   - Individual file: 421 lines of opcode tables and AI documentation
   - Major section: 1,764 lines with ZERO paragraphs about AI scripting
   - Conclusion: These are completely separate knowledge domains

### Topic Separation Verified

| Topic | Major Section | Individual File |
|-------|---------------|-----------------|
| Battle Mechanics (damage, formulas) | ✅ EXTENSIVE (1000+ lines) | ❌ NOT COVERED |
| Enemy Battle Models (PSX) | ✅ DETAILED (300+ lines) | ❌ NOT COVERED |
| Enemy Battle Models (PC) | ✅ DETAILED (300+ lines) | ❌ NOT COVERED |
| Battle AI Opcodes | ❌ NOT COVERED | ✅ COMPLETE (421 lines) |
| Stack-based VM | ❌ NOT COVERED | ✅ DETAILED (100+ lines) |
| Scene.bin Format | ✅ COVERED | ❌ NOT COVERED |

---

## Individual File Content Already in Major Section?

**Answer: NO**

The Battle Script opcode documentation is **NOT** present anywhere in the major section. The individual file is:
- Self-contained
- Internally coherent
- Complete for its topic
- Not replicated or summarized in the major section

---

## Images Analysis

**Images in Individual File**: NONE (no ![](format) or <img> tags found)

**Images in Major Section** (if merged into individual file): NOT APPLICABLE - no merge needed

**Recommendation**: N/A

---

## Content Already in Individual File from Major Section?

**Query**: Does the individual file already contain content from the major section?

**Answer: NO**

The individual file focuses exclusively on:
- Opcode instruction reference (lines 29-374)
- General opcode notes (lines 377-422)

The major section's content (battle mechanics, formulas, models) is completely absent from the individual file.

---

## Content for Other Files

**Potential Related Files**:
- `FF7_Battle_Battle_Mechanics.md` - May benefit from reference to opcode cost calculation (86h notes)
- `FF7_Battle_Battle_Scenes.md` - May benefit from reference to scene.bin data structures in AI context
- `FF7_Playstation_Battle_Model_Format.md` - May benefit from reference to animation opcode system

**Recommendation**: No mandatory cross-file merging needed, but hyperlinks could improve navigation.

---

## Gaps and Discrepancies

### Gap Analysis

**In Individual File**:
- No explanation of HOW to use opcodes together (no code examples/sequences)
- No reference to which opcodes are used in actual enemy AI scripts
- No explanation of when each command group is typically used
- Limited explanation of stack type system scoping

**In Major Section**:
- No documentation of AI scripting system at all
- Scene.bin format described, but no explanation of AI scripts within scene.bin

**Recommendation**: Individual file could benefit from:
1. Examples of opcode sequences (if such exist)
2. Cross-reference to specific enemy AI implementations
3. Clarification of the complete battle execution flow (mechanics → AI → opcode execution)

### Verification Notes

- Individual file clearly attributes opcode information to "Terence Fergusson" (line 7)
- Major section is ALSO largely based on Terence Fergusson's Battle Mechanics Guide
- This suggests they are complementary works by the same author on different aspects

---

## Merge Plan Summary

### Recommendation: **DO NOT MERGE**

**Rationale**:
1. Zero content overlap - topics are orthogonal
2. Different file sizes reflect different scope (421 vs 1,764 lines)
3. Individual file is self-contained and complete for its topic
4. Major section does not claim to include opcode information
5. Both files serve different purposes in the documentation set

### File Status

- **FF7_Battle_Battle_Scenes_Battle_Script.md**: ✅ COMPLETE - No changes needed
- **06_BATTLE_MODULE.md**: ✅ COMPLETE - Self-contained in major sections

### Alternative Actions (Optional)

If documentation improvement is desired (NOT required):

1. **Add hyperlinks** from Battle Mechanics file to Battle Script file for opcode cost references
2. **Add context note** at top of Battle Script file: "For battle mechanics formulas that use opcode values, see FF7_Battle_Battle_Mechanics.md"
3. **Add section** to Scene.bin documentation explaining that AI scripts are stored within scene.bin files

---

## Files Examined

- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/extracted_major_sections/06_BATTLE_MODULE.md` (1,764 lines)
- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/FF7_Battle_Battle_Scenes_Battle_Script.md` (421 lines)
- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/extracted_major_sections/MAPPING.md` (context)

---

## Conclusion

The individual file `FF7_Battle_Battle_Scenes_Battle_Script.md` and the major section `06_BATTLE_MODULE.md` are **completely non-overlapping documents**. No merge operation is necessary or beneficial.

The MAPPING.md file's assessment is confirmed: these files represent different knowledge domains within the battle system documentation.

**Analysis Complete**: 2025-11-28 14:32 JST
