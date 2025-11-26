# Japanese Assets Installation Guide for Windows

**Created**: 2025-11-25 17:33:00 JST (Tuesday)
**Session-ID**: 0ba935f5-efe0-457c-ad7e-c18f89cfba18
**Purpose**: Step-by-step guide to install Japanese text support for FF7 using PR #737

---

## Prerequisites (Windows)

### Required Software:
1. **Final Fantasy VII PC** (Steam 2013 or 1998 version)
2. **FFNx Driver** (latest build with PR #737 merged)
   - Download: https://github.com/julianxhokaxhiu/FFNx/releases
   - OR build from PR #737 branch yourself
3. **7th Heaven Mod Manager** (optional but recommended)
   - Download: https://7thheaven.rocks/
4. **ulgp Tool** (LGP extraction)
   - Download: http://forums.qhimm.com/index.php?topic=12831.0
5. **TexTool** (TEX to PNG conversion)
   - Download: https://drive.google.com/file/d/0B0FYTN9Fe13HSTVCM3Z3QjhKZWc/view

---

## Part 1: Extract Japanese Font Textures

### Step 1: Extract menu_ja.lgp

```cmd
REM Navigate to your asset folder
cd C:\japanese-assets-extracted\raw-files

REM Extract LGP archive
ulgp extract menu_ja.lgp extracted\menu

REM This creates extracted\menu\ with all files from menu_ja.lgp
```

**Expected files** (look for these):
- `jafont_1.tim` (Hiragana, Katakana, ASCII)
- `jafont_2.tim` (Kanji page 1)
- `jafont_3.tim` (Kanji page 2)
- `jafont_4.tim` (Kanji page 3)
- `jafont_5.tim` (Kanji page 4)
- `jafont_6.tim` (Kanji page 5)

### Step 2: Convert TIM to PNG

```cmd
REM Convert each font texture to PNG
TexTool.exe extracted\menu\jafont_1.tim converted\jafont_1.png
TexTool.exe extracted\menu\jafont_2.tim converted\jafont_2.png
TexTool.exe extracted\menu\jafont_3.tim converted\jafont_3.png
TexTool.exe extracted\menu\jafont_4.tim converted\jafont_4.png
TexTool.exe extracted\menu\jafont_5.tim converted\jafont_5.png
TexTool.exe extracted\menu\jafont_6.tim converted\jafont_6.png
```

**Alternative**: Use FFNx's built-in texture dumping:
1. Copy menu_ja.lgp to FF7 install directory temporarily
2. Enable `save_textures = true` in FFNx.toml
3. Run game once with ff7_ja.exe
4. FFNx auto-exports PNG files to `mods/Textures/`

---

## Part 2: Set Up Mod Directory Structure

### Option A: 7th Heaven Mod (Recommended)

Create this folder structure:

```
FF7-Japanese-Text-Mod/
├── mod.xml
├── preview.png (optional)
├── Readme.txt
└── data/
    ├── textures/
    │   └── menu/
    │       ├── jafont_1.png
    │       ├── jafont_2.png
    │       ├── jafont_3.png
    │       ├── jafont_4.png
    │       ├── jafont_5.png
    │       └── jafont_6.png
    ├── kernel/
    │   ├── KERNEL.BIN
    │   └── kernel2.bin
    └── field/
        └── jfleve.lgp
```

**Copy files**:
```cmd
copy converted\jafont_*.png FF7-Japanese-Text-Mod\data\textures\menu\
copy raw-files\KERNEL.BIN FF7-Japanese-Text-Mod\data\kernel\
copy raw-files\kernel2.bin FF7-Japanese-Text-Mod\data\kernel\
copy raw-files\jfleve.lgp FF7-Japanese-Text-Mod\data\field\
```

### Option B: Direct FFNx Mod (No 7th Heaven)

Place files in FF7 install directory:

```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\
└── mods/
    ├── Textures/
    │   └── menu/
    │       ├── jafont_1.png
    │       ├── jafont_2.png
    │       ├── jafont_3.png
    │       ├── jafont_4.png
    │       ├── jafont_5.png
    │       └── jafont_6.png
    └── lang-ja/
        ├── kernel/
        │   ├── KERNEL.BIN
        │   └── kernel2.bin
        └── field/
            └── jfleve.lgp
```

**Copy files**:
```cmd
REM Navigate to FF7 install directory
cd "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII"

REM Create directories
mkdir mods\Textures\menu
mkdir mods\lang-ja\kernel
mkdir mods\lang-ja\field

REM Copy textures
copy C:\japanese-assets-extracted\converted\jafont_*.png mods\Textures\menu\

REM Copy dialogue files
copy C:\japanese-assets-extracted\raw-files\KERNEL.BIN mods\lang-ja\kernel\
copy C:\japanese-assets-extracted\raw-files\kernel2.bin mods\lang-ja\kernel\
copy C:\japanese-assets-extracted\raw-files\jfleve.lgp mods\lang-ja\field\
```

---

## Part 3: Configure FFNx

### Step 1: Locate FFNx.toml

**7th Heaven users**:
```
%APPDATA%\7thHeaven\FFNx.toml
```

**Manual FFNx users**:
```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.toml
```

### Step 2: Edit FFNx.toml

Open FFNx.toml in Notepad++ or VS Code, find and modify these settings:

```toml
###############################################################################
# Japanese Text Support (PR #737)
###############################################################################

# CRITICAL: Enable Japanese text rendering
ff7_japanese_edition = true

# Optional: Save textures for debugging (disable after first run)
save_textures = false

# Optional: Show missing texture warnings
show_missing_textures = false

# Optional: Debug logging (helpful for troubleshooting)
trace_all = false
trace_loaders = false
```

**IMPORTANT**: Set `ff7_japanese_edition = true` - This is the only required change!

### Step 3: Verify File Paths (Optional)

If using Option B (direct FFNx mod), verify FFNx can find your files:

```toml
# FFNx texture override path (default is correct)
# No need to change unless you moved mods folder
```

---

## Part 4: Test Installation

### Test Procedure:

1. **Launch FF7**:
   - If using 7th Heaven: Enable "FF7-Japanese-Text-Mod" and click Play
   - If using FFNx directly: Run `ff7_en.exe`

2. **Check FFNx.log** (in FF7 install directory):
   ```
   [INFO] Japanese edition mode: ENABLED
   [INFO] Loading texture: menu/jafont_1.png
   [INFO] Loading texture: menu/jafont_2.png
   [INFO] Loading texture: menu/jafont_3.png
   [INFO] Loading texture: menu/jafont_4.png
   [INFO] Loading texture: menu/jafont_5.png
   [INFO] Loading texture: menu/jafont_6.png
   ```

3. **Start New Game**:
   - Opening cutscene should show Japanese text
   - Menu should display Japanese characters
   - Dialogue boxes should render Japanese correctly

4. **Test All Text Contexts**:
   - [ ] Field dialogue (talk to NPCs)
   - [ ] Battle menu (attack, magic, item)
   - [ ] Main menu (save, item, materia)
   - [ ] Character names
   - [ ] Item descriptions

### Expected Results:

✅ **WORKING**:
- Japanese characters display correctly
- Text is not "squashed" (variable width working)
- No crashes or freezes
- All 6 font pages load successfully

⚠️ **KNOWN ISSUES** (from PR #737):
- Colored text may not work correctly (FE code conflict)
- Character input (name entry) may be corrupted
- Cursor alignment may be slightly off

❌ **FAILING** (needs investigation):
- Text doesn't appear at all → Check FFNx.log for errors
- Crashes on startup → Check FFNx.log for missing files
- English text instead of Japanese → `ff7_japanese_edition` not set

---

## Part 5: Create 7th Heaven IRO (Optional)

If you want to distribute as a 7th Heaven mod:

### Step 1: Create mod.xml

Save this in `FF7-Japanese-Text-Mod\mod.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModInfo>
  <ID>YOUR-GENERATED-GUID-HERE</ID>
  <Name>FF7 Japanese Text Support (PR #737)</Name>
  <Author>CosmosXIII (PR #737) + Your Name</Author>
  <Version>1.00</Version>
  <ReleaseDate>2025-11-25</ReleaseDate>
  <Category>User Interface</Category>
  <Description>Enables Japanese text rendering in English FF7 executable using FFNx PR #737. Includes all 6 Japanese font pages (Hiragana, Katakana, Kanji) and Japanese dialogue files.</Description>
  <PreviewFile>preview.png</PreviewFile>

  <ModFolder Folder="data" />
</ModInfo>
```

**Generate GUID**:
1. Open 7th Heaven
2. Workshop → Catalog/Mod Creation Tool
3. Click "Generate new GUID"
4. Copy into `<ID>` field

### Step 2: Package as IRO

```cmd
cd FF7-Japanese-Text-Mod
7z a -tzip "..\FF7-Japanese-Text-v1.00.iro" *
```

### Step 3: Import to 7th Heaven

1. Open 7th Heaven
2. Library tab → Import Mod
3. Select `FF7-Japanese-Text-v1.00.iro`
4. Go to My Mods tab
5. Enable the mod
6. Click Play

---

## Troubleshooting

### Issue: "Mod failed to load"

**Solution**:
1. Extract IRO with 7-Zip
2. Check mod.xml for syntax errors
3. Verify folder structure matches guide
4. Rebuild IRO

### Issue: Textures don't appear

**Solution**:
1. Check FFNx.log for "File not found" errors
2. Verify PNG files are in `mods/Textures/menu/`
3. Check file names match exactly (case-sensitive on some systems)
4. Try `save_textures = true` to see what FFNx expects

### Issue: Dialogue still in English

**Solution**:
1. Verify `ff7_japanese_edition = true` in FFNx.toml
2. Check `jfleve.lgp` is in correct location
3. Verify KERNEL.BIN is in correct location
4. Check FFNx.log for VFS redirect messages

### Issue: Crashes on startup

**Solution**:
1. Check FFNx.log for error messages
2. Verify all 6 font PNG files exist
3. Try disabling other mods (conflict test)
4. Rebuild FFNx from PR #737 branch

### Issue: Known bugs (colored text, cursor)

**Solution**:
- These are documented issues in PR #737
- Wait for bug fixes to be merged
- See `docs/PR737_COMPLETE_ANALYSIS.md` Section 7 for details

---

## Advanced: Building FFNx with PR #737

If PR #737 isn't merged yet, build it yourself:

### Prerequisites:
- Visual Studio 2022 (Community Edition is free)
- CMake 3.20+
- vcpkg (included in repo)

### Build Steps:

```cmd
REM Clone FFNx repository
git clone https://github.com/julianxhokaxhiu/FFNx.git
cd FFNx

REM Fetch PR #737
git fetch origin pull/737/head:pr-737
git checkout pr-737

REM Build
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release

REM Output: build\Release\FFNx.dll
```

### Install:

```cmd
REM Backup original FFNx.dll
copy "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.dll" FFNx.dll.backup

REM Copy new build
copy build\Release\FFNx.dll "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.dll"
```

---

## Quick Reference: File Locations

### Raw Assets (Mac extraction):
```
japanese-assets-extracted/
├── raw-files/
│   ├── menu_ja.lgp (26MB)
│   ├── jfleve.lgp (123MB)
│   ├── KERNEL.BIN (20KB)
│   ├── kernel2.bin (12KB)
│   └── WINDOW.BIN (13KB)
```

### Converted Assets (Windows, after extraction):
```
converted/
├── jafont_1.png
├── jafont_2.png
├── jafont_3.png
├── jafont_4.png
├── jafont_5.png
└── jafont_6.png
```

### Final Installation (FFNx direct):
```
FINAL FANTASY VII/
├── FFNx.dll (PR #737 build)
├── FFNx.toml (ff7_japanese_edition = true)
└── mods/
    ├── Textures/menu/
    │   └── jafont_*.png
    └── lang-ja/
        ├── kernel/
        │   ├── KERNEL.BIN
        │   └── kernel2.bin
        └── field/
            └── jfleve.lgp
```

---

## Summary: What You're Transferring to Windows

**Files to copy from Mac**:
1. `raw-files/menu_ja.lgp` (26MB)
2. `raw-files/jfleve.lgp` (123MB)
3. `raw-files/KERNEL.BIN` (20KB)
4. `raw-files/kernel2.bin` (12KB)

**Tools to download on Windows**:
1. ulgp (LGP extraction)
2. TexTool (TIM to PNG conversion)
3. 7-Zip (IRO packaging, if making 7H mod)

**Steps on Windows**:
1. Extract menu_ja.lgp → get jafont_1-6.tim
2. Convert TIM to PNG → get jafont_1-6.png
3. Copy all assets to FF7 mods directory
4. Set `ff7_japanese_edition = true` in FFNx.toml
5. Launch ff7_en.exe
6. Enjoy Japanese text!

---

**End of Guide**

**Questions? Issues?**
- Check FFNx.log first
- Review `docs/PR737_COMPLETE_ANALYSIS.md` for technical details
- Post on Qhimm forums: https://forums.qhimm.com/
