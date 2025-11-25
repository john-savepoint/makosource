# Multi-Language Implementation Findings

**Document Version:** 1.0
**Created:** 2025-11-24 15:14:19 JST (Monday)
**Project:** FFNx Japanese & Multi-Language Support
**Session ID:** Current session

---

## Executive Summary

After analyzing the 7th Heaven ecosystem, Qhimm forum discussions, and FF7's text architecture, we've identified both critical constraints and expanded opportunities for multi-language support.

**Key Finding:** 7th Heaven's **requirement for FF7_en.exe is actually an advantage** for our implementation strategy, not a limitation.

---

## Critical Discovery: The 7th Heaven / Hext Constraint

### What We Learned from the Forum Discussion

**Source:** Qhimm Forums - "7th Heaven: Allow running FF7_en.exe in other languages" (2024-12-29)

**The Constraint:**
- 7th Heaven has **ALWAYS** required the English executable (FF7_en.exe)
- This is not new to version 4.0
- The reason: **Hext patches are address-specific**
- Different language executables have different memory layouts

**Why This Matters:**

```
Memory Layout Differences (Example):

English (FF7_en.exe):
  draw_text function    = 0x66E272
  font_width_table      = 0x99DDA8

Spanish (FF7_es.exe):
  draw_text function    = 0x67A1B4  ← Different!
  font_width_table      = 0x9A1FC2  ← Different!

French (FF7_fr.exe):
  draw_text function    = 0x669F82  ← Different!
  font_width_table      = 0x99B3D1  ← Different!
```

**Impact on Our Implementation:**
- Our Hext patch (text parser hook for FA-FE codes) only works on FF7_en.exe
- We **cannot** support multiple executables
- We **must** keep FF7_en.exe as the base

**Why This is Actually Good News:**
- ✅ Maintains compatibility with ALL 7th Heaven mods (ESUI, Echo-s, etc.)
- ✅ We only need ONE Hext patch (not 6 different patches for 6 languages)
- ✅ Simpler testing and deployment
- ✅ No version fragmentation

---

## Our Solution: Text Data Routing (Not Executable Switching)

### Architecture

```
Single Executable (FF7_en.exe) - ALWAYS
    ↓
FFNx Driver Routes Text Data Based on Selected Language
    ↓
┌─────────────────────────────────────────────┐
│ Language:  EN     JA     ZH-TW   ES   FR  DE│
├─────────────────────────────────────────────┤
│ KERNEL:    .BIN   _JA    _ZH     _ES  _FR _DE│
│ menu:      _us    _ja    _zh     _es  _fr _de│
│ field:     flevel jfleve jfleve  _es  _fr _de│
│ Font:      ASCII  6-page 6-page  ASCII     │
└─────────────────────────────────────────────┘
    ↓
Text Rendered with Appropriate Font Pages
```

**Key Insight:** We **change the data files**, not the executable.

---

## Text Storage Locations in FF7

### Where Translated Strings Are Stored

| File | Content | Encoding | Size |
|------|---------|----------|------|
| **KERNEL.BIN** | Item names, spell names, ability names, status effects | FF7 custom | ~200KB |
| **WINDOW.BIN** | Menu text, system messages, button prompts | FF7 custom | ~50KB |
| **SCENE.BIN** | Enemy names, AI scripts | FF7 custom | ~1.5MB |
| **flevel.lgp** | Field dialogue (per-map .DAT files) | FF7 custom | ~15MB |
| **world_us.lgp** | World map text, chocobo names | FF7 custom | ~2MB |
| **menu_us.lgp** | Menu graphics with embedded text | TEX + strings | ~5MB |

### Language Variants

**English (Base):**
```
data/kernel/KERNEL.BIN
data/menu/menu_us.lgp
data/field/flevel.lgp
```

**Japanese:**
```
data/lang-ja/kernel/KERNEL.BIN  (FA-FE encoded)
data/lang-ja/menu/menu_ja.lgp   (contains jafont_*.tex)
data/lang-ja/field/jfleve.lgp   (FA-FE encoded, note the typo!)
```

