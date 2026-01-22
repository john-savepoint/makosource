## Chunk 15 Analysis (Lines 20226-21033)

### Function sub_1000EFD0 (line 20226)
- **Category**: Text
- **Purpose**: Calculates the total character width of a Shift-JIS encoded string by processing single and double-byte characters. Handles special control codes for color/formatting and recursively processes embedded strings.
- **Suggested Name**: calculate_string_width
- **Key Calls**: sub_1000EB90 (control code handler), sub_1000EF70 (character width lookup), recursive sub_1000EFD0
- **Notes**: Processes up to 1024 bytes; returns 0xFF as string terminator; handles special Shift-JIS ranges (0xFA-0xFE for kanji); tracks v4 as double-byte lead byte state

### Function sub_1000F190 (line 20333)
- **Category**: Graphics
- **Purpose**: Renders a single Japanese character glyph to the vertex buffer by constructing a quad with texture coordinates. Handles character page lookup and applies scaling/positioning based on parameter flags.
- **Suggested Name**: render_character_glyph
- **Key Calls**: sub_1000ED80 (special case for code 217), dword_1004CCD0/CCD4/CCD8/CCDC/CCE0/CCE4 (font texture page pointers), MEMORY[0x66E272] (memory check)
- **Notes**: Uses qmemcpy to copy vertex data; builds 32-float vertex buffer (8 floats per quad vertex); handles 6 font pages (0x00, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE); sets MEMORY[0xDC3CEC] flag after write

### Function sub_1000F5C0 (line 20567)
- **Category**: Text
- **Purpose**: Main text rendering loop that processes a Shift-JIS string byte-by-byte, handles multi-byte characters, control codes, and special formatting while accumulating horizontal position. Recursively calls itself for embedded strings.
- **Suggested Name**: render_text_string
- **Key Calls**: sub_1000F190 (character rendering), sub_1000EB90 (control code handler), recursive sub_1000F5C0, MEMORY[0x91AA8C] (enabled check), MEMORY[0x91F034] (max character count)
- **Notes**: Complex state machine with v7 tracking double-byte state; handles control codes 0xE and 0xF; up to 1024 byte limit; references global arrays unk_10042480 and unk_1004247C for nested strings

### Function sub_1000F7D0 (line 20766)
- **Category**: Text
- **Purpose**: Renders a multi-line text block with special handling for control codes, italic/bold flags, and text alignment. Validates against magic bytes and manages line wrapping and character counting.
- **Suggested Name**: render_text_block
- **Key Calls**: sub_1000F5C0 (line rendering), sub_1000EB90 (control code handling), MEMORY[0xDC3CCC] (render loop check)
- **Notes**: Checks for magic bytes unk_10042488 at start; manages flags MEMORY[0xDC3CC0] and MEMORY[0xDC3CC4]; handles special codes 0xD2-0xD9 and 0xEA; limits to 1024 characters (0x400)

### Function sub_1000FB80 (line 21019)
- **Category**: Utility
- **Purpose**: Performs character-level lookup and patches in game data structures. Checks for specific word patterns (866, 1098) and applies conditional modifications to memory.
- **Suggested Name**: patch_character_data
- **Key Calls**: None (direct memory reads/writes)
- **Notes**: Checks array at offset 0xCBFC00 for 0xFFFF markers; handles two special cases with magic constants 1162625325 and 1095583014; modifies memory at MEMORY[0xDC0D26] with bounds checking

### Function sub_1000FC60 (line 21083)
- **Category**: Text
- **Purpose**: Thin wrapper that delegates character rendering to sub_1000F190 with a1=1 (first parameter).
- **Suggested Name**: render_character_simple
- **Key Calls**: sub_1000F190
- **Notes**: Fixed parameters: a1=1, a7=0; passes through a2-a5 directly

### Function sub_1000FCC0 (line 21107)
- **Category**: Text
- **Purpose**: Thin wrapper that delegates string rendering to sub_1000F5C0 with a6=0 and a7=0.
- **Suggested Name**: render_text_string_mode0
- **Key Calls**: sub_1000F5C0
- **Notes**: Fixed parameters: a6=0, a7=0; passes through a1, a2, a3, a4, a5

### Function sub_1000FCF0 (line 21127)
- **Category**: Text
- **Purpose**: Thin wrapper that delegates string rendering to sub_1000F5C0 with a6=1 and a7=0. Differs from sub_1000FCC0 only in the a6 parameter (rendering mode).
- **Suggested Name**: render_text_string_mode1
- **Key Calls**: sub_1000F5C0
- **Notes**: Fixed parameters: a6=1, a7=0; passes through a1, a2, a3, a4, a5; used for alternate rendering mode

