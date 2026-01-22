# FF7 Multi-Party Battle System & Multiplayer Feasibility Analysis

**Created**: 2026-01-16 14:38:55 JST (Thursday)
**Session ID**: 0218ee3c-5e2d-4970-8fb8-9d1e701db4ab
**Author**: John Zealand-Doyle
**Topic**: Bizarro Sephiroth multi-party mechanics, custom boss applications, multiplayer implementation feasibility

---

## Executive Summary

This document analyzes Final Fantasy VII's unique multi-party battle system as exemplified by the Bizarro Sephiroth boss fight, examines the feasibility of applying this mechanic to other bosses, and evaluates the possibility of implementing networked multiplayer battles using FFNx hooks. Key findings:

1. **Multi-party mechanics are script-driven** - Not hardcoded to Bizarro Sephiroth
2. **Application to other bosses is feasible** - Requires AI script modification and field script coordination
3. **Multiplayer is theoretically possible** - FFNx has necessary hooks, but requires extensive networking infrastructure
4. **9-character simultaneous rendering is impractical** - Engine designed for 3 active characters maximum

---

## Part 1: Bizarro Sephiroth Multi-Party Mechanics

### How the System Works

The Bizarro Sephiroth battle demonstrates FF7's most complex party rotation system. Analysis of the AI script reveals the following key mechanics:

#### Global Variable Party Switching

```
GlobalVar:ChangeParty - Party switching trigger values:
  - Value 0 = No switch
  - Value 5 = Switch to Sub1 party
  - Value 6 = Switch to Sub2 party
```

The AI script sets this value in the **Counter - Death** section when specific parts are destroyed:

```
If (Self is TempVar:Head) Then {
    Print Message [Head Portion (B) Dead]
    GlobalVar:ChangeParty = 5  ← Triggers party switch
}

If (Self is TempVar:Core) Then {
    Print Message [Core (C) Dead]
    GlobalVar:ChangeParty = 6  ← Triggers party switch
}
```

#### Death Tracking Across Parties

The system uses persistent GlobalVars to track which parts have been destroyed across all three parties:

```
GlobalVar:BzDead-MainHead = 0/1
GlobalVar:BzDead-MainCore = 0/1
GlobalVar:BzDead-MainRMgc = 0/1
GlobalVar:BzDead-MainLMgc = 0/1
GlobalVar:BzDead-Sub1Core = 0/1
GlobalVar:BzDead-Sub1LArm = 0/1
GlobalVar:BzDead-Sub2Core = 0/1
GlobalVar:BzDead-Sub2LArm = 0/1
... etc
```

This allows the boss to "remember" progress when control rotates between parties.

#### Multi-Target Formation

Bizarro Sephiroth consists of 5 independently targetable entities:

- **Bizarro·Sephiroth A** (Main Body) - Controls the battle logic
- **Bizarro·Sephiroth B** (Head) - Can be killed and revived
- **Bizarro·Sephiroth C** (Core) - Protected until magic parts die
- **Bizarro·Sephiroth D** (Right Magic) - Absorbs Ice/Lightning
- **Bizarro·Sephiroth E** (Left Magic) - Absorbs Ice/Lightning

Each has independent HP pools calculated based on character level and story progression:

```
TempVar:MainBody's Max HP = 40000 + TempVar:CharLv99 * 5000 + TempVar:JenovaBonus
TempVar:Head's Max HP = 4000 - ((8 - TempVar:CharLv99) * 250)
TempVar:Core's Max HP = 16000 + TempVar:CharLv99 * 2000
TempVar:RightMgc's Max HP = 8000 + TempVar:CharLv99 * 1000
TempVar:LeftMgc's Max HP = 8000 + TempVar:CharLv99 * 1000
```

#### Core Protection Mechanic

The Core (Part C) has conditional immunity:

```
TempVar:Core's Physical Immunity = On
TempVar:Core's Magical Immunity = On

If ((GlobalVar:BzDead-Sub2Core == 1)
  & (GlobalVar:BzDead-Sub1Core == 1)
  & (GlobalVar:BzDead-MainLMgc == 1)
  & (GlobalVar:BzDead-MainRMgc == 1)) Then
{
  TempVar:Core's Physical Immunity = Off
  TempVar:Core's Magical Immunity = Off
}
```

The Core only becomes vulnerable after both magic parts AND the sub-party cores are destroyed.

#### Revival System

The Main Body can revive dead parts with cooldown tracking:

```
If (TempVar:Head has Death Status) Then
{
  If ((TempVar:MainBody's CustomVar:HRvvTurns == 0) Then
  {
    Remove Death Status from TempVar:Head
    Activate TempVar:Head
    TempVar:Head's HP = TempVar:Head's Max HP
    Print Message [Head Portion (B) Revived]
    TempVar:MainBody's CustomVar:HRvvTurns = Rnd(1..3)  ← Random cooldown
  } Else {
    TempVar:MainBody's CustomVar:HRvvTurns = TempVar:MainBody's CustomVar:HRvvTurns - 1
  }
}
```

