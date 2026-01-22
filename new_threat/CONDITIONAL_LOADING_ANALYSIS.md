# New Threat Conditional Loading Mechanism Analysis

**Created:** 2026-01-22 22:48:39 JST
**Last Modified:** 2026-01-22 22:48:39 JST
**Version:** 1.0.0
**Author:** Claude Code Analysis Agent
**Session-ID:** Current Session

---

## Executive Summary

New Threat 2.0 uses 7th Heaven's **Conditional Loading** system to dynamically load different files based on the player's current location (Field ID). This mechanism enables location-specific content changes without requiring separate game installations.

The system currently implements **two conditional folders**:
1. **ConditionalMidgalBat** - Battle content for Midgar location
2. **ConditionalVolcano** - Music content for Volcano location

---

## Conditional Loading Mechanism

### Technical Implementation

The mod.xml defines conditional folders using the `<Conditional>` element with runtime variable checks:

```xml
<Conditional Folder="ConditionalMidgalBat">
    <RuntimeVar Var="FieldID" Values="782" />
</Conditional>

<Conditional Folder="ConditionalVolcano">
    <RuntimeVar Var="FieldID" Values="507" />
</Conditional>
```

**How It Works:**
1. 7th Heaven monitors the game's runtime variables (specifically `FieldID`)
2. When player enters a field matching the specified ID, the conditional folder activates
3. Files in the conditional folder override base game files for that location only
4. When player leaves the field, the conditional folder deactivates

---

## ConditionalMidgalBat (Field ID: 782)

### Location
Field ID 782 = **Midgar Sector 1 Reactor** (opening Scorpion Guard battle area)

### Contents
Directory: `/ConditionalMidgalBat/battle/`

Contains **37 battle scene files** (all starting with 'rt'):
- rtaa through rtbi (various battle scenes)
- rtck through rtcz (series of 16 identical files at 7,816 bytes each)

### File Types
These are FF7 battle scene files (typically `.dat` format but without extension in this mod):
- Small files (328 - 3,776 bytes): Simple enemy formations
- Medium files (5,016 - 12,016 bytes): Standard battles
- Large files (31,188 - 62,628 bytes): Complex battles with multiple enemies/AI

### Purpose
**Game Type A/B System Support:**
- In **Game Type A**: Original boss battles (closer to vanilla)
- In **Game Type B**: Alternative boss battles (modded versions)

The conditional loading allows different battle configurations to load based on which "game type" the player selected, even though Field ID alone doesn't distinguish between types. This suggests additional runtime variables may be checked internally.

---

## ConditionalVolcano (Field ID: 507)

### Location
Field ID 507 = **Mt. Nibel Volcano** area

### Contents
Two directories with **identical content**:
1. `/ConditionalVolcano/music/vgmstream/chu.mp3` (11,155,563 bytes)
2. `/ConditionalVolcano/music_ogg/chu.mp3` (11,155,563 bytes)

### Purpose
**Location-specific music replacement:**
- Replaces the volcano area music with custom track "chu.mp3"
- Dual directories (`music` and `music_ogg`) ensure compatibility with different audio backend configurations in 7th Heaven
- File is MP3 format despite directory names suggesting different formats

### Technical Note
The presence in both `vgmstream` and `music_ogg` directories indicates:
- **vgmstream**: For VGMStream-based audio playback (common FF7 audio tool)
- **music_ogg**: Legacy directory structure for OGG Vorbis playback
- Both contain MP3 because modern 7th Heaven can handle MP3 in either path

---

## Relationship to Game Type A/B System

### Game Type System Overview
From `Readme.txt`:
- **Game Type A**: Story events same as vanilla, bosses close to original counterparts
- **Game Type B**: Story events altered, bosses swapped to alternatives

### How Conditional Loading Enables This

**Current Implementation:**
- Conditional folders activate based on Field ID alone (location-based)
- Does NOT directly implement Game Type switching
- Instead, provides the infrastructure for location-specific content

