# Simple Instructions: Get Japanese Text Working in FF7

**Created**: 2025-11-25 18:20:00 JST (Tuesday)
**For**: John Zealand-Doyle

---

## What You Already Have ✅

1. ✅ **Font textures** (jafont_1.png through jafont_6.png) - in `assets/fonts/png/`
2. ✅ **Japanese dialogue files** - in `japanese-assets-extracted/raw-files/`
3. ✅ **PR #737 source code** - in `PR737/` directory
4. ✅ **Complete 7th Heaven mod** - in `FF7-Japanese-Mod/` directory (I just created this!)

---

## What You Need to Do on Windows

### Step 1: Transfer Files to Windows

Copy these folders to Windows:
- `FF7-Japanese-Mod/` (126MB) - The complete mod
- `PR737/` (entire directory) - FFNx source code

### Step 2: Build FFNx on Windows

```cmd
REM Prerequisites: Visual Studio 2022, CMake

cd PR737
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release

REM Output: build\Release\FFNx.dll
```

### Step 3: Install FFNx

```cmd
REM Copy to FF7 directory (adjust path for your install)
copy build\Release\FFNx.dll "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.dll"
```

### Step 4: Create IRO File (for 7th Heaven)

```cmd
cd FF7-Japanese-Mod
7z a -tzip "..\FF7-Japanese-v1.00.iro" *
```

### Step 5: Install in 7th Heaven

1. Open 7th Heaven
2. Library tab → Import Mod
3. Select `FF7-Japanese-v1.00.iro`
4. Enable the mod in My Mods

### Step 6: Configure FFNx

**Find FFNx.toml** at:
- `%APPDATA%\7thHeaven\FFNx.toml` (if using 7th Heaven)
- OR `C:\...\FINAL FANTASY VII\FFNx.toml` (if direct install)

**Add ONE line**:
```toml
ff7_japanese_edition = true
```

### Step 7: Play!

Click Play in 7th Heaven (or run ff7_en.exe directly).

---

## About the Encoder/Decoder Mapping

**Your question about the mapping files**:

The character mapping you created (in `assets/character_mappings/`) is for **CREATING** Japanese text files from Unicode.

**PR #737 already has the decoder built-in!**

Look at `PR737/src/ff7/japanese_text.cpp:311`:

```cpp
int charWidthData[6][256] = {
    // This IS the decoder mapping!
    // It knows how to render FA-FE encoded text
    { 30, 30, 28, 31, 30, 30, ... },  // jafont_1 character widths
    { 31, 31, 30, 31, 31, 30, ... },  // jafont_2 character widths
    ...
};
```

**Right now**, your mapping files are **NOT needed** because:
- PR #737 reads **existing** Japanese dialogue files (jfleve.lgp, KERNEL.BIN)
- Those files are already FA-FE encoded (by Square Enix)
- PR #737's code already knows how to decode them

**Later**, you'll need your mapping when:
- Creating NEW dialogue (e.g., translating English → Japanese)
- Building an encoder tool (Unicode → FA-FE)
- Creating a crowdsourced translation platform

But for **just displaying Japanese text**, PR #737 + the dialogue files are complete!

---

## Quick Answer to Your Questions

### Q: Do I have the font textures?
**A**: YES! In `assets/fonts/png/` - all 6 files.

### Q: Do I have to build FFNx?
**A**: YES. PR737/ has source code. Build it on Windows to get FFNx.dll.

### Q: Where do I get KERNEL.BIN, jfleve.lgp?
**A**: I already copied them! In `japanese-assets-extracted/raw-files/` and now in `FF7-Japanese-Mod/lang-ja/`.

### Q: Can you make the 7th Heaven mod?
**A**: DONE! It's in `FF7-Japanese-Mod/`. Just need to zip it as .iro on Windows.

### Q: Does 7th Heaven load from IRO or folder?
**A**: IRO files. Use 7-Zip to create: `7z a -tzip mod.iro *`

### Q: Do the encoder/decoder mappings factor in?
**A**: NOT YET. PR #737 already has a decoder. You'll need the encoder when creating NEW dialogue later.

---

## What's in FF7-Japanese-Mod/ (Ready to Use!)

```
FF7-Japanese-Mod/
├── mod.xml (7th Heaven metadata)
├── Readme.txt (user instructions)
├── mods/
│   └── Textures/
│       └── menu/
│           ├── jafont_1.png (your PNG files!)
│           ├── jafont_2.png
│           ├── jafont_3.png
│           ├── jafont_4.png
│           ├── jafont_5.png
│           └── jafont_6.png
└── lang-ja/
    ├── kernel/
    │   ├── KERNEL.BIN (from Japanese install)
    │   └── kernel2.bin
    └── field/
        └── jfleve.lgp (from Japanese install)
```

**Total size**: 126MB

---

## The ONLY Things You Need to Do on Windows

1. **Build FFNx.dll** from PR737 source
2. **Create IRO**: `7z a -tzip FF7-Japanese-v1.00.iro *` (in FF7-Japanese-Mod folder)
3. **Import IRO** into 7th Heaven
4. **Edit FFNx.toml**: Add `ff7_japanese_edition = true`
5. **Play!**

---

## Expected Result

- Launch ff7_en.exe
- Opening cutscene shows Japanese text
- Field dialogue is Japanese
- Menus are Japanese
- Variable-width fonts work
- All 1,536 characters render correctly

---

## If It Doesn't Work

Check FFNx.log for:
```
[INFO] Japanese edition mode: ENABLED
[INFO] Loading texture: menu/jafont_1.png
[INFO] Loading texture: menu/jafont_2.png
...
```

If those lines are missing:
- Verify FFNx.dll is from PR737 build
- Verify `ff7_japanese_edition = true` in FFNx.toml
- Verify IRO imported successfully in 7th Heaven

---

**That's it! Much simpler than my previous explanation. Everything is ready - just build on Windows and test!**