After the Head is killed, it stays dead for 1-3 turns before being revived.

---

## Part 2: Applying Multi-Party Mechanics to Other Bosses

### Technical Requirements

To implement multi-party rotation for custom bosses, you need:

#### 1. Battle Formation Structure

From GameEngine.md (offsets 0x0118-0x0287 in scene.bin):

```
Each scene contains 4 battle formations (not "setups" to choose from)
Each formation has 6 enemy slots (16 bytes per slot)

Formation layout:
  0x0118 | 6 * 16 bytes | Formation 1
  0x0178 | 6 * 16 bytes | Formation 2
  0x01E8 | 6 * 16 bytes | Formation 3
  0x0238 | 6 * 16 bytes | Formation 4
```

The 4 formations in a scene are typically used for:
- Random encounter variants
- Pre-emptive/back attack variations
- Different camera angle arrangements
- Rare encounter versions

For Bizarro Sephiroth, these formations likely represent the three different battle camera perspectives (Center, Right Side, Left Side).

#### 2. Field Script Integration

The multi-party behavior is NOT solely in the AI script - it requires field script coordination:

```
Field Script Actions Required:
1. Set up party rotation triggers (opcode unknown - needs reverse engineering)
2. Configure which formations chain together
3. Initialize GlobalVar:ChangeParty system
4. Handle post-battle party restoration
```

The battle location IDs for Bizarro battles are:
- 0x0001 = Bizarro Battle - Center
- 0x0044 = Bizarro Battle - Right Side
- 0x0045 = Bizarro Battle - Left Side

Custom multi-party bosses would need to either:
- Reuse these existing battle locations
- Create custom battle scenes with appropriate camera systems

#### 3. AI Script Implementation

To create a multi-party boss, the AI script must:

**Setup Phase:**
```
AI: Setup {
  Turn off Death Handling for [Boss Entity]

  If (GlobalVar:[Boss]PartyStart == 0) Then
  {
    [Initialize HP values]
    [Initialize death tracking GlobalVars]
    GlobalVar:[Boss]PartyStart = 1
    Print Message [Instructional text]
  }

  GlobalVar:ChangeParty = 0
}
```

**Death Counter Phase:**
```
AI: Counter - Death {
  If (Self is [Critical Part]) Then
  {
    GlobalVar:BzDead-[PartID] = 1
    GlobalVar:ChangeParty = 5 or 6  ← Trigger party switch
    Print Message [Part destroyed]
  }

  If ([All parts destroyed]) Then
  {
    Remove All Allies
    GlobalVar:ChangeParty = 0
  }
}
```

### Limitations and Constraints

#### Maximum Enemy Count

From Battle Formation Data documentation:
- Maximum 6 enemies per formation
- Bizarro Sephiroth uses 5 slots (A, B, C, D, E)
- 1 slot remains available for additional parts

#### Battle Location Dependencies

The multi-party camera system requires specific battle locations. Creating new multi-party bosses limits you to:
- Reusing Bizarro's 3 battle locations (Center/Right/Left)
- Modifying existing battle scenes with appropriate camera angles
- Creating entirely new battle scenes (advanced, requires 3D modeling tools)

#### Memory Considerations

Each enemy in a battle requires:
- Model data (HRC skeleton + textures)
- Animation data
- AI script memory
- Battle effect memory

Loading 5+ enemies with complex models can strain PS1-era memory limits.

### Recommended Approach for Custom Multi-Party Bosses

**Step 1: Design the Boss Layout**
- Decide how many parts (2-6 recommended)
- Define which parts trigger party switches
- Plan camera angles (can reuse Bizarro locations)

**Step 2: Create AI Scripts**
- Use Hojo/Proud Clod's successor to edit scene.bin
- Implement GlobalVar:ChangeParty logic in Counter - Death
- Set up revival mechanics (optional)
- Test each party rotation

**Step 3: Modify Field Script**
- Use Makou Reactor to edit the field that triggers the battle
- Configure battle initialization opcodes
- Set up party selection before battle
- Handle post-battle party restoration

**Step 4: Test Thoroughly**
- Verify all 3 parties can engage the boss
- Confirm death tracking persists across rotations
- Test edge cases (what if all 3 parties die?)
- Verify revival mechanics work correctly

### Example: Two-Party "Duo Boss" Implementation

Simpler alternative to Bizarro's 3-party system:

```
Boss: Guardian Duo (two mini-bosses with shared HP pool)

AI: Setup {
  TempVar:LeftGuard = Guardian A
  TempVar:RightGuard = Guardian B

  If (GlobalVar:GuardianStart == 0) Then
  {
    TempVar:LeftGuard's Max HP = 30000
    TempVar:RightGuard's Max HP = 30000
    GlobalVar:GuardianStart = 1
    GlobalVar:ChangeParty = 0
    Print Message [Split your party to defeat both!]
  }
}

AI: Counter - Death {
  If (Self is TempVar:LeftGuard) Then
  {
    GlobalVar:BzDead-LeftGuard = 1
    GlobalVar:ChangeParty = 5  ← Switch to Sub1 party
    Print Message [Left Guardian fallen! Switch teams!]
  }

  If ((GlobalVar:BzDead-LeftGuard == 1)
    & (GlobalVar:BzDead-RightGuard == 1)) Then
  {
    Remove All Allies  ← Battle victory
    GlobalVar:ChangeParty = 0
  }
}
```