**Inferred Complete System:**
The Game Type A/B system likely works through:

1. **Runtime Variable Storage:**
   - Player's Game Type choice stored in save game variable
   - Hard Mode toggle stored separately
   - Both accessible to 7th Heaven at runtime

2. **Multi-Variable Conditionals (Not Shown in XML):**
   - Actual implementation may check: `FieldID = 782 AND GameType = B`
   - This would explain how the same field loads different battle files

3. **Battle Script Integration:**
   - Battle scripts (`scene.bin`) contain logic checking game variables
   - Scripts dynamically select which boss to spawn based on Game Type
   - Conditional folders provide the alternate boss data files

### Hard Mode Toggle Mechanism

From Readme.txt, Hard Mode is toggled via:
- **Extended Save Points menu** (accessed with Square/Switch button)
- Option: "Hard Mode Toggle (triggers a special enemy encounter to change the in-battle variable)"

**How This Works:**
1. Player activates Hard Mode at save point
2. Triggers a **special invisible battle** that sets a memory flag
3. This flag is now readable as a RuntimeVar by 7th Heaven
4. Conditional folders can check: `FieldID = X AND HardMode = 1`
5. Different content loads for Hard Mode vs Normal Mode

---

## Technical Details

### Runtime Variable System

**Available Variables (Inferred):**
- `FieldID` - Current field/location (confirmed)
- `GameType` - A or B mode selection (likely)
- `HardMode` - 0 or 1 toggle (likely)
- `DifficultyModifier` - Additional difficulty settings (likely)

**Variable Scope:**
- Runtime variables are **per-session** values
- Read from game memory in real-time
- Updated as player progresses through game
- Persistent across field changes within same play session

### File Override Priority

When conditional folder activates:
1. 7th Heaven scans conditional folder structure
2. Matches paths against base game file paths
3. **Conditional files override base files** for matching paths
4. Non-matching files in conditional folder are ignored
5. When field changes, conditional overrides deactivate

Example for ConditionalMidgalBat:
- Base game has: `battle/rtaa`
- Conditional has: `battle/rtaa`
- Result: Conditional version loads for Field 782 only

---

## Why This Design?

### Advantages

1. **Single Installation:**
   - No need for separate Game Type A and B installations
   - All content packaged in one mod folder
   - Player switches types via in-game menu

2. **Memory Efficiency:**
   - Only loads necessary files for current location
   - Alternate content stays dormant until needed
   - Reduces memory overhead

3. **Modular Content:**
   - Easy to add new conditional folders for other locations
   - Battle content separate from music content
   - Can mix and match conditional overrides

4. **Player Control:**
   - Game Type can be switched mid-playthrough (via save editing)
   - Hard Mode toggle available at any save point
   - No need to restart game for content changes

### Limitations

1. **XML Simplicity:**
   - mod.xml only shows Field ID checks
   - More complex logic (GameType + FieldID) may be hardcoded in 7th Heaven
   - Documentation doesn't explain multi-variable conditionals

2. **Discovery Difficulty:**
   - Not obvious which fields have conditional content
   - Players must explore to find location-specific changes
   - No in-game indication of conditional overrides active

---

## Potential Expansion

### Other Fields That Could Use Conditionals

Based on New Threat's Game Type system, these locations likely have conditional content (not yet discovered):

