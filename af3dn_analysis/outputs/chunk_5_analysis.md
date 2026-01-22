## Chunk 5 Analysis (Lines 11849-12689)

### Function sub_10004390 (line 11849)
- **Category**: Text
- **Purpose**: Looks up a character attribute (likely glyph position or width) from a table based on index `a2` and offset stored in `a3`. Returns pointer to the attribute data. Branches on locale flag.
- **Suggested Name**: lookup_character_attribute
- **Key Calls**: sub_10003FF0
- **Notes**: Accesses offsets +2208 (JP) or +2080 (EN) from base, suggesting parallel data structures for Japanese vs English character handling

### Function sub_10004400 (line 11858)
- **Category**: Graphics
- **Purpose**: Renders a character or sprite by setting up transformation data and calling rendering function. Handles locale-specific data structure offsets.
- **Suggested Name**: render_character_sprite
- **Key Calls**: sub_10003FF0, qmemcpy, sub_1000B740
- **Notes**: Copies 64 bytes (0x40) of transformation data to unk_1004E578, suggests matrix/transform operations; calls render function with 8 parameters

### Function sub_100044F0 (line 11897)
- **Category**: Text
- **Purpose**: Retrieves a character index or pointer based on locale flag and input parameter. Conditionally calls either sub_100085D0 (JP) or sub_1000E470 (EN).
- **Suggested Name**: get_character_index_by_locale
- **Key Calls**: sub_100085D0, sub_1000E470
- **Notes**: Clear locale branching pattern; offset +0x18 (JP) vs +0x14 (EN) suggests different data layouts

### Function sub_10004550 (line 11913)
- **Category**: Text
- **Purpose**: Updates character state/selection flags based on input parameter `a1`. Sets flags at offsets +2344 (JP) or +2076 (EN), then calls rendering/update function.
- **Suggested Name**: update_character_selection_state
- **Key Calls**: sub_100085D0, sub_1000E470
- **Notes**: Complex branching logic with multiple offset reads; appears to manage mutual exclusion between two state flags (v10 and v5)

### Function sub_10004660 (line 11979)
- **Category**: Text
- **Purpose**: Stores current state to history array (dword_100512C0) and marks character as active if not already. Returns 0 if already active, 1 if newly activated.
- **Suggested Name**: push_character_state_to_history
- **Key Calls**: sub_10004550, qmemcpy
- **Notes**: Manages history stack with 8-entry limit (dword_1004CBA8); copies 184 bytes (0xB8) per entry from dword_1004E540

### Function sub_10004700 (line 12019)
- **Category**: Text
- **Purpose**: Pops and restores the most recent character state from history array. Clears active flags after restoration.
- **Suggested Name**: pop_character_state_from_history
- **Key Calls**: sub_1000B530
- **Notes**: Decrements history counter before popping; restores state to offset +2204 (JP) or +2076 (EN)

### Function sub_10004780 (line 12057)
- **Category**: Utility
- **Purpose**: Simple flag setter that enables a feature or mode by setting dword_1004CC04 to 1.
- **Suggested Name**: enable_feature_flag
- **Key Calls**: None
- **Notes**: Minimal function, possibly initialization for optional feature

### Function sub_100047A0 (line 12064)
- **Category**: Graphics
- **Purpose**: Sets up parameters and calls sub_1000B740 (render function) with character glyph/sprite data. Extracts coordinates and dimensions from locale-specific structure.
- **Suggested Name**: render_character_glyph_simple
- **Key Calls**: sub_1000B740
- **Notes**: Parameters mirror sub_1000B740 signature (8 params); reads glyph dimensions at offsets +0x2C, +0x18, +0x20 (JP) or +44, +24, +32 (EN)

### Function sub_10004810 (line 12093)
- **Category**: Graphics
- **Purpose**: Complex glyph rendering loop that renders multiple consecutive identical glyphs (character run). Accumulates width/height deltas for positioning. Calls sub_1000B740 per run.
- **Suggested Name**: render_character_run_batch
- **Key Calls**: sub_100033B0, sub_1000CED0, sub_1000B740
- **Notes**: 40-line function with 26 local variables; handles character width compression (runs of same char); increments dword_100501EC (glyph counter); includes offset +0x28 for character data pointer

### Function sub_10004AE0 (line 12297)
- **Category**: Graphics
- **Purpose**: Wrapper function that calls sub_100047A0 with fixed a3 parameter of 3.
- **Suggested Name**: render_character_wrapper_type3
- **Key Calls**: sub_100047A0
- **Notes**: Simple indirection; parameter `a3=3` likely indicates render type or layer

