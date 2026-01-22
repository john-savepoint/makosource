# New Threat Mod - Quick Reference: Core Mechanisms

**Created:** 2026-01-22 23:15 JST (Wednesday)
**Session ID:** eea0d067-35d5-4ce9-9b9b-903325602c1f

---

## How the Custom "NEW GAME" Menu Works

**What You See:**
After pressing NEW GAME, a menu appears with Cloud, Tifa, and Yuffie in the background, asking you to choose between "Normal Mode" (Type A) or "Arrange Mode" (Type B).

**How It's Done:**
```
1. FF7 loads "startmap" field file after NEW GAME
2. New Threat replaces this field entirely
3. Replacement field contains:
   - Character model loading commands
   - ASK opcode (0x48) - displays 2-3 choice menu
   - Player selection captured
   - SETBYTE opcode (0x80) - writes choice to save Bank 2
   - MAPJUMP opcode - transitions to first reactor
4. Game continues normally with Type A/B flag set
```

**Technical Details:**
- **File:** `flevel.lgp/startmap*`
- **Size:** 377 bytes dialogue + 2.1KB script
- **Save Variable:** Bank 2, offset 0x00 (0x00 = Type A, 0x01 = Type B)
- **Key Opcode:** ASK (0x48) for menu display

---

## How Game Type A/B Switching Works

**Implementation Strategy:**

### Level 1: Save Variable
```
startmap field writes to save Bank 2:
  Type A (Normal) = 0x00
  Type B (Arrange) = 0x01
```

### Level 2: Field Scripts Check Variable
```
All 702 field files contain:
  GETBYTE Bank2, 0x00 → GameType
  IF GameType == 0x00:
      [Type A content: dialogue, bosses, events]
  ELSE:
      [Type B content: alternative versions]
  ENDIF
```

### Level 3: Battle AI Checks Variable
```
scene.bin AI scripts:
  [Initialization]
  GETVAR GameTypeFlag → VAR_A

  IF VAR_A == 0:
      Load Type A boss stats
      Execute Type A behavior
  ELSE:
      Load Type B boss stats
      Execute Type B behavior
  ENDIF
```

### Level 4: 7th Heaven Conditional Loading
```xml
<Conditional Folder="ConditionalMidgalBat">
  <RuntimeVar Var="FieldID" Values="782" />
  <!-- Loads Type A or B boss files based on save variable -->
</Conditional>
```

**Result:** Single scene.bin, single field set, dual content via conditional branching

---

## How Hard Mode Toggle Works

**The Challenge:**
Field scripts can't directly write to all save memory locations.

**The Solution:**
Use a battle encounter as a "system call" to write variables.

**Implementation:**
```
[Player at Save Point]
1. Presses Square/Switch
2. Extended menu appears
3. Selects "Hard Mode Toggle"
4. Field script: BATTLE FormationID_HardModeToggle
5. Battle loads (invisible/instant-win enemy)
6. Enemy AI script: SETVAR HardModeFlagOffset, [new value]
7. Battle ends immediately
8. Player returns to field with flag toggled
9. All battles read flag and adjust stats/AI accordingly
```

**Why It Works:**
- Battle AI scripts have full memory write access
- Field scripts have limited write access
- Instant battle is invisible workaround
- Player sees brief transition, flag is set, continues playing

---

## How Extended Save Point Menu Works

**What You See:**
At save points, press Square/Switch for extended menu:
1. Keep Field Music for Battles
2. Source Point Upgrade
3. Hard Mode Toggle
4. 0 EXP Toggle
5. Return to Highwind (location-specific)

**How It's Done:**

### Step 1: Hotkey Detection
```
[Field Script Main Loop]
IFKEYON 0x0040:  // Square/Switch button
    CALL Extended_Menu_Routine
ENDIF
```

### Step 2: Menu Display
```
[Extended_Menu_Routine]
WINDOW 10, 10, 220, 150
MENU 5:
    "Keep Field Music for Battles"
    "Source Point Upgrade"
    "Hard Mode Toggle"
    "0 EXP Toggle"
    "Return to Highwind"

GETMENUSELECTION → SELECTED_OPTION
```

### Step 3: Option Execution

**Option 1 - Music Toggle:**
```
GETBYTE Bank3, MusicFlag → VALUE
SETBYTE Bank3, MusicFlag, !VALUE
```

**Option 2 - Source Upgrade:**
```
Display character selection submenu (9 options)
ADDSTAT CHARACTER_ID, [ALL_STATS], +[values]
SETBYTE Bank4, SourcePoints, SourcePoints - 1
```

**Option 3 - Hard Mode:**
```
BATTLE HardModeToggleFormation
// Battle AI writes flag
```

**Option 4 - 0 EXP:**
```
GETBYTE Bank3, ZeroEXPFlag → VALUE
SETBYTE Bank3, ZeroEXPFlag, !VALUE
```

**Option 5 - Teleport:**
```
IF CurrentField IN [North Crater range]:
    MAPJUMP HighwindFieldID, X, Y
ELSE:
    MESSAGE "Cannot use here"
ENDIF
```

**Implementation Scope:**
- All 702 field files modified
- Universal consistency
- ~100 fields have actual save points

---

## How Conditional Loading Works

**7th Heaven's RuntimeVar System:**

### Configuration (mod.xml):
```xml
<Conditional Folder="ConditionalMidgalBat">
  <RuntimeVar Var="FieldID" Values="782" />
</Conditional>
```

### Runtime Process:
```
1. Game requests file (e.g., battle scene for Field 782)
2. 7th Heaven intercepts request
3. Checks RuntimeVar conditions:
   - Current FieldID = 782? ✓
   - GameType variable = ? (reads from save)
   - HardMode variable = ? (reads from save)
4. If conditions match:
   Load file from ConditionalMidgalBat folder
5. Else:
   Load file from main mod folder
6. Else:
   Load base game file
```

