# FF7 2026 Reverse Engineering - Activity Log

## Current Status

**Last Updated:** 2026-02-26 20:35 JST (Thursday)
**Session ID:** 334c342d-e070-4590-95e0-3a4126f4bd82
**Tasks Completed:** 12
**Current Task:** create-handoff (Create session handoff document)

---

## Context Summary

This Ralph loop continues the FFVII 2026 Steam Edition reverse engineering task.

### Already Completed (Previous Session)
- All 32 gfx_drv_* functions decompiled and mapped
- Complete 203-entry shim table documented
- VEH Exception-Based Dispatch architecture discovered
- .pdata bulk function creation (20,844/20,853 = 99.96%)
- Key functions identified: global_state_accessor, core_draw_dispatcher, resource_allocator
- candidate_execute_opcode identified at 0x7FF6C8D19A10 (553KB)
- Japanese font loader found at 0x7FF6C9681D90
- Functions #1, #2, #7, #8 of top 10 profiled

### Already Profiled Top 10 Functions
| Rank | Address | Size | Status |
|------|---------|------|--------|
| #1 | 0x7FF6C8D19A10 | 553KB | ✅ Profiled (candidate_execute_opcode) |
| #2 | 0x7FF6C8207AF0 | 334KB | ✅ Profiled (BATTLE MAIN LOOP - 62 callees, 1652 GSA, character data accessor) |
| #3 | 0x7FF6C9571B50 | 128KB | ✅ Profiled (Script VM helper) |
| #4 | 0x7FF6C919F5F0 | 110KB | ✅ Profiled (Field module - dialogue/text) |
| #5 | 0x7FF6C8BC2B80 | 75KB | ✅ Profiled (Battle UI/State subsystem) |
| #6 | 0x7FF6C9331AA0 | 61KB | ✅ Profiled (Script VM opcode handler) |
| #7 | 0x7FF6C9307DC0 | 56KB | ✅ Profiled (48 callees, no callers) |
| #8 | 0x7FF6C90D3CE0 | 53KB | ✅ Profiled (9 callees, opcode-like) |
| #9 | 0x7FF6C95FB250 | 51KB | ✅ Profiled (Script VM high-frequency helper) |
| #10 | 0x7FF6C95B6E50 | 48KB | ✅ Profiled (Script VM opcode handler) |

### Key Addresses (Quick Reference)
| Symbol | Address | Purpose |
|--------|---------|---------|
| IDA Base | 0x7FF6C8110000 | Runtime base for this dump |
| global_state_accessor | 0x7FF6C814F0A0 | Handle → object resolver |
| handle_deref_dword | 0x7FF6C838FE90 | Handle → DWORD |
| handle_deref_word | 0x7FF6C838FEB0 | Handle → WORD |
| Page Table | 0x7FF6C9849010 | Empty in current dump |
| candidate_execute_opcode | 0x7FF6C8D19A10 | 553KB, 923 GSA calls |

### NEW: FF7 Scripting VM Discovery
| Global | Address | Purpose |
|--------|---------|---------|
| VM Stack Pointer | xmmword_7FF6CA1495C8 | Virtual stack for script execution |
| VM Base Pointer | xmmword_7FF6CA1495B8 | Virtual base/frame pointer |
| VM Context Flag | qword_7FF6CA1495D8 | Script execution state flags |

---

## Session Log

### Iteration 1 (2026-02-26 19:20 JST) - Profile Function #3
**Function:** `sub_7FF6C9571B50` (128KB)

**Findings:**
- **Size:** 128,214 bytes (0x1F400)
- **Callers:** 1 - `sub_7FF6C9566E60` (at offset 0x7FF6C9566EF8)
- **Callees:** 9 unique functions:
  - `global_state_accessor` - Handle resolution
  - `sub_7FF6C963BE80` - Stack manipulation helper (uses GSA)
  - `sub_7FF6C8F61030` - Stack/context helper (uses handle 0xDB2BB8)
  - `sub_7FF6C8171A50` - Script context setup (pushes constants 131097, 8086600, etc.)
  - `sub_7FF6C904CBD0` - Memory copy helper (alignment-aware memcpy)
  - `sub_7FF6C95F9EA0` - Unknown
  - `sub_7FF6C95FA400` - Unknown
  - `unk_7FF6C97346B6` - External (likely memcpy)
  - `sub_7FF6C815B2D0` - Return/dispatch helper with timing

**Key Discovery - FF7 Scripting VM:**
- `xmmword_7FF6CA1495C8` = Virtual stack pointer (VM SP)
- `xmmword_7FF6CA1495B8` = Virtual base/frame pointer (VM BP)
- Functions manipulate these globals instead of x86 stack
- Pattern matches FF7's field script execution system
- Caller (`sub_7FF6C9566E60`) has **no xrefs** - called via function pointer table

**Categorization:** **Script VM Helper** - Part of FF7's field/battle script execution engine

**Classification:** This is not a game logic module itself, but infrastructure for the scripting VM. It processes script opcodes using a virtual stack system rather than native x86 stack.

**Related Constants:**
- Handle `0xDB2BB8` - Script context object (close to savemap handle `0xDBFD38`)
- Handle `0xF6E0F0/0xF6E0F4/0xF6E0E8` - Script execution state handles
- Constant `131097` (0x1FFD9) - Script opcode or value
- Constant `8086600/8086664` - Memory addresses or resource IDs

<!-- Agent will append dated entries here -->

---

### Iteration 1 (2026-02-26 19:15 JST) - Profile #3: sub_7FF6C9571B50

**Task:** Profile function #3 (128KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C9571B50` |
| Size | 128,214 bytes (128KB) |
| Callers | 1 (sub_7FF6C9566E60) - NO DIRECT CALLERS (function pointer) |
| Callees | 9 unique |

**Callees Identified:**
1. `global_state_accessor` (0x7FF6C814F0A0) - Handle → object resolver
2. `sub_7FF6C963BE80` - Stack manipulation helper
3. `sub_7FF6C8F61030` - Uses handle 0xDB2BB8 (near savemap region)
4. `sub_7FF6C8171A50` - Script constant pusher (131097, 8086600, 8086664)
5. `sub_7FF6C904CBD0` - Memory copy helper (alignment-aware)
6. `sub_7FF6C95F9EA0` - Unknown
7. `sub_7FF6C95FA400` - Unknown
8. `sub_7FF6C815B2D0` - Return/dispatch helper (timing, sleep)
9. `unk_7FF6C97346B6` - External (likely memcpy)

**Key Discoveries:**

1. **Virtual Stack Machine**: Functions use `xmmword_7FF6CA1495C8` and `xmmword_7FF6CA1495B8` as virtual stack/base pointers for a scripting VM

2. **Script Constant Pattern**:
   - 131097 (0x20059) - FF7 script constant
   - 8086600 (0x7B77B8) - Possible game data handle
   - 8086664 (0x7B77F8) - Possible game data handle
   - Handles 0xF6E0F0, 0xF6E0F4, 0xF6E0E8 - Script-related state

3. **Function Pointer Dispatch**: The caller (sub_7FF6C9566E60) has NO direct callers, indicating this is called via function pointer table - likely the field opcode dispatch table

4. **Category**: **FIELD MODULE - Script VM Helper**
   - Part of FF7's field script execution system
   - Not directly called - dispatched via opcode table
   - Uses virtual stack manipulation pattern

**Updated FFNX_HOOK_MAPPING.md Section 4:**
- Function #3 identified as field script VM helper
- Shares VM infrastructure with candidate_execute_opcode (0x7FF6C8D19A10)

---

### Iteration 2 (2026-02-26 19:30 JST) - Profile #4: sub_7FF6C919F5F0

**Task:** Profile function #4 (110KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C919F5F0` |
| Size | 110,689 bytes (0x1B081, 110KB) |
| Callers | 1 (sub_7FF6C91BAEF0) - 3 calls at different offsets |
| Callees | 11 unique |

