# Session Summary: Jump Table Reordering & Cursor Navigation Investigation

**Date**: 2026-01-16 15:04 JST (Thursday)
**Session ID**: 68f0456e-da0e-4308-b5b6-bd4b9953d22e
**Previous Sessions**:
- e11e5778-b1bf-40a0-a2f3-4a3927eb2451 (Session 29 - Vanilla Sidebar Investigation)
- See SESSION_HANDOFF_2025-12-17-29_VANILLA_SIDEBAR_INVESTIGATION.md

---

## Executive Summary

This session focused on fixing the naming screen sidebar action handling after discovering that the jump table mapping (which determines what code runs when you select a sidebar item) was broken. We successfully reordered the jump table to handle 7 items instead of 4, but discovered a separate cursor navigation limit that still restricts movement to only 4 positions.

### Current State

**What Works**:
- ✅ Sidebar renders 7 items (ひらがな/カタカナ/えいすう/スペース/さくじょ/けってい/デフォルト)
- ✅ Japanese character grid renders (all 9 rows)
- ✅ Page switching via L1/R1
- ✅ Jump table correctly routes actions:
  - Positions 0-2: NOP (do nothing - page labels)
  - Position 3: Add space to name (スペース)
  - Positions 4-6: Delete/Confirm/Default (verified via manual cursor setting)
- ✅ Both switch statements now use the same reordered jump table