**Spanish (Proposed):**
```
data/lang-es/kernel/KERNEL_ES.BIN
data/lang-es/menu/menu_es.lgp
data/lang-es/field/flevel_es.lgp
```

### File Redirection Implementation

```cpp
// src/redirect.cpp

int attempt_redirection(const char* input_path, char* output_path) {

    // Check current language setting
    string lang = GetCurrentLanguage();  // "en", "ja", "zh-tw", "es", etc.

    if (lang == "en") {
        // No redirection needed
        strcpy(output_path, input_path);
        return 0;
    }

    // KERNEL.BIN redirection
    if (strstr(input_path, "KERNEL.BIN")) {
        sprintf(output_path, "data/lang-%s/kernel/KERNEL.BIN", lang.c_str());
        if (fileExists(output_path)) return 0;
    }

    // menu LGP redirection
    if (strstr(input_path, "menu_us.lgp")) {
        sprintf(output_path, "data/lang-%s/menu/menu_%s.lgp",
                lang.c_str(), lang.c_str());
        if (fileExists(output_path)) return 0;
    }

    // field LGP redirection (handle jfleve typo for Japanese)
    if (strstr(input_path, "flevel.lgp")) {
        if (lang == "ja") {
            sprintf(output_path, "data/lang-ja/field/jfleve.lgp");
        } else {
            sprintf(output_path, "data/lang-%s/field/flevel_%s.lgp",
                    lang.c_str(), lang.c_str());
        }
        if (fileExists(output_path)) return 0;
    }

    // Fallback to original path
    strcpy(output_path, input_path);
    return 0;
}
```

---

## Font Page Expansion: Beyond 6 Pages

### Can We Support More Languages?

**YES - We Have Headroom**

**Current Plan:**
- FA, FB, FC, FD, FE = 5 page markers
- Plus base page (no marker) = **6 total pages**

**Available Expansion:**
- **F0-F4** (5 more markers) = 5 additional pages
- **EB-EF** (5 more markers) = 5 additional pages
- **Theoretical Maximum:** ~15 pages before conflicts

### Allocation Strategy for Japanese + Chinese

```
Control Codes and Page Assignments:

Page 0:  (no marker)     - Shared ASCII/Latin/Hiragana/Katakana
Page 1:  0xFA            - Japanese Kanji Set A
Page 2:  0xFB            - Japanese Kanji Set B
Page 3:  0xFC            - Japanese Kanji Set C
Page 4:  0xFD            - Japanese Kanji Set D
Page 5:  0xFE            - Japanese Kanji Set E

Page 6:  0xF0            - Chinese Traditional Set A
Page 7:  0xF1            - Chinese Traditional Set B
Page 8:  0xF2            - Chinese Traditional Set C
Page 9:  0xF3            - Chinese Traditional Set D
Page 10: 0xF4            - Chinese Traditional Set E

Page 11-14: 0xEB-0xEE    - Reserved (Korean? Cyrillic? Future)
```

**Character Coverage:**
- Japanese: ~2,136 characters (JIS Level 1 + Level 2)
- Chinese Traditional: ~5,000+ characters (Big5 common set)
- Total: ~7,000+ unique glyphs across both languages

### Implementation Change

**Texture Allocation (src/common.cpp):**

```cpp
// Expand from 6 to 15 pages
if (is_font_texture && RequiresCJKPages(font_language)) {
    num_textures = 15;  // Maximum possible pages
    ffnx_info("Allocating %d texture pages for CJK language support.\n", num_textures);
}
```

**Asset Loading (src/saveload.cpp):**

```cpp
if (font_language == "ja") {
    // Load jafont_1.png through jafont_6.png (pages 0-5)
    for (int i = 0; i < 6; i++) {
        sprintf(filename, "jafont_%d.png", i + 1);
        LoadFontTexture(filename, i);
    }
}

if (font_language == "zh-tw") {
    // Load shared base page
    LoadFontTexture("jafont_1.png", 0);  // ASCII/Latin/Common

    // Load Chinese pages
    for (int i = 0; i < 5; i++) {
        sprintf(filename, "zhfont_%d.png", i + 1);
        LoadFontTexture(filename, 6 + i);  // Pages 6-10
    }
}

if (font_language == "multi") {
    // Load both Japanese AND Chinese (for hot-switching)
    // Pages 0-5: Japanese
    // Pages 6-10: Chinese
    for (int i = 0; i < 6; i++) {
        sprintf(filename, "jafont_%d.png", i + 1);
        LoadFontTexture(filename, i);
    }
    for (int i = 0; i < 5; i++) {
        sprintf(filename, "zhfont_%d.png", i + 1);
        LoadFontTexture(filename, 6 + i);
    }
}
```

