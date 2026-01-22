# Session Handoff: FFNx PR #737 Japanese Text Implementation

**Created:** 2025-11-26 23:08 JST (Wednesday)
**Session ID:** b8a3e4e3-a694-4e65-84d3-f0ce749f7998
**Author:** Claude Code (Opus 4.5)
**Purpose:** Complete context handoff for next agent to continue Japanese text implementation

---

## Executive Summary

This session achieved a **major breakthrough**: We successfully built FFNx PR #737 from source and got the **first-ever Japanese text rendering working in FF7 on the English version** (`ff7_en.exe`). Battle text, item names, and kernel-based text render correctly in Japanese. However, **field dialogue appears as garbled hiragana/katakana** because while we're loading the Japanese field file (`jfleve.lgp`), the text data pipeline has an encoding interpretation issue.

---

## What Was Accomplished

### 1. FFNx PR #737 Built from Source
- **Location:** `C:\FFNx\`
- **Branch:** PR #737 (japanese text support branch)
- **Build Output:** `C:\FFNx\.build\Release\FFNx.dll`
- **Auto-deploys to:**
  - `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\` (as `AF3DN.P`)
  - `C:\Games\Final Fantasy VII\`

### 2. Custom Modification: LGP File Redirection
We added code to redirect `flevel.lgp` → `jfleve.lgp` when Japanese mode is enabled.

**File Modified:** `C:\FFNx\src\ff7\file.cpp`

**Change Made (lines 31-67):**
```cpp
FILE *open_lgp_file(char *filename, uint32_t mode)
{
    char _filename[260]{ 0 };
    if(trace_all || trace_files) ffnx_trace("opening lgp file %s\n", filename);

    // Japanese edition: redirect flevel.lgp to jfleve.lgp
    if (ff7_japanese_edition && strstr(filename, "flevel.lgp") != NULL)
    {
        // Build path to jfleve.lgp in the same directory
        strcpy(_filename, filename);
        char* pos = strstr(_filename, "flevel.lgp");
        if (pos != NULL)
        {
            strcpy(pos, "jfleve.lgp");
            if (trace_all || trace_files) ffnx_trace("Japanese redirect: %s -> %s\n", filename, _filename);

            FILE* fd = fopen(_filename, "rb");
            if (fd != NULL)
            {
                ffnx_info("Successfully redirected to Japanese field file: %s\n", _filename);
                return fd;
            }
            else
            {
                ffnx_warning("Japanese field file not found: %s, falling back to original\n", _filename);
            }
        }
    }

    int redirect_status = attempt_redirection(filename, _filename, sizeof(_filename));

    if (redirect_status == -1)
    {
        strcpy(_filename, filename);
    }

    return fopen(_filename, "rb");
}
```

**Also added include (line 29):**
```cpp
#include "../globals.h"
```

### 3. Japanese Assets Deployed
Files copied to Steam FF7 installation:

**Kernel files (`data/kernel/`):**
- `kernel.bin` (20K)
- `kernel2.bin` (12K)
- `window.bin` (13K)

**Field file (`data/field/`):**
- `jfleve.lgp` (129MB) - Japanese field dialogue archive

**Font textures (`direct/menu/`):**
- `jafont_1.tex` through `jafont_6.tex` (4.2MB each)
- `jafont_1.png` through `jafont_6.png` (296K-472K each)

**Lang-ja structure (`data/lang-ja/`):**
- `battle/` - Japanese battle data (scene.bin, camdat*.bin, co.bin)
- `kernel/` - Japanese kernel files
- `field/` - (created but may not be needed)

### 4. FFNx.toml Configuration
Located at: `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.toml`

**Critical setting:**
```toml
ff7_japanese_edition = true
```

---

## Current State

### What Works ✅
1. **Japanese font textures load** - TEX files in `direct/menu/` are found
2. **Kernel text renders correctly** - Battle menus, item names, spell names
3. **`jfleve.lgp` loads successfully** - FFNx.log confirms: "Successfully redirected to Japanese field file"
4. **Japanese text rendering hooks active** - PR #737's FA-FE encoding handlers are registered

### What Doesn't Work ❌
1. **Field dialogue is garbled** - Shows random hiragana/katakana instead of actual Japanese sentences
2. **Menu text partially broken** - Some menu text shows same garbled pattern

### FFNx Log Evidence
```
[00000001] INFO: Successfully redirected to Japanese field file: C:\...\data\field/jfleve.lgp
```

No font loading errors. The file redirection works.

---

## Root Cause Analysis

### The Problem
The English executable (`ff7_en.exe`) and Japanese executable (`ff7_ja.exe`) interpret text data differently at a fundamental level.

**Japanese text encoding in `jfleve.lgp`:**
- Single-byte characters (0x00-0xF9): Map to `jafont_1` positions
- FA XX: Two-byte sequence, character at `jafont_2` position XX
- FB XX: Two-byte sequence, character at `jafont_3` position XX
- FC XX: Two-byte sequence, character at `jafont_4` position XX
- FD XX: Two-byte sequence, character at `jafont_5` position XX
- FE XX: Two-byte sequence, character at `jafont_6` position XX
- FF: End of text marker

**What PR #737 provides:**
- FA-FE handling in the **rendering** functions (lines 514-553 of `japanese_text.cpp`)
- Loads all 6 jafont textures
- Character width tables for proper spacing

**What PR #737 assumes:**
- The text data arriving at render functions is **already correctly parsed** by `ff7_ja.exe`
- The Japanese executable natively understands FA-FE encoding

**The gap:**
- `ff7_en.exe` text parser doesn't understand FA-FE encoding
- Text bytes are misinterpreted BEFORE reaching PR #737's render functions
- By the time FA-FE handlers see the data, it's already corrupted

### Why Kernel Text Works But Field Text Doesn't
- **Kernel text** (battle menus, items): Loaded from `KERNEL.BIN`/`kernel2.bin`, simpler encoding, PR #737 handles it
- **Field text**: Loaded from `jfleve.lgp`, uses FA-FE encoding, requires text parser that `ff7_en.exe` doesn't have

---

## Technical Deep Dive

### PR #737 Architecture

**File:** `C:\FFNx\src\ff7\japanese_text.cpp`

**Key functions hooked (from `ff7_opengl.cpp` lines 368-388):**
```cpp
if (ff7_japanese_edition)
{
    replace_function(ff7_externals.field_submit_draw_text_640x480_6E706D, field_submit_draw_text_640x480_6E706D_jp);
    replace_function(ff7_externals.engine_load_menu_graphics_objects_6C1468, engine_load_menu_graphics_objects_6C1468_jp);
    replace_function(ff7_externals.field_draw_text_boxes_and_text_graphics_object_6ECA68, field_draw_text_boxes_and_text_graphics_object_6ECA68_jp);
    replace_function(ff7_externals.common_submit_draw_char_from_buffer_6F564E, common_submit_draw_char_from_buffer_6F564E_jp);
    replace_function(ff7_externals.menu_draw_everything_6CC9D3, menu_draw_everything_6CC9D3_jp);
    replace_function(ff7_externals.battle_draw_menu_everything_6CEE84, battle_draw_menu_everything_6CEE84_jp);
    replace_function(ff7_externals.draw_text_top_display_6D1CC0, draw_text_top_display_6D1CC0_jp);
    replace_function(ff7_externals.main_menu_draw_everything_maybe_6C0B91, main_menu_draw_everything_maybe_6C0B91_jp);
    replace_function(ff7_externals.field_text_box_window_opening_6317A9, field_text_box_window_opening_6317A9_jp);
    replace_function(ff7_externals.sub_6F54A2, sub_6F54A2_jp);
}
```

**FA-FE handling (lines 514-553):**
```cpp
switch ( *buffer_text )
{
    case 0xFAu:
        ++buffer_text;  // Skip FA marker
        graphics_object = ff7_externals.menu_jafont_2_graphics_object;
        kanjiDetected = true;
        charWidth = charWidthData[1][*buffer_text] & 0x1F;
        continue;
    case 0xFBu:
        // Similar for jafont_3
    case 0xFCu:
        // Similar for jafont_4
    case 0xFDu:
        // Similar for jafont_5
    case 0xFEu:
        // Similar for jafont_6
}
```

### Character Mapping Reference

**Location:** `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/character_maps/`
- `ff7_complete_mapping_compact.csv` - Complete 1,536 character mapping
- `JAFONT_CHARACTER_MAP.md` - Documentation of encoding system

**Format:**
```csv
texture,index,character,unicode
jafont_1,0,バ,U+30D0
jafont_2,0,必,U+5FC5
```

### File Locations Summary

| Item | Path |
|------|------|
| FFNx Source | `C:\FFNx\` |
| Build Output | `C:\FFNx\.build\Release\FFNx.dll` |
| Steam FF7 | `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\` |
| Japanese Version | `D:\Games\Stand-alone\FINAL FANTASY VII\` |
| Project Root | `/home/johnzealanddoyle/projects/ff7OG_japanese/` |
| Japanese Assets | `/home/johnzealanddoyle/projects/ff7OG_japanese/japanese-assets-extracted/raw-files/` |
| Font TEX Files | `/home/johnzealanddoyle/projects/ff7OG_japanese/assets/fonts/tex/` |
| Documentation | `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/` |

---

## What Needs to Be Done Next

### Immediate Investigation
1. **Trace the text data pipeline** - Add logging to see what bytes arrive at `field_submit_draw_text_640x480_6E706D_jp`
2. **Compare with Japanese exe** - Run `ff7_ja.exe` with same setup to see if it works
3. **Check field file decompression** - `ff7_read_field_file` in `file.cpp` decompresses field data; verify it's not corrupting FA-FE bytes

### Potential Solutions

**Option A: Hook the text parser earlier**
- Find where `ff7_en.exe` parses text bytes from field files
- Intercept before interpretation
- Properly handle FA-FE as two-byte sequences

**Option B: Pre-process field text data**
- After field file decompression, scan for FA-FE sequences
- Ensure they're preserved intact for the render functions

**Option C: Use ff7_ja.exe with English assets**
- May require different externals addresses
- PR #737 was designed for this configuration

### Key Code Locations to Investigate

1. **Field file reading:** `C:\FFNx\src\ff7\file.cpp` - `ff7_read_field_file()` (line 640)
2. **Text decompression:** Same file, `lzss_decode` call
3. **Text buffer handling:** Look for where `buffer_text` pointer is set before render functions
4. **External addresses:** `C:\FFNx\src\ff7_data.h` - Memory addresses for text-related functions

---

## Build Instructions

### Prerequisites (Already Installed)
- Visual Studio 2022 Community
- CMake 3.27.8 at `C:\cmake-3.27.8\cmake-3.27.8-windows-x86_64\`
- vcpkg at `C:\vcpkg\`

### Build Command
```powershell
cd C:\FFNx
C:\cmake-3.27.8\cmake-3.27.8-windows-x86_64\bin\cmake.exe --build .build --config Release
```

### Build Notes
- Takes ~2-3 minutes
- Automatically deploys to both FF7 installations
- If FFNx.toml is locked, close FF7 and 7th Heaven first

---

## Key Documentation References

| Document | Purpose |
|----------|---------|
| `docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` | Complete technical specification |
| `docs/PR737_ANALYSIS.md` | PR #737 code analysis |
| `docs/FFNX_DEVELOPER_GUIDE.md` | FFNx architecture overview |
| `docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md` | Testing checklist |
| `docs/character_maps/JAFONT_CHARACTER_MAP.md` | Character encoding reference |

---

## Critical Insights

1. **PR #737 was designed for `ff7_ja.exe`** - It provides rendering support but relies on the Japanese executable's native text parser

2. **The English executable doesn't understand FA-FE encoding** - This is the fundamental gap

3. **Our LGP redirection works** - The log proves `jfleve.lgp` is being loaded

4. **Font textures load correctly** - No errors in log

5. **The problem is in the text byte pipeline** - Somewhere between file read and render function, the encoding is misinterpreted

6. **This is documented as "Phase 2" work** - The Master Bible anticipated this would require additional text parser hooks

---

## Session Metrics

- **Duration:** ~2 hours
- **Major Achievement:** First Japanese text rendering on English FF7 exe
- **Build Success:** Yes (with LNK4088 warning, non-fatal)
- **Commits Made:** None (user preference to commit at milestones)

---

## Questions for Next Agent

1. What happens to FA-FE bytes during LZSS decompression in `ff7_read_field_file`?
2. Is there a text encoding translation layer in `ff7_en.exe` that needs to be bypassed?
3. Would adding explicit FA-FE parsing before the render functions receive data solve this?
4. Should we consider generating English-format encoded Japanese text (single-byte mapping)?

---

## Contact Points

- **FFNx GitHub:** https://github.com/julianxhokaxhiu/FFNx
- **PR #737:** https://github.com/julianxhokaxhiu/FFNx/pull/737
- **Project Repo:** https://github.com/john-savepoint/makosource.git

---

---

## Session Continuation Findings (23:23 JST)

### Critical Discovery: Japanese Hooks Are Active But Not Called for Field Text

**Debug logging confirmed:**
1. `ff7_japanese_edition = 1` - config is working
2. Japanese text hooks ARE being installed at startup
3. `common_submit_draw_char_from_buffer_6F564E_jp` IS being called (for menu text)
4. BUT `field_submit_draw_text_640x480_6E706D_jp` is NOT being called for field dialogue

**Character data analysis:**
```
CHAR_DRAW_DEBUG[10]: letter=0x004E  (ASCII 'N')
CHAR_DRAW_DEBUG[11]: letter=0x0054  (ASCII 'T')
CHAR_DRAW_DEBUG[12]: letter=0x0049  (ASCII 'I')
...
```
- All characters are English encoding (0x00-0x5F range)
- NO FA-FE markers seen at all
- Text is "NEW GAME" / "CONTINUE" - menu text, not field dialogue

**Implication:**
Field dialogue on `ff7_en.exe` goes through a DIFFERENT code path than what PR #737 hooks. The hooked functions are for:
- Menu text (working)
- Battle text (working)
- But NOT field dialogue rendering

**Next Investigation:**
Need to find what function actually renders field dialogue on `ff7_en.exe` and hook that instead/additionally.

---

## MAJOR BREAKTHROUGH (23:41 JST)

### Field Dialogue IS WORKING!

User confirmed after playing more:
1. **Field dialogue (story text) = WORKING CORRECTLY** - Japanese text renders properly!
2. **Character names in dialogue = BROKEN** - Shows garbled text (English encoding through Japanese font)
3. **Menus = BROKEN** - Same issue
4. **Character naming screen = Useful** - Shows the English→Japanese byte mapping

### What This Means

**The `jfleve.lgp` redirection IS working for story dialogue!** The FA-FE encoded Japanese text from field files is loading and rendering correctly.

The broken parts are:
- **Character names** - Stored separately (save file, kernel), use English encoding
- **Menu strings** - Come from executable or different data source, use English encoding

When English-encoded text (0x00-0xD4) is rendered through the Japanese font textures (jafont_1), it shows wrong characters because the character positions don't match.

### Remaining Fix Needed

We need to either:
1. **Load Japanese menu/name data** - Find where menu strings and character names come from and redirect to Japanese sources
2. **OR create a character mapping translation layer** - Translate English byte values to Japanese font positions at render time for non-field text

### Files Involved (Likely)

- `KERNEL.BIN` / `kernel2.bin` - Contains menu strings, item names, etc.
- `WINDOW.BIN` - Window/UI data
- Save game data - Character names
- Possibly hardcoded strings in executable

---

## Code Changes Made (23:45 JST)

### 1. Kernel2 Redirect Added

**File:** `C:\FFNx\src\ff7\kernel.cpp`

Added Japanese kernel2.bin redirect to `ff7_load_kernel2_wrapper`:

```cpp
#include "../globals.h"  // Added at top

