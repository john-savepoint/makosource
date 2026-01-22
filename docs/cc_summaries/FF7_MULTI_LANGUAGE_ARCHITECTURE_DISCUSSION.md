# FF7 Multi-Language Architecture Discussion - Session Summary

**Created**: 2026-01-16 12:14:59 JST (Friday)
**Session-ID**: 4f2300ef-48a4-4186-bea1-f3436df97f65
**Version**: 1.0.0
**Author**: John Zealand-Doyle + Claude Code
**Context**: Planning for FF7 International Edition supporting 15+ languages

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Goals](#project-goals)
3. [Character Requirements Analysis](#character-requirements-analysis)
4. [FFNx Research Findings](#ffnx-research-findings)
5. [Architecture Options Explored](#architecture-options-explored)
6. [Technical Deep Dives](#technical-deep-dives)
7. [User Questions & Clarifications](#user-questions--clarifications)
8. [Recommended Implementation Path](#recommended-implementation-path)
9. [Next Steps](#next-steps)

---

## Executive Summary

This session explored the technical feasibility and architecture for creating an "FF7 International Edition" supporting 15+ languages with instant language switching capability. Key findings:

### Is It Achievable?
**Yes**, but requires significant architectural work beyond the current Japanese implementation.

### Key Challenges Identified
1. **Character Volume**: Chinese requires 10-26 texture pages vs. Japanese's 6 pages
2. **Complex Scripts**: Arabic, Hindi, Thai require text shaping (HarfBuzz integration)
3. **Encoding Limits**: Current 2-byte system caps at ~1,280 extended characters
4. **IME Input**: CJK languages need OS-level input method integration

### Critical Discovery
**FFNx has NO hardcoded texture page limits** - the `texturehandle` array is dynamically allocated. The limitation is in the game's byte encoding scheme, not FFNx's rendering capabilities.

---

## Project Goals

### Target Languages (15 Total)

| Group | Languages | Script Type |
|-------|-----------|-------------|
| **Latin Extended** | English, Spanish, French, German, Italian, Portuguese, Polish | Latin alphabet with diacritics |
| **Cyrillic** | Russian | Cyrillic alphabet |
| **CJK** | Japanese, Chinese (Simplified/Traditional), Korean | Character-based scripts |
| **Complex Scripts** | Arabic, Hindi, Thai | Right-to-left + text shaping |

### Stated Requirements
- **Instant language switching** during gameplay
- **Complete game coverage** (field dialogue, menus, battle text, naming screens)
- **OS-level input** for character entry (pinyin, etc.)
- **Concurrent language storage** with tags (e.g., `[EN]text[/EN][JA]テキスト[/JA]`)

---

## Character Requirements Analysis

### Texture Page Calculations

**Formula**: 1024×1024 texture, 16×16 grid, 64×64 glyphs = **256 characters per page**

| Language | Characters Needed | Pages (Full) | Pages (Game-Specific) |
|----------|-------------------|--------------|----------------------|
| Latin Extended (all Romance + Polish) | ~400 | 2 | 2 |
| Russian (Cyrillic) | 66 | 1 | 1 |
| Japanese (current) | 2,800 | 11 | 11 |
| Korean (common Hangul syllables) | 2,780-11,172 | 11-44 | 11 |
| Chinese Simplified (GB2312) | 3,500-6,500 | 14-26 | 10 |
| Chinese Traditional (Big5) | 4,000-13,000 | 16-51 | 12 |
| Arabic (shaped glyphs) | 150-200 | 1 | 1 |
| Hindi (Devanagari precomposed) | 400-1,000 | 2-4 | 2 |
| Thai (precomposed) | 128-200 | 1 | 1 |
| **Total (Conservative)** | ~9,446 | **39 pages** | **39 pages** |

### Language Complexity Tiers

**Tier 1: Simple (Latin + Cyrillic)**
- Shared texture approach
- No text shaping needed
- Standard rendering pipeline

**Tier 2: CJK (Japanese, Chinese, Korean)**
- Large character sets
- Lookup table required
- No text shaping (glyph-per-character)

**Tier 3: Complex Scripts (Arabic, Hindi, Thai)**
- Text shaping required (HarfBuzz)
- Right-to-left rendering (Arabic)
- Contextual glyph forms
- Combining marks and ligatures

---

## FFNx Research Findings

### Key Discovery: No Texture Page Limit

From FFNx source analysis (`common.cpp:1741`):

```c
// FFNx allocates texture handles dynamically based on palette count
VRASS(texture_set, ogl.gl_set->textures,
      VREF(tex_header, palettes) > 0 ? VREF(tex_header, palettes) * 2 : 1);

VRASS(texture_set, texturehandle,
      (uint32_t*)external_calloc(VREF(texture_set, ogl.gl_set->textures), sizeof(uint32_t)));
```

**Meaning**: The `texturehandle` array is a **pointer to dynamically allocated memory**, not a fixed-size array. FFNx can support 6, 60, or 600 texture pages without modification.

### Palette Swapping Mechanism

FFNx exploits the "palette swapping" system for font pages:

**Traditional Usage (Colors)**:
```
Texture data: [2, 5, 2, 3, 1, ...]  (indices)
Palette 0:    Red,  Blue, Red, Green, White, ...
Palette 1:    Green, Orange, Green, Purple, Gray, ...
```

**FFNx's Hijack (Fonts)**:
```
texture_set for fonts:
├── texturehandle[0] = jafont_1.png (Hiragana/Katakana)
├── texturehandle[1] = jafont_2.png (Kanji page 1)
├── texturehandle[2] = jafont_3.png (Kanji page 2)
...
├── texturehandle[N] = any_font_N.png

When game switches "palette":
  FFNx binds corresponding texture instead of changing colors
```

### Graphics Objects Explained

A `graphics_object` is a rendering container:

```c
struct graphics_object {
    texture_set* textures;     // Font texture pages
    vertex_buffer* vertices;   // 3D geometry (for positioning)
    matrix transform;          // Screen position/rotation/scale
    uint32_t flags;            // Rendering state flags
};
```

When FF7 says "draw this graphics object," FFNx handles texture binding, vertex submission, and rendering.

---

## Architecture Options Explored

### Option 1: Extended Byte Encoding (Current System Extension)

**Current FF7 Encoding**:
```
Single-byte: 0x00-0xE9 → Page 0 (233 base characters)
Two-byte:    FA XX → Page 1 (256 chars)
             FB XX → Page 2 (256 chars)
             FC XX → Page 3 (256 chars)
             FD XX → Page 4 (256 chars)
             FE XX → Page 5 (256 chars)

Total: 233 + (5 × 256) = 1,513 characters
```

**Extended Proposal**:
```
Claim prefixes E0-EF for additional pages (16 prefixes):
E0-EF XX → 16 × 256 = 4,096 characters
FA-FE XX → 5 × 256 = 1,280 characters

Total: 233 base + 5,376 extended = ~5,600 characters
```

**Problem**: Still insufficient for full Chinese coverage (~6,500+ needed for Traditional Chinese).

---

### Option 2: Lookup Table Indirection (User's Idea - Recommended)

**Concept**: Two-byte encoding selects lookup table entry, which points to actual texture page + index.

```c
// Define lookup structure
struct GlyphRef {
    uint8_t page;    // Texture page (0-255)
    uint8_t index;   // Character on that page (0-255)
};

// Per-language lookup tables
GlyphRef CHINESE_TABLE[256][256];   // 65,536 addressable chars
GlyphRef KOREAN_TABLE[256][256];    // 65,536 addressable chars
GlyphRef JAPANESE_TABLE[256][256];  // 65,536 addressable chars

// Encoding scheme:
// F0 XX YY = Chinese character at table[XX][YY]
// F1 XX YY = Korean character at table[XX][YY]
// F2 XX YY = Japanese character at table[XX][YY]
```

**Rendering Flow**:
```c
uint8_t prefix = text[0];      // F0 = Chinese
uint8_t table_idx = text[1];   // Which sub-table (0-255)
uint8_t char_idx = text[2];    // Which character (0-255)

// Lookup the actual texture page and glyph index
GlyphRef ref = LANGUAGE_TABLES[prefix - 0xF0][table_idx][char_idx];

// Bind texture and draw
bind_texture(font_textures[ref.page]);
draw_glyph(ref.index);
```

**Advantages**:
- **65,536 addressable characters per language prefix**
- **Memory-efficient**: Only active language's table loaded
- **Texture sharing**: Han unification possible (shared Chinese/Japanese/Korean characters)
- **Scalable**: Add more languages by adding more prefix bytes

**Implementation Requirements**:
1. Reserve `0xF0-0xF7` as language family prefixes (8 families)
2. Generate lookup tables from Unicode character mappings
3. Load/unload tables dynamically based on active language
4. Modify text rendering to perform lookup before drawing

---

### Option 3: Dynamic Font Rendering (Most Scalable)

**Concept**: Render glyphs at runtime using TrueType fonts instead of pre-baked textures.

**AF3DN.P already uses this approach**:
```c
// From AF3DN.P imports (discovered in analysis)
D3DXCreateFontW(device, ..., &font);  // Unicode-aware font creation
MultiByteToWideChar(CP_SHIFT_JIS, 0, text, -1, unicodeText, 256);

// Render text directly with OS font
font->DrawTextW(sprite, unicodeText, -1, &rect, DT_LEFT, color);
```

**Workflow**:
```c
void render_text_unicode(const wchar_t* text) {
    for (int i = 0; text[i]; i++) {
        wchar_t ch = text[i];

        // Check glyph cache
        GlyphTexture* cached = lookup_cache(ch);
        if (!cached) {
            // Rasterize glyph using FreeType or D3DXCreateFontW
            cached = rasterize_glyph(ch, "Noto Sans CJK");
            add_to_cache(cached, ch);
        }

        draw_cached_glyph(cached);
    }
}
```

**Advantages**:
- **Unlimited character support** (full Unicode)
- **Smaller distribution size** (no texture files needed, just TTF fonts)
- **Automatic fallback** (OS can substitute missing glyphs)
- **Future-proof** (new languages = add font file)

**Challenges**:
- Requires integrating FreeType library or using D3DXCreateFontW consistently
- Complex scripts need HarfBuzz for text shaping
- Glyph cache management complexity
- Font licensing (Noto Sans CJK recommended - SIL Open Font License)

---

### Option 4: Hybrid Approach (Pragmatic Choice)

**Recommended for FF7 International Edition**:

| Language Type | Method | Rationale |
|---------------|--------|-----------|
| **Latin + Cyrillic** | Pre-rendered (2 pages) | Small character set, shared texture |
| **Japanese** | Pre-rendered (6 pages) | Already implemented |
| **Chinese/Korean** | Lookup table + 20-30 pages | Too many characters for dynamic, too few for inefficiency |
| **Arabic/Hindi/Thai** | Dynamic rendering + HarfBuzz | Requires text shaping anyway |

**Why Hybrid?**:
- **CJK characters benefit from pre-rendering** (consistent appearance, no font dependencies)
- **Complex scripts must be dynamic** (text shaping impossible with static textures)
- **Latin/Cyrillic are trivial** (fits in 1-2 textures)

---

## Technical Deep Dives

### How FF7 Executables Work

#### Memory Mapping Process

When you double-click `ff7.exe`:

**Step 1: Windows reads PE Header**
```
PE Header contains:
├── Code section addresses (.text)
├── Data section addresses (.data)
├── DLL imports (AF3DN.P, kernel32.dll, etc.)
├── Entry point (where to start executing)
└── Memory allocation size
```

**Step 2: Virtual Address Space Created**
```
File on Disk:              Memory at Runtime:
┌──────────────┐           ┌──────────────────┐
│ PE Header    │ ───────►  │ 0x00400000       │ (ImageBase)
│ .text (code) │ ───────►  │ 0x00401000       │ (Code section)
│ .data        │ ───────►  │ 0x007BA000       │ (Data section)
│ .rdata       │ ───────►  │ 0x009XXXXX       │ (Read-only data)
└──────────────┘           └──────────────────┘
```

**Step 3: Demand Paging**
- Windows doesn't load entire executable at once
- Loads 4KB pages on-demand when accessed
- Reduces memory usage for large executables

**Step 4: DLL Loading**
- `AF3DN.P` mapped into same address space
- Import tables resolved (function pointers linked)

**Step 5: Execution Begins**
- CPU jumps to entry point address
- Game initialization code runs

#### What's Inside ff7.exe?

```
ff7.exe (2.5MB) contains:
├── .text section    - Machine code (x86 assembly instructions)
├── .data section    - Global variables, initialized data
├── .rdata section   - Read-only constants, strings
├── .rsrc section    - Resources (icons, version info)
└── .reloc section   - Address relocation information

Assets are NOT in the executable!
- Textures: menu_us.lgp, battle.lgp, field.lgp
- Audio: music, sound effects
- Videos: FMV sequences
```

---

### How Asset Loading Works

#### From Code to GPU

```
1. Game code: LoadTexture("usfont.tex")
   │
2. File I/O: Open menu_us.lgp archive
   │
3. LGP parser: Extract usfont.tex (TEX format)
   │
4. TEX parser: Read header, decompress pixel data
   │
5. DirectX call: CreateTexture(..., pixel_data)
   │
6. GPU upload: Texture stored in VRAM
   │
7. Handle returned: Game stores handle for later use
```

#### In Assembly

```asm
; Pseudo-assembly for texture loading
push    offset aUsfontTex    ; Push "usfont.tex" string
call    load_texture_func    ; Call loader
mov     [texture_handle], eax ; Store returned handle

; Later, when rendering:
push    [texture_handle]     ; Push texture handle
call    d3d_set_texture      ; Bind to GPU
```

The actual file I/O happens deep in Windows APIs (`CreateFile`, `ReadFile`), not visible in game assembly.

---

### How FF7 Reads Glyphs from Textures

#### Grid Math

```
Texture: 1024×1024 pixels
Grid:    16×16 cells
Cell:    64×64 pixels

To find character at index N:
  column = N % 16         (0-15)
  row    = N / 16         (0-15)

  pixel_x = column * 64   (0-960)
  pixel_y = row * 64      (0-960)
```

#### UV Coordinates (Texture Mapping)

```c
void draw_character(int char_index, int screen_x, int screen_y) {
    // Calculate UV coordinates (0.0-1.0 range)
    float u0 = (char_index % 16) * 64.0f / 1024.0f;  // Left edge
    float v0 = (char_index / 16) * 64.0f / 1024.0f;  // Top edge
    float u1 = u0 + 64.0f / 1024.0f;                  // Right edge (64 pixels)
    float v1 = v0 + 64.0f / 1024.0f;                  // Bottom edge

    // Draw textured quad at screen position
    draw_textured_quad(screen_x, screen_y, 64, 64, u0, v0, u1, v1);
}
```

---

### User's "Bigger Texture" Idea - Detailed Analysis

#### Current System
```
Texture: 1024×1024 pixels
Grid:    16×16 cells
Cell:    64×64 pixels
Total:   256 characters per texture
```

#### Proposed: 4× Larger
```
Texture: 2048×2048 pixels
Grid:    32×32 cells
Cell:    64×64 pixels (same glyph size)
Total:   1024 characters per texture
```

**Benefits**:
- 4× characters per page
- 6 textures × 1024 = **6,144 characters** (covers Japanese + Chinese comfortably)
- No need for complex lookup tables

#### What Needs Patching

**1. Texture Creation**:
```c
// Current (likely):
CreateTexture(1024, 1024, ...);

// Needs to become:
CreateTexture(2048, 2048, ...);
```

**2. UV Calculation**:
```c
// Current:
float u = (index % 16) / 16.0f;
float v = (index / 16) / 16.0f;

// Needs to become:
float u = (index % 32) / 32.0f;
float v = (index / 32) / 32.0f;
```

**3. Index Range Check**:
```c
// Current:
if (index > 255) return ERROR;

// Needs to become:
if (index > 1023) return ERROR;
```

#### Finding Assembly to Patch

Look for patterns:
```asm
; Division by 16 (bit shift right 4)
shr eax, 4        ; index / 16

; Modulo 16 (AND with 0x0F = 15)
and eax, 0Fh      ; index % 16

; Multiply by 64
imul eax, 40h     ; × 64
```

**Patches needed**:
```asm
; Change division by 16 to division by 32
shr eax, 4  →  shr eax, 5

; Change modulo 16 to modulo 32
and eax, 0Fh  →  and eax, 1Fh
```

Use Cheat Engine or IDA Pro to find these instructions, then create HEXT patches.

---

### Multi-Language File Management

#### Current HEXT Format
```hext
# Simple address = bytes format
718E9D = 08
921D48 = 58 2F D0 58 FF 00 00 00
```

#### User's JSON Proposal

**Advantages**:
- **Human-readable** language organization
- **Version control friendly** (structured diffs)
- **Extensible** (add metadata, comments)

**Example Structure**:
```json
{
  "version": "2.0",
  "base_patches": {
    "cursor_y_limit": [
      { "address": "718E9D", "value": "08", "description": "Allow cursor row 8" },
      { "address": "718EA6", "value": "08", "description": "Clamp cursor at row 8" }
    ]
  },
  "languages": {
    "ja": {
      "name": "Japanese",
      "encoding": "shift-jis",
      "patches": {
        "sidebar_labels": [
          { "address": "921D48", "bytes": "58 2F D0 58 FF 00 00 00", "label": "スペース (Space)" },
          { "address": "921D50", "bytes": "55 4F 17 A3 FF 00 00 00", "label": "さくじょ (Delete)" }
        ]
      }
    },
    "zh-cn": {
      "name": "Chinese Simplified",
      "encoding": "gb2312",
      "patches": {
        "sidebar_labels": [
          { "address": "921D48", "bytes": "XX XX XX XX FF 00 00 00", "label": "空格 (Space)" }
        ]
      }
    }
  }
}
```

#### Implementation Options

**Option A: Pre-process JSON → HEXT**
- Build tool generates language-specific HEXT files at compile time
- User selects which HEXT to use before game launch
- Simple, no runtime overhead

**Option B: Runtime JSON Parsing**
- FFNx reads JSON at startup
- Applies patches based on `active_language` config setting
- More flexible, supports runtime switching

**Option C: Binary Patch Format**
- Custom binary format with language blocks
- Fast loading, minimal parsing overhead
- FFNx reads and applies correct block at startup

---

### IME Input for CJK Languages

#### The Challenge

Chinese input example (pinyin to Hanzi):
```
User types:  n i h a o
IME shows:   你好, 尼昊, 逆耗 (candidates)
User selects: 你好
Result:      你好 (inserted into game)
```

Cannot be done with static character grids - requires OS-level input method.

#### Windows IME Integration

**Hook IME Composition Events**:
```c
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_IME_COMPOSITION:
            if (lParam & GCS_RESULTSTR) {
                HIMC hIMC = ImmGetContext(hwnd);

                // Get composed string length
                LONG length = ImmGetCompositionStringW(hIMC, GCS_RESULTSTR, NULL, 0);

                // Allocate buffer and get string
                wchar_t* buffer = (wchar_t*)malloc(length + sizeof(wchar_t));
                ImmGetCompositionStringW(hIMC, GCS_RESULTSTR, buffer, length);
                buffer[length / sizeof(wchar_t)] = L'\0';

                // Insert into game's name buffer
                insert_name_characters(buffer);

                free(buffer);
                ImmReleaseContext(hwnd, hIMC);
                return 0;
            }
            break;
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);
}
```

**FFNx Integration Point**:
- Hook game's window procedure
- Intercept IME events during naming screen
- Convert wide-char string to game's encoding
- Write to name buffer at current cursor position

---

### Unused Memory Space in Executable

#### Finding Candidates

**Alignment Padding**:
```
Sections must align to 4KB boundaries:
.text ends at:  0x6FFFFA
Next section:   0x700000 (4KB aligned)
Unused bytes:   6 bytes (filled with 0x00 or 0xCC)
```

**Dead Code Regions**:
- Disabled features from development
- Debug code never called in release build
- Example: You found unused Hiragana/Katakana tables in EN exe!

**Using Cheat Engine to Identify**:
```
1. Scan: Array of bytes = "00 00 00 00 00 00 00 00"
2. Filter: Address range 0x920000-0x930000 (.data section)
3. Watch: Do values ever change during gameplay?
4. Verify: Check in IDA - any code references these addresses?
```

#### What to Store There

**Option A: Extended Lookup Tables**
```
Per-language character mapping:
- 256 entries × 2 bytes = 512 bytes per page
- 10 pages = 5KB total
```

**Option B: Configuration Data**
```
Active language ID:         1 byte
Texture page assignments:   16 bytes (array of page IDs)
Character set metadata:     32 bytes
Total:                      ~50 bytes
```

**Option C: Small Textures**
```
Icon atlas (16×16 icons, 256×256 texture):
- 256 × 256 × 4 bytes = 256KB
- Too large for unused padding
- Better to load as external file
```

---

## User Questions & Clarifications

### Q1: "How does the game read glyphs from a texture?"

**Answer**: Grid-based UV coordinate calculation.

The game doesn't "read" pixel data directly. It tells the GPU:
1. **Bind this texture** (font page)
2. **Draw a quad** at screen position (X, Y)
3. **Use these UV coordinates** to sample from the texture

UV coordinates define which part of the texture to display:
```
U = horizontal (0.0 = left edge, 1.0 = right edge)
V = vertical (0.0 = top edge, 1.0 = bottom edge)

For character at index 42 in 16×16 grid:
  column = 42 % 16 = 10
  row = 42 / 16 = 2

  u0 = 10 * 64 / 1024 = 0.625
  v0 = 2 * 64 / 1024 = 0.125
  u1 = u0 + 64/1024 = 0.6875
  v1 = v0 + 64/1024 = 0.1875

GPU samples texture between (0.625, 0.125) and (0.6875, 0.1875)
```

---

### Q2: "Why don't we make textures bigger and offset the cells?"

**Answer**: This is exactly right, and it works! Here's why:

**Your Proposal**:
```
Current: 1024×1024, 16×16 grid = 256 chars
Your idea: 2048×2048, 32×32 grid = 1024 chars
           4096×4096, 64×64 grid = 4096 chars
```

**It requires patching**:
1. Texture creation size (tell DirectX to create larger texture)
2. UV calculation (change grid dimensions in math)
3. Index range checks (allow indices 0-1023 or 0-4095)

**How to implement**:
1. Find assembly that does `index / 16` and `index % 16`
2. Change to `index / 32` and `index % 32`
3. Create HEXT patches
4. Generate 2048×2048 texture with 32×32 grid layout

This is **simpler** than lookup tables but **less flexible** than dynamic rendering.

---

### Q3: "Couldn't we have unused parts of the executable for additional textures?"

**Answer**: Partially yes, but with limitations.

**What you can store**:
- **Lookup tables** (kilobytes) ✅
- **Configuration data** (bytes) ✅
- **Small binary data** (few KB) ✅

**What you can't store**:
- **Texture pixel data** (megabytes) ❌
  - jafont_1.tex = 4MB
  - Unused padding is typically < 50KB
  - Better to load as external file

**Best use of unused space**:
- Language-to-texture-page mapping tables
- Active language ID
- Character encoding metadata

---

### Q4: "What is palette swapping and what's a graphics object?"

**Palette Swapping**:

Old games stored textures as indices (0-255) pointing to a color table. Changing the table ("palette") changed all colors at once.

**Example**:
```
Texture data:     [5, 5, 10, 10, 15, 15, ...]
Palette 0 (day):  [Blue, Blue, Yellow, Yellow, Orange, Orange, ...]
Palette 1 (night):[Navy, Navy, Gray, Gray, Brown, Brown, ...]

Same texture data, different palettes = different appearance
```

**FFNx's Hijack for Fonts**:

Instead of color palettes, each "palette slot" holds a different texture page:
```
texturehandle[0] = jafont_1.png
texturehandle[1] = jafont_2.png
texturehandle[2] = jafont_3.png

When game says "use palette 2":
  FFNx binds jafont_3.png instead of changing colors
```

**Graphics Object**:

A container for all data needed to render something:
```c
struct graphics_object {
    texture_set* textures;      // Which textures to use
    vertex_buffer* vertices;    // 3D geometry (positions)
    matrix transform;           // Screen position/rotation/scale
    uint32_t flags;             // Rendering state (blend mode, etc.)
};
```

When FF7 says "draw this graphics object," it means "use these textures, render this geometry, at this position."

---

### Q5: "How does assembly relate to loading assets?"

**Answer**: Assembly calls Windows API functions; file I/O is abstracted away.

**High-level view**:
```c
// C code (conceptual):
LoadTexture("usfont.tex");
```

**Assembly equivalent**:
```asm
push    offset aUsfontTex    ; Push string address onto stack
call    load_texture_func    ; Call function
add     esp, 4               ; Clean up stack (remove parameter)
mov     [handle], eax        ; Store returned texture handle
```

**What `load_texture_func` does internally**:
```c
void load_texture_func(const char* filename) {
    // 1. Call Windows API to open file
    HANDLE hFile = CreateFileA(filename, GENERIC_READ, ...);

    // 2. Read file into memory buffer
    char buffer[4194540];  // 4MB for texture
    ReadFile(hFile, buffer, sizeof(buffer), ...);

    // 3. Parse TEX format header
    parse_tex_header(buffer);

    // 4. Call DirectX to create texture
    IDirect3DTexture9* texture;
    device->CreateTexture(1024, 1024, ..., &texture);

    // 5. Upload pixel data to GPU
    texture->LockRect(&locked, ...);
    memcpy(locked.pBits, buffer + header_size, pixel_data_size);
    texture->UnlockRect();

    // 6. Return handle
    return (uint32_t)texture;
}
```

**In assembly, you only see**:
- Function calls (`call`)
- Stack manipulation (`push`, `pop`)
- Return value handling (`mov [handle], eax`)

The actual file I/O is buried in Windows DLLs (kernel32.dll, d3d9.dll).

---

## Recommended Implementation Path

### Phase 1: Foundation (Extend Current System)

**Goal**: Prove out lookup table system with 1 additional language (Russian - simplest case).

**Tasks**:
1. Reserve byte prefix `0xF0` for Russian Cyrillic lookup table
2. Create lookup table generator tool:
   - Input: Unicode character list
   - Output: Binary lookup table (256 × 2 bytes)
3. Modify FFNx text renderer to check for `0xF0` prefix
4. Generate Russian character texture (1 page, 66 characters)
5. Test with sample Russian text

**Deliverable**: Proof-of-concept with Japanese + Russian working.

---

### Phase 2: CJK Languages (Chinese, Korean)

**Goal**: Implement full Chinese support with lookup tables.

**Tasks**:
1. Analyze FF7 Chinese fan translation for character frequency
2. Generate game-specific character subset (~2,500 chars minimum)
3. Create 10-page Chinese texture atlas
4. Generate Chinese lookup tables (prefix `0xF1` = Simplified, `0xF2` = Traditional)
5. Implement OS-level IME integration for naming screens
6. Test Korean with similar approach (prefix `0xF3`)

**Deliverable**: Japanese + Russian + Chinese (Simplified/Traditional) + Korean working.

---

### Phase 3: Complex Scripts (Arabic, Hindi, Thai)

**Goal**: Integrate HarfBuzz for text shaping, implement RTL rendering.

**Tasks**:
1. Integrate HarfBuzz library into FFNx build
2. Implement Unicode BiDi algorithm for Arabic (or use ICU library)
3. Create shaped glyph cache system
4. Generate dynamic textures from TrueType fonts at runtime
5. Implement RTL rendering pipeline
6. Test with Arabic, Hindi, Thai sample text

**Deliverable**: All 15 languages functional.

---

### Phase 4: Language Switching

**Goal**: Runtime language switching with hot-swapping.

**Tasks**:
1. Create language selection menu
2. Implement texture page hot-swap system
3. Reload text files from language-specific LGPs
4. Save language preference to config
5. Add language tags to dialogue format: `[EN]text[/EN][JA]テキスト[/JA]`

**Deliverable**: Full instant language switching capability.

---

## Next Steps

### Immediate Research Needed

1. **Find UV Calculation Code** in ff7.exe
   - Search for `shr eax, 4` (division by 16)
   - Search for `and eax, 0Fh` (modulo 16)
   - Document addresses for HEXT patching

2. **Test Larger Texture Support**
   - Create 2048×2048 test texture with 32×32 grid
   - Patch texture creation size
   - Patch UV calculation
   - Verify rendering works

3. **Design Lookup Table Format**
   - Binary vs JSON
   - Compression (if needed)
   - Loading mechanism (startup vs on-demand)

### Tools to Develop

1. **Character Frequency Analyzer**
   - Parse FF7 field/battle/menu text
   - Generate minimum character set per language

2. **Lookup Table Generator**
   - Input: Unicode character list
   - Output: Binary lookup table + metadata

3. **Texture Atlas Packer**
   - Input: TTF font + character list
   - Output: PNG texture with grid layout

4. **touphScript Language Extension**
   - Support for multi-byte prefixes
   - Language tags in dialogue format

### Open Questions

1. **Font Licensing**: Confirm Noto Sans CJK license allows redistribution
2. **Performance**: Will 39 texture pages cause memory issues?
3. **Compatibility**: Does this break 7th Heaven mod compatibility?
4. **Distribution**: How to package 15 language assets efficiently?

---

## Conclusion

Creating an FF7 International Edition with 15+ languages is **technically achievable** but requires substantial architectural work:

**Critical Path**:
1. Lookup table indirection system (solves encoding limits)
2. Larger texture support (2048×2048 = 4× capacity)
3. HarfBuzz integration (complex script support)
4. OS-level IME integration (CJK input)
5. Language switching infrastructure

**Estimated Effort**:
- Japanese implementation: ~28 sessions
- Full 15-language system: ~5-10× that effort (140-280 sessions)

**Biggest Unknowns**:
- HarfBuzz integration complexity
- RTL rendering edge cases
- Performance with 39 texture pages
- Testing coverage for all languages

**Recommended Start**:
- Prove out lookup table system with Russian (simplest addition)
- Test 2048×2048 texture support
- Tackle complex scripts last (most challenging)

---

**End of Session Summary**

**Session Duration**: ~2 hours
**Key Deliverable**: Comprehensive architectural analysis for FF7 multi-language support
**Next Session Goal**: Implement Russian lookup table proof-of-concept