**Assembly Hook Extension (misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt):**

```assembly
; Check for Japanese pages (0xFA-0xFE)
CMP AL, 0xFA
JB CheckChinese
CMP AL, 0xFE
JA CheckChinese
; Japanese logic: pages 1-5
SUB AL, 0xFA
INC AL
MOV [g_currentFontPage], AL
JMP LoadNextCharacter

CheckChinese:
; Check for Chinese pages (0xF0-0xF4)
CMP AL, 0xF0
JB NormalCharacter
CMP AL, 0xF4
JA NormalCharacter
; Chinese logic: pages 6-10
SUB AL, 0xF0
ADD AL, 6
MOV [g_currentFontPage], AL
JMP LoadNextCharacter

NormalCharacter:
; Standard single-byte character (page 0)
MOV [g_currentFontPage], 0
; ... continue with normal rendering
```

---

## Runtime Language Switching

### The Hot-Swap Feature

**User Experience:**
```
Playing in English → Press F12 → Switch to Japanese → Continue playing
                   ↓
         All dialogue updates
         Font changes
         Menu text changes
         No restart needed
```

**Technical Flow:**

```cpp
enum Language {
    LANG_EN = 0,      // English (base)
    LANG_JA = 1,      // Japanese
    LANG_ZH_TW = 2,   // Chinese Traditional
    LANG_ES = 3,      // Spanish
    LANG_FR = 4,      // French
    LANG_DE = 5       // German
};

Language current_language = LANG_EN;

void CycleLanguage() {
    // Move to next language in list
    current_language = (Language)((current_language + 1) % 6);

    // Update font system
    UpdateFontLanguage(current_language);

    // Update file redirection
    UpdateTextLanguage(current_language);

    // Reload current screen
    RefreshCurrentDialogue();

    // Show notification
    ShowToast("Language: %s", GetLanguageName(current_language));
}

void UpdateFontLanguage(Language lang) {
    if (lang == LANG_JA || lang == LANG_ZH_TW) {
        // Use CJK width table (16px fixed width)
        PatchFontWidthsForCJK();

        // Set font_language for texture binding
        if (lang == LANG_JA) {
            font_language = "ja";
        } else {
            font_language = "zh-tw";
        }
    } else {
        // Use Latin width table (variable width)
        RestoreOriginalWidthTable();
        font_language = "en";
    }
}

void RefreshCurrentDialogue() {
    // Get current field map
    char* current_field = GetCurrentFieldID();

    // Get current dialogue index
    uint16_t current_string = GetCurrentDialogueIndex();

    // Reload dialogue from new language file
    ReloadFieldDialogue(current_field);

    // Re-render current dialogue box
    DisplayDialogue(current_string);
}
```

### Configuration

```toml
# FFNx.toml

[multi_language]
# Base language on startup
default_language = "en"

# Available languages (shown in cycle order)
available_languages = ["en", "ja", "zh-tw", "es", "fr", "de"]

# Hotkey for cycling languages (default: F12)
language_cycle_key = "F12"

# Show language name toast when switching
show_language_toast = true

# Persist language choice across sessions
remember_language = true
```

---

## Language Support Matrix

### What Each Language Needs

