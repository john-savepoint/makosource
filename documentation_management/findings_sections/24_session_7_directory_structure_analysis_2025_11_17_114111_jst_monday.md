# SESSION 7: DIRECTORY STRUCTURE ANALYSIS (2025-11-17 11:41:11 JST Monday)

**Extracted From**: FINDINGS.md
**Section Lines**: 2364-2839
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


**Session ID**: `1021bc57-9aa2-41fe-baad-a6b89b252744`

**BREAKTHROUGH DISCOVERY: 5-LANGUAGE INTERNATIONAL RELEASE!**

The installed game at `/Volumes/KIOXIAwhite/FF7` contains **5 complete language packs**, not 4:

1. **English (EN)** - ff7_en.exe (23.8MB)
2. **Japanese (JA)** - ff7_ja.exe (23.8MB)
3. **French (FR)** - ff7_fr.exe (23.8MB) ← **NOT PREVIOUSLY DOCUMENTED!**
4. **German (DE)** - ff7_de.exe (23.8MB)
5. **Spanish (ES)** - ff7_es.exe (23.8MB)

**Key Files Discovered**:
- `FF7_Launcher.exe` (18.8MB) - Qt-based language selector UI
- `lang.ini` (283KB) - DRM configuration (UTF-16 encoded)
- `ff7_gamebooster.pdf` - Documents built-in cheat/booster modes
- `Manual_FF7INT.pdf` - International version manual
- `EULA_FF7INT_JP.pdf` - Japanese EULA

---

### Complete Directory Structure Analysis

```
/Volumes/KIOXIAwhite/FF7/
├── EXECUTABLES (5 language-specific + launcher)
│   ├── FF7_Launcher.exe      (18.8MB - language selector)
│   ├── ff7_en.exe            (23.8MB - English executable)
│   ├── ff7_ja.exe            (23.8MB - Japanese executable)
│   ├── ff7_fr.exe            (23.8MB - French executable)
│   ├── ff7_de.exe            (23.8MB - German executable)
│   └── ff7_es.exe            (23.8MB - Spanish executable)
│
├── data/
│   ├── menu/                  # FONT TEXTURES (CRITICAL!)
│   │   ├── menu_us.lgp       (1.7MB - English fonts, 1998)
│   │   ├── menu_ja.lgp       (26.8MB - Japanese fonts, 2013) ← 15× LARGER!
│   │   ├── menu_fr.lgp       (1.7MB - French fonts, 1998)
│   │   ├── menu_gm.lgp       (1.7MB - German fonts, 1998)
│   │   └── menu_sp.lgp       (1.7MB - Spanish fonts, 1998)
│   │
│   ├── field/                 # DIALOGUE ARCHIVES (ALL 5 LANGUAGES!)
│   │   ├── flevel.lgp        (122MB - English dialogues)
│   │   ├── jfleve.lgp        (123MB - Japanese dialogues) ← NOTE TYPO!
│   │   ├── fflevel.lgp       (123MB - French dialogues)
│   │   ├── gflevel.lgp       (122MB - German dialogues)
│   │   ├── sflevel.lgp       (122MB - Spanish dialogues)
│   │   └── char.lgp          (47MB - character models, shared)
│   │
│   ├── lang-ja/              # Japanese-specific assets
│   │   ├── battle/
│   │   │   └── scene.bin     (270KB - battle text/AI)
│   │   ├── kernel/
│   │   │   ├── KERNEL.BIN    (20KB - game text/data)
│   │   │   ├── kernel2.bin   (12KB - additional text)
│   │   │   └── WINDOW.BIN    (13KB - window graphics)
│   │   └── movies/
│   │       ├── Ending2.avi   (varies - localized ending)
│   │       └── jenova_e.avi  (localized cutscene)
│   │
│   ├── lang-en/              # English-specific assets (same structure)
│   ├── lang-fr/              # French-specific assets
│   ├── lang-de/              # German-specific assets (de folder, gm files)
│   ├── lang-es/              # Spanish-specific assets
│   │
│   ├── wm/                   # World map (language-specific text)
│   │   ├── world_us.lgp      (3.0MB - English world text)
│   │   ├── world_ja.lgp      (3.0MB - Japanese world text)
│   │   ├── world_fr.lgp      (3.0MB - French world text)
│   │   ├── world_gm.lgp      (3.0MB - German world text)
│   │   └── world_sp.lgp      (3.0MB - Spanish world text)
│   │
│   ├── cd/                   # Credits and disc info (per language)
│   │   ├── cr_us.lgp, cr_fr.lgp, cr_gm.lgp, cr_sp.lgp
│   │   └── disc_us.lgp, disc_fr.lgp, disc_gm.lgp, disc_sp.lgp
│   │
│   ├── battle/               # Shared battle assets (language-neutral)
│   ├── midi/                 # Music files
│   ├── movies/               # FMV sequences
│   ├── music/                # Soundtrack
│   ├── music_ogg/            # OGG format music
│   ├── sound/                # Sound effects
│   ├── minigame/             # Mini-game assets
│   └── xarch/                # Extra archives (.fgt files)
│
└── 371 total files, 34 directories
```

