# Japanese Menu System Investigation - Complete Findings

**Created:** 2026-01-23 14:27 JST (Friday)
**Session ID:** 2844b4cc-5276-48d1-8630-807bff87b3dc
**Author:** John Zealand-Doyle
**Investigation Scope:** Japanese text encoding, byte allocation, multi-language applicability

---

## Executive Summary

The Japanese menu system in FF7 uses a **hybrid single/double-byte encoding architecture** combined with a **multi-page font texture system** to overcome the 256-character limitation of the original English game. The solution is elegant: it repurposes unused control codes (0xFA-0xFE) as texture page markers, enabling 1,536 character slots across 6 font pages while maintaining the same byte allocation constraints as English.

**Critical Discovery:** Japanese doesn't "overcome" the 4-byte allocation problem for "Yes/No"—it **uses the exact same byte allocations** as English by encoding Hiragana/Katakana in the same single-byte index pool (0x00-0xFF) as English ASCII characters. The magic happens at the **rendering layer**, not the storage layer.

---

## 1. The Byte Allocation "Trick" Explained

### 1.1 The Fundamental Architecture

**Question:** How does Japanese fit into 4 bytes when it uses double-byte characters?

**Answer:** It doesn't use double-byte characters for basic text like "Yes" (はい) or "No" (いいえ).

**Evidence from Hext Patch:**

```hext
# English "Yes" → Japanese "はい"
# Address: 0x9199D0
# Bytes: 41 6D FF 00

# English "No" → Japanese "いいえ"
# Address: 0x9199D4
# Bytes: 6D 6D 6F FF
```

Both use **exactly 4 bytes**, same as English.

### 1.2 How This Works

Japanese Hiragana/Katakana characters are **single-byte encoded** at the same indices as English ASCII:

| Byte Value | English Character | Japanese Character | Texture |
|------------|------------------|-------------------|---------|
| 0x41 | 'A' | 'は' (ha) | Different fonts, same index |
| 0x6D | 'm' | 'い' (i) | Different fonts, same index |
| 0x6F | 'o' | 'え' (e) | Different fonts, same index |

**The trick:** The game engine loads **different font textures** (jafont_1.png vs usfont.png) but reads the **same byte values**. The byte 0x41 points to:
- Cell #65 in `usfont.png` → renders 'A'
- Cell #65 in `jafont_1.png` → renders 'は'

### 1.3 Why German Needs 5 Bytes

German "Nein" needs 5 bytes because:

```
N = 0x4E (1 byte)
e = 0x65 (1 byte)
i = 0x69 (1 byte)
n = 0x6E (1 byte)
terminator = 0xFF (1 byte)
Total: 5 bytes
```

Unlike Japanese, German uses **distinct letters** that cannot share indices with English. Each character requires its own byte allocation.

---

## 2. The FA-FE Multi-Page Font System

### 2.1 System Architecture

The multi-page system extends the 256-character limit to 1,536 characters using **page marker bytes**:

| Page Marker | Font Texture | Character Range | Purpose |
|-------------|-------------|-----------------|---------|
| (none/default) | jafont_1.png | 0x00-0xFF (256 chars) | Hiragana, Katakana, ASCII |
| 0xFA | jafont_2.png | 0x00-0xFF (256 chars) | Kanji set 1 |
| 0xFB | jafont_3.png | 0x00-0xFF (256 chars) | Kanji set 2 |
| 0xFC | jafont_4.png | 0x00-0xFF (256 chars) | Kanji set 3 |
| 0xFD | jafont_5.png | 0x00-0xFF (256 chars) | Kanji set 4 |
| 0xFE | jafont_6.png | 0x00-0xFF (256 chars) | Kanji set 5 |
| **Total** | **6 textures** | **1,536 characters** | **Full JIS support** |

### 2.2 Encoding Examples

**Simple Hiragana (single-byte):**
```
Text: "はい" (Yes)
Bytes: 0x41 0x6D 0xFF
Length: 3 bytes

Rendering:
- 0x41 → Load from jafont_1.png[0x41] → 'は'
- 0x6D → Load from jafont_1.png[0x6D] → 'い'
- 0xFF → Terminator
```

