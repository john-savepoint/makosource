## Chunk 14 Analysis (Lines 19269-20225)

### Function sub_1000DAC0 (line 19269)
- **Category**: File
- **Purpose**: Opens or creates a file with complex path resolution logic that handles .bin, .P, .ff7, and ff7input.cfg files with special directory navigation relative to "data\" subdirectories.
- **Suggested Name**: open_file_with_path_resolution
- **Key Calls**: calloc, malloc, strlen, _stricmp, StrChrA, mbstowcs, wcsstr, PathAppendW, wcstombs, GetCurrentDirectoryA, sub_10015050, sub_100150B0, SHCreateDirectory, StrPBrkA, _wfopen, fseek, sub_1000D6F0, sub_1000DA70
- **Notes**: Implements complex path resolution logic for multiple file types with special handling for .P cache files and directory structure navigation. References dword_10051100 for file handle management.

### Function sub_1000E160 (line 19397)
- **Category**: File
- **Purpose**: Reads data from a file handle with validation that the file pointer matches expected internal state. Returns number of bytes read or -1 on error.
- **Suggested Name**: validated_file_read
- **Key Calls**: fread, ferror, sub_10019A80, sub_1000D930, _invalid_parameter_noinfo
- **Notes**: Validates file state before reading; uses dword_1004CDD8 as reference pointer for validation. Delegates to sub_1000D930 if a3[3] flag is set (possibly LGP archive read).

### Function sub_1000E220 (line 19457)
- **Category**: File
- **Purpose**: Reads exactly ElementCount bytes from file, returning boolean true if read succeeded, false otherwise.
- **Suggested Name**: file_read_exact_count
- **Key Calls**: fread, sub_10019A80, sub_1000D930, _invalid_parameter_noinfo
- **Notes**: Similar validation to sub_1000E160 but returns boolean success/failure instead of byte count. Likely used for validation of critical reads.

### Function sub_1000E2C0 (line 19517)
- **Category**: File
- **Purpose**: Raw file read wrapper with minimal state validation. Directly wraps fread with pointer validation.
- **Suggested Name**: validated_raw_fread
- **Key Calls**: fread, sub_10019A80, _invalid_parameter_noinfo
- **Notes**: Simpler than sub_1000E160; only validates the Stream pointer matches expected state via sub_10019A80.

### Function sub_1000E310 (line 19567)
- **Category**: File
- **Purpose**: Writes data to file with optional buffer allocation. Allocates temporary buffer if Buffer is null, writes, then frees if allocated.
- **Suggested Name**: file_write_with_allocation
- **Key Calls**: calloc, free, fwrite, sub_10015270
- **Notes**: Calls sub_10015270 before writing, possibly for prewrite setup. Returns boolean indicating success (v5 == Count).

### Function sub_1000E390 (line 19647)
- **Category**: File
- **Purpose**: Retrieves file size from file handle. Uses _fstat64i32 for regular files or delegates to sub_1000D9F0 for LGP archive files.
- **Suggested Name**: get_file_size
- **Key Calls**: _fstat64i32, sub_1000D9F0
- **Notes**: Checks a1[3] flag to determine if file is from LGP archive (a3[4] appears to be archive index).

### Function sub_1000E3E0 (line 19697)
- **Category**: File
- **Purpose**: Returns current file position via ftell. Includes basic validation that stream is valid.
- **Suggested Name**: get_file_position
- **Key Calls**: ftell
- **Notes**: Checks Stream->_flag for validity; appears to have confusing offset calculation (Stream->_cnt + 4) which may indicate decompiled artifact.

### Function sub_1000E400 (line 19717)
- **Category**: File
- **Purpose**: Seeks to a position in file with pointer validation before performing fseek.
- **Suggested Name**: validated_file_seek
- **Key Calls**: fseek, sub_10019A80, _invalid_parameter_noinfo
- **Notes**: Only seeks if a1 is valid and bit 12 (0x1000 = bit 3 of dword offset) is not set. References dword_1004CDD8.

### Function sub_1000E470 (line 19767)
- **Category**: Graphics
- **Purpose**: Complex rendering function that processes and renders scene objects based on visibility and transformation flags. Handles both skinned and unskinned geometry with custom render state management.
- **Suggested Name**: render_scene_objects
- **Key Calls**: sub_10008DA0, dword_1005103C, dword_10051038, dword_1005104C, dword_10051054, dword_10051040, dword_10051044, dword_10051048, sub_1000B740, sub_1000B6A0, sub_10003FF0
- **Notes**: Extremely complex function with nested conditionals handling transformation matrices, sprite rendering, custom render passes. References dword_1005103C, dword_10051038, dword_10051040, dword_10051044, dword_10051048 which appear to be function pointers for render callbacks. Manages vertex/matrix data at offsets +3, +19, +20, etc.

### Function sub_1000EAB0 (line 20097)
- **Category**: Graphics
- **Purpose**: Renders a simple 2D quad/triangle strip (4 vertices, 3 indices) with hardcoded index pattern [0,1,2].
- **Suggested Name**: render_simple_quad
- **Key Calls**: sub_1000B740
- **Notes**: Renders to index 4 with 3 indices, vertices at 3, 4 indices. Used for simple geometric shapes, likely UI or debug rendering.

