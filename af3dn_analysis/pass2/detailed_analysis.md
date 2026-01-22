# AF3DN.P Pass 2: Detailed Analysis of Key Japanese Text Functions

## Function: sub_10001340
**Suggested Name**: `find_character_by_cursor_position`

### Algorithm
1. Get naming screen state pointers based on locale (`dword_1004CB78`)
2. Iterate through character table (`unk_10051880`) searching for match
3. Compare cursor position against character table entries
4. Cache result in `dword_1004CBBC` if found
5. Return pointer to matching character entry (5-DWORD struct)

### Data Structures
- `unk_10051880`: Array of character table entries
  - Each entry: 5 DWORDs (20 bytes)
  - Entry[0]: Character ID
  - Entry[4]: Page/position identifier
- Naming screen state structure:
  - Offset +2572 (EN) / +2892 (JP): Contains page data
  - Offset +16 within page: Current selection/cursor position

### Call Graph
- **Calls**: `dword_10050660()` (state initialization function)
- **Called by**: Input handlers, character selection logic

### Key Variables
- `dword_1004CB78`: JP/EN locale flag (0=EN, non-zero=JP)
- `dword_1004CBBC`: Cached character ID from last lookup
- `dword_10050640`: Current cursor position pointer
- `dword_10050D78`: Character table entry count
- `unk_10051880`: Character table base address

### FFNx Porting Notes
This is the **core character lookup function** for the naming screen. To port:
1. Replace character table with Unicode mappings
2. Implement cursor→character resolution for modern UI
3. Cache can be preserved for optimization
4. Consider supporting both Shift-JIS and Unicode paths

---

## Function: sub_100146D0
**Suggested Name**: `map_scan_code_to_character_index`

### Algorithm
1. Massive switch statement mapping scan codes (1-237) to character indices (19-162)
2. Direct 1:1 lookup table implemented as switch/case
3. Returns -1 for unmapped scan codes

### Data Structures
- Input: Scan code (keyboard/controller input code)
- Output: Character index into naming screen character array

### Call Graph
- **Calls**: None (pure lookup)
- **Called by**: Input processing, keyboard event handlers

### Key Variables
- Parameter `a1`: Input scan code
- Return value: Character array index or -1

### FFNx Porting Notes
This is a **keyboard scan code to character position mapper**. For FFNx:
1. Replace with modern input mapping (SDL keycodes, etc.)
2. Consider JSON-based remappable keyboard layout
3. May need separate mappings for Hiragana/Katakana/Latin pages
4. Scan code ranges suggest original used DirectInput

---

## Function: sub_10011EA0
**Suggested Name**: `construct_message_with_payload`

### Algorithm
1. Read message type from `dword_1004CAC0`
2. Allocate appropriate payload object based on type:
   - Type 1: IntPayload
   - Type 2,4,7,8,18,19,20: No payload
   - Type 3,15: IntArrayPayload
   - Type 5,6,9,10,11,12,16,17: WStringPayload (Japanese text)
   - Type 13: Complex payload (sub_10011690)
   - Type 14: IngameTextPayload
3. Initialize payload from data at `dword_1004CAC0 + 4`
4. Attach payload to message structure

### Data Structures
- Message structure:
  - Offset +0: VTable pointer
  - Offset +4: Message type
  - Offset +8: Payload pointer (optional)
- WStringPayload: Wide string (for Japanese text)
  - Offset +0: VTable
  - Offset +4: Type = 4
  - Offset +12-28: Wide string buffer
  - Offset +32: Capacity (7 default)

### Call Graph
- **Calls**: 
  - `operator new` (multiple payload allocations)
  - `sub_10011690` (complex payload constructor)
  - `sub_1001A540` (IngameTextPayload init)
  - `sub_1001EF00`, `sub_1001E970`, etc. (payload attachment)
- **Called by**: Message system, event handlers

### Key Variables
- `dword_1004CAC0`: Source message data pointer
- Payload vtables:
  - `IntPayload::vftable` @ 0x100433BC
  - `WStringPayload::vftable` @ 0x100433DC
  - `IngameTextPayload::vftable` @ 0x100433FC