This provides the multi-party experience with simpler implementation.

---

## Part 3: Multiplayer Battle Feasibility Analysis

### The Challenge: Networked PvP

The question posed: Can players encounter each other on the world map/fields and initiate PvP battles?

**Reality Check**: FF7 has zero networking infrastructure. This would require building a networked multiplayer system from scratch.

### What Would Need to Exist

#### 1. Networking Layer (Does Not Exist)

**Requirements:**
- TCP/UDP socket implementation
- Client-server architecture OR peer-to-peer
- State serialization/deserialization
- Latency compensation
- Packet loss handling
- Cheat prevention (if competitive)

**Estimated Effort**: 2-4 months for basic implementation

#### 2. World State Synchronization (Does Not Exist)

**Requirements:**
- Player position tracking on world map
- Player visibility to each other (render remote players)
- Collision detection for encounter triggers
- Proximity-based battle initiation
- Instance management (prevent multiple interruptions)

**Estimated Effort**: 1-2 months

#### 3. Battle System Modifications (Partially Possible)

**Requirements:**
- Load player party as "enemy" formation
- Replace enemy AI with networked player input
- Synchronize ATB timing across network
- Handle disconnections gracefully

**Estimated Effort**: 3-6 months

#### 4. Character Data Exchange (Needs Implementation)

**Requirements:**
- Serialize party stats, equipment, materia
- Transmit to opponent
- Load into enemy slots
- Validate data integrity (prevent cheating)

**Estimated Effort**: 1-2 weeks

### FFNx Existing Hook Infrastructure

Through analysis of FFNx source code (C++ implementation), we discovered extensive battle hooks already exist:

#### Command Injection System

**File**: `src/ff7/menu.cpp:138-143`

```cpp
void dispatchAttackCommand(){
    *ff7_externals.issued_command_id = 0x01;        // Command: Attack
    *ff7_externals.issued_action_target_type = 0;   // Target type
    *ff7_externals.issued_action_target_index = 4;  // Enemy slot 0
    ((void(*)())ff7_externals.dispatch_chosen_battle_action)();
}
```

This demonstrates **programmatic command execution** is already possible. You can:
- Set any command ID (0x01=Attack, 0x02=Magic, 0x04=Item, etc.)
- Set action ID (specific spell/item)
- Set targeting data
- Execute the command via `dispatch_chosen_battle_action()`

#### Battle State Access

**File**: `src/ff7.h:745-782`

```cpp
struct battle_ai_context {
    byte lastCommandIdx;           // Last command executed
    byte lastActionIdx;            // Last action index
    uint16_t activeActorMask;      // Bitmask of active actors
    uint16_t actorAlliesMask;      // Party member bitmask
    uint16_t actorEnemiesMask;     // Enemy bitmask
    battle_actor_vars actor_vars[10];  // All actor data
};
```

**Actor Slot Layout:**
- Slots 0-2: Player party members
- Slot 3: Unused
- Slots 4-9: Enemies (or opponent party in PvP)

This means FFNx can **read complete battle state** at any time.

#### Per-Actor State Tracking

**File**: `src/ff7.h:687-743`

```cpp
struct battle_actor_vars {
    uint32_t statusMask;    // Status effects (Poison, Haste, etc.)
    byte index;             // Character ID
    byte level;             // Level
    int currentHP;          // Current HP
    int maxHP;              // Max HP
    uint16_t currentMP;     // Current MP
    uint16_t defense;       // Defense stat
    uint16_t magic_defense; // Magic Defense
    uint16_t attack;        // Attack stat
    // ... full stat block accessible
};
```

This provides **complete character state** for all 10 battle slots.

#### Animation Event Queue

**File**: `src/ff7.h:784-794`

```cpp
struct battle_anim_event {
    byte attackerID;        // Who's performing action
    byte commandIndex;      // Command type
    uint16_t actionIndex;   // Specific action
    uint16_t cameraData;    // Camera positioning
};
```

Commands trigger animations via this queue. Networked commands would inject here.

#### Input Blocking System

**File**: `src/input.cpp:165-185`

```cpp
byte* GetGameKeyState()
{
    if (blockKeys || !gamehacks.canInputBeProcessed())
    {
        std::memset(keys, 0, 256);  // Block all input
        return keys;
    }
    // ... normal input handling
}
```

FFNx can **disable local input** via `SetBlockKeysFromGame(true)`, allowing external control.

### Critical Addresses Exposed by FFNx

**File**: `src/ff7_data.h:720-721`

```cpp
ff7_externals.issued_command_id =
    (byte*)get_absolute_value(ff7_externals.dispatch_chosen_battle_action, 0x12B);

ff7_externals.issued_action_id =
    (uint16_t*)get_absolute_value(ff7_externals.dispatch_chosen_battle_action, 0x122);
```

