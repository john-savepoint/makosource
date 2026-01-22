We want our character grid to be a smaller font size. How do we do that?
The input buffer at the top of the screen needs to remain the default size, but the character group inside might need to be a little smaller.

---

Based on the FFNx codebase and Final Fantasy VII's memory map, you can adjust the font size by patching the global text scale variables in memory just before drawing the grid, and restoring them immediately after.

The game uses two 2-byte (WORD) integers to control text scaling:

- **Scale X:** `0x00CC0D68` (Default: `0x100` / 256)
- **Scale Y:** `0x00CC0D6A` (Default: `0x100` / 256)

You need to modify `naming_screen_draw` in `src/ff7/field/naming_screen_jp.cpp` to adjust these values dynamically.

### Step 1: Define the addresses and helper function

Add this near the top of your file (e.g., after the Includes/Enums):

```cpp
// Vanilla Text Scale Memory Addresses (US 1.02)
// 0x100 (256) = 100% scale. 0x80 (128) = 50% scale.
const uint32_t TEXT_SCALE_X_ADDR = 0x00CC0D68;
const uint32_t TEXT_SCALE_Y_ADDR = 0x00CC0D6A;

static void set_text_scale(int percent)
{
    // Convert percentage to fixed point (100% = 256)
    WORD scale_val = (WORD)((256 * percent) / 100);

    // We use patch_code_word from FFNx's patch.h to modify memory safely
    patch_code_word(TEXT_SCALE_X_ADDR, scale_val);
    patch_code_word(TEXT_SCALE_Y_ADDR, scale_val);
}
```

### Step 2: Update the Draw Loop

Modify your `naming_screen_draw` function to sandwich the grid drawing between scale changes. The Input Buffer (Preview) will be drawn after resetting the scale, keeping it at default size.

```cpp
static void naming_screen_draw()
{
    g_jp_naming_screen_drawing = true;

    // --- DRAW GRID (SMALLER) ---
    // Set text size to 85% (adjust this number as needed)
    set_text_scale(85);

    // Update grid constants to pack them tighter if font is smaller
    // (You might need to adjust CELL_WIDTH/HEIGHT constants at the top of the file too)
    naming_screen_draw_character_grid();

    // Also draw sidebar/page indicators with smaller font if desired?
    // naming_screen_draw_page_indicator();

    // --- DRAW PREVIEW (DEFAULT SIZE) ---
    // Reset text size to 100% (Vanilla default)
    set_text_scale(100);

    naming_screen_draw_name_preview();

    g_jp_naming_screen_drawing = false;
}
```

### Note on Layout

When you reduce the font size, the characters will visually shrink, but they will still be spaced apart by `CELL_WIDTH` and `CELL_HEIGHT`. To make the grid look compact, you should also reduce your constants at the top of the file:

```cpp
// Adjust these values to tighten the grid spacing
const int CELL_WIDTH = 32;   // Was 40
const int CELL_HEIGHT = 28;  // Was 33
```
