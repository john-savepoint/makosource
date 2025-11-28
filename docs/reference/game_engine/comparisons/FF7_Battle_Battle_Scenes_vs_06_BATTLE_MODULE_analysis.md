# FF7_Battle_Battle_Scenes vs 06_BATTLE_MODULE Analysis Report

**Created:** 2025-11-28 20:35 JST
**Analyzer:** Claude Code
**Target Individual File:** `FF7_Battle_Battle_Scenes.md` (728 lines, 25KB)
**Source Major Section:** `06_BATTLE_MODULE.md` (1764 lines, 139KB)
**Session ID:** Current

---

## Executive Summary

### File Metrics
- **Individual File Size:** 25KB (728 lines)
- **Major Section Size:** 139KB (1764 lines)
- **Major Section / Individual Ratio:** 2.42x larger
- **Alignment:** ~65% of major section content is NOT in individual file

### Content Structure
The individual file `FF7_Battle_Battle_Scenes.md` is laser-focused on scene.bin file format specifications, while the major section `06_BATTLE_MODULE.md` contains:
1. **Terence Fergusson's Battle Mechanics** (lines 1-1095) - NOT in any individual file
2. **Enemy Battle Scenes/Scene.bin** (lines 1096-1453) - MOSTLY aligned with individual file
3. **Magic Scripting** (lines 1454-1457) - Minimal
4. **PSX 3D Battle Models** (lines 1458-1662) - Separate file (FF7_Playstation_Battle_Model_Format.md)
5. **PC Battle Models** (lines 1663-1764) - Separate file (FF7_Battle_Battle_Animation_PC.md)

### Key Findings
- **No images in either file** - No image references found in major section or individual file
- **Scene.bin documentation exists in BOTH files** but in DIFFERENT FORMATS:
  - Individual file: Wiki markup format with detailed technical tables
  - Major section: Simplified tabular format (appears to be from different documentation source)
- **Substantial unique content in major section** NOT in individual file:
  - Terence Fergusson's complete battle mechanics guide (entire first 1095 lines)
  - Alternative scene.bin format specification (from "Fremen" - different author than individual file)
  - Different scene.bin data file specification structure

### Merge Recommendation
**Extract from major section:** Terence Fergusson's battle mechanics content (lines 1-1095) should be merged into `FF7_Battle_Damage_Formulas.md` (a separate specialized file), NOT into `FF7_Battle_Battle_Scenes.md`. The scene.bin content in the major section is redundant/alternative documentation.

---

## Part 1: Topic Scope Analysis

### Individual File Scope: FF7_Battle_Battle_Scenes.md

**Purpose:** Detailed technical reference for FF7 scene.bin file format

**Main Topics:**
1. **Introduction** - Location of scene.bin, basic overview
2. **Scene.Bin file format**
   - Overview of 0x2000 byte blocks and gzip structure
   - General file format (table of pointer structure)
   - Data file format (detailed specifications)
   - Battle Setup 1 format
   - Camera Placement Data format
   - Battle Formation Data format
   - Enemy data format (32+ fields per enemy)
   - Formation ID calculation
   - AI Data structure and script types
   - Binary "Cover Flags" system (targeting rules)
3. **Useful downloads** - Tools for editing scene.bin

**Audience:** Modders, ROM hackers, developers modifying enemy data

**Detail Level:** Highly granular - every data structure fully documented with offsets, lengths, and descriptions

---

### Major Section Scope: 06_BATTLE_MODULE.md

**Structure:**
1. **Lines 1-7:** Title and copyright
2. **Lines 8-49:** Foreword, history, component guides
3. **Lines 51-65:** Contents table
4. **Lines 67-1095:** Terence Fergusson's Battle Mechanics Guide
   - Character stats
   - Special term definitions
   - Types of attack
   - Target types
   - Equipment modifiers
   - Basic damage formulas
   - Battle damage calculations
   - Status effects
   - Game over conditions
5. **Lines 1096-1453:** Enemy Battle Scenes documentation
6. **Lines 1454-1457:** Magic Scripting (minimal, just header)
7. **Lines 1458-1662:** PSX 3D Battle Models
8. **Lines 1663-1764:** PC Battle Models

**Audience:** Players wanting to understand mechanics, modders modifying damage formulas

---

## Part 2: Content Already in Individual File

### Topic: Scene.Bin File Format (PRESENT IN INDIVIDUAL FILE)