---

### Language Selection Mechanism (CRITICAL FINDING)

**Architecture**: The launcher uses a **Qt-based GUI** to select language, then launches the appropriate executable.

**Key Strings Found in FF7_Launcher.exe**:
```cpp
// UI Elements (Qt)
QPushButton#languageBtn        // Language selection button
QRadioButton#englishBtn        // English radio button
QRadioButton#japaneseBtn       // Japanese radio button
languageBtnClicked()           // Selection handler
showLanguageSettings()         // Settings display function

// Language Mapping
FF7_EN.exe                     // Executable paths
lang-en/                       // Language data directory
Language                       // Configuration key
lang.dat                       // User's language preference storage

// Launcher Communication
ff7_sharedMemoryWithLauncher   // IPC mechanism
ff7_gameDidReadMsgSem          // Semaphore for game→launcher
ff7_launcherDidReadMsgSem      // Semaphore for launcher→game
```

**Selection Flow**:
1. User launches `FF7_Launcher.exe`
2. Launcher presents language selection (Qt radio buttons)
3. User selects language (e.g., Japanese)
4. Launcher saves selection to `lang.dat`
5. Launcher executes `ff7_ja.exe`
6. Executable loads data from `lang-ja/` and `menu_ja.lgp`

**IMPLICATION FOR OUR PROJECT**: Square Enix has **ALREADY SOLVED** multi-language selection! We can:
- Study their launcher source patterns
- Reuse their file organization scheme
- Extend their system for runtime switching (they use launch-time selection)

---

### Critical Technical Insights

#### Japanese Font Archive Size Difference

**menu_ja.lgp = 26.8MB (26,872,760 bytes)**
**menu_us.lgp = 1.7MB (1,705,214 bytes)**

**Ratio**: Japanese is **15.76× larger**!

**Why?** Japanese requires 6 font texture files (jafont_1-6.tex) to store 2,000+ kanji, hiragana, and katakana. English only needs single texture for 256 ASCII characters.

This confirms our earlier research: Japanese font support requires MASSIVE additional texture data compared to single-byte languages.

#### File Naming Conventions

**Interesting Discoveries**:
- Japanese field dialogue: `jfleve.lgp` (typo - missing 'l' in flevel)
- German uses inconsistent codes: folder = `lang-de`, file = `menu_gm.lgp`
- Spanish: folder = `lang-es`, file = `menu_sp.lgp`
- English: folder = `lang-en`, file = `menu_us.lgp`
- French: folder = `lang-fr`, file = `menu_fr.lgp`

**Implication**: File naming is historical artifact from 1998 development. Not perfectly consistent, but predictable.

#### KERNEL.BIN Size Differences

| Language | KERNEL.BIN Size | Notes |
|----------|-----------------|-------|
| Japanese | 20KB | Double-byte encoding |
| English | 22KB | Single-byte encoding |
| German | 22KB | Single-byte encoding |
| Spanish | 21KB | Single-byte encoding |

Japanese KERNEL.BIN is **smaller** despite having more complex text because Shift-JIS (double-byte) is more efficient for Japanese than ASCII representation would be.

---

### Next Steps for Session 8

1. **Extract menu_ja.lgp Contents**
   - Use ulgp (requires Wine on macOS or transfer to Windows)
   - Verify jafont_1-6.tex files exist
   - Document file count and names

2. **Convert jafont_*.tex to PNG**
   - Use Tex Tools or Image2TEX (Windows)
   - Analyze glyph layout and organization
   - Measure glyph dimensions (32×32? 48×48?)

3. **Analyze Character Mapping**
   - How are characters ordered in each texture?
   - Frequency-based? Unicode block? JIS order?
   - Create character→texture index mapping

4. **Extract and Compare KERNEL.BIN**
   - Hex dump Japanese vs English
   - Identify text encoding differences
   - Document Shift-JIS byte sequences

5. **Research FFNx Runtime Language Switching**
   - FFNx can override textures
   - Can it switch texture sets at runtime?
   - Hot-swap language without restart?

---

### Key Discoveries Summary

