# AF3DN.P Analysis Context

## What You Are Analyzing

**AF3DN.P** is Square Enix's custom graphics driver for the Japanese eStore version of Final Fantasy VII PC (2013). This is a **PE32 DLL** (317KB) that replaces the standard graphics driver to enable Japanese text rendering.

## Why This File Matters

1. Contains the **Japanese font injection code** - hardcoded references to jafont_1.tim through jafont_6.tim
2. Implements **double-byte character support** via Windows MultiByteToWideChar APIs
3. Is the **custom engine** that Square Enix built for the Japanese PC release
4. Provides a **reference implementation** for porting Japanese support to FFNx mod

## Known Exports (DLL Entry Points)

1. `new_dll_graphics_driver` - Main entry point (function at 0x100051A0)
2. `dotemuRegCloseKey` - Registry wrapper
3. `dotemuRegDeleteValueA` - Registry wrapper
4. `dotemuRegOpenKeyExA` - Registry wrapper
5. `dotemuRegQueryValueExA` - Registry wrapper
6. `dotemuRegSetValueExA` - Registry wrapper
7. `DllMain` - DLL initialization

## Key External Dependencies

### DirectX 9.0c (d3dx9_29.dll)
- `D3DXCreateTextureFromFileA` - Load font textures
- `D3DXCreateFontW` - Create Unicode-aware fonts (W = Wide/Unicode)
- `D3DXCreateSprite` - 2D sprite rendering
- `D3DXMatrixMultiply`, `D3DXMatrixScaling` - Transformations

### Windows APIs for Japanese Support
- `MultiByteToWideChar` (KERNEL32.dll) - Shift-JIS → Unicode conversion
- `WideCharToMultiByte` (KERNEL32.dll) - Unicode → Shift-JIS conversion

### Audio (libvgmstream, FFmpeg)
- `avcodec_*`, `avformat_*` functions
- `init_vgmstream`, `render_vgmstream`, `close_vgmstream`

## Font System Details

### jafont Textures
- 6 font textures: jafont_1.tex through jafont_6.tex
- Each: 1024×1024 pixels, 64×64 per glyph, 16×16 grid = 256 positions
- Total capacity: ~1,536 characters (actually ~2,800 used)

### Character Encoding
- jafont_1 (0x00-0xFF): Kana, numbers, Latin, symbols
- jafont_2 (0xFA XX): Kanji page 1 (battle/skill terms)
- jafont_3 (0xFB XX): Kanji page 2
- jafont_4 (0xFC XX): Kanji page 3 + lowercase a-z
- jafont_5 (0xFD XX): Kanji page 4
- jafont_6 (0xFE XX): Kanji page 5 + control codes

### Character Layout (NOT JIS Order)
Characters are ordered by **game usage frequency**, not standard JIS encoding. Battle/menu terms appear first.

## Data Structures Already Identified

### Naming Screen Tables (in Japanese AF3DN.P binary)
| Data | Offset | Size |
|------|--------|------|
| Hiragana table | 0x410B8 | 90 bytes (9×10) |
| Katakana table | 0x41112 | 90 bytes (9×10) |
| EISUU table | 0x4116C | 50 bytes (5×10) |
| Page labels | 0x411C8 | Various |

### Sidebar Labels at 0x411C8
- ひらがな: `43 87 0B 73 FF`
- カタカナ: `4A 5E 4A 72 FF`
- えいすう: `6F 6D 59 69 FF`
- スペース: `58 2F D0 58 FF`
- さくじょ: `55 4F 17 A3 FF`
- けってい: `51 9D 65 6D FF`
- デフォルト: `24 44 AC 8A 66 FF`
- キャンセル: `4C 9E 98 5A 8A FF`

## File Structure

- **Lines 1-687**: Function declarations (forward references)
- **Lines 688-8892**: Data arrays, globals, strings
- **Lines 8893-38782**: Function definitions (549 functions)

## Your Task

You are analyzing a **specific chunk** of the function definitions. For each function in your chunk:

1. **Identify the function's purpose** based on:
   - Function name (sub_XXXXXXXX - the hex is the address)
   - Parameters and return type
   - What it calls (other functions, Windows APIs, DirectX)
   - What data structures it accesses
   - String references (error messages, file paths)

2. **Categorize the function** into one of these domains:
   - **Graphics/Rendering** - DirectX calls, texture loading, drawing
   - **Text/Font** - Character encoding, font loading, text rendering
   - **Input** - Keyboard, controller, user input handling
   - **Audio** - Sound playback, vgmstream, FFmpeg
   - **Memory** - Allocation, management, buffers
   - **File I/O** - File reading, LGP archive access
   - **Registry** - Windows registry operations
   - **Initialization** - Setup, DLL loading
   - **Math/Transform** - Matrix operations, calculations
   - **Utility** - String operations, helpers
   - **Unknown** - Cannot determine

3. **Suggest a descriptive name** for the function (e.g., `load_font_texture`, `render_character_glyph`, `init_directx_device`)

4. **Note any interesting findings**:
   - References to game-specific data
   - Relationships to other functions
   - Potential bugs or unusual code patterns

## Output Format

**CRITICAL: You MUST follow this exact structure for EVERY function. Do not summarize or skip functions. Analyze each function individually.**

```markdown
## Chunk [ID] Analysis (Lines [START]-[END])

### Function sub_XXXXXXXX (line NNNN)
- **Category**: [One of: Graphics | Text | Input | Audio | Memory | File | Registry | Init | Math | Utility | Unknown]
- **Purpose**: [1-2 sentences describing what this function does]
- **Suggested Name**: [snake_case_descriptive_name]
- **Key Calls**: [List significant function/API calls, e.g., CreateTexture, MultiByteToWideChar]
- **Notes**: [Any interesting observations, or "None"]

### Function sub_YYYYYYYY (line MMMM)
- **Category**: ...
- **Purpose**: ...
- **Suggested Name**: ...
- **Key Calls**: ...
- **Notes**: ...

[Continue for ALL functions in the chunk]
```

## Example Output (Follow This Exactly)

```markdown
## Chunk 1 Analysis (Lines 8893-9467)

### Function sub_10001340 (line 8976)
- **Category**: Text
- **Purpose**: Looks up a character in the Japanese character table based on cursor position and page number. Returns pointer to character data.
- **Suggested Name**: lookup_japanese_character
- **Key Calls**: dword_10050660, accesses unk_10051880 array
- **Notes**: Branches on dword_1004CB78 which appears to be a JP/EN locale flag

### Function sub_100014B0 (line 9101)
- **Category**: Graphics
- **Purpose**: Sets up viewport and scissor rectangle for DirectX rendering based on window dimensions.
- **Suggested Name**: setup_viewport_scissor
- **Key Calls**: SetViewport, SetScissorRect
- **Notes**: None

### Function sub_10001510 (line 9126)
- **Category**: Init
- **Purpose**: Initializes the complete DirectX rendering pipeline including shaders, render states, and vertex buffers.
- **Suggested Name**: init_render_pipeline
- **Key Calls**: D3DXCompileShaderFromFileA, CreateVertexBuffer, SetRenderState
- **Notes**: Loads shaders from "shaders/main.fx" - critical initialization function
```

**You MUST analyze EVERY function in your assigned chunk using this exact format. Do not provide summaries or skip any functions.**

## Important Notes

- This is **legitimate Square Enix code**, not malware
- Focus on understanding, not modifying
- IDA Pro decompilation may have artifacts - use judgment
- Address format: `sub_1000XXXX` where XXXX is offset from DLL base 0x10000000
- Some functions may be compiler-generated (exception handling, CRT)