**What Doesn't Work**:
- ❌ Cursor navigation limited to positions 0-3 (can't reach 4-6 via D-pad)
- ❌ Bottom sidebar items (positions 4-6) run off screen (Y positioning issue)

---

## Problem Discovery: Broken Jump Table Mapping

### The Core Issue

When we added 3 new labels (ひらがな, カタカナ, えいすう) at the **top** of the sidebar, the original 4 items (Space, Delete, Select, Default) shifted **down** by 3 positions:

**Before (4 items)**:
```
Position 0: Space   → Jump table entry 0
Position 1: Delete  → Jump table entry 1
Position 2: Select  → Jump table entry 2
Position 3: Default → Jump table entry 3
```

**After adding labels (7 items)**:
```
Position 0: ひらがな  → Jump table entry 0 (WRONG - points to Space handler!)
Position 1: カタカナ  → Jump table entry 1 (WRONG - points to Delete handler!)
Position 2: えいすう  → Jump table entry 2 (WRONG - points to Select handler!)
Position 3: スペース  → Jump table entry 3 (WRONG - points to Default handler!)
Position 4: さくじょ  → Entry 4 doesn't exist!
Position 5: けってい  → Entry 5 doesn't exist!
Position 6: デフォルト → Entry 6 doesn't exist!
```

Selecting position 0 (ひらがな) would execute the **Space handler** instead of doing nothing.
Selecting position 3 (スペース/Space) would execute the **Default handler** instead of adding a space.

---

## Understanding Jump Tables

### What is a Jump Table?

A **jump table** is a list of memory addresses stored in the executable. When the game needs to handle a sidebar action, it:

1. Reads the cursor position (0-6)
2. Uses that as an index into the jump table
3. Jumps to the code address stored at that table entry

**Original Jump Table** (at VA 0x719B61, file offset 0x318F61):
```
Entry 0: 0x71905D → Space handler (PUSH 0; CALL write_char)
Entry 1: 0x71906C → Delete handler (CALL delete_last_char)
Entry 2: 0x719076 → Select/Confirm handler (exit naming screen)
Entry 3: 0x719147 → Default handler (reset to default name)
Entry 4-7: [Used by second switch statement]
```

### Assembly Context

When the game processes a sidebar action, the code looks like this:

```assembly
; At VA 0x719040
MOV EAX, [EDX+0xDD453C]    ; Load sidebar cursor Y (0-3)
MOV [EBP-18], EAX          ; Store in local variable
CMP [EBP-18], 3            ; Compare cursor with max (3)
JA  +0xF9                  ; If > 3, skip switch (jump to 0x71914C)
MOV ECX, [EBP-18]          ; Load cursor value into ECX
JMP [ECX*4 + 0x719B61]     ; Jump to table[cursor]
```

The `JMP [ECX*4 + 0x719B61]` instruction:
- Multiplies cursor (0-3) by 4 (each entry is 4 bytes)
- Adds base address 0x719B61
- Jumps to the address **stored** at that location

Example:
- Cursor = 0: Jump to address stored at 0x719B61 = 0x71905D (Space handler)
- Cursor = 1: Jump to address stored at 0x719B65 = 0x71906C (Delete handler)
- Cursor = 2: Jump to address stored at 0x719B69 = 0x719076 (Select handler)
- Cursor = 3: Jump to address stored at 0x719B6D = 0x719147 (Default handler)

---

## Investigation Process

### 1. Locating the Jump Tables

Used `xxd` to examine the original jump table at file offset 0x318F61:

```
00318f61: 5d90 7100 6c90 7100 7690 7100 4791 7100  ].q.l.q.v.q.G.q.
00318f71: 1e97 7100 2d97 7100 3797 7100 0698 7100  ..q.-.q.7.q...q.
```

Decoded (little-endian):
- `5d 90 71 00` = 0x0071905D (Space handler)
- `6c 90 71 00` = 0x0071906C (Delete handler)
- `76 90 71 00` = 0x00719076 (Select handler)
- `47 91 71 00` = 0x00719147 (Default handler)
- Entries 4-7 at 0x719B71+: Second switch handlers

### 2. Finding the Switch Bounds Checks

Located two CMP instructions that check if cursor index is valid:

**First switch at VA 0x719049**:
```assembly
; File offset 0x318449
83 7D E8 03        ; CMP [EBP-18], 3
0F 87 F9 00 00 00  ; JA +0xF9 (jump if > 3)
```

**Second switch at VA 0x71970A**:
```assembly
; File offset 0x318B0A
83 7D DC 03        ; CMP [EBP-24], 3
0F 87 F7 00 00 00  ; JA +0xF7 (jump if > 3)
```

These check if cursor > 3 and skip the switch if true (since old sidebar only had 4 items).

### 3. Discovering the Second Switch Statement

Found that the naming screen has **TWO** switch statements using the same jump table:

**Switch 1** (at VA 0x719055):
```assembly
JMP [ECX*4 + 0x719B61]  ; Base: 0x719B61, uses entries 0-3
```

**Switch 2** (at VA 0x719718):
```assembly
JMP [EAX*4 + 0x719B71]  ; Base: 0x719B71, uses entries 4-7
```

The second switch base (0x719B71) points **10 bytes into** the first table, effectively using entries 4-7 as its own entries 0-3.

### 4. Verifying Handler Function Equivalence

Analyzed the CALL targets in both switches to confirm they use the same functions:

**Switch 1 Space handler** (0x71905D):
```assembly
6A 00              ; PUSH 0
E8 A0 FB FF FF     ; CALL 0x718C04
```

**Switch 2 Space handler** (0x71971E):
```assembly
6A 00              ; PUSH 0
E8 DF F4 FF FF     ; CALL 0x718C04  ; Same function!
```

Both switches call the **same underlying functions**, just from different code locations (hence different relative CALL offsets). This means we can share one jump table.

### 5. Finding the NOP Target

The old switch bounds check jumps to 0x71914C when cursor > 3. Examined this location:

```assembly
; VA 0x71914C (file 0x31854C)
68 00 08 01 00     ; PUSH 0x10800
E8 9B C2 FD FF     ; CALL xxx
```

This is the **post-switch code** that runs after any action handler completes. Perfect for a "do nothing" target for positions 0-2 (page labels).

---

## Solution: Jump Table Reordering

### Patches Applied

#### 1. Fixed Switch Bounds Checks

**WRONG patch removed**:
```
718C4C = 06  ; This was patching random memory!
```

**CORRECT patches**:
```hext
# First switch bounds check
# VA 0x71904C (file 0x31844C): Change CMP [EBP-18], 3 → 6
71904C = 06

# Second switch bounds check
# VA 0x71930D (file 0x318B0D): Change CMP [EBP-24], 3 → 6
71930D = 06
```

#### 2. Reordered Jump Table (8 entries at 0x719B61)

```hext
# Entry 0: ひらがな → NOP (0x71914C)
719B61 = 4C 91 71 00

# Entry 1: カタカナ → NOP (0x71914C)
719B65 = 4C 91 71 00

# Entry 2: えいすう → NOP (0x71914C)
719B69 = 4C 91 71 00

# Entry 3: スペース → Space handler (0x71905D)
719B6D = 5D 90 71 00

# Entry 4: さくじょ → Delete handler (0x71906C)
719B71 = 6C 90 71 00

# Entry 5: けってい → Select handler (0x719076)
719B75 = 76 90 71 00

# Entry 6: デフォルト → Default handler (0x719147)
719B79 = 47 91 71 00

# Entry 7: unused → NOP (0x71914C)
719B7D = 4C 91 71 00
```

#### 3. Unified Both Switches

Changed switch 2's base address to point to the same table as switch 1:

```hext
# Switch 2 base address fix
# VA 0x71971A (file 0x318B1A): Change 0x719B71 → 0x719B61
71971A = 61
```

Now both switches use entries 0-7 from 0x719B61.

### Memory Layout After Patches

```
                    ┌─────────────────────────────────────┐
Jump Table          │ VA 0x719B61 (file 0x318F61)         │
(32 bytes)          ├─────────────────────────────────────┤
                    │ Entry 0: 4C 91 71 00 (0x71914C NOP) │ ← Switch 1 & 2 base
                    │ Entry 1: 4C 91 71 00 (0x71914C NOP) │
                    │ Entry 2: 4C 91 71 00 (0x71914C NOP) │
                    │ Entry 3: 5D 90 71 00 (Space)        │
                    │ Entry 4: 6C 90 71 00 (Delete)       │ ← Old switch 2 base (0x719B71)
                    │ Entry 5: 76 90 71 00 (Select)       │
                    │ Entry 6: 47 91 71 00 (Default)      │
                    │ Entry 7: 4C 91 71 00 (NOP)          │
                    └─────────────────────────────────────┘
                    ┌─────────────────────────────────────┐
Next Function       │ VA 0x719B81: 55 8B EC 83 3D...      │ ← Can't extend table!
                    └─────────────────────────────────────┘
```

---

## Remaining Issue: Cursor Navigation Limit

### Problem

After applying all patches, testing revealed:
- ✅ Selecting positions 0-2 does nothing (NOP works)
- ✅ Selecting position 3 adds a space (Space handler works)
- ❌ **Cursor cannot navigate past position 3 via D-pad**
- ✅ Manually setting cursor to positions 4-6 via Cheat Engine confirms those positions exist (items render off-screen)

### Conclusion

There's a **separate** cursor navigation limit enforced somewhere in the D-pad input handling code. The jump table and switch bounds are now correct, but the cursor increment/wrap logic still clamps to 4 positions.

### Investigation Attempts

Searched for the cursor limit logic using multiple approaches:

1. **CMP with immediate 3 or 4**:
   ```python
   # Searched for: CMP EAX/ECX/EDX, 3 or 4
   # Result: No matches in input handling region
   ```

2. **CMP local variable with 4**:
   ```python
   # Searched for: CMP [EBP-xx], 4
   # Result: Only found rendering loop checks (already patched)
   ```

3. **INC + CMP pattern**:
   ```python
   # Pattern: INC EAX; CMP EAX, 3; conditional
   # Result: No matches
   ```

4. **Cursor write patterns**:
   ```python
   # Searched for: MOV [EDX+0xDD453C], EAX
   # Result: Only found initialization code (sets cursor to 2)
   ```

The cursor limit is enforced through a mechanism we haven't identified yet - possibly:
- Reading item count from memory
- Modulo 4 arithmetic
- Indirect comparison via function call
- Table size calculation

---

## Next Steps

### Immediate Action Required

**Use Cheat Engine to find cursor wrap logic**:

1. Add address `0xDD4574` to Cheat Engine (sidebar cursor Y)
2. Click "Find out what writes to this address"
3. Navigate to position 3 in sidebar
4. Press D-pad Down
5. Check the instruction list - one will show the cursor wrap from 3→0
6. Provide the VA/file offset of that instruction

Expected pattern:
```assembly
; Hypothetical cursor increment logic
MOV EAX, [cursor]     ; Read current cursor (3)
INC EAX               ; Increment (4)
CMP EAX, 4            ; Compare with limit <-- THIS is what we need to find
JGE wrap              ; If >= 4, wrap to 0
MOV [cursor], EAX     ; Write new value
JMP done
wrap:
XOR EAX, EAX          ; Set cursor to 0
MOV [cursor], EAX
done:
...
```

Once we find the comparison, we patch the `4` to `7`.

### Additional Fixes Needed

1. **Sidebar Y positioning**: All 7 items need to fit on screen
   - Currently using Y spacing of 26 pixels (0x1A)
   - May need to reduce further or adjust base Y position

2. **FFNx page indicator**: Disable if vanilla sidebar works correctly
   - Currently using FFNx overlay for page switching
   - Should be redundant once sidebar labels are functional

---

## Technical Details

### Memory Addresses Reference

| Component | Virtual Address | File Offset | Description |
|-----------|----------------|-------------|-------------|
| Sidebar cursor (grid mode) | 0xDD453C | - | Y position when sidebar_flag=0 |
| Sidebar cursor (sidebar mode) | 0xDD4574 | - | Y position when sidebar_flag=1 (0x38 offset) |
| Sidebar flag | 0x921ED4 | - | 0=grid mode, 1=sidebar mode |
| First switch | 0x719055 | 0x318455 | JMP [ECX*4 + 0x719B61] |
| Second switch | 0x719718 | 0x318B18 | JMP [EAX*4 + 0x719B71] → 0x719B61 |
| Jump table | 0x719B61 | 0x318F61 | 8 entries × 4 bytes = 32 bytes |
| NOP target | 0x71914C | 0x31854C | Post-switch code (safe do-nothing) |
| Space handler | 0x71905D | 0x31845D | PUSH 0; CALL write_char |
| Delete handler | 0x71906C | 0x31846C | CALL delete_char |
| Select handler | 0x719076 | 0x318476 | Exit naming screen |
| Default handler | 0x719147 | 0x318547 | Reset to default name |

### HEXT Patch Summary

All patches in `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/ja/japanese_menu.txt`:

```hext
# Switch bounds (allow 7 positions)
71904C = 06  # First switch: CMP [EBP-18], 3 → 6
71930D = 06  # Second switch: CMP [EBP-24], 3 → 6

# Rendering loops (render 7 items)
719227 = 07  # First loop: CMP [EBP-F0], 4 → 7
7198E1 = 07  # Second loop: CMP [EBP-F0], 4 → 7

# Base address adjustments
719237 = 30  # First loop: LEA base 0x921D48 → 0x921D30
7198F1 = 30  # Second loop: LEA base 0x921D48 → 0x921D30

# Jump table reordering (32 bytes)
719B61 = 4C 91 71 00  # Entry 0: NOP
719B65 = 4C 91 71 00  # Entry 1: NOP
719B69 = 4C 91 71 00  # Entry 2: NOP
719B6D = 5D 90 71 00  # Entry 3: Space
719B71 = 6C 90 71 00  # Entry 4: Delete
719B75 = 76 90 71 00  # Entry 5: Select
719B79 = 47 91 71 00  # Entry 6: Default
719B7D = 4C 91 71 00  # Entry 7: NOP (unused)

# Switch 2 base unification
71971A = 61  # Change base 0x719B71 → 0x719B61
```

---

## Key Learnings

### 1. Multiple Switch Statements Can Share Jump Tables

The second switch originally used entries 4-7 of the table by pointing its base address 16 bytes into the table. By changing its base to match switch 1, both switches now use entries 0-7, saving space and simplifying the design.

### 2. Handler Function Equivalence

Even though switch 1 and 2 have different handler addresses, they **call the same functions**:
- Switch 1 Space (0x71905D): `CALL 0x718C04`
- Switch 2 Space (0x71971E): `CALL 0x718C04`

The different handler addresses are just at different code locations with identical logic. This allowed us to merge them.

### 3. Jump Table Size Constraints

The jump table at 0x719B61 is **exactly 32 bytes** (8 entries × 4 bytes), followed immediately by a function at 0x719B81. We cannot extend beyond 8 entries without overwriting code.

This constraint required careful planning:
- Entries 0-2: All point to the same NOP target (saves space)
- Entries 3-6: The 4 action handlers
- Entry 7: Reserved/unused
- Total: 8 entries (fits perfectly)

### 4. Switch Bounds vs Cursor Navigation

Two separate systems:
1. **Switch bounds** (CMP [EBP-18], 3): Validates that the cursor value passed to the switch is within the jump table range
2. **Cursor navigation** (still unknown): Prevents the cursor from incrementing past position 3 when pressing D-pad

Fixing switch bounds alone is not enough - both systems must allow 7 positions.

---

## Session Context Files Read

1. `/home/johnzealanddoyle/projects/tools/.project/SceneSessionContextDirectory.md` (496 lines)
2. `/home/johnzealanddoyle/projects/tools/.project/SESSION_CONTEXT_19-28_NAMING_SCREEN.md` (1168 lines)
3. `/home/johnzealanddoyle/projects/tools/.project/session_handoffs/SESSION_HANDOFF_2025-12-17-29_VANILLA_SIDEBAR_INVESTIGATION.md` (561 lines)
4. `/home/johnzealanddoyle/projects/tools/.project/naming_screen_tables.txt` (362 lines)
5. `/home/johnzealanddoyle/projects/tools/.project/session_handoffs/SESSION_HANDOFF_2025-12-17-28_NAMING_SCREEN_VANILLA_RENDERING.md` (397 lines)

---

## Files Modified

1. `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/ja/japanese_menu.txt`
   - Fixed incorrect switch bounds patch (718C4C → 71904C)
   - Added jump table reordering (8 entries at 719B61-719B7D)
   - Added switch 2 base address unification (71971A = 61)
   - Total additions: ~80 lines of patches + comments

---

## Glossary

**Jump Table**: A data structure containing addresses of code handlers, indexed by a variable (cursor position). The CPU uses `JMP [index*size + base]` to execute the handler for a given index.

**Switch Statement**: A code pattern that uses a jump table to execute different code paths based on a variable's value. Similar to `switch(cursor) { case 0: ... case 1: ... }` in C.

**NOP (No Operation)**: Code that does nothing and simply continues execution. Used here to make page labels (positions 0-2) non-interactive.

**ModR/M byte**: The byte after an opcode that specifies addressing mode and registers. Example: In `83 7D E8 03`, the `7D` is the ModR/M byte indicating `[EBP-0x18]`.

**Little-endian**: Byte order where the least significant byte comes first. Example: `5D 90 71 00` represents 0x0071905D.

**VA (Virtual Address)**: Memory address as seen by the running program. Example: 0x71905D.

**File Offset**: Position in the EXE file on disk. Formula: `VA - 0x401000 + 0x400`. Example: VA 0x71905D → file 0x31845D.

**EBP**: Base Pointer register, used to access local variables and function parameters. `[EBP-18]` means "local variable at offset -0x18 from base pointer".

**HEXT**: Text-based patch format used by FFNx. Format: `ADDRESS = BYTES`. Example: `71904C = 06`.

---

**End of Session Summary**
