---
title: "FF7 Modding Tools Matrix"
created: "2025-12-06 14:58 JST (Saturday)"
modified: "2025-12-06 14:58 JST (Saturday)"
session_id: "7c8fb557-f9d0-4ef3-bc4d-b714c40bb0a1"
author: "John Zealand-Doyle / Claude Code"
version: "1.0.0"
---

# FF7 Modding Tools Matrix

A comprehensive catalog of all tools for modding Final Fantasy VII (PC), organized by function with capability matrices.

---

## Quick Reference Matrix

### Tool Categories at a Glance

| Category | Tool Count | Primary Use |
|----------|------------|-------------|
| Archive Tools | 7 | Extract/repack LGP archives |
| Texture Tools | 6 | Convert TEX/TIM/PNG/BMP formats |
| Model Viewers | 3 | View 3D models and textures |
| Field Editors | 4 | Edit backgrounds, scripts, dialogue |
| Battle/Enemy Editors | 5 | Modify enemies, AI, encounters |
| Kernel/Data Editors | 4 | Edit items, materia, limits |
| Save Editors | 1 | Edit save game files |
| Memory/Hex Tools | 2 | Runtime memory editing |
| Sound Tools | 2 | Edit sound effects and music |
| Translation Tools | 2 | Edit game text and dialogue |
| Graphics Drivers | 2 | Enhanced rendering |

---

## Archive Tools (LGP Handling)

Tools for extracting and repacking FF7's LGP archive format.

| Tool | Author | Version | CLI | GUI | Extract | Repack | Partial Update | Status |
|------|--------|---------|-----|-----|---------|--------|----------------|--------|
| **ulgp** | Luksy/Aali | 1.3.2 | ✅ | ✅ | ✅ | ✅ | ✅ | ⭐ RECOMMENDED |
| LGP/UnLGP | Aali | 0.5b | ✅ | ❌ | ✅ | ✅ | ❌ | Current |
| Unmass | Mirex | 0.82 | ❌ | ✅ | ✅ | ❌ | ❌ | Current |
| LGPTools | Ficedula | 1.60 | ❌ | ✅ | ✅ | ✅ | ❌ | ⚠️ Deprecated |
| Highwind | Christian | 1.20 | ❌ | ✅ | ✅ | ✅ | ❌ | ⚠️ Deprecated |
| Kaddy | Alhexx | 1.11 | ✅ | ❌ | ✅ | ✅ | ❌ | ⚠️ Deprecated |
| Aeris | The SaiNt | 1.0 | ❌ | ✅ | ✅ | ❌ | ❌ | ⚠️ Deprecated |

### ulgp Commands (Recommended Tool)

```bash
# Extract entire archive
ulgp -x menu_us.lgp

# Create archive from folder
ulgp -c menu_us.lgp

# Overwrite files in existing archive (KEY FEATURE)
ulgp -r menu_us.lgp

# Extract specific file
ulgp -d menu_us.lgp output_folder

# Insert specific file
ulgp -i menu_us.lgp specific_file.tex
```

**Download**: https://forums.qhimm.com/index.php?topic=12831.0

---

## Texture Conversion Tools

Tools for converting between FF7's TEX format and standard image formats.

| Tool | Author | Version | TEX→IMG | IMG→TEX | Batch | Formats | Platform |
|------|--------|---------|---------|---------|-------|---------|----------|
| **Image2TEX** | Borde | Latest | ✅ | ✅ | ✅ | BMP, JPG, GIF | Windows |
| **Tex Tools** | Community | 1.0.4.7 | ✅ | ✅ | ✅ | PNG, JPG, BMP, TIFF | Windows |
| Omega | M4v3R | 1.3 | ✅ | ✅ | ❌ | BMP | Windows |
| tim2png | cebix | Latest | ✅ | ❌ | ❌ | PNG (TIM input) | Python |
| FFNx Dumping | julianxhokaxhiu | - | ✅ | ❌ | Auto | PNG | In-game |
| TEX→BMP (Pascal) | Hoehrmann | 1998 | ✅ | ❌ | ❌ | BMP | Reference |

### Texture Format Notes