**Call Chain:**
- `sub_7FF6C919F5F0` (this function, 110KB)
  - Called by `sub_7FF6C91BAEF0` (0x1B1E = 6,942 bytes) - 3 calls
    - Called by `sub_7FF6C8281E60` (0x5F2 = 1,522 bytes)
      - Called by multiple functions in `0x7FF6C827xxxx` region (battle/dispatch)

**Callees Identified:**
1. `global_state_accessor` (0x7FF6C814F0A0) - Handle → object resolver
2. `handle_deref_dword` (0x7FF6C838FE90) - Handle → DWORD
3. `handle_deref_word` (0x7FF6C838FEB0) - Handle → WORD
4. `sub_7FF6C91BA7D0` (0x556 = 1366 bytes) - Helper in same region
5. `sub_7FF6C81E7BD0` (0x1387 = 4999 bytes) - Heavily-used utility (87+ callers)
6. `unk_7FF6C9677F80` - External function
7. `sub_7FF6C967E120` (0x30D = 781 bytes) - Small function
8. `sub_7FF6C9188840` (0x7C = 124 bytes) - Tiny helper
9. `sub_7FF6C8F2C3F0` (0xB0 = 176 bytes) - Small helper
10. `sub_7FF6C815B1E0` (0xE3 = 227 bytes) - Widespread helper (87+ callers)
11. `sub_7FF6C815B2D0` - Return/dispatch helper (seen in other profiled functions)

**Key Discoveries:**

1. **Field Module Function**: Address range `0x7FF6C919xxxx` is in field module territory, not battle
   - Battle region is typically `0x7FF6C820xxxx - 0x7FF6C829xxxx`
   - This function is in field/text/dialogue processing region

2. **Text Processing Pattern**:
   - Multiple calls to `sub_7FF6C81E7BD0` and `sub_7FF6C815B1E0` (both heavily-used utilities)
   - Both utilities called from 87+ functions across codebase
   - Pattern suggests text/dialogue window management

3. **Game State Access**: Uses GSA + both handle_deref variants
   - Pattern consistent with accessing game object properties
   - May be rendering/display related (field dialogue boxes)

4. **Categorization**: **FIELD MODULE - Text/Dialogue Processing**
   - Part of field module's dialogue/text rendering system
   - Called from wrapper `sub_7FF6C91BAEF0` which is called from battle region dispatch
   - Likely shared text display infrastructure used by both field and battle modules

**Related Functions in Region:**
- `sub_7FF6C916xxxx` through `sub_7FF6C91Fxxxx` - Multiple text processing functions
- All use `sub_7FF6C81E7BD0` heavily (text rendering utility?)

---

### Iteration 3 (2026-02-26 19:40 JST) - Profile #5: sub_7FF6C8BC2B80

**Task:** Profile function #5 (75KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C8BC2B80` |
| Size | ~75KB |
| Callers | 5 calls from 4 functions |
| Callees | 20 unique |

**Callers Identified:**
1. `sub_7FF6C8BBBAC0` - Connected to battle region via `sub_7FF6C826B780`
2. `sub_7FF6C8BD80B0` - **NO XREFS** (function pointer dispatch)
3. `sub_7FF6C8BD9730` - Called from multiple places
4. `sub_7FF6C8BDDE80` - Called twice (2 call sites)

**Callees Identified:**
1. `global_state_accessor` - Handle resolver
2. `handle_deref_dword` - Handle → DWORD
3. `handle_deref_word` - Handle → WORD
4. `sub_7FF6C815B1E0` - Widespread utility (87+ callers)
5. `sub_7FF6C815B2D0` - Return/dispatch helper
6. `sub_7FF6C8BC22C0` - **Local helper** (GSA + dispatch)
7. `sub_7FF6C8BC28C0` - **Local helper** (GSA + dispatch + sub_7FF6C9049520)
8. `sub_7FF6C8BC1EB0` - **Local helper** (GSA + dispatch)
9. `sub_7FF6C8BC1F30` - **Local helper** (GSA + dispatch)
10. `sub_7FF6C8BC1FB0` - **Local helper**
11. `sub_7FF6C8BC2030` - **Local helper**
12. `sub_7FF6C8BC23A0` - **Local helper**
13. `sub_7FF6C903BF40` - Unknown
14. `sub_7FF6C8EC6A40` - Unknown
15. `sub_7FF6C8EC75C0` - Unknown
16. `sub_7FF6C9049520` - Unknown
17. `sub_7FF6C9047AC0` - Unknown
18. `sub_7FF6C903BE70` - Unknown
19. `sub_7FF6C8EC5DF0` - Unknown
20. `sub_7FF6C9022690` - Unknown

**Key Discoveries:**

1. **Cohesive Subsystem**: Address range `0x7FF6C8BCxxxx` contains 6+ local helper functions
   - All local helpers follow pattern: GSA call → dispatch helper
   - This is a self-contained battle subsystem

2. **Battle Region Connection**: Call chain leads to battle dispatch
   - `sub_7FF6C82729F0` (battle region) → `sub_7FF6C826B780` → `sub_7FF6C8BBBAC0` → this function

3. **Function Pointer Dispatch**: One caller (`sub_7FF6C8BD80B0`) has NO xrefs
   - Indicates function pointer call pattern (like opcode dispatch)

4. **Categorization**: **BATTLE MODULE - Battle UI/State Subsystem**
   - Part of battle module's UI or state management
   - Highly cohesive with dedicated helper functions in same region
   - Connected to main battle dispatch chain
   - One caller via function pointer suggests dynamic dispatch

**Region Mapping:**
- `0x7FF6C820xxxx - 0x7FF6C829xxxx` - Core battle module
- `0x7FF6C8BCxxxx` - **Battle UI/State subsystem** (this function)
- `0x7FF6C916xxxx - 0x7FF6C91Fxxxx` - Field text/dialogue

---

### Iteration 3 (2026-02-26 19:40 JST) - Profile #5: sub_7FF6C8BC2B80

**Task:** Profile function #5 (75KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C8BC2B80` |
| Size | ~75KB |
| Callers | 5 calls from 4 functions |
| Callees | 20 unique |

**Callers Identified:**
1. `sub_7FF6C8BBBAC0` (1 call) - Connected to battle region via `sub_7FF6C826B780`
2. `sub_7FF6C8BD80B0` (1 call) - **NO XREFS** (function pointer dispatch)
3. `sub_7FF6C8BD9730` (1 call) - Multiple callers
4. `sub_7FF6C8BDDE80` (2 calls) - Called twice from same function

**Call Chain Analysis:**
```
sub_7FF6C82729F0 (battle region 0x7FF6C827xxxx)
  → sub_7FF6C826B780 (battle dispatch)
    → sub_7FF6C8BBBAC0
      → sub_7FF6C8BC2B80 (this function)

sub_7FF6C8BAC850 → sub_7FF6C8BDDE80 → sub_7FF6C8BC2B80
sub_7FF6C8BBEDE0 → sub_7FF6C8BDDE80 → sub_7FF6C8BC2B80
```

**Callees Identified (20 unique):**
1. `global_state_accessor` - Handle resolver
2. `handle_deref_dword` - Handle → DWORD
3. `handle_deref_word` - Handle → WORD
4. `sub_7FF6C815B1E0` - Widespread utility (87+ callers)
5. `sub_7FF6C815B2D0` - Return/dispatch helper
6. `sub_7FF6C8BC22C0` - Local helper (GSA + dispatch)
7. `sub_7FF6C8BC28C0` - Local helper (GSA + dispatch)
8. `sub_7FF6C8BC1EB0` - Local helper (GSA + dispatch)
9. `sub_7FF6C8BC1F30` - Local helper (GSA + dispatch)
10. `sub_7FF6C8BC1FB0` - Local helper
11. `sub_7FF6C8BC2030` - Local helper
12. `sub_7FF6C8BC23A0` - Local helper
13. `sub_7FF6C903BF40` - Unknown
14. `sub_7FF6C8EC6A40` - Unknown
15. `sub_7FF6C8EC75C0` - Unknown
16. `sub_7FF6C9049520` - Unknown
17. `sub_7FF6C9047AC0` - Unknown
18. `sub_7FF6C903BE70` - Unknown
19. `sub_7FF6C8EC5DF0` - Unknown
20. `sub_7FF6C9022690` - Unknown

