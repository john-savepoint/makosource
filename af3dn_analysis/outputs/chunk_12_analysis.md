## Chunk 12 Analysis (Lines 17450-18362)

### Function sub_1000B740 (line 17450)
- **Category**: Graphics
- **Purpose**: Renders text or graphics with matrix transformations and blend modes. Sets up projection matrices (ortho or world-view-projection), configures render states, and dispatches draw call with vertex data.
- **Suggested Name**: render_with_transform
- **Key Calls**: D3DXMatrixMultiply, SetRenderState (offset 228), GetParameter (offset 36), SetValue (offset 84), DrawPrimitive (offset 336)
- **Notes**: Branches on a2 value (0-3) to select between ortho and perspective matrices. Updates global vertex counter dword_100501F0. Uses callback-style function pointers stored at dword_1004CB8C vtable offsets.

### Function sub_1000B9D0 (line 17637)
- **Category**: Graphics
- **Purpose**: Sets blend mode for both Japanese and English text rendering pipelines. Applies blend mode to shader constants via vtable function at offset 60, handles separate pipelines based on dword_1004CB78 (locale flag).
- **Suggested Name**: set_blend_mode
- **Key Calls**: GetParameter (offset 36), SetValue (offset 60), stores result in dword_1004E548
- **Notes**: Branch on blend mode value (0-4) controls specific render states (D3DRS_SRCBLEND, D3DRS_DESTBLEND values like 5, 2, 6, 1, 4). Handles both JP and EN text rendering contexts separately.

### Function sub_1000BBB0 (line 17816)
- **Category**: Text
- **Purpose**: Renders formatted text with Japanese character support. Builds vertex/index buffers for each character glyph, handles line wrapping, applies color, and dispatches rendering with proper matrix transformations.
- **Suggested Name**: render_formatted_text_jp
- **Key Calls**: _vsnprintf (format string parsing), dword_100508FC (character width lookup), sub_1000B9D0 (blend mode), sub_10003A60 (setup), sub_1000B740 (render), malloc/free (vertex buffer allocation)
- **Notes**: Allocates 4100-byte buffer for formatted string, creates vertex/index buffers per character. Uses byte_10050720 lookup table for character metrics. Handles JP (dword_1004CB78==1) and EN text separately with different buffer configurations. Line wrapping at dword_10050620 boundary.

### Function sub_1000C380 (line 18228)
- **Category**: Graphics
- **Purpose**: Initializes main rendering pipeline state. Sets viewport, blend modes, render states, and prepares for frame rendering by configuring device state and setting blend mode to 4.
- **Suggested Name**: init_render_frame
- **Key Calls**: dword_10050660 (state init), SetViewport (offset 72), SetTexture (offset 148), SetSamplerState (offset 156), SetRenderState (offset 188), sub_10001340, sub_1000B9D0, sub_1000CF70, sub_1000B0A0
- **Notes**: Copies rendering state from dword_1004E540 to dword_1004E480. Sets dword_1004E570=0 and dword_1004E548=4. Calls sub_1000B0A0 to clear backbuffer/viewport.

### Function sub_1000C5B0 (line 18401)
- **Category**: Graphics
- **Purpose**: Cleanup function for rendering context. Releases render target/viewport resources and restores saved state from dword_1004E480.
- **Suggested Name**: cleanup_render_context
- **Key Calls**: GetRenderTarget (offset 72), SetRenderTarget (offset 148), SetTexture (offset 156), sub_1000B530 (restore state)
- **Notes**: Very short function; appears to be callback-style invocation with retaddr used as object pointer. Restores viewport state before returning.

### Function sub_1000C640 (line 18433)
- **Category**: Init
- **Purpose**: Creates render target and depth stencil surfaces for off-screen rendering. Sets up shader parameters and configures render target resources.
- **Suggested Name**: create_render_surfaces
- **Key Calls**: CreateRenderTarget (offset 92), CreateDepthStencilSurface (offset 116), GetRenderTarget (offset 72), SetRenderTarget (offset 160), GetDepthStencilSurface (offset 156)
- **Notes**: Uses parameters a1 (width?), a2 (height?), a3 (format?). Stores render target in dword_1004E53C and depth stencil in dword_1004E604/dword_1004E5FC. Multiple error flags track creation success.

### Function sub_1000C750 (line 18543)
- **Category**: Utility
- **Purpose**: Releases render surface objects. Simple wrapper that destroys three surface objects via virtual method calls at offset 8.
- **Suggested Name**: release_render_surfaces
- **Key Calls**: Release (offset 8) called on three objects
- **Notes**: Releases dword_1004E53C, dword_1004E604, and dword_1004E5FC surfaces in sequence.

### Function sub_1000C780 (line 18573)
- **Category**: Graphics
- **Purpose**: Compiles and links shader pipeline (2 vertex shaders + 2 pixel shaders). Loads HLSL from files, compiles with D3DXCompileShaderFromFileA, and sets shaders as active in device.
- **Suggested Name**: compile_shader_pipeline
- **Key Calls**: D3DXCompileShaderFromFileA (4 calls for VS main, VS yuv, PS main, PS yuv), GetFunction (offset 12), SetVertexShader/SetPixelShader (offset 364/424), SetPixelShader (offset 428)
- **Notes**: Shader source files referenced via dword_10051D84 (vertex) and dword_10051D90 (pixel). Two separate rendering pipelines (main + yuv) with error tracking flags. Returns 0 if any shader compilation fails.

### Function sub_1000C9D0 (line 18684)
- **Category**: Utility
- **Purpose**: Releases compiled shader objects. Destroys all four shader compiled code buffers.
- **Suggested Name**: release_compiled_shaders
- **Key Calls**: Release (offset 8) called on four objects
- **Notes**: Releases dword_1004E454, dword_1004E464, dword_1004E460, and dword_1004E444 shader buffers.

### Function sub_1000CA10 (line 18708)
- **Category**: Graphics
- **Purpose**: Activates compiled shaders in device. Retrieves function pointers from compiled shader buffers and sets them as active vertex/pixel shaders.
- **Suggested Name**: activate_compiled_shaders
- **Key Calls**: GetFunction (offset 12), SetVertexShader (offset 364), SetPixelShader (offset 424), GetPixelShader (offset 428)
- **Notes**: Processes shaders in pairs (VS/PS for main pipeline, VS/PS for yuv pipeline). Returns final pixel shader selection result. Complements sub_1000C780 by linking compiled shaders.