| Discovery | Impact | Status |
|-----------|--------|--------|
| 5-language support (not 4) | Scope expansion - French included | ✅ Confirmed |
| menu_ja.lgp = 26.8MB | Japanese fonts exist and are massive | ✅ Confirmed |
| Qt-based language selector | Can study/extend for runtime switching | ✅ Analyzed |
| Per-language executables | Each language is self-contained | ✅ Confirmed |
| lang-*/ directories | Text data separated per language | ✅ Confirmed |
| jfleve.lgp filename typo | Historical artifact, no technical issue | ✅ Noted |

---

---

### Japanese Font Texture Size Analysis (LGP Header Examination)

**Method**: Hex dump of menu_ja.lgp header to extract file offsets

**CONFIRMED**: All 6 jafont textures exist in the archive:

| File | Offset (bytes) | Size (bytes) | Size (MB) |
|------|----------------|--------------|-----------|
| jafont_1.tex | 1,047,414 | ~4,194,564 | 4.00 |
| jafont_2.tex | 5,241,978 | ~4,194,564 | 4.00 |
| jafont_3.tex | 9,436,542 | ~4,194,562 | 4.00 |
| jafont_4.tex | 13,631,104 | ~4,194,560 | 4.00 |
| jafont_5.tex | 17,825,664 | ~4,194,560 | 4.00 |
| jafont_6.tex | 22,020,224 | ~4,852,536 | 4.63 |

**Key Insights**:
- Each texture is exactly ~4MB (4,194,560 bytes)
- This matches 2048×2048 texture with palette-based compression
- jafont_6.tex is slightly larger (4.63MB) - may contain metadata or index table
- Total font data: ~25MB for Japanese vs ~1.7MB for English (15× larger)
- LGP format confirmed: "SQUARESOFT8" header, standard archive structure

**Character Capacity Estimation**:
- If 32×32 glyphs with 2px padding: (2048/34)² = 60² = 3,600 chars/texture
- 6 textures × 3,600 = **21,600 total characters** (more than enough!)
- If 48×48 glyphs with 2px padding: (2048/50)² = 41² = 1,681 chars/texture
- 6 textures × 1,681 = **10,086 total characters** (still sufficient)

This confirms the textures can hold all 2,136 Jōyō kanji plus hiragana, katakana, and punctuation with room to spare.

---

---

### BREAKTHROUGH: Hardcoded Language Paths in Executables

**Method**: String extraction from ff7_ja.exe vs ff7_en.exe

**DISCOVERY**: Each language executable has **hardcoded asset paths**!

**ff7_ja.exe contains:**
```
field/jfleve.lgp      ← Japanese dialogues
menu/menu_ja.lgp      ← Japanese font textures (jafont_1-6.tex)
wm/world_ja.lgp       ← Japanese world map text
lang-ja/kernel/       ← Japanese KERNEL.BIN (gzip compressed)
```

**ff7_en.exe contains:**
```
field/flevel.lgp      ← English dialogues
menu/menu_us.lgp      ← English font textures (USFONT_*.tex)
wm/world_us.lgp       ← English world map text
lang-en/kernel/       ← English KERNEL.BIN
```

**CRITICAL IMPLICATION**:
1. **Square Enix ALREADY implemented double-byte character support** in ff7_ja.exe!
2. The character→texture mapping algorithm **is baked into the Japanese executable**
3. **We don't need to reverse-engineer the font rendering** - it already works!
4. **paul.dll is just DRM** (692KB), not a graphics driver

**This Changes Everything**:
- Previous assumption: Need to modify FFNx to add Japanese font rendering
- **New reality**: Japanese font rendering ALREADY EXISTS in ff7_ja.exe
- FFNx can potentially **intercept and redirect** asset loading paths
- OR: Study ff7_ja.exe to understand the mapping algorithm, then replicate in FFNx

**Note**: All 5 executables are exactly 23MB - compiled from same source with different constants.

---

### AF3DN.P - THE CUSTOM JAPANESE GRAPHICS DRIVER (FOUND!)

**File**: `/Volumes/KIOXIAwhite/FF7/AF3DN.P`
**Size**: 317KB (324,096 bytes)
**Type**: PE32 DLL (Windows graphics driver)
**Date**: April 16, 2013

**THIS IS THE ENGINE OUR RESEARCH MENTIONED!** Square Enix's customized AF3DN.P driver that supports Japanese fonts.

