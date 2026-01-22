# Japanese Naming Screen Implementation Plan for FFNx

**Created:** 2025-12-12 14:40 JST (Friday)
**Session-ID:** 0681f78b-0382-45ee-898b-5a32b7ce32d5
**Version:** 1.0.0
**Author:** John Zealand-Doyle

---

## Table of Contents

1. [Overview](#overview)
2. [Current State Analysis](#current-state-analysis)
3. [Target Design](#target-design)
4. [Architecture](#architecture)
5. [Data Structures](#data-structures)
6. [Character Tables](#character-tables)
7. [Core Functions](#core-functions)
8. [Input Handling](#input-handling)
9. [Rendering System](#rendering-system)
10. [Name Buffer Integration](#name-buffer-integration)
11. [Implementation Phases](#implementation-phases)
12. [File Reference](#file-reference)
13. [Technical Notes](#technical-notes)

---

## Overview

### Goal

Replace the currently disabled English keyboard naming screen with a 3-page Japanese character selection system, matching the original Japanese FF7 experience.

### Pages

| Page | Japanese | Characters | Grid Size |
|------|----------|------------|-----------|
| 1 | ひらがな | Hiragana (あ-ん + voiced + small) | 9×10 |
| 2 | カタカナ | Katakana (ア-ン + voiced + small) | 9×10 |
| 3 | えいすう | Alphanumeric (A-Z, 0-9, ♥) | 5×10 |

### Key Features

- D-pad navigation through character grid
- L1/R1 page switching
- Sidebar with page selector and actions
- Animated hand cursor (matching other FF7 menus)
- Name preview with editable cursor position
- Default name loading per character

---

## Current State Analysis

### What Exists Now

**English EXE (`ff7_en.exe`):**
- Single-page ASCII keyboard at file offset `0x520770`
- 7×10 grid (A-Z uppercase, a-z lowercase, 0-9, punctuation)
- Sidebar labels at `0x520748`: Space, Delete, Select, Default
- `keyboard_name_input` function handles input processing

**FFNx Current Hook (`ff7_opengl.cpp:459`):**
```cpp
replace_function(ff7_externals.keyboard_name_input, noop);
```
- Disables keyboard input entirely (for Steam gamepad compatibility)
- Three related functions also disabled:
  - `set_default_input_settings_save`
  - `keyboard_name_input`
  - `restore_input_settings`

**Japanese EXE Data:**
- Hiragana table at file offset `0x521370`
- Katakana table at file offset `0x521478`
- えいすう (alphanumeric) is dynamically generated, not stored

### Hook Chain (from `ff7_data.h:405-430`)

```
menu_main_loop
  └─ menu_sub_6CDA83 [+0x112]
      └─ name_menu_sub_6CBD32 [+0x9A]
          └─ name_menu_sub_719C08 [+0x7]
              ├─ menu_sub_71894B [+0x2A]
              │   └─ set_default_input_settings_save [+0x188]
              │
              ├─ menu_sub_718DBE [+0x76]
              │   └─ keyboard_name_input [+0x99]  ← OUR HOOK POINT
              │
              └─ menu_sub_719B81 [+0xCB]
                  └─ restore_input_settings [+0x80]
```

---

## Target Design

### Screen Layout (640×480 coordinates)

```
┌─────────────────────────────────────────────────────────────┐
│  名前を決めてください。                                      │  Y: 40-80
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────┐     クラウド                                      │  Y: 100-160
│  │ Face │     ─────────                                     │
│  └──────┘                                                   │
│                                                             │
├───────────────────────────────────────────┬─────────────────┤
│                                           │                 │
│   あ  い  う  え  お  ぁ  ぃ  ぅ  ぇ  ぉ   │  ひらがな      │  Y: 200
│   か  き  く  け  こ  が  ぎ  ぐ  げ  ご   │  カタカナ      │
│   さ  し  す  せ  そ  ざ  じ  ず  ぜ  ぞ   │  えいすう      │
│   た  ち  つ  て  と  だ  ぢ  づ  で  ど   │                 │
│   な  に  ぬ  ね  の  っ       ～         │  スペース      │
│   は  ひ  ふ  へ  ほ  ば  び  ぶ  べ  ぼ   │  さくじょ      │
│   ま  み  む  め  も  ぱ  ぴ  ぷ  ぺ  ぽ   │                 │
│   や  ゆ  よ  ゃ  ゅ  ょ       　  　      │  けってい      │
│   ら  り  る  れ  ろ  わ  を  ん  　  　   │  デフォルト    │  Y: 440
│                                           │                 │
│   X: 100                              450 │ 480         600 │
└───────────────────────────────────────────┴─────────────────┘
```

### Layout Constants

```cpp
// Grid positioning
const int GRID_BASE_X = 100;        // Left edge of character grid
const int GRID_BASE_Y = 200;        // Top edge of character grid
const int CELL_WIDTH = 35;          // Width per cell (pixels)
const int CELL_HEIGHT = 26;         // Height per cell (pixels)
const int GRID_COLS = 10;           // Columns in grid
const int GRID_ROWS_KANA = 9;       // Rows for hiragana/katakana
const int GRID_ROWS_EISUU = 5;      // Rows for alphanumeric

// Sidebar positioning
const int SIDEBAR_X = 480;          // Left edge of sidebar
const int SIDEBAR_Y = 200;          // Top edge of sidebar
const int SIDEBAR_ITEM_HEIGHT = 26; // Height per sidebar item
const int SIDEBAR_ITEMS = 7;        // Number of sidebar items

// Name preview area
const int NAME_PREVIEW_X = 240;     // X position of name display
const int NAME_PREVIEW_Y = 130;     // Y position of name display
const int NAME_CHAR_WIDTH = 24;     // Width per character in preview
const int NAME_MAX_CHARS = 9;       // Maximum name length (Japanese)

// Z-depth for rendering
const float NAMING_SCREEN_Z = 0.95f;
```

---

## Architecture

### Files to Create

| File | Purpose |
|------|---------|
| `/mnt/c/FFNx/src/ff7/naming_screen.cpp` | Main implementation file |

### Files to Modify

| File | Change |
|------|--------|
| `/mnt/c/FFNx/src/ff7/defs.h` | Add function declaration |
| `/mnt/c/FFNx/src/ff7_opengl.cpp` | Change `noop` to our function |

### Hook Integration

**In `ff7/defs.h`** (add after line 131):
```cpp
// Japanese naming screen
void ff7_naming_screen_jp();
```

**In `ff7_opengl.cpp`** (change line 459):
```cpp
// Before:
replace_function(ff7_externals.keyboard_name_input, noop);

// After:
replace_function(ff7_externals.keyboard_name_input, ff7_naming_screen_jp);
```

---

## Data Structures

### State Structure

```cpp
// Page enumeration
enum NamingScreenPage {
    PAGE_HIRAGANA = 0,   // ひらがな
    PAGE_KATAKANA = 1,   // カタカナ
    PAGE_EISUU = 2       // えいすう
};

// Sidebar action enumeration
enum SidebarAction {
    SIDEBAR_HIRAGANA = 0,   // ひらがな
    SIDEBAR_KATAKANA = 1,   // カタカナ
    SIDEBAR_EISUU = 2,      // えいすう
    SIDEBAR_SPACE = 3,      // スペース
    SIDEBAR_DELETE = 4,     // さくじょ
    SIDEBAR_CONFIRM = 5,    // けってい
    SIDEBAR_DEFAULT = 6     // デフォルト
};

// Main state structure
struct NamingScreenState {
    // Page and cursor state
    NamingScreenPage current_page;      // Current active page (0-2)
    int cursor_x;                        // Grid column (0-9)
    int cursor_y;                        // Grid row (0-8 for kana, 0-4 for eisuu)
    int sidebar_cursor;                  // Sidebar position (0-6)
    bool in_sidebar;                     // True if cursor in sidebar

    // Name editing state
    int name_cursor_pos;                 // Current position in name (0-8)
    uint8_t name_buffer[12];             // Name being entered (9 chars + padding)
    int character_index;                 // Which character we're naming (0-8)

    // Control state
    bool is_active;                      // Screen is currently active
    bool confirm_pressed;                // Track confirm button state
    bool cancel_pressed;                 // Track cancel button state
    bool l1_pressed;                     // Track L1 state
    bool r1_pressed;                     // Track R1 state

    // Input timing
    uint32_t last_input_frame;           // Frame counter for debouncing
    uint32_t input_repeat_delay;         // Frames to wait for repeat
    uint32_t input_repeat_rate;          // Frames between repeats
};

// Global state instance
static NamingScreenState g_naming_state = {0};
```

### Input Timing Constants

```cpp
const uint32_t INPUT_INITIAL_DELAY = 15;  // ~0.5 sec before repeat starts
const uint32_t INPUT_REPEAT_RATE = 4;     // ~0.13 sec between repeats
```

---

## Character Tables

### Hiragana Table (9×10 = 90 positions)

Based on Japanese EXE at file offset `0x521370`:

```cpp
// jafont_1 indices for hiragana
// Row format: basic + voiced + small variants
static const uint8_t HIRAGANA_TABLE[9][10] = {
    // Row 0: あ行 + small あ行
    {0x6B, 0x6D, 0x69, 0x6F, 0x71, 0xA5, 0xA7, 0xA9, 0xAB, 0xAD},
    // あ    い    う    え    お    ぁ    ぃ    ぅ    ぇ    ぉ

    // Row 1: か行 + が行
    {0x4B, 0x4D, 0x4F, 0x51, 0x53, 0x0B, 0x0D, 0x0F, 0x11, 0x13},
    // か    き    く    け    こ    が    ぎ    ぐ    げ    ご

    // Row 2: さ行 + ざ行
    {0x55, 0x57, 0x59, 0x5B, 0x5D, 0x15, 0x17, 0x19, 0x1B, 0x1D},
    // さ    し    す    せ    そ    ざ    じ    ず    ぜ    ぞ

    // Row 3: た行 + だ行
    {0x5F, 0x61, 0x63, 0x65, 0x67, 0x1F, 0x21, 0x23, 0x25, 0x27},
    // た    ち    つ    て    と    だ    ぢ    づ    で    ど

    // Row 4: な行 + special
    {0x73, 0x75, 0x77, 0x79, 0x7B, 0x3F, 0x3F, 0x3F, 0x3F, 0xD1},
    // な    に    ぬ    ね    の    　    　    　    　    ～

    // Row 5: は行 + ば行
    {0x41, 0x43, 0x45, 0x47, 0x49, 0x01, 0x03, 0x05, 0x07, 0x09},
    // は    ひ    ふ    へ    ほ    ば    び    ぶ    べ    ぼ

    // Row 6: ま行 + ぱ行
    {0x7D, 0x7F, 0x81, 0x83, 0x85, 0x2A, 0x2C, 0x2E, 0x30, 0x32},
    // ま    み    む    め    も    ぱ    ぴ    ぷ    ぺ    ぽ

    // Row 7: や行 + small や行 + special
    {0x91, 0x93, 0x95, 0x9F, 0xA1, 0xA3, 0x9D, 0x3F, 0x3D, 0x3E},
    // る    れ    ろ    ゃ    ゅ    ょ    っ    　    ＝    −

    // Row 8: ら行 + わ行
    {0x87, 0x89, 0x8B, 0x8D, 0x8F, 0x97, 0x9B, 0x99, 0xAE, 0xAF},
    // や    ゆ    よ    ら    り    わ    ん    を    ー    ～
};
```

### Katakana Table (9×10 = 90 positions)

Based on Japanese EXE at file offset `0x521478`:

```cpp
// jafont_1 indices for katakana
static const uint8_t KATAKANA_TABLE[9][10] = {
    // Row 0: ア行 + small ア行
    {0x6A, 0x6C, 0x68, 0x6E, 0x70, 0xA4, 0xA6, 0xA8, 0xAA, 0xAC},
    // ア    イ    ウ    エ    オ    ァ    ィ    ゥ    ェ    ォ

    // Row 1: カ行 + ガ行
    {0x4A, 0x4C, 0x4E, 0x50, 0x52, 0x0A, 0x0C, 0x0E, 0x10, 0x12},
    // カ    キ    ク    ケ    コ    ガ    ギ    グ    ゲ    ゴ

    // Row 2: サ行 + ザ行
    {0x54, 0x56, 0x58, 0x5A, 0x5C, 0x14, 0x16, 0x18, 0x1A, 0x1C},
    // サ    シ    ス    セ    ソ    ザ    ジ    ズ    ゼ    ゾ

    // Row 3: タ行 + ダ行
    {0x5E, 0x60, 0x62, 0x64, 0x66, 0x1E, 0x20, 0x22, 0x24, 0x26},
    // タ    チ    ツ    テ    ト    ダ    ヂ    ヅ    デ    ド

    // Row 4: ナ行 + brackets
    {0x72, 0x74, 0x76, 0x78, 0x7A, 0xD7, 0xD8, 0xDF, 0xE0, 0xD0},
    // ナ    ニ    ヌ    ネ    ノ    【    】    （    ）    ー

    // Row 5: ハ行 + バ行
    {0x40, 0x42, 0x44, 0x46, 0x48, 0x00, 0x02, 0x04, 0x06, 0x08},
    // ハ    ヒ    フ    ヘ    ホ    バ    ビ    ブ    ベ    ボ

    // Row 6: マ行 + パ行
    {0x7C, 0x7E, 0x80, 0x82, 0x84, 0x29, 0x2B, 0x2D, 0x2F, 0x31},
    // マ    ミ    ム    メ    モ    パ    ピ    プ    ペ    ポ

    // Row 7: special
    {0x90, 0x92, 0x94, 0x9E, 0xA0, 0xA2, 0x9C, 0x28, 0xCE, 0xD2},
    // ル    レ    ロ    ャ    ュ    ョ    ッ    パ    ＋    …

    // Row 8: ヤ行 + ワ行
    {0x86, 0x88, 0x8A, 0x8C, 0x8E, 0x96, 0x9A, 0x98, 0xD5, 0xD4},
    // ヤ    ユ    ヨ    ラ    リ    ワ    ン    ヲ    ：    ／
};
```

### Eisuu (Alphanumeric) Table (5×10 = 50 positions)

Using fullwidth characters from jafont_1:

```cpp
// jafont_1 indices for alphanumeric (fullwidth)
static const uint8_t EISUU_TABLE[5][10] = {
    // Row 0: A-J (fullwidth)
    {0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD},
    // Ａ    Ｂ    Ｃ    Ｄ    Ｅ    Ｆ    Ｇ    Ｈ    Ｉ    Ｊ

    // Row 1: K-T (fullwidth)
    {0xBE, 0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7},
    // Ｋ    Ｌ    Ｍ    Ｎ    Ｏ    Ｐ    Ｑ    Ｒ    Ｓ    Ｔ

    // Row 2: U-Z + . α β
    {0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD, 0x3F, 0xDB, 0xDC, 0x3F},
    // Ｕ    Ｖ    Ｗ    Ｘ    Ｙ    Ｚ    　    α     β

    // Row 3: 0-9 (fullwidth)
    {0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C},
    // ０    １    ２    ３    ４    ５    ６    ７    ８    ９

    // Row 4: symbols
    {0xCF, 0xD3, 0xD6, 0xD9, 0xDA, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F},
    // ＊    ％    ＆    ♥     →
};
```

### Sidebar Labels

```cpp
// Sidebar label byte sequences (jafont_1 indices)
// Each label is an array of bytes followed by 0xFF terminator

// ひらがな (hiragana)
static const uint8_t SIDEBAR_HIRAGANA[] = {0x41, 0x87, 0x0B, 0x73, 0xFF};

// カタカナ (katakana)
static const uint8_t SIDEBAR_KATAKANA[] = {0x4A, 0x5E, 0x4A, 0x72, 0xFF};

// えいすう (eisuu)
static const uint8_t SIDEBAR_EISUU[] = {0x6F, 0x6D, 0x59, 0x69, 0xFF};

// スペース (space)
static const uint8_t SIDEBAR_SPACE[] = {0x58, 0x2F, 0xD0, 0x58, 0xFF};

// さくじょ (delete)
static const uint8_t SIDEBAR_DELETE[] = {0x55, 0x4F, 0x17, 0xA3, 0xFF};

// けってい (confirm)
static const uint8_t SIDEBAR_CONFIRM[] = {0x51, 0x9D, 0x65, 0x6D, 0xFF};

// デフォルト (default)
static const uint8_t SIDEBAR_DEFAULT[] = {0x24, 0x44, 0xAC, 0x8A, 0x66, 0xFF};

// Array of sidebar labels
static const uint8_t* SIDEBAR_LABELS[7] = {
    SIDEBAR_HIRAGANA,
    SIDEBAR_KATAKANA,
    SIDEBAR_EISUU,
    SIDEBAR_SPACE,
    SIDEBAR_DELETE,
    SIDEBAR_CONFIRM,
    SIDEBAR_DEFAULT
};
```

---

## Core Functions

### Function Declarations

```cpp
// ===== Main Entry Point =====
void ff7_naming_screen_jp();

// ===== State Management =====
void naming_screen_init(int character_index);
void naming_screen_cleanup();
void naming_screen_reset_cursor();

// ===== Input Processing =====
void naming_screen_process_input();
bool naming_screen_is_button_pressed(uint32_t button_field, bool* was_pressed);
void naming_screen_handle_dpad_move(int dx, int dy);
void naming_screen_handle_page_switch(int direction);
void naming_screen_handle_confirm();
void naming_screen_handle_cancel();

// ===== Character Grid Actions =====
void naming_screen_select_grid_character();
uint8_t naming_screen_get_char_at_cursor();
int naming_screen_get_max_rows();

// ===== Name Buffer Actions =====
void naming_screen_add_character(uint8_t char_code);
void naming_screen_delete_character();
void naming_screen_add_space();
void naming_screen_set_default_name();
void naming_screen_confirm_name();

// ===== Sidebar Actions =====
void naming_screen_execute_sidebar_action();
void naming_screen_switch_to_page(NamingScreenPage page);

// ===== Rendering =====
void naming_screen_draw();
void naming_screen_draw_character_grid();
void naming_screen_draw_sidebar();
void naming_screen_draw_name_preview();
void naming_screen_draw_cursor();
void naming_screen_draw_single_char(int x, int y, uint8_t char_code, int color);
void naming_screen_draw_string(int x, int y, const uint8_t* str, int color);

// ===== Utility =====
void naming_screen_get_default_name(int character_index, uint8_t* out_buffer);
bool naming_screen_is_valid_cell(int row, int col);
```

---

## Input Handling

### Gamepad Status Structure Reference

From `ff7.h:1975-1999`:

```cpp
struct ff7_gamepad_status {
    uint32_t pos_x;        // Analog X
    uint32_t pos_y;        // Analog Y
    uint32_t dpad_up;      // D-Pad UP
    uint32_t dpad_down;    // D-Pad DOWN
    uint32_t dpad_left;    // D-Pad LEFT
    uint32_t dpad_right;   // D-Pad RIGHT
    uint32_t button1;      // Square (X)
    uint32_t button2;      // Cross (A) - OK
    uint32_t button3;      // Circle (B) - Cancel
    uint32_t button4;      // Triangle (Y)
    uint32_t button5;      // L1
    uint32_t button6;      // R1
    uint32_t button7;      // L2
    uint32_t button8;      // R2
    uint32_t button9;      // SELECT
    uint32_t button10;     // START
    // ... more fields
};
```

### Input Mapping

| Input | Action |
|-------|--------|
| D-Pad Up | Move cursor up |
| D-Pad Down | Move cursor down |
| D-Pad Left | Move cursor left / Enter sidebar |
| D-Pad Right | Move cursor right / Exit sidebar |
| L1 (button5) | Previous page |
| R1 (button6) | Next page |
| Cross (button2) | Select character / Execute action |
| Circle (button3) | Delete character / Cancel |

### Input Processing Logic

```cpp
void naming_screen_process_input() {
    ff7_gamepad_status* pad = ff7_externals.gamepad_status;

    // Get current frame for timing
    static uint32_t frame_counter = 0;
    frame_counter++;

    // D-Pad with repeat
    if (pad->dpad_up) {
        if (should_process_input(frame_counter)) {
            naming_screen_handle_dpad_move(0, -1);
        }
    }
    else if (pad->dpad_down) {
        if (should_process_input(frame_counter)) {
            naming_screen_handle_dpad_move(0, 1);
        }
    }
    else if (pad->dpad_left) {
        if (should_process_input(frame_counter)) {
            naming_screen_handle_dpad_move(-1, 0);
        }
    }
    else if (pad->dpad_right) {
        if (should_process_input(frame_counter)) {
            naming_screen_handle_dpad_move(1, 0);
        }
    }
    else {
        // Reset repeat when no D-pad pressed
        g_naming_state.last_input_frame = 0;
    }

    // L1/R1 for page switch (edge-triggered only)
    if (naming_screen_is_button_pressed(pad->button5, &g_naming_state.l1_pressed)) {
        naming_screen_handle_page_switch(-1);  // Previous page
    }
    if (naming_screen_is_button_pressed(pad->button6, &g_naming_state.r1_pressed)) {
        naming_screen_handle_page_switch(1);   // Next page
    }

    // Cross for confirm (edge-triggered)
    if (naming_screen_is_button_pressed(pad->button2, &g_naming_state.confirm_pressed)) {
        naming_screen_handle_confirm();
    }

    // Circle for cancel/delete (edge-triggered)
    if (naming_screen_is_button_pressed(pad->button3, &g_naming_state.cancel_pressed)) {
        naming_screen_handle_cancel();
    }
}

// Edge-triggered button detection
bool naming_screen_is_button_pressed(uint32_t button_state, bool* was_pressed) {
    bool pressed_now = button_state != 0;
    bool result = pressed_now && !(*was_pressed);
    *was_pressed = pressed_now;
    return result;
}
```

---

## Rendering System

### Drawing Characters

Use existing Japanese text rendering function:

```cpp
// From defs.h:123
int common_submit_draw_char_from_buffer_6F564E_jp(
    int x,              // Screen X position
    int vertex_y,       // Screen Y position
    int n_shapes,       // Color index (0-7)
    unsigned __int16 letter,  // Character code (jafont index)
    float z_value       // Depth (0.0-1.0)
);
```

### Color Indices

```cpp
// Color palette (from japanese_text.cpp)
enum CharacterColor {
    COLOR_GRAY = 0,      // (106, 106, 106)
    COLOR_BROWN = 1,     // (189, 98, 7)
    COLOR_BLUE = 2,      // (10, 0, 189)
    COLOR_MAGENTA = 3,   // (230, 10, 230)
    COLOR_GREEN = 4,     // (124, 230, 90)
    COLOR_YELLOW = 5,    // (230, 230, 10)
    COLOR_CYAN = 6,      // (10, 230, 230)
    COLOR_WHITE = 7      // (230, 230, 230)
};
```

### Grid Rendering

```cpp
void naming_screen_draw_character_grid() {
    const uint8_t (*table)[10];
    int max_rows;

    // Select table based on current page
    switch (g_naming_state.current_page) {
        case PAGE_HIRAGANA:
            table = HIRAGANA_TABLE;
            max_rows = GRID_ROWS_KANA;
            break;
        case PAGE_KATAKANA:
            table = KATAKANA_TABLE;
            max_rows = GRID_ROWS_KANA;
            break;
        case PAGE_EISUU:
            table = EISUU_TABLE;
            max_rows = GRID_ROWS_EISUU;
            break;
    }

    // Draw each character
    for (int row = 0; row < max_rows; row++) {
        for (int col = 0; col < GRID_COLS; col++) {
            uint8_t char_code = table[row][col];

            // Skip empty cells (0x3F = ideographic space, 0x00 = invalid)
            if (char_code == 0x3F || char_code == 0x00) continue;

            int x = GRID_BASE_X + (col * CELL_WIDTH);
            int y = GRID_BASE_Y + (row * CELL_HEIGHT);

            // Normal color for all characters
            int color = COLOR_WHITE;

            common_submit_draw_char_from_buffer_6F564E_jp(
                x, y, color, (unsigned __int16)char_code, NAMING_SCREEN_Z
            );
        }
    }
}
```

### Cursor Drawing

Use the animated hand cursor from other FF7 menus:

```cpp
void naming_screen_draw_cursor() {
    int cursor_x, cursor_y;

    if (g_naming_state.in_sidebar) {
        // Position cursor next to sidebar item
        cursor_x = SIDEBAR_X - 24;
        cursor_y = SIDEBAR_Y + (g_naming_state.sidebar_cursor * SIDEBAR_ITEM_HEIGHT);
    } else {
        // Position cursor at grid cell
        cursor_x = GRID_BASE_X + (g_naming_state.cursor_x * CELL_WIDTH) - 24;
        cursor_y = GRID_BASE_Y + (g_naming_state.cursor_y * CELL_HEIGHT);
    }

    // Draw hand cursor sprite
    // TODO: Find existing hand cursor drawing code from other menus
    // Likely uses a graphics object from menu textures
    // Reference: field_submit_draw_pointer_hand or similar
}
```

---

## Name Buffer Integration

### Savemap Character Structure

From `ff7.h:1330-1370`:

```cpp
struct savemap_char {
    char id;
    char level;
    // ... fields ...
    char name[12];        // Offset 0x10 - character name
    char equipped_weapon;
    char equipped_armor;
    // ... more fields ...
};
```

### Name Buffer Operations

```cpp
void naming_screen_add_character(uint8_t char_code) {
    if (g_naming_state.name_cursor_pos >= NAME_MAX_CHARS) {
        return;  // Name full
    }

    g_naming_state.name_buffer[g_naming_state.name_cursor_pos] = char_code;
    g_naming_state.name_cursor_pos++;
}

void naming_screen_delete_character() {
    if (g_naming_state.name_cursor_pos > 0) {
        g_naming_state.name_cursor_pos--;
        g_naming_state.name_buffer[g_naming_state.name_cursor_pos] = 0xFF;
    }
}

void naming_screen_add_space() {
    naming_screen_add_character(0x3F);  // Ideographic space
}

void naming_screen_confirm_name() {
    // Copy name to savemap
    savemap_char* char_data = &ff7_externals.savemap->chars[g_naming_state.character_index];

    // Copy characters
    for (int i = 0; i < NAME_MAX_CHARS; i++) {
        if (g_naming_state.name_buffer[i] == 0x00) {
            char_data->name[i] = 0xFF;  // Terminate
        } else {
            char_data->name[i] = g_naming_state.name_buffer[i];
        }
    }

    // Pad remaining bytes with 0xFF
    for (int i = g_naming_state.name_cursor_pos; i < 12; i++) {
        char_data->name[i] = 0xFF;
    }

    // Mark as complete
    g_naming_state.is_active = false;
}

void naming_screen_set_default_name() {
    // Load default name for this character
    naming_screen_get_default_name(
        g_naming_state.character_index,
        g_naming_state.name_buffer
    );

    // Count characters to set cursor position
    g_naming_state.name_cursor_pos = 0;
    for (int i = 0; i < NAME_MAX_CHARS; i++) {
        if (g_naming_state.name_buffer[i] == 0xFF ||
            g_naming_state.name_buffer[i] == 0x00) {
            break;
        }
        g_naming_state.name_cursor_pos++;
    }
}
```

---

## Implementation Phases

### Phase 1: Basic Framework
**Goal:** Create file structure and verify hook triggers

**Tasks:**
1. Create `/mnt/c/FFNx/src/ff7/naming_screen.cpp`
2. Add declaration to `defs.h`
3. Replace `noop` with `ff7_naming_screen_jp` in `ff7_opengl.cpp`
4. Implement minimal function that logs when called
5. Build and test that hook triggers on naming screen

**Verification:**
- Launch game, start new game
- Check FFNx.log for naming screen function call
- Naming screen may be blank/broken at this stage

### Phase 2: Input Handling
**Goal:** Navigate cursor through all positions

**Tasks:**
1. Initialize state structure
2. Implement D-pad navigation with wrapping
3. Implement L1/R1 page switching
4. Implement sidebar entry/exit (left/right at edge)
5. Add input debouncing and repeat

**Verification:**
- D-pad moves cursor correctly
- L1/R1 switches pages
- Cursor wraps at grid edges
- Sidebar navigation works

### Phase 3: Character Grid Rendering
**Goal:** Display all three character pages correctly

**Tasks:**
1. Create all three character table arrays
2. Implement `naming_screen_draw_character_grid()`
3. Call from `ff7_naming_screen_jp()` draw phase
4. Verify characters render at correct positions

**Verification:**
- All characters visible on all three pages
- Characters align to grid properly
- Page switching shows different characters

### Phase 4: Sidebar Implementation
**Goal:** Functional sidebar with all options

**Tasks:**
1. Create sidebar label data
2. Implement sidebar rendering
3. Implement page switch actions (top 3 items)
4. Implement space/delete/confirm/default actions

**Verification:**
- Sidebar labels display correctly
- Selecting page item switches page
- All sidebar actions work

### Phase 5: Name Buffer Integration
**Goal:** Characters can be named and saved

**Tasks:**
1. Find character index from game context
2. Implement name buffer editing (add/delete)
3. Implement name preview display
4. Implement confirm (saves to savemap)
5. Implement default name loading

**Verification:**
- Selected characters appear in name preview
- Delete removes characters
- Confirm saves name correctly
- Default loads correct name for each character

### Phase 6: Cursor and Polish
**Goal:** Visual polish and edge cases

**Tasks:**
1. Implement animated hand cursor
2. Add cursor animation/blink
3. Test all 9 characters
4. Handle edge cases (empty name, etc.)
5. Verify no crashes or hangs

**Verification:**
- Cursor visible and animated
- All characters can be named
- No visual glitches
- Smooth user experience

---

## File Reference

### Critical Files for Implementation

| File | Purpose |
|------|---------|
| `/mnt/c/FFNx/src/ff7/japanese_text.cpp` | Character rendering reference |
| `/mnt/c/FFNx/src/ff7/defs.h` | Function declarations |
| `/mnt/c/FFNx/src/ff7_opengl.cpp` | Hook point (line 459) |
| `/mnt/c/FFNx/src/ff7.h` | Data structures |
| `/mnt/c/FFNx/src/ff7_data.h` | External resolution |
| `/mnt/c/FFNx/src/ff7/misc.cpp` | Input handling reference |

### Character Mapping Reference

| File | Purpose |
|------|---------|
| `/home/johnzealanddoyle/projects/tools/.project/naming_screen_tables.txt` | Byte mappings |
| `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/character_maps/ff7_complete_mapping_compact.csv` | Complete jafont map |

### Screenshots for Reference

| File | Shows |
|------|-------|
| `ff7_ja_aopoGnuHo1.png` | Japanese hiragana page |
| `ff7_ja_2EhqYWai6C.png` | Japanese katakana page |
| `ff7_ja_FzGaOmAFSm.png` | Japanese eisuu page |
| `ff7_en_lPjjBBCOlA.png` | English naming screen |

---

## Technical Notes

### Memory Addresses

| Description | File Offset | Virtual Address |
|-------------|-------------|-----------------|
| EN sidebar labels | 0x520748 | 0x921D48 |
| JA hiragana table | 0x521370 | 0x921F70 |
| JA katakana table | 0x521478 | 0x922078 |

### VA Calculation

```
VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000
```

### Build Command

```bash
cd /mnt/c/FFNx
powershell.exe -Command "C:\cmake-3.27.8\cmake-3.27.8-windows-x86_64\bin\cmake.exe --build .build --config Release"
```

### Testing Location

Start a new game and proceed to the first naming screen (Cloud).

---

## Open Questions

1. **Character Index**: Need to find how the game passes which character is being named. Check `name_menu_sub_6CBD32` for parameters or global state.

2. **Hand Cursor**: Find existing code that draws the finger cursor in menus. Check `field_submit_draw_pointer_hand` or similar functions.

3. **Default Names**: Need to verify where default character names come from. May be in kernel2 or hardcoded.

---

*End of Implementation Plan*