**Key Discoveries:**

1. **Cohesive Subsystem**: Address range `0x7FF6C8BCxxxx` contains 6+ helper functions
   - All local helpers use same pattern: GSA → dispatch
   - Indicates self-contained subsystem

2. **Battle Region Connection**:
   - Traces back to battle dispatch via `sub_7FF6C826B780`
   - Region 0x7FF6C8BCxxxx is battle-adjacent

3. **Function Pointer Dispatch**:
   - Caller `sub_7FF6C8BD80B0` has NO direct xrefs
   - Called via function pointer table (likely opcode dispatch)

4. **Categorization**: **BATTLE MODULE - Battle UI/State Subsystem**
   - Cohesive module with dedicated local helpers
   - Connected to main battle dispatch chain
   - May handle battle UI, targeting, or state management

**Address Region Analysis:**
- `0x7FF6C8BCxxxx` = Battle submodule region
- Between core battle (0x7FF6C826xxxx) and field (0x7FF6C919xxxx)
- Contains coordinated set of accessor functions

---

### Iteration 4 (2026-02-26 19:50 JST) - Profile #6: sub_7FF6C9331AA0

**Task:** Profile function #6 (61KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C9331AA0` |
| Size | ~61KB |
| Callers | 1 (`sub_7FF6C934A4C0`) |
| Callees | 64 unique |

**Call Chain (TWO entry points - both NO XREFS):**
```
Path A: ??? → sub_7FF6C917DD40 (NO XREFS) → sub_7FF6C934A4C0 → sub_7FF6C9331AA0

Path B: ??? → sub_7FF6C9180D60 (NO XREFS) → sub_7FF6C9187EF0 → sub_7FF6C934A4C0 → sub_7FF6C9331AA0
```

**Wrapper sub_7FF6C934A4C0 Callees (7):**
1. `global_state_accessor` - Handle resolver
2. `sub_7FF6C932D1C0` - Local helper
3. `sub_7FF6C9330730` - Local helper (same region)
4. `sub_7FF6C81F0190` - Utility
5. `sub_7FF6C9331AA0` - This function (main payload)
6. `sub_7FF6C914C020` - Field module helper
7. `sub_7FF6C815B2D0` - Return/dispatch helper

**Entry Point Analysis:**

**sub_7FF6C917DD40** (NO XREFS - function pointer dispatch):
- Callees: 3 (GSA, sub_7FF6C934A4C0, sub_7FF6C815B2D0)
- Minimal wrapper: just GSA → call → return helper

**sub_7FF6C9180D60** (NO XREFS - function pointer dispatch):
- Callees: 24 including:
  - `global_state_accessor`
  - Multiple VM accessor functions (`sub_7FF6C8156CC0`, `sub_7FF6C8156D80`, `sub_7FF6C8156EA0`)
  - `sub_7FF6C815B2D0` (return/dispatch helper)
  - Field module functions (`sub_7FF6C914C020`, `sub_7FF6C9184D10`)

**Script VM Connection:**
- Entry points call functions that access `xmmword_7FF6CA1495C8` (VM Stack Pointer)
- Entry points call functions that access `xmmword_7FF6CA1495B8` (VM Base Pointer)
- 100+ xrefs to VM globals from `0x7FF6C815xxxx` region
- Pattern matches FF7's field script execution VM

**Key Callees of This Function (64 total):**
- `global_state_accessor` - Handle resolution
- `handle_deref_dword` / `handle_deref_word` - Handle dereferencing
- `sub_7FF6C81E7BD0` - Text utility (87+ callers, seen in field module)
- `sub_7FF6C815B1E0` - Widespread utility (87+ callers)
- `sub_7FF6C815B2D0` - Return/dispatch helper
- Multiple local helpers in `0x7FF6C932xxxx - 0x7FF6C934xxxx` region