### Function sub_1000FD20 (line 21147)
- **Category**: Text
- **Purpose**: Conditional string renderer that adjusts rendering position based on a1 value (checks against MEMORY[0x9261C8] + 20) and maintains a dword counter (dword_1004CCE8).
- **Suggested Name**: render_text_string_conditional
- **Key Calls**: sub_1000F5C0
- **Notes**: Maintains state in dword_1004CCE8; calculates vertical offset as 92*counter+100; increments counter; used for multi-line or paginated text

### Function sub_1000FDA0 (line 21169)
- **Category**: Text
- **Purpose**: Renders centered text with special digit formatting. Converts digit strings to display format, calculates center position, and handles optional flag for numeric display mode.
- **Suggested Name**: render_centered_text
- **Key Calls**: sub_1000EFD0 (width calculation), sub_1000F5C0 (text rendering), MEMORY[0xDC3630] (text structure array)
- **Notes**: Checks for pattern (12, 0x8A) as numeric string marker; converts digits by adding 35; uses v21 buffer for conversion; calculates center position from text descriptor struct at MEMORY[0xDC3630]+152*a2

### Function sub_1000FF60 (line 21326)
- **Category**: Utility
- **Purpose**: Wraps external function call and conditionally updates dword_1004CCEC based on parameter value.
- **Suggested Name**: call_external_with_mode_update
- **Key Calls**: MEMORY[0x719C08] (external function)
- **Notes**: When a1==100, sets dword_1004CCEC to 0 if <2, otherwise 3; appears to be UI mode selection logic

### Function sub_1000FF90 (line 21356)
- **Category**: Init
- **Purpose**: Patches game code by writing pointers into two memory locations (0x718BF6 and 0x7191E6) and updates related configuration values based on dword_1004CCF0 state.
- **Suggested Name**: patch_game_pointers
- **Key Calls**: VirtualProtect, memcpy (via direct MEMORY writes)
- **Notes**: Uses VirtualProtect PAGE_EXECUTE_READWRITE (0x40); patches point to unk_100424B8 + 90*dword_1004CCF0; sets MEMORY[0xDD4544] and MEMORY[0xDD4554] to 5 if counter>=2, else 9

### Function sub_10010010 (line 21406)
- **Category**: Text
- **Purpose**: Conditional text renderer that adjusts rendering mode character based on dword_1004CCF0 value. Maps three UI states to character values and delegates to sub_1000F5C0.
- **Suggested Name**: render_text_conditional_mode
- **Key Calls**: sub_1000F5C0
- **Notes**: Checks a2 against 210, 238, 266 and sets v5 based on dword_1004CCF0 (UI state); used for rendering mode indicators

### Function sub_10010080 (line 21453)
- **Category**: Utility
- **Purpose**: Scans game data starting at address 0x14501A0 for first non-question-mark byte. Returns 1 if non-zero byte found within 1024 bytes, 0 if all 0xFF or 1024 bytes scanned.
- **Suggested Name**: scan_game_data_for_content
- **Key Calls**: None (direct memory reads)
- **Notes**: Starts at fixed address 14501360 (0xDD0850 in hex); treats 0xFF as end marker; limit 1024 bytes

### Function sub_10010110 (line 21476)
- **Category**: Utility
- **Purpose**: Conditional jump dispatcher that calls sub_10010080 to determine execution path. Jumps to 0x719076 if content found, otherwise 0x71914C.
- **Suggested Name**: conditional_execution_dispatcher
- **Key Calls**: sub_10010080
- **Notes**: Uses JUMPOUT to transfer control; implements trampoline pattern for code injection/patching

### Function sub_10010130 (line 21492)
- **Category**: Init
- **Purpose**: Complex game code patching routine that modifies multiple memory locations with VirtualProtect, installs hooks, and sets up function pointers for Japanese text rendering integration. Central initialization for text system patches.
- **Suggested Name**: init_japanese_text_patches
- **Key Calls**: VirtualProtect (multiple), sub_1000FF60, sub_1000FC90, sub_10010110, memcpy (via MEMORY writes)
- **Notes**: Patches 6+ memory locations; uses dword_10042628 array for hook locations; saves original values in dword_10049344/48/50/4C; installs jump tables and function pointers; critical system initialization

### Function sub_100102C0 (line 21663)
- **Category**: Utility
- **Purpose**: Initializes a 164-byte game structure with randomized bytes from lookup tables unk_10042638 and unk_10042740. Used for data initialization or random content generation.
- **Suggested Name**: init_randomized_game_structure
- **Key Calls**: rand, memcpy
- **Notes**: Allocates/writes to 164*(a1) byte offset in 15143392; uses 3 random tables with 88-byte stride; copies v2+2 bytes then 2-v2+2 bytes; terminates with 0xFF marker at offset 6