### Function sub_1000EB10 (line 20157)
- **Category**: Graphics
- **Purpose**: Renders geometry object with 3 indices, extracting vertex/index data from structure a1 at specific offsets.
- **Suggested Name**: render_indexed_geometry
- **Key Calls**: sub_1000B740
- **Notes**: Extracts rendering parameters from structure: offset +8 (vertex count?), +16 (index count), +20, +24, +28. Renders with 3 as index buffer parameter.

### Function sub_1000EB40 (line 20187)
- **Category**: Init
- **Purpose**: Patches function addresses by writing x86 JMP instructions. For each address in a2 array, writes 0xE8 (CALL) or 0xE9 (JMP) prefix followed by relative offset to a1.
- **Suggested Name**: patch_function_calls
- **Key Calls**: VirtualProtect
- **Notes**: Uses VirtualProtect to change page permissions to PAGE_EXECUTE_READWRITE (0x40) while writing patches. Iterates flOldProtect times through a2 array of function pointers.

### Function sub_1000EB90 (line 20237)
- **Category**: Utility
- **Purpose**: Decodes color value from lookup table based on instruction pointer, storing result as RGB in a2 and returning the decoded color index (capped at 255).
- **Suggested Name**: decode_color_from_table
- **Key Calls**: sub_10019830
- **Notes**: Reads from dword_10041780, dword_10041784, byte_10041788 arrays with stride of 9 bytes per entry, supporting up to 222 colors (0xDD). Result format: 4 bytes RGB + 1 byte at offset +8.

### Function sub_1000EBE0 (line 20297)
- **Category**: Graphics
- **Purpose**: Executes a graphics operation (via MEMORY[0x66E272]) on primary device a1, then repeats same operation on 6 auxiliary devices from dword_1004CCD0 array.
- **Suggested Name**: apply_graphics_op_to_all_devices
- **Key Calls**: MEMORY[0x66E272] (external function), dword_1004CCD0 array
- **Notes**: Pattern suggests multi-device rendering or synchronization. dword_1004CCD0 appears to hold handles to auxiliary graphics devices.

### Function sub_1000EC20 (line 20337)
- **Category**: Graphics
- **Purpose**: Similar to sub_1000EBE0 but calls MEMORY[0x66E62C] instead, operating on primary device and 6 auxiliary devices.
- **Suggested Name**: apply_state_to_all_devices
- **Key Calls**: MEMORY[0x66E62C] (external function)
- **Notes**: Pattern identical to sub_1000EBE0; suggests different operation type (possibly state cleanup vs. state setup).

### Function sub_1000EC50 (line 20367)
- **Category**: Graphics
- **Purpose**: Applies graphics operation (MEMORY[0x66E641]) with parameter a2 to primary device and 6 auxiliary devices, bracketed by dword_1004E560 flag set/clear.
- **Suggested Name**: apply_graphics_op_with_flag
- **Key Calls**: MEMORY[0x66E641] (external function), dword_1004E560 flag
- **Notes**: Sets dword_1004E560 = 1 before operations, clears to 0 after. Flag may indicate "multi-device operation in progress" for synchronization.

### Function sub_1000ECA0 (line 20407)
- **Category**: Graphics
- **Purpose**: Similar pattern to previous device-sync functions, calling MEMORY[0x670FD3] on primary and 6 auxiliary devices.
- **Suggested Name**: cleanup_all_devices
- **Key Calls**: MEMORY[0x670FD3] (external function)
- **Notes**: Different function pointer address (0x670FD3) suggests cleanup or finalization operation.

### Function sub_1000ED10 (line 20437)
- **Category**: Graphics
- **Purpose**: Executes graphics operation with 5 parameters on primary device, then executes same operation on 6 auxiliary devices substituting off_10049320[i] for parameter a4.
- **Suggested Name**: apply_parametric_op_to_devices
- **Key Calls**: MEMORY[0x6710AC] (external function), off_10049320 array
- **Notes**: off_10049320 contains 6 pointers (likely device identifiers) that are substituted for parameter a4 in auxiliary device calls. Pattern suggests resource allocation or binding operation.

### Function sub_1000ED80 (line 20507)
- **Category**: Graphics
- **Purpose**: Builds and uploads a 4-vertex quad (2x2 triangle strip) to GPU vertex buffer with position, Z-depth, U texture coordinate, and alpha. Returns quad width in screen units.
- **Suggested Name**: upload_quad_vertices
- **Key Calls**: MEMORY[0x66E272], MEMORY[0xDC0FD4]
- **Notes**: Constructs v21 array as 32-float vertex buffer (8 floats per vertex): [x, y, z, w, NaN, -1.7e38, u, v] pattern. Sets alpha blending via MEMORY[0xDC0FD4] + 120 and MEMORY[0xDC0FD4] + 124. References MEMORY[0xDC3CEC] as completion flag.

### Function sub_1000EF70 (line 20747)
- **Category**: Text
- **Purpose**: Looks up character glyph width from font metric tables. Returns width (max 64) based on character code using three lookup tables for different character ranges.
- **Suggested Name**: get_character_glyph_width
- **Key Calls**: dword_10041F70, dword_10042370, dword_100423F0 arrays
- **Notes**: Uses dword_10041F70[256] for codes 0-255, dword_10042370[32] for codes in range [-1312, -1281], dword_100423F0[32] for codes in range [-800, -769]. Width capped at 64 pixels.
