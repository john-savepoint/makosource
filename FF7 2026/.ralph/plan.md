# FF7 2026 Reverse Engineering - Ralph Loop Plan

## Overview

Continue reverse engineering the FFVII 2026 Steam Edition binary. Profile remaining functions, categorize game logic modules, and document findings for FFNx hook mapping.

**Reference:** `analysis/FFNX_HOOK_MAPPING.md`, `analysis/GFX_DRV_DECOMPILATION_COMPLETE.md`

**IDA Database:** FFVII.DMP loaded at base `0x7FF6C8110000`

---

## Task List

```json
[
{
  "category": "profiling",
  "id": "profile-3",
  "description": "Profile function #3: sub_7FF6C9571B50 (128KB)",
  "steps": [
    "Use IDA MCP to get function size and caller info",
    "Count calls to global_state_accessor and handle_deref_*",
    "Identify unique callees",
    "Categorize as field/battle/menu/world/other",
    "Update FFNX_HOOK_MAPPING.md Section 4 with findings"
  ],
  "passes": true,
  "result": "Script VM helper - part of FF7 scripting engine, uses virtual stack at xmmword globals, 1 caller (via function pointer), 9 unique callees including GSA"
},
{
  "category": "profiling",
  "id": "profile-4",
  "description": "Profile function #4: sub_7FF6C919F5F0 (110KB)",
  "steps": [
    "Use IDA MCP to get function size and caller info",
    "Count calls to global_state_accessor and handle_deref_*",
    "Identify unique callees",
    "Categorize as field/battle/menu/world/other",
    "Update FFNX_HOOK_MAPPING.md Section 4 with findings"
  ],
  "passes": true,
  "result": "Field module function - dialogue/text processing, 1 caller (sub_7FF6C91BAEF0 with 3 calls), 11 unique callees including GSA + handle_deref"
},
{
  "category": "profiling",
  "id": "profile-5",
  "description": "Profile function #5: sub_7FF6C8BC2B80 (75KB)",
  "steps": [
    "Use IDA MCP to get function size and caller info",
    "Count calls to global_state_accessor and handle_deref_*",
    "Identify unique callees",
    "Categorize as field/battle/menu/world/other",
    "Update FFNX_HOOK_MAPPING.md Section 4 with findings"
  ],
  "passes": true,
  "result": "Battle UI/State subsystem - 4 callers (1 via function pointer), 20 callees including GSA/handle_deref, 6 local helpers in 0x7FF6C8BCxxxx region, connected to battle dispatch via sub_7FF6C826B780"
},
{
  "category": "profiling",
  "id": "profile-6",
  "description": "Profile function #6: sub_7FF6C9331AA0 (61KB)",
  "steps": [
    "Use IDA MCP to get function size and caller info",
    "Count calls to global_state_accessor and handle_deref_*",
    "Identify unique callees",
    "Categorize as field/battle/menu/world/other",
    "Update FFNX_HOOK_MAPPING.md Section 4 with findings"
  ],
  "passes": true,
  "result": "Script VM opcode handler - 1 caller (sub_7FF6C934A4C0), 64 unique callees, entry points (sub_7FF6C917DD40, sub_7FF6C9180D60) have NO XREFS (function pointer dispatch), parent functions access VM globals (xmmword_7FF6CA1495C8/5B8), region 0x7FF6C930xxxx-0x7FF6C935xxxx is script VM opcode dispatch"
},
{
  "category": "profiling",
  "id": "profile-9",
  "description": "Profile function #9: sub_7FF6C95FB250 (51KB)",
  "steps": [
    "Use IDA MCP to get function size and caller info",
    "Count calls to global_state_accessor and handle_deref_*",
    "Identify unique callees",
    "Categorize as field/battle/menu/world/other",
    "Update FFNX_HOOK_MAPPING.md Section 4 with findings"
  ],
  "passes": true,
  "result": "Script VM high-frequency helper - 72 calls from dispatcher sub_7FF6C95A02C0 (60 calls) and wrappers, 7 callees (GSA, handle_deref, script pusher, return helper), entry point sub_7FF6C956B7D0 has NO XREFS (function pointer dispatch), region 0x7FF6C956xxxx-0x7FF6C95Fxxxx is script VM execution layer"
},
{
  "category": "profiling",
  "id": "profile-10",
  "description": "Profile function #10: sub_7FF6C95B6E50 (48KB)",
  "steps": [
    "Use IDA MCP to get function size and caller info",
    "Count calls to global_state_accessor and handle_deref_*",
    "Identify unique callees",
    "Categorize as field/battle/menu/world/other",
    "Update FFNX_HOOK_MAPPING.md Section 4 with findings"
  ],
  "passes": true,
  "result": "Script VM opcode handler - 1 caller (sub_7FF6C9566E60, NO XREFS via function pointer), uses VM stack (xmmword_7FF6CA1495C8), same entry point as function #3, region 0x7FF6C95Bxxxx is script VM execution layer"
},
{
  "category": "investigation",
  "id": "verify-execute-opcode",
  "description": "Verify candidate_execute_opcode is the field opcode dispatcher",
  "steps": [
    "Decompile first ~500 bytes of sub_7FF6C8D19A10",
    "Look for switch statement on opcode byte value",
    "Check for 256-entry dispatch table pattern",
    "Document findings in activity.md"
  ],
  "passes": true,
  "result": "NOT an opcode dispatcher - is a script VM state accessor (553KB, 2089 handle_deref calls, 1124 GSA calls, no indirect jumps, no switch patterns, table at 0x7FF6C980EAD0 is 1-bit lookup not function pointer table)"
},
{
  "category": "investigation",
  "id": "categorize-no-callers",
  "description": "Categorize the two no-callers functions",
  "steps": [
    "Profile sub_7FF6C9307DC0 (56KB) - may be module entry point",
    "Profile sub_7FF6C90D3CE0 (53KB) - opcode-like dispatcher candidate",
    "Determine if called from main game loop",
    "Update FFNX_HOOK_MAPPING.md with findings"
  ],
  "passes": true,
  "result": "Both are Script VM opcode handlers: sub_7FF6C9307DC0 (56KB, 48 callees) is FIELD/TEXT/DIALOGUE module (calls font functions in 0x7FF6C968xxxx), sub_7FF6C90D3CE0 (53KB, 9 callees) is a simpler focused opcode handler - both use VM stack (xmmword_7FF6CA1495C8), both have NO XREFS (function pointer dispatch), both confirmed as script VM infrastructure"
},
{
  "category": "investigation",
  "id": "find-battle-functions",
  "description": "Identify battle module functions",
  "steps": [
    "Search for battle-related string references",
    "Cross-reference from known battle callers",
    "Profile sub_7FF6C8207AF0 (334KB) - battle candidate",
    "Document in FFNX_HOOK_MAPPING.md Section 4"
  ],
  "passes": true,
  "result": "BATTLE MODULE IDENTIFIED: sub_7FF6C8207AF0 (334KB) is battle main loop with 62 callees, 1652 GSA calls, 1650 handle_deref calls. Entry via sub_7FF6C8270DE0 (battle state machine, NO XREFS = FP dispatch). Character data size: 6892 bytes (0x1AEC). Battle memory addresses: 0x9AE108 (state), 0xBE28D4 (char data), 0xBFCDFC (phase 0-6), 0xBF2DEC (status). Battle region: 0x7FF6C820xxxx - 0x7FF6C82Axxxx. Uses VM stack infrastructure."
},
{
  "category": "investigation",
  "id": "find-menu-functions",
  "description": "Identify menu module functions",
  "steps": [
    "Search for menu-related string references",
    "Look for kernel2.bin access patterns",
    "Document in FFNX_HOOK_MAPPING.md Section 4"
  ],
  "passes": true,
  "result": "Menu architecture discovered — NOT a separate module. Menu scripts run through Script VM (0x7FF6C930xxxx-0x7FF6C95Fxxxx). Text rendering via Japanese font loader (0x7FF6C9681D90). kernel.bin/kernel2.bin NOT found as strings — embedded in resources. Menu state in savemap (handle 0xDBFD38). Candidates: sub_7FF6C9307DC0 (56KB, field/text opcodes), sub_7FF6C919F5F0 (110KB, text/dialogue), sub_7FF6C9681D90 (font loader)."
},
{
  "category": "investigation",
  "id": "find-save-functions",
  "description": "Identify save/load functions",
  "steps": [
    "Search for 'SavedGame' or save file path strings",
    "Cross-reference CreateFileA shim callers",
    "Document in FFNX_HOOK_MAPPING.md"
  ],
  "passes": true,
  "result": "SAVE/LOAD SYSTEM MAPPED — shim_CreateFileA (0x7FF6C9683DE0) routes 'save' prefix to Steam save directory via sub_7FF6C968B220, shim_ReadFile (0x7FF6C9684C60) triggers save data conversion at sub_7FF6C968B660 for 65100-byte reads, save format is 15 slots × 4340 bytes with CRC16 checksum (0x1021), Steam Cloud integration via steam_api64, file handle table at unk_7FF6C983FA80 (212 bytes/entry), documented in FFNX_HOOK_MAPPING.md Section 6"
},
{
  "category": "documentation",
  "id": "create-handoff",
  "description": "Create session handoff document",
  "steps": [
    "Create .project/session_handoffs/SESSION_HANDOFF_2026-02-26-07_RALPH_LOOP.md",
    "Include all findings from this session",
    "List remaining work for next session"
  ],
  "passes": true,
  "result": "Handoff created at .project/session_handoffs/SESSION_HANDOFF_2026-02-26-07_RALPH_LOOP.md - all 12 tasks complete, save/load system mapped, FFNX_HOOK_MAPPING.md Section 6 added"
}
]
```

