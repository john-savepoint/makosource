# FF7 Multi-Language Files Manifest

**Created:** 2025-12-22 20:55 JST (Monday)
**Last Modified:** 2025-12-22 21:50 JST (Monday)
**Version:** 1.1.0
**Author:** John Zealand-Doyle
**Session-ID:** 00f8d68d-0a0e-4b66-831e-20de2642c552

---

## Purpose

This document provides a complete manifest of all language-variant files required for FF7 multi-language support. It is intended for:

1. **Mod Distribution** - Packaging language files for redistribution
2. **Installation Scripts** - Automated file placement
3. **Verification** - Ensuring complete language support

---

## Language Codes

| Code | Language | TOML Setting |
|------|----------|--------------|
| en | English | `ff7_language = "en"` |
| ja | Japanese | `ff7_language = "ja"` |
| de | German | `ff7_language = "de"` |
| fr | French | `ff7_language = "fr"` |
| es | Spanish | `ff7_language = "es"` |

---

## File Manifest by Directory

### 1. Field Dialogue (`data/field/`)

Contains the main game dialogue and field scripts.

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `flevel_en.lgp` | ~128 MB | Renamed from original `flevel.lgp` |
| Japanese | `jfleve.lgp` | ~129 MB | Note: Typo in original naming |
| German | `gflevel.lgp` | ~128 MB | |
| French | `fflevel.lgp` | ~129 MB | |
| Spanish | `sflevel.lgp` | ~128 MB | |

**Shared Files (no variants):**
- `char.lgp` (49 MB) - Character models

---

### 2. Menu System (`data/menu/`)

Contains menu interface text and graphics.

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `menu_us.lgp` | ~1.7 MB | Default Steam file |
| Japanese | `menu_ja.lgp` | ~27 MB | Much larger - includes font data |
| German | `menu_gm.lgp` | ~1.7 MB | Note: "gm" not "de" |
| French | `menu_fr.lgp` | ~1.7 MB | |
| Spanish | `menu_sp.lgp` | ~1.7 MB | Note: "sp" not "es" |

**Shared Files (no variants):**
- `buster.tex` (67 KB) - Buster sword texture

---

### 3. CD Data (`data/cd/`)

Contains disc-related content and credits.

#### CR (Credits Roll) Files

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `cr_us.lgp` | ~2.4 MB | Default |
| Japanese | N/A | - | **NO VARIANT - uses English** |
| German | `cr_gm.lgp` | ~2.4 MB | |
| French | `cr_fr.lgp` | ~2.4 MB | |
| Spanish | `cr_sp.lgp` | ~2.4 MB | |

#### DISC Files

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `disc_us.lgp` | ~3.0 MB | Default |
| Japanese | N/A | - | **NO VARIANT - uses English** |
| German | `disc_gm.lgp` | ~3.0 MB | |
| French | `disc_fr.lgp` | ~3.0 MB | |
| Spanish | `disc_sp.lgp` | ~3.0 MB | |

**Shared Files (no variants):**
- `moviecam.lgp` (2.3 MB)

---

### 4. World Map (`data/wm/`)

Contains world map text and interfaces.

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `world_us.lgp` | ~3.1 MB | Default |
| Japanese | N/A | - | **NO VARIANT - uses English** |
| German | `world_gm.lgp` | ~3.1 MB | |
| French | `world_fr.lgp` | ~3.1 MB | |
| Spanish | `world_sp.lgp` | ~3.1 MB | |

**Shared Files (no variants):**
- `WM0.BOT`, `WM1.BOT`, `WM2.BOT`, `WM3.BOT` (6.7-16 MB each)
- `WM0.MAP`, `WM1.MAP`, `WM2.MAP`, `WM3.MAP`

---

### 5. Minigames (`data/minigame/`)

#### Chocobo Racing

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `chocobo.lgp` | ~4.6 MB | Default (lowercase) |
| Japanese | N/A | - | **NO VARIANT - uses English** |
| German | `gchocobo.lgp` | ~4.6 MB | May also be `GCHOCOBO.lgp` |
| French | `fchocobo.lgp` | ~4.6 MB | |
| Spanish | `schocobo.lgp` | ~4.6 MB | May also be `SCHOCOBO.lgp` |

