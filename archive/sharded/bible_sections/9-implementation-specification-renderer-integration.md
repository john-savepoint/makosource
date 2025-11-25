# 9. IMPLEMENTATION SPECIFICATION: RENDERER INTEGRATION

## 9.1 Reading the Font Page Variable (src/gl/gl.cpp)

**Objective:** Hook the texture binding logic to read `g_currentFontPage` and bind the correct texture.

**Location: gl_bind_texture_set function**

```cpp
// src/gl/gl.cpp

#include "../globals.h"  // [NEW] For g_currentFontPage

void gl_bind_texture_set(struct texture_set *_texture_set)
{
    // ... existing code ...

    VOBJ(texture_set, texture_set, _texture_set);

    if (!VPTR(texture_set)) {
        return;  // Safety check
    }

    // [NEW] Japanese font page switching logic
    if (font_language == "ja") {
        // Detect if this is a font texture
        // We can check the number of allocated textures (fonts have 6)
        uint32_t num_textures = VREF(texture_set, ogl.gl_set->textures);

        if (num_textures == 6) {
            // This is a Japanese font texture set

            // Read the current page from the global variable
            // (Set by the Assembly hook in the game's text parser)
            uint8_t requested_page = g_currentFontPage;

            // Safety check: clamp to valid range (0-5)
            if (requested_page > 5) {
                ffnx_warning("Invalid font page: %d. Clamping to 5.\n", requested_page);
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
                ffnx_error("Font page %d has NULL texture handle!\n", requested_page);
            }

            // Early return - we've handled this texture
            return;
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

**Alternative: More Explicit Detection**

```cpp
// Option: Add a flag to texture_set to mark it as a font
struct texture_set {
    // ... existing fields ...
    bool is_japanese_font;  // [NEW] Flag set during loading
};

// During loading (in load_external_texture):
if (font_language == "ja" && is_font_texture) {
    VRASS(texture_set, is_japanese_font, true);
}

// In gl_bind_texture_set:
if (VREF(texture_set, is_japanese_font)) {
    uint8_t page = g_currentFontPage;
    // ... bind logic ...
}
```

---

## 9.2 Handling Palette Change Events (src/common.cpp)

**Background:**

The game sometimes calls `common_palette_changed` to request a palette swap. For normal textures, this is a color variation. For our fonts, we might receive this call even though we're handling page switching ourselves.

**Location: common_palette_changed function**

```cpp
// src/common.cpp

void common_palette_changed(
    uint32_t new_palette_index,
    struct texture_set* texture_set)
{
    if (!texture_set) return;

    VOBJ(texture_set, tex, texture_set);

    // [NEW] Special handling for Japanese fonts
    if (font_language == "ja") {
        uint32_t num_textures = VREF(tex, ogl.gl_set->textures);

        if (num_textures == 6) {
            // This is a Japanese font - ignore game's palette request
            // because we're controlling pages via g_currentFontPage

            if (trace_all) {
                ffnx_trace("Ignoring palette change for Japanese font (controlled by g_currentFontPage)\n");
            }

            return;  // Don't process this request
        }
    }

    // [ORIGINAL] Standard palette change logic
    if (new_palette_index >= VREF(tex, ogl.gl_set->textures)) {
        ffnx_warning("Palette index %d out of range (max: %d)\n",
                     new_palette_index, VREF(tex, ogl.gl_set->textures) - 1);
        return;
    }

    VRASS(tex, palette_index, new_palette_index);

    // Rebind texture
    gl_bind_texture_set(texture_set);
}
```

---

## 9.3 Rendering Pipeline Integration (src/gl/gl.cpp)

**Understanding the Draw Call Flow:**

```
Game requests character draw
    ↓
gl_draw_indexed_primitive(vertices, texture_set)
    ↓
gl_bind_texture_set(texture_set)  ← We hook here
    ↓
gl_set_texture(handle, unit)
    ↓
BGFX Draw Call
    ↓
GPU renders character
```

**Location: gl_draw_indexed_primitive function**

Add diagnostic logging (optional, for debugging):

```cpp
// src/gl/gl.cpp

void gl_draw_indexed_primitive(
    uint32_t primitivetype,
    uint32_t vertexcount,
    uint32_t indexcount,
    struct nvertex *vertices,
    uint16_t *indices,
    struct graphics_object *graphics_object)
{
    // ... existing code ...

    // [NEW] Font-specific logging (enable only during debugging)
    #ifdef DEBUG_JAPANESE_FONTS
    if (font_language == "ja" && current_state.texture_set) {
        uint32_t num_tex = VREF(current_state.texture_set, ogl.gl_set->textures);
        if (num_tex == 6) {
            ffnx_trace("Drawing Japanese font character:\n");
            ffnx_trace("  Current page: %d\n", g_currentFontPage);
            ffnx_trace("  Vertex count: %d\n", vertexcount);
            ffnx_trace("  Texture handle: 0x%X\n",
                       VREF(current_state.texture_set,
                            texturehandle[g_currentFontPage]));
        }
    }
    #endif

    // ... rest of draw logic ...
}
```

**Compile-time Debug Flag:**

```cpp
// src/globals.h

// Uncomment to enable verbose Japanese font debugging
// #define DEBUG_JAPANESE_FONTS
```

---