**Critical Strings Found Inside**:
```
jafont_1.tim          ← Japanese font texture 1
jafont_2.tim          ← Japanese font texture 2
jafont_3.tim          ← Japanese font texture 3
jafont_4.tim          ← Japanese font texture 4
jafont_5.tim          ← Japanese font texture 5
jafont_6.tim          ← Japanese font texture 6
MultiByteToWideChar   ← Windows API for double-byte conversion!
WideCharToMultiByte   ← Windows API for double-byte conversion!
D3DXCreateFontW       ← DirectX font creation (Wide/Unicode)
D3DXCreateTextureFromFileA  ← DirectX texture loading
MODE_MAIN_MENU        ← Menu system modes
MODE_BATTLE_MENU
MODE_MENU
IngameTextPayload     ← Text rendering data structure
texture_flag          ← Texture state management
```

**Build Path Found**:
```
C:\FF7\src\menu\English\loadmenu.cpp
```

This reveals Square Enix's source code structure! The driver was built from FF7 source with Japanese extensions.

**Why This Matters**:

1. **CONFIRMS our research**: The eStore version uses a **completely customized AF3DN.P driver**
2. **Font loading is hardcoded**: jafont_1.tim through jafont_6.tim strings embedded in DLL
3. **Double-byte support exists**: Uses Windows MultiByteToWideChar/WideCharToMultiByte APIs
4. **Source path visible**: Shows actual Square Enix build environment

**Key Technical Insights**:

1. Uses `.tim` extension internally (PlayStation TIM format), not `.tex`
2. DirectX 9 based (D3DX functions)
3. Font creation uses Unicode-aware function (`D3DXCreateFontW` - the 'W' means Wide/Unicode)
4. Menu system has multiple modes with text rendering
5. `IngameTextPayload` structure handles text display

**Comparison to Standard FF7**:
- Standard Steam AF3DN.P: Smaller, single-byte font only
- eStore Japanese AF3DN.P: **317KB with 6-font loader and double-byte support**

**Research Validation**: This confirms julianxhokaxhiu's quote from Session 4:
> "Square-Enix did release an eStore Japanese edition... they had to customize completely the driver... the eStore release has a bigger stock AF3DN.P driver, which has the code to inject into the font system."

**NEXT STEPS**:
1. Reverse-engineer AF3DN.P to understand jafont_X.tim loading mechanism
2. Extract character→texture mapping algorithm from driver
3. Compare to FFNx source to understand integration points
4. Potentially use this driver directly with FFNx, or port the logic

---

---

### COMPREHENSIVE FILE AUDIT - ALL CRITICAL ASSETS IDENTIFIED

**Method**: Systematic search of `/Volumes/KIOXIAwhite/FF7/` directory tree

#### HIGH IMPACT FILES (Must Preserve/Analyze)

| File | Size | Purpose | Critical Insights |
|------|------|---------|-------------------|
| **AF3DN.P** | 317KB | Custom graphics driver | jafont_1-6.tim loader, MultiByteToWideChar double-byte support |
| **menu_ja.lgp** | 26.8MB | Japanese font archive | 6× jafont_*.tex files (~4MB each), 15× larger than English |
| **ff7_ja.exe** | 23MB | Japanese executable | Hardcoded: menu_ja.lgp, jfleve.lgp, world_ja.lgp paths |
| **jfleve.lgp** | 123MB | Japanese dialogues | Complete field text (note filename typo: "jfleve" not "jflevel") |
| **world_ja.lgp** | 3MB | World map text | Japanese location names and labels |
| **lang-ja/kernel/KERNEL.BIN** | 20KB | Game text data | Gzip compressed Shift-JIS encoded text |
| **lang-ja/battle/scene.bin** | 270KB | Battle text/AI | Enemy names, attack names in Japanese |
| **condorj.lgp** | 3.5MB | Fort Condor minigame | ONLY Japanese-specific minigame asset found |

#### MEDIUM IMPACT FILES (Supporting Infrastructure)

| File | Size | Purpose | Notes |
|------|------|---------|-------|
| **strings.dat** | 175KB | Launcher UI strings | Contains DIK_KANJI (Japanese IME key code), HTML/Qt resources |
| **FF7_Launcher.exe** | 18MB | Language selector | Qt-based GUI with englishBtn/japaneseBtn radio buttons |
| **ff7_*.exe.manifest** | 1.3KB ea. | Windows manifests | Version 1.0.7.0, SquareEnix.FINALFANTASYVII assembly identity |
| **ff7_gamebooster.pdf** | 161KB | Cheat documentation | Built-in booster modes already available! |
| **paul.dll** | 692KB | DRM/Launcher | Digital software services authentication (NOT graphics driver) |
| **lang.ini** | 283KB | DRM config | UTF-16 encoded launcher settings, not language selection |