**Kanji with Page Markers (double-byte):**
```
Text: "魔法" (magic)
Bytes: 0xFA 0x1A 0xFA 0x2B 0xFF
Length: 5 bytes (2 chars + terminator)

Rendering:
- 0xFA → Page marker: switch to jafont_2.png
- 0x1A → Load from jafont_2.png[0x1A] → '魔'
- 0xFA → Page marker: switch to jafont_2.png (again)
- 0x2B → Load from jafont_2.png[0x2B] → '法'
- 0xFF → Terminator
```

**Mixed Hiragana + Kanji:**
```
Text: "まほう" vs "魔法" (both mean "magic")
Option 1 (Hiragana): 0x7D 0x49 0x69 0xFF (4 bytes)
Option 2 (Kanji): 0xFA 0x1A 0xFA 0x2B 0xFF (5 bytes)
```

### 2.3 Parser State Machine

The text parser maintains state across character reads:

```cpp
// Simplified parsing logic from PR #737
uint8_t current_page = 0;  // Default to page 0 (jafont_1)

while (*text_ptr != 0xFF) {  // 0xFF = terminator
    uint8_t byte = *text_ptr++;

    switch (byte) {
        case 0xFA:
            current_page = 1;  // Switch to jafont_2
            byte = *text_ptr++;  // Consume next byte as character index
            break;
        case 0xFB:
            current_page = 2;  // Switch to jafont_3
            byte = *text_ptr++;
            break;
        case 0xFC:
            current_page = 3;  // Switch to jafont_4
            byte = *text_ptr++;
            break;
        case 0xFD:
            current_page = 4;  // Switch to jafont_5
            byte = *text_ptr++;
            break;
        case 0xFE:
            current_page = 5;  // Switch to jafont_6
            byte = *text_ptr++;
            break;
        default:
            // Regular character on current page
            current_page = 0;  // Reset to default
            break;
    }

    // Render character from appropriate font texture
    render_character(current_page, byte);
}
```

**Key Insight:** Page markers **consume two bytes** from the text stream:
1. The marker byte itself (0xFA-0xFE)
2. The character index byte (0x00-0xFF)

---

## 3. Font Texture Structure

### 3.1 Texture Specifications

Each font texture follows the same grid layout:

```
Dimensions: 1024×1024 pixels
Grid: 16×16 cells = 256 character slots
Cell Size: 64×64 pixels per character
Format: PNG (converted to GPU texture at runtime)
```

**Grid Coordinate Calculation:**
```cpp
// Given character index (0-255)
uint8_t char_index = 0x41;  // Example: 'は'

// Calculate grid position
uint8_t grid_x = char_index % 16;   // 0x41 % 16 = 1
uint8_t grid_y = char_index / 16;   // 0x41 / 16 = 4

// Calculate pixel coordinates
uint16_t pixel_x = grid_x * 64;     // 1 * 64 = 64
uint16_t pixel_y = grid_y * 64;     // 4 * 64 = 256

// Calculate UV coordinates for texture sampling
float uv_x = pixel_x / 1024.0f;     // 64/1024 = 0.0625
float uv_y = pixel_y / 1024.0f;     // 256/1024 = 0.25
```

### 3.2 Character Width Tables

From PR #737, each character has a **variable width** value stored in a hardcoded table:

```cpp
// 6 pages × 256 characters = 1,536 width values
int charWidthData[6][256] = {
    // Page 0 (jafont_1): Hiragana/Katakana/ASCII
    {
        30, 30, 28, 31, 30, 30, 29, 29, 30, 30, 29, 30, 31, 30, 29, 27,
        30, 29, 29, 29, 31, 30, 28, 23, 30, 30, 30, 31, 29, 31, 30, 30,
        // ... 256 total values
    },

    // Pages 1-5 (jafont_2-6): Kanji (all 31px wide)
    {
        31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31,
        // ... 256 values per page
    }
};
```

**Width Value Format (Bit-Packed):**
```cpp
int8_t width_data = charWidthData[page][char_index];

// Extract values
int width = width_data & 0x1F;        // Lower 5 bits (0-31 pixels)
int left_padding = width_data >> 5;   // Upper 3 bits (0-7 pixels)

// Total character advance = left_padding + width
int advance = left_padding + width;
```

**Example:**
```
Character: 'は' at index 0x41, page 0
Width data: 30 (0x1E in hex)

Binary: 0001 1110
        │    │
        │    └─ Width: 11110 binary = 30 pixels
        └────── Padding: 000 binary = 0 pixels

Total advance: 0 + 30 = 30 pixels
```

