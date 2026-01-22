# FF7 Language Selection Menu - Implementation Specification

**Document Version:** 1.0.0
**Created:** 2026-01-20 22:40:00 JST (Monday)
**Last Modified:** 2026-01-20 22:40:00 JST (Monday)
**Author:** Claude Code (Opus 4.5)
**Session-ID:** d585214a-2972-4f0c-8c26-b882c71cd253

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Technical Foundation](#3-technical-foundation)
4. [FFNx C++ Implementation](#4-ffnx-c-implementation)
5. [Hext Patch Specifications](#5-hext-patch-specifications)
6. [Asset Requirements](#6-asset-requirements)
7. [Configuration System](#7-configuration-system)
8. [Language Hot-Swapping](#8-language-hot-swapping)
9. [User Interface Design](#9-user-interface-design)
10. [Testing Strategy](#10-testing-strategy)
11. [Implementation Roadmap](#11-implementation-roadmap)
12. [Risk Assessment](#12-risk-assessment)
13. [Appendices](#13-appendices)

---

## 1. Executive Summary

### 1.1 Purpose

This specification defines the implementation of a runtime language selection menu for Final Fantasy VII PC, enabling players to switch between English, Japanese, German, French, and Spanish without restarting the game or manually swapping files.

### 1.2 Scope

| In Scope | Out of Scope |
|----------|--------------|
| Language menu UI rendering | Translation creation |
| FFNx hook integration | Voice acting support |
| Kernel.bin hot-swapping | FMV subtitle support |
| Field dialogue switching | Save file migration |
| Configuration persistence | Online features |
| Input handling | Other FF7 versions (PSX, Switch) |

### 1.3 Target Platforms

- FF7 PC 1998 (1.02 US English)
- FF7 Steam 2013 Edition
- FF7 eStore Edition (Square Enix)

### 1.4 Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| FFNx | 1.19.0+ | Hook system, rendering |
| 7th Heaven | 3.0+ | Optional mod distribution |
| BGFX | Bundled | Rendering backend |

---

## 2. Architecture Overview

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FF7.EXE (Game)                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Game Mode Dispatcher                       │   │
│  │                    (sub_4090E6)                               │   │
│  │  ┌─────────┬─────────┬─────────┬─────────┬─────────────────┐ │   │
│  │  │ Mode 0  │ Mode 1  │ Mode 3  │ Mode 5  │ Mode 0x1D (NEW) │ │   │
│  │  │ Title   │ Field   │ Battle  │ Menu    │ Language Menu   │ │   │
│  │  └────┬────┴────┬────┴────┬────┴────┬────┴────────┬────────┘ │   │
│  └───────┼─────────┼─────────┼─────────┼─────────────┼──────────┘   │
│          │         │         │         │             │              │
│          ▼         ▼         ▼         ▼             ▼              │
│      [Native]  [Native]  [Native]  [Native]    [FFNx Hook]         │
└──────────────────────────────────────────┬──────────────────────────┘
                                           │
                    ┌──────────────────────▼──────────────────────┐
                    │              FFNx.dll                        │
                    │  ┌────────────────────────────────────────┐ │
                    │  │         language_menu.cpp               │ │
                    │  │  • Render language selection UI         │ │
                    │  │  • Handle input (D-pad, confirm, cancel)│ │
                    │  │  • Trigger language hot-swap            │ │
                    │  └────────────────────────────────────────┘ │
                    │  ┌────────────────────────────────────────┐ │
                    │  │         language_manager.cpp            │ │
                    │  │  • Load kernel.bin variants             │ │
                    │  │  • Redirect field LGP paths             │ │
                    │  │  • Manage font texture switching        │ │
                    │  └────────────────────────────────────────┘ │
                    │  ┌────────────────────────────────────────┐ │
                    │  │         cfg.cpp (modified)              │ │
                    │  │  • current_language setting             │ │
                    │  │  • enable_language_menu setting         │ │
                    │  └────────────────────────────────────────┘ │
                    └─────────────────────────────────────────────┘
                                           │
                    ┌──────────────────────▼──────────────────────┐
                    │              FFNx.toml                       │
                    │  current_language = "en"                     │
                    │  enable_language_menu = true                 │
                    │  language_menu_hotkey = "F12"                │
                    └─────────────────────────────────────────────┘
```

### 2.2 Data Flow

```
[User Input] ──► [FFNx Input Handler] ──► [Language Menu State Machine]
                                                     │
                                          ┌──────────┴──────────┐
                                          ▼                     ▼
                                   [Selection Changed]    [Confirmed]
                                          │                     │
                                          ▼                     ▼
                                   [Update Cursor]      [Language Manager]
                                                               │
                                          ┌────────────────────┼────────────────────┐
                                          ▼                    ▼                    ▼
                                   [Swap Kernel.bin]    [Redirect Field LGP]  [Swap Font Textures]
                                          │                    │                    │
                                          └────────────────────┼────────────────────┘
                                                               ▼
                                                        [Save to FFNx.toml]
                                                               │
                                                               ▼
                                                        [Return to Title]
```

### 2.3 Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `language_menu.cpp` | UI rendering, input handling, state machine |
| `language_manager.cpp` | Asset loading, file redirection, hot-swapping |
| `cfg.cpp` | Configuration parsing and persistence |
| `ff7_opengl.cpp` | Hook installation, mode interception |
| Hext patches | Mode dispatcher hook, FFNx callback |

---

## 3. Technical Foundation

### 3.1 Game Mode System

**State Variable**: `word_CC0D84` (16-bit)

| Mode ID | Name | Entry Function | Description |
|---------|------|----------------|-------------|
| 0x00 | INIT/TITLE | `sub_408EBA` | Title screen, New Game/Continue |
| 0x01 | FIELD | `sub_60E542` | Field exploration |
| 0x02 | WORLD_MAP | `sub_41CB24` | World map |
| 0x03 | BATTLE | `sub_74BE09` | Combat |
| 0x05 | MENU | `sub_6CC89A` | Pause menu |
| 0x06 | CHOCOBO | `sub_650383` | Chocobo racing/breeding |
| 0x07 | CONDOR | - | Fort Condor minigame |
| 0x09 | SUBMARINE | `sub_5F4977` | Submarine minigame |
| 0x0B | SNOWBOARD | `sub_5E8E35`, `sub_722C86` | Snowboard minigame |
| 0x0C | CREDITS | `sub_4047D5`, `sub_4094B1` | End credits |
| 0x0D | GAMEOVER | `sub_40989D`, `sub_40B264` | Game over screen |
| 0x10 | COASTER | `sub_409320` | Roller coaster |
| 0x14 | HIGHWAY | `sub_6CC85A` | Motorcycle chase |
| 0x19 | UNKNOWN | `sub_4092BB` | Unknown |
| 0x1A | UNKNOWN | `sub_4064C0` | Unknown |
| **0x1D** | **LANGUAGE_MENU** | **NEW** | **Language selection (proposed)** |

### 3.2 Mode Dispatcher Analysis

**Function**: `sub_4090E6` at `0x4090E6` (2932 bytes)

```c
// Pseudocode reconstruction of mode dispatcher
void game_mode_dispatcher(game_obj* obj) {
    switch (game_mode) {  // word_CC0D84
        case 0x00: handle_title_screen(obj); break;
        case 0x01: handle_field(obj); break;
        case 0x02: handle_world_map(obj); break;
        case 0x03: handle_battle(obj); break;
        case 0x05: handle_menu(obj); break;
        // ... other modes ...
        case 0x0D: handle_gameover(obj); break;
        // We will inject case 0x1D here via Hext
        default: break;
    }
}
```

### 3.3 Menu System Internals

**Menu Initialization**: `sub_6CD3B0`

```c
// Pseudocode of menu init
void menu_system_init(game_obj* obj) {
    debug_print("START OF MENU SYSTEM!!!\n");

    // Set menu active flag
    dword_DC12DC = 1;

    // Initialize menu loading
    sub_6C1468(1);

    // Set window coordinates
    if (result == 0) {
        dword_DC105C = 0;      // X position
        dword_DC1060 = 0;      // Y position
        dword_DC1064 = 0x140;  // Width (320)
        dword_DC1068 = 0xF0;   // Height (240)
        dword_DC130C = 1;      // Window enabled
    }
    // ...
}
```

**Menu Window Variables**:

| Address | Name | Type | Description |
|---------|------|------|-------------|
| `0xDC105C` | menu_x | DWORD | Window X position |
| `0xDC1060` | menu_y | DWORD | Window Y position |
| `0xDC1064` | menu_width | DWORD | Window width (usually 320) |
| `0xDC1068` | menu_height | DWORD | Window height (usually 240) |
| `0xDC12DC` | menu_active | DWORD | Menu system active flag |
| `0xDC130C` | window_enabled | DWORD | Window rendering enabled |

### 3.4 Text Rendering System

**Character Drawing Function**: `sub_66E272` (881 bytes)

```c
// Pseudocode of character drawing
void draw_character(void* context, font_params* params) {
    if (params == NULL) return;

    // Get texture set from params
    texture_set* tex = params->texture_set;  // offset 0x30

    // Calculate UV coordinates based on character index
    // Apply color if specified
    // Submit to rendering pipeline

    // Uses font_info table at 0x99DDA8 for character widths
}
```

**Font Info Table**: `0x99DDA8`
- 256 bytes of character width data
- Used by text rendering to calculate horizontal spacing

---

## 4. FFNx C++ Implementation

### 4.1 New Source Files

#### 4.1.1 `src/ff7/language_menu.h`

```cpp
// src/ff7/language_menu.h
#ifndef FF7_LANGUAGE_MENU_H
#define FF7_LANGUAGE_MENU_H

#include <stdint.h>
#include <string>
#include <vector>

namespace ff7 {
namespace language_menu {

// Language identifiers
enum class Language : uint8_t {
    ENGLISH = 0,
    JAPANESE = 1,
    GERMAN = 2,
    FRENCH = 3,
    SPANISH = 4,
    COUNT = 5
};

// Menu state
enum class MenuState : uint8_t {
    INACTIVE = 0,
    FADE_IN = 1,
    ACTIVE = 2,
    FADE_OUT = 3,
    APPLYING = 4
};

// Language metadata
struct LanguageInfo {
    Language id;
    const char* code;           // "en", "ja", "de", "fr", "es"
    const char* display_name;   // "English", "日本語", etc.
    const char* kernel_path;    // "lang-en/kernel/KERNEL.BIN"
    const char* field_lgp;      // "lang-en/field/flevel.lgp"
    const char* font_prefix;    // "usfont" or "jafont"
    bool requires_extended_font; // True for Japanese
};

// Configuration
struct MenuConfig {
    bool enabled;
    std::string hotkey;
    int fade_duration_ms;
    int menu_x;
    int menu_y;
    int menu_width;
    int menu_height;
};

// Public API
void init();
void shutdown();
void update(float delta_time);
void render();

bool is_active();
void show();
void hide();

Language get_current_language();
void set_current_language(Language lang);

const LanguageInfo& get_language_info(Language lang);

// Called by FFNx hook system
void on_mode_enter();
void on_mode_exit();
bool handle_input();

// Internal state access (for debugging)
MenuState get_state();

} // namespace language_menu
} // namespace ff7

#endif // FF7_LANGUAGE_MENU_H
```

#### 4.1.2 `src/ff7/language_menu.cpp`

```cpp
// src/ff7/language_menu.cpp
#include "language_menu.h"
#include "../cfg.h"
#include "../log.h"
#include "../input.h"
#include "../renderer.h"
#include "language_manager.h"

#include <bgfx/bgfx.h>
#include <bx/math.h>

namespace ff7 {
namespace language_menu {

// ============================================================================
// Static Data
// ============================================================================

static const LanguageInfo LANGUAGES[static_cast<int>(Language::COUNT)] = {
    {
        Language::ENGLISH,
        "en",
        "English",
        "lang-en/kernel/KERNEL.BIN",
        "lang-en/field/flevel.lgp",
        "usfont",
        false
    },
    {
        Language::JAPANESE,
        "ja",
        "\x93\xFA\x96\x7B\x8C\xEA",  // "日本語" in Shift-JIS
        "lang-ja/kernel/KERNEL.BIN",
        "lang-ja/field/jflevel.lgp",
        "jafont",
        true
    },
    {
        Language::GERMAN,
        "de",
        "Deutsch",
        "lang-de/kernel/KERNEL.BIN",
        "lang-de/field/flevel.lgp",
        "usfont",
        false
    },
    {
        Language::FRENCH,
        "fr",
        "Fran\xE7""ais",  // "Français"
        "lang-fr/kernel/KERNEL.BIN",
        "lang-fr/field/flevel.lgp",
        "usfont",
        false
    },
    {
        Language::SPANISH,
        "es",
        "Espa\xF1ol",  // "Español"
        "lang-es/kernel/KERNEL.BIN",
        "lang-es/field/flevel.lgp",
        "usfont",
        false
    }
};

// ============================================================================
// Internal State
// ============================================================================

static struct {
    MenuState state = MenuState::INACTIVE;
    Language current_language = Language::ENGLISH;
    Language selected_language = Language::ENGLISH;
    int cursor_index = 0;
    float fade_alpha = 0.0f;
    float fade_timer = 0.0f;
    bool initialized = false;

    // Rendering resources
    bgfx::ProgramHandle shader_program = BGFX_INVALID_HANDLE;
    bgfx::UniformHandle u_color = BGFX_INVALID_HANDLE;
    bgfx::TextureHandle menu_texture = BGFX_INVALID_HANDLE;

    // Configuration
    MenuConfig config;
} s_state;

// ============================================================================
// Forward Declarations
// ============================================================================

static void render_background();
static void render_menu_box(int x, int y, int width, int height, float alpha);
static void render_text(const char* text, int x, int y, uint32_t color, float alpha);
static void render_cursor(int x, int y, float alpha);
static void process_input();
static void apply_language_change();
static void start_fade_in();
static void start_fade_out();

// ============================================================================
// Public API Implementation
// ============================================================================

void init() {
    if (s_state.initialized) return;

    ffnx_info("Language Menu: Initializing...\n");

    // Load configuration
    s_state.config.enabled = language_menu_enabled;
    s_state.config.hotkey = language_menu_hotkey;
    s_state.config.fade_duration_ms = 300;
    s_state.config.menu_x = 80;
    s_state.config.menu_y = 60;
    s_state.config.menu_width = 160;
    s_state.config.menu_height = 120;

    // Load current language from config
    std::string lang_code = current_language_setting;
    for (int i = 0; i < static_cast<int>(Language::COUNT); i++) {
        if (lang_code == LANGUAGES[i].code) {
            s_state.current_language = static_cast<Language>(i);
            s_state.selected_language = s_state.current_language;
            s_state.cursor_index = i;
            break;
        }
    }

    // Initialize rendering resources
    // Note: Actual shader loading would depend on FFNx's shader system

    s_state.initialized = true;
    ffnx_info("Language Menu: Initialized. Current language: %s\n",
              LANGUAGES[static_cast<int>(s_state.current_language)].display_name);
}

void shutdown() {
    if (!s_state.initialized) return;

    ffnx_info("Language Menu: Shutting down...\n");

    // Release rendering resources
    if (bgfx::isValid(s_state.shader_program)) {
        bgfx::destroy(s_state.shader_program);
    }
    if (bgfx::isValid(s_state.u_color)) {
        bgfx::destroy(s_state.u_color);
    }
    if (bgfx::isValid(s_state.menu_texture)) {
        bgfx::destroy(s_state.menu_texture);
    }

    s_state.initialized = false;
}

void update(float delta_time) {
    if (!s_state.initialized || !s_state.config.enabled) return;

    switch (s_state.state) {
        case MenuState::INACTIVE:
            // Check for hotkey to activate
            break;

        case MenuState::FADE_IN:
            s_state.fade_timer += delta_time;
            s_state.fade_alpha = s_state.fade_timer / (s_state.config.fade_duration_ms / 1000.0f);
            if (s_state.fade_alpha >= 1.0f) {
                s_state.fade_alpha = 1.0f;
                s_state.state = MenuState::ACTIVE;
            }
            break;

        case MenuState::ACTIVE:
            process_input();
            break;

        case MenuState::FADE_OUT:
            s_state.fade_timer += delta_time;
            s_state.fade_alpha = 1.0f - (s_state.fade_timer / (s_state.config.fade_duration_ms / 1000.0f));
            if (s_state.fade_alpha <= 0.0f) {
                s_state.fade_alpha = 0.0f;
                s_state.state = MenuState::INACTIVE;
            }
            break;

        case MenuState::APPLYING:
            // Language change is being applied
            apply_language_change();
            start_fade_out();
            break;
    }
}

void render() {
    if (!s_state.initialized || s_state.state == MenuState::INACTIVE) return;

    float alpha = s_state.fade_alpha;

    // Render semi-transparent background overlay
    render_background();

    // Render menu box
    render_menu_box(
        s_state.config.menu_x,
        s_state.config.menu_y,
        s_state.config.menu_width,
        s_state.config.menu_height,
        alpha
    );

    // Render title
    render_text("Select Language",
                s_state.config.menu_x + 20,
                s_state.config.menu_y + 10,
                0xFFFFFFFF,
                alpha);

    // Render language options
    int y_offset = s_state.config.menu_y + 35;
    for (int i = 0; i < static_cast<int>(Language::COUNT); i++) {
        uint32_t color = (i == s_state.cursor_index) ? 0xFFFFFF00 : 0xFFFFFFFF;

        render_text(LANGUAGES[i].display_name,
                    s_state.config.menu_x + 40,
                    y_offset,
                    color,
                    alpha);

        // Render cursor if this is selected
        if (i == s_state.cursor_index) {
            render_cursor(s_state.config.menu_x + 25, y_offset, alpha);
        }

        y_offset += 16;
    }

    // Render instructions
    render_text("[OK] Confirm  [Cancel] Back",
                s_state.config.menu_x + 10,
                s_state.config.menu_y + s_state.config.menu_height - 20,
                0xFF888888,
                alpha);
}

bool is_active() {
    return s_state.state != MenuState::INACTIVE;
}

void show() {
    if (s_state.state != MenuState::INACTIVE) return;

    ffnx_info("Language Menu: Opening...\n");
    s_state.selected_language = s_state.current_language;
    s_state.cursor_index = static_cast<int>(s_state.current_language);
    start_fade_in();
}

void hide() {
    if (s_state.state == MenuState::INACTIVE) return;

    ffnx_info("Language Menu: Closing...\n");
    start_fade_out();
}

Language get_current_language() {
    return s_state.current_language;
}

void set_current_language(Language lang) {
    if (lang >= Language::COUNT) return;

    s_state.current_language = lang;
    s_state.selected_language = lang;
    s_state.cursor_index = static_cast<int>(lang);

    ffnx_info("Language Menu: Set current language to %s\n",
              LANGUAGES[static_cast<int>(lang)].display_name);
}

const LanguageInfo& get_language_info(Language lang) {
    return LANGUAGES[static_cast<int>(lang)];
}

void on_mode_enter() {
    ffnx_info("Language Menu: Mode entered (0x1D)\n");
    show();
}

void on_mode_exit() {
    ffnx_info("Language Menu: Mode exited\n");
    s_state.state = MenuState::INACTIVE;
    s_state.fade_alpha = 0.0f;
}

bool handle_input() {
    if (s_state.state != MenuState::ACTIVE) return false;

    // Return true if input was consumed
    return true;
}

MenuState get_state() {
    return s_state.state;
}

// ============================================================================
// Internal Implementation
// ============================================================================

static void render_background() {
    // Render a semi-transparent black overlay
    // This dims the background while the menu is visible

    // Use BGFX to draw a fullscreen quad with alpha
    // Implementation depends on FFNx's rendering setup
}

static void render_menu_box(int x, int y, int width, int height, float alpha) {
    // Render the FF7-style menu box with borders
    // Blue gradient background with lighter borders

    // Box colors (FF7 style)
    uint32_t bg_color = 0x000040;      // Dark blue
    uint32_t border_color = 0x4080C0;  // Light blue border

    // Apply alpha
    uint8_t a = static_cast<uint8_t>(alpha * 200);  // Slightly transparent

    // Draw background quad
    // Draw border lines
    // Implementation using BGFX primitives
}

static void render_text(const char* text, int x, int y, uint32_t color, float alpha) {
    // Render text using FFNx's text rendering system
    // This should use the game's font textures for consistency

    // Apply alpha to color
    uint8_t a = static_cast<uint8_t>(((color >> 24) & 0xFF) * alpha);
    uint32_t final_color = (a << 24) | (color & 0x00FFFFFF);

    // Use FFNx's text rendering function
    // ff7_draw_text(text, x, y, final_color);
}

static void render_cursor(int x, int y, float alpha) {
    // Render the selection cursor (hand pointer or arrow)
    // Could use a texture or draw with primitives

    // Simple triangle cursor
    // ▶ pointing right
}

static void process_input() {
    // Read game controller/keyboard input
    // FFNx provides input abstraction

    // Up pressed?
    if (ff7_input_is_pressed(FF7_INPUT_UP)) {
        s_state.cursor_index--;
        if (s_state.cursor_index < 0) {
            s_state.cursor_index = static_cast<int>(Language::COUNT) - 1;
        }
        s_state.selected_language = static_cast<Language>(s_state.cursor_index);
        // Play cursor move sound
        ff7_play_sound(FF7_SOUND_CURSOR);
    }

    // Down pressed?
    if (ff7_input_is_pressed(FF7_INPUT_DOWN)) {
        s_state.cursor_index++;
        if (s_state.cursor_index >= static_cast<int>(Language::COUNT)) {
            s_state.cursor_index = 0;
        }
        s_state.selected_language = static_cast<Language>(s_state.cursor_index);
        // Play cursor move sound
        ff7_play_sound(FF7_SOUND_CURSOR);
    }

    // Confirm pressed?
    if (ff7_input_is_pressed(FF7_INPUT_CONFIRM)) {
        if (s_state.selected_language != s_state.current_language) {
            ffnx_info("Language Menu: Confirmed selection: %s\n",
                      LANGUAGES[s_state.cursor_index].display_name);
            // Play confirm sound
            ff7_play_sound(FF7_SOUND_CONFIRM);
            s_state.state = MenuState::APPLYING;
        } else {
            // Same language, just close
            ff7_play_sound(FF7_SOUND_CONFIRM);
            start_fade_out();
        }
    }

    // Cancel pressed?
    if (ff7_input_is_pressed(FF7_INPUT_CANCEL)) {
        ffnx_info("Language Menu: Cancelled\n");
        // Play cancel sound
        ff7_play_sound(FF7_SOUND_CANCEL);
        // Reset selection to current
        s_state.selected_language = s_state.current_language;
        s_state.cursor_index = static_cast<int>(s_state.current_language);
        start_fade_out();
    }
}

static void apply_language_change() {
    Language new_lang = s_state.selected_language;
    const LanguageInfo& info = LANGUAGES[static_cast<int>(new_lang)];

    ffnx_info("Language Menu: Applying language change to %s\n", info.display_name);

    // Update internal state
    s_state.current_language = new_lang;

    // Notify language manager to perform the actual swap
    language_manager::set_language(new_lang);

    // Save to configuration
    current_language_setting = info.code;
    save_cfg();

    ffnx_info("Language Menu: Language change complete\n");
}

static void start_fade_in() {
    s_state.state = MenuState::FADE_IN;
    s_state.fade_timer = 0.0f;
    s_state.fade_alpha = 0.0f;
}

static void start_fade_out() {
    s_state.state = MenuState::FADE_OUT;
    s_state.fade_timer = 0.0f;
    // fade_alpha stays at current value
}

} // namespace language_menu
} // namespace ff7
```

#### 4.1.3 `src/ff7/language_manager.h`

```cpp
// src/ff7/language_manager.h
#ifndef FF7_LANGUAGE_MANAGER_H
#define FF7_LANGUAGE_MANAGER_H

#include "language_menu.h"
#include <string>

namespace ff7 {
namespace language_manager {

// Initialize the language manager
void init();

// Shutdown and cleanup
void shutdown();

// Set the current language (triggers hot-swap)
void set_language(language_menu::Language lang);

// Get current language
language_menu::Language get_language();

// File redirection
std::string redirect_kernel_path(const std::string& original_path);
std::string redirect_field_path(const std::string& original_path);
std::string redirect_font_path(const std::string& original_path);

// Check if a language's assets are available
bool is_language_available(language_menu::Language lang);

// Reload assets for current language
void reload_assets();

// Hot-swap specific components
void swap_kernel();
void swap_field_lgp();
void swap_fonts();

} // namespace language_manager
} // namespace ff7

#endif // FF7_LANGUAGE_MANAGER_H
```

#### 4.1.4 `src/ff7/language_manager.cpp`

```cpp
// src/ff7/language_manager.cpp
#include "language_manager.h"
#include "language_menu.h"
#include "../cfg.h"
#include "../log.h"
#include "../redirect.h"

#include <filesystem>
#include <map>

namespace fs = std::filesystem;

namespace ff7 {
namespace language_manager {

// ============================================================================
// Internal State
// ============================================================================

static struct {
    language_menu::Language current_language = language_menu::Language::ENGLISH;
    bool initialized = false;

    // Cached paths
    std::string base_path;
    std::map<language_menu::Language, bool> available_languages;
} s_state;

// ============================================================================
// Forward Declarations
// ============================================================================

static void scan_available_languages();
static std::string get_language_base_path(language_menu::Language lang);

// ============================================================================
// Public API Implementation
// ============================================================================

void init() {
    if (s_state.initialized) return;

    ffnx_info("Language Manager: Initializing...\n");

    // Determine base path (game directory)
    s_state.base_path = get_game_directory();

    // Scan for available language packs
    scan_available_languages();

    // Log available languages
    ffnx_info("Language Manager: Available languages:\n");
    for (int i = 0; i < static_cast<int>(language_menu::Language::COUNT); i++) {
        auto lang = static_cast<language_menu::Language>(i);
        const auto& info = language_menu::get_language_info(lang);
        bool available = s_state.available_languages[lang];
        ffnx_info("  %s (%s): %s\n",
                  info.display_name,
                  info.code,
                  available ? "Available" : "Not Found");
    }

    s_state.initialized = true;
}

void shutdown() {
    if (!s_state.initialized) return;

    ffnx_info("Language Manager: Shutting down...\n");
    s_state.initialized = false;
}

void set_language(language_menu::Language lang) {
    if (!s_state.initialized) return;
    if (lang == s_state.current_language) return;
    if (!is_language_available(lang)) {
        ffnx_error("Language Manager: Language %s not available!\n",
                   language_menu::get_language_info(lang).code);
        return;
    }

    const auto& info = language_menu::get_language_info(lang);
    ffnx_info("Language Manager: Switching to %s...\n", info.display_name);

    s_state.current_language = lang;

    // Perform hot-swap of assets
    swap_kernel();
    swap_field_lgp();
    swap_fonts();

    ffnx_info("Language Manager: Language switch complete\n");
}

language_menu::Language get_language() {
    return s_state.current_language;
}

std::string redirect_kernel_path(const std::string& original_path) {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    // Check if this is a kernel file request
    if (original_path.find("kernel") != std::string::npos ||
        original_path.find("KERNEL") != std::string::npos) {

        std::string redirected = s_state.base_path + "/" + info.kernel_path;

        if (fs::exists(redirected)) {
            ffnx_trace("Language Manager: Redirecting %s -> %s\n",
                       original_path.c_str(), redirected.c_str());
            return redirected;
        }
    }

    return original_path;  // No redirection
}

std::string redirect_field_path(const std::string& original_path) {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    // Check if this is a field LGP request
    if (original_path.find("flevel") != std::string::npos ||
        original_path.find("FLEVEL") != std::string::npos) {

        std::string redirected = s_state.base_path + "/" + info.field_lgp;

        if (fs::exists(redirected)) {
            ffnx_trace("Language Manager: Redirecting %s -> %s\n",
                       original_path.c_str(), redirected.c_str());
            return redirected;
        }
    }

    return original_path;
}

std::string redirect_font_path(const std::string& original_path) {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    // Check if this is a font texture request
    if (original_path.find("font") != std::string::npos) {
        // Replace font prefix
        std::string redirected = original_path;

        // Replace usfont with jafont for Japanese, etc.
        size_t pos = redirected.find("usfont");
        if (pos != std::string::npos && info.requires_extended_font) {
            redirected.replace(pos, 6, info.font_prefix);
        }

        if (redirected != original_path) {
            ffnx_trace("Language Manager: Redirecting font %s -> %s\n",
                       original_path.c_str(), redirected.c_str());
        }

        return redirected;
    }

    return original_path;
}

bool is_language_available(language_menu::Language lang) {
    auto it = s_state.available_languages.find(lang);
    return it != s_state.available_languages.end() && it->second;
}

void reload_assets() {
    ffnx_info("Language Manager: Reloading assets for %s\n",
              language_menu::get_language_info(s_state.current_language).display_name);

    swap_kernel();
    swap_field_lgp();
    swap_fonts();
}

void swap_kernel() {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    ffnx_info("Language Manager: Swapping kernel to %s\n", info.kernel_path);

    // The kernel contains:
    // - Item names and descriptions
    // - Materia names and descriptions
    // - Command names
    // - Character default names
    // - System messages

    // FFNx needs to either:
    // 1. Reload the kernel data structures in memory
    // 2. Or redirect file reads to the new kernel.bin

    // Option 2 is simpler - set up file redirection
    // The game will read from the redirected path automatically

    // For immediate effect, we may need to trigger a kernel reload
    // This depends on when the game reads kernel data

    // TODO: Implement kernel memory reload if needed for immediate effect
}

void swap_field_lgp() {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    ffnx_info("Language Manager: Swapping field LGP to %s\n", info.field_lgp);

    // The field LGP contains:
    // - Field dialogue scripts
    // - Field background text

    // File redirection handles this automatically
    // New field loads will use the redirected LGP

    // Note: Current field dialogue won't change until scene transition
}

void swap_fonts() {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    ffnx_info("Language Manager: Swapping fonts (prefix: %s, extended: %s)\n",
              info.font_prefix,
              info.requires_extended_font ? "yes" : "no");

    // For Japanese, need to:
    // 1. Load all 6 jafont textures
    // 2. Update character width table
    // 3. Enable FA-FE page marker parsing

    if (info.requires_extended_font) {
        // Enable Japanese font mode
        font_language = "ja";

        // Patch character widths for fixed-width Japanese
        // (Handled by PatchFontWidthsForJapanese in FFNx)
    } else {
        // Standard Western font
        font_language = "en";

        // Restore variable-width character widths
        // TODO: Implement width table restoration
    }

    // Trigger font texture reload
    // TODO: Implement font texture hot-reload
}

// ============================================================================
// Internal Implementation
// ============================================================================

static void scan_available_languages() {
    ffnx_info("Language Manager: Scanning for language packs...\n");

    for (int i = 0; i < static_cast<int>(language_menu::Language::COUNT); i++) {
        auto lang = static_cast<language_menu::Language>(i);
        const auto& info = language_menu::get_language_info(lang);

        // Check if kernel exists
        std::string kernel_path = s_state.base_path + "/" + info.kernel_path;
        bool available = fs::exists(kernel_path);

        s_state.available_languages[lang] = available;

        if (available) {
            ffnx_trace("Language Manager: Found %s at %s\n",
                       info.code, kernel_path.c_str());
        }
    }
}

static std::string get_language_base_path(language_menu::Language lang) {
    const auto& info = language_menu::get_language_info(lang);
    return s_state.base_path + "/lang-" + info.code;
}

} // namespace language_manager
} // namespace ff7
```

### 4.2 Modifications to Existing Files

#### 4.2.1 `src/cfg.h` Additions

```cpp
// Add to src/cfg.h

// Language menu configuration
extern bool language_menu_enabled;
extern std::string language_menu_hotkey;
extern std::string current_language_setting;
```

#### 4.2.2 `src/cfg.cpp` Additions

```cpp
// Add to src/cfg.cpp

bool language_menu_enabled = false;
std::string language_menu_hotkey = "F12";
std::string current_language_setting = "en";

// In read_cfg() function:
void read_cfg() {
    // ... existing code ...

    // Language menu settings
    language_menu_enabled = config["enable_language_menu"].value_or(false);
    language_menu_hotkey = config["language_menu_hotkey"].value_or("F12");
    current_language_setting = config["current_language"].value_or("en");

    ffnx_info("Language menu: %s (hotkey: %s, current: %s)\n",
              language_menu_enabled ? "enabled" : "disabled",
              language_menu_hotkey.c_str(),
              current_language_setting.c_str());
}

// In save_cfg() function (if exists, or create):
void save_cfg() {
    // Update FFNx.toml with current settings
    // This is called when language is changed

    toml::table config = toml::parse_file("FFNx.toml");
    config.insert_or_assign("current_language", current_language_setting);

    std::ofstream file("FFNx.toml");
    file << config;
}
```

#### 4.2.3 `src/ff7_opengl.cpp` Additions

```cpp
// Add to src/ff7_opengl.cpp

#include "ff7/language_menu.h"
#include "ff7/language_manager.h"

// Game mode constant for our language menu
#define FF7_MODE_LANGUAGE_MENU 0x1D

// Pointer to game mode variable
static uint16_t* game_mode_ptr = nullptr;

// Hook for mode dispatcher
void language_menu_mode_handler(struct game_obj* game_object) {
    // Called when game is in mode 0x1D

    // Initialize on first entry
    static bool first_entry = true;
    if (first_entry) {
        ff7::language_menu::on_mode_enter();
        first_entry = false;
    }

    // Update menu
    ff7::language_menu::update(1.0f / 60.0f);  // Assuming 60 FPS

    // Render menu
    ff7::language_menu::render();

    // Check if menu closed
    if (!ff7::language_menu::is_active()) {
        // Return to title screen
        *game_mode_ptr = 0;
        ff7::language_menu::on_mode_exit();
        first_entry = true;
    }
}

// In ff7_init_hooks():
void ff7_init_hooks(struct game_obj* game_object) {
    // ... existing hook code ...

    // Initialize language systems
    if (language_menu_enabled) {
        ff7::language_menu::init();
        ff7::language_manager::init();

        // Store pointer to game mode variable
        game_mode_ptr = (uint16_t*)0xCC0D84;

        // Install mode handler hook via Hext
        // The Hext patch will call our handler when mode == 0x1D

        ffnx_info("Language menu hooks installed\n");
    }

    // ... rest of existing code ...
}
```

### 4.3 Build System Updates

#### 4.3.1 `CMakeLists.txt` Additions

```cmake
# Add to CMakeLists.txt source list

set(FF7_SOURCES
    # ... existing sources ...
    src/ff7/language_menu.cpp
    src/ff7/language_manager.cpp
)
```

---

## 5. Hext Patch Specifications

### 5.1 Mode Dispatcher Hook

**File**: `misc/hext/ff7/en/FFNx.LANGUAGE_MENU.txt`

```hext
# FFNx Language Menu Mode Hook
# Adds support for game mode 0x1D (Language Selection Menu)
#
# This patch hooks into the game mode dispatcher (sub_4090E6)
# to recognize our custom mode ID and call FFNx's handler.
#
# Target: FF7 PC English 1.02
# Author: Claude Code
# Version: 1.0.0

# ============================================================================
# APPROACH: Hook the mode dispatcher's switch statement
# ============================================================================
#
# The mode dispatcher at sub_4090E6 uses a series of CMP/JZ instructions
# to handle different game modes. We need to add our check at the beginning
# or find an unused code path.
#
# Strategy: Hook early in the dispatcher, check for mode 0x1D, jump to FFNx
# ============================================================================

# Find a suitable injection point after the function prologue
# sub_4090E6 starts with: push ebp / mov ebp, esp / sub esp, ...

# We'll patch at the beginning of the actual mode checking logic
# After local variable setup, before first mode comparison

# Base address of mode dispatcher function
+0x4090E6

# Skip prologue (approximately 0x20 bytes of setup)
+0x20

# Original code here does mode checks
# We need to insert: CMP word ptr [CC0D84], 1Dh / JZ to_ffnx_handler

# ============================================================================
# INJECTION SITE ANALYSIS NEEDED
# ============================================================================
#
# The exact bytes to patch depend on the original instructions at this location.
# We need to:
# 1. Save the original bytes we're overwriting
# 2. Write a JMP to our code cave or inline our check
# 3. Our check jumps to FFNx handler if mode == 0x1D
# 4. Otherwise execute original code and continue
#
# Since code caves are limited, we should use FFNx's trampoline system instead.
# FFNx can hook this function directly in C++ using replace_function().
# ============================================================================

# ALTERNATIVE: Use FFNx's hook system instead of Hext
# This is documented below as the recommended approach
```

### 5.2 Recommended: FFNx Function Hook (Instead of Hext)

Since code caves are limited, the recommended approach is to use FFNx's existing hook system:

```cpp
// In src/ff7_opengl.cpp

// Original function pointer
static void (*original_mode_dispatcher)(struct game_obj*) = nullptr;

// Our wrapper
void hooked_mode_dispatcher(struct game_obj* game_object) {
    // Check if we're in language menu mode
    uint16_t mode = *(uint16_t*)0xCC0D84;

    if (mode == 0x1D && language_menu_enabled) {
        // Handle language menu mode
        language_menu_mode_handler(game_object);
        return;
    }

    // Call original dispatcher for all other modes
    original_mode_dispatcher(game_object);
}

// In ff7_init_hooks():
void ff7_init_hooks(struct game_obj* game_object) {
    // ... existing code ...

    if (language_menu_enabled) {
        // Hook mode dispatcher
        original_mode_dispatcher = (void(*)(struct game_obj*))0x4090E6;
        replace_function(0x4090E6, (void*)hooked_mode_dispatcher);

        ffnx_info("Mode dispatcher hooked for language menu\n");
    }
}
```

### 5.3 Title Screen Hook (Alternative Entry Point)

**File**: `misc/hext/ff7/en/FFNx.LANGUAGE_HOTKEY.txt`

```hext
# FFNx Language Menu Hotkey Hook
# Allows F12 (or configured key) to open language menu from title screen
#
# This is an ALTERNATIVE to adding a new mode - instead we overlay
# the language menu on top of the title screen when hotkey is pressed.
#
# Target: FF7 PC English 1.02

# ============================================================================
# This approach overlays the menu rather than creating a new mode.
# Simpler but less integrated with the game's state machine.
# ============================================================================

# No Hext patches needed for this approach.
# FFNx handles the hotkey via its input system.
```

### 5.4 Hotkey Implementation

```cpp
// In src/input.cpp

void process_hotkeys() {
    // ... existing hotkey processing ...

    // Language menu hotkey
    if (language_menu_enabled) {
        // Check if configured hotkey is pressed
        if (is_hotkey_pressed(language_menu_hotkey)) {
            // Only allow in title screen or field
            uint16_t mode = *(uint16_t*)0xCC0D84;

            if (mode == 0x00 || mode == 0x01) {  // Title or Field
                if (!ff7::language_menu::is_active()) {
                    ff7::language_menu::show();
                    ffnx_info("Language menu opened via hotkey\n");
                }
            }
        }
    }
}
```

---

## 6. Asset Requirements

### 6.1 Directory Structure

```
FF7/
├── ff7.exe
├── FFNx.dll (AF3DN.P)
├── FFNx.toml
├── FFNx.log
│
├── lang-en/                          # English (default)
│   ├── kernel/
│   │   ├── KERNEL.BIN               # Core game data
│   │   └── kernel2.bin              # Extended data
│   └── field/
│       └── flevel.lgp               # Field dialogues
│
├── lang-ja/                          # Japanese
│   ├── kernel/
│   │   ├── KERNEL.BIN
│   │   └── kernel2.bin
│   ├── field/
│   │   └── jflevel.lgp              # Japanese field dialogues
│   └── menu/                         # Optional: menu textures
│       └── *.tex
│
├── lang-de/                          # German
│   ├── kernel/
│   │   ├── KERNEL.BIN
│   │   └── kernel2.bin
│   └── field/
│       └── flevel.lgp
│
├── lang-fr/                          # French
│   ├── kernel/
│   │   ├── KERNEL.BIN
│   │   └── kernel2.bin
│   └── field/
│       └── flevel.lgp
│
├── lang-es/                          # Spanish
│   ├── kernel/
│   │   ├── KERNEL.BIN
│   │   └── kernel2.bin
│   └── field/
│       └── flevel.lgp
│
└── mods/
    └── Textures/
        └── menu/
            ├── jafont_1.png         # Japanese font page 1
            ├── jafont_2.png         # Japanese font page 2
            ├── jafont_3.png         # Japanese font page 3
            ├── jafont_4.png         # Japanese font page 4
            ├── jafont_5.png         # Japanese font page 5
            └── jafont_6.png         # Japanese font page 6
```

### 6.2 Asset Sources

| Language | Kernel Source | Field Source | Notes |
|----------|---------------|--------------|-------|
| English | FF7 PC 1.02 | FF7 PC 1.02 | Default installation |
| Japanese | FF7 International | PSX extraction | Requires conversion |
| German | FF7 PC German | FF7 PC German | Direct copy |
| French | FF7 PC French | FF7 PC French | Direct copy |
| Spanish | FF7 PC Spanish | FF7 PC Spanish | Direct copy |

### 6.3 Font Requirements

| Language | Font Files | Pages | Character Set |
|----------|------------|-------|---------------|
| English | usfont_*.tex | 2 | ASCII + Extended Latin |
| Japanese | jafont_*.tex | 6 | Hiragana + Katakana + Kanji |
| German | usfont_*.tex | 2 | ASCII + Umlauts |
| French | usfont_*.tex | 2 | ASCII + Accents |
| Spanish | usfont_*.tex | 2 | ASCII + Ñ + Accents |

---

## 7. Configuration System

### 7.1 FFNx.toml Additions

```toml
# =============================================================================
# Language Selection Settings
# =============================================================================

# Enable the language selection menu
# When enabled, press the configured hotkey to open the language menu
enable_language_menu = true

# Hotkey to open language menu (from title screen or field)
# Valid values: F1-F12, or key combinations like "Ctrl+L"
language_menu_hotkey = "F12"

# Current language setting
# Valid values: "en", "ja", "de", "fr", "es"
# This is automatically updated when you select a language in the menu
current_language = "en"

# Language asset paths (relative to game directory)
# These can be customized if your language files are in different locations
[language_paths]
en_kernel = "lang-en/kernel"
en_field = "lang-en/field"
ja_kernel = "lang-ja/kernel"
ja_field = "lang-ja/field"
de_kernel = "lang-de/kernel"
de_field = "lang-de/field"
fr_kernel = "lang-fr/kernel"
fr_field = "lang-fr/field"
es_kernel = "lang-es/kernel"
es_field = "lang-es/field"
```

### 7.2 Configuration Validation

```cpp
// In language_manager.cpp

bool validate_language_config(language_menu::Language lang) {
    const auto& info = language_menu::get_language_info(lang);

    // Check kernel exists
    std::string kernel_path = base_path + "/" + info.kernel_path;
    if (!fs::exists(kernel_path)) {
        ffnx_error("Language %s: kernel not found at %s\n",
                   info.code, kernel_path.c_str());
        return false;
    }

    // Check field LGP exists
    std::string field_path = base_path + "/" + info.field_lgp;
    if (!fs::exists(field_path)) {
        ffnx_warning("Language %s: field LGP not found at %s\n",
                     info.code, field_path.c_str());
        // Warning only - field dialogue may be in default location
    }

    // For Japanese, check font textures
    if (info.requires_extended_font) {
        for (int i = 1; i <= 6; i++) {
            std::string font_path = base_path + "/mods/Textures/menu/jafont_"
                                    + std::to_string(i) + ".png";
            if (!fs::exists(font_path)) {
                ffnx_error("Language %s: font page %d not found at %s\n",
                           info.code, i, font_path.c_str());
                return false;
            }
        }
    }

    return true;
}
```

---

## 8. Language Hot-Swapping

### 8.1 Hot-Swap Sequence

```
[User Confirms Language Selection]
          │
          ▼
[1. Save Selection to FFNx.toml]
          │
          ▼
[2. Update Internal State]
          │
          ▼
[3. Redirect File Paths]
    ├── Kernel path → lang-XX/kernel/
    ├── Field path → lang-XX/field/
    └── Font path → jafont/usfont
          │
          ▼
[4. Reload Active Assets]
    ├── Kernel: Already loaded, schedule reload on next kernel access
    ├── Field: Next scene transition loads new dialogue
    └── Fonts: Trigger texture reload
          │
          ▼
[5. Update Font Mode]
    ├── Japanese: Enable FA-FE parsing, fixed widths
    └── Western: Disable FA-FE, variable widths
          │
          ▼
[6. Close Menu, Return to Title]
```

### 8.2 Kernel Hot-Swap Implementation

```cpp
void swap_kernel() {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    // The kernel is typically loaded once at game start
    // Full hot-swap requires either:
    // A) Reloading kernel into memory (complex, may cause issues)
    // B) Redirecting and requiring return to title (safer)

    // We use approach B: Set up redirection, warn user to return to title

    // Update redirection table
    redirect_set_kernel_path(info.kernel_path);

    // If we're not at title screen, the change won't fully apply
    // until the game reloads the kernel
    uint16_t mode = *(uint16_t*)0xCC0D84;
    if (mode != 0x00) {
        ffnx_warning("Kernel change will fully apply after returning to title screen\n");
    }
}
```

### 8.3 Field Dialogue Hot-Swap

```cpp
void swap_field_lgp() {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    // Field dialogue is loaded per-scene
    // Changing the LGP path means the NEXT scene load gets new dialogue
    // Current scene keeps its already-loaded text

    redirect_set_field_path(info.field_lgp);

    ffnx_info("Field dialogue will update on next scene transition\n");
}
```

### 8.4 Font Hot-Swap

```cpp
void swap_fonts() {
    const auto& info = language_menu::get_language_info(s_state.current_language);

    if (info.requires_extended_font) {
        // Japanese font mode

        // 1. Enable multi-page font loading (6 pages)
        enable_japanese_font_mode(true);

        // 2. Patch character width table to fixed 16px
        patch_character_widths_japanese();

        // 3. Enable FA-FE page marker parsing
        enable_page_markers(true);

        // 4. Trigger font texture reload
        reload_font_textures("jafont");

    } else {
        // Western font mode

        // 1. Disable multi-page loading
        enable_japanese_font_mode(false);

        // 2. Restore variable character widths
        restore_character_widths_western();

        // 3. Disable FA-FE parsing
        enable_page_markers(false);

        // 4. Reload standard font
        reload_font_textures("usfont");
    }
}

void reload_font_textures(const char* prefix) {
    // Invalidate cached font textures
    // This forces the game to reload them with the new prefix

    // Find font texture handles
    // Mark them as invalid/dirty
    // Next render pass will reload from new paths

    ffnx_info("Font textures marked for reload (prefix: %s)\n", prefix);
}
```

---

## 9. User Interface Design

### 9.1 Visual Mockup

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║                    SELECT LANGUAGE                       ║
║                    ───────────────                       ║
║                                                          ║
║                  ► English                               ║
║                    日本語                                ║
║                    Deutsch                               ║
║                    Français                              ║
║                    Español                               ║
║                                                          ║
║                                                          ║
║           [○] Confirm    [×] Cancel                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

### 9.2 UI Specifications

| Element | Position | Size | Color |
|---------|----------|------|-------|
| Background Overlay | Fullscreen | 320x240 | #000000 @ 50% alpha |
| Menu Box | Centered | 200x130 | Blue gradient #000040 → #000080 |
| Border | Box edges | 2px | #4080C0 |
| Title Text | Top center | 14px | #FFFFFF |
| Option Text | Left-aligned | 12px | #FFFFFF (normal), #FFFF00 (selected) |
| Cursor | Left of selected | 8x8 | #FFFFFF, animated |
| Instructions | Bottom | 10px | #888888 |

### 9.3 Animation Specifications

| Animation | Duration | Easing |
|-----------|----------|--------|
| Menu Fade In | 300ms | Ease Out |
| Menu Fade Out | 300ms | Ease In |
| Cursor Move | Instant | N/A |
| Cursor Pulse | 500ms loop | Sine wave (scale 0.9-1.1) |

### 9.4 Input Mapping

| Input | Action |
|-------|--------|
| D-Pad Up / W / ↑ | Move selection up |
| D-Pad Down / S / ↓ | Move selection down |
| Circle / Enter / Z | Confirm selection |
| Cross / Escape / X | Cancel, close menu |
| F12 (configurable) | Toggle menu (from title/field) |

---

## 10. Testing Strategy

### 10.1 Unit Tests

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_language_enum` | Verify all languages defined | 5 languages (EN, JA, DE, FR, ES) |
| `test_language_info` | Verify language metadata | All fields populated correctly |
| `test_config_parse` | Parse FFNx.toml settings | Settings loaded correctly |
| `test_config_save` | Save language to FFNx.toml | File updated, persists restart |
| `test_path_redirect_kernel` | Kernel path redirection | Returns language-specific path |
| `test_path_redirect_field` | Field LGP redirection | Returns language-specific path |
| `test_availability_check` | Language availability scan | Correct results based on files |

### 10.2 Integration Tests

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| `test_menu_open_close` | Press F12, navigate, cancel | Menu opens, closes, no crash |
| `test_language_change` | Select different language, confirm | Language changes, saves |
| `test_kernel_swap` | Change language, check item names | Names in new language |
| `test_field_swap` | Change language, enter new field | Dialogue in new language |
| `test_font_swap_ja` | Switch to Japanese | Japanese characters render |
| `test_font_swap_en` | Switch back to English | English renders correctly |
| `test_persistence` | Change language, restart game | Language persists |

### 10.3 Compatibility Tests

| Test Case | Configuration | Expected Result |
|-----------|---------------|-----------------|
| `test_7h_compatibility` | With 7th Heaven | Menu works, no conflicts |
| `test_mod_compatibility` | With texture mods | Textures load correctly |
| `test_steam_version` | Steam 2013 | All features work |
| `test_estore_version` | eStore | All features work |
| `test_1998_version` | Original 1998 | All features work |

### 10.4 Edge Cases

| Test Case | Scenario | Expected Result |
|-----------|----------|-----------------|
| `test_missing_language` | Language files not present | Graceful fallback to English |
| `test_corrupted_kernel` | Invalid kernel.bin | Error message, no crash |
| `test_hotkey_conflict` | F12 used by other software | Alternative hotkey works |
| `test_rapid_toggle` | Open/close menu rapidly | No crashes or state corruption |
| `test_mid_dialogue` | Change language during dialogue | Current text unchanged, next uses new |

---

## 11. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| Create `language_menu.h/cpp` skeleton | HIGH | 4h | None |
| Create `language_manager.h/cpp` skeleton | HIGH | 4h | None |
| Add config options to `cfg.cpp` | HIGH | 2h | None |
| Set up directory structure | HIGH | 1h | None |
| Basic menu rendering (box only) | HIGH | 4h | BGFX setup |
| Input handling framework | HIGH | 4h | FFNx input system |

**Milestone 1**: Menu box renders, opens/closes with hotkey

### Phase 2: Core Functionality (Week 3-4)

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| Language selection UI | HIGH | 8h | Phase 1 |
| Cursor navigation | HIGH | 4h | Phase 1 |
| File path redirection | HIGH | 8h | Phase 1 |
| Kernel swapping | HIGH | 8h | Redirection |
| Configuration persistence | HIGH | 4h | Phase 1 |

**Milestone 2**: Can select language, kernel changes

### Phase 3: Font System (Week 5-6)

| Task | Priority | MEDIUM | Dependencies |
|------|----------|--------|--------------|
| Japanese font loading (6 pages) | HIGH | 12h | PR #737 code |
| Character width patching | HIGH | 8h | Japanese fonts |
| Font hot-swap | HIGH | 8h | Font loading |
| FA-FE page marker support | HIGH | 8h | Japanese fonts |

**Milestone 3**: Japanese text renders correctly

### Phase 4: Field Dialogue (Week 7-8)

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| Field LGP redirection | HIGH | 8h | Redirection system |
| Scene transition handling | MEDIUM | 4h | LGP redirection |
| Dialogue hot-swap testing | MEDIUM | 8h | Field redirection |

**Milestone 4**: Field dialogue in selected language

### Phase 5: Polish & Testing (Week 9-10)

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| Animation polish | LOW | 4h | Phase 2 |
| Sound effects | LOW | 2h | FFNx audio |
| Error handling | MEDIUM | 8h | All phases |
| Compatibility testing | HIGH | 16h | All phases |
| Documentation | MEDIUM | 8h | All phases |
| Bug fixes | HIGH | 16h | Testing |

**Milestone 5**: Production-ready release

### Total Estimated Effort

| Phase | Effort | Duration |
|-------|--------|----------|
| Phase 1: Foundation | 19h | 2 weeks |
| Phase 2: Core | 32h | 2 weeks |
| Phase 3: Fonts | 36h | 2 weeks |
| Phase 4: Field | 20h | 2 weeks |
| Phase 5: Polish | 54h | 2 weeks |
| **Total** | **161h** | **10 weeks** |

---

## 12. Risk Assessment

### 12.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Kernel hot-swap causes crashes | MEDIUM | HIGH | Require title screen return |
| Font texture reload fails | LOW | HIGH | Implement robust fallback |
| Mode hook conflicts with mods | MEDIUM | MEDIUM | Use unique mode ID (0x1D) |
| Japanese encoding issues | MEDIUM | MEDIUM | Use PR #737's proven approach |
| Memory corruption from patches | LOW | HIGH | Extensive testing, boundaries |

### 12.2 Compatibility Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| 7th Heaven VFS conflicts | MEDIUM | MEDIUM | Test extensively with 7H |
| Steam overlay interference | LOW | LOW | Document workarounds |
| Anti-virus false positives | LOW | LOW | Code signing, documentation |
| Save file corruption | LOW | HIGH | Language stored in FFNx.toml, not save |

### 12.3 Scope Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Feature creep | MEDIUM | MEDIUM | Strict scope control |
| Translation quality issues | HIGH | LOW | Out of scope - use existing translations |
| Performance impact | LOW | LOW | Profile and optimize |

---

## 13. Appendices

### Appendix A: Memory Addresses Quick Reference

```
Game Mode:       0xCC0D84  (word)    - Current game mode
Menu Active:     0xDC12DC  (dword)   - Menu system flag
Menu X:          0xDC105C  (dword)   - Menu window X
Menu Y:          0xDC1060  (dword)   - Menu window Y
Menu Width:      0xDC1064  (dword)   - Menu window width
Menu Height:     0xDC1068  (dword)   - Menu window height
Font Info:       0x99DDA8  (ptr)     - Character width table
```

### Appendix B: Function Addresses Quick Reference

```
Mode Dispatcher:     0x4090E6  (sub_4090E6)  - 2932 bytes
Menu Init:           0x6CD3B0  (sub_6CD3B0)  - Menu system start
Menu Loading:        0x6C1468  (sub_6C1468)  - 1618 bytes
Character Drawing:   0x66E272  (sub_66E272)  - 881 bytes
Debug Print:         0x664E30  (sub_664E30)  - Logging function
```

### Appendix C: Game Mode Values

```
0x00 = Title/Init      0x0B = Snowboard
0x01 = Field           0x0C = Credits
0x02 = World Map       0x0D = Game Over
0x03 = Battle          0x10 = Coaster
0x05 = Menu            0x14 = Highway
0x06 = Chocobo         0x1D = Language Menu (NEW)
0x09 = Submarine
```

### Appendix D: File Hash Reference

For asset validation:

```
# English KERNEL.BIN (1.02 US)
MD5: <calculate from your file>

# Japanese KERNEL.BIN (International)
MD5: <calculate from your file>

# etc.
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-20 | Claude Code | Initial specification |

---

**END OF SPECIFICATION**