### FFNx Porting Notes
**Critical for Japanese text display**. This constructs messages containing Japanese text payloads:
1. WStringPayload (types 5-12, 16-17) handles dialogue/UI text
2. IngameTextPayload (type 14) handles in-game text rendering
3. Replace with UTF-8 or UTF-16 string handling
4. Preserve message type system for compatibility

---

## Function: sub_10014FF0
**Suggested Name**: `initialize_japanese_locale`

### Algorithm
1. Check initialization flag `byte_1004CE97`
2. Call `sub_10014DC0()` to detect game version
3. Set C locale using `setlocale(0, Locale)`
4. Call `sub_10014E10()` to patch binary for Japanese support
5. Validate launcher (check `sub_10015520()`)
6. Call `sub_10015710()` for final initialization

### Data Structures
- None directly, but sets up global locale state

### Call Graph
- **Calls**:
  - `sub_10014DC0()` - Version detection
  - `setlocale()` - C runtime locale setup
  - `sub_10014E10()` - Binary patching
  - `sub_10015520()` - Launcher validation
  - `sub_10015710()` - Final init
- **Called by**: Startup code, DLL initialization

### Key Variables
- `byte_1004CE97`: Initialization flag (prevents double-init)
- `dword_1004CAC8`: Detected game version
- `Locale`: Locale string (likely "Japanese_Japan.932")

### FFNx Porting Notes
**Entry point for Japanese localization**. For FFNx:
1. Skip launcher check (`sub_10015520`)
2. Preserve version detection for compatibility
3. Replace locale setup with UTF-8 throughout
4. Binary patching (`sub_10014E10`) likely enables Shift-JIS rendering - may need equivalent for Unicode fonts

---

## Function: sub_10014E10
**Suggested Name**: `patch_binary_for_japanese_version`

### Algorithm
1. Detect game version from magic value at `MEMORY[0x401004]`
2. Set version-specific function pointers based on detected version:
   - Version 1/20: Steam/original (pointers at 0x404XXX)
   - Version 2: Unknown variant
   - Version 3: Another variant
   - Version 4: Yet another variant
3. Apply VirtualProtect + code patches at 2 locations per version:
   - Patch location 1: `dword_1004C790` (5 bytes)
   - Patch location 2: `dword_1004CAF4` (5 bytes)
4. Store original bytes in `dword_1004E620[]` for potential restoration
5. Write JMP instructions (`0xE9` = -23) to redirect to custom handlers

### Data Structures
- Patch record array `dword_1004E620[]`:
  - Stores original byte, original DWORD, target address
- Version-specific pointers:
  - `dword_1004C790`, `dword_1004CAF4`, `dword_1004CABC`, `dword_1004CAE8`

### Call Graph
- **Calls**: 
  - `VirtualProtect()` - Make code writable
  - `sub_10014D90()` - Patch target 1
  - `nullsub_1()` - Patch target 2 (empty function)
- **Called by**: `sub_10014FF0()` (initialization)

### Key Variables
- `MEMORY[0x401004]`: Version magic (0x99CE0805, 0x99EBF805, etc.)
- `dword_1004CAC8`: Detected version (1-4, 20)
- `dword_1004CC50`: Patch record count

### FFNx Porting Notes
**Runtime code patching for Japanese support**. This injects custom text rendering:
1. FFNx should skip these patches (use clean binary)
2. Patch targets likely override:
   - Text rendering functions
   - Font texture loading
3. Version detection useful for supporting multiple FF7 releases
4. JMP targets (`sub_10014D90`) are Japanese text handlers

---

## Function: sub_100086B0
**Suggested Name**: `render_japanese_font_texture_page`

### Algorithm
1. Get font texture page data from structure at `*v1[38]` (38th pointer in some object)
2. Extract texture dimensions: `width = v[15]`, `height = v[16]`, `depth = v[26]`
3. Calculate texture size: `size = width * height * depth`
4. Check 64-entry cache (`dword_1004FF80[]`) for existing matching texture
5. If no match:
   - Evict oldest cache entry (circular buffer at `dword_10050180`)
   - Allocate new buffer with `malloc(size)`
   - Copy texture data from offset +216 (JP) or +212 (EN)
   - Update cache
6. Call `sub_100029E0()` and `sub_100033B0()` to upload texture

### Data Structures
- Font texture page structure:
  - Offset +60: Width (v[15])
  - Offset +64: Height (v[16])
  - Offset +104: Depth/BPP (v[26])
  - Offset +212 (EN) / +216 (JP): Texture data pointer