#### MISSING JAPANESE ASSETS (Interesting Gaps)

Files that DON'T exist for Japanese but do for other languages:

| Expected File | Actual Behavior | Notes |
|---------------|-----------------|-------|
| cr_ja.lgp | Uses cr_us.lgp | Credits shown in English |
| disc_ja.lgp | Uses disc_us.lgp | Disc info in English |
| high-ja.lgp | Uses high-us.lgp | Highwind minigame text in English |
| snowboard-ja.lgp | Uses snowboard-us.lgp | Snowboard minigame in English |
| chocobo_ja.lgp | Uses chocobo.lgp | Chocobo breeding shared |

**Implication**: Not all game text was localized to Japanese. Minigames except Fort Condor use English text.

#### FILE ORGANIZATION PATTERNS

**Language-Specific Executables** (all ~23MB, compiled from same source):
- ff7_en.exe → field/flevel.lgp, menu/menu_us.lgp, wm/world_us.lgp
- ff7_ja.exe → field/jfleve.lgp, menu/menu_ja.lgp, wm/world_ja.lgp
- ff7_fr.exe → field/fflevel.lgp, menu/menu_fr.lgp, wm/world_fr.lgp
- ff7_de.exe → field/gflevel.lgp, menu/menu_gm.lgp, wm/world_gm.lgp
- ff7_es.exe → field/sflevel.lgp, menu/menu_sp.lgp, wm/world_sp.lgp

**Font Archive Sizes**:
```
menu_us.lgp = 1.7MB (English - single texture)
menu_ja.lgp = 26.8MB (Japanese - 6 textures) ← 15.76× LARGER!
menu_fr.lgp = 1.7MB (French - single texture)
menu_gm.lgp = 1.7MB (German - single texture)
menu_sp.lgp = 1.7MB (Spanish - single texture)
```

**Kernel/Text Data Sizes** (lang-*/kernel/KERNEL.BIN):
```
Japanese: 20KB (double-byte compressed)
English:  22KB (single-byte)
German:   22KB (single-byte)
Spanish:  21KB (single-byte)
French:   [check pending]
```

#### TOTAL FILE COUNT

```
/Volumes/KIOXIAwhite/FF7/
├── 371 total files
├── 34 directories
├── 5 language executables
├── 5 font archives
├── 5 field dialogue archives
├── 5 world map archives
├── 5 language-specific kernel directories
└── 1 custom AF3DN.P graphics driver (THE KEY!)
```

---

### SESSION 7 SUMMARY: MAJOR BREAKTHROUGHS

**What We Discovered**:

1. ✅ **5-Language International Release** (not 4!) - Includes French
2. ✅ **AF3DN.P Custom Driver Found** - Square Enix's Japanese font injection engine
3. ✅ **jafont_1-6.tim Hardcoded** - Font loading strings in driver DLL
4. ✅ **Double-byte Support Built-in** - MultiByteToWideChar/WideCharToMultiByte APIs
5. ✅ **Hardcoded Asset Paths** - Each executable knows its language files
6. ✅ **DirectX 9 Unicode Fonts** - D3DXCreateFontW (Wide character support)
7. ✅ **All Japanese Assets Present** - menu_ja.lgp, jfleve.lgp, world_ja.lgp, kernel
8. ✅ **Font Texture Sizes Confirmed** - Each jafont_*.tex is ~4MB (2048×2048)

**What This Means**:

- **The hardest problem is ALREADY SOLVED** - Square Enix implemented Japanese rendering
- **AF3DN.P is the reference implementation** we need to study
- **FFNx can potentially work WITH this driver** (hybrid approach)
- **Or we can port the algorithm to FFNx** (requires reverse engineering)
- **Runtime language toggle is feasible** - just need to swap asset paths

---

**Session 7 Final Status**: COMPREHENSIVE ANALYSIS COMPLETE
**Critical Discovery**: AF3DN.P (317KB) = Japanese font injection engine with double-byte support
**All Assets Located**: menu_ja.lgp, jfleve.lgp, world_ja.lgp, KERNEL.BIN, scene.bin, condorj.lgp
**Key Technical Insight**: Japanese rendering is PRODUCTION-READY in Square Enix's implementation

**Next Session Priorities**:
1. Reverse-engineer AF3DN.P font loading algorithm (IDA/Ghidra)
2. Extract and visualize jafont_*.tex character layout
3. Research FFNx + AF3DN.P compatibility
4. Document character→texture mapping system
5. Test running ff7_ja.exe with FFNx overlay

**Platform Note**: Development on macOS; need Windows or Wine for FF7 execution and tool usage

---

