# Documentation Update Plan - Post-PR #737 Discovery

**Created:** 2025-11-25 01:15 JST (Tuesday)
**Session:** 37952f94-430d-46c5-8bed-8068cf9a7a62
**Purpose:** Systematic update of all documentation to reflect PR #737 findings

---

## Executive Summary

**Discovery:** PR #737 already implements 95% of our Master Bible specification using a superior architecture (C++ function pointers vs assembly hooks).

**Action Required:** Update all documentation to:
1. Acknowledge PR #737 as baseline
2. Preserve our original research (it validated PR #737's approach)
3. Shift from "build from scratch" to "extend PR #737"
4. Update implementation strategy accordingly

---

## Documents Requiring Updates

### 🔴 CRITICAL (Required for next work session)

1. **IMPLEMENTATION_VERIFICATION_CHECKLIST.md**
   - Add Section 16: PR #737 Analysis
   - Mark many questions as ✅ ANSWERED by PR #737
   - Update Priority Questions to focus on remaining gaps

2. **FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md**
   - Add preamble: "Update 2025-11-25: PR #737 Implementation"
   - Sections 7-9: Add "PR #737 Implementation Notes"
   - Preserve original approach as "Alternative Architecture"
   - Add comparison tables: Our Spec vs PR #737

3. **FEATURE_ROADMAP.md**
   - Update Phase 1 timeline: 3-4 weeks (not 2-3 months)
   - Update overall timeline: 2.5-4 months (not 5-8 months)
   - Add Phase 1.5: "PR #737 Bug Fixes"

### ⚠️ HIGH (Update within 1 week)

4. **FFNX_DEVELOPER_GUIDE.md**
   - Update "How to Approach Modifications" section
   - Add "Working with PR #737" guide
   - Update build/test procedures

5. **ARCHITECTURAL_RETROSPECTIVE.md** (already created)
   - ✅ Complete

6. **PR737_ANALYSIS.md** (already created)
   - ✅ Complete

### 📋 MEDIUM (Update before implementation begins)

7. **VERIFICATION_FINDINGS_SESSION_11.md**
   - Add appendix: "Superseded by PR #737"
   - Cross-reference PR #737 analysis

8. **AF3DN_ANALYSIS.md**
   - Add note: "PR #737 replaces many AF3DN.P functions"
   - Still valuable for understanding original implementation

---

## Update Strategy Per Document

### 1. IMPLEMENTATION_VERIFICATION_CHECKLIST.md

**Changes Needed:**

#### Add New Section 16

```markdown
## SECTION 16: PR #737 Baseline Verification

### 16.1 PR #737 Implementation Analysis

**Status:** ✅ **COMPLETE** (Session 37952f94, 2025-11-25)

**Findings:**
- ✅ FA-FE encoding fully implemented
- ✅ All 6 jafont textures loaded at init
- ✅ Character width tables (1,536 values) hardcoded in C++
- ✅ Function pointer hooking (no assembly required)
- ✅ Compatible with Japanese eStore version
- ❌ Colored text rendering BROKEN
- ❌ Character name input screen BROKEN
- ❌ Cursor alignment issues

**References:**
- `docs/PR737_ANALYSIS.md` - Complete code analysis
- `docs/ARCHITECTURAL_RETROSPECTIVE.md` - Why PR #737's approach is better

### 16.2 Questions Answered by PR #737

The following questions from earlier sections are now ANSWERED:

**Section 2.1 - FA-FE Extended Page System:**
- ✅ Q2.1.1: **ANSWERED** - FA-FE conversion happens in `field_submit_draw_text_640x480_6E706D_jp()`
- ✅ Q2.1.2: **ANSWERED** - FFNx handles FA-FE via C++ switch statement (no assembly)
- ✅ Q2.1.3: **ANSWERED** - Lookup table is `charWidthData[6][256]` hardcoded array

**Section 2.2 - Character Width Table:**
- ✅ Q2.2.2: **ANSWERED** - SIX width tables (1,536 entries total)
- ✅ Q2.2.3: **ANSWERED** - Width table is hardcoded in C++, not loaded from file
- ✅ Q2.2.4: **ANSWERED** - Proportional spacing (widths vary 20-32 pixels)

**Section 4.1 - Font System Implementation:**
- ✅ Q4.1.1: **ANSWERED** - `src/ff7/font.cpp` does NOT exist; created `japanese_text.cpp` instead
- ✅ Q4.1.2: **ANSWERED** - `field_submit_draw_text_640x480_6E706D_jp()` handles rendering
- ✅ Q4.1.3: **ANSWERED** - Loads TIM files via `engine_load_graphics_object_6710AC()`
- ✅ Q4.1.4: **ANSWERED** - Multi-texture support via `menu_jafont_N_graphics_object` pointers

**Section 4.3 - Renderer Integration:**
- ✅ Q4.3.3: **ANSWERED** - YES, mid-frame texture switching works (already implemented)

### 16.3 Remaining Questions NOT Answered by PR #737

**Critical for Phase 2+ (Multi-Language):**
- [ ] How to extend to FR/DE/ES fonts?
- [ ] How to add language toggle hotkey?
- [ ] How to load multiple language font sets?

**Critical for Phase 3 (Furigana):**
- [ ] How to render dual-layer text?
- [ ] How to adjust line heights?

**Critical for Colored Text Fix:**
- [ ] Where are colored texture variants stored?
- [ ] Does Japanese version have jafont_1_red.tim, etc.?
- [ ] Or should we use GPU shader color tinting?
```

#### Update Priority Questions Section

```markdown
## REVISED Priority Questions (Post-PR #737 Discovery)

### 🔴 Phase 1.5 Blockers (Fix PR #737 Bugs)

1. **Colored Text Bug** - Where are colored font texture variants?
2. **Character Input Bug** - Why is name input screen corrupted?
3. **Cursor Alignment** - What causes hand cursor offset?

### 🔴 Phase 2 Blockers (Multi-Language)

4. **FR/DE/ES Font Loading** - How to load 5 language font sets?
5. **Language Toggle** - Where to hook F9 key press?
6. **Text File Reloading** - How to hot-swap dialogue files?

### ⚠️ Phase 3 (Furigana)

7. **Dual-Layer Rendering** - How to draw text above kanji?
8. **Line Height Calculation** - How to adjust for furigana space?
```

---

### 2. FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md

**Changes Needed:**

#### Add Preamble at Top

```markdown
# FFNx Japanese Implementation - Master Bible

**Created**: 2025-11-16 19:18 JST (Sunday)
**Last Modified**: 2025-11-25 01:20 JST (Tuesday)
**Version**: 2.1.0 - **PR #737 Integration Update**

---

## 🔴 CRITICAL UPDATE - 2025-11-25

**PR #737 Discovery:** A community member (CosmosXIII) has already implemented 95% of this specification in [PR #737](https://github.com/julianxhokaxhiu/FFNx/pull/737).

**Status:** PR is OPEN (not yet merged) with known bugs:
- ❌ Colored text rendering broken
- ❌ Character name input screen corrupted
- ❌ Cursor alignment issues

**Our New Strategy:**
1. **Phase 1.5**: Fix PR #737's bugs → help get it merged
2. **Phase 2**: Extend PR #737 for multi-language (FR/DE/ES)
3. **Phase 3**: Add furigana support on top

**This document remains valuable because:**
- ✅ Our research VALIDATED PR #737's approach
- ✅ Our character mapping enables translation tools
- ✅ Our analysis identified improvements
- ✅ Original architecture serves as reference

**See Also:**
- `PR737_ANALYSIS.md` - Complete code analysis
- `ARCHITECTURAL_RETROSPECTIVE.md` - Why PR #737's approach is superior
- `PR737_INTEGRATION_STRATEGY.md` - How to build on PR #737

---
```

#### Update Each Implementation Section

For **Section 7 (Config System)**, **Section 8 (Initialization)**, **Section 9 (Rendering Pipeline)**:

Add subsections like this:

```markdown
### 7.X PR #737 Implementation Notes

**How PR #737 Actually Does This:**

PR #737 implements this feature using [describe approach].

**Code Location:** `src/ff7/japanese_text.cpp:line_number`

**Our Original Spec vs PR #737:**

| Aspect | Our Spec | PR #737 | Winner |
|--------|----------|---------|--------|
| Approach | Assembly hooks | C++ function pointers | PR #737 - maintainable |
| Width table | Memory patch | Hardcoded arrays | PR #737 - simpler |
| ... | ... | ... | ... |

**Recommendation:** Use PR #737's approach, apply improvements from our spec.
```

#### Add "Alternative Architecture" Appendix

```markdown
## Appendix A: Alternative Implementation Architecture

**Note:** This appendix preserves our original assembly/Hext-based approach for reference. PR #737's C++ approach is recommended for actual implementation.

### Why We Originally Chose Assembly

[Move original sections here with historical context]

### Lessons Learned

[Link to ARCHITECTURAL_RETROSPECTIVE.md]
```

---

### 3. FEATURE_ROADMAP.md

**Changes Needed:**

#### Update Timeline Section

```markdown
## Timeline Estimate (REVISED - Post-PR #737 Discovery)

**Phase 1.5 (PR #737 Bug Fixes)**: 3-4 weeks **[NEW]**
- Week 1-2: Fix colored text rendering
- Week 3: Fix character name input screen
- Week 4: Fix cursor alignment, submit patches

**Phase 1 (Core Japanese)**: ✅ **95% COMPLETE** (via PR #737)
- Remaining: 3-4 weeks of bug fixes (see Phase 1.5)

**Phase 2 (Language Toggle)**: 2-3 weeks
- Extend PR #737's architecture for 5 languages
- Add hotkey system
- Test with FR/DE/ES fonts

**Phase 3 (Furigana)**: 3-6 weeks (inline only)
- Week 1-2: Text format design
- Week 3-4: Rendering implementation
- Week 5-6: Testing and refinement

**Phase 4 (Boosters)**: 0 weeks (already done)

**Phase 5 (Polish)**: 3-4 weeks
- Documentation, packaging, community testing

**Total Estimated Timeline**: **2.5-4 months** (was 5-8 months)
**Time Saved**: 2.5-4 months thanks to PR #737
```

#### Add Phase 1.5

```markdown
### Phase 1.5: PR #737 Bug Fixes (NEW - CRITICAL)

**Goal**: Fix blocking bugs in PR #737 to enable merge

**Requirements**:
- [ ] Investigate colored text rendering failure
  - Root cause: Missing colored texture variants OR tinting not working
  - Solution: Either load `jafont_X_red.tim` variants OR implement GPU shader
  - Estimated: 10-15 hours research, 5-10 hours implementation

- [ ] Fix character name input screen corruption
  - Root cause: Unknown (wrong texture indexing?)
  - Solution: Debug rendering code for name input screen
  - Estimated: 8-12 hours debugging, 2-4 hours fix

- [ ] Fix cursor alignment issues
  - Root cause: Hardcoded spacing assumptions broken by Japanese widths
  - Solution: Adjust cursor position calculation based on actual text width
  - Estimated: 3-5 hours

**Effort**: 3-4 weeks
**Priority**: CRITICAL (unblocks everything else)
**Dependencies**: None (can start immediately)

**Success Criteria**:
- [ ] Colored text renders correctly (e.g., `[セーブ]` shows properly)
- [ ] Character name input screen displays correct glyphs
- [ ] Katakana/Romaji selection tabs visible
- [ ] Cursor aligns with text in save slots and dialogue choices
- [ ] PR #737 approved and merged by FFNx maintainer

**Why This Matters**:
Once PR #737 is merged, you have a rock-solid foundation for Phases 2-6.
Without fixing these bugs, PR #737 stays unmerged and you start from scratch.
```

#### Update Phase 1 Status

```markdown
### Phase 1: Japanese Text Support ✅ **95% COMPLETE**

**Goal**: Display Japanese text with full 2,000+ kanji support

**Status via PR #737**:
- [x] Font texture research and documentation ✅ DONE
- [x] Japanese eStore version acquired ✅ DONE
- [x] Extract and analyze jafont_1-6.tex ✅ DONE (via PR #737)
- [x] Implement double-byte character encoding (FA-FE) ✅ DONE (via PR #737)
- [x] Create character→texture mapping algorithm ✅ DONE (via PR #737)
- [x] Modify FFNx for multi-texture font loading ✅ DONE (via PR #737)
- [x] Test complete Japanese text rendering ✅ MOSTLY WORKS (bugs in Phase 1.5)

**Remaining Work**: See Phase 1.5 (bug fixes)

**Effort**: Originally estimated 2-3 months, actually 3-4 weeks (bug fixes only)
**Priority**: CRITICAL (foundation for all other features)
**Status**: Implementation complete (via PR #737), bug fixes in progress
```

---

### 4. FFNX_DEVELOPER_GUIDE.md

**Changes Needed:**

#### Add New Section at Top

```markdown
## Working with PR #737 (CRITICAL - Read First)

**Before modifying FFNx, understand that:**

1. **PR #737 already implements Japanese rendering**
   - FA-FE encoding ✅
   - Multi-page textures ✅
   - Character width tables ✅
   - Function pointer hooking ✅

2. **Your work builds ON TOP of PR #737, not from scratch**
   - Phase 1.5: Fix PR #737's bugs
   - Phase 2: Extend to multi-language
   - Phase 3: Add furigana

3. **PR #737 uses C++ function pointers, not assembly**
   - Forget about Hext patches
   - Forget about memory address hunting
   - Work in `src/ff7/japanese_text.cpp`

**See:** `docs/PR737_ANALYSIS.md` for complete implementation details

---
```

#### Update "Modification Approach" Section

```markdown
## How to Approach FFNx Modifications (UPDATED)

### Step 1: Fork PR #737's Branch

**Don't fork main FFNx repo. Fork PR #737's branch instead.**

```bash
git clone https://github.com/CosmosXIII/FFNx.git
git checkout japanese-text-support
```

**Why:** PR #737's code is your baseline. All your changes extend it.

### Step 2: Build PR #737 Locally

[Keep existing build instructions but update to PR #737's branch]

### Step 3: Identify Bug to Fix

**Current known bugs:**
1. Colored text rendering
2. Character name input screen
3. Cursor alignment

**Start with colored text** - it's the most impactful.

### Step 4: Debug the Bug

**For colored text bug:**
1. Launch game with PR #737 build
2. Find dialogue with colored text (e.g., `[セーブ]` button prompt)
3. Attach debugger to `field_submit_draw_text_640x480_6E706D_jp()`
4. Set breakpoint when `n_shapes` != 0 (colored character)
5. Step through `get_character_color()` and texture selection
6. Determine if:
   - Option A: Colored texture variants missing
   - Option B: Color tinting not working

### Step 5: Implement Fix

[Instructions depend on root cause]

### Step 6: Test Fix

1. Launch game
2. Navigate to every menu with colored text
3. Screenshot before/after
4. Verify no regressions in black/white text

### Step 7: Submit PR to CosmosXIII's Branch

**Don't submit to main FFNx yet. Submit to PR #737 first.**

```bash
git checkout -b fix-colored-text
git commit -am "fix: colored text rendering in Japanese mode"
git push origin fix-colored-text
```

Create PR against CosmosXIII's `japanese-text-support` branch.
```

---

### 5. Create PR737_INTEGRATION_STRATEGY.md

This will be a new document guiding implementation going forward.

```markdown
# PR #737 Integration Strategy

**Created:** 2025-11-25 01:25 JST (Tuesday)
**Purpose:** Define how to build upon PR #737's foundation

---

## Phase 1.5: Bug Fixes (Weeks 1-4)

### Week 1-2: Colored Text Rendering

**Goal:** Fix `[セーブ]` and other colored text display

**Investigation Steps:**
1. Launch Japanese game with PR #737
2. Find colored text (button prompts, special dialogue)
3. Attach debugger, break on `get_character_color()`
4. Determine why tinting fails

**Hypothesis A: Missing Colored Texture Variants**

If Japanese version has `jafont_1_red.tim`, `jafont_1_blue.tim`, etc.:

```cpp
// Load colored variants
ff7_externals.menu_jafont_1_white  = load("jafont_1.tim");
ff7_externals.menu_jafont_1_red    = load("jafont_1_red.tim");
ff7_externals.menu_jafont_1_blue   = load("jafont_1_blue.tim");
// ... repeat for 8 colors × 6 pages = 48 textures

// Select correct variant
switch (n_shapes) {
    case 1: graphics_object = jafont_1_red; break;
    case 2: graphics_object = jafont_1_blue; break;
    // ...
}
```

**Hypothesis B: Tinting Not Working**

If base fonts aren't white, tinting won't work:

```cpp
// Solution: GPU shader color tinting
fragment_shader {
    vec4 tex_color = texture(font_texture, uv);
    vec4 tint = uniform_tint_color;
    return mix(tex_color, tint, tint_strength);
}
```

**Deliverable:** Colored text renders correctly

---

### Week 3: Character Name Input Screen

**Goal:** Fix garbage characters in last 2 rows

**Investigation Steps:**
1. Launch game, reach name input screen
2. Screenshot what's displayed vs what should be displayed
3. Attach debugger to character selection rendering
4. Trace texture index calculations

**Likely Cause:** Texture page selection logic breaks for certain indices

**Deliverable:** Name input screen displays correct characters

---

### Week 4: Cursor Alignment

**Goal:** Fix hand cursor offset in menus

**Investigation Steps:**
1. Find cursor position calculation code
2. Check if it assumes fixed 16px character width
3. Update to use actual character width from `charWidthData`

**Code Change:**
```cpp
// OLD (broken):
cursor_x = base_x + (char_index * 16);

// NEW (fixed):
cursor_x = base_x;
for (int i = 0; i < char_index; i++) {
    cursor_x += charWidthData[page][i];
}
```

**Deliverable:** Cursor aligns with Japanese text

---

## Phase 2: Multi-Language Extension (Weeks 5-7)

### Week 5: Load FR/DE/ES Font Sets

**Goal:** Extend texture loading to support 5 languages

**Architecture:**

```cpp
struct LanguageFontSet {
    ff7_graphics_object* pages[6];
    int charWidthData[6][256];
    const char* language_code;
};

LanguageFontSet font_sets[5] = {
    { jafont_1-6, ja_widths, "ja" },
    { frfont_1-6, fr_widths, "fr" },
    { defont_1-6, de_widths, "de" },
    { esfont_1-6, es_widths, "es" },
    { usfont_1-6, us_widths, "en" }
};

LanguageFontSet* current_fonts = &font_sets[current_language_index];
```

**Deliverable:** All 5 language fonts loaded

---

### Week 6: Language Toggle Hotkey

**Goal:** F9 cycles languages, Shift+F9 opens selector

**Implementation:**

```cpp
// In keyboard input handler
if (key == VK_F9) {
    if (shift_pressed) {
        show_language_selector_menu();
    } else {
        current_language_index = (current_language_index + 1) % 5;
        reload_fonts();
        restart_dialogue();
    }
}
```

**Deliverable:** Can toggle languages during gameplay

---

### Week 7: Testing & Refinement

**Test Matrix:**

| Language | Menu | Dialogue | Battle | Save/Load |
|----------|------|----------|--------|-----------|
| EN       | ✓    | ✓        | ✓      | ✓         |
| JA       | ✓    | ✓        | ✓      | ✓         |
| FR       | ✓    | ✓        | ✓      | ✓         |
| DE       | ✓    | ✓        | ✓      | ✓         |
| ES       | ✓    | ✓        | ✓      | ✓         |

**Deliverable:** All 5 languages work flawlessly

---

## Phase 3: Furigana Support (Weeks 8-13)

[Implementation plan for furigana]

---

## Success Metrics

**Phase 1.5 Complete When:**
- [ ] PR #737 merged into main FFNx
- [ ] All known bugs fixed
- [ ] Community testing confirms stability

**Phase 2 Complete When:**
- [ ] Can toggle between all 5 languages
- [ ] No crashes or rendering errors
- [ ] Language preference persists

**Phase 3 Complete When:**
- [ ] Furigana displays above kanji
- [ ] Toggle on/off works
- [ ] No text overflow issues

---
```

---

## Execution Plan

### Immediate (Today - 2025-11-25)

1. ✅ Create this DOCUMENTATION_UPDATE_PLAN.md
2. ⏳ Update IMPLEMENTATION_VERIFICATION_CHECKLIST.md (Section 16)
3. ⏳ Create PR737_INTEGRATION_STRATEGY.md
4. ⏳ Update FEATURE_ROADMAP.md (timelines)

### This Week

5. Update FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md (preamble + notes)
6. Update FFNX_DEVELOPER_GUIDE.md (PR #737 workflow)

### Before Implementation Begins

7. Final review of all updated docs
8. User approval of new strategy
9. Set up PR #737 fork and build environment
10. Begin Phase 1.5 (colored text bug fix)

---

## Review Checklist

Before marking documentation updates complete:

- [ ] All references to "build from scratch" updated to "extend PR #737"
- [ ] All assembly/Hext approaches marked as "alternative" or "historical"
- [ ] All timelines updated to reflect 50-60% time savings
- [ ] PR #737 credited as baseline in all relevant sections
- [ ] Original research preserved for reference (not deleted)
- [ ] Cross-references added between related documents
- [ ] Consistency check: terminology, naming, structure

---

**Next Session:**
Start with updating IMPLEMENTATION_VERIFICATION_CHECKLIST.md Section 16.