---

## 4. Hext Patch System Analysis

### 4.1 Patch File Structure

The Japanese menu hext patch (`japanese_menu.txt`) contains 559 string replacements:

```hext
# Header
# Japanese Menu Text Patch for FF7 English
# AUTO-GENERATED by generate_exe_hext.py
# Generated: 2025-12-08 17:52:48 JST
# Total patches: 559

# Virtual address calculation formula:
# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000

# Example patch
# Do you want to quit -> ファイナルファンタジー７の
# EN: 0x00518370 (30 bytes allocated)
# JA: 0x00518F70 (same 30 bytes)
919970 = 44 A4 6C 72 8A 44 A4 98 5E 16 D0 3A 7B FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

### 4.2 Address Mapping Strategy

**English vs Japanese Executable Offset:**
```
JA_address = EN_address + 0xC00

Example:
EN "Yes" address: 0x005183D0
JA "Yes" address: 0x00518FD0
Offset: 0x00518FD0 - 0x005183D0 = 0xC00
```

This consistent offset suggests the Japanese and English executables have **nearly identical code**, with Japanese strings placed 0xC00 bytes higher in memory.

### 4.3 Byte Allocation Analysis

Sample comparisons from hext file:

| String | EN Address | JA Address | Bytes Allocated | EN Length | JA Length |
|--------|-----------|-----------|-----------------|-----------|-----------|
| "Yes" | 0x005183D0 | 0x00518FD0 | 4 | 3+term | 3+term |
| "No" | 0x005183D4 | 0x00518FD4 | 4 | 2+term | 4+term |
| "Window color" | 0x005188A8 | 0x005194A8 | 48 | 12+term | 9+term |
| "Sound" | 0x005188D8 | 0x005194D8 | 48 | 5+term | 5+term |
| "Controller" | 0x00518908 | 0x00519508 | 48 | 10+term | 6+term |

**Key Observation:** Japanese often uses **fewer bytes** than English because:
- English: "Controller" = 10 letters + terminator = 11 bytes
- Japanese: "キーボード" = 6 characters + terminator = 7 bytes
  - Encoded as: `4C D0 08 D0 26 FF` (6 single-byte chars + term)

---

## 5. Applicability to Multi-Language Systems

### 5.1 German/French/Spanish Requirements

**German Character Set:**
```
Base Latin: a-z, A-Z (52 characters)
Accented: ä, ö, ü, Ä, Ö, Ü, ß (7 characters)
Numbers: 0-9 (10 characters)
Punctuation: .,!?;:- etc. (30 characters)
Total: ~100 unique characters
```

**Verdict:** Fits easily in single-byte encoding (0x00-0xFF). No need for multi-page system.

### 5.2 The German "Nein" Problem

**Problem Statement:**
```
English "No" = 4 bytes allocated (N, o, term, padding)
German "Nein" = 5 bytes needed (N, e, i, n, term)
```

**Solutions:**

**Option 1: Static Hext Patching (Limited)**
- Requires finding strings with 5+ byte allocations
- Cannot patch all locations (many have 4-byte limits)
- **Not viable for comprehensive translation**

**Option 2: Dynamic Runtime Replacement (Recommended)**
- Intercept text rendering calls in FFNx
- Replace English strings with German strings on-the-fly
- Allocate new memory buffers dynamically
- **No byte allocation limits**

**Option 3: Abbreviation System**
- Store multi-byte strings in lookup tables
- Use single bytes as indices: 0xF0 = "Nein", 0xF1 = "Ja"
- Similar to Japanese Hiragana approach
- **Requires custom parser modification**

### 5.3 Extending FA-FE for Additional Languages

**Current Usage:**
```
0xFA-0xFE = Japanese Kanji pages (5 markers, fully used)
```

**Available Control Codes:**
```
0xE7-0xEF = Currently unused (9 codes available)
0xF0-0xF9 = Potentially available (10 codes)
```

**Proposed Extension:**
```
0xF0-0xF4 = Chinese Traditional (5 pages, ~1,280 chars)
0xF5-0xF9 = Korean Hangul (5 pages, ~1,280 chars)
0xE7-0xEB = Reserved for future (5 pages)
```

**Conflict Risk:** Some codes may be used for:
- Color control (FE D2-D9 range)
- Special formatting commands
- **Requires thorough investigation before implementation**

---

## 6. Technical Implementation Details

### 6.1 Memory Layout

**Font Texture Loading (from PR #737):**
```cpp
// Initialization (called once at game start)
ff7_externals.menu_jafont_1_graphics_object =
    ff7_externals.engine_load_graphics_object_6710AC(
        1, 12, &a2, "jafont_1.tim",
        (int)game_object_676578->dx_sfx_something
    );

