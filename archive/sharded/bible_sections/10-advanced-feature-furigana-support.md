# 10. ADVANCED FEATURE: FURIGANA SUPPORT

**⚠️ NOTE:** This section is for **Phase 2** implementation. Complete and test the core Japanese rendering first.

## 10.1 The Furigana Challenge

**What is Furigana?**

Furigana (振り仮名) are small Hiragana characters placed above (or beside) Kanji to indicate pronunciation. This is critical for language learners.

**Example:**
```
    わたし
私
("watashi" = "I/me")
```

**The Problem:**

FF7's text boxes are designed for **3 lines of 16px text** with **no vertical spacing**:

```
┌──────────────────┐
│ Line 1: 16px     │  ← No space above
│ Line 2: 16px     │
│ Line 3: 16px     │
└──────────────────┘
```

If we render Furigana above Kanji, it will **overlap the previous line**:

```
┌──────────────────┐
│ Previous line    │
│ ふりがな ← Overlap!
│ 振り仮名         │
└──────────────────┘
```

---

## 10.2 Solution Strategy: The "Half-Height" Renderer

**Approach:**

1. Define a new control code: `0xF9` = Furigana Marker
2. Format: `0xF9 [Kanji] [Furigana]`
3. Modify renderer to:
   - Draw Kanji at normal size
   - Draw Furigana at **half size** (8px tall)
   - Position Furigana **above** the Kanji (Y offset: -10px)

**Data Format:**

```
Text stream: 0xF9 0xFA 0x12 0x41 0x42 0x43 0x00

Decoding:
  0xF9         = Furigana marker
  0xFA 0x12    = Kanji character (page 1, index 0x12) = 必
  0x41         = Furigana char 1 (page 0, index 0x41) = ひ
  0x42         = Furigana char 2 (page 0, index 0x42) = つ
  0x43         = Furigana char 3 (page 0, index 0x43) = よう
  0x00         = End marker

Result:
    ひつよう
    必
```

---

## 10.3 Assembly Hook Extension (Hext Patch)

**Extend misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt:**

```hext
# ... existing FA-FE check ...

# [NEW] Check for Furigana marker (0xF9)
CMP AL, 0xF9
JNE NotFurigana

# ---- Furigana Mode ----

# Set Furigana mode flag
MOV BYTE PTR [g_furiganaMode], 1  # Enable flag

# Load Kanji character (next byte)
INC ESI
MOV AL, [ESI]

# Draw the Kanji at normal size
CALL DrawCharacter

# Now draw Furigana characters (small, above)
FuriganaLoop:
    INC ESI
    MOV AL, [ESI]

    # Check for end marker (0x00)
    CMP AL, 0x00
    JE EndFurigana

    # Draw Furigana character (renderer will handle sizing)
    CALL DrawCharacter

    JMP FuriganaLoop

EndFurigana:
    # Disable Furigana mode
    MOV BYTE PTR [g_furiganaMode], 0

    JMP ContinueNormal

NotFurigana:
    # ... existing normal character logic ...
```

**New Global Variable:**

```cpp
// src/globals.h
extern "C" __declspec(dllexport) uint8_t g_furiganaMode;

// src/common.cpp
uint8_t g_furiganaMode = 0;
```

---

## 10.4 Renderer Modification (src/gl/gl.cpp)

**Location: gl_draw_indexed_primitive**

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
    // ... existing setup code ...

    // [NEW] Furigana geometry modification
    if (font_enable_furigana && g_furiganaMode) {
        // We're drawing a Furigana character

        if (trace_all) {
            ffnx_trace("Rendering Furigana character\n");
        }

        // Modify vertices BEFORE submitting to GPU
        for (uint32_t i = 0; i < vertexcount; i++) {
            // Original vertex data:
            float x = vertices[i]._.x;
            float y = vertices[i]._.y;
            float z = vertices[i]._.z;

            // 1. Scale down to 50% (half width, half height)
            float center_x = (vertices[0]._.x + vertices[2]._.x) / 2.0f;
            float center_y = (vertices[0]._.y + vertices[2]._.y) / 2.0f;

            vertices[i]._.x = center_x + (x - center_x) * 0.5f;
            vertices[i]._.y = center_y + (y - center_y) * 0.5f;

            // 2. Shift UP by 10 pixels (to position above Kanji)
            // Note: Adjust multiplier based on rendering resolution
            float y_offset = -10.0f * newRenderer.getScalingFactor();
            vertices[i]._.y += y_offset;
        }
    }

    // ... existing draw call submission ...
}
```

**Scaling Factor Calculation:**

```cpp
// src/renderer.cpp (or renderer.h)

float Renderer::getScalingFactor() {
    // Original FF7 resolution: 640x480
    // If rendering at 1920x1080, scaling factor = 1920/640 = 3.0

    float scale_x = (float)window_width / 640.0f;
    float scale_y = (float)window_height / 480.0f;

    // Use the average to maintain aspect ratio
    return (scale_x + scale_y) / 2.0f;
}
```

---

## 10.5 Line Height Patch (The Hard Part)

**Objective:** Increase vertical spacing between text lines to prevent Furigana overlap.

**Finding the Line Height Variable:**

**Step 1: Memory Search (Cheat Engine)**

1. Open Cheat Engine, attach to FF7 process
2. Search for: **Unknown initial value** (4-byte integer)
3. In-game: Open a menu with text
4. Search for: **Changed value**
5. In-game: Close menu
6. Search for: **Unchanged value**
7. Repeat until you have 1-5 candidates
8. Look for value `16` (0x10) or `24` (0x18)

**Step 2: Verify the Address**

```cpp
// Test by modifying the value
DWORD* line_height_ptr = (DWORD*)0xABCD1234;  // Your found address
*line_height_ptr = 24;  // Try 24px spacing

// Check if text boxes now have more spacing
```

**Step 3: Create a Hext Patch**

```hext
# misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt

# [NEW] Line Height Patch
# Location: Address found via Cheat Engine
+0xABCD1234  # REPLACE WITH ACTUAL ADDRESS

# Original value: 16 (0x10)
# New value: 24 (0x18)
=0x18
```

**Or via C++ at Runtime:**

```cpp
// src/ff7/font.cpp

void PatchLineHeightForFurigana() {
    if (!font_enable_furigana) return;

    // Address found via reverse engineering
    // ⚠️ This is version-specific!
    DWORD* line_height = (DWORD*)0xABCD1234;  // PLACEHOLDER

    DWORD oldProtect;
    VirtualProtect(line_height, sizeof(DWORD), PAGE_READWRITE, &oldProtect);

    *line_height = 24;  // Increase from 16 to 24

    VirtualProtect(line_height, sizeof(DWORD), oldProtect, &oldProtect);

    ffnx_info("Line height increased to 24px for Furigana support.\n");
}
```

**Trade-offs:**

| Line Height | Lines per Box | Furigana Support | Notes |
|-------------|---------------|------------------|-------|
| 16px (original) | 3 lines | ❌ Overlap | Standard FF7 |
| 20px | 2-3 lines | ⚠️ Tight fit | Minimal change |
| 24px | 2 lines | ✅ No overlap | **Recommended** |
| 32px | 2 lines | ✅ Generous spacing | May feel too spacious |

**Recommendation:** Use **24px** for a balance between functionality and aesthetic.

---
