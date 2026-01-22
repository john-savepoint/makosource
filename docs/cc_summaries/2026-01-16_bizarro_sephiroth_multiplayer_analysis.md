# Final Fantasy VII - Bizarro Sephiroth Multi-Party Battle & Multiplayer Implementation Analysis

**Created**: 2026-01-16 15:09 JST (Thursday)
**Session ID**: f85be4a3-6581-4309-964b-bd8a1c470dce
**Author**: Claude Code (Sonnet 4.5)
**Context**: Analysis of Bizarro Sephiroth's unique multi-party battle mechanic and feasibility assessment for implementing similar systems in custom bosses and potential multiplayer/PvP battles

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Bizarro Sephiroth AI Script Analysis](#bizarro-sephiroth-ai-script-analysis)
3. [Multi-Party Battle Mechanics](#multi-party-battle-mechanics)
4. [Custom Boss Implementation](#custom-boss-implementation)
5. [Multiplayer/PvP Feasibility](#multiplayerpvp-feasibility)
6. [FFNx Existing Infrastructure](#ffnx-existing-infrastructure)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Technical Specifications](#technical-specifications)
9. [Recommendations](#recommendations)

---

## Executive Summary

### Key Questions Addressed

1. **Can Bizarro Sephiroth's multi-party mechanic be applied to other bosses?**
   ✅ **YES** - Technically feasible using existing tools (Makou Reactor, kernel editors)

2. **Can networked multiplayer battles be implemented?**
   ⚠️ **POSSIBLE BUT COMPLEX** - Requires significant FFNx development, no existing networking infrastructure

3. **Can all 9 characters render simultaneously?**
   ❌ **NOT WITHOUT ENGINE REWRITE** - Battle system designed for 3v6 layout, fundamental rendering constraints

### Critical Findings

- Bizarro Sephiroth's multi-party system uses `GlobalVar:ChangeParty` (values: 0, 5, 6) to trigger party rotation
- Party switching is **NOT** in the AI script itself - controlled by field scripts and global variables
- FFNx already has robust battle input hooks suitable for command injection
- Multiplayer would require async turn-based approach first, real-time networking extremely complex

---

## Bizarro Sephiroth AI Script Analysis

### Multi-Target Structure

Bizarro Sephiroth consists of **5 independently targetable parts**:

| Part ID | Name | Role | Max HP Calculation |
|---------|------|------|-------------------|
| A | Main Body | Primary target | 40000 + CharLv99*5000 + JenovaBonus |
| B | Head | Reviving part | 4000 - ((8-CharLv99)*250) |
| C | Core | Immunity controller | 16000 + CharLv99*2000 |
| D | Right Magic | Elemental attacker | 8000 + CharLv99*1000 |
| E | Left Magic | Elemental attacker | 8000 + CharLv99*1000 |

**Jenova Bonus**: +60000 HP if `GlobalVar:JenovaKoR == 1` (Jenova·SYNTHESIS defeated)

### Party Rotation Mechanic

The AI script uses `GlobalVar:ChangeParty` to trigger party switches:

```text
GlobalVar:ChangeParty Values:
  0 = No party change
  5 = Switch to Sub-Party 1 (when Head or Right Magic dies)
  6 = Switch to Sub-Party 2 (when Core or Left Magic dies)
```

**Example from AI Counter-Death**:
```text
If (Self is TempVar:Head) Then {
    If (TempVar:MainBody doesn't have Death Status) Then {
        Choose TempVar:Head's Last Attacker (General)
        Use Demi3 on Target
        Print Message [Head Portion (B) Dead]
        ...
        GlobalVar:ChangeParty = 5  ← TRIGGERS PARTY SWITCH
    }
}
```

### Death Tracking System

The AI maintains persistent state across party rotations via GlobalVars:

```text
Death Tracking Variables:
  GlobalVar:BzDead-MainHead  (0 = alive, 1 = dead)
  GlobalVar:BzDead-MainCore
  GlobalVar:BzDead-MainRMgc  (Right Magic)
  GlobalVar:BzDead-MainLMgc  (Left Magic)
  GlobalVar:BzDead-Sub1Core
  GlobalVar:BzDead-Sub1LArm
  GlobalVar:BzDead-Sub2Core
  GlobalVar:BzDead-Sub2LArm
  ...
```

These variables allow the battle to "remember" which parts died under which party, enabling complex revival mechanics.

### Revival Mechanics

**Head Revival** (AI Main section, Count == 1):
```text
If (TempVar:Head has Death Status) Then {
    If (TempVar:MainBody's CustomVar:HRvvTurns == 0) Then {
        Remove Death Status from TempVar:Head
        Activate TempVar:Head
        TempVar:Head's HP = TempVar:Head's Max HP
        Print Message [Head Portion (B) Revived]
        GlobalVar:BzDead-MainHead = 0
        ...
    } Else {
        TempVar:MainBody's CustomVar:HRvvTurns -= 1  ← Revival countdown
    }
}
```

**Magic Parts Revival** (requires Core to be alive for 8+ turns):
```text
If ((TempVar:Core doesn't have Death Status)
    & (TempVar:RightMgc has Death Status)
    & (TempVar:LeftMgc has Death Status)
    & (TempVar:CoreTurns > 8)) Then {

    Choose TempVar:RightMgc and TempVar:LeftMgc
    Remove Death Status from Target
    Activate Target
    Use Bizarro Enegy on Target  ← Revival action
    ...
    GlobalVar:MainCoreTurns = 0  ← Reset turn counter
}
```

### Core Immunity System

The Core (Part C) has **conditional immunity** based on other parts' status:

```text
TempVar:Core's Physical Immunity = On  ← Default state
TempVar:Core's Magical Immunity = On

If ((GlobalVar:BzDead-Sub2Core == 1)
    & (GlobalVar:BzDead-Sub1Core == 1)
    & (GlobalVar:BzDead-MainLMgc == 1)
    & (GlobalVar:BzDead-MainRMgc == 1)) Then {

    TempVar:Core's Physical Immunity = Off  ← Only vulnerable when conditions met
    TempVar:Core's Magical Immunity = Off
}
```

**Strategic Implication**: Players must destroy all Magic parts and Sub-Party Cores before the Main Party's Core becomes vulnerable.

---

## Multi-Party Battle Mechanics

### Battle Formation Structure

From GameEngine.md documentation (offsets 0x0118-0x0287):

```text
Scene.bin Formation Data:
  0x0118 | 6 * 16 bytes | Battle Formation 1 (6 enemy slots)
  0x0178 | 6 * 16 bytes | Battle Formation 2 (6 enemy slots)
  0x01E8 | 6 * 16 bytes | Battle Formation 3 (6 enemy slots)
  0x0238 | 6 * 16 bytes | Battle Formation 4 (6 enemy slots)
```

**Important Clarification**: These are NOT "4 setup choices" - they're 4 different enemy arrangements that can occur within a scene:
- Formation 1: Standard encounter
- Formation 2: Variant encounter (different enemy mix)
- Formation 3: Back attack variant
- Formation 4: Rare/special encounter

For Bizarro Sephiroth, the multi-party behavior is achieved through:
1. **Field scripting** - Sets up party rotation before battle starts
2. **GlobalVar:ChangeParty** - AI-controlled trigger for switching
3. **Formation chaining** - "Upon defeat" field (offset 0x0002) chains battles without ending scene

### Battle Location System

Bizarro Sephiroth uses **three distinct battle locations**:

| Location ID | Name | Usage |
|-------------|------|-------|
| 0x0001 | Bizarro Battle - Center | Main party fighting torso/head |
| 0x0044 | Bizarro Battle - Right Side | Sub-party 1 fighting right arm |
| 0x0045 | Bizarro Battle - Left Side | Sub-party 2 fighting left arm |

These locations determine:
- Camera angles and positioning
- Background rendering
- Character/enemy placement coordinates

**Constraint**: Custom multi-party battles must either:
- Reuse existing multi-party battle locations (0x0001, 0x0044, 0x0045)
- Create entirely new battle scenes with custom camera systems (advanced)

### Actor Slot Layout

FF7's battle system supports **10 actor slots total**:

```text
Slot Layout:
  Slots 0-2: Party members (player-controlled characters)
  Slot 3:    Unused/reserved
  Slots 4-9: Enemies (6 maximum)
```

**Why only 3 characters render at once**:
- Battle rendering pipeline designed for 3v6 layout
- ATB bars, command windows UI assume 3 active characters
- Model loading system has hardcoded limits for active character slots
- Animation and camera systems expect standard formation

**Bizarro's 9-character illusion**:
- Characters rotate in/out between formations via party switching
- Only 3 active at any moment
- GlobalVars preserve state across switches

---

## Custom Boss Implementation

### Applying Multi-Party Mechanic to Other Bosses

**Required Components**:

1. **Field Script Modification** (using Makou Reactor or Hojo)
   - Set up initial party configuration
   - Configure party rotation opcodes
   - Initialize GlobalVars before battle starts

2. **AI Script with Party Switch Logic**
   ```text
   AI: Counter - Death {
       If (Self is CustomBossPart) Then {
           GlobalVar:ChangeParty = 5  ← Trigger switch to Sub-Party 1
           Print Message [Part destroyed! Switch parties!]
       }
   }
   ```

3. **Death State Tracking**
   ```text
   AI: Setup {
       GlobalVar:CustomBoss-Part1Dead = 0
       GlobalVar:CustomBoss-Part2Dead = 0
       GlobalVar:CustomBoss-Part3Dead = 0
   }

   AI: Counter - Death {
       If (Self is Part1) Then {
           GlobalVar:CustomBoss-Part1Dead = 1
       }
   }
   ```

4. **Battle Location Assignment**
   - Reuse existing Bizarro locations (easiest)
   - OR create custom battle scene (requires hex editing scene.bin)

### Tools Required

| Tool | Purpose | Availability |
|------|---------|--------------|
| Makou Reactor | Field script editing | ✅ Available |
| Hojo / Proud Clod | Scene.bin editing (AI, formations) | ✅ Available |
| Kernel.bin editor | Attack/spell definitions | ✅ Available |
| HxD / hex editor | Direct scene.bin offset editing | ✅ Available |

### Example Custom Boss: "Tri-Head Hydra"

**Concept**: 3-headed boss where defeating each head switches to a different party

**AI Structure**:
```text
AI: Setup {
    TempVar:HydraBody = Hydra A
    TempVar:LeftHead  = Hydra B
    TempVar:CenterHead = Hydra C
    TempVar:RightHead = Hydra D

    GlobalVar:HydraLeftDead = 0
    GlobalVar:HydraCenterDead = 0
    GlobalVar:HydraRightDead = 0
}

AI: Counter - Death {
    If (Self is TempVar:LeftHead) Then {
        GlobalVar:HydraLeftDead = 1
        GlobalVar:ChangeParty = 5  ← Switch to Sub-Party 1
        Print Message [Left head severed! Party 2 advancing!]
    }

    If (Self is TempVar:CenterHead) Then {
        GlobalVar:HydraCenterDead = 1
        GlobalVar:ChangeParty = 6  ← Switch to Sub-Party 2
        Print Message [Center head destroyed! Party 3 engaging!]
    }

    If (Self is TempVar:RightHead) Then {
        GlobalVar:HydraRightDead = 1
        GlobalVar:ChangeParty = 0  ← Return to main party
        Print Message [Right head defeated! Finish the body!]
    }
}

AI: Main {
    If ((GlobalVar:HydraLeftDead == 1)
        & (GlobalVar:HydraCenterDead == 1)
        & (GlobalVar:HydraRightDead == 1)) Then {

        TempVar:HydraBody's Physical Immunity = Off
        TempVar:HydraBody's Magical Immunity = Off
        Print Message [The body is now vulnerable!]
    }
}
```

**Implementation Steps**:
1. Create enemy entries in scene.bin (Hydra A, B, C, D)
2. Write AI script with death counters and party switches
3. Configure field script to enable multi-party mode
4. Assign battle location (reuse Bizarro location 0x0001)
5. Test party rotation triggers

### Limitations

- **Maximum 6 enemy parts** (slots 4-9)
- **No simultaneous rendering** of all 9 characters
- **Battle location reuse** or extensive scene creation required
- **GlobalVar limit** (256 total, shared across game)

---

## Multiplayer/PvP Feasibility

### The Fundamental Challenge

FF7 was designed as a **single-player, deterministic** game with:
- No networking code whatsoever
- ATB timing based on local frame counters
- Battle state stored in local memory only
- Player input directly modifying battle variables

### What Multiplayer Would Require

#### 1. Networking Layer (Does Not Exist)

**Required Components**:
- TCP/UDP socket implementation
- Packet serialization/deserialization
- Connection management (matchmaking, lobbies)
- Latency compensation
- Disconnection handling

**Estimated Effort**: 4-8 weeks for basic WebSocket implementation

#### 2. Battle State Synchronization

**Critical State to Sync**:
```cpp
// Per-actor state (10 actors * ~100 bytes each)
battle_actor_vars actors[10] = {
    { currentHP, maxHP, currentMP, maxMP, level, defense, ... },
    ...
};

// Global battle state
uint32_t currentFrame;           // Frame counter for timing
uint16_t activeActorMask;        // Who's alive/dead
byte ATB_gauges[10];             // ATB fill states
byte lastCommandIdx;             // Last executed command
uint16_t lastActionIdx;          // Last executed action
```

**Synchronization Strategies**:

| Strategy | Pros | Cons | Feasibility |
|----------|------|------|-------------|
| Full state sync | Simple, no desyncs | High bandwidth (1KB+ per frame) | Low |
| Delta sync | Low bandwidth | Complex diffing, potential desyncs | Medium |
| Lockstep deterministic | Minimal bandwidth | Requires perfect frame sync | Hard |
| Input-only sync | Very low bandwidth | Clients must simulate identically | Very Hard |

**Recommended**: Delta sync with periodic full state snapshots

#### 3. Input Routing & Control

**Current System**:
```text
Player Input → Game reads keyboard/controller →
  Updates issued_command_id/issued_action_id →
    Calls dispatch_chosen_battle_action() →
      Battle state changes
```

**Networked System**:
```text
LOCAL PLAYER:
  Player Input → Block local execution →
    Send to server → Wait for confirmation →
      Execute when authorized

REMOTE PLAYER:
  Receive command packet →
    Inject into issued_command_id/issued_action_id →
      Call dispatch_chosen_battle_action() →
        Battle state changes
```

#### 4. ATB Timing Challenges

**The Problem**: ATB gauges fill based on local frame timing. In multiplayer:
- Player 1 at 60 FPS sees different ATB speeds than Player 2 at 30 FPS
- Network latency causes commands to arrive at different frame counts
- Frame-perfect inputs become non-deterministic

**Solutions**:

1. **Remove ATB Entirely** (Easiest)
   - Convert to pure turn-based
   - Each player takes turns sequentially
   - No timing synchronization needed

2. **Server-Authoritative Timing** (Medium)
   - Server calculates all ATB gauge fills
   - Clients display what server dictates
   - Commands queued and executed on server frame boundaries

3. **Lockstep Simulation** (Hardest)
   - Both clients run identical frame-by-frame simulation
   - Input delays ensure perfect sync
   - Any desync = battle pauses to resync

**Recommendation**: Start with turn-based, add ATB later if feasible

#### 5. Loading Opponent as Enemies

**The Core Challenge**: Enemy models ≠ Character models

**Character Model Structure**:
- Located in `char.lgp` archive
- HRC skeleton + RSD textures + animations
- Designed for party member slots (0-2)

**Enemy Model Structure**:
- Located in `battle.lgp` archive
- Different bone structure, texture formats
- Designed for enemy slots (4-9)

**Required for PvP**:
1. Load opponent's character models into enemy slots (4-6)
2. Remap animations (character attack animations → enemy attack animations)
3. Override enemy AI with networked input commands
4. Synchronize opponent's materia/equipment effects

**Implementation Approach**:
```cpp
// Pseudo-code for loading opponent as enemy
void loadOpponentParty(PartyData opponent, int enemy_slot_offset) {
    for (int i = 0; i < 3; i++) {
        int enemy_slot = 4 + i;  // Slots 4, 5, 6 for opponent's party

        // Load character model into enemy slot
        loadCharacterAsEnemy(opponent.characters[i].model_id, enemy_slot);

        // Copy stats to enemy battle actor
        battle_context->actor_vars[enemy_slot].index = opponent.characters[i].char_id;
        battle_context->actor_vars[enemy_slot].level = opponent.characters[i].level;
        battle_context->actor_vars[enemy_slot].currentHP = opponent.characters[i].currentHP;
        battle_context->actor_vars[enemy_slot].maxHP = opponent.characters[i].maxHP;
        // ... copy all stats

        // Disable enemy AI, route to networked input instead
        disableAI(enemy_slot);
        routeInputToNetwork(enemy_slot);
    }
}
```

**Estimated Effort**: 2-4 weeks for basic implementation

---

## FFNx Existing Infrastructure

### Command Injection System

**Location**: `src/ff7/menu.cpp:138-143`

```cpp
void dispatchAttackCommand(){
    *ff7_externals.issued_command_id = 0x01;        // Command type
    *ff7_externals.issued_action_id = 0x0000;       // Action (basic attack)
    *ff7_externals.issued_action_target_type = 0;   // Target type (enemy)
    *ff7_externals.issued_action_target_index = 4;  // Target slot (enemy 0)

    // Execute the command
    ((void(*)())ff7_externals.dispatch_chosen_battle_action)();
}
```

**Key Insight**: FFNx already demonstrates programmatic command injection. This is the foundation for networked commands.

**Command IDs**:
```text
0x01 = Attack
0x02 = Magic
0x03 = Summon
0x04 = Item
0x05 = E.Skill
0x06 = W-Item
0x07 = W-Magic
0x08 = W-Summon
0x09 = Mime
0x0A = Defend
0x0B = Limit Break
```

**Target Types**:
```text
0 = Single enemy
1 = All enemies
2 = Random enemy
3 = Single ally
4 = All allies
5 = Self
```

### Battle State Access

**Location**: `src/ff7.h:3538`

```cpp
// Global battle context (1 instance)
battle_ai_context *battle_context;

struct battle_ai_context {
    byte lastCommandIdx;           // Last command executed
    uint16_t lastActionIdx;        // Last action executed
    uint16_t activeActorMask;      // Bitmask: which actors are active
    uint16_t actorAlliesMask;      // Bitmask: which are allies
    uint16_t actorEnemiesMask;     // Bitmask: which are enemies
    battle_actor_vars actor_vars[10];  // Full data for all 10 actors
    // ... additional battle state
};
```

**Per-Actor State**: `src/ff7.h:687-743`

```cpp
struct battle_actor_vars {
    uint32_t statusMask;           // Status effects (bitmask)
    byte index;                    // Character/Enemy ID
    byte level;                    // Level
    byte formationID;              // Enemy formation ID
    int currentHP;                 // Current HP
    int maxHP;                     // Max HP
    uint16_t currentMP;            // Current MP
    uint16_t maxMP;                // Max MP
    uint16_t attack;               // Attack stat
    uint16_t defense;              // Defense stat
    uint16_t magicAttack;          // Magic stat
    uint16_t magicDefense;         // Magic defense
    byte dexterity;                // Dexterity
    byte luck;                     // Luck
    // ... materia, equipment, status timers
};
```

**Reading State Example**:
```cpp
// Get current HP of party member 0
int cloud_hp = ff7_externals.battle_context->actor_vars[0].currentHP;

// Check if enemy 2 (slot 6) is dead
uint16_t active_mask = ff7_externals.battle_context->activeActorMask;
bool enemy2_alive = (active_mask & (1 << 6)) != 0;

// Get ATB gauge fill for Tifa (slot 1)
byte tifa_atb = ff7_externals.g_battle_model_state[1].ATB_gauge;
```

### Input Blocking

**Location**: `src/input.cpp:165-185`

```cpp
byte* GetGameKeyState() {
    IDirectInputDeviceA* keyboard_device = *common_externals.keyboard_device;

    // Check if input should be blocked
    if (blockKeys || !gamehacks.canInputBeProcessed()) {
        std::memset(keys, 0, 256);  // Zero out all key states
        return keys;
    }

    // Normal input processing
    keyboard_device->GetDeviceState(256, keys);
    return keys;
}

// External interface
void SetBlockKeysFromGame(bool block) {
    blockKeys = block;
}
```

**Use Case for Multiplayer**:
```cpp
// When it's remote player's turn
SetBlockKeysFromGame(true);   // Block local input

// When it's local player's turn
SetBlockKeysFromGame(false);  // Allow input
```

### Animation Event Queue

**Location**: `src/ff7.h:3539-3540`

```cpp
struct battle_anim_event {
    byte attackerID;        // Who is performing the action (0-9)
    byte commandIndex;      // Command type (Attack, Magic, etc.)
    uint16_t actionIndex;   // Specific action ID (which spell, item, etc.)
    uint16_t cameraData;    // Camera positioning data
    byte targetMask;        // Which actors are targeted (bitmask)
    // ... animation timing data
};

std::span<battle_anim_event> anim_event_queue;  // 64 events max
byte* anim_event_index;  // Current queue position
```

**How Commands Trigger Animations**:
```text
1. Player chooses "Fire on Enemy 2"
2. dispatch_chosen_battle_action() called
3. Adds event to anim_event_queue:
   {
       attackerID: 0 (Cloud),
       commandIndex: 0x02 (Magic),
       actionIndex: 0x0003 (Fire),
       targetMask: 0x40 (binary 01000000 = slot 6)
   }
4. Animation system processes queue each frame
5. Plays Cloud casting animation → Fire spell effect → Enemy hit reaction
```

**Networked Command Flow**:
```cpp
// Receive command from network
NetworkPacket packet = receiveFromOpponent();

// Inject into animation queue
battle_anim_event event = {
    .attackerID = packet.actor_slot,      // Opponent's character (4-6)
    .commandIndex = packet.command_id,
    .actionIndex = packet.action_id,
    .targetMask = packet.target_mask
};
addToAnimQueue(event);  // FFNx would need to expose this
```

### Model State Access

**Location**: `src/ff7.h:3454-3455`

```cpp
// Battle model state (animations, positions, effects)
std::span<battle_model_state> g_battle_model_state;  // 10 actors

struct battle_model_state {
    vector3d modelPosition;     // 3D position in battle scene
    byte commandID;             // Currently executing command
    uint16_t actionIdx;         // Currently executing action
    byte animationID;           // Current animation
    byte ATB_gauge;             // ATB fill (0-255)
    // ... rotation, scale, animation frame
};
```

**Use Cases**:
```cpp
// Check if character is ready to act
if (ff7_externals.g_battle_model_state[0].ATB_gauge == 255) {
    // Cloud's ATB is full
}

// Get current animation for synchronization
byte cloud_anim = ff7_externals.g_battle_model_state[0].animationID;
```

### Existing Hook Points

**Function Replacement System**: `src/ff7_opengl.cpp`

```cpp
// FFNx can replace any game function with custom implementation
replace_function(ff7_externals.dispatch_chosen_battle_action, custom_dispatch);

void custom_dispatch() {
    // Intercept command before execution
    byte cmd = *ff7_externals.issued_command_id;
    uint16_t action = *ff7_externals.issued_action_id;

    // Send to network
    sendCommandToOpponent(cmd, action);

    // Call original function
    ((void(*)())original_dispatch_chosen_battle_action)();
}
```

**Available Hooks** (already demonstrated in FFNx):
- `dispatch_chosen_battle_action` - Command execution
- `display_battle_action_text_sub_6D71FA` - Action display text
- `battle_sub_6DB0EE` - Main battle loop (per-frame)
- `set_battle_targeting_data` - Targeting system

---

## Implementation Roadmap

### Phase 1: Proof of Concept - Battle Recording/Replay
**Duration**: 1-2 weeks
**Difficulty**: Easy-Medium
**Goal**: Prove command injection works deterministically

**Tasks**:
1. Hook `dispatch_chosen_battle_action()` to log all commands
2. Record to file:
   ```cpp
   struct RecordedCommand {
       uint32_t frame_number;
       byte actor_slot;
       byte command_id;
       uint16_t action_id;
       byte target_type;
       byte target_index;
   };
   ```
3. Implement replay system:
   - Load recorded battle
   - Block player input (`SetBlockKeysFromGame(true)`)
   - Inject commands at matching frame numbers
4. Verify determinism (replay produces identical results)

**Success Criteria**:
- ✅ Full battle can be recorded to file
- ✅ Replay produces identical HP/MP/status changes
- ✅ No input from player required during replay

**Deliverables**:
- `battle_recorder.cpp` - Recording implementation
- `battle_replayer.cpp` - Replay implementation
- Sample recorded battles (.brec files)

---

### Phase 2: Ghost Battle Mode
**Duration**: 2-4 weeks
**Difficulty**: Medium
**Goal**: Load opponent's recorded battle and fight against their "ghost"

**Tasks**:
1. Export party data structure:
   ```cpp
   struct ExportedParty {
       PartyMember members[3];
       RecordedCommand commands[1000];  // Full battle recording
   };

   struct PartyMember {
       byte char_id;        // Character (0=Cloud, 1=Barret, etc.)
       byte level;
       uint16_t currentHP;
       uint16_t maxHP;
       uint16_t currentMP;
       uint16_t maxMP;
       Equipment equipment;
       Materia materia[8];
   };
   ```

2. Load opponent's party into enemy slots (4-6):
   ```cpp
   void loadOpponentAsGhost(ExportedParty* opponent) {
       for (int i = 0; i < 3; i++) {
           int enemy_slot = 4 + i;

           // Load character model as enemy
           loadCharacterModel(opponent->members[i].char_id, enemy_slot);

           // Copy stats
           battle_context->actor_vars[enemy_slot] = convertToActorVars(opponent->members[i]);

           // Route commands to replay instead of AI
           disableAI(enemy_slot);
           attachRecording(enemy_slot, opponent->commands);
       }
   }
   ```

3. Implement replay-driven AI:
   - Enemy's "AI" reads from recorded commands
   - Executes commands at appropriate times
   - Player fights against pre-recorded opponent

**Success Criteria**:
- ✅ Opponent's party loads correctly as enemies
- ✅ Opponent's attacks match recorded battle
- ✅ Player can fight and defeat "ghost" opponent

**Deliverables**:
- `ghost_loader.cpp` - Party-to-enemy conversion
- `replay_ai.cpp` - Replay-driven AI system
- Ghost battle files (.ghost)

---

### Phase 3: Async Turn-Based Multiplayer
**Duration**: 4-8 weeks
**Difficulty**: Medium-Hard
**Goal**: Real multiplayer battles using turn-based system (no ATB)

**Tasks**:

1. **Networking Layer** (2-3 weeks)
   ```cpp
   class BattleNetworkClient {
   public:
       bool connect(const char* server_address, uint16_t port);
       void disconnect();

       void sendCommand(BattleCommand cmd);
       bool receiveCommand(BattleCommand* out_cmd);

       void sendPartyData(ExportedParty party);
       bool receivePartyData(ExportedParty* out_party);

   private:
       WebSocket ws_connection;  // Or raw TCP socket
   };
   ```

   **Technology Options**:
   - WebSocket (recommended) - Easy debugging, works through firewalls
   - Raw TCP sockets - Lower latency, more complex
   - UDP - Lowest latency, requires packet loss handling

2. **Battle Initialization** (1 week)
   ```cpp
   void initNetworkedBattle() {
       // Exchange party data
       client.sendPartyData(getLocalParty());
       ExportedParty opponent;
       client.receivePartyData(&opponent);

       // Load opponent as enemies
       loadOpponentAsEnemy(&opponent);

       // Disable ATB, enable turn-based
       setTurnBasedMode(true);

       // Determine turn order (by speed stat)
       calculateTurnOrder();
   }
   ```

3. **Turn-Based Combat Loop** (2-3 weeks)
   ```cpp
   void processBattleTurn() {
       Actor current_actor = turn_queue.front();

       if (current_actor.is_local) {
           // Local player's turn
           SetBlockKeysFromGame(false);  // Allow input
           waitForPlayerCommand();       // Block until command chosen

           BattleCommand cmd = getPlayerCommand();
           client.sendCommand(cmd);      // Send to opponent
           executeCommand(cmd);          // Execute locally

       } else {
           // Opponent's turn
           SetBlockKeysFromGame(true);   // Block input
           displayMessage("Opponent's turn...");

           BattleCommand cmd;
           client.receiveCommand(&cmd);  // Wait for opponent's command
           executeCommand(cmd);          // Execute received command
       }

       turn_queue.pop();
       checkBattleEnd();
   }
   ```

4. **Synchronization & Error Handling** (1-2 weeks)
   - Periodic state checksums to detect desyncs
   - Reconnection handling for dropped connections
   - Timeout detection (opponent disconnected)
   - Cheat detection (impossible HP values, etc.)

**Success Criteria**:
- ✅ Two players can connect via network
- ✅ Players see each other's parties as enemies
- ✅ Turns alternate smoothly between players
- ✅ Battle concludes with win/loss result
- ✅ Disconnections handled gracefully

**Deliverables**:
- `network_client.cpp` - Networking implementation
- `turn_based_controller.cpp` - Turn-based battle logic
- Matchmaking server (simple Node.js/Python server)
- User guide for port forwarding / local network setup

---

### Phase 4: Real-Time ATB Multiplayer (Ambitious)
**Duration**: 3-6 months
**Difficulty**: Very Hard
**Goal**: Full ATB multiplayer with real-time synchronization

**Why This Is Hard**:
- Requires lockstep networking (both clients simulate identically frame-by-frame)
- Frame timing must be perfectly synchronized (60 FPS on both clients)
- Any desync requires pause → full state resync → resume
- Latency compensation for inputs (predict future frames)

**Tasks**:

1. **Deterministic Simulation** (4-6 weeks)
   - Make battle system fully deterministic (remove all RNG variations)
   - Use shared random seed between clients
   - Ensure identical frame timing (60 FPS locked)

2. **Lockstep Networking** (4-8 weeks)
   ```cpp
   void lockstepFrame() {
       // Collect local input
       InputState local_input = getLocalInput();

       // Send to opponent
       client.sendInput(current_frame, local_input);

       // Receive opponent's input for THIS SAME FRAME
       InputState remote_input;
       client.receiveInput(current_frame, &remote_input);

       // BOTH clients simulate this frame with IDENTICAL inputs
       simulateFrame(local_input, remote_input);

       current_frame++;
   }
   ```

3. **Latency Compensation** (2-4 weeks)
   - Input delay (delay local inputs by N frames to match network latency)
   - Rollback netcode (if desync detected, rollback frames and resimulate)
   - Prediction (predict opponent's inputs to hide latency)

4. **State Verification** (2-3 weeks)
   - Periodic checksum exchanges
   - Desync detection (if checksums don't match)
   - Full state resync protocol

**Success Criteria**:
- ✅ ATB gauges fill in real-time on both clients
- ✅ Commands execute with <100ms perceived latency
- ✅ Battles complete without desyncs
- ✅ Works over internet (not just LAN)

**Deliverables**:
- `lockstep_network.cpp` - Lockstep implementation
- `rollback_engine.cpp` - Rollback netcode
- Comprehensive testing suite
- Public beta server

**Realistic Assessment**: This phase approaches the complexity of rewriting FF7's battle system from scratch. May be more practical to wait for OpenVII or similar open-source reimplementations.

---

## Technical Specifications

### Network Protocol Design

**Packet Types**:
```cpp
enum PacketType : uint8_t {
    PARTY_DATA = 0x01,      // Initial party exchange
    COMMAND = 0x02,         // Battle command
    STATE_SYNC = 0x03,      // Full state snapshot
    CHECKSUM = 0x04,        // State verification
    HEARTBEAT = 0x05,       // Connection keepalive
    DISCONNECT = 0x06       // Graceful disconnect
};
```

**Command Packet Structure**:
```cpp
struct BattleCommandPacket {
    uint8_t packet_type;     // 0x02 (COMMAND)
    uint32_t frame_number;   // Frame when executed
    uint8_t actor_slot;      // Who executes (0-9)
    uint8_t command_id;      // Command type (0x01 = Attack, etc.)
    uint16_t action_id;      // Specific action
    uint8_t target_type;     // Target type
    uint8_t target_index;    // Target slot
    uint32_t checksum;       // CRC32 of above fields
} __attribute__((packed));   // 16 bytes total
```

**Party Data Packet**:
```cpp
struct PartyDataPacket {
    uint8_t packet_type;     // 0x01 (PARTY_DATA)
    uint8_t num_members;     // 1-3

    struct Member {
        uint8_t char_id;     // Character ID
        uint8_t level;       // Level
        uint16_t currentHP;
        uint16_t maxHP;
        uint16_t currentMP;
        uint16_t maxMP;
        uint16_t attack;
        uint16_t defense;
        uint16_t magic;
        uint16_t magic_def;
        uint8_t dexterity;
        uint8_t luck;

        // Equipment
        uint16_t weapon_id;
        uint16_t armor_id;
        uint16_t accessory_id;

        // Materia (8 slots)
        struct {
            uint16_t materia_id;
            uint32_t ap;
        } materia[8];
    } members[3];

    uint32_t checksum;
} __attribute__((packed));  // ~300 bytes
```

### State Synchronization

**Full State Snapshot** (for desyncs or new connections):
```cpp
struct BattleStateSnapshot {
    uint32_t frame_number;

    // All 10 actors
    struct ActorState {
        uint32_t statusMask;
        int currentHP;
        int maxHP;
        uint16_t currentMP;
        uint16_t maxMP;
        byte ATB_gauge;
        // ... all relevant state
    } actors[10];

    // Battle flags
    uint16_t activeActorMask;
    uint16_t actorAlliesMask;
    uint16_t actorEnemiesMask;

    // RNG state (for determinism)
    uint32_t random_seed;

    uint32_t checksum;
} __attribute__((packed));  // ~500 bytes
```

**Checksum Calculation**:
```cpp
uint32_t calculateBattleChecksum() {
    uint32_t crc = 0xFFFFFFFF;

    for (int i = 0; i < 10; i++) {
        battle_actor_vars* actor = &battle_context->actor_vars[i];
        crc = crc32_update(crc, &actor->currentHP, sizeof(int));
        crc = crc32_update(crc, &actor->currentMP, sizeof(uint16_t));
        crc = crc32_update(crc, &actor->statusMask, sizeof(uint32_t));
    }

    return crc;
}
```

### Memory Layout

**Battle System Memory Map** (FF7 PC Steam version):

```text
Base Address: 0x00DC0000 (battle module loaded dynamically)

Offsets (relative to battle base):
  +0x0000: Battle context pointer
  +0x0100: Actor vars array (10 actors * ~200 bytes = 2KB)
  +0x0900: ATB gauge array (10 bytes)
  +0x0910: Animation event queue (64 events * 32 bytes = 2KB)
  +0x1910: Model state array (10 actors * ~150 bytes = 1.5KB)

Global variables (absolute addresses):
  0x009ABFE0: issued_command_id (1 byte)
  0x009ABFE1: issued_action_id (2 bytes)
  0x009ABFE4: issued_target_type (1 byte)
  0x009ABFE5: issued_target_index (1 byte)
```

**FFNx Access**:
```cpp
// FFNx dynamically resolves these addresses at runtime
extern ff7_externals;

byte* cmd_id = ff7_externals.issued_command_id;      // 0x009ABFE0
uint16_t* action_id = ff7_externals.issued_action_id; // 0x009ABFE1
```

### Performance Considerations

**Network Bandwidth Estimates**:

| Mode | Packet Size | Packets/Second | Bandwidth |
|------|-------------|----------------|-----------|
| Turn-based | 16 bytes | 0.5 (one command per 2 sec) | 8 bytes/sec |
| Turn-based + State Sync | 16 + 500 bytes | 0.5 + 0.1 | 60 bytes/sec |
| Real-time ATB | 16 bytes | 60 (per frame) | 960 bytes/sec |
| Real-time + Checksums | 16 + 4 bytes | 60 + 10 | 1240 bytes/sec |

**Conclusion**: Even real-time mode uses <2KB/sec bandwidth - network bandwidth is NOT a constraint.

**Latency Requirements**:

| Mode | Acceptable Latency | Playable Experience |
|------|-------------------|---------------------|
| Turn-based | <500ms | Excellent |
| Turn-based | 500-1000ms | Good |
| Turn-based | 1000-2000ms | Frustrating but functional |
| Real-time ATB | <50ms | Excellent |
| Real-time ATB | 50-100ms | Good (requires input delay) |
| Real-time ATB | 100-200ms | Poor (requires rollback) |
| Real-time ATB | >200ms | Unplayable |

---

## Recommendations

### For Custom Multi-Party Bosses

**Recommended Approach**: ✅ Implement using existing tools

**Tools to Use**:
1. **Makou Reactor** - Field script editing
2. **Hojo** - Scene.bin AI script editing
3. **Wallmarket** - Kernel.bin editing (if custom attacks needed)

**Best Practices**:
- Reuse existing battle locations (0x0001, 0x0044, 0x0045) to avoid scene creation
- Keep GlobalVar usage minimal (you have 256 total, shared across entire game)
- Test party switches thoroughly (ensure characters don't duplicate or disappear)
- Document AI scripts clearly (future modders will thank you)

**Example Project**: "FF7 New Threat Mod" already uses multi-party mechanics for custom Weapons battles - study this as reference.

---

### For Multiplayer Implementation

**Phase-Based Approach**: ✅ Start simple, iterate upward

**Recommendation Priority**:

1. **Phase 1 (Recording/Replay)** - START HERE
   - Low risk, high learning value
   - Proves command injection works
   - Useful for debugging and TAS (Tool-Assisted Speedruns)
   - **Time Investment**: 1-2 weeks
   - **Success Rate**: 95%

2. **Phase 2 (Ghost Battles)** - GOOD NEXT STEP
   - Novel gameplay feature (fight your past self)
   - Tests party-to-enemy loading
   - Can be distributed as standalone mod
   - **Time Investment**: 2-4 weeks
   - **Success Rate**: 80%

3. **Phase 3 (Async Turn-Based)** - REALISTIC GOAL
   - Actual multiplayer gameplay
   - Turn-based removes timing complexity
   - Achievable with WebSocket implementation
   - **Time Investment**: 4-8 weeks
   - **Success Rate**: 60%

4. **Phase 4 (Real-Time ATB)** - LONG-TERM AMBITION
   - Significant engineering challenge
   - May require years of development
   - Consider waiting for OpenVII project instead
   - **Time Investment**: 3-6 months (or more)
   - **Success Rate**: 30%

**Technology Stack Recommendation**:

| Component | Recommended Technology | Rationale |
|-----------|----------------------|-----------|
| Network Transport | WebSocket (C++ library: websocketpp) | Cross-platform, firewall-friendly, easy debugging |
| Serialization | JSON (nlohmann/json) | Human-readable, easy debugging |
| Matchmaking Server | Node.js + Socket.io | Quick to develop, well-documented |
| Testing Framework | Google Test | Industry standard, integrates with CI/CD |

---

### Alternative: Open World PvP

**Question**: "Can players meet in open world and battle each other?"

**Technical Reality**: This requires even MORE complexity than arena-based PvP:

**Additional Requirements**:
1. **World Map Synchronization**
   - Player positions on world map
   - Movement synchronization
   - Collision detection

2. **Field Script Synchronization**
   - NPCs, doors, triggers
   - Significantly more state than just battles

3. **Encounter Triggering**
   - Proximity detection for PvP initiation
   - Challenge/accept UI system

**Recommendation**: ❌ Do NOT start here

**Better Alternative**:
- Implement lobby-based matchmaking first (Phase 3)
- Once battles work reliably, THEN consider open world integration
- Or use external launcher/lobby system (like Dark Souls' matchmaking)

**Realistic Timeline**: Add 6-12 months to Phase 3 for open world integration

---

### 9-Character Simultaneous Rendering

**Question**: "Can all 9 characters render on screen at once?"

**Assessment**: ❌ Not feasible without major engine rewrite

**Why It's Hard**:

1. **UI Constraints**
   - Command windows designed for 3 characters
   - ATB bars positioned for 3 characters
   - Status displays assume 3v6 layout

2. **Rendering Pipeline**
   - Model loading slots hardcoded to 3 active characters
   - Battle camera system expects standard formations
   - Animation blending assumes 3v6 layout

3. **Memory Allocation**
   - Character model buffers allocated for 3 active slots
   - Expanding to 9 requires rewriting memory management

**Alternative Solutions**:

1. **UI-Only Display** (Easier)
   - Show HP/MP/status for all 9 characters in UI
   - Still only render 3 active characters in 3D scene
   - Party rotation for actual combat

2. **Picture-in-Picture** (Medium)
   - Split screen showing both active parties
   - Each "screen" renders 3 characters
   - Not truly simultaneous combat

3. **Full Engine Rewrite** (Very Hard)
   - Wait for OpenVII or similar reimplementation
   - Design 9-character rendering from scratch
   - Multi-year project

**Recommendation**: Accept the 3-character limitation and use party rotation (like Bizarro Sephiroth does)

---

## Conclusion

### What's Achievable Today

✅ **Custom Multi-Party Bosses**
- Fully achievable with existing tools
- Copy Bizarro Sephiroth's GlobalVar pattern
- Expected time: 1-2 days per boss (once familiar with tools)

✅ **Battle Recording/Replay**
- Proof-of-concept for multiplayer
- Useful standalone feature
- Expected time: 1-2 weeks

✅ **Ghost Battles**
- Fight against recorded opponents
- Novel gameplay mechanic
- Expected time: 2-4 weeks

⚠️ **Async Turn-Based Multiplayer**
- Technically feasible
- Significant development effort
- Expected time: 4-8 weeks (full-time work)

❌ **Real-Time ATB Multiplayer**
- Extremely complex
- May not be worth the effort
- Expected time: 3-6+ months

❌ **Open World PvP**
- Beyond current scope
- Better suited for full remake project
- Expected time: 1+ year

❌ **9-Character Simultaneous Rendering**
- Requires engine rewrite
- Not practical with current FFNx

---

### Next Steps

**If Interested in Custom Bosses**:
1. Download Makou Reactor and Hojo
2. Extract scene.bin from game files
3. Study Bizarro Sephiroth's AI script (Scene 0x??)
4. Create simple test boss with party rotation
5. Iterate and expand

**If Interested in Multiplayer**:
1. Set up FFNx development environment
2. Implement Phase 1 (Recording/Replay)
3. Test determinism across multiple playthroughs
4. Evaluate feasibility before proceeding to Phase 2
5. Join FFNx Discord for community support

**Resources**:
- FFNx GitHub: https://github.com/julianxhokaxhiu/FFNx
- Makou Reactor: https://github.com/myst6re/makou-reactor
- Qhimm Forums: https://forums.qhimm.com/ (modding community)
- FF7 Scene.bin format: http://wiki.qhimm.com/view/FF7/Scene.bin

---

### Final Thoughts

The Bizarro Sephiroth multi-party mechanic is a brilliant use of FF7's existing systems - GlobalVars, formation chaining, and party rotation. Applying this to custom bosses is absolutely feasible and could create amazing new encounters.

Multiplayer is technically possible, but the scope increases dramatically with each phase. A turn-based async system is achievable by a dedicated developer in 1-2 months. Real-time ATB multiplayer approaches the complexity of writing a new battle system from scratch.

The foundation is there in FFNx - command injection, state access, input blocking. The question is: how much time are you willing to invest?

---

**End of Document**