These pointers allow **direct memory modification** of issued commands.

**File**: `src/ff7_data.h:806`

```cpp
ff7_externals.g_battle_model_state =
    std::span((battle_model_state*)get_absolute_value(battle_sub_42B66A, 0xD9), 10);
```

Access to **all 10 actor model states** (party + enemies).

**File**: `src/ff7_data.h:1338`

```cpp
ff7_externals.battle_context =
    (battle_ai_context*)get_absolute_value(ff7_externals.battle_sub_41CCB2, 0x5F);
```

Direct access to **complete battle AI context**.

**File**: `src/ff7_data.h:1344`

```cpp
ff7_externals.g_active_actor_id =
    (byte*)get_absolute_value(ff7_externals.display_battle_action_text_42782A, 0x52);
```

Identifies **currently acting character**.

### Implementation Roadmap

#### Phase 1: Input Recording/Replay System (1-2 weeks)

**Goal**: Prove command injection works for "ghost battles"

```cpp
// Conceptual structure
struct BattleCommand {
    uint32_t frame_number;      // When to execute
    byte actor_slot;            // Who (0-2 for party)
    byte command_id;            // Command type
    uint16_t action_id;         // Specific action
    byte target_type;           // Target type
    byte target_index;          // Target slot
};

std::vector<BattleCommand> battle_log;

// Hook to record commands
void recordBattleCommand() {
    BattleCommand cmd;
    cmd.frame_number = current_frame;
    cmd.actor_slot = *ff7_externals.g_active_actor_id;
    cmd.command_id = *ff7_externals.issued_command_id;
    cmd.action_id = *ff7_externals.issued_action_id;
    cmd.target_type = *ff7_externals.issued_action_target_type;
    cmd.target_index = *ff7_externals.issued_action_target_index;

    battle_log.push_back(cmd);
}

// Replay recorded commands
void replayBattleCommand(BattleCommand cmd) {
    *ff7_externals.issued_command_id = cmd.command_id;
    *ff7_externals.issued_action_id = cmd.action_id;
    *ff7_externals.issued_action_target_type = cmd.target_type;
    *ff7_externals.issued_action_target_index = cmd.target_index;

    ff7_externals.dispatch_chosen_battle_action();
}
```

**Deliverable**: Save battle to file, replay it later

#### Phase 2: Ghost Battle Mode (2-4 weeks)

**Goal**: Fight against recorded opponent

**Implementation:**
1. Player A records battle → exports to file
2. Player B loads that file
3. Enemy AI reads from recording instead of actual AI
4. Player B fights against Player A's "ghost"

**Benefits:**
- No networking required
- Proves injection system works
- Async "play-by-mail" style multiplayer

#### Phase 3: Async Turn-Based Network (4-8 weeks)

**Goal**: Simple networked battles without real-time sync

**Architecture:**
```
Player 1                          Server                          Player 2
   |                                |                                |
   |------ Execute Command -------->|                                |
   |                                |------ Forward Command -------->|
   |                                |                                |
   |                                |<----- Command Executed --------|
   |<----- Confirmation ------------|                                |
   |                                |                                |
```

**Implementation:**
- Remove ATB entirely (make pure turn-based)
- Player 1 executes → waits for Player 2
- Server validates → forwards commands
- Much simpler than real-time sync

**Network Protocol:**
```cpp
struct BattlePacket {
    uint8_t packet_type;        // CMD, SYNC, ACK
    uint32_t frame;             // Frame number
    BattleCommand command;      // The command
    uint32_t checksum;          // Validation
};
```

**Transport Options:**
- WebSocket (easier, more overhead)
- UDP (faster, requires reliability layer)
- TCP (simplest, slight latency)

#### Phase 4: Real-Time Networked (Ambitious - Months)

**Goal**: Full real-time ATB battles

**Challenges:**
- **Lockstep networking** required
- Both clients simulate identical battle
- Input delay = network latency
- Desyncs are catastrophic
- Requires rollback on packet loss

**Architecture:**
```
Client 1                                               Client 2
   |                                                      |
   |--- Input (frame N) --->  Server  <--- Input (frame N)|
   |                             |                         |
   |<-- Sync (frame N+1) --------|-------- Sync (frame N+1)|
   |                             |                         |
   | Simulate frame N+1          |        Simulate frame N+1|
   |                             |                         |
```

**Implementation Complexity:**
- Deterministic simulation (exact same RNG on both sides)
- Frame-perfect synchronization
- Rollback on desync detection
- Graceful handling of disconnects

**Estimated Effort**: 6-12 months for stable implementation

### Party-as-Enemy Loading Challenge

To implement PvP, opponent's party must appear as enemies.

**The Problem:**

```cpp
// Party members use player character models (Cloud, Tifa, Barret, etc.)
// Enemies use enemy models (Soldier, Guard Scorpion, etc.)
// These are loaded from different files with different structures
```

**Potential Solution:**