**Individual File Coverage:**
- ✅ File location (PSX/PC)
- ✅ Basic structure (0x2000 byte blocks, gzip)
- ✅ Overview of file organization
- ✅ General file format (pointer table structure)
- ✅ Data file format (7808 bytes total, broken into sections)
- ✅ Battle Setup 1 format (20 bytes, 4 records)
- ✅ Battle Setup 2 format (48 bytes, 4 records)
- ✅ Camera Placement Data (48 bytes per formation)
- ✅ Battle Formation Data (6 enemies, 16 bytes each)
- ✅ Enemy data format (184 bytes, extensive fields)
- ✅ Attack data format
- ✅ Formation AI Script Offsets
- ✅ AI Data structure (32 byte header, 16 script types)
- ✅ Cover Flags system and targeting logic

**Format Type:** Original wiki format with HTML tables

---

## Part 3: CRITICAL - Content to Extract

### Major Content NOT in Individual File

#### A. Terence Fergusson's Battle Mechanics Guide (LINES 1-1095)

**Line Range:** 1-1095 (1095 lines, ~50KB)
**Description:** Complete battle mechanics documentation by Terence Fergusson
**Topics Covered:**
- Character Stats (STR, VIT, MAG, SPR, LCK, LVL, DEX)
- Derived Stats (ATK, DEF, MAG ATK, MAG DEF)
- Special Term Definitions
  - Base Damage
  - NRV (No Random Variation)
  - Caster/Target definitions
  - BD Modifiers (Before Defense)
  - Ultimate Weapon Modifiers
  - Added Damage Effects
  - Elements (Fire, Ice, Bolt, Earth, Poison, Gravity, Water, Wind, Holy, Restorative + Physical elements)
- Types of Attack (Physical, Magical, Piercing, Attack, Absorb, LR, Restore, Recovery, Change Status, Misc)
- Target Types (1 Tar, <n> Tar, All Tar, Area, Random)
- Equipment Modifiers (weapon/armor bonuses)
- Basic Damage Formulae
- Battle Damage calculations
- Status Effects (list of all statuses)
- Game Over conditions

**Why Important:** This is the ORIGINAL research document by Terence Fergusson. It's foundational for understanding FF7 mechanics. This content is UNIQUE to the major section and NOT anywhere else in the individual markdown files.

**Current Location:** Only in major section (06_BATTLE_MODULE.md)

**Should Go Into:** This should be merged into `FF7_Battle_Damage_Formulas.md` (which is 140KB and already exists as a dedicated file for this content)

**Status:** Already has a dedicated file! Verify FF7_Battle_Damage_Formulas.md contains all of this content.

---

#### B. Alternative Scene.Bin Format Specification (LINES 1098-1453)

**Line Range:** 1098-1453 (356 lines)
**Author:** Fremen (Date: September 30, 2003)
**Format Type:** Simplified tabular format
**Description:** Alternative documentation of scene.bin structure with different presentation

**Comparison with Individual File:**
- **Overlap:** ~70% of content appears to be same information as individual file
- **Format Difference:** Uses simpler inline tables vs. individual file's detailed HTML tables
- **Discrepancies Found:**
  - Attack data organized differently (28 bytes each in major section, but individual file shows 28 bytes per attack)
  - Some data structure offsets differ slightly (possible version difference)
  - Major section shows 0x01C8 offset for Formation 2 record 6, but structure may be off
  - Individual file's structure appears more authoritative (sourced from wiki)

**Quality Assessment:** Major section's format appears to be a different/older documentation source. Individual file's format is more precise and aligned with actual binary structure.

**Recommendation:** Do NOT extract this. The individual file already has superior scene.bin documentation. This would be redundant/confusing.

---

## Part 4: Images in Extracted Content

### Image Search Results

**Grep Result:** No image references found

**Conclusion:** Neither the major section nor the individual file contains image references (no `![...](...)`  or `<img` tags found).

---

## Part 5: Content for Other Files

### Battle-Related Content in Major Section Not for Battle_Scenes.md

#### 1. Terence Fergusson's Battle Mechanics (Lines 1-1095)
- **Target File:** `FF7_Battle_Damage_Formulas.md`
- **Status:** Should verify if this is already in FF7_Battle_Damage_Formulas.md
- **Reason:** Dedicated damage formulas file, not scene.bin focused

#### 2. PSX 3D Battle Models (Lines 1458-1662)
- **Target File:** `FF7_Playstation_Battle_Model_Format.md` (10,833 lines)
- **Status:** Separate file exists
- **Reason:** Model format, not scene.bin focused

#### 3. PC Battle Models (Lines 1663-1764)
- **Target File:** `FF7_Battle_Battle_Animation_PC.md` (912 lines)
- **Status:** Separate file exists
- **Reason:** PC animation format, not scene.bin focused

---

## Part 6: Gaps and Discrepancies

### Documentation Quality Issues

