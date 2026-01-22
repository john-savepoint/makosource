# New Threat Mod - Technical Investigation Index

**Created:** 2026-01-22 22:46 JST (Wednesday)
**Session ID:** eea0d067-35d5-4ce9-9b9b-903325602c1f
**Status:** Complete
**Completed:** 2026-01-22 23:15 JST (Wednesday)

## Investigation Overview

The New Threat mod is an extensive gameplay overhaul for Final Fantasy VII that implements:
1. A custom game mode selection menu injected after pressing "NEW GAME"
2. Two distinct game modes (Type A and Type B) with different bosses and story events
3. Hard Mode toggle functionality
4. Extended save point menus with various options
5. Comprehensive battle system rebalancing
6. Modified dialogue and scenes
7. New and revised materia system

## Key Questions to Answer

1. **Menu Injection**: How does the mod inject a new menu screen after "NEW GAME"?
2. **Game Type System**: How are the two game types (A/B) implemented and switched between?
3. **Hard Mode Toggle**: What mechanism allows in-game difficulty switching?
4. **Save Point Extensions**: How are additional menu options added to save points?
5. **Battle Modifications**: How are enemy AI, stats, and formations altered?
6. **Scene Alterations**: How are story events modified for Type B mode?
7. **Kernel Changes**: How are materia, equipment, and formulas modified?

## Investigation Structure

### Component Analysis Files

1. `HEXT_PATCHES_ANALYSIS.md` - Analysis of executable patches
2. `GAME_MODE_SELECTION_ANALYSIS.md` - Menu injection mechanism
3. `KERNEL_MODIFICATIONS_ANALYSIS.md` - Battle system changes
4. `FIELD_MODIFICATIONS_ANALYSIS.md` - Dialogue and event changes
5. `SCENE_MODIFICATIONS_ANALYSIS.md` - Battle scene alterations
6. `SAVE_POINT_SYSTEM_ANALYSIS.md` - Extended menu implementation
7. `CONDITIONAL_LOADING_ANALYSIS.md` - Runtime conditional file loading

## Mod File Structure

```
New Threat/
├── mod.xml                          # 7th Heaven mod configuration
├── Readme.txt                       # Full changelog
├── hext/
│   └── NT_01.txt                   # Executable patches
├── New Threat - Sega Chief/
│   ├── battle/                     # Battle scene files
│   ├── battle.lgp/                 # Battle models/textures
│   ├── char.lgp/                   # Character models
│   ├── flevel.lgp/                 # Field files (dialogue, events, NPCs)
│   ├── kernel/                     # Battle system data
│   ├── menu/                       # Menu assets
│   ├── music/                      # Music replacements
│   └── world_us.lgp/               # World map data
├── ConditionalMidgalBat/           # Field 782 conditional files
├── ConditionalVolcano/             # Field 507 conditional files
└── OptionDifficultyModifier/       # Optional easier mode
```

## Key Mod Features to Investigate

### 1. Game Mode Selection (Priority: CRITICAL)
- Custom menu after "NEW GAME" press
- Mode A: Vanilla-like story with rebalanced bosses
- Mode B: Altered story events with different bosses
- Implementation likely involves field script modification

### 2. Hard Mode Toggle (Priority: HIGH)
- Can be toggled mid-game at save points
- Triggers special battle encounter to set variable
- Affects enemy levels, behavior, exp, and gil

### 3. Extended Save Point Menu (Priority: HIGH)
- Hotkey: Square/Switch button
- Options include:
  - Keep Field Music for Battles
  - Source Point Upgrade
  - Hard Mode Toggle
  - 0 EXP Toggle
  - Return to Highwind (location-specific)

### 4. Conditional File Loading (Priority: MEDIUM)
- Uses `RuntimeVar FieldID` system
- Loads different files for specific locations
- Example: Field 782 (Midgar Bat area), Field 507 (Volcano)

