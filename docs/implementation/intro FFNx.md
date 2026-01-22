There is an intro video or image that gets played when the game launches for FFNx that plays before even the game's actual developer intros play. Is it possible to remove this?

---

Based on the code analysis, it is **not possible** to disable the FFNx startup logo through configuration files (like `FFNx.toml`). The sequence is hardcoded into the driver's C++ source code.

However, the code does include logic to skip it immediately upon button press.

### Technical Details

The logo logic is defined in `src/common.cpp` and hooked in `src/ff7_opengl.cpp`.

1.  **Duration:** The logo is set to display for 180 frames (approx. 3 seconds at 60FPS).

    - _Source:_ `src/common.cpp` line 3548: `constexpr int FFNX_LOGO_FRAME_COUNT = 180;`

2.  **Logic:** The function `drawFFNxLogoFrame` checks the frame count. If it hasn't reached 180, it draws the logo and returns `true`, preventing the game from rendering the actual scene behind it.

    - _Source:_ `src/common.cpp` lines 3551-3584.

3.  **Skip Mechanism:** You can skip the logo by pressing any button. The hook checks for button presses and calls `stopDrawFFNxLogo()` if detected.
    - _Source:_ `src/ff7_opengl.cpp` lines 38-49:
      ```cpp
      uint32_t ff7_credits_loop_gfx_begin_scene(uint32_t unknown, struct game_obj *game_object)
      {
          if (drawFFNxLogoFrame(game_object)) {
              if (ff7_externals.get_button_pressed(-1)) {
                  stopDrawFFNxLogo();
              }
              return 0;
          }
          return common_begin_scene(unknown, game_object);
      }
      ```

### How to remove it (Source Code Modification)

If you are compiling FFNx yourself, you can disable it by modifying `src/common.cpp` to set the frame count to 0:

**File:** `src/common.cpp`

```cpp
// Change line 3548
constexpr int FFNX_LOGO_FRAME_COUNT = 0;
```