```cpp
void loadOpponentAsEnemies(battle_actor_vars* opponent_party, int count) {
    for (int i = 0; i < count && i < 6; i++) {
        // Copy stats to enemy slots
        ff7_externals.battle_context->actor_vars[4 + i] = opponent_party[i];

        // HARD PART: Load character model into enemy slot
        // Character models are in different format than enemy models
        // May require:
        //   - Custom model loader
        //   - Format conversion layer
        //   - Animation remapping
    }
}
```

**Character Model Format** (from field/battle):
- HRC skeleton system
- Separate weapon models
- Complex bone hierarchy
- Field vs Battle variants

**Enemy Model Format**:
- Different skeleton structure
- No weapon separation
- Simpler hierarchy
- Battle-only

**Feasibility**: Medium-Hard. FFNx has hooks for model loading (`read_battle_hrc`), but format conversion is non-trivial.

### Rendering 9 Characters Simultaneously

**Question**: Can all 9 party members be on screen at once?

**Answer**: Not without major engine modifications.

**Current Limitations:**

From Battle Formation Data (GameEngine.md):
- Maximum 6 enemies per battle
- Maximum 3 active party members
- Battle animations/camera assume 3v6 layout

**Why 9 Simultaneous is Hard:**

1. **Model Slot Limits**
```cpp
// Battle system has hardcoded arrays:
battle_model_state g_battle_model_state[10];  // 10 total slots
// Slots 0-2: Party
// Slot 3: Unused
// Slots 4-9: Enemies (6 slots)
```

Rendering 9 party members would require:
- Expanding arrays to 12+ slots
- Modifying all battle code that references these arrays
- Extensive engine surgery

2. **UI Limitations**
- ATB bars designed for 3 characters
- Command windows designed for 3 characters
- Status display designed for 3 characters

Showing 9 simultaneous ATB bars would require:
- Complete UI redesign
- Modified rendering pipeline
- New layout system

3. **Camera System**
- Battle cameras positioned for 3v6 layout
- Character positions hardcoded
- Camera angles assume standard formation

With 9 characters on one side:
- Overcrowding on screen
- Characters overlapping
- Camera can't frame everyone
- Animation conflicts

4. **Memory Constraints**
- Each character model = skeleton + textures + animations
- 9 characters = 9x memory usage
- PS1-era memory limits may be exceeded
- Even on modern PC, battle system assumes smaller counts

**Theoretical Maximum**: With extensive FFNx modifications, possibly 6v6 (12 total). Beyond that, fundamental engine redesign required.

**Practical Recommendation**: Keep 3v3 layout for networked battles, use standard party rotation for larger engagements.

### Feasibility Matrix

| Component | Difficulty | Time Estimate | Existing FFNx Support |
|-----------|------------|---------------|----------------------|
| **Command Injection** | Easy | 1 week | ✅ Already demonstrated |
| **Input Blocking** | Easy | 1 week | ✅ `SetBlockKeysFromGame()` exists |
| **State Reading** | Easy | 1 week | ✅ Full battle_context access |
| **Input Recording** | Medium | 2-3 weeks | Hook `dispatch_chosen_battle_action()` |
| **Ghost Battles** | Medium | 3-4 weeks | Replay system + AI override |
| **Network Layer** | Hard | 2-4 months | ❌ Nothing exists |
| **Frame Sync** | Hard | 2-3 months | ❌ ATB determinism issues |
| **Party-as-Enemy** | Hard | 1-2 months | Partial (model loading hooked) |
| **9-Char Rendering** | Very Hard | 4-6 months | ❌ Fundamental engine limits |
| **Real-Time Multiplayer** | Very Hard | 6-12 months | ❌ Complete networking stack needed |

### Recommended Path Forward

If serious about multiplayer implementation:

**Phase 1: Prove the Concept (Month 1-2)**
- Implement input recording system
- Create battle replay functionality
- Verify command injection works reliably

**Phase 2: Ghost Battles (Month 3-4)**
- Save/load battle recordings
- Override enemy AI with recorded actions
- Build "fight against recording" mode

**Phase 3: Async Multiplayer (Month 5-8)**
- Simple WebSocket server
- Turn-based command exchange
- No ATB, pure turn-based
- Minimal sync requirements

**Phase 4: Evaluate Real-Time (Month 9+)**
- If async works well, attempt real-time
- Implement lockstep networking
- Build rollback system
- Extensive testing

**Key Functions to Hook**

| Function | Address Retrieval | Purpose |
|----------|------------------|---------|
| `dispatch_chosen_battle_action` | Dynamic lookup via `ff7_externals` | Execute any command |
| `set_battle_targeting_data` | Dynamic lookup via `ff7_externals` | Set targets |
| `battle_sub_6DB0EE` | Battle main loop | Per-frame hook point |
| `display_battle_action_text_sub_6D71FA` | Display action text | Post-action hook |

**Example Hook Pattern** (from `src/ff7/menu.cpp:147-149`):

```cpp
// Auto-attack is implemented via constant command injection
// Same pattern could inject networked commands
if (gamehacks.isAutoAttack()) {
    dispatchAttackCommand();  // Injects attack every frame
}
```

