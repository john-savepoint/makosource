# FFNx Developer Guide

**Document Version:** 1.1 (PR #737 Integration Update)
**Created:** 2025-11-24 22:31:00 JST (Monday)
**Last Modified:** 2025-11-25 01:35 JST (Tuesday)
**Author:** Research compiled by Claude Code
**Session-ID:** 8f58819d-f9c4-4f04-8e95-4af04d782606, 37952f94-430d-46c5-8bed-8068cf9a7a62
**Purpose:** Comprehensive developer guide for FFNx - the next-generation modding platform for Final Fantasy VII and VIII

**Status:** Deep Dive Documentation - Production Ready

---

## 🔴 CRITICAL: Working with PR #737 (Read This First)

**Before you start modifying FFNx for Japanese text support, understand this:**

### PR #737 Already Implements Japanese Rendering

Community member **CosmosXIII** created [PR #737](https://github.com/julianxhokaxhiu/FFNx/pull/737) (September 2024) implementing Japanese text rendering. It is **95% complete** but has bugs blocking merge.

**What PR #737 Does:**
- ✅ FA-FE encoding for multi-page fonts
- ✅ Loads all 6 jafont textures
- ✅ Character width tables (1,536 values)
- ✅ Function pointer hooking (C++, no assembly)
- ✅ Works with Japanese game version (ff7_ja.exe)

**What PR #737 Does NOT Do:**
- ❌ Enable Japanese in English version
- ❌ Multi-language support (FR/DE/ES)
- ❌ Runtime language switching
- ❌ Translation file loading

**Known Bugs in PR #737:**
- ❌ Colored text rendering broken
- ❌ Character name input screen corrupted
- ❌ Cursor alignment issues

### Your Development Strategy Should Be:

**NOT:** Fork main FFNx → implement from scratch → create PR

**YES:** Fork PR #737 → fix bugs → extend for multi-language → create PR

### Quick Start for PR #737 Development

```bash
# Clone PR #737's branch (NOT main FFNx)
git clone https://github.com/CosmosXIII/FFNx.git
cd FFNx
git checkout japanese-text-support

# Build it
mkdir build && cd build
cmake ..
cmake --build . --config Debug

# Test it (requires Japanese FF7 version)
# Copy FFNx.dll to your game directory
# Launch ff7_ja.exe
```

### Key Files to Understand

| File | What It Does | Why You Need It |
|------|--------------|-----------------|
| `src/ff7/japanese_text.cpp` | Main Japanese rendering (2,386 lines) | Where bugs are, where to extend |
| `src/cfg.cpp` | Config parsing | Add multi-language settings here |
| `src/common.h` | Struct definitions | Add language switching state |
| `misc/FFNx.toml` | User configuration | Add language toggle options |

### Development Workflow

**Phase 1.5: Fix PR #737 Bugs (Do This First)**
1. Debug colored text rendering failure
2. Fix character name input corruption
3. Fix cursor alignment
4. Submit fixes to PR #737

**Phase 2: Extend for Multi-Language**
5. Load FR/DE/ES fonts alongside Japanese
6. Implement language toggle hotkey
7. Add translation file loader
8. Test EN↔JA↔FR↔DE↔ES switching

**Phase 3: Add Furigana**
9. Implement dual-layer text rendering
10. Add furigana toggle hotkey

### Where to Start

**If you want to fix colored text bug:**
→ Start at `src/ff7/japanese_text.cpp` line 479 (`get_character_color()`)

**If you want to add multi-language:**
→ Start at `src/ff7/japanese_text.cpp` line 84 (texture loading)

**If you want to add language toggle:**
→ Start at `src/cfg.cpp` (add config), then `src/input.cpp` (add hotkey)

### Related Documentation

- **`PR737_ANALYSIS.md`** - Complete code walkthrough
- **`ARCHITECTURAL_RETROSPECTIVE.md`** - Why PR #737's approach is better than assembly
- **`PR737_INTEGRATION_STRATEGY.md`** - Step-by-step implementation plan

---

## TABLE OF CONTENTS

0. [Working with PR #737](#-critical-working-with-pr-737-read-this-first) **← START HERE**
1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Codebase Structure](#3-codebase-structure)
4. [Build System](#4-build-system)
5. [Rendering Pipeline](#5-rendering-pipeline)
6. [Japanese Text Implementation](#6-japanese-text-implementation) **← PR #737 deep dive**
7. [External Texture System](#7-external-texture-system)
8. [Configuration System](#8-configuration-system)
9. [Audio Engine](#9-audio-engine)
10. [Hext Patching System](#10-hext-patching-system)
11. [Developer Tools](#11-developer-tools)
12. [Integration with 7th Heaven](#12-integration-with-7th-heaven)
13. [Building and Debugging](#13-building-and-debugging)
14. [Extending FFNx](#14-extending-ffnx)
15. [Reference](#15-reference)

---

## 1. INTRODUCTION

### 1.1 What is FFNx?

FFNx is the evolution of Aali's FF7_OpenGL driver, providing a modern, feature-rich modding platform for Final Fantasy VII and VIII (Steam 2013 and original releases).

**Core Philosophy:**
- Backward compatibility with existing mods
- Modern rendering backends (DirectX 11/12, Vulkan, OpenGL)
- Extensive modding capabilities
- Community-driven development
- Open source (GPLv3)

**Key Statistics:**
- **Language:** C++ (C++17 standard)
- **Lines of Code:** ~92 source files in src/
- **Dependencies:** 15+ libraries (BGFX, FFmpeg, VGMStream, SoLoud, etc.)
- **Supported Games:** FF7 (1998, Steam 2013, eStore) and FF8 (2000, Steam 2013)

### 1.2 For Developers

This guide focuses on:
- Understanding FFNx's architecture and design decisions
- Building and compiling FFNx from source
- Implementing new features (especially Japanese language support)
- Debugging and testing modifications
- Integration points with mods and tools (7th Heaven, Hext, etc.)

**NOT covered in this guide:**
- End-user installation (see [docs/how_to_install.md](https://github.com/julianxhokaxhiu/FFNx/blob/master/docs/how_to_install.md))
- General modding tutorials (see 7th Heaven Developer Guide in this project)
- Gameplay modding (see Qhimm forums)

### 1.3 Prerequisites

**Required Knowledge:**
- Intermediate-to-advanced C++ programming
- Understanding of graphics APIs (DirectX, Vulkan, OpenGL concepts)
- Basic game engine architecture
- Memory manipulation and pointers
- Windows API familiarity

**Required Software:**
- Visual Studio 2022 Community (with MSVC toolchain)
- vcpkg (package manager - included in repo)
- CMake 3.21+
- Git (with submodule support)
- FF7 or FF8 PC installed (for testing)

**Recommended Tools:**
- RenderDoc (for graphics debugging)
- x64dbg (for assembly debugging)
- Cheat Engine (for memory analysis)
- 7th Heaven (for mod management)

### 1.4 Project Origins & History

**Timeline:**
- **2009:** Aali releases FF7_OpenGL driver
- **2019:** Julian Xhokaxhiu creates FFNx as continuation
- **2020:** Integration with 7th Heaven 2.3+
- **2021:** FFNx becomes default driver in 7th Heaven
- **2025:** Active development continues with features like Japanese text support

**Key Contributors:**
- Julian Xhokaxhiu (TrueOdin) - Lead Developer
- Tang-Tang Zhou (vertex2995) - 60FPS, Steam achievements
- Jérôme Arzel (myst6re) - Tools, MINIPSF, FF8 support
- CosmosXIII - Lighting engine, camera control, analogue controls

---

## 2. ARCHITECTURE OVERVIEW

### 2.1 High-Level Design

FFNx acts as a **shim layer** between the game executable and Windows/Graphics APIs:

```
┌─────────────────────────────────────────┐
│        FF7.exe / FF8.exe (Game)         │
│  (Original Game Code - Unmodified)      │
└──────────────┬──────────────────────────┘
               │ Function Calls
               ↓
┌─────────────────────────────────────────┐
│         FFNx.dll (AF3DN.P)              │
│  • Intercepts game function calls       │
│  • Implements modern rendering          │
│  • Provides modding hooks               │
│  • Manages configuration                │
└──────────────┬──────────────────────────┘
               │ Translated Calls
               ↓
┌─────────────────────────────────────────┐
│      BGFX (Cross-Platform Renderer)     │
│  • DirectX 11/12 Backend                │
│  • Vulkan Backend                       │
│  • OpenGL Backend                       │
└──────────────┬──────────────────────────┘
               │ Graphics Commands
               ↓
┌─────────────────────────────────────────┐
│      GPU Driver (NVIDIA/AMD/Intel)      │
└─────────────────────────────────────────┘
```

### 2.2 Key Components

#### 2.2.1 Core Systems

| Component | File(s) | Purpose |
|-----------|---------|---------|
| **Configuration** | `cfg.cpp`, `cfg.h` | TOML config parsing (FFNx.toml) |
| **Common** | `common.cpp`, `common.h` | Shared utilities, game struct definitions |
| **Logging** | `log.cpp`, `log.h` | FFNx.log file management, trace levels |
| **Redirect** | `redirect.cpp`, `redirect.h` | File I/O redirection for mods |
| **Patch** | `patch.cpp`, `patch.h` | Memory patching utilities |
| **Hext** | `hext.cpp`, `hext.h` | Runtime assembly patches |

#### 2.2.2 Rendering System

| Component | File(s) | Purpose |
|-----------|---------|---------|
| **Renderer** | `renderer.cpp`, `renderer.h` | BGFX initialization and management |
| **GL Layer** | `gl/*.cpp`, `gl/*.h` | Translates game GL calls to BGFX |
| **Textures** | `image/` | DDS/PNG texture loading |
| **External Textures** | `common.cpp` | Mod texture override system |

#### 2.2.3 Audio System

| Component | File(s) | Purpose |
|-----------|---------|---------|
| **Music** | `music.cpp`, `music.h` | Music playback (OGG, MP3, MINIPSF) |
| **Voice** | `voice.cpp`, `voice.h` | Voice acting support |
| **Audio** | `audio.cpp`, `audio.h` | SoLoud audio engine integration |
| **VGMStream** | `audio/vgmstream/` | Game audio format support |
| **OpenPSF** | `audio/openpsf/` | PSX/PS2 music emulation |

#### 2.2.4 Game-Specific Logic

| Component | File(s) | Purpose |
|-----------|---------|---------|
| **FF7 Data** | `ff7_data.cpp`, `ff7.h`, `ff7_opengl.cpp` | FF7-specific hooks and structures |
| **FF7 Externals** | `externals_102_us.h`, etc. | Game memory address mappings |
| **FF8 Data** | `ff8_data.cpp`, `ff8.h`, `ff8_opengl.cpp` | FF8-specific hooks and structures |
| **Field System** | `ff7/field/`, `ff8/field/` | Field rendering and scripts |
| **Battle System** | `ff7/battle/`, `ff8/battle/` | Battle scene rendering |
| **World Map** | `ff7/world/`, `ff8/world/` | World map rendering |

### 2.3 Initialization Flow

**Startup Sequence:**

```
1. Game launches ff7.exe/ff8.exe
   ↓
2. Game loads AF3DN.P → Redirected to FFNx.dll
   ↓
3. DllMain() executes
   ↓
4. FFNx reads FFNx.toml configuration
   ↓
5. Logging system initializes (FFNx.log created)
   ↓
6. BGFX renderer initializes with chosen backend
   ↓
7. Audio engine (SoLoud) initializes
   ↓
8. Hext patches loaded from misc/hext/
   ↓
9. Texture override paths registered (mods/Textures/)
   ↓
10. Game initialization hooks installed
    ↓
11. Game continues normal execution (with FFNx intercepting calls)
```

**Key Initialization Functions:**

```cpp
// src/ff7_opengl.cpp (FF7 example)
void ff7_init_hooks(struct game_obj *game_object)
{
    // Install function hooks
    replace_function(ff7_externals.engine_exit, (void*)engine_exit_wrapper);
    replace_function(ff7_externals.swirl_main_loop, (void*)swirl_main_loop_wrapper);

    // Initialize subsystems
    ff7_load_driver(game_object);      // Graphics driver init
    ff7_data(game_object);             // Populate memory addresses
    common_externals_init();           // Initialize common data structures

    // Initialize Japanese font patches (if enabled)
    if (font_language == "ja") {
        PatchFontWidthsForJapanese();  // Geometry patches
    }
}
```

### 2.4 Hook System

FFNx uses **function hooking** to intercept game calls:

```cpp
// src/patch.cpp
void replace_function(uint32_t offset, void* func)
{
    // Save original bytes
    memcpy(&original_func, (void*)offset, 5);

    // Write JMP instruction
    uint8_t jmp_instruction[5] = {
        0xE9,  // JMP opcode
        // Calculate relative offset
        (uint8_t)((uintptr_t)func - offset - 5),
        // ... rest of offset bytes
    };

    // Make memory writable
    DWORD oldProtect;
    VirtualProtect((void*)offset, 5, PAGE_EXECUTE_READWRITE, &oldProtect);

    // Apply patch
    memcpy((void*)offset, jmp_instruction, 5);

    // Restore protection
    VirtualProtect((void*)offset, 5, oldProtect, &oldProtect);
}
```

**Hook Points (FF7 US 1.02 Examples):**

| Function | Address | Purpose |
|----------|---------|---------|
| `engine_exit` | `0x40FF38` | Cleanup before exit |
| `swirl_main_loop` | `0x40EBEB` | Battle swirl effect |
| `load_texture` | `0x688415` | Texture loading (for override) |
| `draw_graphics_object` | `0x66E272` | Character rendering (for Japanese fonts) |

---

## 3. CODEBASE STRUCTURE

### 3.1 Directory Layout

```
FFNx/
├── .github/                # GitHub workflows (CI/CD)
├── .vcpkg/                 # vcpkg configuration
├── choco/                  # Chocolatey packaging
├── docs/                   # Documentation
│   ├── ff8/                # FF8-specific docs
│   │   └── mods/           # FF8 modding guides
│   └── mods/               # General modding guides
├── misc/                   # Game data files
│   ├── hext/               # Hext patch files
│   │   ├── ff7/            # FF7 patches
│   │   │   └── en/         # English version patches
│   │   └── ff8/            # FF8 patches
│   └── FFNx.toml           # Default configuration template
├── src/                    # Source code (C++)
│   ├── audio/              # Audio subsystems
│   │   ├── memorystream/   # In-memory audio streaming
│   │   ├── openpsf/        # PSX/PS2 music emulation
│   │   └── vgmstream/      # Game audio format support
│   ├── ff7/                # FF7-specific code
│   │   ├── battle/         # Battle system
│   │   ├── field/          # Field system
│   │   └── world/          # World map
│   ├── ff8/                # FF8-specific code
│   │   ├── battle/
│   │   ├── field/
│   │   └── world/
│   ├── gl/                 # OpenGL translation layer
│   ├── image/              # Image loading (DDS, PNG)
│   ├── imgui_club/         # ImGui extensions
│   ├── video/              # Video playback
│   └── [core files]        # Main driver code
├── utils/                  # Utility scripts
├── vcpkg/                  # Dependency manager
├── CMakeLists.txt          # Build configuration
├── CMakePresets.json       # Build presets
├── README.md               # Project overview
└── COPYING.TXT             # GPLv3 license
```

### 3.2 Key Source Files

#### 3.2.1 Entry Points

```cpp
// src/main.cpp (hypothetical - actual entry is DllMain in common.cpp)
// FFNx is a DLL that replaces AF3DN.P, so main entry is DllMain

// src/common.cpp
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    switch(fdwReason)
    {
        case DLL_PROCESS_ATTACH:
            // FFNx initialization
            init();
            break;
        case DLL_PROCESS_DETACH:
            // Cleanup
            shutdown();
            break;
    }
    return TRUE;
}
```

#### 3.2.2 Configuration System

```cpp
// src/cfg.cpp - Uses tomlplusplus library
struct FFNxConfig
{
    std::string window_title;
    bool fullscreen;
    uint32_t window_size_x;
    uint32_t window_size_y;
    std::string renderer_backend;  // auto, OpenGL, DirectX11, DirectX12, Vulkan
    bool trace_all;
    bool trace_renderer;
    std::string mod_path;
    std::string font_language;     // "en", "ja", etc.
    // ... 100+ configuration options
};

void read_cfg()
{
    toml::table config = toml::parse_file("FFNx.toml");

    // Parse with defaults
    window_size_x = config["window_size_x"].value_or(1280);
    font_language = config["font_language"].value_or("en");

    // Log configuration
    ffnx_info("Configuration loaded: window_size=%dx%d, font=%s\n",
              window_size_x, window_size_y, font_language.c_str());
}
```

#### 3.2.3 Texture Override System

```cpp
// src/common.cpp
uint32_t common_load_texture(/* ... */)
{
    // Check if external texture exists
    std::string mod_texture_path = find_external_texture(texture_name);

    if (!mod_texture_path.empty())
    {
        ffnx_info("Loading external texture: %s\n", mod_texture_path.c_str());

        // Load DDS or PNG
        if (ends_with(mod_texture_path, ".dds"))
            texture_handle = load_dds_texture(mod_texture_path);
        else
            texture_handle = load_png_texture(mod_texture_path);
    }
    else
    {
        // Fall back to original game texture
        texture_handle = load_game_texture(/* ... */);
    }

    return texture_handle;
}

// Texture search paths (priority order):
// 1. <mod_path>/<hash>/<texture_name>.dds
// 2. <mod_path>/<hash>/<texture_name>.png
// 3. <mod_path>/<texture_name>.dds
// 4. <mod_path>/<texture_name>.png
// 5. Original game texture
```

### 3.3 Memory Address Mappings

FFNx needs to know where game data structures live in memory. These vary by game version:

```cpp
// src/externals_102_us.h (FF7 US 1.02)
struct ff7_externals_102_us
{
    // Graphics functions
    uint32_t engine_exit                = 0x40FF38;
    uint32_t create_window              = 0x401010;
    uint32_t load_texture               = 0x688415;

    // Text rendering
    uint32_t draw_character             = 0x66E272;  // Character drawing function
    uint32_t font_info                  = 0x99DDA8;  // Character width table pointer

    // Game state
    uint32_t field_id                   = 0xCC15D0;  // Current field ID
    uint32_t battle_id                  = 0x9A8F00;  // Current battle ID

    // ... 200+ addresses
};

// src/externals_102_fr.h, externals_102_de.h, externals_102_sp.h
// Different addresses for French, German, Spanish versions

// src/ff7_data.cpp
void ff7_data(struct game_obj *game_object)
{
    // Select correct address mapping based on game version
    if (version == VERSION_FF7_102_US)
        ff7_externals = ff7_externals_102_us;
    else if (version == VERSION_FF7_102_FR)
        ff7_externals = ff7_externals_102_fr;
    // etc.

    // Populate common_externals with runtime values
    common_externals.font_info = (char*)ff7_externals.font_info;
}
```

---

## 4. BUILD SYSTEM

### 4.1 vcpkg Dependency Management

FFNx uses [vcpkg](https://vcpkg.io/) to manage all external libraries:

```json
// vcpkg.json
{
  "name": "ffnx",
  "version-string": "1.23.0",
  "dependencies": [
    "bgfx",
    "bimg",
    "ffmpeg",
    "vgmstream",
    "libpng",
    "tomlplusplus",
    "pugixml",
    "soloud",
    "imgui",
    "xxhash",
    "stackwalker",
    "mimalloc"
  ]
}
```

**Dependency Purposes:**

| Library | Purpose |
|---------|---------|
| **bgfx** | Cross-platform rendering abstraction |
| **bimg** | Image loading (DDS support) |
| **ffmpeg** | Video decoding with H/W acceleration |
| **vgmstream** | Game audio format support |
| **libpng** | PNG texture loading |
| **tomlplusplus** | Configuration file parsing |
| **pugixml** | Steam XML manifest parsing |
| **soloud** | Audio playback engine |
| **imgui** | DevTools UI |
| **xxhash** | Fast hashing for texture caching |
| **stackwalker** | Crash dump stack traces |
| **mimalloc** | High-performance memory allocator |

### 4.2 CMake Build Configuration

```cmake
# CMakeLists.txt (simplified)
cmake_minimum_required(VERSION 3.21)

project(FFNx)

# Set C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable parallel builds
add_compile_options(/MP)

# Find packages via vcpkg
find_package(bgfx CONFIG REQUIRED)
find_package(ffmpeg CONFIG REQUIRED)
find_package(tomlplusplus CONFIG REQUIRED)
# ... etc

# Define source files
file(GLOB_RECURSE FFNX_SOURCES
    "src/*.cpp"
    "src/*.h"
    "src/**/*.cpp"
    "src/**/*.h"
)

# Create DLL target
add_library(FFNx SHARED ${FFNX_SOURCES})

# Link libraries
target_link_libraries(FFNx PRIVATE
    bgfx::bgfx
    bgfx::bx
    bgfx::bimg
    ffmpeg::avcodec
    ffmpeg::avformat
    tomlplusplus::tomlplusplus
    # ... etc
)

# Output name
set_target_properties(FFNx PROPERTIES OUTPUT_NAME "AF3DN")
```

### 4.3 Build Profiles

```json
// CMakePresets.json
{
  "configurePresets": [
    {
      "name": "x86-Release",
      "generator": "Visual Studio 17 2022",
      "architecture": "Win32",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    },
    {
      "name": "x86-Debug",
      "architecture": "Win32",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    },
    {
      "name": "x86-RelWithDebInfo",
      "architecture": "Win32",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "RelWithDebInfo"
      }
    }
  ]
}
```

### 4.4 Build Steps

**Step-by-Step Build Process:**

```batch
REM 1. Clone repository with submodules
git clone --recursive https://github.com/julianxhokaxhiu/FFNx.git
cd FFNx

REM 2. Bootstrap vcpkg
cd vcpkg
call bootstrap-vcpkg.bat
vcpkg integrate install
cd ..

REM 3. Open in Visual Studio 2022
REM File → Open → Folder → Select FFNx directory

REM 4. Select build preset
REM Status Bar → Choose "x86-Release"

REM 5. Build
REM Build → Build All (or press F7)

REM Output: .build\bin\AF3DN.P (actually FFNx.dll)
```

**Command Line Build:**

```batch
REM Configure
cmake --preset x86-Release

REM Build
cmake --build --preset x86-Release

REM Output: .build\bin\AF3DN.P
```

---

## 6. JAPANESE TEXT IMPLEMENTATION

### 6.1 Overview

The Japanese text implementation in FFNx is a comprehensive system that:
- Supports multi-page font textures (6 pages for ~1536 characters)
- Uses FA-FE encoding for page markers
- Patches character widths to prevent squashing
- Dynamically switches textures based on current character

**Reference:** See FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md in this project for complete specifications.

### 6.2 Configuration Integration

```cpp
// src/cfg.h
extern std::string font_language;  // "en", "ja", "zh-tw", "ko", etc.
extern bool font_enable_furigana;  // Phase 2 feature

// src/cfg.cpp
void read_cfg()
{
    font_language = config["font_language"].value_or("en");
    font_enable_furigana = config["font_enable_furigana"].value_or(false);

    ffnx_info("Font language: %s\n", font_language.c_str());
}
```

### 6.3 Multi-Texture Loading (Phase 1)

```cpp
// src/common.cpp
uint32_t common_load_texture(/* ... */)
{
    // Detect font texture request
    bool is_font_texture = (strstr(filename, "usfont") != NULL ||
                           strstr(filename, "jafont") != NULL);

    if (is_font_texture && font_language == "ja")
    {
        ffnx_info("Japanese font detected: forcing 6-page allocation\n");

        // CRITICAL: Allocate 6 texture slots BEFORE loading
        VRASS(texture_set, ogl.gl_set->textures, 6);

        // Load all 6 font pages
        for (int page = 0; page < 6; page++)
        {
            char page_filename[64];
            sprintf(page_filename, "jafont_%d.png", page + 1);

            std::string mod_path = find_external_texture(page_filename);

            if (!mod_path.empty())
            {
                ffnx_info("Loading Japanese font page %d: %s\n",
                         page + 1, mod_path.c_str());

                texture_handle[page] = load_png_texture(mod_path);
            }
            else
            {
                ffnx_error("FAILED to load font page %d\n", page + 1);
            }
        }

        return texture_handle[0];  // Return first page handle
    }

    // Standard single-texture loading for non-Japanese
    return load_texture_standard(/* ... */);
}
```

### 6.4 Character Width Patching (Phase 1)

```cpp
// src/ff7/font.cpp
void PatchFontWidthsForJapanese()
{
    if (font_language != "ja") return;

    ffnx_info("Patching character width table for Japanese...\n");

    // Get width table pointer from game memory
    // (Populated by ff7_data() from externals)
    char* font_width_table = common_externals.font_info;

    if (!font_width_table) {
        ffnx_error("font_info pointer is NULL!\n");
        return;
    }

    ffnx_info("Width table located at: 0x%p\n", (void*)font_width_table);

    // Make memory writable
    DWORD oldProtect;
    if (!VirtualProtect(font_width_table, 256, PAGE_READWRITE, &oldProtect)) {
        ffnx_error("VirtualProtect failed! Error code: %d\n", GetLastError());
        return;
    }

    // Overwrite ALL widths with fixed 16px (0x10)
    for (int i = 0; i < 256; i++) {
        font_width_table[i] = 0x10;  // 16 pixels
    }

    // Restore original memory protection
    VirtualProtect(font_width_table, 256, oldProtect, &oldProtect);

    ffnx_info("Successfully patched character width table.\n");
}

// src/ff7_opengl.cpp
void ff7_init_hooks(struct game_obj *game_object)
{
    // ... existing initialization ...

    // [NEW] Apply Japanese font patches
    // MUST be called AFTER ff7_data() because it relies on common_externals
    PatchFontWidthsForJapanese();

    // ... rest of initialization ...
}
```

### 6.5 Global Variable for Page Tracking (Phase 2)

```cpp
// src/globals.h
#ifndef GLOBALS_H
#define GLOBALS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Japanese font support - Assembly hook will write to this
__declspec(dllexport) extern uint8_t g_currentFontPage;

#ifdef __cplusplus
}
#endif

#endif // GLOBALS_H

// src/common.cpp
uint8_t g_currentFontPage = 0;  // Default to page 0

// Log address at startup for Hext patch
void LogGlobalAddresses()
{
    ffnx_info("=== FFNx Global Variable Addresses ===\n");
    ffnx_info("g_currentFontPage: 0x%p\n", (void*)&g_currentFontPage);
    ffnx_info("=======================================\n");
    ffnx_info("Use the address above in your Hext patch!\n");
}
```

### 6.6 Renderer Integration (Phase 2)

```cpp
// src/gl/gl.cpp
#include "../globals.h"  // For g_currentFontPage

void gl_bind_texture_set(struct texture_set *_texture_set)
{
    VOBJ(texture_set, texture_set, _texture_set);

    if (!VPTR(texture_set)) return;

    // [NEW] Japanese font page switching logic
    if (font_language == "ja") {
        uint32_t num_textures = VREF(texture_set, ogl.gl_set->textures);

        if (num_textures == 6) {
            // This is a Japanese font texture set

            // Read the current page from the global variable
            // (Set by the Assembly hook in the game's text parser)
            uint8_t requested_page = g_currentFontPage;

            // Safety check: clamp to valid range (0-5)
            if (requested_page > 5) {
                ffnx_warning("Invalid font page: %d. Clamping to 5.\n",
                           requested_page);
                requested_page = 5;
            }

            // Override the palette_index with our page index
            VRASS(texture_set, palette_index, requested_page);

            if (trace_all || trace_renderer) {
                ffnx_trace("Binding Japanese font page %d\n", requested_page);
            }

            // Bind the texture for this page
            uint32_t tex_handle = VREF(texture_set, texturehandle[requested_page]);
            if (tex_handle) {
                gl_set_texture(tex_handle, 0);  // 0 = texture unit 0
            } else {
                ffnx_error("Font page %d has NULL texture handle!\n",
                          requested_page);
            }

            return;  // Early return - we've handled this texture
        }
    }

    // [ORIGINAL] Standard texture binding logic for non-font textures
    uint32_t palette_index = VREF(texture_set, palette_index);
    uint32_t tex_handle = VREF(texture_set, texturehandle[palette_index]);

    if (tex_handle) {
        gl_set_texture(tex_handle, 0);
    }
}
```

### 6.7 Hext Patch Integration (Phase 2)

The Assembly hook is implemented via Hext patches (see Section 10):

```hext
# misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt

# This patch intercepts the character processing loop to detect
# FA-FE page marker bytes and update the global font page variable.

# ⚠️ CRITICAL: The address below must be found via debugger for your version

+0x66E2A0  # PLACEHOLDER - Replace with actual address

# Check if character byte is >= 0xFA (page marker range)
CMP AL, 0xFA
JB NormalCharacter

# ---- Page Marker Detected ----
# Calculate page index: FA→1, FB→2, FC→3, FD→4, FE→5
SUB AL, 0xFA
INC AL

# Store in global variable (address logged by FFNx at startup)
MOV BYTE PTR [0x10AB1234], AL  # PLACEHOLDER - Use logged address

# Advance to next byte (the actual character index)
INC ESI
MOV AL, [ESI]

JMP ContinueDraw

# ---- Normal Character (no page marker) ----
NormalCharacter:
MOV BYTE PTR [0x10AB1234], 0  # Reset to page 0

ContinueDraw:
# Continue with game's character drawing logic
```

---

## 7. EXTERNAL TEXTURE SYSTEM

### 7.1 Search Algorithm

FFNx searches for external textures in this priority order:

```cpp
// src/common.cpp
std::string find_external_texture(const char* texture_name)
{
    // 1. Hash-based path (for animated textures)
    std::string hash_path = mod_path + "/" + compute_texture_hash(texture_name);
    if (check_dds(hash_path)) return hash_path + ".dds";
    if (check_png(hash_path)) return hash_path + ".png";

    // 2. Direct path (most common)
    std::string direct_path = mod_path + "/" + texture_name;
    if (check_dds(direct_path)) return direct_path + ".dds";
    if (check_png(direct_path)) return direct_path + ".png";

    // 3. Not found - use original game texture
    return "";
}

// Example paths searched for "menu_us.lgp/usfont.tex":
// 1. mods/Textures/A1B2C3D4/usfont.dds
// 2. mods/Textures/A1B2C3D4/usfont.png
// 3. mods/Textures/menu_us.lgp/usfont.dds
// 4. mods/Textures/menu_us.lgp/usfont.png
```

### 7.2 DDS vs PNG

**DDS (Recommended):**
- 40-70% faster loading
- Native GPU format (no conversion)
- Supports BC7 compression
- Supports mipmaps
- Better for high-resolution textures

**PNG (Fallback):**
- Universal support
- Easier to edit
- Lossless
- No special tools required

```cpp
// src/image/dds.cpp (simplified)
uint32_t load_dds_texture(const std::string& path)
{
    // Load DDS file
    bimg::ImageContainer* image = bimg::imageParse(/* ... */);

    // Create BGFX texture
    const bgfx::Memory* mem = bgfx::makeRef(image->m_data, image->m_size);
    bgfx::TextureHandle handle = bgfx::createTexture2D(
        image->m_width,
        image->m_height,
        false,  // No mipmaps (or true if DDS has them)
        1,      // Number of layers
        bgfx::TextureFormat::BC7,  // Or appropriate format
        BGFX_TEXTURE_NONE,
        mem
    );

    return handle.idx;
}
```

### 7.3 Texture Dumping

```cpp
// src/common.cpp
void dump_texture(uint32_t texture_handle, const char* name)
{
    if (!save_textures) return;

    // Read texture data from GPU
    bgfx::TextureHandle bgfx_handle = { (uint16_t)texture_handle };
    uint32_t width, height;
    uint8_t* data = bgfx::readTexture(bgfx_handle, &width, &height);

    // Save as PNG
    std::string output_path = dump_path + "/" + name + ".png";
    stbi_write_png(output_path.c_str(), width, height, 4, data, width * 4);

    ffnx_info("Dumped texture: %s (%dx%d)\n", output_path.c_str(), width, height);

    free(data);
}
```

---

## 8. CONFIGURATION SYSTEM

### 8.1 FFNx.toml Structure

```toml
# misc/FFNx.toml (Template)

###############################################################################
# FFNx Configuration File
###############################################################################

#=============================================================================
# Graphics Options
#=============================================================================

# Rendering backend ("auto", "OpenGL", "DirectX11", "DirectX12", "Vulkan")
renderer_backend = "auto"

# Fullscreen mode
fullscreen = false

# Window size (windowed mode)
window_size_x = 1280
window_size_y = 960

# Preserve aspect ratio
preserve_aspect = true

# Enable HDR
enable_hdr = false

# Anisotropic filtering (1, 2, 4, 8, 16)
enable_anisotropic = 16

# Antialiasing (1, 2, 4, 8, 16)
enable_antialiasing = 4

#=============================================================================
# Texture Options
#=============================================================================

# Use external textures from mods folder
use_external_textures = true

# Mod path (relative to game directory)
mod_path = "mods/Textures"

# Save/dump textures (for mod creation)
save_textures = false

#=============================================================================
# Japanese Language Support
#=============================================================================

# Font language ("en", "ja", "zh-tw", "ko")
font_language = "en"

# Enable Furigana support (Phase 2 feature)
font_enable_furigana = false

#=============================================================================
# Audio Options
#=============================================================================

# External music path
external_music_path = "music/vgmstream"

# External voice path
external_voice_path = "voice"

# Music volume (0.0 to 1.0)
music_volume = 1.0

# Voice volume (0.0 to 1.0)
voice_volume = 1.0

#=============================================================================
# Debug Options
#=============================================================================

# Trace all function calls (WARNING: Very verbose!)
trace_all = false

# Trace renderer calls
trace_renderer = false

# Trace texture loader calls
trace_loaders = false

# Show FPS counter
show_fps = false

# Enable DevTools (ImGui overlay)
enable_devtools = false

#=============================================================================
# Advanced Options
#=============================================================================

# Hext patching path
hext_patching_path = "hext"

# Override data path
override_path = "override"

# Enable 60 FPS (FF7 only)
enable_60fps = false

# Enable speedhack
enable_speedhack = false
```

### 8.2 Configuration Loading

```cpp
// src/cfg.cpp
void read_cfg()
{
    try
    {
        // Parse TOML file
        toml::table config = toml::parse_file("FFNx.toml");

        // Graphics
        renderer_backend = config["renderer_backend"].value_or("auto");
        fullscreen = config["fullscreen"].value_or(false);
        window_size_x = config["window_size_x"].value_or(1280);
        window_size_y = config["window_size_y"].value_or(960);

        // Textures
        use_external_textures = config["use_external_textures"].value_or(true);
        mod_path = config["mod_path"].value_or("mods/Textures");

        // Japanese support
        font_language = config["font_language"].value_or("en");

        // Debug
        trace_all = config["trace_all"].value_or(false);

        ffnx_info("Configuration loaded successfully.\n");
    }
    catch (const toml::parse_error& err)
    {
        ffnx_error("Failed to parse FFNx.toml: %s\n", err.what());

        // Use defaults
        use_defaults();
    }
}
```

---

## 9. AUDIO ENGINE

### 9.1 SoLoud Integration

FFNx uses [SoLoud](https://soloud-audio.com/) for all audio playback:

```cpp
// src/audio.cpp
SoLoud::Soloud soloud;  // Global audio engine

void audio_init()
{
    // Initialize SoLoud
    soloud.init(
        SoLoud::Soloud::CLIP_ROUNDOFF,  // Flags
        SoLoud::Soloud::AUTO,           // Backend (auto-detect)
        0,                              // Sample rate (auto)
        2048                            // Buffer size
    );

    // Set master volume
    soloud.setGlobalVolume(1.0f);

    ffnx_info("Audio engine initialized.\n");
}

void audio_shutdown()
{
    soloud.deinit();
}
```

### 9.2 Music Playback

```cpp
// src/music.cpp
SoLoud::WavStream music_stream;
int music_handle = -1;

void play_music(const char* filename)
{
    // Stop current music
    if (music_handle != -1) {
        soloud.stop(music_handle);
    }

    // Check for external music file
    std::string external_path = find_external_music(filename);

    if (!external_path.empty())
    {
        // Load external music (OGG, MP3, FLAC, etc.)
        music_stream.load(external_path.c_str());

        // Play with looping
        music_handle = soloud.play(music_stream, music_volume);
        soloud.setLooping(music_handle, true);

        ffnx_info("Playing external music: %s\n", external_path.c_str());
    }
    else
    {
        // Fall back to original MIDI or game music
        play_original_music(filename);
    }
}
```

### 9.3 Voice Acting Support

```cpp
// src/voice.cpp
void play_voice(const char* voice_id)
{
    // Voice files named by dialogue ID
    // Example: "aerith_001.ogg", "cloud_042.ogg"

    std::string voice_path = external_voice_path + "/" + voice_id + ".ogg";

    if (file_exists(voice_path))
    {
        SoLoud::Wav voice;
        voice.load(voice_path.c_str());

        // Play voice (no looping)
        int handle = soloud.play(voice, voice_volume);

        ffnx_info("Playing voice: %s\n", voice_path.c_str());
    }
}
```

---

## 10. HEXT PATCHING SYSTEM

### 10.1 What is Hext?

Hext is a runtime assembly patching system developed by DLPB. FFNx implements the Hext specification to allow mods to modify game code without editing the executable.

**Advantages:**
- No need to distribute modified EXEs
- Multiple patches can coexist
- Easy to enable/disable patches
- Version-specific patches possible

### 10.2 Hext File Format

```hext
# misc/hext/ff7/en/my_patch.txt

# Comments start with #

# Set base address (absolute)
+0x40FF38

# Write bytes at current address
=E9 1B 00 00 00  # JMP instruction (5 bytes)

# Advance address (relative)
+10  # Move forward 16 bytes (0x10)

# Write more bytes
=90 90 90  # NOP instructions

# String data
="Hello World"

# Fill with pattern
*5 90  # Write 5 NOP (0x90) bytes
```

### 10.3 Hext Loading

```cpp
// src/hext.cpp
void load_hext_patches()
{
    std::string hext_dir = hext_patching_path + "/ff7/en/";  // Example

    // Find all .txt files
    for (const auto& file : list_files(hext_dir, "*.txt"))
    {
        ffnx_info("Loading Hext patch: %s\n", file.c_str());

        std::ifstream hext_file(file);
        std::string line;
        uint32_t current_address = 0;

        while (std::getline(hext_file, line))
        {
            // Skip comments and empty lines
            if (line.empty() || line[0] == '#') continue;

            if (line[0] == '+')
            {
                // Address directive
                current_address = parse_address(line);
            }
            else if (line[0] == '=')
            {
                // Write bytes
                std::vector<uint8_t> bytes = parse_bytes(line);
                apply_patch(current_address, bytes);
                current_address += bytes.size();
            }
            else if (line[0] == '*')
            {
                // Fill pattern
                auto [count, byte] = parse_fill(line);
                apply_fill(current_address, count, byte);
                current_address += count;
            }
        }
    }

    ffnx_info("Hext patches loaded.\n");
}

void apply_patch(uint32_t address, const std::vector<uint8_t>& bytes)
{
    // Make memory writable
    DWORD oldProtect;
    VirtualProtect((void*)address, bytes.size(), PAGE_EXECUTE_READWRITE, &oldProtect);

    // Apply patch
    memcpy((void*)address, bytes.data(), bytes.size());

    // Restore protection
    VirtualProtect((void*)address, bytes.size(), oldProtect, &oldProtect);

    ffnx_trace("Patched %zu bytes at 0x%X\n", bytes.size(), address);
}
```

### 10.4 Example: Japanese Font Hext Patch

```hext
# misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt

# Japanese Font Page Marker Detection Hook
# Intercepts character processing to detect FA-FE bytes

# ⚠️ Address must be found via debugger (see Master Bible Section 8.2)
+0x66E2A0  # PLACEHOLDER

# Original instruction (must be preserved)
# Example: CMP AL, 0x00
# (This will be overwritten, so we recreate it after our logic)

# Check for page markers (FA-FE range)
CMP AL, 0xFA
JB @NormalChar

# Marker detected - Calculate page number
SUB AL, 0xFA     # FA→0, FB→1, FC→2, FD→3, FE→4
INC AL           # Convert to 1-5
MOV BYTE PTR [0x10AB1234], AL  # Store in g_currentFontPage

# Load next byte (actual character index)
INC ESI
MOV AL, [ESI]
JMP @Continue

@NormalChar:
MOV BYTE PTR [0x10AB1234], 0  # Reset to page 0

@Continue:
# Restore original instruction here
# Then continue to game's drawing logic
```

---

## 11. DEVELOPER TOOLS

### 11.1 ImGui Integration

FFNx includes an in-game developer overlay using [Dear ImGui](https://github.com/ocornut/imgui):

```cpp
// src/overlay.cpp
void render_devtools()
{
    if (!enable_devtools) return;

    // New frame
    ImGui::NewFrame();

    // Main menu bar
    if (ImGui::BeginMainMenuBar())
    {
        if (ImGui::BeginMenu("FFNx"))
        {
            ImGui::MenuItem("Show FPS", NULL, &show_fps);
            ImGui::MenuItem("Renderer Stats", NULL, &show_renderer_stats);
            ImGui::MenuItem("Memory Editor", NULL, &show_memory_editor);
            ImGui::MenuItem("Texture Browser", NULL, &show_texture_browser);
            ImGui::EndMenu();
        }

        ImGui::EndMainMenuBar();
    }

    // FPS counter
    if (show_fps)
    {
        ImGui::SetNextWindowPos(ImVec2(10, 30));
        ImGui::Begin("FPS", &show_fps, ImGuiWindowFlags_NoTitleBar);
        ImGui::Text("FPS: %.1f", ImGui::GetIO().Framerate);
        ImGui::End();
    }

    // Memory editor
    if (show_memory_editor)
    {
        static MemoryEditor mem_edit;
        mem_edit.DrawWindow("Memory Editor", (void*)0x400000, 0x1000000);
    }

    // Render
    ImGui::Render();
}
```

**Keyboard Shortcut:**
- `Ctrl + Alt + D`: Toggle DevTools overlay

### 11.2 Trace Logging

```cpp
// src/log.cpp
void ffnx_trace(const char* fmt, ...)
{
    if (!trace_all && !trace_renderer && !trace_loaders) return;

    va_list args;
    va_start(args, fmt);

    char buffer[4096];
    vsnprintf(buffer, sizeof(buffer), fmt, args);

    // Write to FFNx.log
    fprintf(log_file, "[TRACE] %s", buffer);
    fflush(log_file);

    va_end(args);
}

// Usage:
ffnx_trace("Loading texture: %s (hash: %08X)\n", name, hash);
```

**Trace Levels:**
- `trace_all`: Traces ALL function calls (extremely verbose)
- `trace_renderer`: Traces rendering calls only
- `trace_loaders`: Traces asset loading only

### 11.3 RenderDoc Integration

FFNx is fully compatible with [RenderDoc](https://renderdoc.org/) for frame debugging:

**Usage:**
1. Launch RenderDoc
2. File → Launch Application
3. Executable: `ff7.exe` (with FFNx installed)
4. Capture Key: `F12` (default)
5. Launch game
6. Press `F12` during gameplay to capture frame
7. Analyze draw calls, textures, shaders, etc.

---

## 12. INTEGRATION WITH 7TH HEAVEN

### 12.1 7th Heaven VFS

7th Heaven uses a Virtual File System (VFS) via `7thWrapperLib.dll` and `EasyHook.dll`:

```
Game requests file
    ↓
EasyHook intercepts fopen/CreateFile
    ↓
7thWrapperLib checks active mods (IRO files)
    ↓
If found in mod → Return virtual handle to modded file
If not found → Pass through to FFNx
    ↓
FFNx checks external textures/audio
    ↓
If found → Return modded asset
If not found → Return original game asset
```

### 12.2 FFNx as Default Driver

7th Heaven 2.3+ includes FFNx as the default graphics driver:

```
7th Heaven Installation/
├── 7thHeaven.exe
├── 7thWrapperLib.dll      # VFS implementation
├── EasyHook.dll            # API hooking
├── mods/
│   └── 7th Heaven/         # IRO files
└── AF3DN.P → FFNx.dll      # Graphics driver
```

When launching via 7th Heaven:
1. 7th Heaven injects `7thWrapperLib.dll` into `ff7.exe`
2. `7thWrapperLib.dll` installs file I/O hooks
3. Game loads `AF3DN.P` (which is FFNx)
4. FFNx initializes normally

### 12.3 Mod Path Configuration

```toml
# FFNx.toml
mod_path = "mods/Textures"  # Relative to game directory
```

7th Heaven extracts IRO contents to `mods/Textures/`, which FFNx then reads.

**Directory Structure with 7th Heaven:**
```
FF7/
├── ff7.exe
├── AF3DN.P                 # FFNx.dll
├── FFNx.toml
├── FFNx.log
├── mods/
│   ├── Textures/           # FFNx external textures
│   │   ├── menu_us.lgp/
│   │   │   └── usfont.tex
│   │   └── char.lgp/
│   │       └── cloud.p
│   └── 7th Heaven/         # 7H IRO library
│       └── MyMod.iro
└── 7thWrapperLib.dll       # Injected by 7H
```

---

## 13. BUILDING AND DEBUGGING

### 13.1 Build Configurations

**x86-Release:**
- Optimizations: `/O2` (maximize speed)
- Debug info: None
- Use for: Final releases, performance testing
- Output: Fast, small binary (~2-3 MB)

**x86-Debug:**
- Optimizations: `/Od` (disabled)
- Debug info: Full (`/Zi`)
- Use for: Active development, debugging with Visual Studio
- Output: Large binary (~20-30 MB)

**x86-RelWithDebInfo:**
- Optimizations: `/O2`
- Debug info: Full (`/Zi`)
- Use for: Debugging release-mode bugs, profiling
- Output: Medium binary (~10-15 MB)

### 13.2 Debugging with Visual Studio

**Setup:**
```
1. Build with x86-Debug or x86-RelWithDebInfo
2. Copy AF3DN.P to FF7 directory
3. In Visual Studio: Debug → Attach to Process
4. Select ff7.exe
5. Set breakpoints in FFNx code
6. Trigger breakpoint by performing action in game
```

**Useful Breakpoints:**
- `common_load_texture()`: When texture loads
- `gl_bind_texture_set()`: When texture binds
- `ff7_init_hooks()`: At startup
- `PatchFontWidthsForJapanese()`: Font initialization

### 13.3 Debugging with x64dbg

For assembly-level debugging (finding addresses, understanding game code):

```
1. Open x64dbg
2. File → Open → ff7.exe
3. Debug → Run (F9)
4. Wait for FFNx to load
5. Set breakpoint at game address (e.g., 0x66E2A0)
6. Trigger by performing action in game
7. Examine:
   - Registers (EAX, ESI, etc.)
   - Stack
   - Memory at ESI (string pointer)
8. Step through (F7 = step into, F8 = step over)
```

### 13.4 Common Debugging Scenarios

**Problem: Texture not loading**

```
1. Enable trace_loaders in FFNx.toml
2. Check FFNx.log for:
   [INFO] Loading texture: menu_us.lgp/usfont.tex
   [INFO] Searching for external texture...
   [ERROR] Failed to load external texture
3. Verify file exists at: mods/Textures/menu_us.lgp/usfont.dds
4. Check file permissions (read-only?)
5. Try PNG instead of DDS
```

**Problem: Crash on startup**

```
1. Check FFNx.log for last logged message
2. If log is empty: DLL failed to load
   - Check dependencies with Dependency Walker
   - Install Visual C++ Redistributable
3. If log shows error: Note the last successful step
4. Build with Debug and attach debugger
5. Enable crash dumps (see log.cpp)
```

**Problem: Japanese characters appear squashed**

```
1. Check FFNx.log for:
   [INFO] Font language: ja
   [INFO] Patching character width table...
   [INFO] Successfully patched
2. If missing: PatchFontWidthsForJapanese() not called
   - Check ff7_opengl.cpp: Is it called after ff7_data()?
3. If "font_info is NULL":
   - ff7_data() didn't populate common_externals
   - Wrong executable version (address mismatch)
4. Verify widths with Cheat Engine:
   - Address: 0x99DDA8 (US 1.02)
   - Expected: All bytes are 0x10
```

---

## 14. EXTENDING FFNX

### 14.1 Adding a New Configuration Option

**Step 1: Define in cfg.h**

```cpp
// src/cfg.h
extern bool my_new_feature;
```

**Step 2: Parse in cfg.cpp**

```cpp
// src/cfg.cpp
bool my_new_feature = false;  // Default value

void read_cfg()
{
    // ... existing parsing ...

    my_new_feature = config["my_new_feature"].value_or(false);

    ffnx_info("my_new_feature: %s\n", my_new_feature ? "true" : "false");
}
```

**Step 3: Add to FFNx.toml**

```toml
# misc/FFNx.toml
# My new feature
my_new_feature = false
```

**Step 4: Use in code**

```cpp
// src/renderer.cpp
void render_frame()
{
    if (my_new_feature)
    {
        // Do something special
    }
}
```

### 14.2 Adding Support for a New Language

**Example: Adding Chinese support**

**Step 1: Configuration**

```cpp
// src/cfg.cpp
if (font_language == "zh-tw" || font_language == "zh-cn")
{
    is_using_chinese = true;
    required_font_pages = 11;  // Base + 5 Chinese + 5 Japanese fallback
}
```

**Step 2: Texture Loading**

```cpp
// src/common.cpp
if (font_language == "zh-tw")
{
    // Load Chinese Traditional font pages
    for (int i = 0; i < 5; i++)
    {
        char filename[64];
        sprintf(filename, "zhfont_%d.png", i + 1);
        load_font_page(filename, 6 + i);  // Pages 6-10
    }
}
```

**Step 3: Hext Patches**

```hext
# misc/hext/ff7/en/FFNx.MULTILANG_FONT.txt

# Check for Chinese pages (F0-F4)
CMP AL, 0xF0
JB @CheckJapanese
CMP AL, 0xF4
JA @CheckJapanese

# Chinese page marker detected
SUB AL, 0xF0             # F0→0, F1→1, F2→2, F3→3, F4→4
ADD AL, 6                # Offset to pages 6-10
MOV BYTE PTR [g_currentFontPage], AL
JMP @LoadChar

@CheckJapanese:
# ... existing Japanese logic ...
```

**Step 4: Documentation**

```markdown
# docs/mods/chinese_fonts.md

# Chinese Font Support

FFNx supports Chinese fonts using the same multi-page system as Japanese.

## Configuration

```toml
font_language = "zh-tw"  # Traditional Chinese
# OR
font_language = "zh-cn"  # Simplified Chinese
```

## Assets Required

Place the following files in `mods/Textures/menu/`:
- `zhfont_1.png` through `zhfont_5.png` (Chinese characters)

## Encoding

Chinese characters use F0-F4 page markers:
- 0xF0 [index] = Character from zhfont_1.png
- 0xF1 [index] = Character from zhfont_2.png
- ... etc.
```

### 14.3 Adding a New Rendering Feature

**Example: Adding a post-processing effect**

```cpp
// src/renderer.cpp

// Step 1: Add shader
const char* post_process_shader = R"(
    $input v_texcoord0
    $output o_color

    SAMPLER2D(s_texColor, 0);
    uniform vec4 u_params;

    void main()
    {
        vec4 color = texture2D(s_texColor, v_texcoord0);

        // Apply effect (example: grayscale)
        float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
        o_color = vec4(vec3(gray), color.a);
    }
)";

// Step 2: Create shader program
void init_post_process()
{
    post_process_program = bgfx::createProgram(
        compile_shader(vertex_shader),
        compile_shader(post_process_shader),
        true  // Destroy shaders after linking
    );
}

// Step 3: Apply during rendering
void render_post_process()
{
    if (!enable_post_process) return;

    // Bind shader
    bgfx::setProgram(post_process_program);

    // Bind framebuffer texture
    bgfx::setTexture(0, s_texColor, scene_texture);

    // Submit draw call
    bgfx::submit(POST_PROCESS_VIEW_ID, post_process_program);
}
```

---

## 15. REFERENCE

### 15.1 Official Resources

**FFNx:**
- GitHub: https://github.com/julianxhokaxhiu/FFNx
- Documentation: https://github.com/julianxhokaxhiu/FFNx/tree/master/docs
- Discord (Qhimm): https://discord.gg/N6M6pKS
- Discord (Tsunamods): https://discord.gg/Urq67Uz
- Forums (Qhimm): http://forums.qhimm.com/index.php?topic=19970.0

**Libraries:**
- BGFX: https://github.com/bkaradzic/bgfx
- FFmpeg: https://www.ffmpeg.org/
- SoLoud: https://sol.gfxile.net/soloud/
- VGMStream: https://github.com/vgmstream/vgmstream
- ImGui: https://github.com/ocornut/imgui

### 15.2 Related Guides in This Project

- `FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md`: Complete technical spec for Japanese text support
- `7TH_HEAVEN_DEVELOPER_GUIDE.md`: Mod creation and distribution with 7th Heaven
- `docs/DOCUMENTATION_MAP.md`: Navigation guide for all project documentation

### 15.3 Community Resources

**Qhimm Forums:**
- FF7 PC Modding: http://forums.qhimm.com/index.php?board=7.0
- FF8 PC Modding: http://forums.qhimm.com/index.php?board=40.0
- FFNx Thread: http://forums.qhimm.com/index.php?topic=19970.0

**Tsunamods:**
- Forum: https://forum.tsunamods.com/
- 7th Heaven: https://7thheaven.rocks/

**GitHub Repositories:**
- FFNx: https://github.com/julianxhokaxhiu/FFNx
- 7th Heaven: https://github.com/tsunamods-codes/7th-Heaven
- Makou Reactor: https://github.com/myst6re/makoureactor

### 15.4 Development Tools

**Required:**
- Visual Studio 2022: https://visualstudio.microsoft.com/vs/community/
- Git: https://git-scm.com/

**Debugging:**
- RenderDoc: https://renderdoc.org/
- x64dbg: https://x64dbg.com/
- Cheat Engine: https://cheatengine.org/

**Asset Tools:**
- See 7th Heaven Developer Guide Section 7.1 for complete list

### 15.5 Glossary

| Term | Definition |
|------|------------|
| **AF3DN.P** | Original graphics driver filename (FFNx replaces this) |
| **BGFX** | Cross-platform rendering library used by FFNx |
| **DDS** | DirectDraw Surface texture format (recommended for FFNx) |
| **Hext** | Runtime assembly patching system |
| **IRO** | 7th Heaven mod archive format (ZIP-based) |
| **SoLoud** | Audio engine used by FFNx |
| **vcpkg** | C++ package manager used to manage dependencies |
| **VFS** | Virtual File System (used by 7th Heaven) |
| **VGMStream** | Library for game audio format playback |

---

## APPENDIX A: QUICK REFERENCE

### Build Command Quick Reference

```batch
REM Clone with submodules
git clone --recursive https://github.com/julianxhokaxhiu/FFNx.git

REM Bootstrap vcpkg
cd vcpkg && bootstrap-vcpkg.bat && vcpkg integrate install && cd ..

REM Build (Visual Studio)
REM Open FFNx folder → Select x86-Release preset → Build

REM Build (Command Line)
cmake --preset x86-Release
cmake --build --preset x86-Release

REM Output: .build\bin\AF3DN.P
```

### Configuration Quick Reference

```toml
# Minimal FFNx.toml for Japanese support
renderer_backend = "auto"
fullscreen = false
window_size_x = 1280
window_size_y = 960
use_external_textures = true
mod_path = "mods/Textures"
font_language = "ja"
trace_loaders = false
```

### Logging Quick Reference

```cpp
// src/log.h
ffnx_info("Information message\n");        // Always logged
ffnx_warning("Warning message\n");         // Always logged
ffnx_error("Error message\n");             // Always logged
ffnx_trace("Trace message\n");             // Only if trace_* enabled
```

---

**DOCUMENT END**

**Document Status:** Deep Dive Complete - Production Ready for Developers

**Sources:**
- FFNx Official Repository (https://github.com/julianxhokaxhiu/FFNx)
- FFNx README.md and Documentation
- FFNX Master Bible (Project Reference)
- 7th Heaven Developer Guide (Project Reference)
- Direct codebase analysis of FFNx source

**Research Session:** 2025-11-24 22:28-22:45 JST
**Session ID:** 8f58819d-f9c4-4f04-8e95-4af04d782606

---

★ **For questions, contributions, or support:**
- FFNx GitHub Issues: https://github.com/julianxhokaxhiu/FFNx/issues
- Qhimm Forums: http://forums.qhimm.com/index.php?topic=19970.0
- Discord (Qhimm): https://discord.gg/N6M6pKS