- Cache:
  - `dword_1004FF80[64]`: Cached texture object pointers
  - `Block[64]`: Cached texture data buffers
  - `dword_10050180`: Next eviction index (circular)

### Call Graph
- **Calls**:
  - `malloc()`, `free()` - Texture buffer management
  - `memcpy()` - Texture data copy
  - `sub_100029E0()` - Texture preparation
  - `sub_100033B0()` - Texture upload to GPU
- **Called by**: Text rendering, font system

### Key Variables
- `dword_1004CB78`: JP/EN flag (affects structure offsets)
- `dword_1004FF80[64]`: Texture object cache
- `dword_10050180`: Cache eviction index
- `dword_100501E4`: Cache miss counter

### FFNx Porting Notes
**Font texture page renderer for Japanese fonts**. This is critical:
1. Handles 6 font texture pages (0x00, 0xFA-0xFE for kanji)
2. 64-entry cache suggests frequent page swapping
3. Texture data likely raw bitmap (width × height × depth bytes)
4. For FFNx:
   - Replace with modern font atlas rendering (FreeType, stb_truetype)
   - Preserve page-based architecture for compatibility
   - Consider pre-caching all 6 pages (modern VRAM can handle it)

---

## Function: sub_10008DA0
**Suggested Name**: `multiply_4x4_matrices`

### Algorithm
1. Standard 4×4 matrix multiplication: `result = a2 = *this * *a3`
2. Computes all 16 elements of result matrix
3. Row-major order (typical for Direct3D)

### Data Structures
- Matrices stored as `float[16]` (4×4 row-major)
- Matrix layout:
  ```
  [0]  [1]  [2]  [3]
  [4]  [5]  [6]  [7]
  [8]  [9]  [10] [11]
  [12] [13] [14] [15]
  ```

### Call Graph
- **Calls**: None (pure math)
- **Called by**: 3D rendering pipeline, text positioning

### Key Variables
- `result`: Left-hand matrix (this)
- `a2`: Output matrix
- `a3`: Right-hand matrix

### FFNx Porting Notes
Standard matrix math - not Japanese-text specific, but used for positioning 2D text quads. FFNx can:
1. Use existing math library (glm, DirectXMath, etc.)
2. Preserve for compatibility if needed
3. Likely used to position dialogue boxes and UI elements

---

## Function: sub_10008550
**Suggested Name**: `initialize_naming_screen_character_table`

### Algorithm
1. Call `sub_10008050()` (prerequisite initialization)
2. Copy character table data from `unk_1004A620` to `unk_10051880` (300 bytes = 15 entries × 20 bytes)
3. Copy secondary data from `unk_1004A758` to `byte_10050720`
4. Set character table count: `dword_10050D78 = 15`
5. Initialize 8 character ID globals (`dword_100501A0` through `dword_100501BC`)

### Data Structures
- Character table: 15 entries × 20 bytes at `unk_10051880`
- Character ID quick-access globals (indices into table):
  - `dword_100501A0 = 1` (likely space)
  - `dword_100501B8 = 2` (likely backspace)
  - `dword_100501A8 = 3` (likely confirm)
  - etc.

### Call Graph
- **Calls**: 
  - `sub_10008050()` - Prerequisite init
  - `qmemcpy()` - Data copy
- **Called by**: Naming screen initialization

### Key Variables
- `unk_1004A620`: Source character table (ROM data)
- `unk_10051880`: Runtime character table (RAM)
- `dword_10050D78`: Character count (15)
- `byte_10050720`: Secondary character data

### FFNx Porting Notes
**Initializes naming screen character layout**. 15 entries likely represent:
- Special buttons (Space, Backspace, Confirm, Cancel, Default)
- Page switchers (Hiragana, Katakana, EISUU)

For FFNx:
1. Replace with UTF-8 character table
2. Preserve special button indices (100501A0-100501BC)
3. Consider loading from external JSON for localization

---

## Function: sub_10004B20
**Suggested Name**: `setup_japanese_font_texture_transform`

### Algorithm
1. Get texture data pointers based on locale:
   - JP: offset +0x2C from `a2`, +0x30 from `a1`
   - EN: offset +0x30 from `a2`, +0x2C from `a1`