| Format | Description | Use Case |
|--------|-------------|----------|
| TEX | FF7 PC native texture | Game assets in LGP |
| TIM | PlayStation texture | PSX version analysis |
| PNG | Portable Network Graphics | FFNx mod_path overrides |
| BMP | Windows Bitmap | Image2TEX conversion |
| DDS | DirectDraw Surface | FFNx high-res textures |

### FFNx Texture Override Configuration

```toml
# FFNx.toml settings
mod_path = "mods/Textures"
mod_ext = ["dds", "png"]
save_textures = true   # Dump textures for extraction
show_missing_textures = true
```

**Image2TEX Download**: https://github.com/niemasd/Image2TEX
**Tex Tools Download**: https://forums.qhimm.com/index.php?topic=17755.0

---

## 3D Model Viewers

Tools for viewing FF7's 3D models and textures.

| Tool | Author | Version | Field Models | Battle Models | Enemy Models | Export | Import |
|------|--------|---------|--------------|---------------|--------------|--------|--------|
| **Biturn** | Mirex | 0.87b4 | ✅ | ✅ | ✅ | ✅ | ❌ |
| Leviathan | Mirex | 0.41 | ❌ | ❌ | ✅ | ❌ | ❌ |
| Kimera | Borde | 0.96b | ✅ (.P files) | ❌ | ❌ | ✅ | ✅ |

### Model Format Reference

| Format | Location | Description |
|--------|----------|-------------|
| .P | flevel.lgp | Field character models |
| .BCX | char.lgp | Battle character models |
| Scene.bin | battle/ | Enemy model references |
| .HRC | char.lgp | Skeleton hierarchy |
| .RSD | char.lgp | Resource definition |
| .A | char.lgp | Animation data |

**Biturn Download**: http://mirex.mypage.sk/index.php?selected=1#Biturn
**Leviathan Download**: http://mirex.mypage.sk/index.php?selected=1#Leviathan

---

## Field Editors

Tools for editing field backgrounds, scripts, and dialogue.

| Tool | Author | Version | Backgrounds | Scripts | Dialogue | Walkmesh | Encounters | Cross-Platform |
|------|--------|---------|-------------|---------|----------|----------|------------|----------------|
| **Makou Reactor** | myst6re | 1.7.2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Palmer | Aali | 0.6b | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Meteor | Synergy Blades | 0.2b | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Hack7 | lasyan3 | v3 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Cosmo | Ficedula | 0.95c | ❌ | ❌ | ✅ | ❌ | ❌ | ⚠️ Deprecated |
| Loveless | Squall78 | 2.4 | ❌ | ❌ | ✅ | ❌ | ❌ | ⚠️ Deprecated |

**Makou Reactor Download**: https://forums.qhimm.com/index.php?topic=9658.0

---

## Battle & Enemy Editors

Tools for modifying enemies, AI scripts, and battle mechanics.

| Tool | Author | Version | Enemy Stats | AI Scripts | Attacks | Formations | Scene.bin |
|------|--------|---------|-------------|------------|---------|------------|-----------|
| **Proud Clod** | NFITC1 | 1.5.0.α_4 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hojo | Squall78 | 1.1 | ✅ | ❌ | ❌ | ❌ | ✅ |
| FF7 Enemy Manipulator | drdimension | 0.9.2 | ✅ (bulk) | ❌ | ❌ | ❌ | ❌ |
| SceneEdit | M4v3R | 1.3.0 | ✅ | ✅ | ❌ | ❌ | ⚠️ Deprecated |
| Scenester | Lord Ramza | Beta | ✅ | ❌ | ❌ | ❌ | ⚠️ Deprecated |
| Scene Reader | M4v3R | 1.0 | ❌ | ❌ | ❌ | ❌ | ⚠️ Deprecated |

**Proud Clod Download**: https://forums.qhimm.com/index.php?topic=8481.0
**Hojo Download**: https://forums.qhimm.com/index.php?topic=7186.0

---

## Kernel & Data Editors

Tools for editing items, materia, weapons, and core game data.

| Tool | Author | Version | Items | Materia | Weapons | Armor | Limits | Shops |
|------|--------|---------|-------|---------|---------|-------|--------|-------|
| **WallMarket** | NFITC1 | 1.4.5 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| WhiteChoco | titeguy3 | 0.7b | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| LiBrE | Bosola | 0.3 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| PCreator | Reunion | 0.85b | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Kernel Files Reference