| Language | Font Pages | Text Files | Encoding | Complexity |
|----------|------------|------------|----------|------------|
| **English** | 1 (ASCII) | Base files | Single-byte | ✅ Already done |
| **Spanish** | 1 (ASCII + accents) | KERNEL_ES, etc. | Single-byte | 🟡 Easy (text only) |
| **French** | 1 (ASCII + accents) | KERNEL_FR, etc. | Single-byte | 🟡 Easy (text only) |
| **German** | 1 (ASCII + umlauts) | KERNEL_DE, etc. | Single-byte | 🟡 Easy (text only) |
| **Japanese** | 6 (Kana + Kanji) | KERNEL_JA, etc. | FA-FE multi-byte | 🔴 Hard (our focus) |
| **Chinese Trad** | 6 (Hanzi) | KERNEL_ZH, etc. | F0-F4 multi-byte | 🔴 Hard (after Japanese) |
| **Korean** | 5-6 (Hangul) | KERNEL_KO, etc. | EB-EF multi-byte | 🔴 Hard (future) |

### Why Spanish/French/German Are Easy

**No new font pages needed!**

Extended Latin characters can fit in the existing base page:

```
Page 0 Extended Mapping:
0x00-0x7F:  Standard ASCII
0x80-0x9F:  Accented characters (á, é, í, ó, ú, ñ, ü, à, è, etc.)
0xA0-0xE6:  Japanese Hiragana/Katakana (for Japanese mode)
0xE7-0xEF:  Reserved
0xF0-0xFE:  Page markers
```

**Implementation for Romance Languages:**

1. **Text extraction:** Export official Spanish/French/German translations
2. **Re-encoding:** Convert to FF7 single-byte format (already standard)
3. **File creation:** Create KERNEL_ES.BIN, menu_es.lgp, etc.
4. **Packaging:** Bundle as .iro mod for 7th Heaven
5. **Testing:** Verify with FF7_en.exe

**Estimated effort:** 20-40 hours per language (mostly extraction/QA)

---

## Translation Workflow for New Languages

### For Languages WITH Official Versions

**Example: Spanish, French, German**

**Step 1: Extract Original Text**

```bash
# Use existing tools to extract from official releases
ulgp -x data/lang-es/kernel/KERNEL.BIN
# Output: item_names_es.txt, spell_names_es.txt, etc.

touphscript --export field/flevel_es.lgp
# Output: dialogue_es.csv
```

**Step 2: Re-encode for FF7_en.exe Compatibility**

```python
# encode_text.py
import csv

def encode_spanish_text(text):
    """Convert Spanish text to FF7 single-byte encoding"""
    result = []
    for char in text:
        if char in STANDARD_ASCII:
            result.append(ord(char))
        elif char == 'á':
            result.append(0x80)  # Custom mapping
        elif char == 'é':
            result.append(0x81)
        elif char == 'ñ':
            result.append(0x85)
        # etc.
    return bytes(result)
```

**Step 3: Create Language-Specific LGP Archives**

```bash
# Pack into LGP format
lgp_pack kernel_es.lgp kernel/*.BIN
lgp_pack menu_es.lgp menu/*.TEX
lgp_pack flevel_es.lgp field/*.DAT
```

**Step 4: Package for 7th Heaven**

```bash
# Create .iro mod
7z a -tzip Spanish_Translation.iro lang-es/
ren Spanish_Translation.zip Spanish_Translation.iro
```

### For Languages WITHOUT Official Versions

**Example: Chinese Traditional**

**Step 1: Extract English Base**

```bash
ulgp -x KERNEL.BIN
touphscript --export flevel.lgp
# Output: en_dialogue.csv
```

**Step 2: Translate**

```csv
# translation_zh_tw.csv
field_id,string_id,en,zh_tw,zh_tw_encoded
md1_1,0,"Let's get outta here!","我們離開這裡吧!","F0 12 F0 13 F0 14 F0 15 F0 16 F0 17 F0 18 00"
md1_1,1,"This isn't normal!","這不正常!","F0 1A F0 1B F0 1C F0 1D 00"
```

**Step 3: Encode with F0-F4 Page Markers**

```python
def encode_chinese_text(text):
    """Convert Chinese to FF7 F0-F4 multi-byte encoding"""
    result = []
    for char in text:
        page, index = lookup_chinese_char(char)  # From zhfont mapping CSV

        if page == 0:
            result.append(index)  # Single byte (ASCII/Latin)
        else:
            # Two-byte encoding
            marker = 0xF0 + (page - 6)  # F0 for page 6, F1 for page 7, etc.
            result.append(marker)
            result.append(index)

    return bytes(result)
```

