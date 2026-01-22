# Session Summary: Sidebar Navigation & Cursor Rendering Investigation

**Date:** 2026-01-16 14:03 JST (Friday)
**Session ID:** 5fdb9279-3929-4d55-83ca-6cd64371b1c5
**Project:** FF7 Japanese Naming Screen (FFNx PR #737)

---

## Context Documents Reviewed

This session built upon extensive prior work documented in:
- `SESSION_HANDOFF_2025-12-21-36_SIDEBAR_NAVIGATION_INVESTIGATION.md`
- `SESSION_HANDOFF_2025-12-21-35_CANCEL_START_BUTTON_FIX.md`
- `SESSION_CONTEXT_29-34_NAMING_SCREEN.md`
- `SESSION_CONTEXT_19-28_NAMING_SCREEN.md`
- `SceneSessionContextDirectory.md`

### Prior Achievements
- ✅ Cancel button fixed via HEXT NOP at `71915B = EB`
- ✅ Start button fixed via FFNx handler + HEXT NOP at `71980B`
- ✅ Sidebar navigation investigation complete with 4 HEXT patches identified

---

## Initial Task

Apply sidebar navigation improvements for Japanese naming screen to enable:
- **D-pad RIGHT** when X=9 (rightmost column) → Enter sidebar
- **D-pad LEFT** in sidebar → Exit to grid

However, the HEXT patches identified in session 36 were deemed inadequate. A new approach was adopted based on external AI consultation.

---

## New Methodology: External AI Consultation

### Philosophy Shift

Instead of trial-and-error HEXT patching, we adopted a research-first approach:
1. **Ask external AI** (with full FFNx codebase access) for architectural guidance
2. **Use Cheat Engine** to find breakpoints and verify addresses
3. **Implement in FFNx** following best practices from the codebase

This approach proved significantly more effective than blind HEXT patching.

---

## Key Technical Insights from External AI

### 1. Why Grid Characters Flickered (Previous Issue)

**Problem:** Race condition between vanilla and FFNx drawing code.

**Explanation:**
- Calling `g_original_menu_sub_718DBE()` still writes English grid data
- Our FFNx code writes Japanese data immediately after
- Renderer reads data **asynchronously**, causing random English/Japanese flicker

**Solution:**
- Don't call original function, or NOP out vanilla writes to `0x00921D70`

---

### 2. The "Fighting vs Replacing" Principle

**Core Concept:**
> A hook is just a detour, not a deletion. If you call the original function, original behavior still happens.

**Application to Sidebar Navigation:**
- HEXT patches that change button masks (`PUSH 0x2000` → `PUSH 0x8000`) are **fighting** vanilla logic
- Better approach: **Silence vanilla entirely** (NOP writes to `sidebar_flag`) and implement in FFNx

---

### 3. Execution Point Matters for Rendering

**Problem:** Drawing at wrong execution point causes visual glitches.

**Key Locations:**
- **Input Hook** (`ff7_naming_keyboard_input_jp`): Called during input processing, may skip frames
- **Common Flip** (`common_flip`): Runs at **end** of frame (post-render) - **too late for drawing**
- **Naming Screen Draw** (`naming_screen_draw`): Runs **inside** the game's render loop - **correct place**

**Lesson:** Drawing in `common_flip` fails because the render scene is already closed.

---

## Implementation: Sidebar Navigation

### Step 1: Find Vanilla Write Addresses (Cheat Engine)

**Addresses Found:**
- **Enter sidebar:** `0x718F46` - `mov [921ED4], 1` (10 bytes)
- **Exit sidebar:** `0x71900E` - `mov [921ED4], 0` (10 bytes)

**HEXT Patches Applied:**
```hext
# NOP vanilla sidebar ENTRY (grid -> sidebar)
718F46 = 90 90 90 90 90 90 90 90 90 90

# NOP vanilla sidebar EXIT (sidebar -> grid)
71900E = 90 90 90 90 90 90 90 90 90 90
```

### Step 2: Implement in FFNx

**File:** `src/ff7/naming_screen.cpp`

**Added State Tracking:**
```cpp
bool dpad_right_pressed;  // Track D-pad RIGHT for sidebar entry edge detection
bool dpad_left_pressed;   // Track D-pad LEFT for sidebar exit edge detection
```

**Sidebar Entry Logic (lines 834-854):**
```cpp
// Handle ENTRY: Grid -> Sidebar (D-pad RIGHT when at rightmost column)
if (current_sidebar == 0) {
    if (naming_screen_check_button_edge(pad->dpad_right != 0, &g_naming_state.dpad_right_pressed)) {
        if (cursor_x == 9) {
            // ENTER SIDEBAR
            *VANILLA_IN_SIDEBAR_FLAG = 1;
            *VANILLA_SIDEBAR_CURSOR_Y = 0;  // Start at top (ひらがな)
            ffnx_info("naming_screen: D-pad RIGHT at X=9 - entering sidebar at position 0\n");
        }
    }
}
```

**Sidebar Exit Logic (lines 847-854):**
```cpp
// Handle EXIT: Sidebar -> Grid (D-pad LEFT)
else {
    if (naming_screen_check_button_edge(pad->dpad_left != 0, &g_naming_state.dpad_left_pressed)) {
        // EXIT SIDEBAR
        *VANILLA_IN_SIDEBAR_FLAG = 0;
        *VANILLA_GRID_CURSOR_X = 9;  // Return to rightmost column
        ffnx_info("naming_screen: D-pad LEFT in sidebar - exiting to grid at X=9\n");
    }
}
```

**Result:** ✅ Sidebar entry/exit works correctly via D-pad RIGHT/LEFT.

---

## Implementation: Cursor Rendering (Failed Attempts)

### Attempt 1: NOP Vanilla Cursor Draw + Call 0x6EB3B8 Directly

**HEXT Patches:**
```hext
# NOP grid cursor draw call
718EFA = 90 90 90 90 90  # Original: E8 B9 24 FD FF = call 0x6EB3B8

# NOP sidebar cursor draw call
718FD6 = 90 90 90 90 90  # Original: E8 DD 23 FD FF = call 0x6EB3B8
```

**FFNx Code:**
```cpp
typedef void (__cdecl *draw_menu_cursor_func)(int x, int y, int z_bits);
static draw_menu_cursor_func g_vanilla_draw_cursor = (draw_menu_cursor_func)0x6EB3B8;

// Called from common_flip
void ff7_naming_screen_draw_cursor_tick()
{
    if (g_jp_naming_screen_active) {
        g_vanilla_draw_cursor(cursor_x, cursor_y, Z_DEPTH_BITS);
    }
}
```

**Result:** ❌ Cursor invisible. Function called with valid coordinates but nothing rendered.

**Why It Failed:**
- `common_flip` runs **after** the render scene is closed
- Vanilla's `0x6EB3B8` requires internal game state that isn't available at that execution point

---

### Attempt 2: Draw Cursor Using FFNx Text Renderer

**Approach:** Use `common_submit_draw_char_from_buffer_6F564E_jp()` inside `naming_screen_draw()`.

**Code:**
```cpp
const uint16_t HAND_CURSOR_CHAR = 0x1A;  // Tried 0xE0 first (was closed paren)
int cursor_x = GRID_BASE_X + grid_x * CELL_WIDTH - 25;
int cursor_y = GRID_BASE_Y + grid_y * CELL_HEIGHT;
common_submit_draw_char_from_buffer_6F564E_jp(cursor_x, cursor_y, 0, HAND_CURSOR_CHAR, NAMING_SCREEN_Z);
```

**Result:** ⚠️ **Partially Working But Issues Found**

---

## Current Problems Identified

### 1. Wrong Cursor Character
- `0xE0` → Closed parenthesis `)`
- `0x1A` → Japanese katakana `ゼ` (2 columns higher in katakana grid)
- **Need to find:** Actual hand cursor character code in window.bin

### 2. Cursor Positioning Issues

**Grid Cursor:**
- ❌ Too far high
- ❌ Too far to the right

**Sidebar Cursor:**
- ❌ Vertically too high
- ❌ Slightly too much to the left

**Current Calculation:**
```cpp
// Grid
cursor_x = GRID_BASE_X + grid_x * CELL_WIDTH - 25;  // 25px offset left
cursor_y = GRID_BASE_Y + grid_y * CELL_HEIGHT;      // No vertical offset

// Sidebar
cursor_x = SIDEBAR_X - 25;
cursor_y = SIDEBAR_Y + sidebar_y_pos * SIDEBAR_ITEM_HEIGHT;
```

**Constants:**
```cpp
GRID_BASE_X = 118;    // Where first column character renders
GRID_BASE_Y = 172;    // Where first row character renders
CELL_WIDTH = 40;      // Horizontal spacing between columns
CELL_HEIGHT = 33;     // Vertical spacing between rows

SIDEBAR_X = 505;      // Adjusted left
SIDEBAR_Y = 172;      // Aligned with grid top
SIDEBAR_ITEM_HEIGHT = 33;  // Match grid row height
```

---

### 3. Input Buffer Underscores Missing

**Problem:** Only 6 underscores visible instead of 9.

**Observation:**
- Users can still enter 9 characters
- Only the underscore `_` placeholder characters are not rendering fully
- Likely a rendering issue, not a buffer issue

---

### 4. Compilation Time Variance

**Observation:** FFNx build times vary dramatically:
- Fast builds: 1-2 seconds
- Slow builds: 10-15 seconds
- This session: Very long wait (15+ seconds)

**Possible Causes:**
- Incremental vs full rebuild
- CMake cache state
- Antivirus scanning
- WSL file system overhead

---

## Lessons Learned

### 1. External AI Consultation is Invaluable

**Benefits:**
- Avoids hours of trial-and-error
- Provides architectural context we couldn't discover alone
- Explains **why** things work, not just **what** to do

**Example:** Understanding the "fighting vs replacing" principle saved us from creating fragile HEXT patches.

---

### 2. Execution Point is Critical for Rendering

**Key Rule:**
> Never draw from `common_flip` - it runs **after** the render scene is closed.

**Correct Approach:**
- Draw from functions that run **inside** the game's render loop
- For naming screen: `naming_screen_draw()` is the right place

---

### 3. Character Codes Require Manual Discovery

**Process:**
1. Try likely values from external AI (`0xE0`, `0x1A`)
2. Observe what renders
3. Use a character map tool or dump window.bin to find actual code
4. Iterate

**Next Steps:**
- Dump window.bin character map
- Find actual hand cursor code
- Could be in range: `0x00-0x1F` (control characters)

---

### 4. Position Calculations Need Fine-Tuning

**Current Approach (Too Simplistic):**
```cpp
cursor_x = char_x - 25;  // Fixed offset
cursor_y = char_y;
```

**Better Approach:**
1. **Measure vanilla's cursor offset** from character position using screenshots
2. **Calculate exact offset** in pixels
3. **Apply offset** relative to our grid layout constants
4. **Test iteratively** with different offsets

**Formula:**
```cpp
// Vanilla cursor offset relative to character (measured from screenshots)
const int CURSOR_OFFSET_X = -20;  // Left of character
const int CURSOR_OFFSET_Y = +5;   // Slightly below character center

cursor_x = char_x + CURSOR_OFFSET_X;
cursor_y = char_y + CURSOR_OFFSET_Y;
```

---

## Next Steps (Recommended Priority)

### Immediate (High Priority)

1. **Find Hand Cursor Character Code**
   - Extract/dump window.bin character map
   - Identify actual hand cursor glyph code
   - Test values: `0x00`, `0x01`, `0x02`, ... `0x1F`

2. **Fix Cursor Positioning**
   - Take screenshots of vanilla cursor at various positions
   - Measure pixel offset from character to cursor "finger tip"
   - Calculate correct offset values
   - Update `cursor_x` and `cursor_y` calculations

3. **Fix Input Buffer Underscores**
   - Investigate why only 6 of 9 underscores render
   - Check if it's a string length issue or a rendering loop issue
   - Verify `NAME_MAX_CHARS` constant is 9

---

### Medium Priority

4. **Optimize Cursor Drawing**
   - Once character code is found, verify no blinking occurs
   - Ensure cursor updates smoothly during navigation
   - Test edge cases (fast navigation, page switches)

5. **Sidebar Cursor Fine-Tuning**
   - Adjust sidebar cursor Y offset to match label height
   - Verify alignment with all 7 sidebar items

---

### Future Work (Documented but Deferred)

From session 36 handoff:

6. **Sidebar Highlighting**
   - Yellow highlight for selected page (ひらがな/カタカナ/えいすう)
   - Implement via text color parameter in draw calls

7. **Visual Separation in Sidebar**
   - Add spacing between page labels and action buttons
   - Consider separator line or increased spacing

8. **Font Size Reduction**
   - Scale down grid and sidebar text if needed for fit
   - Use `patch_code_word()` to modify scale addresses:
     - Scale X: `0x00CC0D68`
     - Scale Y: `0x00CC0D6A`

---

## Files Modified This Session

### HEXT Patches
**File:** `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/ja/japanese_menu.txt`

**Added Patches:**
```hext
# Lines 3269-3275: Sidebar Navigation Control (FFNx Takeover)
718F46 = 90 90 90 90 90 90 90 90 90 90  # NOP vanilla sidebar entry
71900E = 90 90 90 90 90 90 90 90 90 90  # NOP vanilla sidebar exit

# Lines 3293-3299: Cursor Rendering Takeover
718EFA = 90 90 90 90 90  # NOP grid cursor draw
718FD6 = 90 90 90 90 90  # NOP sidebar cursor draw
```

---

### FFNx Source Code
**File:** `/mnt/c/FFNx/src/ff7/naming_screen.cpp`

**Added:**
- Lines 179-180: D-pad edge detection state variables
- Lines 218-223: Vanilla cursor draw function pointer (unused but kept for reference)
- Lines 820-854: Sidebar navigation logic (entry/exit)
- Lines 1245-1274: Cursor drawing using FFNx text renderer

**File:** `/mnt/c/FFNx/src/ff7/defs.h`

**Added:**
- Lines 138-139: `ff7_naming_screen_draw_cursor_tick()` declaration

**File:** `/mnt/c/FFNx/src/common.cpp`

**Added:**
- Lines 1088-1090: Call to cursor draw tick (now disabled)

---

## Technical Reference

### Memory Addresses Used

| Address    | Purpose              | Size   | Access    |
|------------|----------------------|--------|-----------|
| `0x921ED4` | `sidebar_flag`       | DWORD  | Read/Write|
| `0x921ED8` | `sidebar_cursor_y`   | DWORD  | Read/Write|
| `0xDD4538` | `grid_cursor_x`      | DWORD  | Read      |
| `0xDD453C` | `grid_cursor_y`      | DWORD  | Read      |
| `0x718F46` | Sidebar entry write  | 10B    | Patched   |
| `0x71900E` | Sidebar exit write   | 10B    | Patched   |
| `0x718EFA` | Grid cursor draw     | 5B     | Patched   |
| `0x718FD6` | Sidebar cursor draw  | 5B     | Patched   |

---

### Key Constants

```cpp
// Grid Layout
const int GRID_BASE_X = 118;
const int GRID_BASE_Y = 172;
const int CELL_WIDTH = 40;
const int CELL_HEIGHT = 33;
const int GRID_COLS = 10;
const int GRID_ROWS_HIRAGANA = 9;
const int GRID_ROWS_KATAKANA = 9;
const int GRID_ROWS_EISUU = 8;

// Sidebar Layout
const int SIDEBAR_X = 505;
const int SIDEBAR_Y = 172;
const int SIDEBAR_ITEM_HEIGHT = 33;
const int SIDEBAR_ITEM_COUNT = 7;

// Character Codes (Attempted)
const uint16_t HAND_CURSOR_CHAR = 0x1A;  // Currently: Katakana ゼ (WRONG)
// Tried: 0xE0 (closed parenthesis)
// Need: Actual hand cursor code (TBD)

// Z-Depth
const float NAMING_SCREEN_Z = 0.10f;
const int Z_DEPTH_BITS = 0x3DCCCCCD;  // 0.10f as int bits
```

---

## Cheat Engine Methodology

### Finding Write Addresses

**Process:**
1. Add target address to cheat table (e.g., `0x921ED4`)
2. Right-click → "Find out what writes to this address"
3. Perform action in-game (e.g., press D-pad to enter sidebar)
4. Note instruction address from breakpoint list
5. Calculate file offset: `File Offset = VA - 0x400000`

**Example:**
```
Virtual Address: 0x718F46
File Offset: 0x318F46  (0x718F46 - 0x400000)
HEXT Patch: 718F46 = 90 90 90 90 90 90 90 90 90 90
```

---

### Finding Read Addresses

**Process:**
1. Add target address to cheat table
2. Right-click → "Find out what accesses this address"
3. Perform action in-game
4. Filter results by:
   - **High count** (1000+) = likely in render loop
   - **Address range** `0x718XXX` = naming screen code
   - **Low count** (10-100) = likely input/logic code

---

## Performance Notes

### FFNx Build Time Variance

**Observations:**
- Cold build: 15+ seconds
- Warm build (no changes): 1-2 seconds
- Incremental (small change): 3-5 seconds

**Potential Causes:**
1. **CMake Cache:** First build after changes reconfigures
2. **WSL I/O Overhead:** Windows Defender scanning DLL writes
3. **Incremental Compilation:** Only changed files recompiled

**Recommendations:**
- Use `cmake --build . --config Release` for incremental builds
- Disable Windows Defender real-time scanning for FFNx build directory
- Build on WSL ext4 filesystem, not `/mnt/c/` for better I/O

---

## External AI Questions Archive

### Question 1: Sidebar Navigation Strategy

**Asked:** How to implement sidebar entry/exit via FFNx instead of HEXT?

**Answer:**
1. NOP vanilla writes to `sidebar_flag`
2. Implement in FFNx with edge detection
3. Put logic in `naming_screen_process_input()`

**Result:** ✅ Implemented successfully

---

### Question 2: Cursor Rendering Failure

**Asked:** Why does calling `0x6EB3B8` from `common_flip` not render the cursor?

**Answer:**
- `common_flip` runs **after** render scene is closed
- Must use `common_submit_draw_char_from_buffer_6F564E_jp()` inside `naming_screen_draw()`
- Hand cursor character code likely `0xE0` or `0x1A`

**Result:** ⚠️ Partial - rendering works but wrong character code and positioning

---

## Session Outcome Summary

### ✅ Completed
- Sidebar entry/exit via D-pad RIGHT/LEFT working correctly
- Vanilla sidebar entry/exit writes successfully NOPed
- FFNx sidebar navigation logic implemented with edge detection
- Cursor rendering approach identified (text renderer in draw loop)

### ⚠️ Partial
- Cursor visible but wrong character (showing katakana ゼ instead of hand)
- Cursor positioning incorrect (too high, too far right in grid)
- Sidebar cursor positioning incorrect (too high, too far left)

### ❌ Blocked
- Input buffer underscores: only 6 visible instead of 9

### 🔍 Investigation Needed
- Find actual hand cursor character code in window.bin
- Measure vanilla cursor offset from screenshots
- Debug underscore rendering issue

---

## Recommendations for Next Session

### 1. Character Code Discovery (Priority 1)

**Option A: Dump window.bin**
```bash
# Extract window.bin character map
cd /mnt/c/Program\ Files\ \(x86\)/Steam/steamapps/common/FINAL\ FANTASY\ VII/data
# Use FF7 tools to dump window.bin to image/map

# Or brute-force test all codes 0x00-0xFF in FFNx
for (int i = 0; i < 256; i++) {
    common_submit_draw_char_from_buffer_6F564E_jp(100 + (i % 16) * 20, 100 + (i / 16) * 20, 0, i, Z);
}
```

**Option B: Search FFNx Codebase**
```bash
rg "hand|finger|cursor.*0x" /mnt/c/FFNx/src --type cpp
rg "window.*char.*E0|1A" /mnt/c/FFNx/src --type cpp
```

---

### 2. Position Measurement (Priority 2)

**Process:**
1. Launch vanilla English FF7 naming screen
2. Take screenshots of cursor at positions (0,0), (5,3), (9,6)
3. Measure pixel offset from character top-left to cursor "finger tip"
4. Calculate average offset
5. Apply to FFNx cursor drawing code

**Expected Offset:**
```cpp
// Typical menu cursor offset (estimate)
const int CURSOR_OFFSET_X = -18;  // Left of character
const int CURSOR_OFFSET_Y = +8;   // Below character top, centered vertically
```

---

### 3. Underscore Investigation (Priority 3)

**Check:**
1. `NAME_MAX_CHARS` constant value (should be 9)
2. Name buffer rendering loop count
3. Underscore character rendering conditions
4. Z-depth conflicts (underscores behind other elements?)

**Likely Cause:** Rendering loop only iterates 6 times instead of 9.

**Code to Review:**
```cpp
// Find where underscores are drawn
rg "underscore|0x5F|NAME_MAX" /mnt/c/FFNx/src/ff7/naming_screen.cpp
```

---

## Closing Notes

This session demonstrated the value of **external AI consultation** combined with **systematic debugging via Cheat Engine**. The methodology shift from "trial HEXT patches" to "ask AI, verify with CE, implement in FFNx" proved significantly more effective.

However, the cursor rendering problem revealed that even with expert guidance, low-level game engine integration requires **iterative refinement**. Character codes and pixel-perfect positioning cannot be determined theoretically - they require empirical testing and measurement.

**Key Takeaway:**
> External AI provides the **architecture and strategy**. Cheat Engine provides the **addresses and verification**. But **character codes, offsets, and visual alignment** still require manual discovery and tuning.

---

## References

### Session Handoffs
- `SESSION_HANDOFF_2025-12-21-36_SIDEBAR_NAVIGATION_INVESTIGATION.md`
- `SESSION_HANDOFF_2025-12-21-35_CANCEL_START_BUTTON_FIX.md`

### External AI Responses
- `.project/ai responses/1.txt` - Sidebar navigation architecture
- `.project/ai responses/3.txt` - Cursor rendering execution point

### FFNx PR
- **PR #737:** Japanese Naming Screen Implementation
- **Branch:** `feature/japanese-naming-screen`

### Tools Used
- **Cheat Engine:** Memory breakpoint analysis
- **External AI:** Architectural guidance (full FFNx codebase access)
- **FFNx:** C++ implementation
- **HEXT:** Binary patching for vanilla code NOP

---

**End of Session Summary**