#### Submarine

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `sub.lgp` | ~667 KB | Default |
| Japanese | N/A | - | **NO VARIANT - uses English** |
| German | `gsub.lgp` | ~667 KB | |
| French | `fsub.lgp` | ~667 KB | |
| Spanish | `ssub.lgp` | ~667 KB | |

#### Highwind

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `high-us.lgp` | ~2.7 MB | Note: hyphen separator |
| Japanese | N/A | - | **NO VARIANT - uses English** |
| German | `high-ge.lgp` | ~2.7 MB | Note: "ge" not "gm" |
| French | `high-fr.lgp` | ~2.7 MB | |
| Spanish | `high-sp.lgp` | ~2.7 MB | |

#### Snowboard

| Language | Filename | Size | Notes |
|----------|----------|------|-------|
| English | `snowboard-us.lgp` | ~1.7 MB | Note: hyphen separator |
| Japanese | N/A | - | **NO VARIANT - uses English** |
| German | `snowboard-ge.lgp` | ~1.7 MB | Note: "ge" not "gm" |
| French | `snowboard-fr.lgp` | ~1.7 MB | |
| Spanish | `snowboard-sp.lgp` | ~1.7 MB | |

**Shared Files (no variants):**
- `coaster.lgp` (~1.2 MB) - Gold Saucer coaster
- `condor.lgp` (~3.5 MB) - Fort Condor minigame

---

### 6. Language Override Directories

#### `data/lang-en/` - English Overrides

| Subdirectory | File | Size | Purpose |
|--------------|------|------|---------|
| `battle/` | `camdat0.bin` | 49 KB | Camera data |
| `battle/` | `camdat1.bin` | 43 KB | Camera data |
| `battle/` | `camdat2.bin` | 43 KB | Camera data |
| `battle/` | `co.bin` | 5.7 KB | Battle config |
| `battle/` | `scene.bin` | 270 KB | Battle dialogue/scenes |
| `kernel/` | `KERNEL.BIN` | 22 KB | Kernel data (larger than base) |
| `kernel/` | `kernel2.bin` | 15 KB | Extended kernel |
| `kernel/` | `WINDOW.BIN` | 13 KB | Window/font data |
| `movies/` | `ending2.avi` | 142 MB | English ending movie |
| `movies/` | `jenova_e.avi` | 12 MB | Jenova scene (English) |

#### `data/lang-ja/` - Japanese Overrides

| Subdirectory | File | Size | Purpose |
|--------------|------|------|---------|
| `battle/` | `camdat0.bin` | 49 KB | Camera data |
| `battle/` | `camdat1.bin` | 43 KB | Camera data |
| `battle/` | `camdat2.bin` | 43 KB | Camera data |
| `battle/` | `co.bin` | 5.7 KB | Battle config |
| `battle/` | `scene.bin` | 270 KB | Battle dialogue/scenes |
| `field/` | `jfleve.lgp` | 129 MB | Japanese field data (duplicate) |
| `kernel/` | `KERNEL.BIN` | 20 KB | Kernel data |
| `kernel/` | `kernel2.bin` | 12 KB | Extended kernel |
| `kernel/` | `WINDOW.BIN` | 13 KB | Window/font data |
| `menu/` | `menu_ja.lgp` | 27 MB | Japanese menu (duplicate) |
| `menu/` | `buster.tex` | 67 KB | Buster texture |
| `movies/` | `ending2.avi` | 142 MB | Japanese ending movie |
| `movies/` | `jenova_e.avi` | 12 MB | Jenova scene (Japanese) |

#### `data/lang-de/` - German Overrides

| Subdirectory | File | Size | Purpose |
|--------------|------|------|---------|
| `battle/` | `camdat0.bin` | 49 KB | Camera data |
| `battle/` | `camdat1.bin` | 43 KB | Camera data |
| `battle/` | `camdat2.bin` | 43 KB | Camera data |
| `battle/` | `co.bin` | 5.7 KB | Battle config |
| `battle/` | `scene.bin` | 279 KB | Battle dialogue/scenes (German) |
| `kernel/` | `KERNEL.BIN` | 22 KB | Kernel data |
| `kernel/` | `KERNEL2.bin` | 15 KB | Extended kernel (note: uppercase) |
| `kernel/` | `WINDOW.BIN` | 13 KB | Window/font data |
| `movies/` | `Ending2.avi` | 142 MB | German ending movie |
| `movies/` | `jenova_e.avi` | 12 MB | Jenova scene |

#### `data/lang-fr/` - French Overrides