This demonstrates FFNx can inject commands on every frame - the same pattern would work for networked inputs.

---

## Part 4: Key Findings Summary

### Multi-Party Boss Mechanics

**✅ Feasible for Custom Bosses**

The Bizarro Sephiroth multi-party system is NOT unique to that boss - it's a combination of:
1. AI script using GlobalVar:ChangeParty
2. Field script coordination
3. Death tracking via persistent GlobalVars
4. Appropriate battle location (camera system)

Custom multi-party bosses can be created using:
- Hojo/Proud Clod for AI script editing
- Makou Reactor for field script editing
- Existing Bizarro battle locations OR custom scenes

**Recommended First Project**: Create a simpler 2-party boss to learn the system.

### Multiplayer Implementation

**⚠️ Technically Possible, Practically Difficult**

FFNx provides exceptional hooks for battle system manipulation:
- Command injection: ✅ Working
- State reading: ✅ Complete access
- Input blocking: ✅ Available

What's missing:
- Networking layer (requires building from scratch)
- Synchronization system (complex timing issues)
- Party-as-enemy loading (model format challenges)

**Realistic Approach**: Build incrementally
1. Input recording → Proves injection works
2. Ghost battles → Async "multiplayer"
3. Turn-based network → Removes timing complexity
4. Real-time (optional) → Ambitious long-term goal

### 9-Character Rendering

**❌ Impractical Without Major Engine Overhaul**

The battle system is fundamentally designed for 3 active party members:
- Hardcoded array sizes
- UI assumptions
- Camera positioning
- Memory allocation

Displaying all 9 simultaneously would require:
- Expanding battle_model_state arrays
- Complete UI redesign
- Camera system rewrite
- Memory expansion

**Estimated Effort**: 4-6 months minimum, possibly fundamental incompatibilities.

**Alternative**: Keep 3-character active party, use Bizarro-style rotation to involve all 9 across multiple engagements.

---

## Part 5: Technical Deep Dive - FFNx Battle Hooks

### Memory Address Discovery

FFNx uses dynamic address resolution to locate game functions. From `src/ff7_data.h`:

```cpp
// Find the dispatch function via relative call
ff7_externals.dispatch_chosen_battle_action =
    get_relative_call(ff7_externals.battle_sub_6DB0EE, 0x50E);

// Find command/action pointers via absolute addressing
ff7_externals.issued_command_id =
    (byte*)get_absolute_value(ff7_externals.dispatch_chosen_battle_action, 0x12B);

ff7_externals.issued_action_id =
    (uint16_t*)get_absolute_value(ff7_externals.dispatch_chosen_battle_action, 0x122);
```

This works across different FF7 versions (1998, Steam, eStore) by following relative offsets rather than hardcoding addresses.

### Command Execution Flow

**Step 1: Player Input** (normal gameplay)
```
Player presses button → Menu selection → Command chosen
```

**Step 2: Command Data Set**
```cpp
*ff7_externals.issued_command_id = 0x02;    // Magic
*ff7_externals.issued_action_id = 0x001A;   // Fire3
*ff7_externals.issued_action_target_type = 0;  // Single target
*ff7_externals.issued_action_target_index = 4; // Enemy slot 0
```

**Step 3: Dispatch**
```cpp
ff7_externals.dispatch_chosen_battle_action();
```

**Step 4: Animation Queue**
```cpp
struct battle_anim_event event;
event.attackerID = 0;  // Cloud
event.commandIndex = 0x02;  // Magic
event.actionIndex = 0x001A;  // Fire3
// Added to queue for rendering
```

**Step 5: Damage Calculation**
```
Battle engine calculates damage → Applies to target → Updates HP
```

### Hook Injection Points

**Pre-Command Hook** (menu.cpp:147):
```cpp
// Before command dispatch
if (gamehacks.isAutoAttack()) {
    dispatchAttackCommand();  // Inject auto-attack
}
```

**Post-Action Hook** (voice.cpp:813):
```cpp
void ff7_display_battle_action_text() {
    // After action executes, can read results:
    byte actor_id = *ff7_externals.g_active_actor_id;
    byte command_id = ff7_externals.g_battle_model_state[actor_id].commandID;
    uint16_t action_id = ff7_externals.g_small_battle_model_state[actor_id].actionIdx;

    // Log for recording/network transmission
}
```

### Example: Programmatic Spell Casting

```cpp
void castFireOnEnemy(int enemy_slot) {
    // Block player input
    SetBlockKeysFromGame(true);

    // Set command data
    *ff7_externals.issued_command_id = 0x02;        // Magic command
    *ff7_externals.issued_action_id = 0x0016;       // Fire
    *ff7_externals.issued_action_target_type = 0;   // Single target
    *ff7_externals.issued_action_target_index = 4 + enemy_slot;  // Enemy slot

    // Execute
    ((void(*)())ff7_externals.dispatch_chosen_battle_action)();

    // Re-enable input after animation
    SetBlockKeysFromGame(false);
}
```

### Command ID Reference

From game analysis:

```
0x00 = (nothing)
0x01 = Attack
0x02 = Magic
0x03 = Summon
0x04 = Item
0x05 = E.Skill
0x06 = Defend
0x07 = (unknown)
0x08 = Change
0x09 = Limit
0x0A = Coin
0x0B = Morph
0x0C = Deathblow
0x0D = Manipulate
0x0E = Mime
```

### Network Packet Design (Theoretical)

**Command Packet Structure:**
```cpp
struct NetworkBattleCommand {
    uint8_t packet_type;        // 0x01 = COMMAND
    uint32_t sequence_number;   // For ordering/ack
    uint32_t frame_number;      // Game frame (for sync)

    // Command data
    uint8_t actor_slot;         // Who executes (0-2)
    uint8_t command_id;         // Command type
    uint16_t action_id;         // Spell/item ID
    uint8_t target_type;        // Single/all/etc
    uint8_t target_index;       // Which slot

    uint32_t checksum;          // Validation
};
```

**Sync Packet Structure:**
```cpp
struct NetworkBattleSync {
    uint8_t packet_type;        // 0x02 = SYNC
    uint32_t frame_number;      // Current frame

    // Critical state
    int16_t party_hp[3];        // HP for validation
    int16_t enemy_hp[6];        // Enemy HP
    uint32_t status_masks[9];   // Status effects

    uint32_t checksum;
};
```

**Frequency**:
- Commands: Sent when executed (event-driven)
- Sync: Every 60 frames (~1 second at 60fps)

### Desync Detection

```cpp
bool validateSync(NetworkBattleSync remote_state) {
    // Compare HP values
    for (int i = 0; i < 3; i++) {
        if (abs(remote_state.party_hp[i] -
                ff7_externals.battle_context->actor_vars[i].currentHP) > 10) {
            return false;  // Desync detected
        }
    }

    // Compare status masks
    for (int i = 0; i < 9; i++) {
        if (remote_state.status_masks[i] !=
            ff7_externals.battle_context->actor_vars[i].statusMask) {
            return false;
        }
    }

    return true;  // Sync OK
}
```

On desync:
1. Pause both clients
2. Send full state snapshot
3. Force client with lower sequence number to resync
4. Resume

---

## Part 6: Practical Next Steps

### For Multi-Party Custom Bosses

**Immediate Actions:**
1. Download Hojo (Proud Clod successor) or Makou Reactor
2. Export Bizarro Sephiroth's AI script from scene.bin
3. Study the GlobalVar usage patterns
4. Create simplified 2-party boss as proof-of-concept

**Learning Path:**
- Week 1: Study existing multi-target boss scripts (Carry Armor, Jenova·SYNTHESIS)
- Week 2: Implement simple 2-part boss (no party rotation)
- Week 3: Add party rotation mechanics
- Week 4: Test and refine

**Resources Needed:**
- Hojo/Proud Clod (scene.bin editor)
- Makou Reactor (field script editor)
- Bizarro Sephiroth AI script (reference)
- Test save file near Northern Crater

### For Multiplayer Experimentation

**Phase 1 Prototype (Weeks 1-4):**
1. Fork FFNx repository
2. Add logging to `dispatch_chosen_battle_action()`
3. Record commands to JSON file
4. Create replay system that reads JSON

**Phase 2 Ghost Battles (Weeks 5-8):**
1. Override enemy AI script execution
2. Feed recorded commands instead
3. Test fighting against recorded battles
4. Export/import battle recordings

**Phase 3 Network Foundation (Weeks 9-16):**
1. Choose network library (Asio, Enet, RakNet)
2. Implement basic client-server
3. Send command packets
4. Remove ATB, make turn-based
5. Test 2-player battles locally

**Development Environment:**
- Visual Studio 2019+ (FFNx uses C++17)
- CMake (FFNx build system)
- FFNx source code (GitHub: julianxhokaxhiu/FFNx)
- FF7 1998 or Steam version
- Network library (recommend Asio for async I/O)

**Testing Approach:**
- Local loopback first (127.0.0.1)
- LAN testing second
- Internet testing last (after LAN stable)

### Resources and Documentation

**FFNx Source Code Locations:**
```
/mnt/c/FFNx/src/
├── ff7/
│   ├── battle/
│   │   ├── battle.cpp       ← Battle hooks
│   │   ├── menu.cpp         ← Command dispatch
│   │   └── animations.cpp   ← Animation system
│   ├── defs.h               ← Battle structure definitions
│   └── menu.cpp             ← Menu interaction
├── ff7.h                    ← Master externals structure
├── ff7_data.h               ← Address resolution
├── input.cpp                ← Input handling
└── gamepad.cpp              ← Controller input
```

**Key Documentation:**
- GameEngine.md (Battle System section: lines 3000-5000)
- FFNX_DEVELOPER_GUIDE.md (FFNx hooking system)
- FFNx GitHub Wiki (build instructions)

**Community Resources:**
- Qhimm Forums (FF7 modding community)
- FFNx Discord (technical support)
- FF7 Speedrun Wiki (battle mechanics deep-dive)

