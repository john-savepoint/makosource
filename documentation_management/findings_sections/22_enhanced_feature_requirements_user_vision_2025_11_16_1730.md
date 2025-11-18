# Enhanced Feature Requirements (User Vision - 2025-11-16 17:30)

**Extracted From**: FINDINGS.md
**Section Lines**: 2094-2325
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### Product Vision: "FF7 Japanese Learning Edition"

**Beyond Basic Japanese Support**: The goal is not just to display Japanese text, but to create a **comprehensive Japanese language learning tool** using FF7 as the vehicle.

### Feature 1: Cheat/Booster Functions

**Status**: ✅ ALREADY IMPLEMENTED

User's Japanese eStore version includes:
- **Product**: ファイナルファンタジーVII インターナショナル for PC
- **Code**: J13308W_001_D01
- **Version**: 2.00 (September 19, 2013)

**Built-in Boosters** (keyboard shortcuts):
- 3x Speed Mode (faster gameplay)
- Max Stats (instant character growth)
- God Mode (invincibility)
- No Random Encounters (focus on story)
- Gil/Items (max resources)

**Relevance**: Reduces grinding, allows focus on language learning

---

### Feature 2: English ↔ Japanese Language Toggle

**Priority**: HIGH (Phase 2 after core Japanese support)
**Difficulty**: MEDIUM
**Estimated Effort**: 2-4 weeks

**User Story**: "I want to toggle between English and Japanese text at runtime to compare translations and learn vocabulary in context."

**Technical Implementation Options**:

**Option A: Dual Text File Loading**
```
Directory structure:
data/
├── field_en/flevel.lgp  (English dialogues)
├── field_ja/flevel.lgp  (Japanese dialogues)
└── FFNx switches based on user setting

Runtime:
Press F9 → Toggle language → Reload current scene text
```

**Option B: Tagged Bilingual Text Files**
```
Text format:
{CLOUD}: {EN}Let's go!{/EN}{JA}行こう！{/JA}

FFNx rendering:
if (language == "EN") render EN tags
if (language == "JA") render JA tags
```

**Option C: Configuration-Based Asset Switching**
```toml
# FFNx.toml
language = "JA"  # or "EN"
text_path = "data/lang_ja"  # switches all text assets
font_path = "mods/Fonts/ja"  # loads Japanese fonts
```

**Requirements**:
1. ✅ Japanese font support (jafont_1-6.tex) - current goal
2. ✅ Double-byte encoding (2,000+ kanji) - current goal
3. ⏳ Text file management system (select EN vs JA)
4. ⏳ FFNx configuration extension
5. ⏳ Runtime toggle UI (keyboard shortcut)

**Benefits**:
- Compare translations for learning
- Switch when stuck on difficult kanji
- Study sentence structure differences
- Ideal for JLPT N3-N1 learners

---

### Feature 3: Furigana (Reading Guides Above Kanji)

**Priority**: MEDIUM (Phase 3 capstone feature)
**Difficulty**: HIGH
**Estimated Effort**: 3-6 weeks (inline) / 2-3 months (proper)

**User Story**: "I want furigana displayed above kanji so Japanese learners can read pronunciation while studying the kanji forms."

**Example Display**:
```
Standard (no furigana):
「人として一番大切なものを失ったのだから」

With proper furigana (above):
  ひと    いちばんたいせつ      うしな
「人として一番大切なものを失ったのだから」

With inline furigana (parenthetical):
「人(ひと)として一番(いちばん)大切(たいせつ)なものを失(うしな)ったのだから」
```

**Technical Challenges**:

1. **Text Data Format**
   - Current: `人として一番大切なもの`
   - Required: `人{ひと}として一番{いちばん}大切{たいせつ}なもの`
   - Need markup system associating furigana with kanji

2. **Rendering Architecture**
   - Current: Single line, fixed height
   - Required: Two rendering layers (kanji + furigana above)
   - Dual font sizes (main 24px, furigana 12px)

3. **Window Sizing**
   - Dialog boxes need extra vertical space
   - Line height calculations must account for furigana layer
   - All game windows affected (menus, battles, field)

**Implementation Approaches**:

**Approach A: Inline Furigana (Recommended Start)**
```
Display: 漢字(かんじ)
Pros: Minimal rendering changes, works with current text system
Cons: Uses horizontal space, not traditional appearance
Effort: 3-6 weeks
```

**Approach B: Proper Vertical Furigana (Advanced)**
```
Display:  かんじ
         漢字
Pros: Authentic Japanese typography
Cons: Complete rendering overhaul, complex positioning
Effort: 2-3 months
```

**Approach C: Toggle System (Flexible)**
```
Default: Japanese without furigana (fluent readers)
Toggle ON: Inline furigana for learners
Toggle OFF: Clean kanji-only display
```

**Text File Source for Furigana**:
- Manual annotation (extremely time-consuming)
- MeCab/kuromoji morphological analyzer (auto-generate)
- Existing furigana databases (if available)
- Community contribution

**Benefits**:
- Essential for N4-N2 Japanese learners
- Enables reading without constant dictionary lookup
- Progressive learning (turn off as proficiency increases)
- Could attract significant Japanese learning community interest

---

### Implementation Roadmap

**Phase 1: Core Japanese Support** (CURRENT)
- ✅ Font texture loading (jafont_1-6.tex)
- ⏳ Double-byte encoding (Shift-JIS / 2,000+ kanji)
- ⏳ Character→texture mapping system
- ⏳ FFNx driver modifications
- **Deliverable**: Game displays Japanese text correctly

**Phase 2: Language Toggle** (NEXT)
- ⏳ Dual language text file management
- ⏳ FFNx configuration for language selection
- ⏳ Runtime toggle (F9 key or similar)
- **Deliverable**: Switch EN↔JA during gameplay

**Phase 3: Furigana Support** (ADVANCED)
- ⏳ Text format with furigana markup
- ⏳ Inline furigana rendering (MVP)
- ⏳ Optional: Proper above-kanji rendering
- ⏳ Toggle on/off for user preference
- **Deliverable**: Kanji with reading guides for learners

**Phase 4: Polish & Distribution** (FUTURE)
- 7th Heaven mod packaging
- User documentation / tutorial
- Community feedback integration
- Performance optimization

---

### Target User Personas

**Persona 1: Japanese Language Learner (N4-N2)**
- Knows hiragana/katakana
- Learning kanji (500-1,000 known)
- Needs furigana for unknown kanji
- Uses EN↔JA toggle to check comprehension

**Persona 2: Heritage Speaker / Returning Learner**
- Can read some Japanese but rusty
- Uses furigana occasionally
- Prefers Japanese text but switches to English for complex scenes

**Persona 3: Japanese Native Playing English**
- Wants to see original Japanese dialogue
- No furigana needed
- Language toggle for localization comparison

**Persona 4: FF7 Fan Learning Japanese**
- Knows FF7 story in English
- Uses familiar context to learn Japanese
- Game nostalgia + language study motivation

---

### Unique Value Proposition

**"FF7 Japanese Learning Edition"** would be the **first classic JRPG** to offer:

1. ✅ Full Japanese text with 2,000+ kanji (not hiragana-only)
2. ✅ Built-in cheat modes to reduce grinding
3. ⏳ Runtime EN↔JA language switching
4. ⏳ Furigana reading guides for kanji learners
5. ✅ Beloved story users already know

**Market**: Japanese learners, heritage speakers, localization enthusiasts, FF7 fans

This could become a **viral tool** in Japanese learning communities (JapanesePod101, WaniKani, Tofugu, etc.) and bring new attention to FF7 modding.

---

---

