# Implementation Plan: Transparent Menu with Blurred Field Background

**Created:** 2026-01-23 17:14:00 JST (Friday)
**Last Modified:** 2026-01-23 17:14:00 JST (Friday)
**Version:** 1.0.0
**Author:** Claude Code (Session: 8969934f-c366-4a8d-8b0b-4af04d286bd1)
**Project:** FFNx Enhancement - Transparent Menu System

---

## Executive Summary

This document provides a complete implementation plan for adding transparent menu backgrounds with blur effects in FFNx. The approach captures the field's rendered framebuffer when transitioning to the menu module, applies a blur shader, and renders it behind the menu UI with alpha blending.

**Estimated Effort:** 3-4 weeks (experienced C++ developer with graphics programming knowledge)
**Difficulty:** Medium-High
**Risk Level:** Medium (requires careful FFNx integration, testing needed)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Phase 1: Framebuffer Capture System](#phase-1-framebuffer-capture-system)
3. [Phase 2: Blur Shader Implementation](#phase-2-blur-shader-implementation)
4. [Phase 3: Menu Rendering Integration](#phase-3-menu-rendering-integration)
5. [Phase 4: Configuration & Polish](#phase-4-configuration--polish)
6. [Testing Strategy](#testing-strategy)
7. [Risk Mitigation](#risk-mitigation)
8. [Code Reference Guide](#code-reference-guide)

---

## Architecture Overview

### Current System Flow

```text
Field Active:
  field_main_loop() → field_draw_everything() → common_flip()
                                                      ↓
                                           [Screen displays field]

Menu Trigger (e.g., player presses menu button):
  ff7_engine_exit_game_mode(MODE_FIELD) → [field unloaded]
  ff7_engine_enter_game_mode(MODE_MENU)
  menu_main_loop() → menu_draw_everything() → common_flip()
                                                      ↓
                                           [Screen displays menu with fade]
```

### New System Flow

```text
Field Active:
  field_main_loop() → field_draw_everything() → common_flip()
                                                      ↓
                                           [Screen displays field]

Menu Trigger:
  ┌─ INTERCEPT POINT ─────────────────────────────────────┐
  │ 1. Capture current framebuffer to texture             │
  │ 2. Store texture in menu module context               │
  └────────────────────────────────────────────────────────┘
  ff7_engine_exit_game_mode(MODE_FIELD)
  ff7_engine_enter_game_mode(MODE_MENU)
  menu_main_loop() → menu_draw_blurred_background() ←─ [Uses captured texture]
                  → menu_draw_ui() (with alpha)
                  → common_flip()
                                                      ↓
                                [Screen displays menu over blurred field]
```

### Key Components to Implement

| Component | Purpose | Location |
|-----------|---------|----------|
| **Framebuffer Capture** | Save field's last frame to texture | `/src/ff7/menu.cpp` |
| **Blur Shader** | Apply Gaussian blur to captured texture | `/misc/*.frag` + `/src/renderer.cpp` |
| **Menu Background Renderer** | Draw blurred texture behind menu | `/src/ff7/menu.cpp` |
| **Texture Manager** | Cache and release framebuffer textures | `/src/common.cpp` |
| **Configuration** | Enable/disable feature, blur intensity | `FFNx.toml` + `/src/cfg.cpp` |

---

## Phase 1: Framebuffer Capture System

**Duration:** 1 week
**Files Modified:** 3
**New Files:** 1

### Task 1.1: Create Framebuffer Capture Module

**File:** `/src/ff7/framebuffer_capture.h` (NEW)

```cpp
// framebuffer_capture.h
#ifndef FF7_FRAMEBUFFER_CAPTURE_H
#define FF7_FRAMEBUFFER_CAPTURE_H

#include "../common.h"

// Framebuffer capture state
struct framebuffer_capture_state {
    uint32_t texture_handle;        // BGFX texture handle for captured frame
    uint32_t width;                 // Framebuffer width
    uint32_t height;                // Framebuffer height
    bool is_valid;                  // Whether capture is available
    uint64_t capture_timestamp;     // When capture was taken (for cache invalidation)
};

// Global capture state (singleton)
extern framebuffer_capture_state g_menu_background_capture;

// API Functions
bool framebuffer_capture_init();
void framebuffer_capture_shutdown();
bool framebuffer_capture_field_to_texture();
void framebuffer_capture_release();
uint32_t framebuffer_capture_get_texture();

#endif // FF7_FRAMEBUFFER_CAPTURE_H
```

**File:** `/src/ff7/framebuffer_capture.cpp` (NEW)

```cpp
// framebuffer_capture.cpp
#include "framebuffer_capture.h"
#include "../renderer.h"
#include "../log.h"

framebuffer_capture_state g_menu_background_capture = {0};

bool framebuffer_capture_init() {
    ffnx_info("Initializing framebuffer capture system...\n");

    g_menu_background_capture.texture_handle = 0;
    g_menu_background_capture.width = window_size_x;
    g_menu_background_capture.height = window_size_y;
    g_menu_background_capture.is_valid = false;
    g_menu_background_capture.capture_timestamp = 0;

    return true;
}

void framebuffer_capture_shutdown() {
    framebuffer_capture_release();
}

bool framebuffer_capture_field_to_texture() {
    // Get current framebuffer dimensions
    uint32_t fb_width = window_size_x;
    uint32_t fb_height = window_size_y;

    ffnx_trace("Capturing framebuffer: %dx%d\n", fb_width, fb_height);

    // Create texture if needed
    if (g_menu_background_capture.texture_handle == 0) {
        // Create BGFX texture for framebuffer capture
        bgfx::TextureHandle tex_handle = bgfx::createTexture2D(
            fb_width,
            fb_height,
            false,                              // No mipmaps
            1,                                  // 1 layer
            bgfx::TextureFormat::RGBA8,         // 8-bit RGBA
            BGFX_TEXTURE_RT |                   // Render target
            BGFX_TEXTURE_BLIT_DST              // Can be blit destination
        );

        if (!bgfx::isValid(tex_handle)) {
            ffnx_error("Failed to create framebuffer capture texture!\n");
            return false;
        }

        g_menu_background_capture.texture_handle = tex_handle.idx;
        g_menu_background_capture.width = fb_width;
        g_menu_background_capture.height = fb_height;
    }

    // Blit current framebuffer to our capture texture
    bgfx::TextureHandle capture_tex = {(uint16_t)g_menu_background_capture.texture_handle};

    // Get current frame buffer (FFNx manages this internally)
    bgfx::FrameBufferHandle current_fb = bgfx::getFrameBuffer();

    // Blit operation: copy frame buffer to texture
    bgfx::blit(
        0,                          // View ID
        capture_tex,                // Destination texture
        0, 0,                       // Dest X, Y
        bgfx::getTexture(current_fb), // Source texture (from framebuffer)
        0, 0,                       // Source X, Y
        fb_width, fb_height         // Width, Height
    );

    g_menu_background_capture.is_valid = true;
    g_menu_background_capture.capture_timestamp = bgfx::getFrameNum();

    ffnx_trace("Framebuffer captured successfully.\n");
    return true;
}

void framebuffer_capture_release() {
    if (g_menu_background_capture.texture_handle != 0) {
        bgfx::TextureHandle tex = {(uint16_t)g_menu_background_capture.texture_handle};
        bgfx::destroy(tex);
        g_menu_background_capture.texture_handle = 0;
    }

    g_menu_background_capture.is_valid = false;
}

uint32_t framebuffer_capture_get_texture() {
    if (g_menu_background_capture.is_valid) {
        return g_menu_background_capture.texture_handle;
    }
    return 0;
}
```

### Task 1.2: Hook Menu Entry Point

**File:** `/src/ff7/misc.cpp`

**Location:** In `ff7_engine_exit_game_mode()` function (around line 44-68)

```cpp
// EXISTING CODE:
void ff7_engine_exit_game_mode(struct ff7_game_obj *game_object) {
    if (game_object->engine_loop_obj.exit_callback) {
        game_object->engine_loop_obj.exit_callback((game_obj*)game_object);
    }
}

// ADD BEFORE EXIT CALLBACK:
void ff7_engine_exit_game_mode(struct ff7_game_obj *game_object) {
    // NEW: Capture framebuffer when leaving field mode for menu
    if (enable_transparent_menu_blur) {  // Config flag
        uint8_t current_mode = game_object->engine_loop_obj.current_mode;
        uint8_t next_mode = game_object->engine_loop_obj.next_mode;

        // Capture field when transitioning to menu
        if (current_mode == FF7_MODE_FIELD && next_mode == FF7_MODE_MENU) {
            ffnx_info("Capturing field framebuffer for menu background...\n");
            framebuffer_capture_field_to_texture();
        }
    }

    // EXISTING CODE CONTINUES:
    if (game_object->engine_loop_obj.exit_callback) {
        game_object->engine_loop_obj.exit_callback((game_obj*)game_object);
    }
}
```

### Task 1.3: Add to Build System

**File:** `CMakeLists.txt`

Add to source files list:
```cmake
# Around line where other ff7/*.cpp files are listed
src/ff7/framebuffer_capture.cpp
src/ff7/framebuffer_capture.h
```

### Task 1.4: Initialize in FFNx Startup

**File:** `/src/common.cpp`

**Location:** In `init()` function

```cpp
// In init() function, after other subsystem initialization:
void init() {
    // ... existing initialization code ...

    // Initialize framebuffer capture system
    if (enable_transparent_menu_blur) {
        if (!framebuffer_capture_init()) {
            ffnx_error("Failed to initialize framebuffer capture. Feature disabled.\n");
            enable_transparent_menu_blur = false;
        }
    }
}

// In shutdown() function:
void shutdown() {
    // ... existing shutdown code ...

    // Cleanup framebuffer capture
    framebuffer_capture_shutdown();
}
```

---

## Phase 2: Blur Shader Implementation

**Duration:** 1 week
**Files Modified:** 2
**New Files:** 2

### Task 2.1: Create Blur Fragment Shader

**File:** `/misc/FFNx.menu_blur.frag` (NEW)

```glsl
// FFNx.menu_blur.frag
// Gaussian Blur Fragment Shader for Menu Background

$input v_texcoord0

#include "FFNx.common.sh"

SAMPLER2D(s_texture, 0);  // Input texture (captured field)

uniform vec4 u_blur_params;
// u_blur_params.x = blur radius (pixels)
// u_blur_params.y = texture width
// u_blur_params.z = texture height
// u_blur_params.w = blur intensity (0.0-1.0)

void main() {
    vec2 texel_size = vec2(1.0 / u_blur_params.y, 1.0 / u_blur_params.z);
    float blur_radius = u_blur_params.x;
    float intensity = u_blur_params.w;

    vec4 color = vec4(0.0);
    float total_weight = 0.0;

    // Gaussian kernel (9x9 for good quality)
    // Weights for 2D Gaussian approximation
    const int kernel_size = 4;  // Radius in pixels

    for (int x = -kernel_size; x <= kernel_size; x++) {
        for (int y = -kernel_size; y <= kernel_size; y++) {
            vec2 offset = vec2(float(x), float(y)) * texel_size * blur_radius;
            vec2 sample_coord = v_texcoord0 + offset;

            // Gaussian weight calculation
            float dist = length(vec2(x, y));
            float weight = exp(-(dist * dist) / (2.0 * blur_radius * blur_radius));

            color += texture2D(s_texture, sample_coord) * weight;
            total_weight += weight;
        }
    }

    // Normalize
    color /= total_weight;

    // Mix between blurred and original based on intensity
    vec4 original = texture2D(s_texture, v_texcoord0);
    gl_FragColor = mix(original, color, intensity);
}
```

**File:** `/misc/FFNx.menu_blur.vert` (NEW)

```glsl
// FFNx.menu_blur.vert
// Vertex Shader for Menu Background

$input a_position, a_texcoord0
$output v_texcoord0

#include "FFNx.common.sh"

void main() {
    gl_Position = mul(u_modelViewProj, vec4(a_position, 1.0));
    v_texcoord0 = a_texcoord0;
}
```

### Task 2.2: Integrate Shader into Renderer

**File:** `/src/renderer.cpp`

Add shader program handle:
```cpp
// Near other shader program declarations (search for "ProgramHandle"):
bgfx::ProgramHandle menu_blur_program = BGFX_INVALID_HANDLE;
bgfx::UniformHandle u_blur_params = BGFX_INVALID_HANDLE;
```

Initialize shader in `renderer_init()`:
```cpp
// In renderer_init() function, after other shader loading:
void renderer_init() {
    // ... existing shader initialization ...

    // Load menu blur shader
    if (enable_transparent_menu_blur) {
        ffnx_info("Loading menu blur shader...\n");

        bgfx::ShaderHandle vsh = load_shader("FFNx.menu_blur.vert");
        bgfx::ShaderHandle fsh = load_shader("FFNx.menu_blur.frag");

        if (bgfx::isValid(vsh) && bgfx::isValid(fsh)) {
            menu_blur_program = bgfx::createProgram(vsh, fsh, true);

            if (bgfx::isValid(menu_blur_program)) {
                // Create uniform for blur parameters
                u_blur_params = bgfx::createUniform("u_blur_params", bgfx::UniformType::Vec4);
                ffnx_info("Menu blur shader loaded successfully.\n");
            } else {
                ffnx_error("Failed to create menu blur shader program!\n");
            }
        } else {
            ffnx_error("Failed to load menu blur shaders!\n");
        }
    }
}
```

Cleanup shader in `renderer_shutdown()`:
```cpp
void renderer_shutdown() {
    // ... existing cleanup ...

    if (bgfx::isValid(menu_blur_program)) {
        bgfx::destroy(menu_blur_program);
    }

    if (bgfx::isValid(u_blur_params)) {
        bgfx::destroy(u_blur_params);
    }
}
```

### Task 2.3: Create Blur Rendering Function

**File:** `/src/renderer.h`

Add function declaration:
```cpp
// Public API for blur rendering
void renderer_draw_blurred_texture(uint32_t texture_handle, float blur_radius, float intensity);
```

**File:** `/src/renderer.cpp`

Implement rendering function:
```cpp
void renderer_draw_blurred_texture(uint32_t texture_handle, float blur_radius, float intensity) {
    if (!bgfx::isValid(menu_blur_program)) {
        ffnx_error("Menu blur program not initialized!\n");
        return;
    }

    // Set blur parameters uniform
    float params[4] = {
        blur_radius,                    // Blur radius in pixels
        (float)window_size_x,          // Texture width
        (float)window_size_y,          // Texture height
        intensity                       // Blur intensity (0-1)
    };
    bgfx::setUniform(u_blur_params, params);

    // Bind captured texture
    bgfx::TextureHandle tex = {(uint16_t)texture_handle};
    bgfx::setTexture(0, s_texture, tex);

    // Set render state (no depth test, alpha blend)
    uint64_t state = 0
        | BGFX_STATE_WRITE_RGB
        | BGFX_STATE_WRITE_A
        | BGFX_STATE_BLEND_ALPHA;
    bgfx::setState(state);

    // Create full-screen quad vertices
    struct PosTexVertex {
        float x, y, z;
        float u, v;
    };

    PosTexVertex vertices[4] = {
        {-1.0f, -1.0f, 0.0f, 0.0f, 1.0f},  // Bottom-left
        { 1.0f, -1.0f, 0.0f, 1.0f, 1.0f},  // Bottom-right
        { 1.0f,  1.0f, 0.0f, 1.0f, 0.0f},  // Top-right
        {-1.0f,  1.0f, 0.0f, 0.0f, 0.0f}   // Top-left
    };

    uint16_t indices[6] = {0, 1, 2, 0, 2, 3};

    // Create transient buffers
    bgfx::TransientVertexBuffer tvb;
    bgfx::TransientIndexBuffer tib;

    if (bgfx::allocTransientBuffers(&tvb, vertex_layout, 4, &tib, 6)) {
        memcpy(tvb.data, vertices, sizeof(vertices));
        memcpy(tib.data, indices, sizeof(indices));

        bgfx::setVertexBuffer(0, &tvb);
        bgfx::setIndexBuffer(&tib);

        // Submit draw call
        bgfx::submit(MENU_BACKGROUND_VIEW_ID, menu_blur_program);
    }
}
```

---

## Phase 3: Menu Rendering Integration

**Duration:** 1 week
**Files Modified:** 2

### Task 3.1: Add Background Rendering to Menu Module

**File:** `/src/ff7/menu.cpp`

**Location:** In `menu_draw_everything_6CC9D3()` or equivalent menu rendering function

```cpp
// EXISTING FUNCTION (find the menu drawing function):
void menu_draw_everything_6CC9D3(struct game_obj *game_object) {
    // NEW: Draw blurred field background FIRST (before menu elements)
    if (enable_transparent_menu_blur) {
        uint32_t captured_texture = framebuffer_capture_get_texture();

        if (captured_texture != 0) {
            // Draw blurred background
            renderer_draw_blurred_texture(
                captured_texture,
                menu_blur_radius,      // From config (e.g., 5.0)
                menu_blur_intensity    // From config (e.g., 0.8)
            );
        }
    }

    // EXISTING CODE: Draw menu elements (these now render on top)
    // ... original menu drawing code ...
}
```

### Task 3.2: Add Alpha Blending to Menu Graphics Objects

**File:** `/src/ff7/menu.cpp`

Find where menu graphics objects are drawn and modify their alpha:

```cpp
// Search for menu graphics object drawing code
// Typically looks like: engine_draw_graphics_object(menu_graphics_obj, ...)

// ADD BEFORE DRAWING:
if (enable_transparent_menu_blur) {
    // Set menu graphics to semi-transparent
    menu_graphics_obj->vertex_alpha = menu_ui_alpha;  // From config (e.g., 230 for ~90% opacity)
    menu_graphics_obj->field_4 |= BIT(V_ALPHABLEND);  // Enable alpha blending
}

// THEN: existing drawing code
engine_draw_graphics_object(menu_graphics_obj, ...);
```

### Task 3.3: Release Capture When Exiting Menu

**File:** `/src/ff7/misc.cpp`

**Location:** In module exit code

```cpp
void ff7_engine_exit_game_mode(struct ff7_game_obj *game_object) {
    uint8_t current_mode = game_object->engine_loop_obj.current_mode;

    // NEW: Release captured framebuffer when leaving menu
    if (current_mode == FF7_MODE_MENU && enable_transparent_menu_blur) {
        ffnx_info("Releasing menu background capture...\n");
        framebuffer_capture_release();
    }

    // EXISTING CODE:
    if (game_object->engine_loop_obj.exit_callback) {
        game_object->engine_loop_obj.exit_callback((game_obj*)game_object);
    }
}
```

---

## Phase 4: Configuration & Polish

**Duration:** 3-5 days
**Files Modified:** 3

### Task 4.1: Add Configuration Options

**File:** `misc/FFNx.toml`

Add new section:
```toml
###############################################################################
# Transparent Menu with Blur Effect
###############################################################################

# Enable transparent menu with blurred field background
# When enabled, opening the menu will show a blurred version of the field
# underneath instead of fading to black
enable_transparent_menu_blur = false

# Blur radius in pixels (higher = more blur, but slower performance)
# Recommended range: 3.0 - 10.0
# Default: 5.0
menu_blur_radius = 5.0

# Blur intensity (0.0 = no blur, 1.0 = maximum blur)
# Recommended range: 0.5 - 1.0
# Default: 0.8
menu_blur_intensity = 0.8

# Menu UI opacity (0 = fully transparent, 255 = fully opaque)
# This controls how see-through the menu elements are
# Recommended range: 200 - 255
# Default: 230 (about 90% opaque)
menu_ui_alpha = 230
```

**File:** `/src/cfg.h`

Add global variables:
```cpp
// Transparent menu configuration
extern bool enable_transparent_menu_blur;
extern float menu_blur_radius;
extern float menu_blur_intensity;
extern uint8_t menu_ui_alpha;
```

**File:** `/src/cfg.cpp`

Define and parse configuration:
```cpp
// Define globals
bool enable_transparent_menu_blur = false;
float menu_blur_radius = 5.0f;
float menu_blur_intensity = 0.8f;
uint8_t menu_ui_alpha = 230;

// In read_cfg() function:
void read_cfg() {
    // ... existing config parsing ...

    // Parse transparent menu settings
    enable_transparent_menu_blur = config["enable_transparent_menu_blur"].value_or(false);
    menu_blur_radius = config["menu_blur_radius"].value_or(5.0f);
    menu_blur_intensity = config["menu_blur_intensity"].value_or(0.8f);
    menu_ui_alpha = config["menu_ui_alpha"].value_or(230);

    // Validation
    if (menu_blur_radius < 0.0f) menu_blur_radius = 0.0f;
    if (menu_blur_radius > 20.0f) menu_blur_radius = 20.0f;

    if (menu_blur_intensity < 0.0f) menu_blur_intensity = 0.0f;
    if (menu_blur_intensity > 1.0f) menu_blur_intensity = 1.0f;

    ffnx_info("Transparent menu blur: %s\n", enable_transparent_menu_blur ? "enabled" : "disabled");
    if (enable_transparent_menu_blur) {
        ffnx_info("  Blur radius: %.1f\n", menu_blur_radius);
        ffnx_info("  Blur intensity: %.2f\n", menu_blur_intensity);
        ffnx_info("  Menu UI alpha: %d\n", menu_ui_alpha);
    }
}
```

### Task 4.2: Add Performance Monitoring

**File:** `/src/ff7/framebuffer_capture.cpp`

Add timing metrics:
```cpp
bool framebuffer_capture_field_to_texture() {
    uint64_t start_time = get_time_us();  // Microsecond timer

    // ... existing capture code ...

    uint64_t end_time = get_time_us();
    float capture_time_ms = (end_time - start_time) / 1000.0f;

    if (trace_all || trace_renderer) {
        ffnx_trace("Framebuffer capture took %.2f ms\n", capture_time_ms);
    }

    return true;
}
```

### Task 4.3: Add Fallback Behavior

**File:** `/src/ff7/menu.cpp`

Handle failure cases gracefully:
```cpp
void menu_draw_everything_6CC9D3(struct game_obj *game_object) {
    if (enable_transparent_menu_blur) {
        uint32_t captured_texture = framebuffer_capture_get_texture();

        if (captured_texture != 0) {
            // Draw blurred background
            renderer_draw_blurred_texture(captured_texture, menu_blur_radius, menu_blur_intensity);
        } else {
            // FALLBACK: Capture failed, use traditional fade
            ffnx_warning("No captured framebuffer available, using default menu rendering.\n");
            // Let existing menu fade code handle it
        }
    }

    // Existing menu drawing code...
}
```

---

## Testing Strategy

### Unit Testing

1. **Framebuffer Capture**
   - Test capture at different resolutions (640x480, 1280x720, 1920x1080)
   - Verify texture is valid after capture
   - Test memory cleanup (no leaks)

2. **Blur Shader**
   - Test different blur radii (1.0, 5.0, 10.0, 20.0)
   - Verify intensity parameter works (0.0 to 1.0)
   - Test performance impact at different resolutions

3. **Configuration**
   - Verify all config options are parsed correctly
   - Test with invalid values (negative, too large)
   - Test enabling/disabling feature

### Integration Testing

1. **Module Transitions**
   - Field → Menu → Field (basic cycle)
   - Field → Battle → Field → Menu (with battle in between)
   - Field → Save Menu → Field
   - Field → Equipment Menu → Field
   - Test with different field locations (indoor, outdoor, cutscenes)

2. **Edge Cases**
   - Rapid menu open/close
   - Menu open during fade transitions
   - Alt-tab while menu is open
   - Resolution changes while menu is open
   - Mod compatibility (texture mods, field mods)

3. **Performance Testing**
   - FPS impact measurement (target: <5% drop)
   - Memory usage (capture texture should be ~8MB at 1920x1080)
   - Shader compilation time
   - Test on low-end hardware (integrated graphics)

### Visual Testing Checklist

- [ ] Blurred field is recognizable but not too clear
- [ ] Menu elements are readable and properly contrasted
- [ ] No visual artifacts (tearing, flickering)
- [ ] Blur looks smooth and natural (no pixelation)
- [ ] Menu UI alpha works correctly
- [ ] Transition from field to menu is smooth
- [ ] Transition from menu to field is smooth
- [ ] Works with all menu types (main, battle, save, equipment, etc.)

---

## Risk Mitigation

### Known Risks & Solutions

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **BGFX API changes** | Medium | High | Version lock BGFX, add compatibility layer |
| **Performance on old hardware** | High | Medium | Make feature optional, add quality presets |
| **Mod compatibility issues** | Medium | Medium | Test with popular mods, add compatibility flags |
| **Capture timing issues** | Medium | High | Add multiple capture attempts, fallback to no blur |
| **Memory leaks** | Low | High | Strict resource management, automated testing |
| **Shader compilation failures** | Low | Medium | Fallback to no blur, better error messages |

### Compatibility Considerations

1. **7th Heaven Mods**
   - Test with popular texture replacements
   - Ensure captured framebuffer includes modded textures
   - Document any incompatibilities

2. **FFNx Features**
   - Ensure compatibility with HDR mode
   - Test with different render backends (DX11, DX12, Vulkan, OpenGL)
   - Verify works with external textures enabled

3. **Game Versions**
   - Test with Steam version
   - Test with original PC version
   - Test with different language versions

---

## Code Reference Guide

### Key FFNx Functions to Study

| Function | File | Purpose |
|----------|------|---------|
| `ff7_engine_exit_game_mode()` | `/src/ff7/misc.cpp` | Module switching logic |
| `common_begin_scene()` | `/src/common.cpp` | Scene rendering start |
| `common_end_scene()` | `/src/common.cpp` | Scene rendering end |
| `common_flip()` | `/src/common.cpp` | Present frame to screen |
| `menu_draw_everything_6CC9D3()` | `/src/ff7/menu.cpp` | Main menu drawing |
| `field_draw_everything()` | `/src/ff7/field/field.cpp` | Field rendering |
| `engine_draw_graphics_object()` | `/src/ff7_data.h` | Graphics object rendering |

### Important Data Structures

```cpp
// Game object (main game state)
struct ff7_game_obj {
    struct engine_loop_obj engine_loop_obj;  // Module state
    uint32_t in_scene;                       // Scene depth counter
    // ... many other fields
};

// Graphics object (drawable entity)
struct ff7_graphics_object {
    void* texture_handle;
    uint32_t field_4;          // Blend mode flags
    uint8_t vertex_alpha;      // Alpha value (0-255)
    // ... other fields
};

// BGFX texture handle
struct bgfx::TextureHandle {
    uint16_t idx;  // Internal texture ID
};
```

### Useful Macros

```cpp
// Set alpha blending on graphics object
graphics_obj->field_4 |= BIT(V_ALPHABLEND);

// Enable texture mapping blend
graphics_obj->field_4 |= BIT(V_TMAPBLEND);

// Access game object fields safely
VREF(game_object, in_scene)
VRASS(game_object, in_scene, value)
```

---

## Build & Deployment

### Build Steps

```bash
# 1. Ensure FFNx codebase is up to date
cd /c/FFNx
git pull

# 2. Apply changes from this implementation plan
# (All file modifications described above)

# 3. Rebuild shaders
cd misc
# Shaders are compiled automatically by CMake

# 4. Build FFNx
cd ..
mkdir -p .build
cd .build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release

# 5. Test build
# Copy FFNx.dll to FF7 directory and test
```

### Deployment Checklist

- [ ] Code changes compiled without errors
- [ ] Shaders compiled successfully
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Performance benchmarks acceptable
- [ ] Documentation updated
- [ ] Configuration template updated
- [ ] Changelog entry added

---

## Timeline

### Week 1: Framebuffer Capture System
- Days 1-2: Implement framebuffer capture module
- Day 3: Hook menu entry point
- Days 4-5: Testing and debugging capture logic

### Week 2: Blur Shader Implementation
- Days 1-2: Write and test blur shaders
- Day 3: Integrate shader into renderer
- Days 4-5: Performance optimization and testing

### Week 3: Menu Rendering Integration
- Days 1-2: Modify menu drawing code
- Day 3: Add alpha blending to menu elements
- Days 4-5: Testing and bug fixes

### Week 4: Configuration & Polish
- Days 1-2: Add configuration options
- Day 3: Performance monitoring and fallbacks
- Days 4-5: Final testing and documentation

**Total Estimated Time:** 20-28 days (4 weeks)

---

## Success Criteria

The implementation will be considered successful when:

1. **Functionality**
   - ✅ Menu opens with blurred field background
   - ✅ Menu UI is semi-transparent and readable
   - ✅ Transition is smooth (no stuttering)
   - ✅ Works across all menu types

2. **Performance**
   - ✅ FPS drop < 5% when menu is open
   - ✅ Memory usage increase < 10MB
   - ✅ Capture time < 5ms on average hardware

3. **Quality**
   - ✅ No visual artifacts or glitches
   - ✅ Blur effect looks professional
   - ✅ Menu elements properly composited

4. **Compatibility**
   - ✅ Works with major mods (7th Heaven)
   - ✅ Compatible with all render backends
   - ✅ Graceful fallback when feature disabled

5. **Usability**
   - ✅ Easy to enable/disable via config
   - ✅ Configurable parameters work as expected
   - ✅ Clear documentation for users

---

## Future Enhancements

After initial implementation is stable, consider:

1. **Live Field Updates** (Advanced)
   - Continue field animations while menu is open
   - Requires keeping field module active
   - Major architectural change

2. **Variable Blur Zones**
   - Blur field more at screen edges
   - Keep center sharper for context
   - Artistic enhancement

3. **Motion Blur Effect**
   - Subtle blur based on camera movement
   - Adds "polish" to transitions

4. **Hotkey Toggle**
   - Allow users to toggle blur on/off in-game
   - Preview different blur settings

---

## References

- FFNx GitHub: https://github.com/julianxhokaxhiu/FFNx
- BGFX Documentation: https://bkaradzic.github.io/bgfx/
- Gaussian Blur Theory: https://en.wikipedia.org/wiki/Gaussian_blur
- FFNx Developer Guide: `/docs/FFNX_DEVELOPER_GUIDE.md` (this project)

---

**Document End**

**Status:** Ready for Implementation
**Next Action:** Begin Phase 1 - Framebuffer Capture System
**Recommended Review:** Have FFNx maintainer review plan before starting