| Subdirectory | File | Size | Purpose |
|--------------|------|------|---------|
| `battle/` | `camdat0.bin` | 49 KB | Camera data |
| `battle/` | `camdat1.bin` | 43 KB | Camera data |
| `battle/` | `camdat2.bin` | 43 KB | Camera data |
| `battle/` | `co.bin` | 5.7 KB | Battle config |
| `battle/` | `scene.bin` | 279 KB | Battle dialogue/scenes (French) |
| `kernel/` | `KERNEL.BIN` | 22 KB | Kernel data |
| `kernel/` | `kernel2.bin` | 14 KB | Extended kernel |
| `kernel/` | `window.bin` | 13 KB | Window/font data (note: lowercase) |
| `movies/` | `Ending2.avi` | 142 MB | French ending movie |
| `movies/` | `jenova_e.avi` | 12 MB | Jenova scene |

#### `data/lang-es/` - Spanish Overrides

| Subdirectory | File | Size | Purpose |
|--------------|------|------|---------|
| `battle/` | `camdat0.bin` | 49 KB | Camera data |
| `battle/` | `camdat1.bin` | 43 KB | Camera data |
| `battle/` | `camdat2.bin` | 43 KB | Camera data |
| `battle/` | `co.bin` | 5.8 KB | Battle config (slightly larger) |
| `battle/` | `scene.bin` | 279 KB | Battle dialogue/scenes (Spanish) |
| `kernel/` | `KERNEL.BIN` | 22 KB | Kernel data |
| `kernel/` | `KERNEL2.bin` | 14 KB | Extended kernel (note: uppercase) |
| `kernel/` | `WINDOW.BIN` | 13 KB | Window/font data |
| `movies/` | `Ending2.avi` | 142 MB | Spanish ending movie |
| `movies/` | `jenova_e.avi` | 12 MB | Jenova scene |

---

## Distribution Package Structure

For redistribution, organize files as follows:

```
FF7_Language_Pack/
├── README.txt
├── install.bat (or .ps1)
├── languages/
│   ├── japanese/
│   │   ├── field/
│   │   │   └── jfleve.lgp
│   │   ├── menu/
│   │   │   └── menu_ja.lgp
│   │   ├── kernel/
│   │   │   ├── KERNEL.BIN
│   │   │   ├── kernel2.bin
│   │   │   └── WINDOW.BIN
│   │   └── battle/
│   │       └── scene.bin
│   │
│   ├── german/
│   │   ├── field/
│   │   │   └── gflevel.lgp
│   │   ├── menu/
│   │   │   └── menu_gm.lgp
│   │   ├── cd/
│   │   │   ├── cr_gm.lgp
│   │   │   └── disc_gm.lgp
│   │   ├── wm/
│   │   │   └── world_gm.lgp
│   │   └── minigame/
│   │       ├── gchocobo.lgp
│   │       ├── gsub.lgp
│   │       ├── high-ge.lgp
│   │       └── snowboard-ge.lgp
│   │
│   ├── french/
│   │   ├── field/
│   │   │   └── fflevel.lgp
│   │   ├── menu/
│   │   │   └── menu_fr.lgp
│   │   ├── cd/
│   │   │   ├── cr_fr.lgp
│   │   │   └── disc_fr.lgp
│   │   ├── wm/
│   │   │   └── world_fr.lgp
│   │   └── minigame/
│   │       ├── fchocobo.lgp
│   │       ├── fsub.lgp
│   │       ├── high-fr.lgp
│   │       └── snowboard-fr.lgp
│   │
│   └── spanish/
│       ├── field/
│       │   └── sflevel.lgp
│       ├── menu/
│       │   └── menu_sp.lgp
│       ├── cd/
│       │   ├── cr_sp.lgp
│       │   └── disc_sp.lgp
│       ├── wm/
│       │   └── world_sp.lgp
│       └── minigame/
│           ├── schocobo.lgp
│           ├── ssub.lgp
│           ├── high-sp.lgp
│           └── snowboard-sp.lgp
│
└── hext/
    └── ff7/
        ├── ja/
        │   └── japanese_menu.txt
        ├── de/
        │   └── (HEXT patches if needed)
        ├── fr/
        │   └── (HEXT patches if needed)
        └── es/
            └── (HEXT patches if needed)
```

---

## Installation Paths