### 5. Battle System Overhaul (Priority: HIGH)
- 99% of formations restored
- All enemy AI rebalanced
- Boss variations per game type
- Damage formula modifications
- Long Range flag for enemies
- Adjusted status effects (poison, drain, etc.)

### 6. Materia System Changes (Priority: MEDIUM)
- New materia added (Omni-Plus, Hydro, Pearl, etc.)
- "Splinter" materia for single spells
- Command materia separated

### 7. Scene Modifications (Priority: MEDIUM)
- Restored deleted scenes
- New optional scenes
- Skippable flashback sequences
- Scene staging improvements

## Investigation Tasks

- [x] Read mod documentation
- [x] Analyze mod.xml structure
- [x] Examine hext patches
- [x] Investigate field files for menu injection
- [x] Analyze kernel modifications
- [x] Study scene.bin changes
- [x] Document conditional loading system
- [x] Map save point extension mechanism
- [x] Compile comprehensive technical report

## Analysis Results

### Master Report
**File:** `NEW_THREAT_TECHNICAL_MASTER_REPORT.md`
**Size:** 30+ pages comprehensive technical analysis
**Contents:** Complete breakdown of all mod mechanisms

### Component Analysis Files
1. ✅ `HEXT_PATCHES_ANALYSIS.md` - 1,127 executable patches analyzed
2. ✅ `KERNEL_MODIFICATIONS_ANALYSIS.md` - 27 kernel sections analyzed
3. ✅ `FIELD_MODIFICATIONS_ANALYSIS.md` - 702 field files analyzed
4. ✅ `SCENE_MODIFICATIONS_ANALYSIS.md` - Battle system analyzed
5. ✅ `CONDITIONAL_LOADING_ANALYSIS.md` - RuntimeVar system explained
6. ✅ `GAME_MODE_MENU_ANALYSIS.md` - Startmap injection detailed
7. ✅ `SAVE_POINT_EXTENSION_ANALYSIS.md` - Extended menu documented

## Key Findings

### 1. Game Mode Selection Menu
**Mechanism:** Complete replacement of `startmap` field file
- Uses FF7's ASK opcode (0x48) to display menu after NEW GAME
- Player selects Type A (Normal) or Type B (Arrange)
- Choice stored in save Bank 2 via SETBYTE opcode (0x80)
- All 702 field files check this variable for conditional content

### 2. Hard Mode Toggle
**Mechanism:** Special invisible battle encounter
- Field scripts limited in save variable write access
- Battle AI scripts have full memory write capabilities
- Instant-win battle used to toggle Hard Mode flag
- Clever workaround for technical limitation

### 3. Save Point Extensions
**Mechanism:** Universal field script modifications
- All 702 fields modified for consistency
- IFKEYON opcode monitors Square/Switch button
- Custom WINDOW/MENU opcodes create extended menu
- 5 options: Music, Source Upgrade, Hard Mode, 0 EXP, Teleport

### 4. Conditional Loading
**Mechanism:** 7th Heaven RuntimeVar system
- Monitors FieldID, GameType, HardMode variables
- Loads different files based on conditions
- Example: Field 782 loads different boss files for Type A/B
- Single mod installation supports multiple configurations

### 5. Battle System Overhaul
**Mechanism:** Multi-layer approach
- HEXT: 1,127 patches for damage formulas and economy
- Kernel: 13+ new materia, all stats rebalanced
- Scene.bin: Conditional AI branching for dual boss sets
- Hard Mode integration via flag checking in AI

## Statistics Summary
- **HEXT Patches:** 1,127 modifications
- **Field Files:** 702 replacements
- **Kernel Sections:** 27 modified
- **New Materia:** 13+ added
- **Boss Variations:** Dual sets (Type A/B)
- **Save Points:** ~100 enhanced with extended menu

## Subagent Assignments

Subagents will investigate specific components and output their findings to individual markdown files in this directory. Each subagent will receive:
- Specific component to investigate
- Context about FF7 file formats
- IDA Pro access for executable analysis
- Instructions to minimize response length and output analysis to markdown

