# FF7 Japanese Assets Package

**Created**: 2025-11-25 17:35:00 JST (Tuesday)
**Session-ID**: 0ba935f5-efe0-457c-ad7e-c18f89cfba18
**Source**: Final Fantasy VII International Edition (Japanese)

---

## Package Contents

This directory contains all Japanese text assets needed to enable Japanese rendering in FF7 PC using FFNx PR #737.

### Directory Structure:

```
japanese-assets-extracted/
├── README.md (this file)
├── WINDOWS_INSTALLATION_GUIDE.md (complete step-by-step guide)
├── FFNx-japanese.toml (sample configuration)
└── raw-files/
    ├── menu_ja.lgp (26MB) - Contains jafont_1-6.tim (font textures)
    ├── jfleve.lgp (123MB) - Japanese field dialogue
    ├── KERNEL.BIN (20KB) - Japanese menu/battle text
    ├── kernel2.bin (12KB) - Additional kernel data
    └── WINDOW.BIN (13KB) - Window layout data
```

---

## What's Included

### 1. Font Textures (inside menu_ja.lgp)
- **jafont_1.tim** - Hiragana, Katakana, ASCII (256 characters)
- **jafont_2.tim** - Kanji page 1 (256 characters)
- **jafont_3.tim** - Kanji page 2 (256 characters)
- **jafont_4.tim** - Kanji page 3 (256 characters)
- **jafont_5.tim** - Kanji page 4 (256 characters)
- **jafont_6.tim** - Kanji page 5 (256 characters)

**Total**: 1,536 Japanese glyphs across 6 texture pages

### 2. Dialogue Files
- **jfleve.lgp** - All field map dialogue in Japanese (123MB)
- **KERNEL.BIN** - Menu text, item names, battle text (20KB)
- **kernel2.bin** - Additional kernel data (12KB)
- **WINDOW.BIN** - Window sizing and layout (13KB)

---

## Quick Start (Windows Only)

**This package requires Windows for installation!**

1. **Transfer entire `japanese-assets-extracted/` folder to Windows PC**

2. **Read the complete guide**:
   - Open `WINDOWS_INSTALLATION_GUIDE.md`
   - Follow all steps in order

3. **Required tools** (download on Windows):
   - ulgp (LGP extraction)
   - TexTool (TIM to PNG conversion)
   - FFNx with PR #737 support

4. **Summary of steps**:
   - Extract menu_ja.lgp to get jafont TIM files
   - Convert TIM to PNG
   - Copy assets to FF7 mods directory
   - Configure FFNx.toml
   - Launch ff7_en.exe

---

## Technical Details

### File Formats:

| File | Format | Size | Purpose |
|------|--------|------|---------|
| menu_ja.lgp | LGP Archive | 26MB | Contains 6 font texture files (.tim) |
| jfleve.lgp | LGP Archive | 123MB | Field dialogue scripts |
| KERNEL.BIN | Binary | 20KB | Game text database |
| kernel2.bin | Binary | 12KB | Extended kernel data |
| WINDOW.BIN | Binary | 13KB | UI layout data |

### Extraction Requirements:

**Tools needed on Windows**:
1. **ulgp** - Extracts LGP archives
   - Input: menu_ja.lgp
   - Output: jafont_1.tim through jafont_6.tim

2. **TexTool** - Converts PSX textures
   - Input: jafont_*.tim (PSX texture format)
   - Output: jafont_*.png (PNG format for FFNx)

### Target Installation Paths:

After extraction and conversion, files go here:

```
FINAL FANTASY VII/
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

---

## Prerequisites

### On Windows (required):

1. **Final Fantasy VII PC**
   - Steam 2013 version (recommended)
   - OR 1998 retail version
   - OR 2012 Square Enix eStore version

2. **FFNx Graphics Driver with PR #737**
   - Download latest release: https://github.com/julianxhokaxhiu/FFNx/releases
   - OR build from source (PR #737 branch)
   - Must have Japanese text support merged

3. **Extraction Tools**:
   - ulgp.exe (LGP extraction)
   - TexTool.exe (texture conversion)
   - Both available from Qhimm forums

### Optional but Recommended:

4. **7th Heaven Mod Manager**
   - Download: https://7thheaven.rocks/
   - Makes installation easier
   - Provides mod management UI

---

## What This Enables

After installation, you'll have:

✅ **Japanese text rendering** in ff7_en.exe (English executable)
✅ **All 1,536 Japanese characters** (Hiragana, Katakana, Kanji)
✅ **Variable-width fonts** (characters sized correctly, not "squashed")
✅ **Japanese dialogue** for all field maps
✅ **Japanese menu text** (items, magic, commands)
✅ **Japanese battle text** (attack names, status effects)

### What Works:
- Field dialogue boxes (NPC conversations)
- Menu screens (Item, Magic, Materia, etc.)
- Battle menus (Attack, Magic, Item commands)
- Character names
- Item descriptions
- Location names

### Known Issues (from PR #737):
⚠️ **Colored text** may not work correctly
⚠️ **Character input** (name entry) may be corrupted
⚠️ **Cursor alignment** may be slightly off

These are documented bugs that need fixing in PR #737.

---

## Licensing & Credits

### Source:
- **Original Assets**: Square Enix (Final Fantasy VII International Edition)
- **Extraction**: Personal backup of legally owned game
- **PR #737 Implementation**: CosmosXIII (GitHub user)
- **FFNx Driver**: Julian Xhokaxhiu and contributors

### Usage:
- These assets are for **personal use only**
- Extracted from legally owned copy of FF7 International
- Do not distribute commercially
- Credit original authors if sharing modifications

### Legal Note:
This package contains assets extracted from Final Fantasy VII International Edition.
You must own a legal copy of FF7 to use these assets.

---

## Support & Resources

### Documentation:
- **WINDOWS_INSTALLATION_GUIDE.md** - Complete installation steps
- **FFNx-japanese.toml** - Sample configuration file
- **docs/PR737_COMPLETE_ANALYSIS.md** - Technical deep-dive (in parent directory)

### Community Resources:
- **Qhimm Forums**: https://forums.qhimm.com/
- **7th Heaven Website**: https://7thheaven.rocks/
- **FFNx GitHub**: https://github.com/julianxhokaxhiu/FFNx
- **PR #737**: https://github.com/julianxhokaxhiu/FFNx/pull/737

### Getting Help:
1. Read `WINDOWS_INSTALLATION_GUIDE.md` thoroughly
2. Check FFNx.log for error messages
3. Post on Qhimm forums with:
   - FFNx.log contents
   - Your FFNx.toml configuration
   - Screenshot of issue
   - Steps to reproduce

---

## Version History

**v1.0** (2025-11-25):
- Initial extraction from FF7 International Edition
- Includes all 6 font texture files
- Includes Japanese dialogue files (field, menu, battle)
- Complete Windows installation guide
- Sample FFNx configuration

---

## File Checksums (MD5)

Use these to verify file integrity after transfer:

```
menu_ja.lgp: [Calculate on Windows]
jfleve.lgp: [Calculate on Windows]
KERNEL.BIN: [Calculate on Windows]
kernel2.bin: [Calculate on Windows]
WINDOW.BIN: [Calculate on Windows]
```

To verify on Windows:
```cmd
certutil -hashfile menu_ja.lgp MD5
certutil -hashfile jfleve.lgp MD5
certutil -hashfile KERNEL.BIN MD5
certutil -hashfile kernel2.bin MD5
certutil -hashfile WINDOW.BIN MD5
```

---

## Next Steps

1. **Read `WINDOWS_INSTALLATION_GUIDE.md`** completely
2. **Transfer this folder to Windows PC**
3. **Download required tools** (ulgp, TexTool)
4. **Follow installation guide** step by step
5. **Test in-game** and report any issues

**Good luck, and enjoy Japanese FF7! 🎮🇯🇵**

---

**Package prepared by**: Claude Code (Session 0ba935f5-efe0-457c-ad7e-c18f89cfba18)
**Source extraction date**: 2025-11-25
**Documentation version**: 1.0