**Address Region Mapping:**
- `0x7FF6C815xxxx` - VM accessor functions (manipulate xmmword globals)
- `0x7FF6C914xxxx - 0x7FF6C918xxxx` - Field module entry points
- `0x7FF6C930xxxx - 0x7FF6C935xxxx` - Script VM opcode handlers (THIS REGION)
- `0x7FF6C957xxxx` - Script VM helper (function #3)

**Categorization**: **SCRIPT VM MODULE - Opcode Handler Subsystem**

This function is part of FF7's scripting engine. It's called via function pointer dispatch (no direct callers) through wrapper functions that connect to the VM infrastructure. The 64 callees indicate a complex opcode handler that interacts with:
- Game state via GSA
- Script VM via accessor functions
- Field module via helper functions
- Text rendering via utility functions

**Decompilation:** 511KB output (truncated) - massive function with complex control flow

---

### Iteration 5 (2026-02-26 20:05 JST) - Profile #9: sub_7FF6C95FB250

**Task:** Profile function #9 (51KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C95FB250` |
| Size | ~51KB |
| Callers | 72 calls from multiple functions |
| Callees | 7 unique |

**Callers Breakdown:**
1. `sub_7FF6C95A02C0` (46KB) - **60 calls** (main dispatcher)
2. `sub_7FF6C95B2AC0` - 4 calls (wrapper)
3. `sub_7FF6C95AC2A0` - 6 calls (wrapper, **NO XREFS**)
4. `sub_7FF6C95AB730` - 1 call (wrapper)
5. `sub_7FF6C95ABAD0` - 1 call (wrapper)
6. `sub_7FF6C95AD650` - 1 call (wrapper)
7. `sub_7FF6C95ADC90` - 1 call (wrapper)
8. `sub_7FF6C95AE2D0` - 1 call (wrapper)
9. `sub_7FF6C95AE910` - 1 call (wrapper)
10. `sub_7FF6C95AEF50` - 1 call (wrapper)

**Call Chain:**
```
??? (function pointer table)
  → sub_7FF6C956B7D0 (NO XREFS - 19KB entry point)
    → sub_7FF6C95A02C0 (46KB main dispatcher)
      → sub_7FF6C95FB250 (51KB) [THIS FUNCTION] - 60 calls
    → sub_7FF6C95B2AC0 → sub_7FF6C95FB250 (4 calls)
  → sub_7FF6C95AC2A0 (NO XREFS) → sub_7FF6C95FB250 (6 calls)
```

**Callees Identified (7 unique):**
1. `global_state_accessor` - Handle resolution
2. `sub_7FF6C8171A50` - Script constant pusher (seen in function #3)
3. `sub_7FF6C815B1E0` - Widespread utility (87+ callers)
4. `handle_deref_word` - Handle → WORD
5. `handle_deref_dword` - Handle → DWORD
6. `sub_7FF6C8F2C3F0` - Small helper (seen in function #4)
7. `sub_7FF6C815B2D0` - Return/dispatch helper

**Key Discoveries:**

1. **High-Frequency Helper**: Called 72 times total, 60 from single dispatcher
   - Indicates a core operation used repeatedly during script execution
   - Similar to how an "eval" or "execute" helper might be called for each opcode

2. **Entry Point via Function Pointer**:
   - `sub_7FF6C956B7D0` has NO XREFS - called via function pointer table
   - `sub_7FF6C95AC2A0` has NO XREFS - also function pointer dispatch
   - Confirms script VM dispatch architecture

3. **Wrapper Pattern**:
   - Multiple small wrappers (sub_7FF6C95AB730, etc.) all call:
     - GSA → this function → return helper
   - Consistent pattern suggests opcode-specific wrappers

4. **Address Region Analysis**:
   - `0x7FF6C956xxxx - 0x7FF6C95Fxxxx` - Script VM execution layer
   - Same region as function #3 (sub_7FF6C9571B50)
   - Contains both dispatcher and helper functions

**Categorization**: **SCRIPT VM MODULE - High-Frequency Helper Function**

This function is a frequently-called utility in FF7's script execution system. The 72 calls from a single large dispatcher (sub_7FF6C95A02C0) indicates it's a core operation used for every script instruction or frequently during script interpretation. The pattern of simple callees (GSA, handle_deref, script pusher, return helper) suggests it may be responsible for:
- Fetching script operands
- Resolving variable references
- Accessing game state during script execution

**Region Mapping Updated:**
- `0x7FF6C815xxxx` - VM accessor functions
- `0x7FF6C820xxxx - 0x7FF6C829xxxx` - Core battle module
- `0x7FF6C8BCxxxx` - Battle UI/State subsystem
- `0x7FF6C916xxxx - 0x7FF6C91Fxxxx` - Field text/dialogue
- `0x7FF6C930xxxx - 0x7FF6C935xxxx` - Script VM opcode handlers
- `0x7FF6C956xxxx - 0x7FF6C95Fxxxx` - **Script VM execution layer** (this function)

---

### Iteration 5 (2026-02-26 20:05 JST) - Profile #9: sub_7FF6C95FB250

**Task:** Profile function #9 (51KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C95FB250` |
| Size | ~51KB |
| Callers | 72 calls from 9+ functions |
| Callees | 7 unique |

**Callers Analysis:**
| Caller | Calls | Notes |
|--------|-------|-------|
| sub_7FF6C95A02C0 | 60 | Main dispatcher (46KB) |
| sub_7FF6C95AC2A0 | 6 | NO XREFS (function pointer) |
| sub_7FF6C95B2AC0 | 4 | Called from entry point |
| sub_7FF6C95AB730 | 1 | Wrapper in same region |
| sub_7FF6C95ABAD0 | 1 | Wrapper in same region |
| sub_7FF6C95AD650 | 1 | Wrapper in same region |
| sub_7FF6C95ADC90 | 1 | Wrapper in same region |
| sub_7FF6C95AE2D0 | 1 | Wrapper in same region |
| sub_7FF6C95AE910 | 1 | Wrapper in same region |

**Call Chain:**
```
??? (function pointer table)
  → sub_7FF6C956B7D0 (NO XREFS - 19KB entry point)
    → sub_7FF6C95A02C0 (46KB main dispatcher)
      → sub_7FF6C95FB250 (51KB) [THIS FUNCTION] - 60 calls
    → sub_7FF6C95B2AC0 → sub_7FF6C95FB250 (4 calls)
  → sub_7FF6C95AC2A0 (NO XREFS) → sub_7FF6C95FB250 (6 calls)
```

**Callees Identified (7 unique):**
1. `global_state_accessor` - Handle resolver
2. `handle_deref_dword` - Handle → DWORD
3. `handle_deref_word` - Handle → WORD
4. `sub_7FF6C8171A50` - Script constant pusher (seen in function #3)
5. `sub_7FF6C815B1E0` - Widespread utility (87+ callers)
6. `sub_7FF6C8F2C3F0` - Small helper (seen in function #4)
7. `sub_7FF6C815B2D0` - Return/dispatch helper

**Key Discoveries:**

1. **High-Frequency Helper**: Called 72 times total - unusual for a 51KB function
   - Main dispatcher `sub_7FF6C95A02C0` calls it 60 times
   - Indicates a core operation used repeatedly during script execution

2. **Function Pointer Dispatch**: Entry point `sub_7FF6C956B7D0` has NO XREFS
   - Same pattern as other script VM functions
   - Region `0x7FF6C956xxxx - 0x7FF6C95Fxxxx` is script execution layer

3. **Minimal Callees**: Only 7 callees for a 51KB function
   - GSA + handle deref + script pusher + return helper
   - Pattern suggests a focused utility function, not a dispatcher

4. **Wrapper Pattern**: Multiple small wrappers call this function
   - All wrappers follow same pattern: GSA → this function → return helper
   - Wrappers themselves have NO XREFS (function pointer dispatch)

**Address Region Mapping:**
- `0x7FF6C956xxxx` - Script VM entry point
- `0x7FF6C95Axxxx` - Script dispatcher region
- `0x7FF6C95Bxxxx` - Script helper wrappers
- `0x7FF6C95Fxxxx` - Script helper utilities (this function)

**Categorization**: **SCRIPT VM MODULE - High-Frequency Helper Function**

This function is a frequently-called helper in FF7's script execution system. The 72 calls from a single dispatcher indicate it's a core operation used repeatedly during script execution. It's part of the same VM infrastructure discovered in functions #3 and #6, located in the script execution layer between field module entry points and opcode handlers.

---

### Iteration 6 (2026-02-26 20:25 JST) - Profile #10: sub_7FF6C95B6E50

**Task:** Profile function #10 (48KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C95B6E50` |
| Size | ~48KB |
| Callers | 1 (sub_7FF6C9566E60) - NO DIRECT CALLERS (function pointer) |
| Callees | 10+ (estimated from region pattern) |

**Call Chain:**
```
??? (function pointer table)
  → sub_7FF6C9566E60 (NO XREFS - 15KB entry point, same as function #3)
    → sub_7FF6C95B6E50 (this function, 48KB)
```

**Key Discovery - VM Stack Manipulation:**
On entry, function immediately manipulates VM stack pointer:
```asm
mov     ecx, dword ptr cs:xmmword_7FF6CA1495C8  ; Load VM SP
mov     ebx, dword ptr cs:xmmword_7FF6CA1495C8+4
add     ecx, 0FFFFFFFCh                           ; Decrement by 4 (push)
mov     dword ptr cs:xmmword_7FF6CA1495C8, ecx    ; Store VM SP
call    global_state_accessor
mov     ecx, 0E996C4h                             ; Script handle
mov     [rax], ebx
...
add     eax, 0FFFFFFB0h                           ; Another stack adjustment
call    global_state_accessor
```

**Callees Identified:**
1. `global_state_accessor` (confirmed from disassembly)
2. Other callees estimated from region pattern (GSA, handle_deref, return helper)

**Key Discoveries:**

1. **VM Stack Infrastructure**: Uses `xmmword_7FF6CA1495C8` (VM Stack Pointer) immediately on entry
   - Same VM globals as functions #3, #6, and #9
   - Confirms this is part of FF7's scripting engine

2. **Same Entry Point as Function #3**:
   - Both function #3 (sub_7FF6C9571B50) and function #10 are called from sub_7FF6C9566E60
   - sub_7FF6C9566E60 has NO XREFS - called via function pointer table
   - This entry point is likely a dispatcher that routes to different opcode handlers

3. **Script Handle Pattern**:
   - Uses handle `0xE996C4` (script context object)
   - Similar to handles seen in function #3 (0xDB2BB8, 0xF6E0F0, etc.)

4. **Address Region Mapping:**
   - `0x7FF6C956xxxx` - Script VM entry point (sub_7FF6C9566E60)
   - `0x7FF6C957xxxx` - Script VM helper (function #3)
   - `0x7FF6C95Bxxxx` - Script VM opcode handler (this function)
   - `0x7FF6C95Fxxxx` - Script VM high-frequency helper (function #9)

**Categorization**: **SCRIPT VM MODULE - Opcode Handler**

This function is an opcode handler in FF7's script execution engine. It shares the same entry point (sub_7FF6C9566E60) as function #3, suggesting they're both dispatched from the same function pointer table. The VM stack manipulation on entry confirms it's part of the scripting VM infrastructure discovered in functions #3, #6, and #9.

**Region Mapping Updated:**
- `0x7FF6C815xxxx` - VM accessor functions
- `0x7FF6C820xxxx - 0x7FF6C829xxxx` - Core battle module
- `0x7FF6C8BCxxxx` - Battle UI/State subsystem
- `0x7FF6C916xxxx - 0x7FF6C91Fxxxx` - Field text/dialogue
- `0x7FF6C930xxxx - 0x7FF6C935xxxx` - Script VM opcode handlers (function #6)
- `0x7FF6C956xxxx - 0x7FF6C95Fxxxx` - Script VM execution layer (functions #3, #9, #10)

---

### Iteration 6 (2026-02-26 20:25 JST) - Profile #10: sub_7FF6C95B6E50

**Task:** Profile function #10 (48KB) from top 10 list

**Function Profile:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C95B6E50` |
| Size | ~48KB |
| Callers | 1 (sub_7FF6C9566E60) - NO DIRECT CALLERS (function pointer) |
| Callees | ~10-15 (estimated based on disassembly pattern) |

**Key Discovery - VM Stack Manipulation:**
Function entry code:
```asm
7ff6c95b6e6c  mov     ecx, dword ptr cs:xmmword_7FF6CA1495C8
7ff6c95b6e72  mov     ebx, dword ptr cs:xmmword_7FF6CA1495C8+4
7ff6c95b6e78  add     ecx, 0FFFFFFFCh           ; decrement by 4
7ff6c95b6e7b  mov     dword ptr cs:xmmword_7FF6CA1495C8, ecx
7ff6c95b6e81  call    global_state_accessor
```

This confirms `xmmword_7FF6CA1495C8` is the VM Stack Pointer - same pattern as function #3.

**Callees Identified:**
1. `global_state_accessor` - Handle resolution (confirmed in disassembly)
2. Pattern similar to functions #3 and #9 (script VM helpers)
3. Expected: handle_deref_*, return helper, local helpers

**Call Chain:**
```
??? (function pointer table)
  → sub_7FF6C9566E60 (NO XREFS - 120KB entry point)
    → sub_7FF6C95B6E50 (this function, 48KB)
    → sub_7FF6C9571B50 (function #3, 128KB) - same caller!
```

**Relationship to Function #3:**
- **Same caller**: Both called from sub_7FF6C9566E60
- **Same VM stack**: Both manipulate xmmword_7FF6CA1495C8
- **Same region**: Both in 0x7FF6C95xxxxx (script VM layer)
- **Different sizes**: 48KB vs 128KB (this function is smaller)

**Address Region Analysis:**
- `0x7FF6C95B6E50` - This function (opcode handler)
- `0x7FF6C9566E60` - Entry point (dispatch via function pointer)
- `0x7FF6C9571B50` - Function #3 (VM helper)
- `0x7FF6C95FB250` - Function #9 (high-frequency helper)

All share the same VM infrastructure and entry point dispatch pattern.

**Categorization**: **SCRIPT VM MODULE - Opcode Handler**

This function is part of FF7's script execution engine, dispatched from the same entry point as function #3. The VM stack manipulation at entry confirms it's part of the script VM infrastructure. It's called via function pointer dispatch (no direct callers), consistent with an opcode handler in a switch-table dispatch pattern.

**Key Findings Summary:**
- **Region**: 0x7FF6C95Bxxxx - Script VM execution layer
- **Pattern**: VM stack manipulation → GSA → game state access
- **Role**: Opcode handler or script execution helper
- **Evidence**: Same entry point as function #3, same VM stack access

---

### Iteration 8 (2026-02-26 20:30 JST) - Categorize No-Callers Functions

**Task:** Categorize the two functions with no direct callers (functions #7 and #8 from top 10)

**Function #7: sub_7FF6C9307DC0 (56KB)**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C9307DC0` |
| Size | 56,161 bytes (56KB) |
| Direct Callers | 0 (NO XREFS) |
| Callees | 48 unique |

**Callees Analysis:**
1. `global_state_accessor` - Handle resolution
2. `handle_deref_dword` / `handle_deref_word` - Handle dereferencing
3. `sub_7FF6C81E7BD0` - Text utility (87+ callers)
4. `sub_7FF6C815B2D0` - Return/dispatch helper
5. `sub_7FF6C9680730` - Font/text function (88+ callers)
6. `sub_7FF6C9680410` - Font/text function
7. `sub_7FF6C9680050` - Font/text function
8. Multiple functions in `0x7FF6C91xxxx` and `0x7FF6C92xxxx` regions

**VM Stack Pattern:**
```asm
mov     ecx, dword ptr cs:xmmword_7FF6CA1495C8  ; Load VM SP
mov     ebx, dword ptr cs:xmmword_7FF6CA1495C8+4
add     ecx, 0FFFFFFFCh                           ; Decrement by 4
mov     dword ptr cs:xmmword_7FF6CA1495C8, ecx
call    global_state_accessor
```

**Key Discovery - Font/Text Integration:**
- Calls font functions in `0x7FF6C968xxxx` region
- `sub_7FF6C9680730` uses FNV-1a hash table lookup
- `sub_7FF6C9680730` calls `resource_allocator` with handle `0x6F5B03`
- Font functions read 5+ parameters from VM stack (offsets 4, 8, 0xC, 0x10, 0x14)

**Categorization**: **SCRIPT VM MODULE - Field/Text/Dialogue Opcode Handler**

---

**Function #8: sub_7FF6C90D3CE0 (53KB)**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C90D3CE0` |
| Size | ~53KB |
| Direct Callers | 0 (NO XREFS) |
| Callees | 9 unique |

**Callees Identified:**
1. `global_state_accessor` - Handle resolution
2. `handle_deref_dword` - Handle → DWORD
3. `sub_7FF6C815B2D0` - Return/dispatch helper
4. `sub_7FF6C90D3A80` - Local helper (nearby address)
5. `sub_7FF6C90D3BB0` - Local helper (nearby address)
6. `sub_7FF6C96493F0` - Unknown
7. `sub_7FF6C8EE8CE0` - Unknown
8. `sub_7FF6C8EE8DB0` - Unknown
9. `sub_7FF6C8EE8680` - Unknown

**VM Stack Pattern:**
```asm
mov     ecx, dword ptr cs:xmmword_7FF6CA1495C8  ; Load VM SP
mov     ebx, dword ptr cs:xmmword_7FF6CA1495C8+4
add     ecx, 0FFFFFFFCh                           ; Decrement by 4
mov     dword ptr cs:xmmword_7FF6CA1495C8, ecx
call    global_state_accessor
mov     [rax], ebx                                ; Store to VM stack
```

**Constant Used:**
- `0x917DC4` - Script context handle or value

**Key Observations:**
- **Minimal callees** (only 9) compared to function #7 (48 callees)
- **Local helpers** at `0x7FF6C90D3A80` and `0x7FF6C90D3BB0` (within same region)
- Simpler, more focused than function #7
- Same VM stack pattern as all other script VM functions

**Categorization**: **SCRIPT VM MODULE - Focused Opcode Handler**

---

**Summary:**

Both functions are **Script VM opcode handlers** called via function pointer dispatch:

| Function | Size | Callees | Purpose |
|----------|------|---------|---------|
| sub_7FF6C9307DC0 | 56KB | 48 | Field/Text/Dialogue opcode handler |
| sub_7FF6C90D3CE0 | 53KB | 9 | Focused opcode handler (unknown module) |

**Evidence for Function Pointer Dispatch:**
- Zero xrefs to both functions
- Same VM stack access pattern as all profiled script VM functions
- Same entry pattern: VM SP manipulation → GSA call → game state access

**Script VM Function Count:**
| Rank | Address | Size | Callers | Callees | Category |
|------|---------|------|---------|---------|----------|
| #1 | 0x7FF6C8D19A10 | 553KB | 1 (wrapper, no xrefs) | 24 | Script VM state accessor |
| #2 | 0x7FF6C8207AF0 | 334KB | TBD | TBD | Battle candidate |
| #3 | 0x7FF6C9571B50 | 128KB | 1 (no xrefs) | 9 | Script VM helper |
| #4 | 0x7FF6C919F5F0 | 110KB | 1 | 11 | Field text/dialogue |
| #5 | 0x7FF6C8BC2B80 | 75KB | 4 | 20 | Battle UI/State |
| #6 | 0x7FF6C9331AA0 | 61KB | 1 (no xrefs) | 64 | Script VM opcode handler |
| #7 | 0x7FF6C9307DC0 | 56KB | 0 | 48 | Script VM field/text opcode |
| #8 | 0x7FF6C90D3CE0 | 53KB | 0 | 9 | Script VM focused opcode |
| #9 | 0x7FF6C95FB250 | 51KB | 9+ (72 calls) | 7 | Script VM high-frequency helper |
| #10 | 0x7FF6C95B6E50 | 48KB | 1 (no xrefs) | ~10 | Script VM opcode handler |

**Region Mapping Updated:**
- `0x7FF6C815xxxx` - VM accessor functions
- `0x7FF6C820xxxx - 0x7FF6C829xxxx` - Core battle module
- `0x7FF6C8BCxxxx` - Battle UI/State subsystem
- `0x7FF6C8D0xxxx - 0x7FF6C8D1xxxx` - Script VM state accessor (function #1)
- `0x7FF6C8EExxxx` - Unknown helper region (called by function #8)
- `0x7FF6C90Dxxxx` - Script VM focused opcode handler (function #8)
- `0x7FF6C916xxxx - 0x7FF6C91Fxxxx` - Field text/dialogue
- `0x7FF6C930xxxx - 0x7FF6C935xxxx` - Script VM opcode handlers
- `0x7FF6C956xxxx - 0x7FF6C95Fxxxx` - Script VM execution layer
- `0x7FF6C964xxxx` - Unknown (called by function #8)
- `0x7FF6C968xxxx` - Font/text rendering functions

---

### Iteration 7 (2026-02-26 21:00 JST) - Verify candidate_execute_opcode

**Task:** Verify if candidate_execute_opcode (sub_7FF6C8D19A10) is the field opcode dispatcher

**Function Analysis:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C8D19A10` |
| Size | 553,137 bytes (553KB) |
| Direct Callers | 1 (`sub_7FF6C8D046A0` - 109 byte wrapper) |
| Callees | 24 unique |
| GSA Calls | 1,124 |
| Handle Deref Calls | 2,089 (1,453 dword + 636 word) |

**Caller Analysis (sub_7FF6C8D046A0):**
```c
__int64 sub_7FF6C8D046A0() {
  // VM stack push
  v0 = DWORD1(xmmword_7FF6CA1495C8);
  LODWORD(xmmword_7FF6CA1495C8) = xmmword_7FF6CA1495C8 - 4;
  *(_DWORD *)global_state_accessor(xmmword_7FF6CA1495C8) = v0;
  DWORD1(xmmword_7FF6CA1495C8) = xmmword_7FF6CA1495C8;
  LODWORD(xmmword_7FF6CA1495C8) -= 4;

  candidate_execute_opcode();  // Main function call

  // VM stack pop and return
  v1 = global_state_accessor(xmmword_7FF6CA1495C8);
  if (v1) LODWORD(v1) = *v1;
  LODWORD(xmmword_7FF6CA1495C8) += 4;
  DWORD1(xmmword_7FF6CA1495C8) = (_DWORD)v1;
  sub_7FF6C815B2D0();  // Return/dispatch helper
  LODWORD(xmmword_7FF6CA1495C8) += 4;
}
```

**Caller XREFs:** NONE - called via function pointer dispatch

**Top Callees by Frequency:**
1. `handle_deref_dword` - 1,453 calls
2. `global_state_accessor` - 1,124 calls
3. `handle_deref_word` - 636 calls
4. `sub_7FF6C8D02EB0` - 33 calls
5. `sub_7FF6C8D18AE0` - 24 calls

**Evidence Against Opcode Dispatcher:**

1. **No Indirect Jumps**: Searched entire function for `jmp rax` or `jmp [table]` patterns - found ZERO
2. **No Switch Patterns**: Only 3 unique comparison values < 256 (0x40, 0x04, 0x03)
3. **Massive Handle Dereferencing**: 2,089 handle_deref calls indicates state accessor, not dispatcher
4. **Table at 0x7FF6C980EAD0**: 1-bit lookup table (128 zeros, 128 ones) - NOT function pointer table
5. **VM Stack Manipulation**: Immediate VM stack operations at entry, not dispatch pattern
6. **Function Pointer Call**: Wrapper has no xrefs, called via function pointer

**Code Pattern at Entry:**
```asm
mov     eax, dword ptr cs:xmmword_7FF6CA1495C8  ; Load VM SP
sub     eax, 4                                      ; Decrement (push)
mov     dword ptr cs:xmmword_7FF6CA1495C8, eax    ; Store VM SP
call    global_state_accessor
...
sub     eax, 16Ch                                   ; Large stack offset
```

**Categorization**: **SCRIPT VM STATE ACCESSOR - NOT OPCODE DISPATCHER**

This is a massive helper function in the script VM infrastructure that:
- Processes game state through extensive handle resolution
- Uses virtual stack (xmmword_7FF6CA1495C8) for VM operations
- Called via function pointer dispatch like other script VM functions
- NOT the field opcode dispatcher - no dispatch mechanism found

**Implications:**
- The actual field opcode dispatcher must use a different mechanism
- May be the 256-entry function pointer table mentioned in FFNx docs
- The "no-callers" functions (profile-7, profile-8) may be entry points to the real dispatcher

**Updated FFNX_HOOK_MAPPING.md:**
- Section 4 entry for `candidate_execute_opcode` should be updated to reflect this finding
- Continue searching for actual opcode dispatch mechanism

---

### Iteration 7 (2026-02-26 21:00 JST) - verify-execute-opcode

**Task:** Verify candidate_execute_opcode is the field opcode dispatcher

**Function Analyzed:** `sub_7FF6C8D19A10` (553KB)

**Analysis Performed:**
1. Disassembled function entry (500 bytes)
2. Searched for indirect jump patterns (jmp rax, jmp [table])
3. Analyzed comparison values for switch patterns
4. Examined table at 0x7FF6C980EAD0
5. Profiled callees and call patterns
6. Checked xrefs to entry points

**Key Findings:**

**NOT an opcode dispatcher - Evidence Against:**
1. **No indirect jumps** - Zero `jmp rax` or `jmp [table]` patterns in 553KB function
2. **No switch patterns** - Only 3 unique comparison values < 256 (0x40, 0x04, 0x03)
3. **No 256-entry table** - Table at `0x7FF6C980EAD0` is a 1-bit lookup (128 zeros, 128 ones)
4. **Massive state access** - 2089 handle_deref calls, 1124 GSA calls
5. **Only 24 unique callees** - Not a dispatcher with many branch targets

**What It Actually Is:**
- **Script VM state accessor function**
- Uses VM stack infrastructure (`xmmword_7FF6CA1495C8`)
- Called via wrapper `sub_7FF6C8D046A0` (109 bytes)
- Wrapper has NO XREFS - function pointer dispatch pattern

**Call Chain:**
```
??? (function pointer table)
  → sub_7FF6C8D046A0 (109-byte wrapper, NO XREFS)
    → sub_7FF6C8D19A10 (553KB state accessor)
```

**Wrapper Decompiled:**
```c
__int64 sub_7FF6C8D046A0() {
  // Push to VM stack
  xmmword_7FF6CA1495C8 -= 4;
  *global_state_accessor(xmmword_7FF6CA1495C8) = xmmword_7FF6CA1495C8[1];
  xmmword_7FF6CA1495C8[1] = xmmword_7FF6CA1495C8;
  xmmword_7FF6CA1495C8 -= 4;

  candidate_execute_opcode();  // 553KB state accessor

  // Pop from VM stack
  v1 = global_state_accessor(xmmword_7FF6CA1495C8);
  if (v1) *v1 = *v1;
  xmmword_7FF6CA1495C8 += 4;
  xmmword_7FF6CA1495C8[1] = v1;

  return sub_7FF6C815B2D0();  // Return/dispatch helper
}
```

**Table Analysis (0x7FF6C980EAD0):**
- 512 bytes examined
- Only values: 0x00 and 0x01
- Exactly 128 zeros, 128 ones
- Purpose: 1-bit property lookup (possibly opcode validity flag)
- NOT a function pointer table

**Categorization**: **SCRIPT VM MODULE - State Accessor**

This function is NOT the field opcode dispatcher. It's a massive state accessor that processes game state through the VM infrastructure. The actual opcode dispatcher has not been found yet - it's likely in a different region or uses a different dispatch mechanism (possibly the function pointer tables that call the entry points we've discovered).

**Remaining Task:** Find the actual field opcode dispatcher. Candidates:
- Function pointer tables containing our known entry points
- A region with 256-way dispatch (jmp/call through table)
- The "no callers" functions (sub_7FF6C9307DC0, sub_7FF6C90D3CE0)

---

### Iteration 7 (2026-02-26 21:00 JST) - Verify candidate_execute_opcode

**Task:** Verify if `candidate_execute_opcode` (sub_7FF6C8D19A10) is the field opcode dispatcher

**Analysis Performed:**
1. Decompiled function prologue (500 bytes)
2. Analyzed control flow patterns (911 jz branches, 0 indirect jumps)
3. Counted comparison values (< 256): only 3 unique values
4. Examined table at 0x7FF6C980EAD0
5. Profiled callees (24 unique, 2089 handle_deref, 1124 GSA)

**Evidence Against Dispatch Role:**
| Evidence | Finding |
|----------|---------|
| Indirect jumps | 0 (dispatcher would have jump table) |
| Small comparison values | Only 3 (dispatcher would test 256 opcodes) |
| jz branches | 911 in first 10k instructions (state machine, not switch) |
| Table lookup | 1-bit lookup table (128 zeros, 128 ones) - NOT function pointers |
| Callee pattern | 2089 handle_deref, 1124 GSA (state accessor, not dispatcher) |
| Caller | Single wrapper via function pointer |

**What It Actually Is:**
- **Script VM State Accessor** - 553KB function that processes game state
- Called via wrapper `sub_7FF6C8D046A0` (109 bytes, no xrefs)
- Uses VM stack infrastructure (`xmmword_7FF6CA1495C8`)
- Part of script execution infrastructure, NOT the opcode dispatcher

**Prologue Analysis:**
```asm
mov     eax, 5CA8h           ; Large stack frame (23720 bytes)
call    __alloca_probe
sub     rsp, rax
mov     eax, xmmword_7FF6CA1495C8  ; VM Stack Pointer
sub     eax, 4               ; Stack push
mov     xmmword_7FF6CA1495C8, eax
call    global_state_accessor
; ... extensive handle dereferencing follows
```

**Callees (Top 15):**
| Function | Calls |
|----------|-------|
| handle_deref_dword | 1453 |
| global_state_accessor | 1124 |
| handle_deref_word | 636 |
| sub_7FF6C8D02EB0 | 33 |
| sub_7FF6C8D18AE0 | 24 |

**Conclusion:** `candidate_execute_opcode` is **NOT** the field opcode dispatcher. It is a massive script VM state accessor function that processes game state through extensive handle resolution. The actual opcode dispatch mechanism remains unknown - likely uses indirect dispatch through registers or a different pattern not yet identified.

**Updated FFNX_HOOK_MAPPING.md:** Section 4 entry corrected

---

### Iteration 9 (2026-02-26 21:50 JST) - Find Battle Functions

**Task:** Identify battle module functions

**Function Profile: sub_7FF6C8207AF0 (334KB)**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C8207AF0` |
| Size | 333,912 bytes (334KB) |
| Callers | 5 functions |
| Callees | 62 unique |
| GSA Calls | 1,652 |
| Handle Deref Calls | 1,650 (855 dword + 795 word) |

**Callers Identified:**
1. `sub_7FF6C8274980` - Via wrapper chain from battle state machine
2. `sub_7FF6C8285080` - Direct caller
3. `sub_7FF6C8285550` - Direct caller
4. `sub_7FF6C8AF1840` - Direct caller
5. `sub_7FF6C8B08980` - Direct caller

**Entry Point Analysis:**
- `sub_7FF6C8270DE0` (NO XREFS) - Battle state machine entry, dispatched via function pointer
- `sub_7FF6C8271CE0` (NO XREFS) - Another battle entry point
- Both use VM stack (`xmmword_7FF6CA1495C8`)

**Key Callee: sub_7FF6C825A7E0**
- Called 40 times from battle main loop
- Uses constant 6892 (0x1AEC) - FF7 character data size
- Uses offset 12456372 (0xBE28D4) - Character data base
- Purpose: Access character stats/HP/MP in battle

**Battle Memory Addresses Discovered:**
| Address | Purpose |
|---------|---------|
| `0x9AE108` | Battle state (0=init, 1=started, 2=continue, 3=setup) |
| `0xBE28D4` | Character data base offset |
| `0xBFCDFC` | Battle phase (0-6) |
| `0xBF2DEC` | Battle status |
| `0xBF2A30` | Battle flag |
| `0xCC0828` | Battle flag |
| `0xBE1128` | Battle data pointer |
| `0xC05F7C` | Screen width (512) |

**State Machine Constants:**
- State values: 0, 1, 2, 3, 4, 6 (from `0xBFCDFC` assignments)
- Handles battle initialization, setup, and main loop

**Region Mapping:**
- `0x7FF6C820xxxx - 0x7FF6C82Axxxx` - Core battle module
- Entry points dispatched via function pointer table

**Categorization**: **BATTLE MODULE - Main Loop & State Machine**

The battle system uses the script VM infrastructure (`xmmword_7FF6CA1495C8` for stack) but is a distinct battle processing module. The state machine handles phases 0-6 (init, setup, main, etc.) and calls the main 334KB battle processing function.

**Updated FFNX_HOOK_MAPPING.md:**
- Battle Module section added with addresses and analysis
- Top 10 table updated with battle categorization for function #2

---

### Iteration 9 (2026-02-26 21:45 JST) - find-battle-functions

**Task:** Identify battle module functions

**Function Profiled:** `sub_7FF6C8207AF0` (334KB - function #2 from top 10)

**Analysis Results:**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C8207AF0` |
| Size | 333,912 bytes (334KB) |
| Callers | 5 (via wrappers) |
| Callees | 62 unique |
| GSA Calls | 1,652 |
| Handle Deref Calls | 1,650 (855 dword + 795 word) |

**Call Chain Analysis:**
```
??? (function pointer table)
  → sub_7FF6C8270DE0 (NO XREFS - battle state machine entry)
    → sub_7FF6C8281E60 → sub_7FF6C8207AF0
  → sub_7FF6C8271CE0 (NO XREFS - battle entry point)
    → sub_7FF6C8281E60 → sub_7FF6C8207AF0
  → sub_7FF6C82825B0 → sub_7FF6C8285080 → sub_7FF6C8207AF0
  → sub_7FF6C8289CF0/sub_7FF6C8289F80 → sub_7FF6C8AE0500 → sub_7FF6C8207AF0
```

**Top Callee - Battle Character Data Accessor (sub_7FF6C825A7E0):**
- Called 40 times from main battle function
- Uses constant 6892 (0x1AEC) - FF7 character data size
- Uses constant 12456372 (0xBE28D4) - character data offset
- Pattern: `6892 * character_index + 12456372` → character data access

**Battle State Machine (sub_7FF6C8270DE0) Analysis:**
- 3,826 bytes (0xEF2)
- **NO XREFS** - dispatched via function pointer
- Handles battle states 0-6 (via 0xBFCDFC address)
- Switch on comparison values: `0x429CBD`, `0x429C0C`, `0x429C29`, `0x429C61`
- Calls battle init (sub_7FF6C82729F0), setup (sub_7FF6C82763F0), and main loop

**Battle Memory Addresses Identified:**
| Address | Purpose |
|---------|---------|
| `0x9AE108` | Battle state (0=init, 1=started, 2=continue, 3=setup) |
| `0xBE28D4` | Character data base offset |
| `0xBFCDFC` | Battle phase (0-6) |
| `0xBF2DEC` | Battle status |
| `0xBF2A30` | Battle flag |
| `0xCC0828` | Battle flag |
| `0xBE1128` | Battle data pointer (12529584) |
| `0xC05F7C` | Screen width (512) |

**Battle Region Mapping:**
- `0x7FF6C820xxxx - 0x7FF6C82Axxxx` - Core battle module
- `0x7FF6C8BCxxxx` - Battle UI/State subsystem (function #5)
- `0x7FF6C8AE0500` - Battle helper region

**Key Discovery - VM Stack Integration:**
- Battle functions use `xmmword_7FF6CA1495C8` (VM Stack Pointer)
- Same VM infrastructure as field script functions
- Indicates battle scripts share VM with field module

**Categorization:** **BATTLE MODULE - Main Loop with State Machine**

The 334KB function `sub_7FF6C8207AF0` is the battle main loop. Entry point `sub_7FF6C8270DE0` is the battle state machine dispatcher (states 0-6). Character data is accessed using 6892-byte structure (confirmed FF7 character size). Uses VM stack infrastructure indicating integration with script VM.

**Updated FFNX_HOOK_MAPPING.md:**
- Added Battle Module section with function addresses
- Added battle memory address mapping
- Updated Top 10 table with battle categorization

---

### Iteration 11 (2026-02-26 20:25 JST) - find-menu-functions

**Task:** Identify menu module functions

**Investigation Approach:**
1. Searched for "menu" and "kernel" strings via IDA MCP - no direct matches (functions use `sub_XXXXXXXX` naming)
2. Traced xrefs from Japanese font loader (0x7FF6C9681D90)
3. Examined global_state_accessor callers
4. Analyzed text/dialogue function call chain

**Key Findings - Menu Architecture:**

**NOT a Separate Module:**
- Menu functionality is NOT in a distinct "menu module" region
- Menu scripts run through the Script VM infrastructure
- Text rendering uses native Japanese font support

**Japanese Font Loader (0x7FF6C9681D90):**
- Loads `jafont_1.tim` through `jafont_6.tim`
- Allocates 312-byte struct
- Called from: `sub_7FF6C96842D0` (initialization wrapper, 19 bytes)
- Wrapper has NO XREFS → function pointer dispatch

**Text/Dialogue Chain:**
```
sub_7FF6C8270DE0 (battle state machine, NO XREFS)
  → sub_7FF6C8281E60 (5 calls from battle entry points)
    → sub_7FF6C91BAEF0 (wrapper, 3 calls)
      → sub_7FF6C919F5F0 (110KB text/dialogue function)
```
- Text function is used by BATTLE module, not just field
- Same function handles dialogue rendering across modules

**kernel.bin/kernel2.bin Discovery:**
- NOT found as direct file path strings
- Likely embedded in ff7_ja/ff7_en resources
- Accessed via resource_allocator patterns (handle system)
- No CreateFileA xrefs to "kernel" (VEH dispatch bypasses)

**Menu State Access:**
- Savemap handle: `0xDBFD38` (accessed via global_state_accessor)
- Menu state variables stored in savemap at known offsets
- Script VM opcodes handle menu logic

**Menu Function Candidates:**
| Address | Size | Purpose |
|---------|------|---------|
| `sub_7FF6C9681D90` | ~2KB | Japanese font loader - menu text rendering |
| `sub_7FF6C919F5F0` | 110KB | Text/dialogue processing - used by field and battle |
| `sub_7FF6C9307DC0` | 56KB | Script VM field/text opcode handler - menu scripts |
| `sub_7FF6C96842D0` | 19 bytes | Font init wrapper (calls font loader) |

**Categorization:** Menu functionality is distributed across:
1. Script VM infrastructure (0x7FF6C930xxxx-0x7FF6C95Fxxxx) - menu scripts
2. Text rendering (0x7FF6C919xxxx) - dialogue/text display
3. Font system (0x7FF6C968xxxx) - Japanese font loading

**Recommendation:** Hook at Script VM level for menu modifications, or text rendering functions for font replacement. The kernel2_get_text equivalent is handled by resource_allocator calls to embedded resources.

**Updated FFNX_HOOK_MAPPING.md:**
- Added Menu Module section with architecture analysis
- Documented menu function candidates
- Explained kernel2.bin embedding in resources

---

### Iteration 12 (2026-02-26 20:31 JST) - find-save-functions

**Task:** Identify save/load functions

**Investigation Approach:**
1. Searched for save-related string patterns via xrefs
2. Traced xrefs to CreateFileA shim (0x7FF6C9683DE0)
3. Analyzed save data conversion function (0x7FF6C968B660)
4. Decompiled save directory function (0x7FF6C968B220)

**Key Findings - Save/Load System:**

**Save Directory Function (sub_7FF6C968B220):**
- Uses Steam API: `steam_api64_SteamInternal_ContextInit`
- Returns path to Steam user save directory
- Path format: `{Steam User Data Dir}/{Steam64 ID}/`
- Buffer: `byte_7FF6CA1A1C20` (260 bytes)

**Save Data Conversion Function (sub_7FF6C968B660):**
- **Source file:** `W:\proj\ff7\kitamura\Material\Game\Saves\SaveDataConvertLocation.cpp`
- Called from `shim_ReadFile` at `0x7FF6C9684D28`
- Trigger: Reading exactly 65,100 bytes (save file read)
- **Save format:**
  - 15 save slots
  - 4340 bytes per slot (0x10F4)
  - Total: 65,100 bytes (0xFE2C)
  - CRC16 checksum (polynomial 0x1021) at offset 0x0000
  - Character data at offsets 0x0064 (11 chars × 132 bytes)
  - Location data at offset 0x0B8C (field/world/battle)

**Path Routing in CreateFileA Shim:**
```c
if (strncmp(path, "save", 4) == 0) {
    // Route to Steam save directory
    save_dir = sub_7FF6C968B220(); // Steam user path
    full_path = combine(save_dir, path);
}
else if (strncmp(path, "ff7input.cfg", 12) == 0) {
    // Route to config directory
    config_dir = sub_7FF6C968B330();
    full_path = combine(config_dir, path);
}
else if (strstr(path, "APP.LOG")) {
    return -1; // BLOCKED — no logging
}
else {
    // Route to game data directory
    data_dir = unk_7FF6C968AE70();
    full_path = combine(data_dir, path);
}
```

**File Handle Table:**
| Property | Value |
|----------|-------|
| Base address | `unk_7FF6C983FA80` |
| Entry size | 212 bytes |
| First free slot | Index 6 |
| Max entries | ~20 (bounded by `byte_7FF6C9840BDC`) |

**Save Data Constants:**
- `0x1021` — CRC16 polynomial
- `11` — Number of characters (charId < 11 validation)
- `4340` — Save slot size
- `15` — Number of save slots
- `word_7FF6C8110000[11749900]` — Location name table base

**WriteFile Shim (0x7FF6C9685620):**
- Uses file handle table at `word_7FF6C8110000[...]`
- Buffer resolved via `global_state_accessor`
- Write tracking at `qword_7FF6CA19F488`
- Special handling for certain file handles (0x7FF6CA19F4E0 buffer fallback)

**FFNx Hook Points for Save/Load:**
| FFNx Target | 2026 Address | Notes |
|-------------|--------------|-------|
| `ff7_externals.save_file` | `shim_CreateFileA` | Route "save" prefix |
| `ff7_externals.load_file` | `shim_ReadFile` | 65100-byte trigger |
| Save conversion | `0x7FF6C968B660` | Direct data manipulation |
| Savemap access | `0xDBFD38` | Via global_state_accessor |

**Categorization:** **SAVE/LOAD MODULE — Steam Cloud Integrated**

The save system uses Steam Cloud for persistence. Save files are converted between FF7 format and Steam format on read/write. The 4340-byte slot size confirms FF7's original save structure. CRC16 checksum validates data integrity.

**Updated FFNX_HOOK_MAPPING.md:**
- Added Section 6: Save/Load Hooks
- Documented all save-related functions
- Added save data format and offsets
- Explained path routing and Steam integration