### Function sub_10004B00 (line 12307)
- **Category**: Graphics
- **Purpose**: Wrapper function that calls sub_10004810 with fixed a3 parameter of 3.
- **Suggested Name**: render_character_run_wrapper_type3
- **Key Calls**: sub_10004810
- **Notes**: Parallel to sub_10004AE0; batches glyph runs with render type 3

### Function sub_10004B20 (line 12317)
- **Category**: Graphics
- **Purpose**: Performs glyph rendering with optional transformation/animation data. Reads scale/transform factors and copies animation frame data before rendering.
- **Suggested Name**: render_character_with_transform
- **Key Calls**: sub_10003FF0, qmemcpy
- **Notes**: Handles animation frames; copies 64 bytes (0x40) from two possible locations based on condition at offset +156/+152; scales values by dword_1004CB60/dword_1004CB64

### Function sub_10004C20 (line 12411)
- **Category**: Graphics
- **Purpose**: Wrapper that calls sub_10004810 with a3=2.
- **Suggested Name**: render_character_run_wrapper_type2
- **Key Calls**: sub_10004810
- **Notes**: Type-2 rendering variant; same signature as other wrappers

### Function sub_10004C40 (line 12427)
- **Category**: Graphics
- **Purpose**: Extracts character glyph parameters and calls sub_1000B740 render function. Handles locale-specific offsets into character data structure.
- **Suggested Name**: render_glyph_from_character_data
- **Key Calls**: sub_1000B740
- **Notes**: Reads offsets: +11/+44 (width?), +6/+24 (x?), +8/+32 (y?), +3/+12 (u0?), +5/+20 (v0?); calls render with type 2

### Function sub_10004CB0 (line 12477)
- **Category**: Utility
- **Purpose**: Simple flag setter that enables dword_1004CC08 if not already set.
- **Suggested Name**: enable_render_feature_flag
- **Key Calls**: None
- **Notes**: Mirrors sub_10004780 structure; separate feature flag

### Function sub_10004CD0 (line 12490)
- **Category**: Memory
- **Purpose**: Allocates and initializes a character/glyph structure with transformation matrices and animation data. Scales dimensions by resolution factors.
- **Suggested Name**: allocate_and_init_character_struct
- **Key Calls**: dword_10050694 (allocator)
- **Notes**: Allocates from either JP (v11) or EN (v10) memory pool; copies 128 bytes (0x80) of animation frame data from dword_10051010; applies aspect ratio scaling via dword_10050620 and dword_10051D80

### Function sub_10004E30 (line 12607)
- **Category**: Math
- **Purpose**: Updates high-resolution timer state using QueryPerformanceCounter and timeGetTime. Synchronizes performance counter with system time to prevent drift.
- **Suggested Name**: update_hires_timer
- **Key Calls**: QueryPerformanceCounter, timeGetTime
- **Notes**: Complex timer sync logic; maintains qword_10050D70 (perf counter) and dword_10050DB8 (system time); includes drift detection and correction (20ms threshold); used for frame timing

### Function sub_10004FA0 (line 12689)
- **Category**: Math
- **Purpose**: Wrapper for sub_10004E30 with scaling factor of 1.
- **Suggested Name**: update_timer_normal_speed
- **Key Calls**: sub_10004E30
- **Notes**: Multiplies timer deltas by 1; maintains same precision as base timer

### Function sub_10004FB0 (line 12699)
- **Category**: Math
- **Purpose**: Wrapper for sub_10004E30 with scaling factor of 5.
- **Suggested Name**: update_timer_fast_speed
- **Key Calls**: sub_10004E30
- **Notes**: Multiplies timer deltas by 5; used for accelerated playback or special effects

### Function sub_10005000 (line 12709)
- **Category**: Init
- **Purpose**: Initializes DirectX 9 rendering context, creates device, and queries graphics adapter. Sets up presentation parameters and device creation flags based on configuration.
- **Suggested Name**: init_directx_device
- **Key Calls**: Direct3DCreate9, GetAdapterIdentifier, StringFromGUID2, wcstombs, IDirect3D9::CreateDevice
- **Notes**: Critical initialization function; checks dword_1004AF1C and dword_1004AF24 for fullscreen/VSYNC flags; creates presentation params at dword_10050D80-dword_10050DAC; exits with error if device creation fails

### Function sub_100051A0 (line 12813)
- **Category**: Utility
- **Purpose**: CPU/processor detection function that identifies processor type via instruction patterns in memory. Returns processor ID (1-20) or 0 if unknown.
- **Suggested Name**: detect_cpu_type
- **Key Calls**: None (direct memory inspection)
- **Notes**: Matches x86 instruction opcodes at 0x401004 and secondary checks at 0x401404 to identify specific processors; returns 1-16 for known types, 20 for special case of type 1; appears to be anti-emulation or hardware-specific optimization check
