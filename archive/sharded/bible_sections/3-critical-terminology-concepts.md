# 3. CRITICAL TERMINOLOGY & CONCEPTS

## 3.1 Core Technologies

**FFNx:**
- A modern, open-source **graphics driver replacement** for FF7/FF8
- Replaces the original game's `AF3DN.P` (English) or proprietary driver (Japanese)
- Provides advanced features: high-resolution rendering, texture replacement, mod API
- Written in C++ with BGFX backend (cross-platform graphics abstraction)
- **Our primary development target**

**BGFX:**
- Rendering library that abstracts DirectX, OpenGL, Vulkan, Metal
- Used by FFNx for modern graphics API support
- Handles texture binding, shader management, and draw calls
- We hook into BGFX's texture binding logic for page switching

**7th Heaven:**
- The de facto **mod manager** for FF7
- Acts as a **Virtual File System (VFS)**
- Intercepts the game's file I/O calls
- Serves modified assets from `.iro` archives (ZIP-like containers)
- **Primary distribution platform** for this mod

**Hext:**
- A system for applying **in-memory assembly patches** to executables at runtime
- Used by FFNx to modify game logic without changing the EXE on disk
- Patch files are human-readable text with custom syntax
- **Critical for intercepting the text parser**

## 3.2 File Formats

**LGP Archive (.lgp):**
- Square Enix's proprietary archive format (similar to ZIP/TAR)
- Contains game assets: textures, models, dialogue, scripts
- Structure: Header + File Table + Data Blocks
- Tools: `ulgp` (extract), `lgp_tool` (pack/unpack)
- **Critical files:**
  - `menu_us.lgp` / `menu_ja.lgp`: UI textures, fonts
  - `flevel.lgp` / `jfleve.lgp`: Field maps, scripts (note the typo!)
  - `battle.lgp` / `battle_ja.lgp`: Battle assets

**TEX Texture (.tex):**
- Bitmap image format used by FF7 PC port
- Derived from PlayStation's TIM (Tim Image) format
- Structure: Header (palette count, dimensions) + Palette Data + Pixel Data
- **Critical header field:** `palettes` (determines texture slot allocation)
- Tools: `TexTools`, FFNx's built-in loader
- **Our intervention point:** Override allocation based on filename, not header

**PNG Override System:**
- FFNx checks `mods/Textures/` for `.png` files **before** loading `.tex` files
- Naming convention: `{original_name}.png` (e.g., `usfont_h.png`)
- **Load order (priority):**
  1. `mods/Textures/` (loose files)
  2. 7th Heaven VFS (`.iro` archives)
  3. Game directory (vanilla `.lgp` archives)

## 3.3 Encoding Systems

**FF7 Text Encoding (English):**
- **Single-Byte System:** Each character is 1 byte (0x00-0xFF)
- **Direct Mapping:** Byte value = texture cell index
- Example: `0x41` = 'A' (cell 65 in USFONT.TEX)
- **Control codes:** `0x00-0x1F` (line breaks, colors, etc.)
- **Limitation:** Maximum 256 characters (0x00-0xFF)

**FF7 Japanese Encoding (FA-FE System):**
- **Two-Byte Sequences for Extended Characters:**
  - First byte: `0xFA`, `0xFB`, `0xFC`, `0xFD`, or `0xFE` (page marker)
  - Second byte: `0x00-0xFF` (character index within that page)
- **Example:** `0xFA 0x00` = First character in jafont_2.png
- **Single-Byte Fallback:** `0x00-0xE6` still map to jafont_1.png (base page)
- **Total Capacity:**
  - Page 0: 231 characters (0x00-0xE6)
  - Pages 1-5: 256 characters each × 5 = 1,280
  - **Total: 1,511 characters** (sufficient for core Japanese)

**Shift-JIS (NOT Used):**
- Standard Japanese encoding in Windows/web
- We do **NOT** use Shift-JIS internally
- Unicode → FF7 Encoding conversion happens via `character_map_accurate.csv`
- Game text files are encoded in the custom FA-FE system

## 3.4 Memory Structures

**Character Width Table:**
- **Location:** Loaded from `KERNEL.BIN` / `WINDOW.BIN` into RAM
- **Pointer:** `common_externals.font_info` (FFNx struct)
- **Address (US 1.02):** `0x99DDA8` (varies by version!)
- **Structure:** Array of 256 bytes, each representing a character's width in pixels
  ```c
  char width_table[256] = {
      0x04, // 0x00: Control code width
      0x04, // 0x01: ...
      ...
      0x08, // 0x41: 'A' width
      0x0C, // 0x57: 'W' width (wider)
      ...
  };
  ```
- **Problem:** English widths are 4-12px. Kanji require 16px.
- **Solution:** Overwrite this table in RAM with fixed 16px values

**Texture Set Structure (FFNx):**
```c
struct texture_set {
    struct gl_texture_set *gl_set;
    uint32_t *texturehandle;  // Array of GPU texture handles
    uint32_t palette_index;   // Currently active palette
    // ... other fields
};

struct gl_texture_set {
    uint32_t textures;  // Number of allocated texture slots
    // ... other fields
};
```
- **Critical:** `textures` determines array size allocation
- **Default logic:** `textures = (palettes > 0) ? palettes * 2 : 1`
- **English font:** USFONT.TEX has `palettes = 1` → allocates 2 slots
- **Our override:** Force `textures = 6` for Japanese fonts

---