| File | Description | Editor |
|------|-------------|--------|
| KERNEL.BIN | Core game data (items, materia, etc.) | WallMarket |
| kernel2.bin | Text strings for kernel data | WallMarket |
| SHOPMENU.MNU | Shop inventory and prices | WhiteChoco |

**WallMarket Download**: https://forums.qhimm.com/index.php?topic=7928.0

---

## Memory & Hex Editing Tools

Tools for runtime memory editing and hex manipulation.

| Tool | Author | Version | Runtime Edit | Hex Edit | Text Edit | Trainer |
|------|--------|---------|--------------|----------|-----------|---------|
| **Ochu** | DLPB | 3.2 | ✅ | ✅ | ❌ | ✅ |
| DLPB Tools | DLPB | 3.0 | ✅ | ✅ | ✅ | ❌ |

### Memory Editing Features

| Feature | Ochu | DLPB Tools |
|---------|------|------------|
| View game memory | ✅ | ✅ |
| Edit memory values | ✅ | ✅ |
| Save/Load states | ✅ | ❌ |
| Built-in cheats | ✅ | ❌ |
| File hex editing | ❌ | ✅ |
| Text file editing | ❌ | ✅ |

**Ochu Download**: https://forums.qhimm.com/index.php?topic=14194.0
**DLPB Tools Download**: https://forums.qhimm.com/index.php?topic=13574.0

---

## Save Game Editors

| Tool | Author | Version | PC Saves | PSX Saves | Cross-Platform | Open Source |
|------|--------|---------|----------|-----------|----------------|-------------|
| **Black Chocobo** | Sithlord48 | 1.9.90 | ✅ | ✅ | ✅ | ✅ |

### Save Data Categories

| Category | Editable |
|----------|----------|
| Character stats | ✅ |
| Inventory | ✅ |
| Materia | ✅ |
| Gil | ✅ |
| Game progress | ✅ |
| Chocobo data | ✅ |
| Location | ✅ |

**Black Chocobo Download**: http://www.blackchocobo.com

---

## Sound & Music Tools

| Tool | Author | Version | Sound Effects | Music | Encode | Decode |
|------|--------|---------|---------------|-------|--------|--------|
| sfxEdit | Luksy | 0.2 | ✅ | ❌ | ✅ | ✅ |
| FF7Midi | Ficedula | 1.01 | ❌ | ✅ | ❌ | ✅ | ⚠️ Deprecated |
| Anxious Heart | DLPB | A05 | ❌ | ✅ (replacement) | ❌ | ❌ |

**sfxEdit Download**: https://forums.qhimm.com/index.php?topic=12755.0

---

## Translation & Text Tools

| Tool | Author | Version | All Text | Auto-resize | Script Fix | CLI |
|------|--------|---------|----------|-------------|------------|-----|
| **touphScript** | Luksy | 1.3.1 | ✅ | ✅ | ✅ | ✅ |
| BoxFF7 | DLPB | 2.0 | ❌ | ✅ | ❌ | ❌ |

### Text System Scope

| Scope | touphScript | BoxFF7 |
|-------|-------------|--------|
| Field dialogue | ✅ | ✅ |
| Menu text | ✅ | ❌ |
| Battle text | ✅ | ❌ |
| Item/Materia names | ✅ | ❌ |
| Window positioning | ❌ | ✅ |
| Window sizing | ✅ | ✅ |

**touphScript Download**: https://forums.qhimm.com/index.php?topic=11944.0

---

## Graphics Drivers & Renderers

| Tool | Author | Version | OpenGL | High-Res | Texture Override | Active |
|------|--------|---------|--------|----------|------------------|--------|
| **FFNx** | julianxhokaxhiu | Latest | ✅ | ✅ | ✅ | ✅ CURRENT |
| Aali's OpenGL Driver | Aali | 0.8.1b | ✅ | ✅ | ❌ | Legacy |

### FFNx Key Features

| Feature | Support |
|---------|---------|
| Texture replacement via mod_path | ✅ |
| Texture dumping | ✅ |
| High resolution rendering | ✅ |
| Widescreen support | ✅ |
| 60fps battles | ✅ |
| Multi-language support | ✅ |
| PNG/DDS texture loading | ✅ |

