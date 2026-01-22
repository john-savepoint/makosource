# FFNx Japanese Implementation Master Bible

**Document Version:** 4.2 (Edge Cases & Control Codes Update)
**Created:** 2025-11-24 10:42:14 JST (Monday)
**Last Major Update:** 2025-11-25 14:55 JST (Tuesday)
**Project Codename:** "One-7 Language Learner Edition"
**Target Platform:** FFNx Driver for Final Fantasy VII (1998/2013 PC)
**Target Architecture:** C++ / BGFX (PR #737 baseline, extend for multi-language)
**Reference Hardware:** Square Enix Japanese eStore Release (ff7_ja.exe + AF3DN.P)

---

## 🔴 CRITICAL UPDATE - 2025-11-25 (PR #737 Discovery)

**Major Strategic Pivot:** A community member (CosmosXIII) has already implemented 95% of the Japanese rendering system described in this document via [FFNx PR #737](https://github.com/julianxhokaxhiu/FFNx/pull/737) (opened September 2024).

### What PR #737 Provides

**✅ Already Implemented (Production-Quality Code):**
- FA-FE encoding system (identical to our spec)
- Multi-page texture loading (all 6 jafont textures)
- Character width tables (1,536 values hardcoded in C++)
- Function pointer hooking (C++, no assembly required)
- Dynamic texture switching mid-frame
- Text box auto-resizing for Japanese characters
- Auto-detection of Japanese game version

**❌ Known Issues (Require Fixing):**
- Colored text rendering broken (14 months unresolved)
- Character name input screen corrupted
- Cursor alignment offset in menus

**⚠️ Scope Limitation:**
PR #737 enables Japanese rendering in the **Japanese game version only**. It does NOT enable:
- Japanese text in English version
- Runtime language switching
- Translation file loading
- Multi-language support (FR/DE/ES)

### Our New Mission

**Phase 1.5 (NEW - 3-4 weeks):**
Fix PR #737's bugs → help get it merged into FFNx

**Phase 2 (2-3 weeks):**
Extend PR #737 to support multi-language (EN/JA/FR/DE/ES in English version)

**Phase 3 (3-6 weeks):**
Add furigana support on top of PR #737's foundation

**Phase 4+ (as planned):**
Translation tools, crowdsourcing platform, 7th Heaven integration

### Why This Document Still Matters

**This Master Bible remains ESSENTIAL because:**

1. ✅ **Our research VALIDATED PR #737's approach**
   - We independently arrived at the same FA-FE encoding solution
   - Our architectural analysis confirms it's the correct approach
   - Our character mapping (1,331 glyphs) enables translation tools PR #737 can't do

2. ✅ **We're solving a DIFFERENT problem**
   - PR #737: Japanese rendering in Japanese version
   - Our goal: Multi-language learning edition in English version
   - We need text encoder, language switcher, translation loader

3. ✅ **This spec identifies improvements**
   - Configuration-based width tables (vs hardcoded)
   - GPU shader color tinting (fixes colored text bug)
   - Multi-language architecture design
   - Furigana rendering system

4. ✅ **Serves as reference architecture**
   - Sections 7-9 describe implementation details PR #737 uses
   - Understanding the "why" helps extend the "what"
   - Alternative approaches preserved for comparison

### How To Read This Document Now

**Section 1-6:** Read as **architectural reference** and **problem analysis**
- Understand WHY the multi-page system is necessary
- Learn the constraints and technical background
- See how our research validates PR #737's approach

**Section 7-9:** Read as **PR #737 implementation notes**
- Each section now includes "PR #737 Implementation" subsection
- Compares our original spec vs actual PR #737 code
- Identifies what to reuse vs what to extend

**Section 10-14:** Read as **future work** building on PR #737
- Furigana, testing, deployment all still applicable
- Assumes PR #737 as baseline, not starting from scratch

### Related Documents

- **`PR737_ANALYSIS.md`** - Complete code analysis of PR #737 (42,000 tokens)
- **`ARCHITECTURAL_RETROSPECTIVE.md`** - Why PR #737's approach is superior to our original spec
- **`IMPLEMENTATION_VERIFICATION_CHECKLIST.md` Section 16** - Questions answered by PR #737
- **`FEATURE_ROADMAP.md`** - Updated timeline (2.5-4 months vs 5-8 months)

---

## TABLE OF CONTENTS

1. [Executive Mission Briefing](#1-executive-mission-briefing)
2. [Architectural Overview & Strategic Analysis](#2-architectural-overview--strategic-analysis)
3. [Critical Terminology & Concepts](#3-critical-terminology--concepts)
4. [Asset Specifications & Data Structures](#4-asset-specifications--data-structures)
5. [FFNx Codebase Architecture](#5-ffnx-codebase-architecture)
6. [Deep Dive: Technical Constraints & Solutions](#6-deep-dive-technical-constraints--solutions)
7. [Implementation Specification: C++ Modifications](#7-implementation-specification-c-modifications)
8. [Implementation Specification: Assembly Hooks](#8-implementation-specification-assembly-hooks)
9. [Implementation Specification: Renderer Integration](#9-implementation-specification-renderer-integration)
10. [Advanced Feature: Furigana Support](#10-advanced-feature-furigana-support)
11. [Testing & Verification Protocol](#11-testing--verification-protocol)
12. [Risk Mitigation & Debugging Guide](#12-risk-mitigation--debugging-guide)
13. [Deployment Checklist](#13-deployment-checklist)
14. [Reference Materials & Appendices](#14-reference-materials--appendices)

---

## 1. EXECUTIVE MISSION BRIEFING

### 1.1 The Objective

You are tasked with extending the **FFNx graphics driver** to enable **native Japanese text rendering** in the English version of Final Fantasy VII (1998/Steam/2013).

**The Problem:**
- The vanilla English game engine is architecturally limited to a **Single-Byte Character Encoding** system (0x00-0xFF)
- It can only address a maximum of **256 unique characters**
- Japanese requires approximately **2,300+ glyphs** (Hiragana, Katakana, and Kanji)
- Mathematical impossibility: 256 < 2,300

**The Breakthrough:**
- Analysis of the rare 2013 Japanese eStore version revealed Square Enix's production solution
- They implemented a **Multi-Page Texture System** using the proprietary AF3DN.P driver
- The system uses **unused control codes (0xFA-0xFE)** as texture page-switching opcodes
- This is a **proven, production-viable architecture**

**Your Mission:**
- Reimplement this architecture within the **open-source FFNx driver**
- Do NOT use the proprietary AF3DN.P directly
- Leverage FFNx's modern **BGFX rendering backend**
- Create a legally sound, community-maintainable solution
- Enable future extensibility (multi-language support, Furigana, real-time switching)

### 1.2 Success Criteria

**Phase 1 (Core Implementation):**
- ✅ FFNx successfully loads 6 font texture pages
- ✅ FA-FE control codes trigger texture page switching
- ✅ Japanese characters render at correct width (16px, not squashed)
- ✅ No crashes when launching ff7_ja.exe
- ✅ English mode continues to work (backward compatibility)

**Phase 2 (Advanced Features):**
- ✅ Furigana (reading guides) render correctly above Kanji
- ✅ Runtime language switching (en ↔ ja without restart)
- ✅ 7th Heaven .iro integration working
- ✅ Custom font path override functional

**Phase 3 (Polish):**
- ✅ All verification tests pass
- ✅ FFNx.log shows clear diagnostic information
- ✅ No memory leaks or corruption
- ✅ Performance overhead < 5% compared to English mode

### 1.3 Research Foundation & Prerequisites

This specification is based on comprehensive analysis of:

**Primary Source:**
- Square Enix's 2013 Japanese eStore version (ff7_ja.exe + AF3DN.P)
- Complete reverse engineering of AF3DN.P driver (317KB)
- Extraction and analysis of all 6 Japanese font textures (jafont_1-6.tex)

**Community Resources Analyzed:**
- 52 technical documentation sources
- qhimm.com modding community archives
- FFNx GitHub repository and issue tracker
- Japanese community blogs and resources

**Critical Discoveries:**
- Complete character encoding system (FA-FE extended pages)
- 1,331 character mapping to Unicode (ff7_complete_mapping_compact.csv)
- Production-proven multi-page texture architecture

**Prerequisites:**
- Familiarity with C++ and x86 assembly
- Understanding of DirectX/OpenGL rendering pipelines
- Access to FF7 PC version (Steam or original)
- FFNx development environment setup
- Debugging tools (x64dbg, Cheat Engine, or similar)

For complete research documentation: See masterfindings.md (Sessions 1-12)

### 1.4 Architecture Rationale

**Why Driver-Level Implementation:**
- ✅ No EXE modification required (works with unmodified executables)
- ✅ Clean separation of concerns (rendering vs game logic)
- ✅ Compatible with both ff7_en.exe and ff7_ja.exe
- ✅ Maintainable and legally sound (clean-room implementation)

**Why FFNx Over AF3DN.P:**
- ✅ Open source (MIT license) vs proprietary
- ✅ Modern rendering backend (BGFX supports Vulkan, DX12, Metal)
- ✅ Active community development and support
- ✅ Cross-platform potential (Windows, Linux via Wine)
- ✅ Future extensibility (multi-language, real-time switching, furigana)

**Rejected Alternatives:**

**Approach A: Direct Shift-JIS Implementation**
- ❌ FF7 doesn't use Shift-JIS internally (uses custom FA-FE encoding)
- ❌ Would require complete text parser rewrite
- ❌ Incompatible with existing game logic

**Approach B: EXE Patching**
- ❌ Version-specific (breaks with updates)
- ❌ Legal concerns (binary modification)
- ❌ Difficult to maintain and distribute
- ❌ Conflicts with other mods

**Approach C: Use AF3DN.P Directly**
- ❌ Proprietary (cannot legally distribute)
- ❌ Closed source (cannot extend or fix)
- ❌ Limited to DirectX 9
- ❌ No community support

**This Implementation (Driver Extension):**
- ✅ Proven architecture (Square Enix validated in production)
- ✅ Community maintainable
- ✅ Compatible with existing mods and tools
- ✅ Extensible for future features

### 1.5 Known Issues & Community Context

**FFNx Japanese Support Status (as of 2025):**

Per HAL's Blog (Japanese FF7 modding community):
- ⚠️ **FFNx Japanese support broken since 2020**
- Issue: Post-v1.x updates broke Japanese font rendering
- Workaround: Some users reverted to older FFNx versions
- **This implementation fixes the root cause**

**Platform Compatibility:**

**Windows 7:**
- ⚠️ FFNx versions >1.6.1 are incompatible with Windows 7
- Limitation: DirectX 11 requirement in newer builds
- Solution: Use FFNx ≤1.6.1 or upgrade to Windows 10/11

**Windows 10/11:**
- ✅ Full compatibility with latest FFNx versions
- ✅ All features supported

**Known Limitations:**

1. **Character Set:**
   - 1,536 total character slots (6 pages × 256)
   - 1,331 currently mapped characters
   - 205 empty slots available for expansion

2. **Performance:**
   - Minimal overhead (<5%) compared to English mode
   - DDS textures recommended for SSDs (40-70% faster)
   - PNG textures recommended for HDD compatibility

3. **Text File Encoding:**
   - Game text must be encoded in FF7's custom FA-FE format
   - Standard Shift-JIS files require conversion
   - Use provided character mapping CSV for encoding

**Text Rendering Contexts (Edge Cases):**

FF7 has multiple distinct text rendering systems. Each requires separate consideration:

| Context | Texture Source | Rendering Path | Japanese Status |
|---------|---------------|----------------|-----------------|
| **Field Dialogue** | `menu_ja.lgp` → jafont_*.tex | Field module, dialog windows | ✅ PR #737 works |
| **Menu Screens** | `menu_ja.lgp` → jafont_*.tex | Menu module | ✅ PR #737 works |
| **Battle Text** | `battle_ja.lgp` | Battle module, separate queue | ⚠️ Needs verification |
| **Name Entry** | `menu_ja.lgp` | Grid-based selection UI | ❌ PR #737 broken |
| **Minigames** | Various | Game-specific code paths | ❓ Not documented |
| **World Map** | World module assets | World map text handler | ⚠️ Needs verification |

**Dialog Window System (Field Module):**
- Supports up to **4 simultaneous dialog windows**
- Window structure: 0x30 bytes per window (position, size, state, text pointer)
- **State machine:** 15 states (0-E) controlling open/close/scroll/input
- Window bounds: X ≥ 8, Y ≥ 8, max X+W = 0x138 (312px), max Y+H = 0xE0 (224px)
- Row height: 16px + 9px padding
- Opcodes: MESSAGE (0x40), ASK (0x48), WINDOW (0x50), WMODE (0x52), etc.

**Battle Text System:**
- Uses `battle_display_text_queue` (64 entries max)
- Separate timing/frame system with `battle_frame_multiplier`
- Battle-specific encoding: EA-F0 are variable markers, F8 = box color, F9 = LZS compression
- FFNx hooks: `display_battle_action_text_42782A`, `set_battle_text_active`

**Name Entry Screen (Japanese Version):**
- **4 input pages:** ひらがな (Hiragana), カタカナ (Katakana), 英数 (EISUU/Alphanumeric), possibly symbols
- Navigation: スペース (Space), さくじょ (Delete), けってい (Enter), デフォルト (Default)
- Uses **grid-based character selection** (not stream-based like dialogue)
- FFNx patches `keyboard_name_input` function for Steam gamepad compatibility
- **PR #737 Bug:** Grid rendering assumes single-page fonts → shows corruption

**Community Resources:**
- qhimm.com: Primary modding forum
- FFNx Discord: Real-time developer support
- 7th Heaven Catalog: Mod distribution platform

**7th Heaven & Hext Constraint:**

⚠️ **CRITICAL:** 7th Heaven requires FF7_en.exe (not FF7_ja.exe or other language executables)

**Why This Matters:**
- Hext patches are memory address-specific
- Different language executables have different memory layouts
- Popular mods (ESUI, Echo-s, Finishing Touch) all target FF7_en.exe addresses

**Example Memory Layout Differences:**

| Function/Data | FF7_en.exe | FF7_es.exe | FF7_fr.exe |
|---------------|------------|------------|------------|
| draw_text     | 0x66E272   | 0x67A1B4   | 0x669F82   |
| font_width    | 0x99DDA8   | 0x9A1FC2   | 0x99B3D1   |

**Our Implementation Strategy:**
- ✅ Use FF7_en.exe exclusively
- ✅ Route text data by language (not executable switching)
- ✅ Maintains compatibility with entire 7th Heaven mod ecosystem
- ✅ Single Hext patch works for all languages

**For Non-Technical Explanation:**
See `reference/ARCHITECTURE_CLARIFICATION.md` for user-friendly overview of how this system works.

### 1.6 Multi-Language Expansion Architecture

**Overview:**

While this specification focuses on Japanese implementation, the architecture supports expansion to 10+ languages with minimal additional work.

**Language Categories:**

**Category 1: Romance Languages (Easy - No Driver Changes)**
- Spanish, French, German, Portuguese, Italian
- Fit in 256 characters (single-byte encoding)
- Only need: translated text files + accented font variants
- Implementation: 20-40 hours per language

**Category 2: CJK Languages (Medium - Require Multi-Page System)**
- Japanese (current focus) - 6 pages
- Chinese Traditional - 5-6 pages
- Chinese Simplified - 5-6 pages
- Korean - 5-6 pages
- Implementation: 100-150 hours per language

**Font Page Allocation Map:**

```
Current Implementation (Japanese):
Page 0:  (no marker)     - ASCII/Latin/Hiragana/Katakana
Page 1:  0xFA            - Japanese Kanji Set A
Page 2:  0xFB            - Japanese Kanji Set B
Page 3:  0xFC            - Japanese Kanji Set C
Page 4:  0xFD            - Japanese Kanji Set D
Page 5:  0xFE            - Japanese Kanji Set E

Available Expansion Slots:
Page 6:  0xF0            - Chinese Traditional Set A
Page 7:  0xF1            - Chinese Traditional Set B
Page 8:  0xF2            - Chinese Traditional Set C
Page 9:  0xF3            - Chinese Traditional Set D
Page 10: 0xF4            - Chinese Traditional Set E

Future Reserved:
Page 11-14: 0xEB-0xEF    - Korean/Cyrillic/Arabic (future)

Theoretical Maximum: ~15 pages before control code conflicts
```

**Character Coverage:**
- Japanese: ~2,136 characters (JIS Level 1 + Level 2)
- Chinese Traditional: ~5,000 characters (Big5 common set)
- Korean: ~2,350 characters (Hangul syllables)
- Total capacity: ~9,500 unique glyphs across all CJK languages

**Multi-Language Support Matrix:**

| Language | Font Pages | Text Encoding | Driver Changes | Complexity | Effort |
|----------|-----------|---------------|----------------|------------|--------|
| English | 1 (ASCII) | Single-byte | None | Simple | ✅ Done |
| Spanish | 1 (ASCII+á,é,í,ó,ú,ñ) | Single-byte | None | Simple | 20-40h |
| French | 1 (ASCII+à,é,è,ê,ç) | Single-byte | None | Simple | 20-40h |
| German | 1 (ASCII+ä,ö,ü,ß) | Single-byte | None | Simple | 20-40h |
| Japanese | 6 (Kana+Kanji) | FA-FE multi-byte | **Required** | Complex | ✅ Current |
| Chinese Trad | 5-6 (Hanzi) | F0-F4 multi-byte | Extension | Complex | 100-150h |
| Korean | 5-6 (Hangul) | EB-EF multi-byte | Extension | Complex | 100-150h |

**Implementation Implications:**

**For Spanish/French/German (Category 1):**
1. Extract official translations (if available)
2. Re-encode for FF7_en.exe compatibility
3. Create `lang-{code}/` directory structure
4. Package as .iro mod for 7th Heaven
5. No FFNx code changes needed

**For Chinese/Korean (Category 2):**
1. Extend Assembly hook to detect new page markers (0xF0-0xF4, 0xEB-0xEF)
2. Create additional font texture pages (zhfont_*.png, kofont_*.png)
3. Build character mapping CSV (Unicode → page + index)
4. Translate and encode text files
5. Test with FF7_en.exe + FFNx

**Runtime Language Switching (Future Feature):**

The architecture supports hot-swapping languages without restart:

```toml
# FFNx.toml (future)
[multi_language]
default_language = "en"
available_languages = ["en", "ja", "zh-tw", "es", "fr", "de"]
language_cycle_key = "F12"
show_language_toast = true
```

User Experience:
```
Playing in English → Press F12 → Switch to Japanese → Continue playing
                   → All dialogue updates
                   → Font system changes
                   → No restart needed
```

**For Complete Multi-Language Implementation:**
See `reference/MULTI_LANGUAGE_FINDINGS.md` for:
- Detailed translation workflows
- Chinese/Korean encoding examples
- Community translation platform architecture
- File redirection routing logic
- Translation validation tools

---

### 1.7 Potential PR #737 Improvements (Future Enhancements)

PR #737 provides a working Japanese implementation, but these improvements could be made after fixing its known bugs:

**1. Configuration-Based Width Tables**

*Current:* 1,536 values hardcoded in C++ array (`charWidthData[6][256]`)
*Better:* Load from `jafont_widths.csv` at runtime

```cpp
// Current (PR #737)
int charWidthData[6][256] = {
    { 30, 30, 28, 31, ... }, // 1,536 hardcoded values
};

// Better (future)
FontMetrics metrics = FontMetrics::LoadFromFile("mods/Textures/menu/jafont_widths.csv");
```

*Benefits:*
- Mod customization without recompiling FFNx
- Per-font-pack width adjustments
- Community can fix individual character widths

**2. Abstracted FontPage Struct**

*Current:* Repetitive switch statements for FA/FB/FC/FD/FE

```cpp
// Current (PR #737)
switch (*buffer_text) {
    case 0xFAu:
        graphics_object = ff7_externals.menu_jafont_2_graphics_object;
        charWidth = charWidthData[1][*buffer_text];
        break;
    case 0xFBu:
        // ... repeated for each page marker
}
```

*Better:* Data-driven FontPage struct array

```cpp
// Better (future)
struct FontPage {
    ff7_graphics_object* texture;
    int* widthTable;
    byte page_marker;
};

FontPage font_pages[6] = {
    { &jafont_1, charWidthData[0], 0x00 },
    { &jafont_2, charWidthData[1], 0xFA },
    // ... extensible for Chinese/Korean
};
```

*Benefits:*
- Extensible for Chinese/Korean without code changes
- Cleaner maintainability
- Runtime language additions possible

**3. Colored Texture Variants or Shader Tinting**

*Current Issue:* `get_character_color()` RGB multiply fails on non-white base textures

*Option A (Texture Variants):*
- Load separate `jafont_X_red.tim`, `jafont_X_blue.tim` variants
- More textures but authentic to original

*Option B (Shader Tinting):*
- GPU shader applies color tint dynamically
- Fewer textures, more flexible

---

## 2. ARCHITECTURAL OVERVIEW & STRATEGIC ANALYSIS

### 2.1 The Core Technical Deficit

**English FF7 Engine Architecture:**
```
Text Data (KERNEL.BIN) → Single-Byte Indices (0x00-0xFF) → USFONT.TEX (256x256 texture) → Renderer
```

**Why This Fails for Japanese:**
1. **Capacity Constraint:** 256 slots < 2,300 required characters
2. **Encoding Conflict:** Shift-JIS is double-byte (e.g., `0x82 0xA0`)
   - English engine reads this as TWO separate characters: `0x82` and `0xA0`
   - Results in rendering two garbage Latin characters instead of one Kanji
3. **Architectural Limitation:** The game's text parser is hardcoded for single-byte reads
4. **Memory Layout:** Width tables, coordinate calculations, and buffer sizes assume 256 max

### 2.2 The AF3DN.P Solution (Reference Architecture)

**Discovered Architecture from Japanese eStore Release:**

```
Text Data → Custom Parser → Page Marker Detection → Multi-Texture System → Renderer
                ↓                      ↓                       ↓
        0xFA detected           Switch to Page 1        Bind jafont_2.tex
        0xFB detected           Switch to Page 2        Bind jafont_3.tex
        ...                     ...                     ...
```

**Key Components:**
1. **Asset Structure:** Six 1024x1024 texture pages (jafont_1.tex through jafont_6.tex)
2. **Encoding System:**
   - `0x00-0xE6`: Standard characters → Page 0 (jafont_1)
   - `0xFA [Index]`: Extended characters → Page 1 (jafont_2)
   - `0xFB [Index]`: Extended characters → Page 2 (jafont_3)
   - `0xFC [Index]`: Extended characters → Page 3 (jafont_4)
   - `0xFD [Index]`: Extended characters → Page 4 (jafont_5)
   - `0xFE [Index]`: Extended characters → Page 5 (jafont_6)
3. **Driver Logic:** AF3DN.P intercepts DirectX 9 texture binding calls
4. **Geometry Handling:** Custom width tables for fixed-width Kanji rendering

**Why This Works:**
- `0xFA-0xFE` were **unused control codes** in the English version
- No collision with existing game logic
- Backward compatible (English files don't contain these codes)
- Minimal changes required (driver-level only, no EXE modification)

### 2.3 The FFNx Implementation Strategy (Path C - Hybrid Extension)

**Our Approach:**

```
FFNx Driver Extensions:
├── Configuration Layer (TOML settings)
├── Memory Allocation Override (Force 6 texture slots)
├── Asset Loading Pipeline (Load all 6 PNGs)
├── Registry Virtualization (Language-aware paths)
├── Assembly Hook (Text parser injection)
├── Renderer State Management (Texture page binding)
└── Geometry Patch (Character width table)
```

**Advantages:**
- ✅ **Open Source:** FFNx is MIT licensed
- ✅ **Modern Backend:** BGFX supports Vulkan, DirectX 12, Metal
- ✅ **Community Support:** Active development and maintenance
- ✅ **Legal:** Clean-room reimplementation based on reverse engineering
- ✅ **Extensible:** Foundation for multi-language, Furigana, and future features
- ✅ **No EXE Patching:** Works with both ff7_en.exe and ff7_ja.exe unmodified

**Implementation Layers:**

| Layer | Component | Language | Files Modified |
|-------|-----------|----------|----------------|
| 1. Configuration | User-facing toggles | TOML | FFNx.toml |
| 2. Globals | State variables | C++ | src/cfg.h, src/cfg.cpp, src/globals.h |
| 3. Allocation | Memory override | C++ | src/common.cpp |
| 4. Loading | Asset pipeline | C++ | src/saveload.cpp |
| 5. Redirection | File path handling | C++ | src/redirect.cpp, src/common.cpp |
| 6. Geometry | Width table patch | C++ | src/ff7/font.cpp, src/ff7/menu.cpp |
| 7. Parser Hook | Text byte stream | Assembly (Hext) | misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt |
| 8. Renderer | Texture binding | C++ | src/gl/gl.cpp |

---

## 3. CRITICAL TERMINOLOGY & CONCEPTS

### 3.1 Core Technologies

**FFNx:**
- A modern, open-source **graphics driver replacement** for FF7/FF8
- Replaces the original game's `AF3DN.P` (English) or proprietary driver (Japanese)
- Provides advanced features: high-resolution rendering, texture replacement, mod API
- Written in C++ with BGFX backend (cross-platform graphics abstraction)
- **Our primary development target**

**BGFX:**
- Rendering library that abstracts DirectX, OpenGL, Vulkan, Metal
- Used by FFNx for modern graphics API support
- Handles texture binding, shader management, and draw calls
- We hook into BGFX's texture binding logic for page switching

**7th Heaven:**
- The de facto **mod manager** for FF7
- Acts as a **Virtual File System (VFS)**
- Intercepts the game's file I/O calls
- Serves modified assets from `.iro` archives (ZIP-like containers)
- **Primary distribution platform** for this mod

**Hext:**
- A system for applying **in-memory assembly patches** to executables at runtime
- Used by FFNx to modify game logic without changing the EXE on disk
- Patch files are human-readable text with custom syntax
- **Critical for intercepting the text parser**

### 3.2 File Formats

**LGP Archive (.lgp):**
- Square Enix's proprietary archive format (similar to ZIP/TAR)
- Contains game assets: textures, models, dialogue, scripts
- Structure: Header + File Table + Data Blocks
- Tools: `ulgp` (extract), `lgp_tool` (pack/unpack)
- **Critical files:**
  - `menu_us.lgp` / `menu_ja.lgp`: UI textures, fonts
  - `flevel.lgp` / `jfleve.lgp`: Field maps, scripts (note the typo!)
  - `battle.lgp` / `battle_ja.lgp`: Battle assets

**TEX Texture (.tex):**
- Bitmap image format used by FF7 PC port
- Derived from PlayStation's TIM (Tim Image) format
- Structure: Header (palette count, dimensions) + Palette Data + Pixel Data
- **Critical header field:** `palettes` (determines texture slot allocation)
- Tools: `TexTools`, FFNx's built-in loader
- **Our intervention point:** Override allocation based on filename, not header

**PNG Override System:**
- FFNx checks `mods/Textures/` for `.png` files **before** loading `.tex` files
- Naming convention: `{original_name}.png` (e.g., `usfont_h.png`)
- **Load order (priority):**
  1. `mods/Textures/` (loose files)
  2. 7th Heaven VFS (`.iro` archives)
  3. Game directory (vanilla `.lgp` archives)

### 3.3 Encoding Systems

**FF7 Text Encoding (English):**
- **Single-Byte System:** Each character is 1 byte (0x00-0xFF)
- **Direct Mapping:** Byte value = texture cell index
- Example: `0x41` = 'A' (cell 65 in USFONT.TEX)
- **Control codes:** `0xE0-0xEF` (character names, tabs), `0xFE XX` (colors, variables)
- **Limitation:** Maximum 256 characters (0x00-0xFF)

**Control Code Categories (All Versions):**

| Range | Purpose | Notes |
|-------|---------|-------|
| `0x00-0xD3` | Printable characters | Direct texture index |
| `0xD4-0xDF` | **UNUSED** | Produces graphical errors |
| `0xE0-0xE6` | Tab/formatting | E0=Choice indent, E1=Tab(4), E7=Newline |
| `0xE7` | Line break | Advance to next line |
| `0xE8-0xE9` | Window control | Next window/page |
| `0xEA-0xF2` | Character names | EA=Cloud, EB=Barret, EC=Tifa, etc. |
| `0xF3-0xF5` | Party member names | Current party slots 1-3 |
| `0xF6-0xF9` | Button symbols | PlayStation controller buttons |
| `0xFA-0xFE` | **Japanese extended** | Page markers (see below) |
| `0xFF` | End of string | Terminator |

**Text Color Control Codes (via FE opcode):**

| Code | Color | Behavior |
|------|-------|----------|
| `FE D2` | Gray | Standard modifier - can be reset |
| `FE D3` | Blue | Standard modifier - can be reset |
| `FE D4` | Red | Standard modifier - can be reset |
| `FE D5` | Purple | Standard modifier - can be reset |
| `FE D6` | Green | Standard modifier - can be reset |
| `FE D7` | Cyan | Standard modifier - can be reset |
| `FE D8` | Yellow | Standard modifier - can be reset |
| `FE D9` | White | Reset to default color |
| `FE DA` | **Flash** | ⚠️ **Global** - affects entire window, cannot reset |
| `FE DB` | **Rainbow** | ⚠️ **Global + Animated** - cycles colors per-frame |

**Color Implementation (How It Works):**
- Font textures are **grayscale/white base**
- Colors applied via **RGB multiplication** at render time
- PR #737's `get_character_color()` returns BGRA values per color code
- **Bug:** Japanese fonts may have non-white base → multiplication produces wrong colors
- **Solution:** GPU shader tinting or ensure pure white font base

**FF7 Japanese Encoding (FA-FE System):**
- **Two-Byte Sequences for Extended Characters:**
  - First byte: `0xFA`, `0xFB`, `0xFC`, `0xFD`, or `0xFE` (page marker)
  - Second byte: `0x00-0xFF` (character index within that page)
- **Example:** `0xFA 0x00` = First character in jafont_2.png
- **Single-Byte Fallback:** `0x00-0xE6` still map to jafont_1.png (base page)
- **Total Capacity:**
  - Page 0: 231 characters (0x00-0xE6)
  - Pages 1-5: 256 characters each × 5 = 1,280
  - **Total: 1,511 characters** (sufficient for core Japanese)

**Shift-JIS (NOT Used):**
- Standard Japanese encoding in Windows/web
- We do **NOT** use Shift-JIS internally
- Unicode → FF7 Encoding conversion happens via `ff7_complete_mapping_compact.csv`
- Game text files are encoded in the custom FA-FE system

### 3.4 Memory Structures

**Character Width Table:**
- **Location:** Loaded from `KERNEL.BIN` / `WINDOW.BIN` into RAM
- **Pointer:** `common_externals.font_info` (FFNx struct)
- **Address (US 1.02):** `0x99DDA8` (varies by version!)
- **Structure:** Array of 256 bytes, each representing a character's width in pixels
  ```c
  char width_table[256] = {
      0x04, // 0x00: Control code width
      0x04, // 0x01: ...
      ...
      0x08, // 0x41: 'A' width
      0x0C, // 0x57: 'W' width (wider)
      ...
  };
  ```
- **Problem:** English widths are 4-12px. Kanji require 16px.
- **Solution:** Overwrite this table in RAM with fixed 16px values

**Texture Set Structure (FFNx):**
```c
struct texture_set {
    struct gl_texture_set *gl_set;
    uint32_t *texturehandle;  // Array of GPU texture handles
    uint32_t palette_index;   // Currently active palette
    // ... other fields
};

struct gl_texture_set {
    uint32_t textures;  // Number of allocated texture slots
    // ... other fields
};
```
- **Critical:** `textures` determines array size allocation
- **Default logic:** `textures = (palettes > 0) ? palettes * 2 : 1`
- **English font:** USFONT.TEX has `palettes = 1` → allocates 2 slots
- **Our override:** Force `textures = 6` for Japanese fonts

---

## 4. ASSET SPECIFICATIONS & DATA STRUCTURES

### 4.1 Font Texture Manifest

**Required Assets Location:** `mods/Textures/menu/`

| Filename | Encoding Range | Content Description | Dimensions | Grid Layout |
|----------|----------------|---------------------|------------|-------------|
| `jafont_1.png` | `0x00-0xE6` | Hiragana, Katakana, Numbers, ASCII, Punctuation | 1024×1024 | 16×16 grid (64px glyphs) |
| `jafont_2.png` | `0xFA + [0x00-0xFF]` | Kanji Set A (Battle/Skill/Magic terms) | 1024×1024 | 16×16 grid |
| `jafont_3.png` | `0xFB + [0x00-0xFF]` | Kanji Set B (Character names, locations) | 1024×1024 | 16×16 grid |
| `jafont_4.png` | `0xFC + [0x00-0xFF]` | Kanji Set C (Dialogue, common words) | 1024×1024 | 16×16 grid |
| `jafont_5.png` | `0xFD + [0x00-0xFF]` | Kanji Set D (Rare Kanji, proper nouns) | 1024×1024 | 16×16 grid |
| `jafont_6.png` | `0xFE + [0x00-0xFF]` | Kanji Set E (Extended set, special characters) | 1024×1024 | 16×16 grid |

**Texture Specifications:**
- **Format:** PNG (RGBA8888 recommended for best compatibility)
- **Resolution:** 1024×1024 pixels (enforced by FFNx)
- **Grid:** 16×16 cells = 256 total cells per texture
- **Cell Size:** 64×64 pixels per glyph
- **Color Depth:** 32-bit RGBA (supports anti-aliasing and drop shadows)
- **UV Mapping:** Standard (0,0) = top-left, (1,1) = bottom-right
- **Coordinate Calculation:**
  - Given character index `idx` (0-255):
    - `grid_x = idx % 16`
    - `grid_y = idx / 16`
    - `uv_x0 = grid_x * (1.0 / 16.0)`
    - `uv_y0 = grid_y * (1.0 / 16.0)`
    - `uv_x1 = uv_x0 + (1.0 / 16.0)`
    - `uv_y1 = uv_y0 + (1.0 / 16.0)`

### 4.2 Character Mapping Data

**Master Mapping Table:** `docs/ff7_complete_mapping_compact.csv`

**Structure:**
```csv
texture,index,character,unicode
jafont_1,0,バ,U+30D0
jafont_1,1,ば,U+3070
jafont_1,2,ビ,U+30D3
jafont_1,3,び,U+3073
...
jafont_2,0,必,U+5FC5
jafont_2,1,殺,U+6BBA
...
jafont_6,255,,
```

**Fields:**
- `texture`: Which PNG file (`jafont_1` through `jafont_6`)
- `index`: Cell position within the 16×16 grid (0-255)
- `character`: The actual Unicode character (for human readability)
- `unicode`: Unicode code point in U+XXXX format

**Total Characters Mapped:** 1,331
**Format:** LLM-optimized CSV for easy parsing and tool integration

**Usage Example (Text Encoding):**
```python
# To encode the character '私' (watashi = "I"):
# 1. Look up in CSV: '私' = U+79C1
# 2. Find row: texture=jafont_2, index=12
# 3. Encode as: 0xFA 0x0C
#    - 0xFA = switch to Page 1 (jafont_2)
#    - 0x0C = character index 12 (hex)
```

### 4.3 Japanese File Structure (Critical Differences)

**Directory Layout (ff7_ja.exe expects):**
```
FF7_JA/
├── ff7_ja.exe
├── data/
│   ├── lang-ja/              # ← Japanese-specific path
│   │   ├── menu_ja.lgp       # ← Contains jafont_*.tex
│   │   ├── jfleve.lgp        # ← Correct Japanese filename
│   │   ├── battle_ja.lgp
│   │   └── movies/
│   │       ├── eidoslogo.avi
│   │       └── ...
│   ├── cd/                   # Shared data
│   └── ...
├── AF3DN.P                   # Japanese driver (proprietary)
└── ...
```

**vs. English File Structure:**
```
FF7_EN/
├── ff7.exe
├── data/
│   ├── menu/
│   │   └── menu_us.lgp       # ← English path
│   ├── field/
│   │   └── flevel.lgp        # ← Correct spelling
│   ├── battle/
│   │   └── battle.lgp
│   └── movies/
│       └── ...
└── ...
```

**Critical File Name Differences (MUST Handle):**

| Component | English Filename | Japanese Filename | Notes |
|-----------|------------------|-------------------|-------|
| Menu/Font | `menu_us.lgp` | `menu_ja.lgp` | Contains font textures |
| Field Maps | `flevel.lgp` | `jfleve.lgp` | **Correct Japanese name** (not a typo) |
| Battle | `battle.lgp` | `battle_ja.lgp` | Standard `_ja` suffix |
| Movies Path | `data/movies/` | `data/lang-ja/movies/` | Nested in lang-ja/ |
| Data Path | `data/` | `data/lang-ja/` | Base path difference |

**Important Note:**
`jfleve.lgp` is the **actual, correct** Japanese filename. This is NOT a typo. Do not attempt to redirect to `jflevel.lgp` as that file does not exist in Japanese installations.

**Why This Matters:**
- `ff7_ja.exe` requests these specific paths via registry queries
- If FFNx returns English paths, the game crashes immediately
- Our registry virtualization (Section 7.2) must handle this

---

## 5. FFNX CODEBASE ARCHITECTURE

### 5.1 Repository Structure

```
FFNx/
├── src/                      # C++ source code
│   ├── cfg.cpp               # Configuration parsing (TOML)
│   ├── cfg.h                 # Configuration declarations
│   ├── common.cpp            # Core driver logic, hooks, texture loading
│   ├── common.h              # Common headers
│   ├── globals.h             # Global variables
│   ├── saveload.cpp          # Texture loading pipeline
│   ├── redirect.cpp          # File path redirection
│   ├── hext.cpp              # Hext patch system
│   ├── ff7/                  # FF7-specific code
│   │   ├── menu.cpp          # Menu rendering
│   │   ├── font.cpp          # Font handling (we'll create this)
│   │   ├── font.h            # Font declarations (we'll create this)
│   │   └── ff7_data.h        # Memory addresses, structures
│   └── gl/                   # OpenGL/BGFX rendering
│       ├── gl.cpp            # Main rendering logic
│       └── texture.cpp       # Texture management
├── misc/
│   └── hext/                 # Hext patch files
│       └── ff7/
│           ├── en/           # English version patches
│           │   └── FFNx.JAPANESE_FONT.txt  # We'll create this
│           └── jp/           # Japanese version patches
├── FFNx.toml                 # User configuration file
└── ...
```

### 5.2 Key Subsystems

**Configuration System (cfg.cpp / cfg.h):**
- Parses `FFNx.toml` using TOML11 library
- Exposes settings as global `extern` variables
- Read once at startup, immutable during runtime
- **Our additions:** `font_language`, `font_enable_furigana`, `font_path_override`

**Common Driver Logic (common.cpp):**
- **`DllMain`:** Entry point, initializes FFNx, detects executable
- **`common_init`:** Sets up hooks, loads configuration
- **`common_load_texture`:** Allocates texture memory (**critical intervention point**)
- **`common_palette_changed`:** Handles palette switching requests
- **`dotemuReg*` functions:** Virtual registry for game compatibility

**Texture Pipeline (saveload.cpp):**
- **`load_external_texture`:** Checks for PNG overrides before loading TEX
- **`load_texture_helper`:** PNG decoding, GPU upload
- **`load_texture`:** Main entry point, orchestrates loading

**File Redirection (redirect.cpp):**
- **`attempt_redirection`:** Maps virtual paths to physical paths
- Handles 7th Heaven VFS, mod paths, language paths
- **Our addition:** `flevel.lgp` → `jfleve.lgp` mapping for Japanese

**Rendering Backend (gl/gl.cpp):**
- **`gl_draw_indexed_primitive`:** Main draw call function
- **`gl_bind_texture_set`:** Texture binding logic (**critical hook point**)
- **`gl_set_texture`:** Sets active texture on GPU
- Interfaces with BGFX for cross-platform rendering

### 5.3 Critical Memory Addresses & Structures

**Version-Specific Addresses (US 1.02):**

| Symbol | Address | Type | Description |
|--------|---------|------|-------------|
| `font_info` | `0x99DDA8` | `char*` | Pointer to character width table (256 bytes) |
| `draw_graphics_object` | `0x66E272` | Function | Main text rendering function (approximation) |
| Character processing loop | ~`0x66E2A0` | Code | Loop that reads text bytes (target for Hext) |

**⚠️ CRITICAL WARNING:**
- These addresses are **ONLY VALID** for FF7 US 1.02 executable
- Steam version has **DIFFERENT** addresses (ASLR, different build)
- `ff7_ja.exe` has **COMPLETELY DIFFERENT** addresses
- **ALWAYS use `common_externals` pointers** instead of hardcoded addresses
- FFNx already resolves version-specific addresses at runtime

**FFNx Common Externals Structure:**
```c
struct common_externals {
    // ... many fields ...
    char *font_info;              // Points to width table (version-agnostic)
    void (*create_texture_set)(); // Texture set allocator
    // ... more fields ...
};

extern struct common_externals common_externals;  // Global instance
```

**Accessing Memory Safely:**
```c
// ✅ CORRECT: Use FFNx's version-agnostic pointer
char* width_table = common_externals.font_info;
if (width_table) {
    width_table[0x41] = 0x10;  // Set 'A' width to 16px
}

// ❌ WRONG: Hardcoded address (will crash on different versions)
char* width_table = (char*)0x99DDA8;  // NEVER DO THIS
```

---

## 6. DEEP DIVE: TECHNICAL CONSTRAINTS & SOLUTIONS

### 6.1 Constraint #1: The Geometry vs. Texture Problem ("Squashed Kanji")

**The Single Most Critical Technical Hurdle**

**Symptom:**
You replace an English character's texture (e.g., 'W') with a full-width Kanji (私). In-game, the Kanji appears horizontally compressed, vertically stretched, or "squashed" like a barcode.

**Root Cause Analysis:**

The FF7 engine **separates geometry generation from texture mapping**. This is a two-stage process:

**Stage 1: Geometry Generation (FF7.exe)**
```c
// Pseudocode of what the game does
void DrawCharacter(char character_code) {
    // 1. Look up width from the table in RAM
    char width = font_width_table[character_code];

    // 2. Generate 3D quad vertices
    float x0 = cursor_x;
    float y0 = cursor_y;
    float x1 = cursor_x + width;   // ← Width comes from table
    float y1 = cursor_y + 16;      // Height is fixed 16px

    // 3. Send to renderer
    Vertex vertices[4] = {
        {x0, y0, uv_x0, uv_y0},
        {x1, y0, uv_x1, uv_y0},
        {x1, y1, uv_x1, uv_y1},
        {x0, y1, uv_x0, uv_y1}
    };
    RenderQuad(vertices, current_texture);

    // 4. Advance cursor
    cursor_x += width;
}
```

**Stage 2: Texture Mapping (FFNx)**
```c
// FFNx receives pre-calculated vertices
void gl_draw_indexed_primitive(Vertex* vertices, int count, uint32_t texture) {
    // FFNx has NO CONTROL over vertex positions
    // It can only change the texture being mapped

    // If vertices define a 8px wide quad...
    // But the texture contains a 64px wide Kanji...
    // The GPU will squash the 64px texture into the 8px quad!

    BindTexture(texture);
    DrawTriangles(vertices, count);
}
```

**Example Failure:**
```
English 'W' in USFONT:
- Width table: font_width_table[0x57] = 12  (12 pixels wide)
- Geometry: 12px × 16px quad
- Texture: 12px wide glyph
- Result: ✅ Perfect fit

Japanese '私' replacing 'W':
- Width table: font_width_table[0x57] = 12  (STILL 12! Not updated)
- Geometry: 12px × 16px quad (STILL narrow!)
- Texture: 64px wide Kanji glyph (from jafont_2.png)
- Result: ❌ 64px texture squashed into 12px quad = barcode Kanji
```

**Visual Representation:**
```
Expected (16px quad):        Actual (8px quad):
┌────────────────┐           ┌──────┐
│                │           │      │
│      私        │           │ 私   │  ← Squashed!
│                │           │      │
└────────────────┘           └──────┘
   16px × 16px                  8px × 16px
```

**The Solution:**

**Patch the width table in RAM BEFORE the game generates geometry:**

```c
void PatchFontWidthsForJapanese() {
    if (font_language != "ja") return;

    // Get pointer to width table (version-agnostic)
    char* width_table = common_externals.font_info;
    if (!width_table) {
        ffnx_error("font_info pointer is NULL! Cannot patch widths.\n");
        return;
    }

    ffnx_info("Patching character width table for Japanese mode...\n");

    // Make memory writable
    DWORD oldProtect;
    if (!VirtualProtect(width_table, 256, PAGE_READWRITE, &oldProtect)) {
        ffnx_error("VirtualProtect failed! Error: %d\n", GetLastError());
        return;
    }

    // Overwrite ALL widths with fixed 16px
    for (int i = 0; i < 256; i++) {
        // 0x00-0x1F are control codes, but we set them anyway (unused for geometry)
        width_table[i] = 0x10;  // 16 pixels in hex
    }

    // Restore original memory protection
    VirtualProtect(width_table, 256, oldProtect, &oldProtect);

    ffnx_info("Width table patched: all characters now 16px wide.\n");
}
```

**When to Call:**
- **MUST** be called during `ff7_init_hooks` (in `src/ff7_opengl.cpp`)
- **MUST** be called AFTER `ff7_data(game_object)` (which sets up `common_externals`)
- **MUST** be called BEFORE any text rendering occurs

**Side Effects:**
- ✅ Fixes Kanji squashing
- ⚠️ Makes English text look "spaced out" (each letter becomes 16px wide)
- ⚠️ May cause text to overflow dialog boxes if mixing English/Japanese
- ✅ Necessary trade-off for correct rendering

---

### 6.2 Constraint #2: The Texture Allocation & Palette System

**Understanding FFNx's Texture Management**

**The Palette Swapping Mechanism:**

FFNx inherits a **palette-swapping system** from the PlayStation version of FF7. This allows multiple color variations of the same texture without duplicating geometry.

**How It Works:**
```c
struct texture_set {
    uint32_t* texturehandle;  // Array of GPU texture handles
    uint32_t palette_index;   // Currently active palette (0-based)
};

// When the game wants to change color:
void common_palette_changed(texture_set* tex, uint32_t new_palette) {
    tex->palette_index = new_palette;
    // Bind the corresponding texture handle
    gl_set_texture(tex->texturehandle[new_palette]);
}
```

**Example (Character Sprites):**
```
Cloud sprite might have:
- texturehandle[0] = Normal color scheme
- texturehandle[1] = Poison (green tint)
- texturehandle[2] = Berserk (red tint)
```

**Our Exploitation:**

We **hijack this system** for font page switching:
```
Font texture_set:
- texturehandle[0] = jafont_1.png (base page)
- texturehandle[1] = jafont_2.png (Kanji A)
- texturehandle[2] = jafont_3.png (Kanji B)
- texturehandle[3] = jafont_4.png (Kanji C)
- texturehandle[4] = jafont_5.png (Kanji D)
- texturehandle[5] = jafont_6.png (Kanji E)
```

**The Allocation Problem:**

**Current FFNx Logic (src/common.cpp:~1457):**
```c
// Determine number of texture slots to allocate
uint32_t num_textures = VREF(tex_header, palettes) > 0
                        ? VREF(tex_header, palettes) * 2
                        : 1;

// Allocate array
VRASS(texture_set, texturehandle,
      (uint32_t*)external_calloc(num_textures, sizeof(uint32_t)));
```

**English USFONT.TEX Header:**
```
palettes = 1
→ num_textures = 1 * 2 = 2
→ Allocates array: texturehandle[0..1]
```

**If We Try to Load 6 Textures Without Override:**
```c
for (int i = 0; i < 6; i++) {
    texture_set->texturehandle[i] = LoadTexture(...);
    // ❌ When i=2: BUFFER OVERFLOW!
    // ❌ When i=3, 4, 5: Writing to unallocated memory
    // ❌ Result: Segmentation fault / heap corruption
}
```

**The Fix - Force Allocation Override:**

```c
// Inside common_load_texture, BEFORE the allocation block
bool is_font_texture = false;
if (VREF(tex_header, file.pc_name)) {
    const char* name = VREF(tex_header, file.pc_name);
    if (strstr(name, "usfont") || strstr(name, "jafont")) {
        is_font_texture = true;
    }
}

if (!VREF(texture_set, texturehandle)) {
    uint32_t num_textures_to_alloc;

    if (is_font_texture && font_language == "ja") {
        // [OVERRIDE] Force 6 slots for Japanese
        num_textures_to_alloc = 6;
        ffnx_info("Japanese font detected: forcing allocation of 6 texture pages.\n");
    } else {
        // [ORIGINAL] Standard behavior
        num_textures_to_alloc = VREF(tex_header, palettes) > 0
                                 ? VREF(tex_header, palettes) * 2
                                 : 1;
    }

    // Allocate with correct size
    VRASS(texture_set, ogl.gl_set->textures, num_textures_to_alloc);
    VRASS(texture_set, texturehandle,
          (uint32_t*)external_calloc(num_textures_to_alloc, sizeof(uint32_t)));
}
```

**Critical Timing:**
- ✅ MUST happen BEFORE any `texturehandle[i]` writes
- ✅ MUST check filename, NOT just rely on config (English might load usfont)
- ✅ MUST allocate EXACTLY 6 (not dynamic based on actual files found)

---

### 6.3 Constraint #3: Registry Virtualization & File Pathing

**The Problem:**

The 2013 Steam/eStore executables were designed to run in a **sandboxed environment** (DRM protection). They don't use the Windows Registry directly. Instead, they call **virtual registry functions** that the driver provides.

**The Virtual Registry System:**

```c
// ff7.exe (or ff7_ja.exe) calls these:
LSTATUS RegOpenKeyExA(HKEY hKey, LPCSTR lpSubKey, ...);
LSTATUS RegQueryValueExA(HKEY hKey, LPCSTR lpValueName, ...);

// But these redirect to:
LSTATUS dotemuRegOpenKeyExA(HKEY hKey, LPCSTR lpSubKey, ...);  // FFNx provides this
LSTATUS dotemuRegQueryValueExA(HKEY hKey, LPCSTR lpValueName, ...);  // FFNx provides this

// FFNx exports these functions (see misc/FFNx.def)
```

**What the Game Queries:**

```c
// The game asks for these registry keys:
RegQueryValueExA(hKey, "AppPath", ...)    // Where is FF7 installed?
RegQueryValueExA(hKey, "DataPath", ...)   // Where is data folder?
RegQueryValueExA(hKey, "MoviePath", ...)  // Where are movies?
```

**Current FFNx Implementation (English-only):**

```c
// src/common.cpp
__declspec(dllexport) LSTATUS __stdcall
dotemuRegQueryValueExA(HKEY hKey, LPCSTR lpValueName, ...) {
    char buf[MAX_PATH];

    if (strcmp(lpValueName, "DataPath") == 0) {
        GetCurrentDirectory(sizeof(buf), buf);
        strcat(buf, "\\data\\");  // ← HARDCODED ENGLISH PATH
        strcpy((CHAR*)lpData, buf);
        return ERROR_SUCCESS;
    }

    // Similar for MoviePath...
}
```

**Why This Breaks for ff7_ja.exe:**

```
ff7_ja.exe requests "DataPath"
→ FFNx returns "C:\FF7\data\"
→ ff7_ja.exe looks for "C:\FF7\data\menu_ja.lgp"
→ File doesn't exist (it's in "C:\FF7\data\lang-ja\menu_ja.lgp")
→ Crash: "Cannot load required data"
```

**The Solution - Language-Aware Paths:**

```c
__declspec(dllexport) LSTATUS __stdcall
dotemuRegQueryValueExA(HKEY hKey, LPCSTR lpValueName, LPDWORD lpReserved,
                       LPDWORD lpType, LPBYTE lpData, LPDWORD lpcbData) {
    char buf[MAX_PATH];
    LSTATUS ret = ERROR_SUCCESS;

    // [NEW] Detect which executable is running
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    _strlwr(exePath);  // Convert to lowercase for easier comparison

    bool isJapaneseExe = (strstr(exePath, "ff7_ja.exe") != NULL);

    /* FF7 Registry Queries */
    if (strcmp(lpValueName, "AppPath") == 0) {
        GetCurrentDirectory(*lpcbData, buf);
        strcat(buf, "\\");
        strcpy((CHAR*)lpData, buf);
    }
    else if (strcmp(lpValueName, "DataPath") == 0) {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-specific path
        if (isJapaneseExe) {
            strcat(buf, "\\data\\lang-ja\\");  // Japanese path
        } else {
            strcat(buf, "\\data\\");           // English path
        }

        strcpy((CHAR*)lpData, buf);
    }
    else if (strcmp(lpValueName, "MoviePath") == 0) {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-specific path
        if (isJapaneseExe) {
            strcat(buf, "\\data\\lang-ja\\movies\\");  // Japanese path
        } else {
            strcat(buf, "\\data\\movies\\");           // English path
        }

        strcpy((CHAR*)lpData, buf);
    }
    // ... other registry keys ...

    return ret;
}
```

**Additional Considerations:**

**Option 1: Exe Detection (Current approach)**
- Pro: Automatic, no user configuration needed
- Pro: Works even if user forgets to set `font_language`
- Con: Requires both exe files to coexist

**Option 2: Config-Based (Alternative)**
```c
if (font_language == "ja") {
    strcat(buf, "\\data\\lang-ja\\");
}
```
- Pro: Works with single exe (ff7.exe) in Japanese mode
- Con: User MUST set `font_language = "ja"` in config
- Con: Crash if misconfigured

**Recommendation:** Use **BOTH** for redundancy:
```c
bool useJapanesePaths = isJapaneseExe || (font_language == "ja");
```

---

### 6.4 Japanese File Naming Conventions

**Understanding Japanese Filenames:**

The Japanese version of FF7 uses specific file naming conventions that differ from the English version. These are **intentional design choices** by Square Enix, not errors.

**Complete Japanese File Manifest:**

| Component | English | Japanese | Notes |
|-----------|---------|----------|-------|
| Menu/Font | `menu_us.lgp` | `menu_ja.lgp` | Standard _ja suffix |
| Field Maps | `flevel.lgp` | `jfleve.lgp` | **Intentional Japanese name** |
| Battle | `battle.lgp` | `battle_ja.lgp` | Standard _ja suffix |
| Movies | `movies/` | `lang-ja/movies/` | Handled by registry paths |

**Critical Note on jfleve.lgp:**

`jfleve.lgp` is the **correct, intentional** Japanese filename. This is NOT a typo or packaging error. Do not implement redirections from flevel→jfleve as this can cause issues when:
- Running ff7_ja.exe (expects jfleve.lgp explicitly)
- Using Japanese asset packs
- Working with community Japanese mods

**File Resolution:**

The Japanese executable (ff7_ja.exe) and registry paths handle file location automatically:
- Registry returns `data/lang-ja/` base path
- Game appends `jfleve.lgp` to construct full path
- No redirection logic needed in FFNx

**Implementation Guidance:**

Do not add special redirection logic for jfleve.lgp. The standard FFNx file resolution handles Japanese files correctly through:
1. Registry path virtualization (Section 7.2)
2. mod_path system for overrides
3. 7th Heaven VFS integration

---

## 7. IMPLEMENTATION SPECIFICATION: C++ MODIFICATIONS

### 7.1 Configuration Extension (src/cfg.h, src/cfg.cpp)

**Objective:** Add user-facing toggles to `FFNx.toml` without breaking existing functionality.

**File: src/cfg.h**

Add these declarations **AFTER** existing `extern` declarations:

```cpp
// src/cfg.h

// ... existing externs ...
extern long external_music_volume;
extern bool ff7_advanced_blinking;
extern long display_index;

// [NEW] Japanese Language Support Configuration
extern std::string font_language;         // "en", "ja" - Primary language toggle
extern bool font_enable_furigana;         // true/false - Enable Furigana rendering
extern std::string font_path_override;    // Custom path for font textures (advanced users)
extern bool is_using_japanese_exe;        // Runtime detection flag (set by DllMain)
```

**File: src/cfg.cpp**

Add definitions and parsing logic:

```cpp
// src/cfg.cpp

// [NEW] Definitions (at top with other definitions)
std::string font_language;
bool font_enable_furigana;
std::string font_path_override;
bool is_using_japanese_exe = false;  // Default to false, set during init

void read_cfg()
{
    // ... existing parsing code ...

    // [NEW] Parse font configuration from FFNx.toml
    // Place this BEFORE the "SAFE DEFAULTS" section

    font_language = config["font_language"].value_or("en");

    // Validate font_language value
    if (font_language != "en" && font_language != "ja") {
        ffnx_warning("Invalid font_language '%s'. Defaulting to 'en'.\n",
                     font_language.c_str());
        font_language = "en";
    }

    font_enable_furigana = config["font_enable_furigana"].value_or(false);
    font_path_override = config["font_path_override"].value_or("");

    // Log configuration
    ffnx_info("Font Language: %s\n", font_language.c_str());
    if (font_enable_furigana) {
        ffnx_info("Furigana: Enabled\n");
    }
    if (!font_path_override.empty()) {
        ffnx_info("Font Path Override: %s\n", font_path_override.c_str());
    }

    // ... rest of read_cfg() ...
}
```

**User-Facing Configuration (FFNx.toml):**

Users will add these lines to their `FFNx.toml`:

```toml
###############################################################################
# Japanese Language Support
###############################################################################

# Font language ("en" = English, "ja" = Japanese)
# Default: "en"
font_language = "ja"

# Enable Furigana (reading guides above Kanji)
# Note: Requires special font textures with Furigana data
# Default: false
font_enable_furigana = false

# Custom font texture path (advanced users only)
# Leave empty to use default: mods/Textures/menu/
# Example: "mods/CustomFonts/ja/"
# Default: ""
font_path_override = ""
```

---

### 7.2 Runtime Executable Detection & Registry Hooks (src/common.cpp)

**Objective:** Detect if `ff7_ja.exe` is running and provide correct registry paths.

**Location: DllMain (Entry Point)**

```cpp
// src/common.cpp

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // ... existing initialization ...

        // [NEW] Detect Japanese executable
        char moduleName[MAX_PATH];
        if (GetModuleFileNameA(NULL, moduleName, MAX_PATH)) {
            _strlwr(moduleName);  // Convert to lowercase

            if (strstr(moduleName, "ff7_ja.exe") != NULL) {
                is_using_japanese_exe = true;
                ffnx_info("Detected Japanese executable: ff7_ja.exe\n");

                // Force Japanese language mode
                font_language = "ja";
                ffnx_info("Auto-enabled Japanese language mode.\n");
            }
        }

        // ... rest of initialization ...
        break;
    }
    return TRUE;
}
```

**Location: dotemuRegQueryValueExA (Virtual Registry)**

```cpp
// src/common.cpp

__declspec(dllexport) LSTATUS __stdcall dotemuRegQueryValueExA(
    HKEY hKey,
    LPCSTR lpValueName,
    LPDWORD lpReserved,
    LPDWORD lpType,
    LPBYTE lpData,
    LPDWORD lpcbData)
{
    char buf[MAX_PATH];
    LSTATUS ret = ERROR_SUCCESS;

    // Determine if we should use Japanese paths
    bool useJapanesePaths = is_using_japanese_exe || (font_language == "ja");

    /* FF7 Registry Keys */
    if (strcmp(lpValueName, "AppPath") == 0)
    {
        GetCurrentDirectory(*lpcbData, buf);
        strcat(buf, "\\");
        strcpy((CHAR*)lpData, buf);

        if (trace_all || trace_registry) {
            ffnx_trace("AppPath: %s\n", buf);
        }
    }
    else if (strcmp(lpValueName, "DataPath") == 0)
    {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-aware path
        if (useJapanesePaths) {
            strcat(buf, "\\data\\lang-ja\\");
            ffnx_info("DataPath (Japanese): %s\n", buf);
        } else {
            strcat(buf, "\\data\\");
            if (trace_all || trace_registry) {
                ffnx_trace("DataPath (English): %s\n", buf);
            }
        }

        strcpy((CHAR*)lpData, buf);
    }
    else if (strcmp(lpValueName, "MoviePath") == 0)
    {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-aware path
        if (useJapanesePaths) {
            strcat(buf, "\\data\\lang-ja\\movies\\");
            ffnx_info("MoviePath (Japanese): %s\n", buf);
        } else {
            strcat(buf, "\\data\\movies\\");
            if (trace_all || trace_registry) {
                ffnx_trace("MoviePath (English): %s\n", buf);
            }
        }

        strcpy((CHAR*)lpData, buf);
    }
    // ... handle other registry keys (CDROM path, etc.) ...
    else
    {
        ret = ERROR_FILE_NOT_FOUND;
    }

    return ret;
}
```

**Also Update Other Registry Functions:**

```cpp
// src/common.cpp

__declspec(dllexport) LSTATUS __stdcall dotemuRegOpenKeyExA(
    HKEY hKey,
    LPCSTR lpSubKey,
    DWORD ulOptions,
    REGSAM samDesired,
    PHKEY phkResult)
{
    // Log for debugging
    if (trace_all || trace_registry) {
        ffnx_trace("RegOpenKeyExA: %s\n", lpSubKey);
    }

    // Always succeed (we fake the registry)
    *phkResult = hKey;
    return ERROR_SUCCESS;
}

// Similar for dotemuRegCloseKey, etc.
```

---

### 7.3 Texture Allocation Override (src/common.cpp)

**Objective:** Force allocation of 6 texture slots for Japanese fonts.

**Location: common_load_texture function (~Line 1450)**

**⚠️ CRITICAL SECTION - Buffer Overflow Prevention**

```cpp
// src/common.cpp

struct texture_set *common_load_texture(
    struct texture_set *_texture_set,
    struct tex_header *_tex_header,
    struct texture_format *texture_format)
{
    // ... existing variable declarations ...
    VOBJ(texture_set, texture_set, _texture_set);
    VOBJ(tex_header, tex_header, _tex_header);

    // no existing texture set, create one
    if (!VPTR(texture_set))
    {
        _texture_set = common_externals.create_texture_set();
        VASS(texture_set, texture_set, _texture_set);
    }

    if(!VREF(texture_set, ogl.gl_set))
    {
        VRASS(texture_set, ogl.gl_set, common_externals.create_texture_format());
    }

    // [NEW] Detect if this is a font texture BEFORE allocation
    bool is_font_texture = false;
    if (VREF(tex_header, file.pc_name)) {
        const char* tex_name = VREF(tex_header, file.pc_name);

        // Check for font texture names (case-insensitive)
        char lower_name[256];
        strncpy(lower_name, tex_name, sizeof(lower_name));
        _strlwr(lower_name);

        if (strstr(lower_name, "usfont") || strstr(lower_name, "jafont")) {
            is_font_texture = true;
            ffnx_info("Font texture detected: %s\n", tex_name);
        }
    }

    // texture handle array may not have been initialized
    if(!VREF(texture_set, texturehandle))
    {
        uint32_t num_textures;

        if (is_font_texture && font_language == "ja") {
            // [CRITICAL OVERRIDE] Force 6 texture slots for Japanese
            num_textures = 6;
            ffnx_info("Japanese mode: Allocating %d texture pages for font.\n", num_textures);
        }
        else {
            // [ORIGINAL LOGIC] Standard palette-based allocation
            num_textures = VREF(tex_header, palettes) > 0
                           ? VREF(tex_header, palettes) * 2
                           : 1;

            if (trace_all || trace_loaders) {
                ffnx_trace("Allocating %d texture slots (palettes=%d).\n",
                           num_textures, VREF(tex_header, palettes));
            }
        }

        // Allocate the array
        VRASS(texture_set, ogl.gl_set->textures, num_textures);
        VRASS(texture_set, texturehandle,
              (uint32_t*)external_calloc(num_textures, sizeof(uint32_t)));

        if (!VREF(texture_set, texturehandle)) {
            ffnx_error("Failed to allocate texture handle array!\n");
            return NULL;
        }

        // ... rest of initialization (stats, etc.) ...
        stats.texture_count++;
    }

    // ... rest of common_load_texture function ...

    return _texture_set;
}
```

**Validation Logic:**

Add safety checks to verify allocation succeeded:

```cpp
// Later in common_load_texture, before loading textures:
if (is_font_texture && font_language == "ja") {
    uint32_t allocated_count = VREF(texture_set, ogl.gl_set->textures);
    if (allocated_count < 6) {
        ffnx_error("CRITICAL: Font texture allocation failed! Expected 6, got %d\n",
                   allocated_count);
        return NULL;  // Abort to prevent corruption
    }
}
```

---

### 7.4 Multi-Page Texture Loader (src/saveload.cpp)

**Objective:** Load all 6 Japanese font textures when requested.

**Location: load_external_texture function**

```cpp
// src/saveload.cpp

uint32_t load_external_texture(
    const char* name,
    uint32_t* width,
    uint32_t* height,
    struct texture_set* texture_set)
{
    // ... existing code ...

    // [NEW] Special handler for Japanese fonts
    // This MUST execute BEFORE the standard texture loading logic
    if (font_language == "ja" && (strstr(name, "usfont") || strstr(name, "jafont"))) {
        ffnx_info("Japanese font loading initiated for: %s\n", name);

        // Determine base path
        std::string base_path;
        if (!font_path_override.empty()) {
            base_path = font_path_override;
            ffnx_info("Using custom font path: %s\n", base_path.c_str());
        } else {
            base_path = mod_path + "/menu/";
        }

        // Load all 6 pages
        bool all_loaded = true;
        uint32_t first_handle = 0;

        for (int i = 0; i < 6; i++) {
            char filename[1024];

            // Construct filename: jafont_1.png, jafont_2.png, etc.
            // Note: Files are 1-indexed (jafont_1), array is 0-indexed (i=0)
            _snprintf(filename, sizeof(filename), "%sjafont_%d.png",
                      base_path.c_str(), i + 1);

            // Normalize path (convert / to \ on Windows)
            normalize_path(filename);

            // Load texture from disk
            uint32_t w, h;
            uint32_t tex_handle = load_texture_helper(filename, &w, &h, true, true);

            if (tex_handle) {
                // Store in the texture set array
                // Note: We're directly writing to the texturehandle array we allocated
                VREF(texture_set, texturehandle[i]) = tex_handle;

                // Store dimensions (all pages should be same size)
                if (i == 0) {
                    *width = w;
                    *height = h;
                    first_handle = tex_handle;
                }

                ffnx_info("Loaded Japanese font page %d: %s (%dx%d)\n",
                          i + 1, filename, w, h);
            }
            else {
                ffnx_error("FAILED to load Japanese font page %d: %s\n",
                           i + 1, filename);
                all_loaded = false;

                // [CRITICAL DECISION] Fail-fast or continue?
                // Option A: Abort completely
                // return 0;

                // Option B: Continue and hope the page isn't needed
                // (Current behavior - risky but allows partial functionality)
            }
        }

        if (!all_loaded) {
            ffnx_warning("Not all Japanese font pages loaded. Text may appear corrupted.\n");
        } else {
            ffnx_info("Successfully loaded all 6 Japanese font pages.\n");
        }

        // Return the first page's handle (base page with Hiragana/Katakana)
        return first_handle;
    }

    // ... existing standard texture loading logic ...

    return 0;  // Not found
}
```

**Error Handling Improvement:**

Add a validation function:

```cpp
// src/saveload.cpp (helper function)

bool validate_font_texture_set(struct texture_set* tex_set) {
    if (!tex_set || !VREF(tex_set, texturehandle)) {
        ffnx_error("Texture set validation failed: NULL pointer\n");
        return false;
    }

    uint32_t allocated = VREF(tex_set, ogl.gl_set->textures);
    if (allocated < 6) {
        ffnx_error("Texture set validation failed: only %d slots allocated (need 6)\n",
                   allocated);
        return false;
    }

    // Check if all handles are valid
    for (int i = 0; i < 6; i++) {
        uint32_t handle = VREF(tex_set, texturehandle[i]);
        if (handle == 0) {
            ffnx_warning("Texture slot %d is empty (handle=0)\n", i);
        }
    }

    return true;
}

// Call after loading:
if (font_language == "ja") {
    if (!validate_font_texture_set(texture_set)) {
        ffnx_error("Font texture set validation failed!\n");
    }
}
```

---

### 7.5 File Redirection for Japanese Variants (src/redirect.cpp)

**Objective:** Handle Japanese archive naming conventions when English executables are used with Japanese assets.

**⚠️ IMPORTANT:** Do NOT implement flevel→jfleve redirection. `jfleve.lgp` is the correct Japanese filename, not a typo. The Japanese executable (ff7_ja.exe) requests jfleve.lgp directly and handles paths through registry virtualization.

**Location: attempt_redirection function**

```cpp
// src/redirect.cpp

int attempt_redirection(const char* input_path, char* output_path) {
    // ... existing redirection logic (mod paths, 7th Heaven VFS, etc.) ...

    // [NEW] Japanese file name variants (only for EN→JA conversion)
    // This should be checked BEFORE the final "file not found" return

    if (font_language == "ja" && !is_using_japanese_exe) {
        // NOTE: Only redirect when using English EXE with Japanese assets
        // The Japanese EXE handles these paths automatically

        // Handle menu archive variants
        if (strstr(input_path, "menu_us.lgp") || strstr(input_path, "MENU_US.LGP")) {
            std::string ja_variant = input_path;
            size_t pos;

            pos = ja_variant.find("menu_us.lgp");
            if (pos != std::string::npos) {
                ja_variant.replace(pos, 11, "menu_ja.lgp");
            } else {
                pos = ja_variant.find("MENU_US.LGP");
                if (pos != std::string::npos) {
                    ja_variant.replace(pos, 11, "MENU_JA.LGP");
                }
            }

            if (fileExists(ja_variant.c_str())) {
                strcpy(output_path, ja_variant.c_str());
                ffnx_info("Redirected menu archive: %s → %s\n",
                          input_path, output_path);
                return 0;
            }
        }

        // Handle battle archive variants
        if (strstr(input_path, "battle.lgp") || strstr(input_path, "BATTLE.LGP")) {
            // Only redirect if NOT already "battle_ja"
            if (!strstr(input_path, "battle_ja") && !strstr(input_path, "BATTLE_JA")) {
                std::string ja_variant = input_path;
                size_t pos;

                pos = ja_variant.find("battle.lgp");
                if (pos != std::string::npos) {
                    ja_variant.replace(pos, 10, "battle_ja.lgp");
                } else {
                    pos = ja_variant.find("BATTLE.LGP");
                    if (pos != std::string::npos) {
                        ja_variant.replace(pos, 10, "BATTLE_JA.LGP");
                    }
                }

                if (fileExists(ja_variant.c_str())) {
                    strcpy(output_path, ja_variant.c_str());
                    ffnx_info("Redirected battle archive: %s → %s\n",
                              input_path, output_path);
                    return 0;
                }
            }
        }
    }

    // ... existing final fallback logic ...
    return -1;  // File not found
}
```

**Complete Japanese File Mapping Table:**

For reference, here's the complete mapping:

```cpp
// Documentation comment in redirect.cpp

/*
 * Japanese File Name Mapping
 *
 * English          →  Japanese           Notes
 * ================================================================
 * flevel.lgp       →  jfleve.lgp        Correct Japanese filename
 * menu_us.lgp      →  menu_ja.lgp       Standard _ja suffix
 * battle.lgp       →  battle_ja.lgp     Standard _ja suffix
 * data/            →  data/lang-ja/     Path handled by registry
 * movies/          →  lang-ja/movies/   Path handled by registry
 */
```

#### 7.5.1 Multi-Language File Redirection Extension (Future)

**Objective:** Extend the redirection system to support multiple languages dynamically.

**Architecture:**

```cpp
// src/redirect.cpp (extended version)

// Language code enum
enum LanguageCode {
    LANG_EN,     // English (default)
    LANG_JA,     // Japanese
    LANG_ZH_TW,  // Chinese Traditional
    LANG_ZH_CN,  // Chinese Simplified
    LANG_ES,     // Spanish
    LANG_FR,     // French
    LANG_DE,     // German
    LANG_KO,     // Korean
};

// Get current language from config
LanguageCode GetCurrentLanguage() {
    if (font_language == "ja") return LANG_JA;
    if (font_language == "zh-tw") return LANG_ZH_TW;
    if (font_language == "zh-cn") return LANG_ZH_CN;
    if (font_language == "es") return LANG_ES;
    if (font_language == "fr") return LANG_FR;
    if (font_language == "de") return LANG_DE;
    if (font_language == "ko") return LANG_KO;
    return LANG_EN;  // Default
}

// Language code strings
const char* GetLanguageCode(LanguageCode lang) {
    switch (lang) {
        case LANG_JA: return "ja";
        case LANG_ZH_TW: return "zh-tw";
        case LANG_ZH_CN: return "zh-cn";
        case LANG_ES: return "es";
        case LANG_FR: return "fr";
        case LANG_DE: return "de";
        case LANG_KO: return "ko";
        default: return "en";
    }
}

int attempt_redirection_multilang(const char* input_path, char* output_path) {
    // ... existing mod paths, 7th Heaven VFS logic ...

    LanguageCode lang = GetCurrentLanguage();

    // Skip redirection for English
    if (lang == LANG_EN) {
        strcpy(output_path, input_path);
        return 0;
    }

    const char* lang_code = GetLanguageCode(lang);
    bool is_japanese_exe = (strstr(exe_name, "ff7_ja") != NULL);

    // KERNEL.BIN redirection
    if (strstr(input_path, "KERNEL.BIN") || strstr(input_path, "kernel.bin")) {
        sprintf(output_path, "data/lang-%s/kernel/KERNEL.BIN", lang_code);
        if (fileExists(output_path)) {
            ffnx_info("Redirected KERNEL.BIN → %s\n", output_path);
            return 0;
        }
    }

    // menu LGP redirection
    if (strstr(input_path, "menu_us.lgp") || strstr(input_path, "MENU_US.LGP")) {
        sprintf(output_path, "data/lang-%s/menu/menu_%s.lgp", lang_code, lang_code);
        if (fileExists(output_path)) {
            ffnx_info("Redirected menu → %s\n", output_path);
            return 0;
        }
    }

    // field LGP redirection (handle jfleve for Japanese)
    if (strstr(input_path, "flevel.lgp") || strstr(input_path, "FLEVEL.LGP")) {
        if (lang == LANG_JA) {
            // Japanese uses jfleve.lgp (correct filename)
            sprintf(output_path, "data/lang-ja/field/jfleve.lgp");
        } else {
            // Other languages use standard flevel_*.lgp
            sprintf(output_path, "data/lang-%s/field/flevel_%s.lgp", lang_code, lang_code);
        }
        if (fileExists(output_path)) {
            ffnx_info("Redirected field → %s\n", output_path);
            return 0;
        }
    }

    // battle LGP redirection
    if (strstr(input_path, "battle.lgp") || strstr(input_path, "BATTLE.LGP")) {
        // Only redirect if NOT already language-specific
        if (!strstr(input_path, "_ja") && !strstr(input_path, "_es") &&
            !strstr(input_path, "_fr") && !strstr(input_path, "_de")) {
            sprintf(output_path, "data/lang-%s/battle/battle_%s.lgp", lang_code, lang_code);
            if (fileExists(output_path)) {
                ffnx_info("Redirected battle → %s\n", output_path);
                return 0;
            }
        }
    }

    // world map redirection
    if (strstr(input_path, "world_us.lgp") || strstr(input_path, "WORLD_US.LGP")) {
        sprintf(output_path, "data/lang-%s/world/world_%s.lgp", lang_code, lang_code);
        if (fileExists(output_path)) {
            ffnx_info("Redirected world → %s\n", output_path);
            return 0;
        }
    }

    // Fallback to original path
    strcpy(output_path, input_path);
    return 0;
}
```

**Directory Structure for Multi-Language:**

```
data/
├── lang-ja/           # Japanese
│   ├── kernel/KERNEL.BIN
│   ├── menu/menu_ja.lgp
│   ├── field/jfleve.lgp
│   └── battle/battle_ja.lgp
├── lang-es/           # Spanish
│   ├── kernel/KERNEL.BIN
│   ├── menu/menu_es.lgp
│   ├── field/flevel_es.lgp
│   └── battle/battle_es.lgp
├── lang-fr/           # French
│   ├── kernel/KERNEL.BIN
│   ├── menu/menu_fr.lgp
│   ├── field/flevel_fr.lgp
│   └── battle/battle_fr.lgp
├── lang-zh-tw/        # Chinese Traditional
│   ├── kernel/KERNEL.BIN
│   ├── menu/menu_zh-tw.lgp
│   ├── field/flevel_zh-tw.lgp
│   └── battle/battle_zh-tw.lgp
└── ... (English uses base data/)
```

**Implementation Notes:**

1. **For Romance Languages (Spanish/French/German):**
   - Simple text file swap, no font changes needed
   - Can reuse English font with extended characters (á, é, ñ, ü, etc.)
   - Only requires text translation + file packaging

2. **For CJK Languages (Chinese/Korean):**
   - Requires font page loading (similar to Japanese)
   - Needs Assembly hook extension for new page markers
   - Character encoding workflow required

**Testing Multi-Language Redirection:**

```cpp
// test/redirect_test.cpp
void test_language_redirection() {
    // Test Japanese
    font_language = "ja";
    char output[256];
    attempt_redirection_multilang("data/field/flevel.lgp", output);
    assert(strcmp(output, "data/lang-ja/field/jfleve.lgp") == 0);

    // Test Spanish
    font_language = "es";
    attempt_redirection_multilang("data/field/flevel.lgp", output);
    assert(strcmp(output, "data/lang-es/field/flevel_es.lgp") == 0);

    // Test Chinese
    font_language = "zh-tw";
    attempt_redirection_multilang("data/menu/menu_us.lgp", output);
    assert(strcmp(output, "data/lang-zh-tw/menu/menu_zh-tw.lgp") == 0);
}
```

---

### 7.6 Character Width Table Patch (src/ff7/font.cpp, src/ff7/font.h)

**Objective:** Fix the "Squashed Kanji" problem by overwriting the width table in RAM.

**Create New File: src/ff7/font.h**

```cpp
// src/ff7/font.h
#pragma once

#include "../common.h"

/**
 * Patches the in-memory character width table for Japanese mode.
 *
 * This function overwrites the width table (originally from KERNEL.BIN)
 * to use fixed 16px widths for all characters, preventing Kanji from
 * being squashed into narrow English character widths.
 *
 * MUST be called during ff7_init_hooks, AFTER ff7_data() has run.
 */
void PatchFontWidthsForJapanese();
```

**Create New File: src/ff7/font.cpp**

```cpp
// src/ff7/font.cpp

#include "font.h"
#include "../globals.h"
#include "../log.h"
#include "../ff7_data.h"
#include <windows.h>

void PatchFontWidthsForJapanese()
{
    // Only patch if Japanese mode is enabled
    if (font_language != "ja") {
        if (trace_all || trace_fonts) {
            ffnx_trace("Font width patching skipped (not in Japanese mode).\n");
        }
        return;
    }

    ffnx_info("Attempting to patch character width table for Japanese...\n");

    // Get pointer to width table (version-agnostic)
    // This pointer is set by FFNx during ff7_data() initialization
    char* font_width_table = common_externals.font_info;

    if (!font_width_table) {
        ffnx_error("CRITICAL: font_info pointer is NULL! Cannot patch widths.\n");
        ffnx_error("This usually means ff7_data() hasn't run yet, or the game version is unsupported.\n");
        return;
    }

    // Log the memory address (for debugging)
    ffnx_info("Width table located at: 0x%p\n", (void*)font_width_table);

    // Make the memory region writable
    DWORD oldProtect;
    if (!VirtualProtect(font_width_table, 256, PAGE_READWRITE, &oldProtect)) {
        DWORD error = GetLastError();
        ffnx_error("VirtualProtect failed! Error code: %d\n", error);
        ffnx_error("Cannot modify width table. Text will be squashed.\n");
        return;
    }

    // Overwrite ALL widths with fixed 16px
    for (int i = 0; i < 256; i++) {
        // Characters 0x00-0x1F are control codes (not rendered)
        // but we set them anyway for consistency
        font_width_table[i] = 0x10;  // 16 pixels (0x10 in hex)
    }

    // Optional: Set special widths for specific characters
    // (Uncomment if you want narrower spaces, for example)
    /*
    font_width_table[0x20] = 0x08;  // Space = 8px (half width)
    font_width_table[0x00] = 0x00;  // NULL terminator = 0px
    */

    // Restore original memory protection
    VirtualProtect(font_width_table, 256, oldProtect, &oldProtect);

    ffnx_info("Successfully patched character width table.\n");
    ffnx_info("All characters now use 16px width for Japanese rendering.\n");
}
```

**Integration: Modify src/ff7_opengl.cpp**

```cpp
// src/ff7_opengl.cpp

#include "ff7/font.h"  // [NEW] Add this include

void ff7_init_hooks(struct game_obj *_game_object)
{
    // ... existing code ...

    // Initialize FF7 data structures
    ff7_data(game_object);

    // [NEW] Apply Japanese font patches
    // MUST be called AFTER ff7_data() because it relies on common_externals.font_info
    PatchFontWidthsForJapanese();

    // ... rest of initialization ...
}
```

**Testing the Width Patch:**

Add a diagnostic function (optional, for debugging):

```cpp
// src/ff7/font.cpp

void DumpWidthTable() {
    if (font_language != "ja") return;

    char* table = common_externals.font_info;
    if (!table) return;

    ffnx_info("=== Character Width Table Dump ===\n");
    for (int i = 0; i < 256; i += 16) {
        char line[256];
        int pos = 0;
        pos += sprintf(line + pos, "0x%02X: ", i);
        for (int j = 0; j < 16; j++) {
            pos += sprintf(line + pos, "%02X ", (unsigned char)table[i + j]);
        }
        ffnx_info("%s\n", line);
    }
    ffnx_info("===================================\n");
}

// Call in PatchFontWidthsForJapanese() after patching:
// DumpWidthTable();
```

---

## 8. IMPLEMENTATION SPECIFICATION: ASSEMBLY HOOKS

### 8.1 The Text Parser Hook Concept

**Objective:** Intercept the game's text byte stream to detect FA-FE page markers.

**Current Game Logic (Simplified):**

```c
// Pseudocode of FF7's text rendering loop
void RenderTextString(const char* text) {
    const char* ptr = text;

    while (*ptr != 0x00) {  // Loop until NULL terminator
        char current_byte = *ptr;

        // Skip control codes (0x00-0x1F)
        if (current_byte < 0x20) {
            HandleControlCode(current_byte);
            ptr++;
            continue;
        }

        // Render the character
        DrawCharacter(current_byte);
        ptr++;
    }
}
```

**Our Modification:**

```c
// Modified logic (injected via Assembly)
void RenderTextString(const char* text) {
    const char* ptr = text;

    while (*ptr != 0x00) {
        char current_byte = *ptr;

        // [NEW] Check for page markers (FA-FE)
        if (current_byte >= 0xFA && current_byte <= 0xFE) {
            // Calculate page index: FA→1, FB→2, FC→3, FD→4, FE→5
            uint8_t page_index = current_byte - 0xFA + 1;

            // Update global state (FFNx will read this)
            g_currentFontPage = page_index;

            // Skip to next byte (the actual character index)
            ptr++;
            current_byte = *ptr;  // Now load the character
        } else {
            // Normal character, use page 0
            g_currentFontPage = 0;
        }

        // Skip control codes
        if (current_byte < 0x20) {
            HandleControlCode(current_byte);
            ptr++;
            continue;
        }

        // Render the character (with updated page index)
        DrawCharacter(current_byte);
        ptr++;
    }
}
```

---

### 8.2 Finding the Injection Point

**⚠️ CRITICAL: Address Discovery Process**

The exact memory address for the hook varies by executable version. Here's how to find it:

**Step 1: Set Up Debugging Tools**

- Install **x64dbg** (https://x64dbg.com/) or **Cheat Engine** (https://cheatengine.org/)
- Launch FF7 with FFNx installed
- Attach debugger to `ff7.exe` process

**Step 2: Locate Font Texture Loading**

```
1. Set breakpoint on CreateTextureA or D3DCreateTexture
2. Run game until breakpoint hits
3. Check call stack for function that requested the texture
4. If texture name contains "usfont", note the return address
```

**Step 3: Trace Back to Text Rendering**

```
1. From texture load, step back through call stack
2. Look for function named similar to:
   - draw_graphics_object
   - render_text
   - display_string
3. Note the function's start address (e.g., 0x66E272)
```

**Step 4: Find the Character Processing Loop**

```assembly
; Inside the text rendering function, look for this pattern:

LODSB              ; Load byte from [ESI] into AL, increment ESI
CMP AL, 0x00       ; Check for NULL terminator
JE EndOfString     ; If 0, jump to end
CMP AL, 0x1F       ; Check if control code
JBE ControlCode    ; If <= 0x1F, handle control code
CALL DrawChar      ; Otherwise, draw the character
JMP LoopStart      ; Repeat

; The injection point is RIGHT AFTER LODSB
; and BEFORE the first CMP
```

**Step 5: Verify the Address**

```
1. Set breakpoint at the LODSB instruction
2. Start a new game and enter a name
3. Breakpoint should hit repeatedly as name is rendered
4. Verify AL register contains ASCII values of your name
5. Note the address (e.g., 0x66E2A0)
```

**Known Addresses (Reference Only - DO NOT HARDCODE):**

| Version | Text Render Function | Character Loop | Notes |
|---------|---------------------|----------------|-------|
| US 1.02 | `0x66E272` | `~0x66E2A0` | Approximation |
| Steam (2013) | **Different** | **Different** | Use debugger |
| ff7_ja.exe | **Different** | **Different** | Use debugger |

**⚠️ WARNING:** These addresses are **APPROXIMATIONS** and may be incorrect. **ALWAYS verify with a debugger.**

---

### 8.3 The Hext Patch Implementation

**Create New File: misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt**

```hext
# FFNx Japanese Font Support - Text Parser Hook
#
# This patch intercepts the character processing loop to detect
# FA-FE page marker bytes and update the global font page variable.
#
# Target: FF7.exe (US 1.02)
# Location: Character processing loop inside text rendering function
#
# ⚠️ CRITICAL: The address below (0x66E2A0) is a PLACEHOLDER.
# You MUST replace it with the actual address found via debugger.
#
# Register assumptions (verify with debugger):
#   AL  = Current character byte (just loaded by LODSB)
#   ESI = String pointer (points to next character)
#   EBP = Stack frame pointer

# Set base offset (MUST match your debugger findings)
# Replace 0x66E2A0 with the actual address of the injection point
+0x66E2A0

# ================================================================
# INJECTED CODE STARTS HERE
# ================================================================

# Save original instruction that we're overwriting
# (This MUST be copied from the actual game code at this address)
# Example: If the original code was "CMP AL, 0x00", you'd put:
# CMP AL, 0x00

# Check if character byte is >= 0xFA (page marker range)
CMP AL, 0xFA
JB NormalCharacter     # If below 0xFA, it's a normal character

# ---- Page Marker Detected ----

# Calculate page index: FA→1, FB→2, FC→3, FD→4, FE→5
SUB AL, 0xFA           # AL = AL - 0xFA (FA→0, FB→1, etc.)
INC AL                 # AL = AL + 1 (0→1, 1→2, etc.)

# Store in global variable
# ⚠️ PLACEHOLDER: 0xCC0000 is a TEMPORARY address
# You MUST allocate a proper address (see section 8.4)
MOV BYTE PTR [0xCC0000], AL

# Advance to next byte (the actual character index)
INC ESI                # ESI now points to character index byte
MOV AL, [ESI]          # Load character index into AL

# Jump to the character drawing code
# (This address MUST match the location right after the original CMP)
JMP 0x66E2B0           # PLACEHOLDER - adjust to match actual code

# ---- Normal Character (no page marker) ----
NormalCharacter:

# Reset page index to 0 (base page)
MOV BYTE PTR [0xCC0000], 0

# Continue with original code flow
# (The game's original instruction goes here)
# Example:
# CMP AL, 0x1F
# (Replace with actual instruction)

# ================================================================
# INJECTED CODE ENDS HERE
# ================================================================
```

**Hext Syntax Reference:**

```hext
+0xADDRESS       # Set absolute address for following code
=BYTES           # Write raw bytes
JMP ADDR         # x86 jump instruction
CMP AL, VAL      # x86 compare instruction
MOV [ADDR], REG  # x86 move instruction
```

**⚠️ CRITICAL WARNINGS:**

1. **DO NOT USE 0xCC0000 IN PRODUCTION**
   - This is a placeholder address
   - It may conflict with game memory
   - Could cause random crashes
   - See Section 8.4 for proper allocation

2. **VERIFY ALL ADDRESSES**
   - Hext patches are **NOT** position-independent
   - Wrong addresses = instant crash
   - Test thoroughly after any game patch/update

3. **BACKUP ORIGINAL INSTRUCTIONS**
   - You're overwriting game code
   - Must recreate original behavior
   - Incorrect restoration = broken game logic

---

### 8.4 Global Variable Allocation for g_currentFontPage

**The Problem:**

The Hext patch needs to write to a memory address that:
1. Is safe (won't conflict with game data)
2. Is readable by FFNx C++ code
3. Persists across function calls

**Solution Options:**

**Option A: Static Allocation in FFNx DLL (Recommended)**

```cpp
// src/globals.h
#pragma pack(push, 1)
extern "C" {
    // Export this variable so the Hext patch can find it
    __declspec(dllexport) uint8_t g_currentFontPage;
}
#pragma pack(pop)

// src/common.cpp
uint8_t g_currentFontPage = 0;  // Default to page 0

// To get the address (for Hext patch):
// In DllMain:
void* page_ptr = &g_currentFontPage;
ffnx_info("g_currentFontPage address: 0x%p\n", page_ptr);
// Output: "g_currentFontPage address: 0x10AB1234"
// Use this address in the Hext patch!
```

**Hext patch update:**
```hext
# Replace 0xCC0000 with the actual address logged above
MOV BYTE PTR [0x10AB1234], AL  # Example address
```

**Option B: Allocate in Game Memory Space**

```cpp
// src/common.cpp
uint8_t* g_currentFontPage_ptr = nullptr;

void AllocateFontPageVariable() {
    // Find unused memory in the game's address space
    // FF7's executable typically loads at 0x400000
    // We can use space right after the .data section

    // Example: Allocate at a known safe address
    // (This requires memory map analysis)
    DWORD safe_address = 0xCC0000;  // Example

    g_currentFontPage_ptr = (uint8_t*)safe_address;

    // Make it writable
    DWORD oldProtect;
    VirtualProtect(g_currentFontPage_ptr, 1, PAGE_READWRITE, &oldProtect);

    // Initialize
    *g_currentFontPage_ptr = 0;

    ffnx_info("Allocated g_currentFontPage at: 0x%p\n", g_currentFontPage_ptr);
}
```

**Option C: Use Existing Game Variable (Advanced)**

If you find an unused byte in the game's memory (via debugger inspection), you can repurpose it:

```cpp
// Example: If you find that address 0x99DDFF is always 0 and never read
#define GAME_UNUSED_BYTE ((uint8_t*)0x99DDFF)

// In FFNx code:
uint8_t current_page = *GAME_UNUSED_BYTE;

// In Hext patch:
MOV BYTE PTR [0x99DDFF], AL
```

**Recommendation:**

Use **Option A** (Static DLL Export) because:
- ✅ Guaranteed safe (no conflicts)
- ✅ Easy to access from C++
- ✅ Portable across game versions
- ✅ No risk of overwriting game data

**Complete Implementation:**

```cpp
// src/globals.h
#ifndef GLOBALS_H
#define GLOBALS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Japanese font support
__declspec(dllexport) extern uint8_t g_currentFontPage;

#ifdef __cplusplus
}
#endif

#endif // GLOBALS_H
```

```cpp
// src/common.cpp
#include "globals.h"

uint8_t g_currentFontPage = 0;

// In DllMain or common_init:
void LogGlobalAddresses() {
    ffnx_info("=== FFNx Global Variable Addresses ===\n");
    ffnx_info("g_currentFontPage: 0x%p\n", (void*)&g_currentFontPage);
    ffnx_info("=======================================\n");
    ffnx_info("Use the address above in your Hext patch!\n");
}
```

**Finding the Address at Runtime:**

After compiling and running FFNx, check the log file:

```
FFNx.log:
[INFO] g_currentFontPage: 0x10AB1234
```

Update your Hext patch:

```hext
# Use the logged address
MOV BYTE PTR [0x10AB1234], AL
```

### 8.5 Multi-Language Assembly Hook Extension (Future)

**Objective:** Extend the Assembly hook to support Chinese (0xF0-0xF4) and Korean (0xEB-0xEF) page markers.

**Current Implementation (Japanese Only):**
```
FA-FE → Pages 1-5 (Japanese Kanji)
```

**Extended Implementation (Multi-Language):**
```
FA-FE → Pages 1-5  (Japanese Kanji)
F0-F4 → Pages 6-10 (Chinese Hanzi)
EB-EF → Pages 11-15 (Korean Hangul / Future)
```

**Extended Hext Patch:**

```hext
# misc/hext/ff7/en/FFNx.MULTILANG_FONT.txt

+0x66E272  # Address of text parser (VERIFY FOR YOUR VERSION)

# ================================================================
# MULTI-LANGUAGE FONT PAGE DETECTION
# ================================================================

# Load current byte from text stream
MOV AL, [ESI]

# ---- Check for Japanese Pages (0xFA-0xFE) ----
CMP AL, 0xFA
JB CheckChinese          # Below FA = not Japanese
CMP AL, 0xFE
JA CheckChinese          # Above FE = not Japanese

# Japanese page marker detected
SUB AL, 0xFA             # FA→0, FB→1, FC→2, FD→3, FE→4
INC AL                   # 0→1, 1→2, 2→3, 3→4, 4→5
MOV BYTE PTR [g_currentFontPage], AL
INC ESI                  # Advance to character index
MOV AL, [ESI]            # Load character
JMP ContinueDraw

# ---- Check for Chinese Pages (0xF0-0xF4) ----
CheckChinese:
CMP AL, 0xF0
JB CheckKorean           # Below F0 = not Chinese
CMP AL, 0xF4
JA CheckKorean           # Above F4 = not Chinese

# Chinese page marker detected
SUB AL, 0xF0             # F0→0, F1→1, F2→2, F3→3, F4→4
ADD AL, 6                # 0→6, 1→7, 2→8, 3→9, 4→10
MOV BYTE PTR [g_currentFontPage], AL
INC ESI                  # Advance to character index
MOV AL, [ESI]            # Load character
JMP ContinueDraw

# ---- Check for Korean Pages (0xEB-0xEF) ----
CheckKorean:
CMP AL, 0xEB
JB NormalCharacter       # Below EB = not Korean
CMP AL, 0xEF
JA NormalCharacter       # Above EF = not Korean

# Korean page marker detected
SUB AL, 0xEB             # EB→0, EC→1, ED→2, EE→3, EF→4
ADD AL, 11               # 0→11, 1→12, 2→13, 3→14, 4→15
MOV BYTE PTR [g_currentFontPage], AL
INC ESI                  # Advance to character index
MOV AL, [ESI]            # Load character
JMP ContinueDraw

# ---- Normal Character (Page 0) ----
NormalCharacter:
MOV BYTE PTR [g_currentFontPage], 0
# Continue with original game logic...

ContinueDraw:
# Jump to character drawing routine
JMP 0x66E2B0             # PLACEHOLDER - verify address
```

**Page Allocation Logic:**

| Byte Range | Languages | Page Numbers | Character Sets |
|------------|-----------|--------------|----------------|
| 0x00-0xE6 | All | Page 0 | ASCII, Latin, Hiragana, Katakana |
| 0xFA-0xFE | Japanese | Pages 1-5 | Japanese Kanji (6 pages total) |
| 0xF0-0xF4 | Chinese | Pages 6-10 | Chinese Hanzi (5 pages) |
| 0xEB-0xEF | Korean | Pages 11-15 | Korean Hangul (5 pages) |

**C++ Texture Allocation Update:**

```cpp
// src/common.cpp

uint32_t common_load_texture(...) {
    // ... existing logic ...

    bool is_font_texture = (strstr(filename, "usfont") ||
                           strstr(filename, "jafont") ||
                           strstr(filename, "zhfont") ||
                           strstr(filename, "kofont"));

    if (is_font_texture) {
        // Determine required page count based on language
        uint32_t required_pages = 1;  // Default (English)

        if (font_language == "ja") {
            required_pages = 6;   // Japanese: jafont_1-6
        } else if (font_language == "zh-tw" || font_language == "zh-cn") {
            required_pages = 11;  // Base + 5 Chinese + 5 Japanese (for fallback)
        } else if (font_language == "ko") {
            required_pages = 16;  // Base + 5 Korean + 5 Japanese + 5 Chinese
        } else if (font_language == "multi") {
            required_pages = 16;  // All languages loaded
        }

        // Force allocation
        VRASS(texture_set, ogl.gl_set->textures, required_pages);
        ffnx_info("Allocated %d font texture pages for language: %s\n",
                  required_pages, font_language.c_str());
    }

    // ... rest of loading logic ...
}
```

**Loading Chinese Font Pages:**

```cpp
// src/saveload.cpp

if (font_language == "zh-tw") {
    // Load shared base page (ASCII/Latin/common)
    LoadFontTexture("jafont_1.png", 0);

    // Load Chinese Traditional pages (6-10)
    for (int i = 0; i < 5; i++) {
        char filename[64];
        sprintf(filename, "zhfont_%d.png", i + 1);
        LoadFontTexture(filename, 6 + i);
    }

    ffnx_info("Loaded Chinese Traditional font (6 pages)\n");
}

if (font_language == "ko") {
    // Load shared base
    LoadFontTexture("jafont_1.png", 0);

    // Load Korean pages (11-15)
    for (int i = 0; i < 5; i++) {
        char filename[64];
        sprintf(filename, "kofont_%d.png", i + 1);
        LoadFontTexture(filename, 11 + i);
    }

    ffnx_info("Loaded Korean font (6 pages)\n");
}

if (font_language == "multi") {
    // Load all languages for hot-switching
    // Japanese: pages 0-5
    for (int i = 0; i < 6; i++) {
        char filename[64];
        sprintf(filename, "jafont_%d.png", i + 1);
        LoadFontTexture(filename, i);
    }

    // Chinese: pages 6-10
    for (int i = 0; i < 5; i++) {
        char filename[64];
        sprintf(filename, "zhfont_%d.png", i + 1);
        LoadFontTexture(filename, 6 + i);
    }

    // Korean: pages 11-15
    for (int i = 0; i < 5; i++) {
        char filename[64];
        sprintf(filename, "kofont_%d.png", i + 1);
        LoadFontTexture(filename, 11 + i);
    }

    ffnx_info("Loaded all CJK fonts (16 pages) for multi-language mode\n");
}
```

**Testing Multi-Language Page Switching:**

```cpp
// test/multilang_test.cpp

void test_page_markers() {
    // Test Japanese
    uint8_t ja_stream[] = {0xFA, 0x12, 0xFB, 0x34, 0x00};  // Page 1, Page 2
    parse_text(ja_stream);
    assert(g_currentFontPage == 2);  // Should end on page 2

    // Test Chinese
    uint8_t zh_stream[] = {0xF0, 0x56, 0xF1, 0x78, 0x00};  // Page 6, Page 7
    parse_text(zh_stream);
    assert(g_currentFontPage == 7);  // Should end on page 7

    // Test Korean
    uint8_t ko_stream[] = {0xEB, 0x9A, 0xEC, 0xBC, 0x00};  // Page 11, Page 12
    parse_text(ko_stream);
    assert(g_currentFontPage == 12);  // Should end on page 12

    // Test mixed
    uint8_t mixed[] = {0x41, 0xFA, 0x12, 0xF0, 0x34, 0xEB, 0x56, 0x00};
    // A (page 0), Japanese (page 1), Chinese (page 6), Korean (page 11)
    parse_text(mixed);
    assert(g_currentFontPage == 11);  // Should end on page 11
}
```

**Implementation Priority:**

1. **Phase 1 (Current):** Japanese only (FA-FE)
2. **Phase 2 (Next):** Add Chinese Traditional (F0-F4)
3. **Phase 3 (Future):** Add Korean (EB-EF)
4. **Phase 4 (Advanced):** Multi-language hot-switching

**For Complete Translation Workflow:**
See `reference/MULTI_LANGUAGE_FINDINGS.md` Section 5 for:
- Chinese character encoding examples
- Korean Hangul mapping strategy
- Translation validation tools
- Community crowdsourcing platform

---

## 9. IMPLEMENTATION SPECIFICATION: RENDERER INTEGRATION

### 9.1 Reading the Font Page Variable (src/gl/gl.cpp)

**Objective:** Hook the texture binding logic to read `g_currentFontPage` and bind the correct texture.

**Location: gl_bind_texture_set function**

```cpp
// src/gl/gl.cpp

#include "../globals.h"  // [NEW] For g_currentFontPage

void gl_bind_texture_set(struct texture_set *_texture_set)
{
    // ... existing code ...

    VOBJ(texture_set, texture_set, _texture_set);

    if (!VPTR(texture_set)) {
        return;  // Safety check
    }

    // [NEW] Japanese font page switching logic
    if (font_language == "ja") {
        // Detect if this is a font texture
        // We can check the number of allocated textures (fonts have 6)
        uint32_t num_textures = VREF(texture_set, ogl.gl_set->textures);

        if (num_textures == 6) {
            // This is a Japanese font texture set

            // Read the current page from the global variable
            // (Set by the Assembly hook in the game's text parser)
            uint8_t requested_page = g_currentFontPage;

            // Safety check: clamp to valid range (0-5)
            if (requested_page > 5) {
                ffnx_warning("Invalid font page: %d. Clamping to 5.\n", requested_page);
                requested_page = 5;
            }

            // Override the palette_index with our page index
            VRASS(texture_set, palette_index, requested_page);

            if (trace_all || trace_renderer) {
                ffnx_trace("Binding Japanese font page %d\n", requested_page);
            }

            // Bind the texture for this page
            uint32_t tex_handle = VREF(texture_set, texturehandle[requested_page]);
            if (tex_handle) {
                gl_set_texture(tex_handle, 0);  // 0 = texture unit 0
            } else {
                ffnx_error("Font page %d has NULL texture handle!\n", requested_page);
            }

            // Early return - we've handled this texture
            return;
        }
    }

    // [ORIGINAL] Standard texture binding logic for non-font textures
    uint32_t palette_index = VREF(texture_set, palette_index);
    uint32_t tex_handle = VREF(texture_set, texturehandle[palette_index]);

    if (tex_handle) {
        gl_set_texture(tex_handle, 0);
    }
}
```

**Alternative: More Explicit Detection**

```cpp
// Option: Add a flag to texture_set to mark it as a font
struct texture_set {
    // ... existing fields ...
    bool is_japanese_font;  // [NEW] Flag set during loading
};

// During loading (in load_external_texture):
if (font_language == "ja" && is_font_texture) {
    VRASS(texture_set, is_japanese_font, true);
}

// In gl_bind_texture_set:
if (VREF(texture_set, is_japanese_font)) {
    uint8_t page = g_currentFontPage;
    // ... bind logic ...
}
```

---

### 9.2 Handling Palette Change Events (src/common.cpp)

**Background:**

The game sometimes calls `common_palette_changed` to request a palette swap. For normal textures, this is a color variation. For our fonts, we might receive this call even though we're handling page switching ourselves.

**Location: common_palette_changed function**

```cpp
// src/common.cpp

void common_palette_changed(
    uint32_t new_palette_index,
    struct texture_set* texture_set)
{
    if (!texture_set) return;

    VOBJ(texture_set, tex, texture_set);

    // [NEW] Special handling for Japanese fonts
    if (font_language == "ja") {
        uint32_t num_textures = VREF(tex, ogl.gl_set->textures);

        if (num_textures == 6) {
            // This is a Japanese font - ignore game's palette request
            // because we're controlling pages via g_currentFontPage

            if (trace_all) {
                ffnx_trace("Ignoring palette change for Japanese font (controlled by g_currentFontPage)\n");
            }

            return;  // Don't process this request
        }
    }

    // [ORIGINAL] Standard palette change logic
    if (new_palette_index >= VREF(tex, ogl.gl_set->textures)) {
        ffnx_warning("Palette index %d out of range (max: %d)\n",
                     new_palette_index, VREF(tex, ogl.gl_set->textures) - 1);
        return;
    }

    VRASS(tex, palette_index, new_palette_index);

    // Rebind texture
    gl_bind_texture_set(texture_set);
}
```

---

### 9.3 Rendering Pipeline Integration (src/gl/gl.cpp)

**Understanding the Draw Call Flow:**

```
Game requests character draw
    ↓
gl_draw_indexed_primitive(vertices, texture_set)
    ↓
gl_bind_texture_set(texture_set)  ← We hook here
    ↓
gl_set_texture(handle, unit)
    ↓
BGFX Draw Call
    ↓
GPU renders character
```

**Location: gl_draw_indexed_primitive function**

Add diagnostic logging (optional, for debugging):

```cpp
// src/gl/gl.cpp

void gl_draw_indexed_primitive(
    uint32_t primitivetype,
    uint32_t vertexcount,
    uint32_t indexcount,
    struct nvertex *vertices,
    uint16_t *indices,
    struct graphics_object *graphics_object)
{
    // ... existing code ...

    // [NEW] Font-specific logging (enable only during debugging)
    #ifdef DEBUG_JAPANESE_FONTS
    if (font_language == "ja" && current_state.texture_set) {
        uint32_t num_tex = VREF(current_state.texture_set, ogl.gl_set->textures);
        if (num_tex == 6) {
            ffnx_trace("Drawing Japanese font character:\n");
            ffnx_trace("  Current page: %d\n", g_currentFontPage);
            ffnx_trace("  Vertex count: %d\n", vertexcount);
            ffnx_trace("  Texture handle: 0x%X\n",
                       VREF(current_state.texture_set,
                            texturehandle[g_currentFontPage]));
        }
    }
    #endif

    // ... rest of draw logic ...
}
```

**Compile-time Debug Flag:**

```cpp
// src/globals.h

// Uncomment to enable verbose Japanese font debugging
// #define DEBUG_JAPANESE_FONTS
```

---

## 10. ADVANCED FEATURE: FURIGANA SUPPORT

**⚠️ NOTE:** This section is for **Phase 2** implementation. Complete and test the core Japanese rendering first.

### 10.1 The Furigana Challenge

**What is Furigana?**

Furigana (振り仮名) are small Hiragana characters placed above (or beside) Kanji to indicate pronunciation. This is critical for language learners.

**Example:**
```
    わたし
私
("watashi" = "I/me")
```

**The Problem:**

FF7's text boxes are designed for **3 lines of 16px text** with **no vertical spacing**:

```
┌──────────────────┐
│ Line 1: 16px     │  ← No space above
│ Line 2: 16px     │
│ Line 3: 16px     │
└──────────────────┘
```

If we render Furigana above Kanji, it will **overlap the previous line**:

```
┌──────────────────┐
│ Previous line    │
│ ふりがな ← Overlap!
│ 振り仮名         │
└──────────────────┘
```

---

### 10.2 Solution Strategy: The "Half-Height" Renderer

**Approach:**

1. Define a new control code: `0xF9` = Furigana Marker
2. Format: `0xF9 [Kanji] [Furigana]`
3. Modify renderer to:
   - Draw Kanji at normal size
   - Draw Furigana at **half size** (8px tall)
   - Position Furigana **above** the Kanji (Y offset: -10px)

**Data Format:**

```
Text stream: 0xF9 0xFA 0x12 0x41 0x42 0x43 0x00

Decoding:
  0xF9         = Furigana marker
  0xFA 0x12    = Kanji character (page 1, index 0x12) = 必
  0x41         = Furigana char 1 (page 0, index 0x41) = ひ
  0x42         = Furigana char 2 (page 0, index 0x42) = つ
  0x43         = Furigana char 3 (page 0, index 0x43) = よう
  0x00         = End marker

Result:
    ひつよう
    必
```

---

### 10.3 Assembly Hook Extension (Hext Patch)

**Extend misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt:**

```hext
# ... existing FA-FE check ...

# [NEW] Check for Furigana marker (0xF9)
CMP AL, 0xF9
JNE NotFurigana

# ---- Furigana Mode ----

# Set Furigana mode flag
MOV BYTE PTR [g_furiganaMode], 1  # Enable flag

# Load Kanji character (next byte)
INC ESI
MOV AL, [ESI]

# Draw the Kanji at normal size
CALL DrawCharacter

# Now draw Furigana characters (small, above)
FuriganaLoop:
    INC ESI
    MOV AL, [ESI]

    # Check for end marker (0x00)
    CMP AL, 0x00
    JE EndFurigana

    # Draw Furigana character (renderer will handle sizing)
    CALL DrawCharacter

    JMP FuriganaLoop

EndFurigana:
    # Disable Furigana mode
    MOV BYTE PTR [g_furiganaMode], 0

    JMP ContinueNormal

NotFurigana:
    # ... existing normal character logic ...
```

**New Global Variable:**

```cpp
// src/globals.h
extern "C" __declspec(dllexport) uint8_t g_furiganaMode;

// src/common.cpp
uint8_t g_furiganaMode = 0;
```

---

### 10.4 Renderer Modification (src/gl/gl.cpp)

**Location: gl_draw_indexed_primitive**

```cpp
// src/gl/gl.cpp

void gl_draw_indexed_primitive(
    uint32_t primitivetype,
    uint32_t vertexcount,
    uint32_t indexcount,
    struct nvertex *vertices,
    uint16_t *indices,
    struct graphics_object *graphics_object)
{
    // ... existing setup code ...

    // [NEW] Furigana geometry modification
    if (font_enable_furigana && g_furiganaMode) {
        // We're drawing a Furigana character

        if (trace_all) {
            ffnx_trace("Rendering Furigana character\n");
        }

        // Modify vertices BEFORE submitting to GPU
        for (uint32_t i = 0; i < vertexcount; i++) {
            // Original vertex data:
            float x = vertices[i]._.x;
            float y = vertices[i]._.y;
            float z = vertices[i]._.z;

            // 1. Scale down to 50% (half width, half height)
            float center_x = (vertices[0]._.x + vertices[2]._.x) / 2.0f;
            float center_y = (vertices[0]._.y + vertices[2]._.y) / 2.0f;

            vertices[i]._.x = center_x + (x - center_x) * 0.5f;
            vertices[i]._.y = center_y + (y - center_y) * 0.5f;

            // 2. Shift UP by 10 pixels (to position above Kanji)
            // Note: Adjust multiplier based on rendering resolution
            float y_offset = -10.0f * newRenderer.getScalingFactor();
            vertices[i]._.y += y_offset;
        }
    }

    // ... existing draw call submission ...
}
```

**Scaling Factor Calculation:**

```cpp
// src/renderer.cpp (or renderer.h)

float Renderer::getScalingFactor() {
    // Original FF7 resolution: 640x480
    // If rendering at 1920x1080, scaling factor = 1920/640 = 3.0

    float scale_x = (float)window_width / 640.0f;
    float scale_y = (float)window_height / 480.0f;

    // Use the average to maintain aspect ratio
    return (scale_x + scale_y) / 2.0f;
}
```

---

### 10.5 Line Height Patch (The Hard Part)

**Objective:** Increase vertical spacing between text lines to prevent Furigana overlap.

**Finding the Line Height Variable:**

**Step 1: Memory Search (Cheat Engine)**

1. Open Cheat Engine, attach to FF7 process
2. Search for: **Unknown initial value** (4-byte integer)
3. In-game: Open a menu with text
4. Search for: **Changed value**
5. In-game: Close menu
6. Search for: **Unchanged value**
7. Repeat until you have 1-5 candidates
8. Look for value `16` (0x10) or `24` (0x18)

**Step 2: Verify the Address**

```cpp
// Test by modifying the value
DWORD* line_height_ptr = (DWORD*)0xABCD1234;  // Your found address
*line_height_ptr = 24;  // Try 24px spacing

// Check if text boxes now have more spacing
```

**Step 3: Create a Hext Patch**

```hext
# misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt

# [NEW] Line Height Patch
# Location: Address found via Cheat Engine
+0xABCD1234  # REPLACE WITH ACTUAL ADDRESS

# Original value: 16 (0x10)
# New value: 24 (0x18)
=0x18
```

**Or via C++ at Runtime:**

```cpp
// src/ff7/font.cpp

void PatchLineHeightForFurigana() {
    if (!font_enable_furigana) return;

    // Address found via reverse engineering
    // ⚠️ This is version-specific!
    DWORD* line_height = (DWORD*)0xABCD1234;  // PLACEHOLDER

    DWORD oldProtect;
    VirtualProtect(line_height, sizeof(DWORD), PAGE_READWRITE, &oldProtect);

    *line_height = 24;  // Increase from 16 to 24

    VirtualProtect(line_height, sizeof(DWORD), oldProtect, &oldProtect);

    ffnx_info("Line height increased to 24px for Furigana support.\n");
}
```

**Trade-offs:**

| Line Height | Lines per Box | Furigana Support | Notes |
|-------------|---------------|------------------|-------|
| 16px (original) | 3 lines | ❌ Overlap | Standard FF7 |
| 20px | 2-3 lines | ⚠️ Tight fit | Minimal change |
| 24px | 2 lines | ✅ No overlap | **Recommended** |
| 32px | 2 lines | ✅ Generous spacing | May feel too spacious |

**Recommendation:** Use **24px** for a balance between functionality and aesthetic.

---

## 11. TESTING & VERIFICATION PROTOCOL

### 11.1 Unit Test 1: The "Red W" Test (Texture Override Sanity Check)

**Objective:** Verify FFNx's texture override system is working before implementing complex logic.

**Procedure:**

**Step 1: Create Test Texture**

1. Copy `mods/Textures/menu/usfont_h.png` to backup
2. Open in image editor (GIMP, Photoshop, etc.)
3. Find the 'W' character (cell index 0x57 = 87 decimal)
   - Grid position: Row 5, Column 7 (87 = 5*16 + 7)
4. Replace the 'W' with a **solid red square** or a recognizable Kanji (e.g., 私)
5. Save as PNG

**Step 2: Configure FFNx**

```toml
# FFNx.toml
font_language = "en"  # Keep English mode for now
```

**Step 3: Launch Game**

1. Start FF7
2. Enter name selection screen (type "WWW")
3. Or go to menu and look at text containing 'W'

**Expected Results:**

| Condition | Expected | Meaning |
|-----------|----------|---------|
| See red square/Kanji where 'W' should be | ✅ PASS | Texture override works |
| Character appears squashed horizontally | ⚠️ Expected | Geometry patch not applied yet |
| Still see normal 'W' | ❌ FAIL | Texture not loading |
| Game crashes | ❌ FAIL | File format issue |

**Troubleshooting:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| Normal 'W' appears | PNG not found | Check filename, path |
| Crash on load | Invalid PNG | Re-export with correct settings |
| Squashed character | Width table not patched | Expected at this stage |

---

### 11.2 Unit Test 2: Width Table Patch Verification

**Objective:** Verify the geometry patch prevents squashing.

**Procedure:**

**Step 1: Enable Japanese Mode**

```toml
# FFNx.toml
font_language = "ja"
```

**Step 2: Keep Red Test Texture**

- Use the same modified `usfont_h.png` from Test 1

**Step 3: Launch Game**

1. Start FF7
2. Enter name selection
3. Observe the red character

**Expected Results:**

| Observation | Result | Meaning |
|-------------|--------|---------|
| Red character appears **square** (not squashed) | ✅ PASS | Width patch successful |
| ALL English text appears widely spaced | ✅ Expected | All chars now 16px wide |
| Red character still squashed | ❌ FAIL | Patch didn't apply |
| Crash on startup | ❌ FAIL | Memory protection error |

**Diagnostic Checks:**

1. Check `FFNx.log`:
```
[INFO] Patching character width table for Japanese...
[INFO] Width table located at: 0x99DDA8
[INFO] Successfully patched character width table.
```

2. If log shows errors:
```
[ERROR] font_info pointer is NULL!
→ ff7_data() didn't run or version mismatch
```

**Manual Verification (Advanced):**

Use Cheat Engine to inspect memory at `common_externals.font_info`:

```
Address: 0x99DDA8 (US 1.02)
Expected data (hex):
10 10 10 10 10 10 10 10 ... (all 0x10)

Before patch (hex):
04 04 06 08 0A 08 0C 0E ... (variable widths)
```

---

### 11.3 Integration Test 1: Multi-Texture Loading

**Objective:** Verify all 6 font textures load correctly into memory.

**Procedure:**

**Step 1: Prepare Assets**

Place 6 distinct test textures in `mods/Textures/menu/`:

```
jafont_1.png  →  Fill with RED      (Page 0)
jafont_2.png  →  Fill with GREEN    (Page 1 - triggered by 0xFA)
jafont_3.png  →  Fill with BLUE     (Page 2 - triggered by 0xFB)
jafont_4.png  →  Fill with YELLOW   (Page 3 - triggered by 0xFC)
jafont_5.png  →  Fill with MAGENTA  (Page 4 - triggered by 0xFD)
jafont_6.png  →  Fill with CYAN     (Page 5 - triggered by 0xFE)
```

**Step 2: Configure**

```toml
font_language = "ja"
```

**Step 3: Launch and Check Logs**

```
FFNx.log:
[INFO] Japanese font loading initiated for: usfont
[INFO] Loaded Japanese font page 1: mods/Textures/menu/jafont_1.png (1024x1024)
[INFO] Loaded Japanese font page 2: mods/Textures/menu/jafont_2.png (1024x1024)
[INFO] Loaded Japanese font page 3: mods/Textures/menu/jafont_3.png (1024x1024)
[INFO] Loaded Japanese font page 4: mods/Textures/menu/jafont_4.png (1024x1024)
[INFO] Loaded Japanese font page 5: mods/Textures/menu/jafont_5.png (1024x1024)
[INFO] Loaded Japanese font page 6: mods/Textures/menu/jafont_6.png (1024x1024)
[INFO] Successfully loaded all 6 Japanese font pages.
```

**Expected Results:**

| Log Entry | Status | Action if Failed |
|-----------|--------|------------------|
| All 6 pages loaded | ✅ PASS | Proceed to next test |
| "FAILED to load page X" | ❌ FAIL | Check file exists, correct name |
| Crash after page 2 | ❌ FAIL | Allocation override didn't work |
| No log entries | ❌ FAIL | font_language != "ja" or code path not hit |

**Visual Verification:**

At this stage, all text will appear **RED** (Page 0) because the Assembly hook isn't implemented yet. This is expected.

---

### 11.4 Integration Test 2: Page Switching (Assembly Hook Verification)

**Objective:** Verify the Hext patch detects FA-FE codes and switches textures.

**⚠️ REQUIRES:** Hext patch from Section 8.3 applied with correct addresses.

**Procedure:**

**Step 1: Prepare Test Dialogue**

Use **Makou Reactor** or **Hojo** to edit dialogue:

1. Open `flevel.lgp` (field archive)
2. Extract a simple field (e.g., `md1_1` - first reactor)
3. Edit dialogue text to:
   ```
   Normal text FA 00 FB 00 FC 00 00
   ```
   - `FA 00` = First char from Page 1 (GREEN texture)
   - `FB 00` = First char from Page 2 (BLUE texture)
   - `FC 00` = First char from Page 3 (YELLOW texture)
   - `00` = String terminator

**Step 2: Replace Field File**

1. Repack `flevel.lgp` with modified field
2. Place in game directory
3. Or use 7th Heaven to load as mod

**Step 3: Launch and Trigger**

1. Start new game
2. Advance to the modified dialogue
3. Observe character colors

**Expected Results:**

| Visual | Meaning | Status |
|--------|---------|--------|
| See: RED GREEN BLUE YELLOW sequence | ✅ PERFECT | All systems working |
| All characters are RED | ❌ Hook not firing | Check Hext addresses |
| Crash when dialogue appears | ❌ Invalid memory write | Check g_currentFontPage address |
| Random colors | ⚠️ Partial success | Page index calculation error |

**Diagnostic Logging:**

Enable trace mode:

```cpp
// src/gl/gl.cpp
#define DEBUG_JAPANESE_FONTS  // Uncomment

// Check log:
[TRACE] Binding Japanese font page 0
[TRACE] Binding Japanese font page 1  ← Should appear when FA byte is hit
[TRACE] Binding Japanese font page 2  ← Should appear when FB byte is hit
```

**Advanced Debugging:**

Set breakpoint in `gl_bind_texture_set`:

```cpp
if (g_currentFontPage != 0) {
    // Breakpoint here - should hit when FA/FB/FC are encountered
    __debugbreak();
}
```

---

### 11.5 Full System Test: Real Japanese Dialogue

**Objective:** End-to-end verification with actual Japanese text and real font textures.

**Prerequisites:**
- ✅ All previous tests passed
- ✅ Real `jafont_*.png` files installed (not test colors)
- ✅ Japanese dialogue patch applied

**Procedure:**

**Step 1: Install Assets**

1. Replace test textures with actual Japanese font textures
2. Install a Japanese translation mod (or use ff7_ja.exe's text)

**Step 2: Configure for Production**

```toml
font_language = "ja"
font_enable_furigana = false  # Test basic first
```

**Step 3: Play Through a Scene**

1. Start new game
2. Play through first reactor mission
3. Read all dialogue
4. Check menu screens
5. Check battle text

**Verification Checklist:**

| Component | Check | Status |
|-----------|-------|--------|
| **Dialogue** | All Kanji render correctly | ☐ |
| | No squashed characters | ☐ |
| | No missing glyphs (blank squares) | ☐ |
| | Text fits in dialog boxes | ☐ |
| **Menu** | Item names readable | ☐ |
| | Character names correct | ☐ |
| | Status screen displays properly | ☐ |
| **Battle** | Enemy names show | ☐ |
| | Spell names correct | ☐ |
| | Damage numbers work | ☐ |
| **Performance** | No lag during text rendering | ☐ |
| | Smooth scrolling | ☐ |
| **Stability** | No crashes during 30min play | ☐ |
| | No memory leaks (check Task Manager) | ☐ |

**Known Issues to Check:**

| Issue | Cause | Fix |
|-------|-------|-----|
| Some Kanji missing (blank) | Character not in mapping CSV | Add to jafont_*.png |
| Text overflows boxes | Width table too wide | Reduce width or adjust box size |
| Flickering text | Z-fighting | Check depth buffer settings |
| Crash after 10min | Memory leak in loader | Review allocations |

---

### 11.6 Regression Testing

**Objective:** Ensure English mode still works (backward compatibility).

**Procedure:**

**Step 1: Switch to English**

```toml
font_language = "en"
```

**Step 2: Play Original Game**

1. Launch FF7
2. Start new game
3. Play for 15 minutes
4. Test all UI elements

**Expected Behavior:**

| Feature | Expected | Status |
|---------|----------|--------|
| All text is English | ✅ | ☐ |
| No Japanese characters appear | ✅ | ☐ |
| No performance degradation | ✅ | ☐ |
| No crashes | ✅ | ☐ |
| Mods still work (7th Heaven) | ✅ | ☐ |

**⚠️ CRITICAL:** If English mode breaks, the implementation has a logic error. Common causes:

- Width table patched even when `font_language == "en"`
- Texture loader always loads 6 pages
- Assembly hook fires on English text

**Fix:** Add guard clauses:

```cpp
if (font_language != "ja") {
    return;  // Don't patch, use original logic
}
```

---

## 12. RISK MITIGATION & DEBUGGING GUIDE

### 12.1 Common Failure Modes & Solutions

#### Failure Mode #1: Crash on Startup

**Symptoms:**
- Game crashes before reaching title screen
- No FFNx.log created
- Windows error: "ff7.exe has stopped working"

**Diagnostic Steps:**

1. **Check DLL Loading:**
```
Use Dependency Walker (depends.exe):
- Open ff7.exe
- Look for AF3DN.P or FFNx.dll
- Check if all dependencies are satisfied
```

2. **Check Event Viewer:**
```
Windows → Event Viewer → Application
Look for:
- Access Violation (0xC0000005)
- DLL Not Found (0xC0000135)
```

3. **Enable Debug Mode:**
```toml
# FFNx.toml
trace_all = true
trace_loaders = true
```

**Common Causes & Fixes:**

| Cause | Symptom | Fix |
|-------|---------|-----|
| Missing DLL dependencies | Error code 0xC0000135 | Install Visual C++ Redistributable |
| Invalid registry paths | Crash after splash screen | Check `dotemuRegQueryValueExA` logic |
| Memory corruption in DllMain | Instant crash | Remove global initializations from DllMain |
| Conflicting drivers | Random crash | Remove other graphics mods |

---

#### Failure Mode #2: Crash on Menu Open

**Symptoms:**
- Game runs, reaches title screen
- Crashes when entering menu or name selection
- FFNx.log ends abruptly

**Diagnostic Steps:**

1. **Check Last Log Entry:**
```
FFNx.log:
[INFO] Loading texture: usfont
[INFO] Japanese font detected: forcing allocation...
[CRASH] ← Log ends here
```

2. **Check Allocation:**
```cpp
// Add this debug code before crash point:
ffnx_info("Allocated textures: %d\n", VREF(texture_set, ogl.gl_set->textures));
ffnx_info("Texturehandle ptr: 0x%p\n", VREF(texture_set, texturehandle));
```

**Common Causes & Fixes:**

| Cause | Evidence | Fix |
|-------|----------|-----|
| Buffer overflow in texture loading | Crash after "Loading page 3" | Verify 6-slot allocation happened FIRST |
| NULL texture handle access | Crash in `gl_bind_texture_set` | Add null checks before dereferencing |
| Invalid PNG format | Crash in `load_texture_helper` | Re-export PNGs with correct settings |
| Stack overflow (recursion) | Stack trace shows loop | Check for infinite recursion |

**Fix Template:**

```cpp
// BEFORE loading textures
if (!VREF(texture_set, texturehandle)) {
    ffnx_error("Texturehandle array is NULL!\n");
    return 0;
}

uint32_t allocated_slots = VREF(texture_set, ogl.gl_set->textures);
if (allocated_slots < 6) {
    ffnx_error("Not enough slots! Need 6, have %d\n", allocated_slots);
    return 0;
}

// NOW safe to load
for (int i = 0; i < 6; i++) {
    // Load logic...
}
```

---

#### Failure Mode #3: Squashed / Corrupted Text

**Symptoms:**
- Game runs without crashes
- Japanese text appears but is:
  - Horizontally compressed (barcode-like)
  - Vertically stretched
  - Wrong aspect ratio

**Diagnostic:**

1. **Screenshot and Measure:**
   - Take screenshot of squashed character
   - Measure pixel dimensions in image editor
   - Compare to expected 16×16 (or 64×64 in high-res)

2. **Check Width Table:**
```cpp
// Add diagnostic dump
char* table = common_externals.font_info;
for (int i = 0; i < 256; i++) {
    if (table[i] != 0x10) {
        ffnx_warning("Width[0x%02X] = %d (expected 16)\n", i, table[i]);
    }
}
```

**Common Causes:**

| Cause | Check | Fix |
|-------|-------|-----|
| Width patch didn't apply | Log missing "Patched width table" | Verify `PatchFontWidthsForJapanese()` is called |
| Applied to wrong address | Characters still variable width | Use `common_externals.font_info`, not hardcoded |
| VirtualProtect failed | Log shows "VirtualProtect failed" | Run as administrator |
| Wrong executable version | Widths correct for some chars, wrong for others | Confirm EXE version matches address map |

**Forced Diagnostic Mode:**

```cpp
void VerifyWidthPatch() {
    char* table = common_externals.font_info;
    if (!table) {
        MessageBoxA(NULL, "font_info is NULL!", "Error", MB_OK);
        return;
    }

    bool all_16px = true;
    for (int i = 0x20; i < 0x100; i++) {
        if (table[i] != 0x10) {
            all_16px = false;
            break;
        }
    }

    if (all_16px) {
        MessageBoxA(NULL, "Width patch SUCCESS!", "Info", MB_OK);
    } else {
        MessageBoxA(NULL, "Width patch FAILED!", "Error", MB_OK);
    }
}
```

---

#### Failure Mode #4: Wrong Texture Displayed

**Symptoms:**
- Text appears but with wrong characters
- FA codes show Page 0 characters instead of Page 1
- Random texture pages displayed

**Diagnostic:**

1. **Check g_currentFontPage Value:**
```cpp
// In gl_bind_texture_set
ffnx_info("g_currentFontPage = %d\n", g_currentFontPage);
ffnx_info("Expected page for 0xFA = 1\n");
```

2. **Verify Assembly Hook:**
```
Use debugger:
- Set breakpoint at Hext injection address
- Input text with 0xFA byte
- Check if breakpoint hits
- Verify AL register = 0xFA
- Step through and watch g_currentFontPage change
```

**Common Causes:**

| Cause | Evidence | Fix |
|-------|-------|-----|
| Hext patch wrong address | Breakpoint never hits | Re-find address with debugger |
| Math error in hook | g_currentFontPage = wrong value | Check SUB/INC logic |
| Hook not reading g_currentFontPage | Always shows Page 0 | Verify address in `MOV [addr], AL` |
| Race condition | Flickers between pages | Add synchronization |

**Correct Page Calculation:**

```assembly
; When AL = 0xFA:
SUB AL, 0xFA    ; AL = 0xFA - 0xFA = 0x00
INC AL          ; AL = 0x00 + 1 = 0x01 ✅
                ; g_currentFontPage = 1 (correct for Page 1)

; When AL = 0xFE:
SUB AL, 0xFA    ; AL = 0xFE - 0xFA = 0x04
INC AL          ; AL = 0x04 + 1 = 0x05 ✅
                ; g_currentFontPage = 5 (correct for Page 5)
```

**If Pages are Off by One:**

```assembly
; WRONG version (missing INC):
SUB AL, 0xFA
; AL = 0 for FA, but we want page 1!

; CORRECT:
SUB AL, 0xFA
INC AL          ; ← Don't forget this!
```

---

### 12.2 Memory Debugging Tools

**Tool 1: Cheat Engine**

```
Download: https://cheatengine.org/

Usage for Finding Addresses:
1. Attach to ff7.exe
2. Search: "Unknown initial value" (4-byte)
3. Modify game state (open menu)
4. Search: "Changed value"
5. Repeat until 1-5 candidates
6. Right-click → "Find out what accesses this address"
7. Trigger action → See backtrace
```

**Tool 2: x64dbg**

```
Download: https://x64dbg.com/

Usage for Assembly Debugging:
1. Open ff7.exe
2. Ctrl+G → Enter address (e.g., 0x66E2A0)
3. Set breakpoint (F2)
4. Run (F9)
5. When hit, examine:
   - Registers (AL, ESI, EBP)
   - Stack
   - Memory at ESI (string pointer)
6. Step instruction by instruction (F7)
```

**Tool 3: API Monitor**

```
Download: http://www.rohitab.com/apimonitor

Usage for Registry Call Debugging:
1. Launch API Monitor
2. Select: Kernel32.dll → Registry functions
3. Monitor ff7.exe
4. See all RegQueryValueEx calls
5. Verify our dotemuRegQueryValueExA is called
6. Check returned paths
```

**Tool 4: Process Monitor (ProcMon)**

```
Download: https://docs.microsoft.com/sysinternals

Usage for File Access Debugging:
1. Run ProcMon as admin
2. Filter: Process Name is ff7.exe
3. Filter: Operation contains "Open" or "Read"
4. Start game
5. See exactly which files are requested
6. Check if jfleve.lgp vs flevel.lgp
```

---

### 12.3 Debugging Checklist

When something goes wrong, work through this checklist systematically:

**Phase 1: Environment Verification**

- [ ] FFNx installed correctly (AF3DN.P in game directory)
- [ ] FFNx.log is being created
- [ ] Config file (FFNx.toml) is readable
- [ ] `font_language` is set correctly
- [ ] Font textures exist in `mods/Textures/menu/`
- [ ] File permissions are correct (not read-only)

**Phase 2: Initialization Verification**

- [ ] DllMain executed (check log for "FFNx initialized")
- [ ] `is_using_japanese_exe` detected correctly
- [ ] `read_cfg()` parsed settings (check log)
- [ ] Registry hooks returning correct paths (check log)
- [ ] `ff7_data()` completed (common_externals populated)

**Phase 3: Texture Loading Verification**

- [ ] `common_load_texture` called for font
- [ ] 6 texture slots allocated (check log)
- [ ] All 6 PNGs loaded successfully (check log)
- [ ] Texture handles are non-zero
- [ ] No errors in FFNx.log

**Phase 4: Geometry Verification**

- [ ] `PatchFontWidthsForJapanese()` called
- [ ] `common_externals.font_info` is not NULL
- [ ] VirtualProtect succeeded
- [ ] Width table contains all 0x10 values
- [ ] Log shows "patched successfully"

**Phase 5: Assembly Hook Verification**

- [ ] Hext patch file exists in correct location
- [ ] Addresses in Hext match executable version
- [ ] `g_currentFontPage` address is correct
- [ ] Breakpoint at hook location hits
- [ ] `g_currentFontPage` changes when FA byte is encountered

**Phase 6: Renderer Verification**

- [ ] `gl_bind_texture_set` detects Japanese font (6 textures)
- [ ] Reads `g_currentFontPage` correctly
- [ ] Binds correct texture handle
- [ ] Draw call succeeds
- [ ] Character appears on screen

**Phase 7: Runtime Verification**

- [ ] No memory leaks (check Task Manager over time)
- [ ] No crashes after 30 minutes
- [ ] Performance is acceptable
- [ ] All text systems work (menu, dialogue, battle)

---

### 12.4 Performance Profiling

**Measuring Overhead:**

```cpp
// src/gl/gl.cpp

#include <chrono>

void gl_bind_texture_set(struct texture_set *_texture_set) {
    auto start = std::chrono::high_resolution_clock::now();

    // ... existing logic ...

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    if (duration.count() > 100) {  // Flag if > 100 microseconds
        ffnx_warning("Slow texture bind: %lld μs\n", duration.count());
    }
}
```

**Expected Performance:**

| Operation | Target Time | Acceptable Limit |
|-----------|-------------|------------------|
| Texture bind | < 50 μs | < 100 μs |
| Width table patch | < 1 ms | < 5 ms |
| Texture loading (all 6) | < 500 ms | < 1000 ms |
| Per-character draw | < 100 μs | < 500 μs |

**If Performance is Poor:**

1. **Profile the Bottleneck:**
   - Add timing to each function
   - Identify slowest operation

2. **Common Optimizations:**
   - Cache texture handles (don't reload every frame)
   - Use texture atlases (already done via 6 pages)
   - Reduce logging in release builds
   - Use faster PNG decoder

3. **Release vs Debug:**
```cpp
#ifdef _DEBUG
    // Extensive logging, validation
#else
    // Minimal logging, skip checks
#endif
```

---

## 13. DEPLOYMENT CHECKLIST

### 13.1 Pre-Release Validation

Before distributing to users, complete this checklist:

**Code Quality:**

- [ ] All debug logging is disabled or conditional
- [ ] No hardcoded addresses (use `common_externals`)
- [ ] No placeholder memory addresses (0xCC0000 replaced)
- [ ] Error handling for all file operations
- [ ] Memory leaks checked (Valgrind / Dr. Memory)
- [ ] Code reviewed for security issues
- [ ] Comments explain complex logic
- [ ] Version number updated

**Functionality:**

- [ ] English mode tested and working
- [ ] Japanese mode tested with real textures
- [ ] ff7_en.exe compatibility verified
- [ ] ff7_ja.exe compatibility verified (if supporting)
- [ ] Steam version tested
- [ ] All font pages load correctly
- [ ] Page switching works (FA-FE codes)
- [ ] Character widths correct (no squashing)
- [ ] No crashes in 1-hour play session

**Assets:**

- [ ] All 6 jafont_*.png files prepared
- [ ] Correct resolution (1024×1024)
- [ ] Correct grid layout (16×16)
- [ ] All required characters mapped
- [ ] ff7_complete_mapping_compact.csv up to date
- [ ] Assets tested in-game
- [ ] File sizes reasonable (< 1MB each)

**Documentation:**

- [ ] Installation guide written
- [ ] Configuration guide (FFNx.toml settings)
- [ ] Troubleshooting section
- [ ] Credits and attribution
- [ ] License information (MIT for FFNx)
- [ ] Known issues documented

**Distribution Package:**

- [ ] FFNx.dll compiled (Release mode)
- [ ] All 6 font textures included
- [ ] Example FFNx.toml with Japanese settings
- [ ] README.md with installation steps
- [ ] CHANGELOG.md with version history
- [ ] LICENSE file
- [ ] Optional: Installer script (batch file)

---

### 13.2 User Installation Guide Template

Create a `README.md` for users:

```markdown
# FFNx Japanese Language Support

Native Japanese text rendering for Final Fantasy VII (PC).

## Installation

1. **Install FFNx** (if not already installed):
   - Download from: https://github.com/julianxhokaxhiu/FFNx
   - Follow FFNx installation instructions

2. **Install Japanese Font Mod**:
   - Extract this archive to your FF7 directory
   - Files should be placed in:
     - `mods/Textures/menu/jafont_1.png`
     - `mods/Textures/menu/jafont_2.png`
     - (etc.)

3. **Configure FFNx**:
   - Open `FFNx.toml` in a text editor
   - Find the line: `font_language = "en"`
   - Change to: `font_language = "ja"`
   - Save and close

4. **Install Japanese Text** (optional):
   - Use 7th Heaven to install a Japanese translation mod
   - OR use the original Japanese executable (ff7_ja.exe)

## Troubleshooting

**Issue: Text appears squashed**
- Solution: Ensure `font_language = "ja"` in FFNx.toml
- Restart the game after changing settings

**Issue: Blank boxes instead of Kanji**
- Solution: Verify all 6 jafont_*.png files are in the correct folder
- Check FFNx.log for "Failed to load" errors

**Issue: Game crashes on menu open**
- Solution: Re-extract the mod files
- Ensure you're using FFNx version 1.X or later
- Check for conflicting mods

## Credits

- FFNx: Julian Xhokaxhiu and contributors
- Japanese Font Textures: [Your Name]
- Character Mapping: [Contributors]

## License

This mod is released under [License]. FFNx is licensed under MIT.
```

---

### 13.3 7th Heaven .iro Package Creation

**For Distribution via 7th Heaven:**

**Step 1: Create Mod Structure**

```
MyJapaneseFontMod/
├── info.json
├── mod.xml
└── assets/
    └── menu/
        ├── jafont_1.png
        ├── jafont_2.png
        ├── jafont_3.png
        ├── jafont_4.png
        ├── jafont_5.png
        └── jafont_6.png
```

**Step 2: Create info.json**

```json
{
  "ID": "japanese-font-support",
  "Name": "Japanese Font Support",
  "Author": "Your Name",
  "Version": "1.0.0",
  "Description": "Native Japanese text rendering with 6 high-resolution font pages. Requires FFNx.",
  "Category": "Fonts",
  "ReleaseDate": "2025-11-24",
  "Tags": ["Japanese", "Fonts", "FFNx"],
  "CompatibleGameVersions": ["1.02 US", "Steam 2013"],
  "RequiredMods": ["FFNx"]
}
```

**Step 3: Create mod.xml**

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModConfig>
  <ID>japanese-font-support</ID>
  <Name>Japanese Font Support</Name>
  <Files>
    <File>
      <Source>assets/menu/jafont_1.png</Source>
      <Destination>mods/Textures/menu/jafont_1.png</Destination>
    </File>
    <File>
      <Source>assets/menu/jafont_2.png</Source>
      <Destination>mods/Textures/menu/jafont_2.png</Destination>
    </File>
    <!-- Repeat for all 6 files -->
  </Files>
  <ConfigOptions>
    <Option name="font_language" value="ja" description="Enable Japanese language mode in FFNx.toml" />
  </ConfigOptions>
</ModConfig>
```

**Step 4: Package as .iro**

```batch
7z a -tzip MyJapaneseFontMod.iro *
ren MyJapaneseFontMod.zip MyJapaneseFontMod.iro
```

**Step 5: Test in 7th Heaven**

1. Open 7th Heaven
2. Library → Import Mod
3. Select your .iro file
4. Enable the mod
5. Launch game and test

---

## 14. REFERENCE MATERIALS & APPENDICES

### 14.1 Complete Memory Map (US 1.02)

**⚠️ WARNING: These addresses are ONLY for FF7 US 1.02. Other versions differ!**

| Address | Size | Type | Description |
|---------|------|------|-------------|
| `0x99DDA8` | 256 bytes | `char[]` | Character width table |
| `0x99DCA8` | 4 bytes | `uint32_t` | Current text color |
| `0x66E272` | Function | Code | `draw_graphics_object` (approximation) |
| `0x66E2A0` | Function | Code | Character processing loop (approximation) |
| `0xCC0000` | N/A | ❌ INVALID | PLACEHOLDER - do not use |

**How to Find Addresses for Other Versions:**

See Section 8.2 for detailed instructions.

---

### 14.2 Character Encoding Reference

**Single-Byte Characters (Page 0 / jafont_1):**

| Range | Content |
|-------|---------|
| `0x00` | Space character |
| `0x01-0x5F` | ASCII printable (offset by 0x20 from standard ASCII) |
| `0x60-0x9F` | Extended Latin (accented chars: Ä, Á, Ç, É, etc.) |
| `0xA0-0xCF` | Symbols and special characters |
| `0xD0-0xD3` | Additional special chars |
| `0xD4-0xDF` | **UNUSED** - produces graphical errors |
| `0xE0` | {Choice} - menu selection indent |
| `0xE1` | {Tab} - 4-space indent |
| `0xE2-0xE6` | Shortcut sequences (comma-space, period-quote, etc.) |
| `0xE7` | {EOL} - End of line / line break |
| `0xE8-0xE9` | {New Screen} - advance to next dialog window |
| `0xEA` | {Cloud} - insert Cloud's current name |
| `0xEB` | {Barret} - insert Barret's current name |
| `0xEC` | {Tifa} - insert Tifa's current name |
| `0xED` | {Aerith} - insert Aerith's current name |
| `0xEE` | {Red XIII} - insert Red XIII's current name |
| `0xEF` | {Yuffie} - insert Yuffie's current name |
| `0xF0` | {Cait Sith} - insert Cait Sith's current name |
| `0xF1` | {Vincent} - insert Vincent's current name |
| `0xF2` | {Cid} - insert Cid's current name |
| `0xF3` | {Party #1} - insert party slot 1 name |
| `0xF4` | {Party #2} - insert party slot 2 name |
| `0xF5` | {Party #3} - insert party slot 3 name |
| `0xF6` | 〇 (Circle button) |
| `0xF7` | △ (Triangle button) |
| `0xF8` | ☐ (Square button) |
| `0xF9` | ✕ (Cross button) |
| `0xFA` | Page 1 marker (jafont_2) |
| `0xFB` | Page 2 marker (jafont_3) |
| `0xFC` | Page 3 marker (jafont_4) |
| `0xFD` | Page 4 marker (jafont_5) |
| `0xFE` | {FUNC} opcode - see below |
| `0xFF` | {END} - string terminator |

**FE Function Opcodes (Two-Byte Sequences):**

| Code | Function | Notes |
|------|----------|-------|
| `FE 00`-`FE D1` | **Japanese extended chars** | Maps to jafont_6 (Japanese version only) |
| `FE D2` | Color: Gray | Subsequent text until next color code |
| `FE D3` | Color: Blue | Subsequent text until next color code |
| `FE D4` | Color: Red | Subsequent text until next color code |
| `FE D5` | Color: Purple | Subsequent text until next color code |
| `FE D6` | Color: Green | Subsequent text until next color code |
| `FE D7` | Color: Cyan | Subsequent text until next color code |
| `FE D8` | Color: Yellow | Subsequent text until next color code |
| `FE D9` | Color: White | Reset to default |
| `FE DA` | Color: **Flash** | ⚠️ Global - cycles on/off, cannot reset |
| `FE DB` | Color: **Rainbow** | ⚠️ Global - animated cycling colors |
| `FE DC` | Wait for OK button | Pause text until player input |
| `FE DD XX XX` | Timed pause | Wait XX frames (little-endian) |
| `FE DE` | Variable (numeric) | Insert numeric variable from memory bank |
| `FE DF` | Variable (hex) | Insert hex variable from memory bank |
| `FE E0` | Scroll text | Enable text scrolling mode |
| `FE E1` | Variable (spaced) | Insert variable with space padding |
| `FE E2` | Memory string | Copy string from memory address |
| `FE E9` | Max letter width | Set maximum character width |
| `FE FF` | Wait for OK | Same as FE DC |

**Battle Text Special Codes:**

| Code | Function | Notes |
|------|----------|-------|
| `EA` | Character name | Insert attacker/target name |
| `EB` | Item name | Insert item name by index |
| `EC` | Number | Insert numeric value |
| `ED` | Target name | Insert target's name |
| `EF` | Attack name | Insert attack/ability name |
| `F0` | Target letter | For multi-target enemies (A, B, C) |
| `F8 XX` | Box color | XX=02 for red (Limit Break) box |
| `F9 XX` | LZS reference | Compressed text backreference |

**Two-Byte Sequences (Pages 1-5):**

| First Byte | Second Byte | Meaning |
|------------|-------------|---------|
| `0xFA` | `0x00-0xFF` | Character from jafont_2.png (index 0-255) |
| `0xFB` | `0x00-0xFF` | Character from jafont_3.png (index 0-255) |
| `0xFC` | `0x00-0xFF` | Character from jafont_4.png (index 0-255) |
| `0xFD` | `0x00-0xFF` | Character from jafont_5.png (index 0-255) |
| `0xFE` | `0x00-0xFF` | Character from jafont_6.png (index 0-255) |

**Example Encoding:**

```
Japanese text: "こんにちは" (Konnichiwa / Hello)
Assuming mapping:
  こ = jafont_1, index 0x3A
  ん = jafont_1, index 0x3B
  に = jafont_1, index 0x3C
  ち = jafont_1, index 0x3D
  は = jafont_1, index 0x3E

Encoded bytes: 0x3A 0x3B 0x3C 0x3D 0x3E 0x00
               (All on Page 0, so no FA prefix needed)

Japanese text: "魔法" (Mahou / Magic)
Assuming mapping:
  魔 = jafont_2, index 0x10
  法 = jafont_2, index 0x11

Encoded bytes: 0xFA 0x10 0xFA 0x11 0x00
               (FA = switch to Page 1, then char index)
```

---

### 14.3 FFNx Configuration Reference

**Complete FFNx.toml Settings for Japanese:**

```toml
###############################################################################
# FFNx Configuration File
###############################################################################

# ===========================
# Japanese Language Support
# ===========================

# Font language mode
# Values: "en" (English), "ja" (Japanese)
# Default: "en"
font_language = "ja"

# Enable Furigana (reading guides above Kanji)
# Requires: Furigana-enabled font textures
# Default: false
font_enable_furigana = false

# Custom font texture path
# Leave empty to use default: mods/Textures/menu/
# Example: "mods/CustomFonts/ja/"
# Default: ""
font_path_override = ""

# ===========================
# Related Settings
# ===========================

# Texture dumping (for mod creation)
save_textures = false

# Trace logging (debugging only)
trace_all = false
trace_renderer = false
trace_loaders = false

# Window mode
fullscreen = false
window_size_x = 1280
window_size_y = 960

# Rendering backend
renderer_backend = "auto"  # auto, OpenGL, DirectX11, Vulkan

# ===========================
# Advanced
# ===========================

# Use external textures from mods folder
use_external_textures = true

# Mod path (where mods/Textures/ is located)
mod_path = "mods/Textures"
```

---

### 14.4 File Format Specifications

**PNG Requirements for Font Textures:**

| Property | Value | Notes |
|----------|-------|-------|
| Resolution | 1024×1024 | Enforced by FFNx |
| Color Mode | RGBA | 32-bit with alpha |
| Bit Depth | 8 bits per channel | Total 32 bpp |
| Compression | PNG (lossless) | No JPEG |
| Interlacing | None | Optional but not needed |
| Grid Layout | 16×16 cells | 256 total cells |
| Cell Size | 64×64 pixels | Per glyph |
| Alpha Channel | Required | For anti-aliasing edges |

**Exporting from Image Editors:**

**Photoshop:**
```
File → Export → Export As...
Format: PNG
Transparency: Checked
Interlaced: Unchecked
```

**GIMP:**
```
File → Export As...
Select file type: PNG
Compression level: 9 (maximum)
Save background color: No
Save gamma: No
Interlacing: None
```

**Aseprite:**
```
File → Export...
Format: PNG
Color: RGBA (32-bit)
Scale: 1x
```

---

### 14.5 FFNx Macro System (Critical for Development)

FFNx uses custom macros for safe struct field access through virtual table indirection. **These are mandatory when working with game engine structs.**

| Macro | Purpose | Example |
|-------|---------|---------|
| `VREF(ptr, field)` | Read field value | `uint32_t tex = VREF(texture_set, texturehandle[0]);` |
| `VRASS(ptr, field, val)` | Write field value | `VRASS(texture_set, texturehandle[0], new_tex);` |
| `VREFP(ptr, field)` | Get field pointer | `uint32_t* p = VREFP(texture_set, texturehandle);` |

**CRITICAL:** Never access `texture_set` fields directly - the struct uses virtual table indirection:

```cpp
// ❌ WRONG (will crash or corrupt memory)
texture_set->texturehandle[0] = tex;

// ✅ CORRECT (uses proper indirection)
VRASS(texture_set, texturehandle[0], tex);
```

**Why This Exists:**
- FF7's game engine uses non-standard struct layouts
- Virtual table indirection allows FFNx to intercept field access
- Direct access bypasses FFNx's interception layer, causing crashes

**When Working with FFNx Code:**
- Always grep for existing usage patterns before writing new code
- If you see `VREF`/`VRASS` used for a struct, use them consistently
- Applies to: `texture_set`, `tex_header`, `driver_state`, and other game engine structs

---

### 14.6 Glossary

| Term | Definition |
|------|------------|
| **AF3DN.P** | Square Enix's proprietary graphics driver for FF7 PC |
| **BGFX** | Cross-platform graphics library used by FFNx |
| **Character Width Table** | In-memory array defining pixel width of each character |
| **FA-FE Encoding** | Custom 2-byte system using 0xFA-0xFE as page markers |
| **FFNx** | Open-source graphics driver replacement for FF7/FF8 |
| **Furigana** | Small Hiragana placed above Kanji to show pronunciation |
| **Glyph** | Visual representation of a single character |
| **Hext** | System for applying in-memory assembly patches at runtime |
| **LGP** | Square Enix's archive format (.lgp files) |
| **Palette Index** | Number determining which texture variant to use |
| **Texture Set** | FFNx struct holding multiple texture handles |
| **UV Coordinates** | Texture mapping coordinates (U=horizontal, V=vertical) |

---

### 14.7 Tool Ecosystem & Workflow

**Complete Tool Comparison:**

| Tool | Format | Language | Status | Best For | Availability |
|------|--------|----------|--------|----------|--------------|
| **TexTools v1.0.4.7** | TEX↔PNG/JPG/GIF/BMP/TIFF | Windows GUI | Pre-compiled ✅ | **Recommended** - Easiest for users | qhimm.com forums |
| **Image2TEX** | TEX↔BMP/JPG/GIF batch | VB.NET | Source only ⚠️ | Batch conversion (if compiled) | GitHub: niemasd/Image2TEX |
| **tim2png** | TIM→PNG | Python | Ready ✅ | PSX assets only | GitHub: cebix/ff7tools |
| **TEX to BMP (Pascal)** | TEX→BMP | Pascal | Code example 📖 | Educational reference | Gist: hoehrmann/5720668 |
| **ulgp v1.2** | LGP extract/pack | C++ | Pre-compiled ✅ | **Critical** - Archive management | Dropbox (qhimm) |

**Additional Tools:**

| Tool | Purpose | URL |
|------|---------|-----|
| **Makou Reactor** | Field script editor (Japanese support) | qhimm.com |
| **WallMarket v1.4.5** | KERNEL.BIN editor | qhimm.com |
| **Proud Clod** | scene.bin (battle) editor | qhimm.com |
| **touphScript 1.5.0** | UTF-8 text dump/restore | GitHub |
| **7th Heaven** | Mod manager + VFS | 7thheaven.rocks |
| **Cheat Engine** | Memory debugger | cheatengine.org |
| **x64dbg** | Assembly debugger | x64dbg.com |

**Recommended Workflow:**

```
Phase 1: Asset Extraction
├─ ulgp -x menu_ja.lgp           → Extract Japanese font archives
└─ Result: jafont_1.tex through jafont_6.tex

Phase 2: Format Conversion
├─ TexTools: Open jafont_1.tex   → Convert TEX to PNG
├─ Export as PNG (1024×1024)
└─ Result: jafont_1.png through jafont_6.png

Phase 3: Editing (Optional)
├─ GIMP/Photoshop: Edit PNGs     → Customize glyphs
└─ Maintain: 1024×1024, 16×16 grid, 64×64 cells

Phase 4: Testing
├─ Place in: mods/Textures/menu/
├─ Configure: FFNx.toml (font_language = "ja")
└─ Launch: FF7 + FFNx

Phase 5: Distribution
├─ Create: 7th Heaven .iro package
└─ OR: Distribute as loose PNG files with instructions
```

**Performance Notes:**
- **DDS format**: 40-70% faster loading than PNG (advanced users)
- **PNG format**: Universal compatibility (recommended for distribution)
- TexTools supports both formats

**Community Resources:**

| Resource | Description |
|----------|-------------|
| Qhimm Forums | FF7 modding community hub |
| FFNx Discord | Real-time support |
| FF7 Wiki | Game engine documentation |
| GitHub Issues | Bug tracking and features |

---

### 14.8 Version History

**Document Changelog:**

| Version | Date | Changes |
|---------|------|---------|
| 4.1 | 2025-11-25 | Added Section 1.7 (PR #737 Improvements), Section 14.5 (VREF/VRASS Macros) |
| 4.0 | 2025-11-24 | Ultimate consolidated spec with all clarifications |
| 3.0 | 2025-11-20 | Added implementation details and debugging guide |
| 2.0 | 2025-11-15 | Integrated AF3DN analysis findings |
| 1.0 | 2025-11-10 | Initial specification |

---

## FINAL IMPLEMENTATION CHECKLIST

**Use this checklist to track your implementation progress:**

### Phase 1: Foundation (Core C++)
- [ ] Configuration added (cfg.h, cfg.cpp)
- [ ] Global variables defined (globals.h, common.cpp)
- [ ] Registry hooks updated (common.cpp - dotemuRegQueryValueExA)
- [ ] Texture allocation override (common.cpp - common_load_texture)
- [ ] Multi-page loader (saveload.cpp - load_external_texture)
- [ ] File redirection (redirect.cpp - Japanese archive variants)
- [ ] Width table patch (ff7/font.cpp, ff7/font.h)
- [ ] Width patch called in init (ff7_opengl.cpp)

### Phase 2: Assembly & Renderer
- [ ] g_currentFontPage allocated (globals.h, common.cpp)
- [ ] Hext patch created (misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt)
- [ ] Addresses verified with debugger
- [ ] Renderer hook (gl/gl.cpp - gl_bind_texture_set)
- [ ] Palette change handler (common.cpp - common_palette_changed)

### Phase 3: Assets & Testing
- [ ] All 6 jafont_*.png textures created
- [ ] Character mapping CSV complete
- [ ] Unit Test 1: Red W Test (PASS)
- [ ] Unit Test 2: Width Patch (PASS)
- [ ] Integration Test 1: Multi-texture load (PASS)
- [ ] Integration Test 2: Page switching (PASS)
- [ ] Full System Test: Real Japanese dialogue (PASS)
- [ ] Regression Test: English mode still works (PASS)

### Phase 4: Advanced Features (Optional)
- [ ] Furigana opcode (0xF9) implemented
- [ ] Furigana renderer hook
- [ ] Line height patch applied
- [ ] Furigana testing complete

### Phase 5: Deployment
- [ ] All debug code removed/disabled
- [ ] Performance verified
- [ ] Documentation written
- [ ] .iro package created
- [ ] User installation guide
- [ ] Released to community

---

## APPENDIX A: FFNX TEXTURE OVERRIDE VALIDATION

**Date**: 2025-11-20 13:30:13 JST (Session 10)
**Status**: ✅ PROOF OF CONCEPT ACHIEVED

### Overview

This appendix documents the critical validation that FFNx's texture override system works for font textures. This proof-of-concept test confirms the entire approach is viable before investing in full implementation.

---

### FFNx Texture Pipeline Architecture

**FFNx implements a 3-layer texture system:**

1. **Renderer Interception Layer**
   - Intercepts DirectX/OpenGL texture loading calls
   - Hooks into game engine's texture request pipeline
   - Transparent to FF7 executable

2. **Hash/Identification Layer**
   - Uses **filename-based matching** on dumped textures (not hash-based)
   - Filenames created by `save_textures = true` ARE the correct ones for replacements
   - No manual hash calculation required

3. **Override Injection Layer**
   - Swaps low-res game textures for high-res modded versions
   - Handles format conversion (game internal → PNG/DDS)
   - Zero game code modification required

---

### Validation Test Results

**Test Method:**
1. Enable `save_textures = true` in FFNx.toml
2. Run FF7 to trigger texture dumping
3. FFNx creates actual game textures in `mods/Textures/menu/`
4. Edit dumped textures directly (change to red color)
5. Disable `save_textures = false` to stop overwriting edits
6. Run FF7 - modified textures load successfully!

**Files Tested:**
- `usfont_a_h_14.png` (high-res variant A)
- `usfont_a_l_14.png` (low-res variant A)
- `usfont_b_h_14.png` (high-res variant B)
- `usfont_b_l_14.png` (low-res variant B)

**Result:** ✅ **Menu text appeared RED** - Texture override confirmed working!

---

### Critical Discoveries

1. **No Manual TEX Conversion Needed**
   - FFNx's `save_textures` feature exports PNG directly
   - No need for LGP extraction or TEX format tools
   - Workflow is much simpler than initially thought

2. **Filename-Based Matching**
   - FFNx uses dumped filenames for override matching
   - Not hash-based like Tonberry (FF8 tool)
   - Makes testing and iteration much faster

3. **No IRO Complexity for Testing**
   - Direct file editing in `mods/Textures/` works
   - IRO packaging only needed for distribution
   - Faster development cycle

4. **Format Conversion Handled Automatically**
   - FFNx converts game internal formats → PNG
   - Supports both PNG and DDS for overrides
   - No custom conversion tools required

5. **Entire Pipeline is Functional**
   - Renderer hooks working
   - Texture loading working
   - Override injection working
   - End-to-end system validated

---

### What This Validates for Japanese Implementation

**Confirmed Working:**
- ✅ Texture replacement mechanism functional
- ✅ Font textures can be overridden
- ✅ Multiple font variants supported (a_h, a_l, b_h, b_l)
- ✅ No game executable modification required
- ✅ FFNx pipeline ready for 6-texture Japanese system

**Implementation Path Validated:**
1. Extract jafont_1-6.tex from AF3DN.P or menu_ja.lgp
2. Convert to PNG using FFNx dumping or tools
3. Place in `mods/Textures/menu/` with correct filenames
4. Implement FA-FE page marker system in FFNx driver
5. Test Japanese text rendering
6. Package as IRO for 7th Heaven distribution

**Remaining Challenges** (NOT texture-related):
- Character encoding (FA-FE extended pages) - requires C++ implementation
- Texture grid mapping - algorithm for character→pixel position
- Game data modification - kernel/WINDOW.BIN for encoding support
- Language switching - runtime language selection mechanism

---

### Technical Implications

**For This Implementation:**

This validation confirms we can focus on the **hard problems**:
- C++ driver code for multi-texture font system
- FA-FE page marker decoding logic
- Character→glyph position mapping

**We do NOT need to solve:**
- ❌ Texture file format conversion (FFNx handles it)
- ❌ LGP archive manipulation (FFNx loads from mods/)
- ❌ Hash-based texture identification (filename matching works)
- ❌ Game executable patching for texture loading (FFNx intercepts)

**Development Velocity Impact:**

Before validation: Unsure if approach is viable, might need Plan B/C/D
After validation: Core mechanism proven, can proceed with confidence

---

### Reference: Validation Test Procedure

Full test procedure documented in:
`/docs/TEST_PROCEDURE.md` - Phase 2 "FFNx Texture Dumping (THE WORKING METHOD)"

**Session Documentation:**
- Session ID: 77121986-7211-4ef5-a043-d61a47fa6f66
- Date: 2025-11-20
- Result: Proof of concept successful

---

## CONCLUSION

This document provides everything needed to implement native Japanese text rendering in Final Fantasy VII via the FFNx driver. The system is:

- ✅ **Production-proven** (based on Square Enix's AF3DN.P architecture)
- ✅ **Legally sound** (clean-room reimplementation)
- ✅ **Community-friendly** (open source, MIT licensed)
- ✅ **Future-proof** (extensible for multi-language, Furigana, etc.)
- ✅ **Backward compatible** (English mode unaffected)

**Success Criteria:**
- Japanese characters render correctly (no squashing)
- All 6 font pages load and switch dynamically
- No crashes or memory corruption
- Performance overhead < 5%
- Works with both ff7_en.exe and ff7_ja.exe

**Developer Support:**

If you encounter issues during implementation:

1. **Check FFNx.log** - Most issues are logged with clear errors
2. **Use debugger** - Verify addresses and logic flow
3. **Consult this document** - All known issues documented
4. **Community support** - Qhimm Forums, FFNx Discord
5. **GitHub Issues** - Report bugs to FFNx repository

**Good luck with your implementation!**

---

**Document End**

*This is version 4.0 of the FFNx Japanese Implementation Master Bible.*
*For updates and corrections, visit: [Your Project URL]*