2. If texture exists, call `sub_10003FF0()` to set up rendering
3. Check texture flag at offset +156 (JP) or +152 (EN)
4. Copy 64-byte transform matrix to `unk_1004E578`:
   - If flag set: copy from offset +160 (JP) / +156 (EN)
   - If flag clear: copy from offset +164 (JP) / +160 (EN)

### Data Structures
- Texture object structure:
  - Offset +44/48: Texture data pointer (locale-dependent)
  - Offset +152/156: Transform enable flag
  - Offset +156/160: Custom transform matrix (64 bytes, 4×4 floats)
  - Offset +160/164: Default transform matrix (64 bytes)
- `unk_1004E578`: Global transform matrix buffer (64 bytes)

### Call Graph
- **Calls**: 
  - `sub_10003FF0()` - Set up texture rendering
  - `qmemcpy()` - Copy transform matrix
- **Called by**: Font rendering pipeline

### Key Variables
- `dword_1004CB78`: JP/EN locale flag
- `unk_1004E578`: Current font transform matrix

### FFNx Porting Notes
**Sets up 2D transformation for font rendering**. Transform matrix likely handles:
- Texture coordinate mapping
- Font scaling/positioning
- Possible rotation for vertical text

For FFNx:
1. Replace with modern 2D transform (orthographic projection)
2. Preserve matrix-based approach for compatibility
3. May need to adjust for modern aspect ratios

---

## Function: sub_1000A3E0
**Suggested Name**: `load_and_init_ogg_music_stream`

### Algorithm
1. Clean up previous music stream if exists
2. Build OGG file path: `sprintf("%sdata/music_ogg/%s.ogg")`
3. Check cache `dword_1004C5D8[a2]` for pre-loaded stream
4. If not cached, call `init_vgmstream()` to open OGG file
5. Extract audio format from vgmstream:
   - Sample rate, channels, bit depth
6. Initialize DirectSound secondary buffer with format
7. Calculate buffer size: `5 * sample_rate * channels * (16/8)`
8. Set up streaming state variables
9. Start playback

### Data Structures
- vgmstream structure (external library):
  - Offset +4: Sample rate
  - Offset +8: Channel count
  - Offset +24: Loop flag
- DirectSound buffer format:
  - 16-bit PCM
  - Stereo/mono based on vgmstream
  - 5-second buffer

### Call Graph
- **Calls**:
  - `sprintf()` - Build file path
  - `init_vgmstream()` - Open OGG file (external lib)
  - DirectSound methods - Buffer creation, playback
  - `sub_1000A2A0()`, `sub_1000A1F0()` - Stream setup
- **Called by**: Music playback system

### Key Variables
- `dword_10050DC0`: Game data path
- `dword_1004C5D8[100]`: vgmstream object cache
- `dword_1004C5D4`: Current DirectSound buffer
- `dword_1004C77C`: Buffer size in bytes

### FFNx Porting Notes
Not Japanese-text specific, but relevant for **Japanese voice/music support**:
1. Uses vgmstream library for OGG playback
2. FFNx already has better music support (ambient, vgmstream)
3. Can preserve for compatibility or replace with modern audio API

---

## Function: sub_10011980
**Suggested Name**: `build_naming_screen_page_data`

### Algorithm
1. Loop 36 times (36 = 3 pages × 12 entries? Or grid layout?)
2. For each iteration `v3` (0-35):
   - Store iteration index at `*a2`
   - Look up 3 character entries from tables:
     - `v18` (this+2): Primary character table
     - `v19` (this+10): Secondary character table
     - `v20` (this+18): Tertiary character table
   - Extract wide-string character data from each entry
   - Concatenate all 3 strings into output buffer at `a2`
3. Advance `a2` pointer through all concatenated strings

### Data Structures
- Input object structure:
  - Offset +8: Primary character table pointer
  - Offset +40: Secondary character table pointer
  - Offset +72: Tertiary character table pointer
- Character table entry:
  - Offset +20: String length
  - Offset +4 or +24: String data (wide char)
  - Offset +28: Capacity (if < 8, data inline; else pointer)

### Call Graph
- **Calls**:
  - `sub_10019630()` - Character table lookup (3 times per loop)
  - `memcpy()` - String concatenation