### File Priority:
```
Conditional Folder (highest)
    ↓
Main Mod Folder
    ↓
Base Game Files (lowest)
```

### Example: Boss Variation at Field 782
```
Player at Field 782, Type A selected:
  → Loads ConditionalMidgalBat/TypeA/scene files
  → Original Scorpion Sentinel boss

Player at Field 782, Type B selected:
  → Loads ConditionalMidgalBat/TypeB/scene files
  → Alternative boss encounter
```

**Result:** Single mod installation, multiple configurations, seamless switching

---

## How Battle System Rebalancing Works

**Multi-Layer Approach:**

### Layer 1: HEXT Patches (1,127 modifications)
```
Modify ff7.exe directly:
  - Damage formula calculations
  - Critical: +100% → +50%
  - Elemental: +100% → +50%
  - Barrier: 50% → 33% reduction
  - Back Row: 50% → 10% reduction
  - Drain: 100% → 12.5% effectiveness

  - Economy data (4,913 bytes)
  - Shop prices
  - Equipment costs
  - Item values
```

### Layer 2: Kernel Modifications
```
KERNEL.BIN (9 sections):
  - Command data (new materia)
  - Attack data (revised formulas)
  - Battle/growth (stat progression)
  - Character init (starting stats)
  - Item/weapon/armor/accessory (all rebalanced)
  - Materia data (13+ new added)

kernel2.bin (18 sections):
  - All text names/descriptions updated
```

### Layer 3: Scene.bin Modifications
```
Single 336 KB file:
  - All 128 enemy stats revised
  - All AI scripts rewritten
  - Dual boss sets (Type A/B)
  - Formation tables updated
  - Counter attack labels added
```

### Layer 4: Integration
```
All layers coordinate:
  - HEXT modifies calculation engine
  - Kernel provides stat data
  - Scene provides enemies/AI
  - Field provides story/events
  - RuntimeVar provides switching
```

---

## Technical Stack Summary

| Component | Mechanism | Purpose |
|-----------|-----------|---------|
| **Game Mode Menu** | startmap field replacement | Capture player choice |
| **Mode Switching** | Save variables + conditional branching | Dual content in single files |
| **Hard Mode** | Battle encounter variable writer | Toggle difficulty mid-game |
| **Save Point Menu** | Field script hotkey detection | Extended options |
| **Conditional Loading** | 7th Heaven RuntimeVar | Dynamic file swapping |
| **Battle Balance** | HEXT + Kernel + Scene | Comprehensive rebalancing |
| **New Materia** | Kernel data additions | Strategic options |
| **NPC Additions** | Field script expansion | Enhanced dialogue |

---

## Save Variable Map

**Bank 2 (Progression Flags):**
- Offset 0x00: Game Type (0x00 = Type A, 0x01 = Type B)
- Offset 0x01: Hard Mode Flag (0x00 = Off, 0x01 = On)

**Bank 3 (Gameplay Options):**
- Offset 0x00: Keep Field Music Flag
- Offset 0x01: Zero EXP Flag

**Bank 4 (Custom Counters):**
- Offset 0x00: Source Points Available Count

---

## Key Opcodes Used

| Opcode | Hex | Purpose |
|--------|-----|---------|
| ASK | 0x48 | Display menu with choices |
| SETBYTE | 0x80 | Write byte to save variable |
| GETBYTE | - | Read byte from save variable |
| IFKEYON | - | Check button press |
| WINDOW | - | Create menu window |
| MENU | - | Display menu options |
| MAPJUMP | - | Teleport to field |
| BATTLE | - | Trigger battle encounter |
| ADDSTAT | - | Modify character stat |

---

## File Modification Summary

| File Type | Count | Purpose |
|-----------|-------|---------|
| HEXT patches | 1,127 | Executable modifications |
| Field files | 702 | Scripts, dialogue, events |
| Kernel sections | 27 | Battle system data |
| Scene.bin | 1 | Enemy AI and stats |
| Conditional folders | 2 | Dynamic content |
| Configuration | 1 | mod.xml for 7th Heaven |

---

## Development Techniques

### 1. Menu Injection
**Technique:** Replace initial field file
**Advantage:** No executable patching needed
**Implementation:** Complete startmap replacement

### 2. Variable Writer Pattern
**Technique:** Use battle as system call
**Advantage:** Bypass field script limitations
**Implementation:** Instant-win battles set variables

### 3. Conditional AI
**Technique:** Single file, branching logic
**Advantage:** Cleaner than file duplication
**Implementation:** AI scripts check flags

### 4. RuntimeVar Loading
**Technique:** 7th Heaven monitoring
**Advantage:** Dynamic file switching
**Implementation:** XML conditional definitions

### 5. Universal Modification
**Technique:** Apply to all 702 fields
**Advantage:** Consistency across game
**Implementation:** Scripted modification process

---

## Compatibility Notes

**Compatible With:**
- Translation mods (requires field/kernel merging)
- Graphics mods (models, textures, shaders)
- Music mods (can layer)
- UI mods (with careful field merging)

**Conflicts With:**
- Other difficulty mods (same stats modified)
- Other battle balance mods (formulas conflict)
- Other save point extension mods (script conflicts)

**Requirements:**
- 7th Heaven mod manager
- Memory region 0x913D00-0x913D7F reserved
- Save Bank 2 offsets 0x00-0x40 reserved

---

**End of Quick Reference**

For complete technical details, see `NEW_THREAT_TECHNICAL_MASTER_REPORT.md`