ff7_externals.menu_jafont_2_graphics_object =
    ff7_externals.engine_load_graphics_object_6710AC(
        1, 12, &a2, "jafont_2.tim",
        (int)game_object_676578->dx_sfx_something
    );

// Repeat for jafont_3.tim through jafont_6.tim
```

**GPU Texture Binding:**
```cpp
// Rendering (called per character)
void render_japanese_character(uint8_t page, uint8_t char_index) {
    graphics_object* font_texture;

    // Select texture based on current page
    switch (page) {
        case 0: font_texture = menu_jafont_1_graphics_object; break;
        case 1: font_texture = menu_jafont_2_graphics_object; break;
        case 2: font_texture = menu_jafont_3_graphics_object; break;
        case 3: font_texture = menu_jafont_4_graphics_object; break;
        case 4: font_texture = menu_jafont_5_graphics_object; break;
        case 5: font_texture = menu_jafont_6_graphics_object; break;
    }

    // Bind texture to GPU
    bind_graphics_object(font_texture);

    // Calculate UV coordinates
    float u = (char_index % 16) / 16.0f;
    float v = (char_index / 16) / 16.0f;

    // Render character quad
    draw_character_quad(u, v, width, height);
}
```

### 6.2 Text Parsing Flow

**Complete Rendering Pipeline:**
```
1. Game requests menu text render
   ↓
2. Load text buffer from memory (e.g., "はい魔法")
   ↓
3. Parser reads byte stream:
   - 0x41 → current_page=0, render jafont_1[0x41] = 'は'
   - 0x6D → current_page=0, render jafont_1[0x6D] = 'い'
   - 0xFA → current_page=1 (page marker)
   - 0x1A → render jafont_2[0x1A] = '魔'
   - 0xFA → current_page=1 (page marker)
   - 0x2B → render jafont_2[0x2B] = '法'
   - 0xFF → terminator, stop parsing
   ↓
4. Calculate total text width from charWidthData table
   ↓