**FFNx Download**: https://github.com/julianxhokaxhiu/FFNx/releases

---

## Mod Compilation & Distribution

| Tool | Author | Description | Status |
|------|--------|-------------|--------|
| **7th Heaven** | Community | Mod manager with IRO format | ⭐ CURRENT |
| The Reunion | DLPB et al | Compilation mod pack | Current |
| YAMP | dziugo | Multi-patcher | Legacy |
| Bootleg | Community | Mod installer | Legacy |
| FF7 Remix Patch | titeguy3 | Compilation (outdated) | ⚠️ Deprecated |
| Cetra | Ficedula | Patch manager | ⚠️ Deprecated |

**7th Heaven Download**: https://7thheaven.rocks/

---

## AI Modification Projects

These are complete gameplay modifications, not editing tools:

| Mod | Author | Difficulty | Status |
|-----|--------|------------|--------|
| **New Threat Mod** | Sega Chief | Complete overhaul | ✅ Active |
| Gjoerulv's Hardcore | Gjoerulv | Extreme difficulty | Complete |
| Reasonable Difficulty | hay | Balanced | Complete |
| FF7: Rebirth | Bosola | Rebalance | ⚠️ Abandoned |
| Climhazzard | ff7rules | PSX only | ⚠️ Abandoned |
| Shalua Rui | Auraplatonic | Balanced | ⚠️ Abandoned |

---

## Video Tools

| Tool | Author | Version | Extract | Encode | Quality |
|------|--------|---------|---------|--------|---------|
| **jPSXdec** | m-35 | 0.99.6 | ✅ | ❌ | Best quality |
| TrueMotion 2.0 | On2 | 2.0 | ❌ | ❌ | ⚠️ Deprecated |

**jPSXdec Download**: http://kenai.com/projects/jpsxdec/pages/Home

---

## Memory Address Reference (For Ochu/DLPB Tools)

Common memory locations for runtime editing:

| Category | Address Range | Description |
|----------|---------------|-------------|
| Party data | Varies | Character stats, equipment |
| Inventory | Varies | Items, quantities |
| Game flags | Varies | Story progression |
| Battle state | Varies | HP, MP, status |

For specific addresses, consult the FF7 Memory Hacking documentation on Qhimm forums.

---

## Workflow Summary: Tool Selection by Task

### "I want to edit textures/fonts"
1. **ulgp** → Extract from LGP
2. **Image2TEX** or **Tex Tools** → Convert TEX to PNG/BMP
3. **GIMP/Photoshop** → Edit images
4. **Image2TEX** → Convert back to TEX
5. **ulgp** → Repack into LGP
6. *Alternative*: Use **FFNx** mod_path for PNG override (no repacking needed)

### "I want to edit dialogue/text"
1. **touphScript** → Extract and edit all game text
2. **Makou Reactor** → For field-specific script editing
3. **BoxFF7** → For dialogue box positioning

### "I want to edit enemies/battles"
1. **Proud Clod** → Enemy stats, AI, attacks, formations
2. **Hojo** → Simple stat editing

### "I want to edit items/materia"
1. **WallMarket** → KERNEL.BIN editing

### "I want to edit saves"
1. **Black Chocobo** → Cross-platform save editor

### "I want to view/edit memory at runtime"
1. **Ochu** → Trainer and memory editor
2. **DLPB Tools** → Hex editing

### "I want to view 3D models"
1. **Biturn** → General model viewer
2. **Leviathan** → Enemy model viewer

---

## Resources

### Primary Forums
- **Qhimm Forums**: https://forums.qhimm.com/

### Documentation
- **FF7 Wiki (Qhimm)**: https://qhimm-modding.fandom.com/wiki/
- **FF7 Flat Wiki**: https://ff7-mods.github.io/ff7-flat-wiki/

### GitHub Repositories
- **FFNx**: https://github.com/julianxhokaxhiu/FFNx
- **ff7tools**: https://github.com/cebix/ff7tools
- **Image2TEX**: https://github.com/niemasd/Image2TEX

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ⭐ | Recommended tool for this category |
| ✅ | Feature supported / Active project |
| ❌ | Feature not supported |
| ⚠️ | Deprecated - use alternatives |
| CLI | Command-line interface |
| GUI | Graphical user interface |
