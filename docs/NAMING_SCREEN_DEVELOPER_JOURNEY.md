# Japanese Naming Screen - Developer Journey & Technical Reference

**Created:** 2025-12-22 15:15 JST (Monday)
**Last Modified:** 2025-12-22 15:15 JST (Monday)
**Version:** 1.0.0
**Author:** John Zealand-Doyle
**Session-IDs:**
- Initial Planning: `0681f78b-0382-45ee-898b-5a32b7ce32d5` (2025-12-12)
- Passive Injection: `e2ccd71a-...` (2025-12-13)
- Sidebar Navigation: `41570780-1a81-47b4-b39c-15c065fa0e7a` (2025-12-21)
- Cursor Glitch Fix: `f261594e-5490-45bf-9a96-915dff152055` (2025-12-22)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [The Challenge](#the-challenge)
3. [Evolution of Approaches](#evolution-of-approaches)
4. [Key Technical Discoveries](#key-technical-discoveries)
5. [Mistakes Made & Lessons Learned](#mistakes-made--lessons-learned)
6. [Final Implementation](#final-implementation)
7. [Memory Addresses Reference](#memory-addresses-reference)
8. [HEXT Patches Reference](#hext-patches-reference)
9. [Known Issues & Future Work](#known-issues--future-work)

---

## Executive Summary

The Japanese naming screen implementation required replacing the disabled English keyboard input with a 3-page Japanese character selector (Hiragana, Katakana, Eisuu). What initially seemed straightforward became a complex journey through vanilla game internals, memory patching, and timing-sensitive rendering issues.

**Final Working Solution:**
- FFNx hooks `keyboard_name_input` to handle Japanese character selection
- Japanese character tables are written to vanilla's grid memory at `0x921D70`
- Vanilla renders the characters; FFNx handles input and page switching
- HEXT patches extend the grid from 7 rows to 9 rows and fix sidebar behavior
- Sidebar navigation via D-pad required careful timing fixes to avoid cursor glitches

---

## The Challenge

### Original Problem

The Steam English version of FF7 disables the keyboard naming screen for gamepad compatibility. FFNx's existing code simply `noop`s the keyboard input function. For Japanese localization, we needed to:

1. Display a 3-page Japanese character grid (Hiragana, Katakana, Alphanumeric)
2. Allow D-pad navigation through 9×10 character grids (vs English's 7×10)
3. Implement L1/R1 page switching
4. Integrate with vanilla's name buffer and save system
5. Make sidebar navigation intuitive (D-pad RIGHT to enter, LEFT to exit)

### Why It Was Harder Than Expected

1. **Vanilla's render loop is tightly coupled** - We couldn't just inject characters; vanilla has complex state machines for cursor position, sidebar mode, and rendering
2. **Multiple code paths for the same memory** - The sidebar flag (`0x921ED4`) is written by multiple code paths depending on input
3. **Frame timing matters** - Changing state in the input phase doesn't guarantee correct rendering if vanilla caches values
4. **HEXT address documentation was sometimes wrong** - Some addresses were documented incorrectly, leading to crashes or corrupted behavior

---

## Evolution of Approaches

### Approach 1: Full FFNx Overlay (Abandoned)

**Concept:** FFNx renders everything - character grid, sidebar, cursor, name preview.

**Why it failed:**
- Duplicated vanilla's rendering, causing visual artifacts
- Fighting vanilla's state management was error-prone
- Name saving didn't work because vanilla expected its own buffer format

### Approach 2: Buffer Interception (Abandoned)

**Concept:** Let vanilla render, but intercept its name buffer and inject Japanese characters.

**Why it failed:**
- Vanilla's save logic ran AFTER our injection, overwriting our Japanese characters
- Multiple overwrite points made interception fragile
- Race conditions caused character corruption

### Approach 3: Passive Injection (Current - Working)

**Concept:** Write Japanese character tables directly to vanilla's grid memory. Let vanilla handle ALL rendering and input except page switching.

**Why it works:**
- Vanilla reads character data from `0x921D70` - we just change what's there
- Vanilla's cursor, sidebar, and save logic all work unchanged
- FFNx only handles: L1/R1 page switching, sidebar entry/exit logic
- Minimal intervention = minimal bugs

### Sidebar Navigation Evolution

The sidebar navigation went through several iterations:

1. **Vanilla default:** D-pad DOWN at right edge enters sidebar (unintuitive)
2. **First FFNx attempt:** NOP vanilla's sidebar writes, FFNx controls flag directly
3. **Problem discovered:** Cursor rendered at wrong position for 1 frame on entry/exit
4. **Root cause:** FFNx changed sidebar flag, but `naming_screen_update_cursor_y_patch()` had already run with old state
5. **Fix:** Call `naming_screen_update_cursor_y_patch()` immediately after changing sidebar flag
6. **New problem:** Pressing RIGHT at column 8 skipped column 9 entirely
7. **Root cause:** Vanilla moved cursor to 9, then FFNx immediately entered sidebar (same frame)
8. **Fix:** Only enter sidebar if cursor was ALREADY at column 9 last frame (`g_prev_grid_x == 9`)

---

## Key Technical Discoveries

### 1. Vanilla Grid Memory Layout

The character grid at `0x921D70` stores 90 bytes (9 rows × 10 columns). Each byte is a jafont index:
- `0x00-0xFF` maps to characters in the jafont texture
- `0xFF` = empty/terminator
- `0x00` = バ (ba) - a valid character, NOT empty!

### 2. Sidebar Flag Behavior

The sidebar flag at `0x921ED4`:
- `0` = cursor in character grid
- `1` = cursor in sidebar

Multiple vanilla code paths write to this:
- D-pad navigation code
- Start button handler
- Cancel button handler (problematic - snaps to sidebar unexpectedly)

### 3. Cursor Y Base Value Patching

Vanilla calculates cursor screen position using:
```
Y = cursor_row * row_height + base_offset
```

The base offset is hardcoded in the EXE. When switching between grid and sidebar mode, different base offsets are used. FFNx patches these at runtime via `naming_screen_update_cursor_y_patch()`.

### 4. HEXT Timing

HEXT patches are applied at game load. They modify the EXE in memory before any game code runs. This means:
- Can't use HEXT for runtime-conditional patches
- Must NOP code paths we want to disable, can't just change values conditionally
- FFNx's `memset_code()` can patch at runtime if needed

### 5. Edge Detection for Buttons

Single button presses must use edge detection to avoid repeated triggers:
```cpp
bool naming_screen_check_button_edge(bool current_pressed, bool* prev_pressed) {
    bool edge = current_pressed && !(*prev_pressed);
    *prev_pressed = current_pressed;
    return edge;
}
```

---

## Mistakes Made & Lessons Learned

### Mistake 1: Wrong HEXT Addresses for Y-Spacing

**What happened:** Documented IMUL addresses for Y-spacing patches were wrong. Patches at `718EDD` and `7191F2` corrupted unrelated code.

**Symptom:** The cursor showed a ゼ character instead of the hand sprite, and general instability.

**Lesson:** Always verify HEXT addresses by examining the actual bytes in the EXE. Use a hex editor or Python script to confirm the instruction you're patching.

### Mistake 2: Patching the Wrong Underscore Limit

**What happened:** Added patch `71927A = 06` thinking it was unrelated, but it changed the underscore display count from 9 to 6.

**Symptom:** Only 6 underscores in the name input buffer instead of 9.

**Lesson:** Document EVERY HEXT patch with its purpose. When something breaks, check recent HEXT changes first.

### Mistake 3: NOPing Code That Never Runs

**What happened:** NOPed vanilla's sidebar entry/exit code at addresses that weren't actually executed (FFNx replaces `keyboard_name_input` entirely).

**Why it worked anyway:** The NOPs were in dead code paths, so they didn't break anything - but they also didn't help.

**Lesson:** Understand the call chain. If FFNx replaces a function, vanilla's internal code for that function may never run.

### Mistake 4: Not Tracking Previous Frame State

**What happened:** Sidebar entry triggered when cursor arrived at column 9, skipping the column entirely.

**Root cause:** Check was `cursor_x == 9 && dpad_right_pressed`, but vanilla had just moved cursor from 8 to 9 in the same frame.

**Fix:** Check `cursor_x == 9 && g_prev_grid_x == 9` to ensure cursor was already at 9 last frame.

**Lesson:** Frame timing is critical. Always consider when values change relative to when you read them.

### Mistake 5: Cursor Y Patch Timing

**What happened:** Cursor rendered at wrong position for 1 frame when entering/exiting sidebar.

**Root cause:** `naming_screen_update_cursor_y_patch()` ran at start of `naming_screen_process_input()`, before sidebar flag was changed.

**Fix:** Call `naming_screen_update_cursor_y_patch()` again immediately after changing sidebar flag.

**Lesson:** State changes must be followed by any dependent updates before the frame ends.

---

## Final Implementation

### FFNx Components

**File:** `src/ff7/naming_screen.cpp`

Key functions:
- `naming_screen_init()` - Initialize state, write Japanese tables to grid memory
- `naming_screen_process_input()` - Handle L1/R1 page switching, sidebar navigation
- `naming_screen_write_table_to_grid()` - Copy current page's character table to `0x921D70`
- `naming_screen_update_cursor_y_patch()` - Patch cursor Y base values for grid/sidebar mode
- `ff7_naming_keyboard_input_jp()` - Main hook replacing `keyboard_name_input`

### HEXT Components

**File:** `hext/ff7/ja/japanese_menu.txt`

Key patches:
- Row limit extension (7→9 rows)
- Y-spacing reduction (34px→26px to fit 9 rows)
- Cancel button fix (prevent sidebar snap)
- Start button handler NOP (FFNx handles Start)
- Sidebar entry/exit NOPs (FFNx handles D-pad sidebar navigation)

### Data Flow

```
User Input (D-pad/L1/R1)
    ↓
ff7_naming_keyboard_input_jp()
    ↓
naming_screen_process_input()
    ├── Page switch? → naming_screen_write_table_to_grid()
    ├── Sidebar entry/exit? → Update flag + naming_screen_update_cursor_y_patch()
    └── Character selection? → Write to vanilla buffer at 0xDD45F0
    ↓
Vanilla Render Loop
    ├── Reads grid from 0x921D70
    ├── Reads cursor position from 0xDD4538/0xDD453C
    ├── Reads sidebar flag from 0x921ED4
    └── Draws everything
```

---

## Memory Addresses Reference

### Character Grid & Selection

| Address | Size | Description |
|---------|------|-------------|
| `0x921D70` | 90 bytes | Character grid data (9×10, jafont indices) |
| `0xDD45F0` | 12 bytes | Name buffer (9 chars + terminator) |
| `0xDD4538` | 4 bytes | Grid cursor X position (0-9) |
| `0xDD453C` | 4 bytes | Grid cursor Y position (0-8) |
| `0xDD46F0` | 4 bytes | Name buffer cursor position (0-8) |
| `0xDD46F4` | 4 bytes | Page selector (0=Hiragana, 1=Katakana, 2=Eisuu) |

### Sidebar State

| Address | Size | Description |
|---------|------|-------------|
| `0x921ED4` | 4 bytes | Sidebar flag (0=grid, 1=sidebar) |
| `0xDD4574` | 4 bytes | Sidebar cursor Y position (0-6) |
| `0xDD457C` | 4 bytes | Sidebar item count limit |

### Cursor Rendering

| Address | Description |
|---------|-------------|
| `0x718EDB` | IMUL for cursor Y in grid mode |
| `0x7183C7` | IMUL for cursor Y (secondary) |
| `0x7185F0` | IMUL for grid rendering Y |

---

## HEXT Patches Reference

### Grid Extension (7→9 Rows)

```hext
# Row render limit: 7 → 9
7191D0 = 09

# Y cursor limit patches (6 → 8 for rows 0-8)
718E9D = 08
718EA6 = 08
719560 = 08
719569 = 08

# Y spacing: 34px → 26px (0x22 → 0x1A)
718EDD = 1A
7191F2 = 1A
```

### Sidebar Fixes

```hext
# Cancel button - skip sidebar snap (JMP over handler)
71915B = EB

# Start button handler NOP (56 bytes - FFNx handles Start)
71980B = 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90

# Sidebar entry/exit NOPs (FFNx handles D-pad sidebar navigation)
718F46 = 90 90 90 90 90 90 90 90 90 90
71900E = 90 90 90 90 90 90 90 90 90 90
```

### Sidebar Item Count

```hext
# Sidebar items: 4 → 7 (ひらがな, カタカナ, えいすう, スペース, さくじょ, けってい, デフォルト)
718A28 = 07
```

---

## Known Issues & Future Work

### Current Limitations

1. **No visual page indicator highlight** - The sidebar shows all 7 items but doesn't visually highlight which page is currently selected (Hiragana/Katakana/Eisuu)

2. **Sidebar cursor Y offset** - When entering sidebar, cursor starts at correct position but the Y base patch system is complex and could be simplified

3. **No wrap-around navigation** - Cursor doesn't wrap from column 9 to column 0 (or vice versa) - user must use sidebar to navigate

### Future Improvements

1. **Page indicator highlighting** - Use different text colors (cyan for selected, gray for others) on sidebar page labels

2. **Clean up dead code** - Remove commented-out attempts and unused functions from `naming_screen.cpp`

3. **Simplify cursor Y patching** - Consider pre-calculating all cursor positions in FFNx instead of runtime memory patching

4. **Default names per character** - Load Cloud's default name as クラウド, etc. based on character index

---

## Session Timeline

| Date | Session | Key Accomplishment |
|------|---------|-------------------|
| 2025-12-12 | Planning | Created implementation plan, analyzed vanilla code |
| 2025-12-13 | Passive Injection | Discovered injection approach, got basic grid working |
| 2025-12-15 | Grid Rendering | 9-row grid rendering with HEXT patches |
| 2025-12-17 | Vanilla Sidebar | Let vanilla handle sidebar, simplified FFNx role |
| 2025-12-19 | Cancel Fix | Fixed Cancel button snapping to sidebar |
| 2025-12-21 | Start Button | NOP'd vanilla Start handler, FFNx handles it |
| 2025-12-21 | Sidebar Navigation | Implemented D-pad RIGHT/LEFT for sidebar entry/exit |
| 2025-12-22 | Glitch Fixes | Fixed cursor rendering glitches, column 9 skip issue |

---

## Acknowledgments

This implementation was developed through iterative collaboration between John Zealand-Doyle and Claude (Anthropic), using Claude Code for code generation, debugging, and documentation. The complexity of FF7's internal state machines required extensive trial-and-error and careful analysis of vanilla behavior.

Special thanks to the FFNx team for their existing Japanese text rendering infrastructure, and the FF7 modding community for reverse engineering documentation.