- **Called by**: Naming screen page builder

### Key Variables
- `v18`, `v19`, `v20`: Pointers to 3 character tables
- Loop count: 36 iterations

### FFNx Porting Notes
**Builds naming screen page layout**. 36 iterations suggest:
- 3 pages × 12 rows? Or 6 rows × 6 columns?
- Each grid cell combines 3 character sources (base + dakuten + handakuten?)

For FFNx:
1. Replace with UTF-8 string building
2. Preserve 3-table architecture (supports combining characters)
3. May need to handle Unicode combining marks differently

---

## Function: sub_10007010
**Suggested Name**: `initialize_character_table_28_entries`

### Algorithm
1. Set character table count: `dword_10050D78 = 28`
2. Call `sub_10006280()` (prerequisite init)
3. Copy 560 bytes character table: `unk_1004A868` → `unk_10051880`
4. Copy secondary data: `unk_1004AA98` → `byte_10050720`
5. Initialize 8 character ID globals (similar to `sub_10008550` but different values)

### Data Structures
- Same as `sub_10008550` but:
  - 28 entries × 20 bytes = 560 bytes
  - Different source data (`unk_1004A868` vs `unk_1004A620`)

### Call Graph
- **Calls**:
  - `sub_10006280()` - Prerequisite init
  - `qmemcpy()` - Data copy
- **Called by**: Different naming screen mode initialization

### Key Variables
- `dword_10050D78`: Character count (28 vs 15)
- Source table: `unk_1004A868` (different from sub_10008550)

### FFNx Porting Notes
**Initializes larger character table (28 entries)**. Likely represents:
- English/Latin character mode (A-Z + special chars)
- Different naming screen layout than Japanese

For FFNx:
1. Detect which mode based on call location
2. Support both 15-entry (JP) and 28-entry (EN) layouts
3. Consider unified UTF-8 table with mode flags

---

## Function: sub_10007120
**Suggested Name**: `initialize_english_graphics_driver`

### Algorithm
(Massive function - 670 lines of binary patching and initialization)

1. Call locale setup (`sub_100070A0`, `sub_10001000`)
2. Extract function pointers from driver structure at offset +2700
3. Initialize naming screen with `sub_10007010()` (28-entry English mode)
4. Apply VirtualProtect + code patches at 50+ locations
5. Set up DirectSound buffer initialization
6. Configure graphics driver function table (60+ function pointers)
7. Return initialized driver object

### Data Structures
- Graphics driver structure (240 bytes):
  - 60 function pointers for rendering, textures, state management
  - Examples at offsets:
    - [0]: `sub_10001860` - Init
    - [24]: `dword_10050648` - Something
    - [42-44]: `sub_10004AE0` - Repeated functions
    - [46-50]: `sub_10004B20` - Font transform (analyzed above)

### Call Graph
- **Calls**: Too many to list (50+ VirtualProtect patches, 60+ function assignments)
- **Called by**: DLL entry point, graphics initialization

### Key Variables
- Patched addresses stored in `dword_10051XXX` globals (50+ addresses)
- `dword_1004CC50`: Patch record counter
- `dword_1004E620[]`: Patch backup array
- `Frequency`: QueryPerformanceFrequency result

### FFNx Porting Notes
**Master initialization for English version**. Key observations:
1. Massive binary patching (50+ locations) - FFNx should avoid
2. Sets up English naming screen (28 chars via `sub_10007010`)
3. Function table at end is the **graphics driver API**
4. Distinguish from Japanese version (`sub_10008890` mentioned as alternative)

For FFNx:
1. Skip all VirtualProtect patches
2. Preserve function table structure for compatibility
3. Note: Function [46-50] use `sub_10004B20` (font transform analyzed above)

---

## Function: new_dll_graphics_driver
**Suggested Name**: `create_graphics_driver_with_locale`

### Algorithm
1. Call `sub_10014FF0()` - Initialize Japanese locale if needed
2. Detect game version with `sub_100051A0()` → `dword_10050624`
3. Based on version (1/2/3/4/20), set 50+ global function pointers:
   - Font rendering addresses
   - Text system addresses  
   - Naming screen addresses
