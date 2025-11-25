# FFNx Japanese Implementation - Architecture Clarification

**Created:** 2025-11-24 13:25:45 JST (Monday)
**Purpose:** Clarify the actual implementation approach vs common misconceptions
**Context:** Response to questions about how FFNx handles multi-language support

---

## Table of Contents

1. [What We're Actually Doing](#what-were-actually-doing)
2. [How Other Languages Work](#how-other-languages-work)
3. [7th Heaven + FFNx Language Flow](#7th-heaven--ffnx-language-flow)
4. [Data Flow Breakdown](#data-flow-breakdown)
5. [Why ff7_ja.exe Exists](#why-ff7_jaexe-exists)
6. [Your Learning Tool Use Case](#your-learning-tool-use-case)
7. [Critical Insights](#critical-insights)
8. [Summary Table](#summary-table)

---

## What We're Actually Doing

### Common Misconception

❌ **INCORRECT:** "We're extracting Japanese from ff7_ja.exe and putting it in ff7_en.exe"

### Actual Implementation

✅ **CORRECT:** "We're extending FFNx to handle Japanese fonts with EITHER executable"

### The Real Architecture

**FFNx (our modified driver) works with BOTH executables:**

#### Scenario 1: English Executable with Japanese Mod

```text
ff7_en.exe (English)
├─ Single-byte text system
├─ Loads USFONT.TEX (1 page)
└─ Expects data/ paths

With FFNx Japanese Mode:
├─ FFNx intercepts texture load
├─ Forces 6 texture pages instead of 1
├─ Loads jafont_*.png (from mods/)
├─ Assembly hook handles FA-FE codes
└─ Still runs ff7_en.exe, just modded
```

#### Scenario 2: Japanese Executable (Optional)

```text
ff7_ja.exe (Japanese - optional)
├─ Same single-byte + FA-FE system
├─ Loads jafont_*.tex (6 pages)
└─ Expects data/lang-ja/ paths

With FFNx:
├─ FFNx detects ff7_ja.exe
├─ Auto-enables Japanese mode
├─ Returns correct lang-ja/ paths
└─ Everything just works
```

### Key Point: You Can Use EITHER Executable

**Option 1: ff7_en.exe + Japanese text mod (via 7th Heaven)**

- Replace English dialogue with Japanese dialogue
- FFNx loads Japanese fonts
- Most common approach (doesn't require ff7_ja.exe)

**Option 2: ff7_ja.exe (if you have it)**

- Already has Japanese dialogue built-in
- FFNx just needs to provide correct paths
- Rare (eStore-only release)

---

## How Other Languages Work

### Non-Japanese Languages (French, German, Spanish)

**These are trivial to implement:**

```text
ff7_fr.exe, ff7_de.exe, ff7_es.exe:
├─ SAME engine as English (single-byte)
├─ SAME texture system (USFONT variant)
├─ SAME directory structure (data/)
└─ ONLY difference: translated text strings
```

**How FFNx + 7th Heaven handle this:**

```text
├─ Load French translation mod (dialogue text)
├─ Load French font texture (accented characters: é, ñ, ü)
└─ Everything else identical to English
```

**Why these are simple:**

- French/German/Spanish fit in 256 characters (single-byte)
- Just need a different font texture with accents
- No driver changes needed
- No multi-page system needed

### Japanese is Special

**Why Japanese requires our implementation:**

```text
ff7_ja.exe:
├─ DIFFERENT driver (AF3DN.P with extensions)
├─ DIFFERENT texture system (6 pages)
├─ DIFFERENT directory structure (lang-ja/)
└─ DIFFERENT encoding (FA-FE opcodes)

Why it's hard:
├─ Can't fit 2,300 characters in 256 slots
├─ Needs multi-texture page switching
├─ Requires driver-level changes
└─ This is why we needed all that research!
```

---

## 7th Heaven + FFNx Language Flow

### For French (Simple)

```text
1. User installs "French Translation" mod in 7th Heaven

2. 7th Heaven VFS intercepts file requests

3. When ff7_en.exe asks for "dialogue string 123"
   → 7th Heaven returns French version

4. When ff7_en.exe asks for USFONT.TEX
   → 7th Heaven returns French font (with é, à, ç)

5. Done! No driver changes needed.
```

### For Japanese (Complex - Our Implementation)

```text
1. User installs "Japanese Font Support" mod (our work)
   → Adds jafont_1.png through jafont_6.png

2. User sets font_language = "ja" in FFNx.toml

3. User installs "Japanese Translation" mod via 7th Heaven
   → Contains dialogue encoded with FA-FE opcodes

4. When ff7_en.exe asks for USFONT.TEX:
   → FFNx intercepts
   → Loads all 6 jafont_*.png instead
   → Allocates 6 texture slots

5. When ff7_en.exe renders text with FA-FE bytes:
   → Assembly hook detects page switch codes
   → FFNx binds correct texture page
   → Japanese renders correctly

6. When ff7_en.exe asks for "dialogue string 123":
   → 7th Heaven returns Japanese version (with FA-FE codes)
```

---

## Data Flow Breakdown

### What Comes from Where

| Component | English (Vanilla) | French Mod | Japanese Mod (Our Work) |
|-----------|-------------------|------------|-------------------------|
| **Executable** | ff7_en.exe | ff7_en.exe (same) | ff7_en.exe (same!) |
| **Driver** | FFNx | FFNx | **FFNx (modified by us)** |
| **Font Texture** | USFONT.TEX (1 page) | USFONT_FR.TEX (1 page) | **jafont_*.png (6 pages)** |
| **Dialogue Text** | English strings | French strings (7H mod) | Japanese strings (7H mod) |
| **Text Encoding** | Single-byte (0x00-0xFF) | Single-byte | **FA-FE system** |
| **Directory Structure** | data/ | data/ | data/ (same!) |

### The Magic: Driver-Level Interpretation

**We're NOT changing the executable. We're changing how FFNx interprets the text data.**

```text
ff7_en.exe sends: "Render this byte stream: FA 12 FB 34 FC 56"
                  ↓
Old FFNx says:    "I don't know what FA means, render garbage"
                  ↓
Our FFNx says:    "FA = switch to texture page 1
                   FB = switch to texture page 2
                   FC = switch to texture page 3
                   Render: 必殺技" ✓
```

---

## Why ff7_ja.exe Exists

### What Square Enix Did (2013 eStore)

```text
ff7_ja.exe + AF3DN.P (proprietary driver):
├─ Hardcoded to load from lang-ja/
├─ Hardcoded to use 6 font textures
├─ Includes Japanese dialogue in KERNEL.BIN
└─ Uses FA-FE encoding
```

**Why they made a separate executable:**

- Easy for them (just compile with different paths)
- No need to maintain multi-language switching
- eStore was Japan-only market

### What We're Doing (Open Source)

```text
ff7_en.exe + FFNx (modified, open source):
├─ Runtime language switching (en/ja via config)
├─ Works with ANY executable
├─ Dialogue comes from 7th Heaven mods
└─ Future-proof (can add more languages)
```

**Advantages:**

- Don't need rare ff7_ja.exe
- Users can switch languages without reinstalling
- Works with Steam/GOG English version
- Community can create Japanese translation mods

---

## Your Learning Tool Use Case

### What You Actually Need

**Setup:**

1. `ff7_en.exe` (your existing Steam/GOG install)
2. FFNx (with our Japanese font patches)
3. Bilingual dialogue mod (shows both languages)

**Runtime:**

```text
├─ FFNx handles font rendering (our code)
├─ 7th Heaven serves dialogue (community translation)
├─ Hotkey switches between languages (future feature)
└─ All in ONE executable (ff7_en.exe)
```

**You never need ff7_ja.exe** unless you want the original Japanese release's exact dialogue.

---

## Critical Insights

### What We Documented

**We're teaching ff7_en.exe to speak Japanese** by:

1. **Driver Extension (FFNx)** - Handles multi-page fonts
2. **Text Encoding** - Interprets FA-FE codes
3. **Asset Loading** - Loads 6 textures instead of 1
4. **Geometry Patching** - Renders wide characters correctly

### What We're NOT Doing

- ❌ Replacing ff7_en.exe with ff7_ja.exe
- ❌ Extracting code from ff7_ja.exe
- ❌ Changing the game's text system
- ✅ Extending the **driver** (FFNx) to handle Japanese fonts

### The Architecture We Reverse-Engineered

**From ff7_ja.exe + AF3DN.P, we learned:**

- How the FA-FE encoding system works
- That 6 texture pages are needed
- The directory structure expectations (lang-ja/)
- The character width requirements (16px vs 8-12px)

**We then reimplemented this in FFNx:**

- Not by copying code (legal/licensing issues)
- But by understanding the **architecture** and rebuilding it
- Clean-room implementation based on analysis

---

## Summary Table

### Misconceptions vs Reality

| Common Misconception | Reality |
|---------------------|---------|
| "Extract Japanese from ff7_ja.exe" | ❌ We reverse-engineered the **architecture**, not extracted code |
| "Make it work in ff7_en.exe" | ✅ YES - we extend FFNx to handle Japanese fonts |
| "French = just load French exe" | ❌ French uses same exe, just different text/font via mods |
| "Japanese needs different driver" | ✅ YES - requires multi-page fonts (our contribution) |
| "Need ff7_ja.exe to play in Japanese" | ❌ Optional - FFNx works with ff7_en.exe + mods |

### Language Support Comparison

| Feature | French/German/Spanish | Japanese |
|---------|----------------------|----------|
| **Executable** | Same as English | Same as English (or ff7_ja.exe optional) |
| **Character Set** | 256 chars (single-byte) | ~2,300 chars (multi-byte) |
| **Font Textures** | 1 page (USFONT variant) | 6 pages (jafont_1-6) |
| **Encoding** | Single-byte (0x00-0xFF) | FA-FE page markers |
| **Driver Changes** | None needed | **Requires our FFNx modifications** |
| **Implementation** | Simple texture swap | Complex multi-page system |
| **Directory Structure** | data/ (same) | data/ OR data/lang-ja/ (optional) |

### Bottom Line

**The Key Distinction:**

- **French/German/Spanish**: Just swap text + font texture (simple mods)
- **Japanese**: Requires **driver-level changes** (our implementation)
- **ff7_ja.exe**: Optional reference, we don't need it because we **built the system into FFNx**

**What We Built:**

A **driver extension** that enables ff7_en.exe (or any FF7 executable) to render Japanese text using the same multi-page font system that Square Enix used in their proprietary AF3DN.P driver, but implemented in open-source FFNx.

---

## Architectural Diagram

```text
┌─────────────────────────────────────────────────────────────┐
│                     User's Perspective                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  "I want to play FF7 in Japanese to learn the language"    │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │  What They Need         │
        ├─────────────────────────┤
        │  1. ff7_en.exe (Steam)  │
        │  2. FFNx (our patches)  │
        │  3. Japanese text mod   │
        └────────────┬────────────┘
                     │
        ┌────────────┴─────────────────────────────────────┐
        │          Technical Architecture                   │
        ├──────────────────────────────────────────────────┤
        │                                                   │
        │  ┌─────────────┐    ┌──────────────┐            │
        │  │ ff7_en.exe  │───>│ FFNx Driver  │            │
        │  │ (unmodified)│    │ (our mods)   │            │
        │  └─────────────┘    └──────┬───────┘            │
        │                             │                     │
        │              ┌──────────────┼──────────────┐     │
        │              │              │              │      │
        │         ┌────▼───┐    ┌────▼────┐   ┌────▼───┐ │
        │         │ Config │    │  Font   │   │  Text  │ │
        │         │  .toml │    │  System │   │ Parser │ │
        │         └────────┘    └────┬────┘   └────┬───┘ │
        │                             │              │      │
        │         font_language="ja"  │              │      │
        │                             │              │      │
        │              ┌──────────────▼──────────────▼───┐ │
        │              │     6-Page Font System          │ │
        │              │  jafont_1.png (Hiragana)        │ │
        │              │  jafont_2.png (Kanji A)         │ │
        │              │  jafont_3.png (Kanji B)         │ │
        │              │  jafont_4.png (Kanji C)         │ │
        │              │  jafont_5.png (Kanji D)         │ │
        │              │  jafont_6.png (Kanji E)         │ │
        │              └─────────────────────────────────┘ │
        │                                                   │
        │  ┌──────────────────────────────────────────┐   │
        │  │      7th Heaven (Text Provider)           │   │
        │  │  Serves Japanese dialogue with FA-FE      │   │
        │  │  encoding to ff7_en.exe                   │   │
        │  └──────────────────────────────────────────┘   │
        │                                                   │
        └───────────────────────────────────────────────────┘
```

---

## Final Clarification

### What Each Component Does

| Component | Role | Who Provides |
|-----------|------|--------------|
| **ff7_en.exe** | Game engine (unmodified) | Square Enix (Steam/GOG) |
| **FFNx.dll** | Graphics driver (our mods) | Us (this implementation) |
| **jafont_*.png** | Font textures (6 pages) | Us (extracted from ff7_ja assets) |
| **Japanese dialogue** | Text strings with FA-FE encoding | Community translation mods |
| **7th Heaven** | Mod manager / VFS | Community (existing) |
| **FFNx.toml** | Configuration | User (set font_language="ja") |

### What Makes This Work

**The magic is in FFNx (our modifications):**

1. **Detects** when font_language="ja"
2. **Allocates** 6 texture slots instead of 1
3. **Loads** all 6 jafont_*.png files
4. **Interprets** FA-FE codes via Assembly hook
5. **Renders** Japanese correctly via geometry patches

**Everything else stays the same:**

- Same ff7_en.exe executable
- Same 7th Heaven mod system
- Same game logic
- Just enhanced **driver** capabilities

---

**Document End**

*This clarification explains the actual architecture of the FFNx Japanese implementation.*
*For technical implementation details, see: FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md*
