## Chunk 3 Analysis (Lines 10213-10850)

### Function sub_10002B10 (line 10213)
- **Category**: Graphics
- **Purpose**: Renders a texture surface to a DirectX render target. Handles locale-specific rendering (Japanese/English branching), calculates viewport bounds, copies pixel data with memcpy loops, and manages DirectX surface/device operations. Core graphics pipeline function.
- **Suggested Name**: render_surface_to_target
- **Key Calls**: DirectX virtual methods (offset +52, +56, +8, +72, +144, +128, +136), dword_10050654 (memory allocation), memcpy, sub_1001D5C0, sub_1001D600
- **Notes**: Heavy use of dword_1004CB78 locale flag throughout for Japanese/English branching. Complex viewport clipping logic (v70, v71). Accesses global render state variables (dword_1004CB60, dword_1004CB64, nWidth, nHeight). Error logging via dword_1004CBF4/F8/FC/CC00 flags. Potential undefined variables noted by IDA (v1, v61, v62, v63, v37, v38).

### Function sub_10003140 (line 10717)
- **Category**: Graphics
- **Purpose**: Converts raw pixel data from source buffer to ARGB format with color component scaling and alpha blending. Processes multi-byte pixel encodings (16-bit, 24-bit, 32-bit formats), applies bit-shifting for color channel extraction, and handles transparency/alpha calculation. Used for texture data format conversion.
- **Suggested Name**: convert_pixels_to_argb
- **Key Calls**: None (pure computation - no external function calls)
- **Notes**: Uses a2[11] to determine source pixel format (1=8-bit, 2=16-bit, 3=24-bit, 4=32-bit). Complex bitwise operations for color extraction with lookup in a2[16-23] for bit positions and a2[28-31] for scaling factors. Handles alpha channel specially (a7 flag controls transparency mode). Inner loop processes a5×a6 pixel grid. a8 parameter controls alpha skip logic via a2[19] mask.