4. Set `dword_1004CB78 = 1` for Japanese versions (5+ or 20)
5. Set up exception handler and execution state
6. Query performance counter
7. Call version-specific init:
   - Japanese: `sub_10008890(a1)`
   - English: `sub_10007120(v1)`
8. Patch binary for text rendering (`VirtualProtect` + JMP injection)
9. Create game window with proper dimensions
10. Set up DirectSound and rendering
11. Return initialized graphics driver

### Data Structures
- Version-specific pointer tables (50+ globals per version):
  - `dword_10050658`, `lpAddress`, `dword_10050678`, etc.
  - Each version has different addresses for same functionality
- Graphics driver object (returned)

### Call Graph
- **Calls**:
  - `sub_10014FF0()` - Locale init
  - `sub_100051A0()` - Version detect
  - `sub_10008890()` - Japanese driver init
  - `sub_10007120()` - English driver init
  - `sub_10008C80()` - Patch target
  - Windows API: `CreateWindowEx`, `LoadIcon`, etc.
  - `sub_1000C780()` - Final rendering setup
- **Called by**: DLL export, game startup

### Key Variables
- `dword_10050624`: Detected version (1/2/3/4/20)
- `dword_1004CB78`: JP flag (0=EN, 1=JP)
- `dword_10050620`, `dword_10051D80`: Resolution width/height
- `hWnd`: Game window handle

### FFNx Porting Notes
**Master entry point for graphics driver creation**. Critical observations:

1. **Version Detection**: 5 different FF7 PC versions supported
   - Version 1/20: Steam/original
   - Versions 2/3/4: Unknown variants
   - Each has different binary offsets

2. **Locale Detection**: `dword_1004CB78` set to 1 for JP versions
   - Affects all structure offsets throughout codebase
   - Triggers Japanese init path (`sub_10008890` vs `sub_10007120`)

3. **Function Pointer Tables**: 50+ globals set per version
   - These are hardcoded addresses in AF3DN.P.DLL
   - Point to text rendering, font loading, naming screen code

4. **Binary Patching**: VirtualProtect + JMP injection
   - Redirects to `sub_10008C80()` and others
   - Enables Japanese font rendering at runtime

**For FFNx Implementation**:
1. Skip version detection (use clean FF7.exe)
2. Skip binary patching (use hooking framework instead)
3. Preserve locale flag (`dword_1004CB78`) for compatibility
4. Replace function pointer tables with modern renderer
5. Keep window creation logic (or use FFNx's window manager)
6. Critical: Understand offset differences (+0x2C vs +0x30, +152 vs +156) for JP/EN structure access

---

## Summary: Key Findings for FFNx

### Architecture Overview
1. **Dual-Path Design**: Separate initialization for English (28-char) and Japanese (15-char) naming screens
2. **Locale Flag**: `dword_1004CB78` controls all structure offset differences (JP uses +4 byte offsets in many structs)
3. **Character Tables**: ROM data copied to RAM, 5-DWORD entries (20 bytes each)
4. **Font System**: 6 texture pages cached (0x00 + 0xFA-0xFE for kanji), 64-entry LRU cache

### Critical Globals
- `dword_1004CB78`: JP/EN flag (affects ALL structure access)
- `unk_10051880`: Runtime character table (15 or 28 entries)
- `dword_10050D78`: Character count (15 JP / 28 EN)
- `dword_1004CBBC`: Cached character ID
- `dword_1004CCD0-CCE4`: Font texture page pointers (6 pages)

### Data Flow
1. **Startup**: `new_dll_graphics_driver` → locale detect → version-specific init
2. **Naming Screen**: Character table init → cursor input → `find_character_by_cursor_position` → character lookup
3. **Text Rendering**: Message construction (`construct_message_with_payload`) → font texture load (`render_japanese_font_texture_page`) → transform setup (`setup_japanese_font_texture_transform`) → render

### Porting Strategy for FFNx
1. **Replace Character Tables**: UTF-8 JSON instead of hardcoded Shift-JIS
2. **Skip Binary Patching**: Use FFNx hooking framework
3. **Preserve Locale Flag**: Keep `dword_1004CB78` logic for compatibility
4. **Modernize Font Rendering**: FreeType/stb_truetype instead of texture pages
5. **Keep Message System**: WStringPayload architecture seems sound
6. **Fix Aspect Ratio**: Transform matrices need updating for modern displays