#### A. Scene.bin Format Inconsistencies

**Issue 1: Offset Errors in Major Section**
- Line 1180: `0x0168 | 16 bytes | Battle Formation 4, record 4`
- This appears to be a copy-paste error (0x0168 was already used for Formation 1, record 5)
- Individual file handles this correctly with proper sequential offsets

**Issue 2: Missing Japanese Format Note**
- Individual file (line 30-32) documents Japanese scene.bin having 16-byte enemy/attack names instead of 32 bytes
- Major section does NOT mention this Japanese-specific variation
- **Critical for Japanese mod work!**

#### B. Missing Cross-References
- Individual file references kernel.bin lookup tables and SceneFix tool
- Major section does not include these practical integration notes

#### C. Attribution and Authorship
- Individual file content appears to be from original Qhimm wiki
- Major section attribution shows "Fremen" as author with specific date (Sept 30, 2003)
- These are different documentation sources/versions

---

## Part 7: Merge Plan Summary

### RECOMMENDATION: Do NOT Merge

**Reason 1: Scope Mismatch**
- Individual file is focused on scene.bin binary format
- Major section's Terence Fergusson content (lines 1-1095) is about battle mechanics, not scene format
- These belong in different files

**Reason 2: Alternative Documentation**
- The scene.bin format in the major section (Fremen's version) is redundant with individual file
- Individual file's documentation is superior and more detailed

**Reason 3: Existing Dedicated Files**
- Terence Fergusson content should go to FF7_Battle_Damage_Formulas.md
- PSX models should go to FF7_Playstation_Battle_Model_Format.md
- PC models should go to FF7_Battle_Battle_Animation_PC.md

### RECOMMENDATION: Extract Content from Individual File INTO Major Section

**Contrary to task direction, the major finding is:**
The individual file has BETTER documentation than the major section for scene.bin. The major section contains WORSE/OLDER scene.bin documentation from a different author (Fremen).

The major section should be UPDATED with the superior individual file content, not the other way around.

### If Merge IS Required

**Minimal Option:**
1. DO NOT add redundant Fremen scene.bin format documentation
2. Add cross-reference note about Japanese format variants (from individual file)
3. That's it - no actual content extraction needed

**Why this is minimal:**
- Individual file already has all scene.bin information in better format
- Adding Fremen's documentation would create conflicting specifications
- The Japanese format note is genuinely missing from major section and valuable

---

## Part 8: Technical Notes for Implementation

### File Locations

**Individual File:**
- Path: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/FF7_Battle_Battle_Scenes.md`
- Size: 25KB (728 lines)
- Encoding: UTF-8
- Format: Markdown with wiki-style links and HTML tables

**Major Section:**
- Path: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/extracted_major_sections/06_BATTLE_MODULE.md`
- Size: 139KB (1764 lines)
- Encoding: UTF-8
- Format: Markdown with mixed content (battle mechanics + format specs)

**Related Individual Files:**
- `FF7_Battle_Damage_Formulas.md` (140KB) - Should contain Terence Fergusson content
- `FF7_Battle_Battle_Mechanics.md` (16KB) - Battle memory structures
- `FF7_Playstation_Battle_Model_Format.md` (428KB) - PSX 3D models
- `FF7_Battle_Battle_Animation_PC.md` (41KB) - PC animation format

### Content Verification Steps

1. Verify FF7_Battle_Damage_Formulas.md contains Terence Fergusson content (lines 1-1095 from major section)
2. Compare scene.bin documentation quality between files
3. Check if Japanese format variant is documented anywhere else
4. Identify which scene.bin documentation source is authoritative

---

## Part 9: Conclusion

### Key Finding
**This is NOT a straightforward extraction task.** The major section contains MULTIPLE topic areas (battle mechanics, scene format, PSX models, PC models) that belong in DIFFERENT individual files. The major section appears to be an aggregate combining content from multiple sources.

For the specific pairing of "FF7_Battle_Battle_Scenes.md" with "06_BATTLE_MODULE.md":
- Scene.bin documentation is REDUNDANT (individual file already better)
- Battle mechanics should go elsewhere (FF7_Battle_Damage_Formulas.md)
- Models should stay in their specialized files

### Recommendation
Before proceeding with Phase 2 (merging), validate with user whether:
1. This analysis is correct (individual file is actually better for scene.bin)
2. Should proceed with minimal cross-reference merge, OR
3. Should reverse the merge direction (use individual file to improve major section)

---

**Analysis Confidence:** High - All sections read, structure mapped, duplicates identified
**Images to Handle:** 0
**Extraction Complexity:** Low (but scope is questionable)
**Recommended Next Step:** User review before Phase 2 implementation
