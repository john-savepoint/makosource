# FF7 OVA Remake - Deep Technical Investigation

**Created**: 2026-01-24 14:58 JST
**Session**: 82ef7ba5-0877-4fb2-b55c-4b4fe4cbfa6b
**Investigator**: Claude Code (Sonnet 4.5)

---

## Executive Summary

OVA Remake is a comprehensive FF7 (1998) modification that uses the **tnx3000 framework** (a fork of FFNx - Final Fantasy Remaster project) to implement visual, audio, and gameplay enhancements. Unlike simple texture mods, OVA Remake operates at multiple layers:

1. **Runtime Memory Patching** - HEXT files modify executable code in-memory
2. **Asset Replacement** - Modified LGP archives replace core game assets
3. **Direct File Overrides** - Loose files bypass LGP archives
4. **3D Mesh Replacement** - Modern GLTF format replaces PSX-era models
5. **Enhanced Audio Engine** - External music/SFX/voice/ambient layers
6. **Modified Executable** - Patched ff7.exe with tnx3000 integration

---

## Project Structure

```
ff7ovaremake_extracted/
├── archive_1_contents/          # Qt Installer metadata
├── archive_2_contents/          # Modding tools & utilities
│   └── Tools/                   # Python-based LGP extraction tools
├── archive_3_contents/          # ⭐ CORE GAME DATA
│   ├── data/                    # Modified LGP archives & kernels
│   │   ├── battle/battle.lgp    # Battle scenes (93 MB)
│   │   ├── field/char.lgp       # Character models (48 MB)
│   │   ├── field/flevel.lgp     # Field scripts & maps (133 MB)
│   │   ├── kernel/kernel2.bin   # Game mechanics data
│   │   └── wm/world_us.lgp      # World map (3 MB)
│   ├── direct/                  # Override folders (empty placeholders)
│   ├── mesh/world/              # GLTF 3D mesh replacements
│   ├── mods/textures/           # Texture overrides
│   └── ff7.exe                  # Modified executable (5.7 MB)
├── archive_4_contents/          # TurboBackend memory manager
├── archive_5_contents/          # ⭐ HEXT PATCHES & CONFIGS
│   ├── hext/ff7/{de,en,es,fr}/  # Memory patches (24 files)
│   ├── ambient/config.toml      # Ambient sound config
│   ├── lighting/config.toml     # Lighting system config
│   ├── sfx/config.toml          # Sound effects config
│   ├── time/config.toml         # Day/night cycle config
│   ├── voice/config.toml        # Voice acting config
│   └── tnx3000.toml             # Main framework config (771 lines)
└── archive_6_contents/          # 7th Heaven Workshop launcher
```

---

## Modification Mechanisms Identified

### 1. HEXT Memory Patching System

**What it is**: Runtime hex-editing that patches the game executable in memory (not on disk)

**How it works**:
- HEXT text files specify memory addresses and replacement bytes
- tnx3000 loads these on startup and applies patches
- Patches are applied after EXE loads but before game logic runs

**Example patches found**:

```hext
# FFNx._GLOBALS.txt
6E6C53 = BF    # Set dialog transparency to 75% (0xBF)

# FFNx.BATTLE.transparent_modals.txt
6E9475 = 90 90 90 90 90 90    # NOP out transparency check (enables transparency)

# FFNx.FIELD.transparent_modals.txt
6EB022 = 90 90 90 90 90 90    # NOP out field dialog opacity enforcement

# FFNx.MENU.cursor_vertical_center.txt
715240 = 14    # Adjust cursor Y position
71526B = 14    # Adjust cursor Y position

# FFNx.BATTLE.fullscreen.txt
41B51A = E0    # Battle fullscreen X coordinate adjustment
41B4E8 = 00    # Battle fullscreen Y coordinate adjustment
# ... 100+ more coordinate adjustments for fullscreen battle
```

**Purpose**:
- UI transparency modifications
- Fullscreen battle rendering adjustments
- Cursor positioning fixes
- Dialog box rendering changes

### 2. LGP Archive Replacement

**What LGP is**: Square's proprietary archive format (similar to ZIP but game-specific)

**Modified archives**:

| Archive | Size | Contents | Modifications Expected |
|---------|------|----------|------------------------|
| `battle.lgp` | 93 MB | Battle scenes, animations, models | Enhanced models, textures, animations |
| `char.lgp` | 48 MB | Character models | High-res character models |
| `flevel.lgp` | 133 MB | Field scripts, maps, backgrounds | **CRITICAL**: Field script modifications, new menus |
| `world_us.lgp` | 3 MB | World map data | World map enhancements |

**Investigation priority**: `flevel.lgp` - This is where New Threat injected menu systems

### 3. Field Script System (flevel.lgp)

**FF7 Field Scripts**:
- Each field (location) has a `.DAT` file containing:
  - Background images (pre-rendered 2D)
  - 3D model placements
  - **Field scripts** (bytecode that controls game logic)
  - Triggers, events, dialog

**How mods inject menus**:
1. Modify field script for title screen (`md8_1.dat` or similar)
2. Add opcodes to display custom menu after "NEW GAME" is selected
3. Set game variables based on menu selection
4. Branch to different field scripts or modify game state

**Example New Threat mechanism**:
```
Title Screen → NEW GAME pressed → Custom field script executes
  → Display custom window with options (Normal/Arranged mode)
  → User selects option
  → Set memory flag (e.g., 0x7C = mode selection)
  → Continue to opening sequence
  → Future scripts check flag to alter behavior
```

### 4. Kernel Modifications