---

## Agent Instructions

1. **CRITICAL**: Stop work and exit when approaching 175,000 tokens (your context limit)
2. Read `activity.md` first to understand current state
3. Find next task with `"passes": false`
4. Complete all steps for that task
5. Update task to `"passes": true`
6. Log completion in `activity.md` with timestamp
7. Output `<promise>ITERATION_COMPLETE</promise>` when done with one task
8. Output `<promise>COMPLETE</promise>` only when ALL tasks pass

**Important:**
- Only modify the `passes` field in tasks
- Do not remove or rewrite tasks
- Update markdown files immediately after each discovery
- Each iteration does ONE task only, then exits

---

## Completion Criteria

All tasks marked with `"passes": true`

OR

User manually stops the loop

---

## Token Limit Protocol

When approaching 175,000 tokens:
1. Immediately update activity.md with current progress
2. Update plan.md with current task status
3. Output `<promise>ITERATION_COMPLETE</promise>`
4. The loop will restart with fresh context

---

## Files to Maintain

| File | Purpose |
|------|---------|
| `.ralph/plan.md` | This file - task tracking |
| `.ralph/activity.md` | Progress log per iteration |
| `analysis/FFNX_HOOK_MAPPING.md` | Main hook mapping document |
| `analysis/GFX_DRV_DECOMPILATION_COMPLETE.md` | Graphics decompilation reference |
| `.project/session_handoffs/SESSION_HANDOFF_*.md` | Session handoffs |