void ff7_load_kernel2_wrapper(char *filename)
{
  // DEBUG: Log kernel2 load
  ffnx_info("KERNEL2_LOAD: filename=%s, ff7_japanese_edition=%d\n", filename, ff7_japanese_edition);

  // Japanese edition: try to load from lang-ja path
  if (ff7_japanese_edition)
  {
    char ja_filename[260];
    // Try lang-ja path: data/lang-ja/kernel/kernel2.bin
    _snprintf(ja_filename, sizeof(ja_filename), "%s/data/lang-ja/kernel/kernel2.bin", basedir);

    FILE* fd = fopen(ja_filename, "rb");
    if (fd != NULL)
    {
      fclose(fd);
      ffnx_info("KERNEL2_LOAD: Redirecting to Japanese kernel2: %s\n", ja_filename);
      ff7_externals.kernel_load_kernel2(ja_filename);
      return;
    }
    else
    {
      ffnx_warning("KERNEL2_LOAD: Japanese kernel2 not found at %s, using default\n", ja_filename);
    }
  }

  ff7_externals.kernel_load_kernel2(filename);
  // ... rest of chunk override code
}
```

### 2. Debug Logging Added Throughout

**Files modified with debug logging:**
- `C:\FFNx\src\ff7_opengl.cpp` - Hook installation logging
- `C:\FFNx\src\ff7\japanese_text.cpp` - Character draw and field text box logging
- `C:\FFNx\src\ff7\kernel.cpp` - Kernel2 load logging

### Files Deployed

Japanese kernel files at:
```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\data\lang-ja\kernel\
├── KERNEL.BIN (20K)
├── kernel2.bin (12K)
└── WINDOW.BIN (13K)
```

### Current Test Status

**Awaiting test** - User needs to launch game and check:
1. Does kernel2 redirect message appear in log?
2. Do menus now show correct Japanese text?

---

## Summary of All Code Changes in This Session

| File | Change |
|------|--------|
| `src/ff7/file.cpp` | Added `jfleve.lgp` redirect AND `menu_ja.lgp` redirect |
| `src/ff7/kernel.cpp` | Added `kernel2.bin` redirect + Japanese kernel chunk support |
| `src/ff7/japanese_text.cpp` | Added debug logging for text rendering |
| `src/ff7_opengl.cpp` | Added debug logging for hook installation |

### Latest Addition: menu_ja.lgp Redirect (23:55 JST)

Added redirect for `menu_us.lgp` → `menu_ja.lgp` in `src/ff7/file.cpp`.

Copied `menu_ja.lgp` (27MB) to:
```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\data\menu\menu_ja.lgp
```

**Test needed:** Check if menu text now loads correctly in Japanese.

---

## Critical Understanding: Menu Text Encoding Problem (00:03 JST)

### The Core Issue

**User confirmed:** Menu text bytes are positioned for the **English font texture layout**. The game is:
1. Using English-encoded byte positions (designed for English font texture)
2. But rendering through Japanese font textures (which have different character positions)

**Example:**
- English font: byte `0x29` = "I" at position (x,y) in texture
- Japanese font: byte `0x29` = some random Japanese character at same position
- Result: "Items" displays as garbled Japanese

### Why This Happens

The **menu text source data** still uses English encoding:
- Menu strings like "Items", "Magic", "Equip" are stored as English byte values
- These bytes reference positions in the English font texture (font_a, font_b)
- When Japanese fonts (jafont_1-6) are loaded instead, the same byte positions map to different characters

### What Works vs What Doesn't

| Category | Status | Why |
|----------|--------|-----|
| Field dialogue | ✅ WORKS | Uses FA-FE encoded Japanese from `jfleve.lgp` |
| Item names | ✅ WORKS | Japanese `kernel2.bin` uses FA-FE encoding |
| Battle text | ✅ WORKS | Japanese kernel data |
| Menu labels | ❌ BROKEN | English byte encoding, wrong texture mapping |
| Character names | ❌ BROKEN | Saved in English encoding |

### Potential Solutions

1. **Find Japanese menu strings source** - There might be Japanese menu text in `menu_ja.lgp` or another file that needs proper loading
2. **Create byte translation table** - Map English byte positions to equivalent Japanese font positions
3. **Dual font system** - Use English fonts for menu labels, Japanese fonts for Japanese text
4. **Patch menu strings in memory** - Replace English strings with FA-FE encoded Japanese

### Files That Might Contain Japanese Menu Text

- ~~`menu_ja.lgp` (27MB)~~ - **ONLY contains textures** (jafont_*.tex, usfont_*.tex, portraits), NOT text strings
- `KERNEL.BIN` sections 1-9 - Command names, menu labels **(most likely source)**
- `WINDOW.BIN` - Window/UI strings (gzip compressed)
- Executable hardcoded strings

### Key Finding: menu_*.lgp Contents

`menu_us.lgp` and `menu_ja.lgp` contain **texture files only**:
- `jafont_1.tex` through `jafont_6.tex` (Japanese fonts) - in menu_ja.lgp
- `usfont_a_*.tex`, `usfont_b_*.tex` (English fonts)
- `btl_win_*.tex` (battle window graphics)
- Character portrait textures (cloud.tex, tifa.tex, etc.)

**No .mnu files exist** in PC version (PSX has .MNU files in /MENU/ directory).

### Critical Reference: Qhimm Wiki

From https://qhimm-modding.fandom.com/wiki/FF7/Menu_Module:

> **PSX Version:** Menu modules are `.MNU` files in `/MENU/` directory
> **PC Version:** Menu code is **internal to the executable**, resources in `MENU_US.LGP`

This confirms: **Menu text strings are likely HARDCODED in the PC executable** (`ff7_en.exe`), not in external data files. This is why redirecting LGP/kernel files doesn't fix menu labels.

The wiki also notes:
> "The large blank spot under the menu text is for the Japanese characters that were removed in the non-Japanese version"

This means Japanese VRAM space exists but English exe doesn't have the Japanese strings.

### Next Steps for Future Agent

1. **Investigate `menu_ja.lgp` contents** - Extract and examine what strings it contains
2. **Decompress `WINDOW.BIN`** - Check if it contains menu strings
3. **Extract Japanese KERNEL.BIN sections** - Create chunk files for override system
4. **Consider byte translation** - If menu strings can't be redirected, translate byte positions

---

## Session Statistics

- **Session Start:** 2025-11-26 22:01 JST
- **Session End:** 2025-11-27 00:03 JST
- **Duration:** ~2 hours
- **Build Count:** 8+ rebuilds
- **Major Achievement:** First-ever Japanese field dialogue on English FF7 exe

---

**End of Handoff Document**

*Next agent: Field dialogue works perfectly. Menu text is the remaining challenge - it uses English byte encoding that maps wrong in Japanese fonts. Need to either find Japanese menu data source or create translation layer. Good luck!*