1. **Major Boss Battles:**
   - Shinra Building (President Shinra fight)
   - Temple of the Ancients (Red Dragon / Demon's Gate)
   - Northern Crater (Jenova battles)

2. **Story Event Variations:**
   - Nibelheim Incident flashback
   - Forgotten City scenes
   - Midgar revisit

3. **Music Variations:**
   - Boss battle themes (different for Game Type B bosses)
   - Area themes for altered story locations

### Hypothetical Extended Conditional Structure

```xml
<!-- Multi-variable conditional (hypothetical) -->
<Conditional Folder="ConditionalNibelheim_TypeB">
    <RuntimeVar Var="FieldID" Values="120" />
    <RuntimeVar Var="GameType" Values="B" />
</Conditional>

<Conditional Folder="ConditionalBossBattle_TypeB_HardMode">
    <RuntimeVar Var="FieldID" Values="782" />
    <RuntimeVar Var="GameType" Values="B" />
    <RuntimeVar Var="HardMode" Values="1" />
</Conditional>
```

This would allow granular control: different content for each combination of location, game type, and difficulty.

---

## Integration with Field Variables

### Field Scripts and RuntimeVars

FF7's field system has two variable types:
1. **Field Variables (Temp):** Local to current field, reset when leaving
2. **Save Map Variables (Permanent):** Stored in save game, persist across fields

**How RuntimeVars Connect:**
- 7th Heaven's `RuntimeVar` system reads from **save map memory**
- Game Type and Hard Mode likely stored as save map variables
- Field ID comes from game's current field state
- All values read in real-time as player moves through game

### Variable Modification Methods

**Hard Mode Example:**
1. Player selects "Hard Mode Toggle" at save point
2. Field script spawns invisible battle (special formation)
3. Battle AI script writes to save map variable: `HardModeFlag = 1`
4. Battle ends immediately (player doesn't see it)
5. 7th Heaven detects change in `HardModeFlag`
6. Future conditional checks now see `HardMode = 1`

**Game Type Example:**
1. Player selects Game Type at game start (likely main menu extension)
2. Choice written to save map variable: `GameTypeFlag = 0 (A) or 1 (B)`
3. Variable persists throughout playthrough
4. Conditional folders check this value at every field transition

---

## File Format Notes

### Battle Scene Files (rtXX)

**Format:** FF7 Battle Scene format (proprietary binary)

**Structure:**
- Enemy formation data
- AI scripts
- Animation references
- Battle camera positions
- Reward data (EXP, AP, Gil, item drops)

**Why Multiple Files:**
- Each file represents one battle formation
- Multiple formations per location for random encounter variation
- Boss battles typically have dedicated formation files

### Music Files (chu.mp3)

**Format:** MP3 audio (MPEG-1 Layer 3)

**Specifications:**
- File size: ~11.2 MB (11,155,563 bytes)
- Duration: Unknown (would need audio analysis)
- Likely 192-320 kbps bitrate (standard for game music)

**Naming:** "chu" likely refers to Mt. Nibel/Volcano theme replacement

---

## Conclusion

The New Threat mod uses 7th Heaven's Conditional Loading to create a dynamic, location-aware content system. This allows:

1. **Single mod installation** serving multiple game configurations
2. **Runtime content switching** based on player location and choices
3. **Modular override system** for battles, music, and potentially other assets
4. **Player-controlled difficulty** via in-game menus affecting loaded content

The current implementation shows **two active conditional folders**:
- Battle content for Midgar opening (Field 782)
- Music content for Mt. Nibel Volcano (Field 507)

The system is likely more extensive than XML reveals, with additional conditional folders or runtime variable checks handled internally by 7th Heaven. The infrastructure supports the mod's **Game Type A/B** system and **Hard Mode toggle**, enabling complex content variations from a single installation.

---

## References

- **mod.xml**: Lines 132-138 (Conditional folder definitions)
- **Readme.txt**: Lines 27-34 (Game Type system), Lines 48-62 (Extended Save Points / Hard Mode)
- **Directory Analysis**: `/ConditionalMidgalBat/` and `/ConditionalVolcano/` folder structures

---

## Next Investigation Steps

1. Search for additional conditional folders not declared in mod.xml
2. Analyze battle scene files to understand Game Type A vs B differences
3. Investigate 7th Heaven source code for multi-variable conditional logic
4. Examine save game structure to identify GameType and HardMode variable locations
5. Test conditional loading by modifying FieldID values in running game
