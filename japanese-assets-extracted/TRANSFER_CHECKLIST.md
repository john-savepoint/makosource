# Transfer Checklist: Mac → Windows

**Created**: 2025-11-25 17:37:00 JST (Tuesday)
**Session-ID**: 0ba935f5-efe0-457c-ad7e-c18f89cfba18

---

## Files to Transfer from Mac

Copy this entire folder to Windows:

```
japanese-assets-extracted/
├── README.md
├── WINDOWS_INSTALLATION_GUIDE.md
├── FFNx-japanese.toml
├── TRANSFER_CHECKLIST.md (this file)
└── raw-files/
    ├── menu_ja.lgp (26MB)
    ├── jfleve.lgp (123MB)
    ├── KERNEL.BIN (20KB)
    ├── kernel2.bin (12KB)
    └── WINDOW.BIN (13KB)
```

**Total size**: ~150MB

---

## Transfer Methods

### Option A: External Drive
1. Copy `japanese-assets-extracted/` folder to USB drive
2. Transfer USB drive to Windows PC
3. Copy folder to Windows (e.g., `C:\FF7-Assets\`)

### Option B: Cloud Storage
1. Upload folder to Google Drive / Dropbox / OneDrive
2. Download on Windows PC
3. Extract to local drive

### Option C: Network Share
1. Enable file sharing on Mac
2. Connect from Windows PC
3. Copy folder over network

---

## On Windows: Tools to Download

### Required Tools:

1. **ulgp** (LGP extraction)
   - Forum: http://forums.qhimm.com/index.php?topic=12831.0
   - Purpose: Extract jafont_*.tim from menu_ja.lgp

2. **TexTool** (TIM to PNG conversion)
   - Google Drive: https://drive.google.com/file/d/0B0FYTN9Fe13HSTVCM3Z3QjhKZWc/view
   - Purpose: Convert jafont_*.tim to jafont_*.png

3. **7-Zip** (archive tool)
   - Website: https://www.7-zip.org/
   - Purpose: Create IRO files if making 7th Heaven mod

### Optional Tools:

4. **7th Heaven** (mod manager)
   - Website: https://7thheaven.rocks/
   - Purpose: Easy mod management

5. **FFNx** (graphics driver with PR #737)
   - GitHub: https://github.com/julianxhokaxhiu/FFNx/releases
   - Purpose: Japanese text rendering support

---

## On Windows: Installation Steps

### Step 1: Extract Assets
```cmd
cd C:\FF7-Assets\japanese-assets-extracted\raw-files

REM Extract menu_ja.lgp
ulgp extract menu_ja.lgp extracted\menu

REM Convert TIM to PNG
TexTool.exe extracted\menu\jafont_1.tim converted\jafont_1.png
TexTool.exe extracted\menu\jafont_2.tim converted\jafont_2.png
TexTool.exe extracted\menu\jafont_3.tim converted\jafont_3.png
TexTool.exe extracted\menu\jafont_4.tim converted\jafont_4.png
TexTool.exe extracted\menu\jafont_5.tim converted\jafont_5.png
TexTool.exe extracted\menu\jafont_6.tim converted\jafont_6.png
```

### Step 2: Copy to FF7 Install
```cmd
REM Navigate to FF7 directory
cd "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII"

REM Create mod directories
mkdir mods\Textures\menu
mkdir mods\lang-ja\kernel
mkdir mods\lang-ja\field

REM Copy textures
copy C:\FF7-Assets\japanese-assets-extracted\raw-files\converted\jafont_*.png mods\Textures\menu\

REM Copy dialogue
copy C:\FF7-Assets\japanese-assets-extracted\raw-files\KERNEL.BIN mods\lang-ja\kernel\
copy C:\FF7-Assets\japanese-assets-extracted\raw-files\kernel2.bin mods\lang-ja\kernel\
copy C:\FF7-Assets\japanese-assets-extracted\raw-files\jfleve.lgp mods\lang-ja\field\
```

### Step 3: Configure FFNx
```cmd
REM Edit FFNx.toml
notepad FFNx.toml

REM Add this line:
ff7_japanese_edition = true
```

### Step 4: Test
```cmd
REM Launch FF7
ff7_en.exe

REM Check log
notepad FFNx.log
```

---

## Verification Checklist

After installation on Windows, verify:

### Files Copied:
- [ ] `mods/Textures/menu/jafont_1.png` exists
- [ ] `mods/Textures/menu/jafont_2.png` exists
- [ ] `mods/Textures/menu/jafont_3.png` exists
- [ ] `mods/Textures/menu/jafont_4.png` exists
- [ ] `mods/Textures/menu/jafont_5.png` exists
- [ ] `mods/Textures/menu/jafont_6.png` exists
- [ ] `mods/lang-ja/kernel/KERNEL.BIN` exists
- [ ] `mods/lang-ja/kernel/kernel2.bin` exists
- [ ] `mods/lang-ja/field/jfleve.lgp` exists

### Configuration:
- [ ] `FFNx.toml` has `ff7_japanese_edition = true`
- [ ] `FFNx.dll` is PR #737 build or later

### In-Game:
- [ ] Game launches without crashes
- [ ] Japanese text appears in dialogue boxes
- [ ] Menu shows Japanese characters
- [ ] No "missing texture" errors in FFNx.log

---

## If Something Goes Wrong

### Game won't launch:
1. Check FFNx.log for error messages
2. Verify FFNx.dll is correct version
3. Try disabling other mods

### Text is still English:
1. Verify `ff7_japanese_edition = true` in FFNx.toml
2. Check all 6 PNG files exist
3. Check FFNx.log for "Japanese edition mode: ENABLED"

### Textures missing:
1. Enable `show_missing_textures = true` in FFNx.toml
2. Check FFNx.log for file path errors
3. Verify PNG files are not corrupted
4. Re-extract and re-convert from TIM

### Game crashes:
1. Check FFNx.log for crash location
2. Try loading different save file
3. Rebuild FFNx from PR #737 branch
4. Report issue with FFNx.log to Qhimm forums

---

## Quick Reference URLs

Save these for Windows:

- **ulgp download**: http://forums.qhimm.com/index.php?topic=12831.0
- **TexTool download**: https://drive.google.com/file/d/0B0FYTN9Fe13HSTVCM3Z3QjhKZWc/view
- **7th Heaven**: https://7thheaven.rocks/
- **FFNx GitHub**: https://github.com/julianxhokaxhiu/FFNx
- **PR #737**: https://github.com/julianxhokaxhiu/FFNx/pull/737
- **Qhimm Forums**: https://forums.qhimm.com/

---

## Expected Results

After successful installation:

✅ **Opening cutscene** displays Japanese text
✅ **Field dialogue** shows Japanese characters
✅ **Menu text** rendered in Japanese
✅ **Battle text** displays Japanese
✅ **No crashes** or stability issues
✅ **Variable-width fonts** working (text not squashed)

⚠️ **Known Issues**:
- Colored text may not work
- Character input (name entry) may be corrupted
- Cursor alignment slightly off

---

## Total Time Estimate

- **File transfer**: 5-10 minutes
- **Tool download**: 10-15 minutes
- **Asset extraction**: 10-15 minutes
- **Installation**: 10-15 minutes
- **Testing**: 15-20 minutes

**Total**: 50-75 minutes (first time)

---

## Success Criteria

You're done when:

1. ✅ All files transferred to Windows
2. ✅ All tools downloaded and working
3. ✅ Assets extracted and converted
4. ✅ Files copied to FF7 mods directory
5. ✅ FFNx.toml configured correctly
6. ✅ Game launches successfully
7. ✅ Japanese text displays in-game
8. ✅ FFNx.log shows no errors

---

**Ready to go! Transfer these files to Windows and follow WINDOWS_INSTALLATION_GUIDE.md**

Good luck! 🎮