**Files**:
- `kernel.bin` (23 KB) - Core game data
- `kernel2.bin` (17 KB) - Extended kernel data
- `scene.bin` (400 KB) - Battle scene definitions
- `WINDOW.BIN` (13 KB) - UI window configurations

**What these control**:
- Character stats & progression
- Materia effects & behavior
- Item definitions & effects
- Enemy AI & stats
- Battle formations & rewards
- Magic spells & limits
- Equipment stats

**Modification potential**:
- Rebalanced enemy stats
- New materia configurations
- Altered limit breaks
- Modified battle rewards
- Item stat changes

### 5. 3D Mesh Replacement (GLTF)

**Modern 3D format**: GLTF (GL Transmission Format) - industry standard

**Files found**:
```
mesh/world/
  ├── wm0.gltf (2.8 MB)      # Main world map mesh
  ├── wm2.gltf (121 KB)      # Secondary world map
  ├── wm3.gltf (18 KB)       # Tertiary world map
  ├── clouds.gltf (2.9 KB)   # Cloud effect
  ├── meteo.gltf (2.9 KB)    # Meteor effect
  ├── snake.gltf (36 KB)     # Midgar Zolom
  └── wm0_config.toml        # Mesh configuration
```

**How replacement works**:
1. tnx3000 intercepts original 3D model load requests
2. Checks `mesh/world/` for GLTF replacement
3. Loads modern GLTF instead of PSX-era model
4. Renders with modern OpenGL/DirectX/Vulkan pipeline

### 6. Enhanced Audio Engine

**Layers**:
- **Music** - External OGG files replace MIDI
- **SFX** - External sound effects (vgmstream format)
- **Voice** - Voice acting layer (auto-text advancement)
- **Ambient** - Environmental sounds

**Configuration**:
- Each layer has `config.toml` for advanced control
- Supports shuffle, sequential playback, fade in/out
- Volume control per-layer
- Music resume (world map remembers position)
- Music sync (new track starts at same timestamp)

### 7. Advanced Rendering Features

**tnx3000 features enabled**:
- 16:9 aspect ratio mode (no stretching)
- Internal resolution scaling (supersampling)
- Anisotropic filtering
- Per-vertex/per-pixel lighting (PSX-accurate or enhanced)
- Advanced lighting with real-time shadows
- Day/night cycle support
- HDR support (SDR to HDR conversion)
- NTSC-J color gamut simulation

---

## Investigation Tasks

### Task 2: Analyze HEXT Memory Patches
**Status**: In Progress
**Objective**: Document all memory addresses patched and their functional purpose
**Output**: `docs/HEXT_PATCH_ANALYSIS.md`

### Task 3: Inventory LGP Archives
**Status**: Pending
**Objective**: Extract and list all files in modified LGPs, compare to vanilla
**Output**: `docs/LGP_INVENTORY.md`

### Task 4: Analyze Modified ff7.exe
**Status**: Pending
**Objective**: Use IDA Pro MCP to decompile and identify code changes
**Output**: `docs/EXECUTABLE_ANALYSIS.md`

### Task 5: Examine Field Scripts
**Status**: Pending
**Objective**: Extract flevel.lgp, analyze field scripts for custom menu injection
**Output**: `docs/FIELD_SCRIPT_ANALYSIS.md`

### Task 6: Document 3D Mesh System
**Status**: Pending
**Objective**: Analyze GLTF meshes and replacement mechanism
**Output**: `docs/MESH_REPLACEMENT.md`

### Task 7: Analyze Kernel Modifications
**Status**: Pending
**Objective**: Compare kernel.bin/scene.bin to vanilla, document changes
**Output**: `docs/KERNEL_ANALYSIS.md`

---

## Key Questions to Answer

1. **Does OVA Remake have a custom menu system like New Threat?**
   - Need to analyze flevel.lgp field scripts
   - Check for modified title screen field
   - Look for custom menu opcodes

2. **What gameplay mechanics were changed?**
   - Analyze scene.bin for enemy/battle modifications
   - Check kernel.bin for materia/item changes
   - Compare with vanilla files

3. **How does tnx3000 integration work?**
   - Examine ff7.exe for tnx3000 hooks
   - Understand how LGP override system works
   - Trace HEXT patch application

4. **What assets were enhanced?**
   - Inventory texture replacements
   - List 3D model upgrades
   - Identify audio enhancements

---

## Technical Notes

**Coordinate System Changes (HEXT patches)**:
- Extensive battle scene coordinate adjustments (100+ patches)
- Fullscreen rendering requires repositioning UI elements
- Original game used 640x480, patches adapt to 16:9

**Memory Address Patterns**:
- `6xxxxx` range: UI rendering code
- `4xxxxx` range: Battle system code
- `7xxxxx` range: Menu system code
- `9xxxxx` range: Text rendering / cursor code

**NOP Instructions** (`90 90 90 90 90 90`):
- Used to disable code sections
- 6 bytes = disabling a conditional jump (x86-64)
- Allows transparency/rendering code to execute unconditionally

---

## Next Steps

1. Launch subagents for each investigation task
2. Extract LGP archives using tools from archive_2
3. Use IDA Pro MCP to analyze ff7.exe
4. Compare modified files with vanilla FF7
5. Document findings in structured markdown files
6. Create comprehensive modification summary

---

## References

- tnx3000 GitHub: https://github.com/julianxhokaxhiu/tnx3000
- FFNx Documentation: https://github.com/julianxhokaxhiu/FFNx
- HEXT Format: Text-based hex patching (addresses = byte values)
- GLTF Format: https://www.khronos.org/gltf/
- FF7 LGP Format: Square Enix proprietary archive
- FF7 Field Script Format: Bytecode opcodes for field events