---

## Conclusion

### What We Learned

1. **Multi-party mechanics are flexible**
   - Not hardcoded to Bizarro Sephiroth
   - Can be applied to custom bosses
   - Requires AI script + field script coordination

2. **FFNx provides extensive hooks**
   - Full battle state access
   - Command injection capability
   - Input blocking system
   - Animation event queue access

3. **Multiplayer is theoretically viable**
   - Input recording: Easy
   - Ghost battles: Medium difficulty
   - Networked battles: Hard but possible
   - Real-time multiplayer: Very ambitious

4. **9-character rendering is impractical**
   - Fundamental engine limitations
   - Would require massive overhaul
   - Alternative: Use party rotation (Bizarro-style)

### Realistic Expectations

**If you want custom multi-party bosses:**
- Achievable in 2-4 weeks with existing tools
- Start simple, iterate to complexity
- Reuse Bizarro battle locations

**If you want multiplayer:**
- Start with input recording (1-2 weeks)
- Build ghost battles next (3-4 weeks)
- Async turn-based is achievable (2-4 months)
- Real-time is long-term project (6-12 months)

**If you want 9 simultaneous characters:**
- Consider party rotation instead
- Or accept 3v3 networked battles
- Full 9-char rendering = 4-6 month project minimum

### Final Recommendation

**Start Small:**
1. Create a simple multi-part boss (like Guardian Duo example)
2. Add party rotation to that boss
3. Test thoroughly
4. Then consider multiplayer prototyping

**For Multiplayer:**
1. Implement input recording first (proves concept)
2. Create ghost battle system (useful on its own)
3. Evaluate if full network is worth effort
4. If yes, build incrementally (async first, real-time later)

The foundation exists in FFNx. The question is how much effort you want to invest in building on top of it.

---

## Appendices

### Appendix A: Bizarro Sephiroth Full AI Script

*(Full AI script provided by user - not reproduced here for brevity, see session transcript)*

**Key Sections:**
- Setup: HP calculation, death tracking initialization
- Main: Turn counter, revival mechanics, attack pattern
- Counter - Death: Party switching logic, death tracking updates

### Appendix B: FFNx Battle Hook Reference

**Command Injection:**
- `ff7_externals.issued_command_id` - Byte pointer
- `ff7_externals.issued_action_id` - Uint16 pointer
- `ff7_externals.dispatch_chosen_battle_action` - Function pointer

**State Access:**
- `ff7_externals.battle_context` - Full AI context
- `ff7_externals.g_battle_model_state[10]` - Model states
- `ff7_externals.g_active_actor_id` - Current actor

**Input Control:**
- `SetBlockKeysFromGame(bool)` - Enable/disable input
- `GetGameKeyState()` - Read input state

### Appendix C: Battle Formation Data Structure

From GameEngine.md (offsets in scene.bin):

```
0x0000 | 2 bytes  | Unknown (padding?)
0x0002 | 2 bytes  | Upon defeat of all opponents
0x0004 | 2 bytes  | Pre-emptive flag
0x0006 | 2 bytes  | Unknown
0x0008 | 4 bytes  | Battle scene ID
0x000C | 2 bytes  | Location ID
0x000E | 2 bytes  | Unknown
0x0010 | 2 bytes  | Battle type (Normal/Back/Side/etc)
0x0012 | 2 bytes  | Battle layout type (0-8)
0x0014 | 4 bytes  | Camera data pointer
0x0118 | 96 bytes | Battle Formation 1 (6 enemies * 16 bytes)
0x0178 | 96 bytes | Battle Formation 2
0x01E8 | 96 bytes | Battle Formation 3
0x0238 | 96 bytes | Battle Formation 4
```

### Appendix D: Command ID Complete List

```
0x00 = Nothing
0x01 = Attack
0x02 = Magic
0x03 = Summon
0x04 = Item
0x05 = Enemy Skill
0x06 = Defend
0x07 = (Unused)
0x08 = Change
0x09 = Limit Break
0x0A = Throw (Coin)
0x0B = Morph
0x0C = Deathblow
0x0D = Manipulate
0x0E = Mime
0x0F = W-Magic
0x10 = W-Summon
0x11 = W-Item
... (enemy-specific commands continue)
```

### Appendix E: Recommended Reading

**Game Engine Documentation:**
- GameEngine.md - Battle System (lines 3000-5000)
- GameEngine.md - Scene.bin Format (lines 3040-3382)

**FFNx Documentation:**
- FFNX_DEVELOPER_GUIDE.md - Hooking System
- FFNx GitHub README - Build instructions
- FFNx Wiki - Plugin development

**Community Resources:**
- Qhimm Forums - "Battle Mechanics" section
- TLS (The Lifestream) - Scene.bin tutorials
- FFHacktics Wiki - AI scripting reference

---

**End of Document**

*Total Analysis Duration: ~90 minutes*
*Files Analyzed: GameEngine.md (6000+ lines), FFNx source (15+ files), session context documents*
*Code Examples: 20+ snippets*
*Feasibility Assessments: 3 major systems*