**Step 4: Create Font Textures**

```
zhfont_1.png - Most common characters (Page 6)
zhfont_2.png - Secondary common (Page 7)
zhfont_3.png - Tertiary (Page 8)
zhfont_4.png - Rare (Page 9)
zhfont_5.png - Very rare + proper nouns (Page 10)
```

---

## Known Issues & Constraints

### From Forum Discussion

**Issue 1: Hext Dependency**

**Problem:** Many popular 7th Heaven mods use Hext patches (ESUI, Echo-s, Finishing Touch, etc.)

**Impact:** These mods are address-specific to FF7_en.exe

**Our Solution:** ✅ Use FF7_en.exe exclusively - no conflict

**Issue 2: Texture Text Overlays**

**Problem:** Some mods have English text baked into textures (minigame titles, etc.)

**Example from forum:**
```
Chocobo Racing minigame title texture:
- English: "CHOCOBO RACING" (correct)
- Spanish: "CHOCOBO RACING" (should be "CARRERAS DE CHOCOBO")
```

**Our Solution:**
- Create language-specific texture packs
- Use FFNx's texture override system
- Package as .iro: `Textures_ES.iro`, `Textures_JA.iro`, etc.

**Issue 3: Menu Graphics with Embedded Text**

**Problem:** FF7's menus use textures with baked-in text

**Files affected:**
- `menu_us.lgp/btl_win_c_h.tex` (battle menu)
- `menu_us.lgp/buster_e.tex` (limit break names)
- etc.

**Our Solution:**
- Extract menu textures per language
- Re-create with localized text
- Bundle in language-specific menu_*.lgp archives

---

## Implementation Priority

### Phase 1: Japanese Foundation (Current Focus)

**Goal:** Get Japanese working perfectly with FF7_en.exe

**Deliverables:**
- ✅ 6-page font system (FA-FE encoding)
- ✅ Width table patching
- ✅ Hext parser hook
- ✅ Asset loading pipeline
- ✅ File redirection (jfleve.lgp handling)

**Effort:** 200-300 hours (as documented in Bible)

### Phase 2: Language Switcher

**Goal:** Runtime language cycling (F12 hotkey)

**Deliverables:**
- Language menu UI
- Hotkey handler
- Text reload on switch
- Font system toggle (CJK ↔ Latin widths)
- Config persistence

**Effort:** 40-60 hours

### Phase 3: Spanish/French/German

**Goal:** Add Romance language support (easy wins)

**Deliverables:**
- Extract official translations
- Re-encode for FF7_en.exe
- Create KERNEL_ES/FR/DE.BIN
- Package as .iro mods
- Localized texture packs

**Effort:** 20-40 hours per language

### Phase 4: Chinese Traditional

**Goal:** Second CJK language using F0-F4 pages

**Deliverables:**
- 5-page Chinese font textures (zhfont_1-5.png)
- Character mapping CSV (Unicode → F0-F4 + index)
- Translation workflow (English → Chinese)
- Assembly hook extension (F0-F4 detection)

**Effort:** 100-150 hours

### Phase 5: Community Translation Platform (Future)

**Goal:** Crowdsourced translation improvement

**Deliverables:**
- In-game translation submission UI
- Web-based voting/review system
- Moderator approval workflow
- Auto-update system via 7th Heaven catalog

**Effort:** 50-80 hours

---

## Key Decisions Made

### Decision 1: Single Executable Strategy

**Decision:** Always use FF7_en.exe, route text data by language

**Rationale:**
- ✅ 7th Heaven requirement
- ✅ Hext patch compatibility
- ✅ Simpler maintenance (1 patch, not 6)
- ✅ Community mod ecosystem compatibility

**Trade-off:** Cannot use official non-English executables (acceptable)

### Decision 2: Expanded Page Allocation

**Decision:** Support up to 15 font pages (F0-FE range)

**Rationale:**
- ✅ Enables Japanese (6 pages) + Chinese (5 pages) + future
- ✅ No performance penalty (texture memory is cheap)
- ✅ Future-proof for Korean, Arabic, Cyrillic, etc.

**Trade-off:** Slightly more complex assembly hook (acceptable)

