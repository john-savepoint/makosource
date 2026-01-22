# Naming Screen Yellow Highlight Investigation

**Created:** 2025-12-22 17:30 JST (Monday)
**Session-ID:** f69f12b6-63e5-4c7c-9dfe-30e9fa088f96
**Status:** Parked - Feature not implemented

## Goal

Make the Hiragana, Katakana, and Eisuu sidebar selections display in yellow text to indicate the currently active page, matching the Japanese version behavior.

## Background

In the Japanese version of FF7, the naming screen sidebar shows the current page (ひらがな/カタカナ/えいすう) highlighted in yellow. The English version doesn't have these page labels at all - we added them via HEXT patches to memory addresses 0x921D30, 0x921D38, 0x921D40.

## Investigation Summary

### Approaches Tried

#### 1. FE D8 Color Code Injection (Failed)
- **Approach:** Dynamically patch sidebar label data with `FE D8` (yellow color code) prefix
- **Result:** No effect
- **Root Cause:** Vanilla's sidebar text renderer (`0x6F51B3`) doesn't process FE color codes. This function is different from the main text rendering function that does handle color codes.

#### 2. NOPing Vanilla Sidebar Render (Failed)
- **Approach:** NOP vanilla's sidebar text call at `0x719246-0x71924E` and have FFNx draw with colors
- **Result:** Crashes the game
- **Attempts:**
  - 5-byte NOP (call only) - crashed
  - 9-byte NOP (push + call + stack cleanup) - crashed
- **Root Cause:** The sidebar rendering loop has dependencies we don't fully understand

#### 3. FFNx Overdraw (Failed)
- **Approach:** Let vanilla draw sidebar, then FFNx overdraws with colored text
- **Result:** Strobing/flickering effect
- **Key Finding:** Only FFNx strobes; vanilla renders stably
- **Root Cause:** NOT a race condition between vanilla and FFNx. The issue is internal to FFNx rendering - possibly related to:
  - Vertex buffer timing (FFNx and vanilla share graphics objects)
  - Frame buffer state
  - The `g_get_do_render_menu_6CDBF2()` flag check in FFNx's draw functions
- **Note:** Setting `DO_RENDER_MENU_FLAG` to 1 before FFNx draws did not fix the strobing

#### 4. Global Color Variable (Failed)
- **Approach:** Set `word_91F028` (global text color) to yellow before vanilla renders
- **Result:** No effect on sidebar text
- **Root Cause:** The sidebar renderer `0x6F51B3` doesn't read from `word_91F028`

### Key Technical Findings

1. **Sidebar Text Renderer:** `0x6F51B3`
   - Called from sidebar rendering loop at `0x719247`
   - Takes string pointer as parameter (pushed via EDX)
   - Does NOT process FE color codes
   - Does NOT read from `word_91F028` global color variable
   - Different from `common_submit_draw_char_from_buffer_6F564E` which FFNx hooks

2. **Blinking Underscore:** Uses a DIFFERENT rendering function
   - NOT rendered via `0x6F51B3` (breakpoint didn't trigger)
   - Uses frame counter at `0xDD4630` for blink timing
   - Has code at `0x717E7C` that compares counter and sets color
   - Pushes color values 6 and 7, but patching these didn't affect the blink
   - The actual draw function for underscores remains unidentified

3. **Color System:**
   - FFNx uses: 0=gray, 5=yellow, 6=cyan, 7=white
   - Vanilla may use different values
   - FE Dx control codes: FE D2=gray, FE D8=yellow (but only processed by certain functions)

4. **FFNx Strobing Issue:**
   - Vanilla text is always stable
   - FFNx-drawn text strobes (appears/disappears rapidly)
   - Not caused by: render flag, race conditions, double-buffering
   - Likely caused by: vertex buffer sharing, frame timing, or graphics object state

### Memory Addresses

| Address | Description |
|---------|-------------|
| 0x921D30 | Sidebar label: ひらがな (Hiragana) |
| 0x921D38 | Sidebar label: カタカナ (Katakana) |
| 0x921D40 | Sidebar label: えいすう (Eisuu) |
| 0x6F51B3 | Sidebar text rendering function |
| 0x719246 | Sidebar render call (PUSH+CALL+CLEANUP) |
| 0xDD4630 | Naming screen frame counter |
| 0xDD46F8 | Underscore blink counter |
| 0x91F028 | Global text color variable (word) |
| 0x91AA8C | "Do render menu" flag |

## Future Implementation Options

If this feature is revisited, the following approaches may work:

### Option A: Hook 0x6F51B3 in FFNx
Replace or wrap vanilla's `0x6F51B3` function to add color parameter support. This would require:
1. Understanding the full function signature
2. Adding a mechanism to pass color per-item
3. Implementing the color selection logic based on current page

### Option B: Find the Underscore Draw Function
The blinking underscore successfully renders with colors. If we can identify its draw function, we might be able to:
1. Use the same function for sidebar labels
2. Understand how vanilla handles colored text
3. Apply similar techniques to sidebar rendering

### Option C: Fix FFNx Strobing
If the root cause of FFNx strobing is identified and fixed:
1. FFNx overdraw approach becomes viable
2. Would enable colored sidebar labels and other UI enhancements
3. Requires deep investigation of FFNx rendering pipeline

## Files Modified (Reverted)

- `/mnt/c/FFNx/src/ff7/naming_screen.cpp` - Added then removed color patching code
- `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/ja/japanese_menu.txt` - Test patches removed

## Cheat Engine Investigation Notes

Frame counter scan results in `0x00DDXXXX` range:
- `0xDD4630` - Frame counter (constantly incrementing)

"Changed value" scans for underscore blink found addresses only in graphics memory ranges (0x03, 0x0B, 0x0C, 0x0D, 0x21, 0x26), not in game state memory - suggesting color is calculated on-the-fly or stored in GPU buffers.

## Conclusion

Yellow highlighting for the page indicator is not feasible with current understanding of vanilla's rendering system. The sidebar uses a different text renderer that doesn't support color codes, and FFNx overdraw causes unresolved strobing issues. Future implementation would require either hooking vanilla's sidebar renderer or solving the FFNx rendering stability issue.