All files should be installed to:
```
[Steam Install]/FINAL FANTASY VII/data/[subdirectory]/
```

Default Steam path:
```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\
```

---

## Size Summary by Language

| Language | Total Size (approx) | Notes |
|----------|---------------------|-------|
| English | Included with Steam | Base installation |
| Japanese | ~160 MB | Field + Menu (large) + Kernel |
| German | ~145 MB | Field + Menu + CD + World + Minigames |
| French | ~145 MB | Field + Menu + CD + World + Minigames |
| Spanish | ~145 MB | Field + Menu + CD + World + Minigames |

**Full Multi-Language Pack:** ~595 MB (all non-English languages)

---

## Naming Convention Inconsistencies

**IMPORTANT:** The original FF7 files have inconsistent naming:

| Pattern | Used For | Examples |
|---------|----------|----------|
| Prefix (lowercase) | Field, Chocobo, Sub | `gflevel.lgp`, `fchocobo.lgp` |
| Suffix `_us/_gm/_fr/_sp` | Menu, CD, World | `menu_gm.lgp`, `cr_fr.lgp` |
| Suffix `-us/-ge/-fr/-sp` | High, Snowboard | `high-ge.lgp` (note: ge not gm!) |
| Special case | Japanese field | `jfleve.lgp` (typo: "fleve" not "flevel") |

---

## Source Locations

Files can be obtained from:

1. **Steam English Version** - Base English files included
2. **Steam Other Language Versions** - Purchase other language versions
3. **eStore Japanese Version** - Official Japanese release (D:/Games/Stand-alone/FINAL FANTASY VII/)
4. **Original PC Discs** - Multi-language retail versions

---

## FFNx Configuration

To enable a language, edit `FFNx.toml`:

```toml
# Language selection for field dialogue and all game text
# Valid values: "en", "ja", "de", "fr", "es"
ff7_language = "ja"
```

The routing is handled automatically by FFNx's `apply_language_routing()` function.

---

## Verification Checklist

### Japanese Support
- [ ] `data/field/jfleve.lgp` exists
- [ ] `data/menu/menu_ja.lgp` exists
- [ ] `data/lang-ja/kernel/KERNEL.BIN` exists
- [ ] `data/lang-ja/kernel/kernel2.bin` exists
- [ ] `data/lang-ja/kernel/WINDOW.BIN` exists
- [ ] `hext/ff7/ja/japanese_menu.txt` exists

### German Support
- [ ] `data/field/gflevel.lgp` exists
- [ ] `data/menu/menu_gm.lgp` exists
- [ ] `data/cd/cr_gm.lgp` exists
- [ ] `data/cd/disc_gm.lgp` exists
- [ ] `data/wm/world_gm.lgp` exists
- [ ] `data/minigame/gchocobo.lgp` exists
- [ ] `data/minigame/gsub.lgp` exists
- [ ] `data/minigame/high-ge.lgp` exists
- [ ] `data/minigame/snowboard-ge.lgp` exists

### French Support
- [ ] `data/field/fflevel.lgp` exists
- [ ] `data/menu/menu_fr.lgp` exists
- [ ] `data/cd/cr_fr.lgp` exists
- [ ] `data/cd/disc_fr.lgp` exists
- [ ] `data/wm/world_fr.lgp` exists
- [ ] `data/minigame/fchocobo.lgp` exists
- [ ] `data/minigame/fsub.lgp` exists
- [ ] `data/minigame/high-fr.lgp` exists
- [ ] `data/minigame/snowboard-fr.lgp` exists

### Spanish Support
- [ ] `data/field/sflevel.lgp` exists
- [ ] `data/menu/menu_sp.lgp` exists
- [ ] `data/cd/cr_sp.lgp` exists
- [ ] `data/cd/disc_sp.lgp` exists
- [ ] `data/wm/world_sp.lgp` exists
- [ ] `data/minigame/schocobo.lgp` exists
- [ ] `data/minigame/ssub.lgp` exists
- [ ] `data/minigame/high-sp.lgp` exists
- [ ] `data/minigame/snowboard-sp.lgp` exists

---

## Related Documentation

- `FFNX_DEVELOPER_GUIDE.md` - FFNx development guide
- `FF7_MULTI_LANGUAGE_IMPLEMENTATION_VERIFIED.md` - Implementation details
- FFNx source: `/mnt/c/FFNx/src/ff7/file.cpp` - Language routing code
