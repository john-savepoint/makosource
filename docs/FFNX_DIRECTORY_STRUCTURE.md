# FFNx Directory Structure for Japanese FF7 Mod

**Created:** 2025-12-05 00:30 JST (Friday)
**Last Modified:** 2025-12-05 00:30 JST (Friday)
**Version:** 1.0.0
**Session-ID:** c245e7c0-ec73-4933-b925-5976860e742c

---

## Overview

This document describes the correct directory structure for running FF7 with Japanese text using FFNx (PR737 or later with Japanese text support).

---

## Required FFNx.toml Settings

```toml
# Enable Japanese text mode
ff7_japanese_edition = true

# Path for extracted files (overrides LGP contents)
direct_mode_path = "direct"

# Path for HEXT memory patches
hext_patching_path = "hext"
```

---

## Complete Directory Structure

```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\
│
├── ff7_en.exe                      # English executable (we patch this at runtime)
├── FFNx.dll                        # FFNx driver (must be PR737+ for Japanese support)
├── FFNx.toml                       # Configuration file
├── FFNx.log                        # Runtime log (check for errors)
│
├── hext/                           # HEXT memory patches
│   └── ff7/
│       ├── en/                     # English patches (used when ff7_japanese_edition = false)
│       │   └── *.txt
│       └── ja/                     # Japanese patches (used when ff7_japanese_edition = true)
│           └── japanese_menu.txt   # Our menu text patches
│
├── direct/                         # Extracted files override LGP contents
│   ├── flevel/                     # Field dialogue files (MUST be extracted for Japanese)
│   │   ├── [field files]           # Individual files from jfleve.lgp
│   │   └── ...
│   ├── menu/                       # Menu assets
│   │   └── jafont_*.TEX            # Japanese font textures (optional, PNG in mods preferred)
│   ├── battle/
│   ├── char/
│   └── [other lgp names]/
│
├── mods/                           # Mod files (textures, overrides)
│   ├── Textures/
│   │   └── menu/
│   │       ├── jafont_1.png        # Japanese font texture page 1
│   │       ├── jafont_2.png        # Japanese font texture page 2
│   │       ├── jafont_3.png        # Japanese font texture page 3
│   │       ├── jafont_4.png        # Japanese font texture page 4
│   │       ├── jafont_5.png        # Japanese font texture page 5
│   │       └── jafont_6.png        # Japanese font texture page 6
│   │
│   ├── hext/                       # Backup HEXT location (FFNx checks root hext/ first)
│   │   └── ff7/ja/
│   │
│   ├── field/                      # Field-related mods
│   │   └── flevel.lgp              # Can place full LGP here (but direct/ preferred)
│   │
│   ├── kernel/                     # Kernel data
│   │   ├── KERNEL.BIN
│   │   └── kernel2.bin
│   │
│   └── lang-ja/                    # Language-specific overrides
│       ├── field/
│       │   └── jfleve.lgp          # Japanese field dialogue archive
│       └── kernel/
│           ├── KERNEL.BIN          # Japanese kernel
│           └── kernel2.bin         # Japanese kernel2 (item/magic names)
│
├── lang-ja/                        # Root language folder (alternative location)
│   ├── field/
│   │   └── jfleve.lgp
│   └── kernel/
│       ├── KERNEL.BIN
│       └── kernel2.bin
│
└── data/                           # Original game data
    ├── field/
    │   ├── flevel.lgp              # Original English field dialogue
    │   └── char.lgp
    ├── kernel/
    │   ├── KERNEL.BIN
    │   └── kernel2.bin
    └── [other data]/
```

---

## File Priority / Load Order

FFNx checks locations in this order (first found wins):

### For LGP Contents (e.g., field files)
1. `direct/[lgpname]/[filename]` - Extracted individual files
2. `mods/[lgpname].lgp/[filename]` - Files from mod LGP
3. `data/[lgpname].lgp` - Original game LGP

### For Textures
1. `mods/Textures/[category]/[filename].png`
2. `direct/[lgpname]/[filename].TEX`
3. Original LGP contents

### For HEXT Patches
1. `hext/ff7/ja/*.txt` (when `ff7_japanese_edition = true`)
2. `hext/ff7/en/*.txt` (when `ff7_japanese_edition = false`)

---

## What Each Component Does

### Japanese Font Textures (`jafont_1-6.png`)
- **Purpose:** Provide Japanese character glyphs for rendering
- **Location:** `mods/Textures/menu/`
- **Source:** Extracted from `menu_ja.lgp` using ulgp + TexTool
- **Status:** ✅ Working

### HEXT Patches (`japanese_menu.txt`)
- **Purpose:** Replace hardcoded English menu text with Japanese at runtime
- **Location:** `hext/ff7/ja/`
- **Format:** `VIRTUAL_ADDRESS = BYTE BYTE BYTE ...`
- **Status:** ✅ Working

### Kernel Files (`KERNEL.BIN`, `kernel2.bin`)
- **Purpose:** Item names, magic names, equipment names, descriptions
- **Location:** `mods/kernel/` or `lang-ja/kernel/`
- **Status:** ✅ Working (Japanese item/magic names display correctly)

### Field Dialogue (`jfleve.lgp` → extracted files)
- **Purpose:** NPC dialogue, story text, field messages
- **Location:** Must be extracted to `direct/flevel/`
- **Status:** ❌ NOT WORKING - files not extracted yet

---

## Setting Up Field Dialogue

The Japanese field dialogue (`jfleve.lgp`) must be **extracted** to work with FFNx's direct mode.

### Option 1: Extract Using ulgp (Recommended)

```cmd
cd "C:\FF7-Tools"
ulgp.exe extract "path\to\jfleve.lgp" "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\direct\flevel"
```

### Option 2: Use Unmass

```cmd
unmass.exe "path\to\jfleve.lgp" -o "direct\flevel"
```

### Verification

After extraction, `direct/flevel/` should contain hundreds of files like:
```
ancnt1
ancnt2
blin1
...
md1stin
md1_1
...
```

---

## Troubleshooting

### Menu text shows garbage
- ✅ Check `ff7_japanese_edition = true` in FFNx.toml
- ✅ Check `hext/ff7/ja/japanese_menu.txt` exists
- ✅ Check FFNx.log for "Applied Hext patch"

### Field dialogue still English
- ❌ `direct/flevel/` is empty
- **Fix:** Extract jfleve.lgp to this folder

### Font textures not loading
- ✅ Check `mods/Textures/menu/jafont_*.png` exist
- ✅ Check files are PNG format, not TEX

### HEXT patches not applying
- Check you're using `/ja/` folder, not `/en/`
- Check virtual addresses are correct (not file offsets)
- Check FFNx.log for HEXT-related messages

---

## Quick Checklist

- [ ] `FFNx.toml` has `ff7_japanese_edition = true`
- [ ] `hext/ff7/ja/japanese_menu.txt` exists with patches
- [ ] `mods/Textures/menu/jafont_1-6.png` exist
- [ ] `mods/kernel/kernel2.bin` is Japanese version
- [ ] `direct/flevel/` contains extracted Japanese field files
- [ ] FFNx.log shows "Applied Hext patch" messages

---

## See Also

- `HEXT_PATCHING_GUIDE.md` - How to create HEXT patches
- `MENU_TEXT_ADDRESS_MAP.md` - Complete address reference
- `SESSION_HANDOFF_2025-12-05_COMPREHENSIVE.md` - Full session details