### Decision 3: File Redirection over In-Memory Patching

**Decision:** Use separate KERNEL_*.BIN files, not in-memory string replacement

**Rationale:**
- ✅ Simpler to maintain (files, not code)
- ✅ Easier for translators (edit files, not hex)
- ✅ 7th Heaven .iro packaging works well
- ✅ No risk of memory corruption

**Trade-off:** Larger disk footprint (acceptable - ~50MB per language)

### Decision 4: Hot-Swapping Support

**Decision:** Enable runtime language switching without restart

**Rationale:**
- ✅ Amazing UX for language learners
- ✅ Easy A/B testing of translations
- ✅ Demo/marketing value
- ✅ Technically feasible (reload text, swap font)

**Trade-off:** Slight complexity in cache management (acceptable)

---

## Open Questions

### Question 1: Default Language Behavior

**Question:** When a user first installs the mod, what language should be default?

**Options:**
- A) English (safest, most compatible)
- B) System language (Windows locale detection)
- C) Ask on first launch (modal dialog)

**Recommendation:** **Option A** (English default) with easy switching

**Rationale:** Most users installing 7th Heaven mods are likely English-speaking or comfortable with English UI. System locale can be misleading (e.g., Japanese Windows but user prefers English).

### Question 2: Partial Translation Fallback

**Question:** What happens if Chinese translation is incomplete? Show English for missing strings?

**Options:**
- A) Show English text with (EN) prefix
- B) Show placeholder: `[MISSING: md1_1:0x42]`
- C) Show romanized key: `reactor1_entrance_cloud_01`
- D) Fail gracefully with error message

**Recommendation:** **Option A** (English fallback with indicator)

**Rationale:** Allows partial translations to be shipped. Users can still play and contribute missing translations.

### Question 3: Font Page Sharing

**Question:** Can Chinese and Japanese share Page 0 (base ASCII/Latin)?

**Current Plan:** Yes - both use `jafont_1.png` for Page 0

**Risk:** If Chinese needs different punctuation or symbols, conflict occurs

**Mitigation:** Reserve 0xE7-0xEF for language-specific symbols on Page 0

### Question 4: Translation Validation

**Question:** How do we validate that Chinese text encodes correctly (no missing chars)?

**Options:**
- A) Pre-flight check during .iro build
- B) Runtime check when loading text files
- C) Both

**Recommendation:** **Option C** (both build-time and runtime)

**Implementation:**
```python
# Build-time check (before packaging .iro)
def validate_translation_file(text_file, char_map):
    errors = []
    for line in text_file:
        for char in line.text:
            if not char_in_mapping(char, char_map):
                errors.append(f"Missing: '{char}' (U+{ord(char):04X}) in {line.id}")
    return errors
```

---

## Next Steps

### Immediate (This Week)

1. ✅ **Complete Japanese base implementation** (continue Bible execution)
2. ✅ **Test with FF7_en.exe + Japanese text**
3. ✅ **Verify 7th Heaven compatibility**

### Short-Term (This Month)

1. **Implement language switcher** (F12 hotkey)
2. **Create Spanish translation test** (proof-of-concept for Romance languages)
3. **Document translation workflow** (for community contributors)

### Mid-Term (Next 3 Months)

1. **Add Chinese Traditional support** (F0-F4 pages)
2. **Create translation tools** (encode/decode scripts)
3. **Package as 7th Heaven mods** (Japanese.iro, Spanish.iro, etc.)

### Long-Term (6+ Months)

1. **Community translation platform** (web app + in-game submission)
2. **Additional languages** (Korean, Portuguese, etc.)
3. **Automated testing** (ensure all languages work with major mods)

---

## Conclusion

**The multi-language system is not only feasible, but architecturally elegant:**

- ✅ Works within 7th Heaven constraints
- ✅ Compatible with existing mod ecosystem
- ✅ Expandable to 10+ languages
- ✅ Enables runtime language switching
- ✅ Foundation for community crowdsourcing

**The key insight:** By using FF7_en.exe with routed text data, we get the best of both worlds - Hext compatibility AND multi-language support.

**Status:** Ready to proceed with implementation following the roadmap in `FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md`.

---

**Document End**