5. Resize text box if needed (PR #737 feature)
   ↓
6. Render all characters to screen buffer
```

### 6.3 FFNx Integration Points

**Key Hook Locations (from PR #737 analysis):**

| Original Function | Japanese Replacement | Purpose |
|------------------|---------------------|---------|
| `field_submit_draw_text_640x480_6E706D` | `field_submit_draw_text_640x480_6E706D_jp` | Field dialogue rendering |
| `engine_load_menu_graphics_objects_6C1468` | `engine_load_menu_graphics_objects_6C1468_jp` | Load 6 font textures |
| `common_submit_draw_char_from_buffer_6F564E` | `common_submit_draw_char_from_buffer_6F564E_jp` | Character rendering core |
| `menu_draw_everything_6CC9D3` | `menu_draw_everything_6CC9D3_jp` | Menu text rendering |

**FFNx Hook Installation (from ff7_opengl.cpp):**
```cpp
if (ff7_japanese_edition) {
    // Replace 10 text rendering functions
    replace_function(
        ff7_externals.field_submit_draw_text_640x480_6E706D,
        field_submit_draw_text_640x480_6E706D_jp
    );

    replace_function(
        ff7_externals.common_submit_draw_char_from_buffer_6F564E,
        common_submit_draw_char_from_buffer_6F564E_jp
    );

    // ... 8 more function replacements
}
```

---

## 7. Comparison Tables

### 7.1 Encoding Comparison

| Language | Model | Chars | Pages | Byte/Char | Example |
|----------|-------|-------|-------|-----------|---------|
| English | Single-byte | 256 | 1 | 1.0 | "No" = 3 bytes |
| German | Single-byte | ~110 | 1 | 1.0 | "Nein" = 5 bytes |
| Japanese | Hybrid | 1,536 | 6 | 1.3 avg | "いいえ" = 4 bytes |
| Japanese (Kanji) | Hybrid | 1,536 | 6 | 2.0 | "魔法" = 5 bytes |
| Chinese | Hybrid | ~3,000 | 10+ | 2.0 avg | TBD |
| Korean | Hybrid | ~2,350 | 8-10 | 2.0 avg | TBD |

### 7.2 Memory Footprint Comparison

| Language | Font Textures | Width Table | Total Memory |
|----------|--------------|-------------|--------------|
| English | 1 × 1MB | 256 bytes | ~1.0 MB |
| German | 1 × 1MB | 256 bytes | ~1.0 MB |
| Japanese | 6 × 1MB | 1,536 bytes | ~6.0 MB |
| Chinese (est.) | 10 × 1MB | 2,560 bytes | ~10.0 MB |
| Korean (est.) | 8 × 1MB | 2,048 bytes | ~8.0 MB |

---

## 8. Limitations and Known Issues

### 8.1 PR #737 Known Bugs

From the PR discussion and analysis:

1. **Colored Text Broken**
   - Color codes (FE D2-D9) conflict with page marker 0xFE
   - All colored text appears white or corrupted
   - Root cause: Missing colored font texture variants

2. **Character Input Screen Corrupted**
   - Name entry screen shows garbage in last two rows
   - Wrong character indexing during input
   - Cursor misalignment

3. **Text Box Cursor Misalignment**
   - Selection cursor doesn't align with variable-width characters
   - Hardcoded 8px spacing assumptions broken

### 8.2 Architectural Limitations

**Cannot Support:**
- Languages requiring >10 font pages (emoji systems)
- Dynamic font loading at runtime (all 6 pages must load at init)
- Mixing multiple languages in same text buffer (single global page state)

**Workarounds:**
- Use FFNx's texture override system for runtime font switching
- Implement language-specific text buffers
- Add custom page marker handling for additional languages

---

## 9. Recommendations for Multi-Language Implementation

### 9.1 Recommended Approach

**For German/French/Spanish (Latin alphabet languages):**
1. ✅ Use single-page font system (no FA-FE markers needed)
2. ✅ Implement runtime string replacement in FFNx hooks
3. ✅ Load translation strings from external JSON/XML files
4. ✅ Allocate dynamic memory buffers (no byte limits)

**For Chinese/Korean/Additional CJK:**
1. ✅ Extend FA-FE system with new page markers (0xF0-0xF9)
2. ✅ Generate additional font textures (jafont_7.png+)
3. ✅ Add width tables for new characters
4. ✅ Update parser to handle extended markers

### 9.2 Implementation Priority

**Phase 1: Runtime String Replacement (German/French/Spanish)**
- Hook FFNx text rendering functions
- Load translations from external files
- Replace English strings dynamically
- No executable modifications needed

**Phase 2: Extended Multi-Page System (Chinese/Korean)**
- Add new page marker codes (0xF0-0xF9)
- Generate CJK font textures
- Update parser state machine
- Create character mapping tables

**Phase 3: Integration and Testing**
- Test all languages in all contexts (menu, field, battle)
- Verify no conflicts with color codes or special formatting
- Performance optimization for texture switching
- Create user-friendly language selector

---

## 10. Conclusion

The Japanese menu system demonstrates that **architectural elegance** can solve apparently impossible constraints. By separating storage (bytes) from rendering (textures), FF7 supports 1,536 characters while maintaining the same byte allocation envelope as 256-character systems.

**Key Takeaways:**

1. **Single-byte hiragana/katakana** fit in same allocations as English ASCII
2. **Page markers (0xFA-0xFE)** enable texture switching for extended characters
3. **Variable-width tables** provide proportional rendering for better aesthetics
4. **Runtime string replacement** is superior to static hext patches for multi-language
5. **System is extensible** to Chinese/Korean with additional page markers

**For Your Multi-Language Project:**

The Japanese system proves it's possible, but for German/French/Spanish, you don't need the complexity of FA-FE encoding. Instead, leverage FFNx's runtime hooking capabilities to replace strings dynamically without byte allocation limits.

The investigation file created by the exploration agent contains even more technical details and should be reviewed for comprehensive understanding.

---

**Next Steps:**
1. Investigate FFNx text rendering hooks (menu module)
2. Create proof-of-concept for runtime string replacement
3. Design multi-language translation file format
4. Test with sample German translations

---

**End of Investigation Report**
