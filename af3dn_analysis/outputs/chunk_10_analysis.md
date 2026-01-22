## Chunk 10 Analysis (Lines 15551-16490)

### Function sub_100090C0 (line 15551)
- **Category**: Audio
- **Purpose**: Initializes FFmpeg audio/video decoding pipeline for playback. Opens media file, finds video and audio streams, initializes codecs, allocates frame buffers, and sets up audio playback hardware interface.
- **Suggested Name**: init_ffmpeg_playback
- **Key Calls**: av_open_input_file, av_find_stream_info, avcodec_find_decoder, avcodec_open, avcodec_alloc_frame
- **Notes**: Stores stream indices in dword_1004FF6C (video) and dword_1004FE88 (audio). Calculates frame timing via dbl_1004FF60. Initializes audio hardware via dword_1004FE78 (likely Direct Sound).

### Function sub_100093F0 (line 15722)
- **Category**: Audio
- **Purpose**: Returns playback position from audio hardware interface. Simple wrapper that calls release/close method on audio interface if available.
- **Suggested Name**: get_audio_playback_position
- **Key Calls**: Indirect vtable call (+72 offset) on dword_1004C5D4
- **Notes**: None

### Function sub_10009410 (line 15739)
- **Category**: Graphics
- **Purpose**: Loads decoded video frame data into a DirectX surface for display. Manages rotating surface buffer (max 10 surfaces). Copies raw pixel data to GPU memory via D3DXLoadSurfaceFromMemory.
- **Suggested Name**: upload_video_frame_to_gpu
- **Key Calls**: D3DXLoadSurfaceFromMemory, vtable calls for surface management
- **Notes**: Rotating buffer at dword_1004FEC0 cycles through 10 surfaces (% 0xA). Uses dword_1004CC34 as ring buffer index.

### Function sub_10009500 (line 15859)
- **Category**: Graphics
- **Purpose**: Renders accumulated video frames to output. Copies render state from dword_1004E540, calls render functions with video dimensions and color depth.
- **Suggested Name**: render_accumulated_frames
- **Key Calls**: sub_1000CF70, sub_1000B0A0, sub_1000B530
- **Notes**: None

### Function sub_10009580 (line 15890)
- **Category**: Graphics
- **Purpose**: Loads scaled video frame data into DirectX surface. Handles 2x downscaling when flag set. Manages rotating surface buffers (10 total) for triple-buffered rendering.
- **Suggested Name**: upload_scaled_video_frame
- **Key Calls**: D3DXLoadSurfaceFromMemory, vtable surface creation/release calls
- **Notes**: dword_1004FEC4 array holds scaled surfaces. Supports optional 2x downscaling via a1 parameter (half resolution).

### Function sub_10009670 (line 15996)
- **Category**: Graphics
- **Purpose**: Processes decoded video frame through all three scaling levels (1x, 1/2x, 1/4x) for multi-resolution rendering pipeline. Increments ring buffer counter.
- **Suggested Name**: process_video_frame_all_scales
- **Key Calls**: sub_10009580 (called 3 times with different scale parameters)
- **Notes**: Assumes dword_1004CC2C contains decoded frame pointer. Ring buffer cycles every 10 frames.

### Function sub_100096C0 (line 16048)
- **Category**: Audio
- **Purpose**: Synchronizes audio playback position with video timeline. Calculates audio sample offset based on elapsed performance counter time and updates audio buffer position.
- **Suggested Name**: sync_audio_to_video
- **Key Calls**: QueryPerformanceCounter, vtable call (+52 offset) on dword_1004CC3C
- **Notes**: Uses performance counter for precise timing synchronization. Updates every 0x384 frames (~900 frames).

### Function sub_10009740 (line 16098)
- **Category**: Audio
- **Purpose**: Main playback loop that reads FFmpeg packets, decodes audio/video frames, uploads to GPU, manages audio buffering, handles synchronization timing, and controls frame pacing.
- **Suggested Name**: main_playback_loop
- **Key Calls**: av_read_frame, avcodec_decode_video2, avcodec_decode_audio3, av_free_packet, QueryPerformanceCounter
- **Notes**: Complex state machine handling both video and audio. Implements frame rate limiting via performance counter. Handles audio volume calculation via logarithmic scaling. Returns 0 when playback ends.

### Function sub_10009C60 (line 16568)
- **Category**: Audio
- **Purpose**: Seeks to beginning of media file. Returns result of avformat_seek_file call.
- **Suggested Name**: seek_media_to_start
- **Key Calls**: avformat_seek_file
- **Notes**: Simple wrapper for seeking to start (parameters all zero/negative). No error handling beyond checking if context exists.

### Function sub_10009C90 (line 16593)
- **Category**: Utility
- **Purpose**: Returns current playback frame counter. Trivial getter function.
- **Suggested Name**: get_playback_frame_count
- **Key Calls**: None
- **Notes**: None

### Function sub_10009CA0 (line 16603)
- **Category**: Init
- **Purpose**: Patches 6 functions via code hooks by modifying 5-byte jmp instructions. Allocates vtable for playback interface containing 7 function pointers. Initializes complete video playback system.
- **Suggested Name**: install_playback_hooks_and_init
- **Key Calls**: VirtualProtect, calloc, multiple function references (sub_10009EE0, sub_1000A0A0, sub_1000A0C0, sub_1000A160, sub_1000A0F0, sub_1000A1D0)
- **Notes**: Patches functions at dword_1005067C, 10050680, 10050684, 10050688, 1005068C, 10050690. Stores jump patch history in dword_1004E620 array. Creates vtable at dword_1004FE98 with 7 methods.

### Function sub_10009EE0 (line 16739)
- **Category**: File
- **Purpose**: Resolves video file paths for special ending/boss cutscenes (ending2.avi, jenova_e.avi). Reconstructs full path using international language strings from wide character buffer. Initializes video playback engine.
- **Suggested Name**: load_video_file_with_locale
- **Key Calls**: StrStrA, StrRStrIA, wcstombs, PathAppendA, sub_10017FD0, dword_10051034 (function pointer call)
- **Notes**: Supports Japanese locale path reconstruction. Handles dword_1004AFB0 as wide character buffer (likely Japanese path). Calls sub_10017FD0 for resource initialization.

### Function sub_1000A0A0 (line 16859)
- **Category**: Audio
- **Purpose**: Stops video playback. Calls cleanup function and retrieves shutdown status via vtable.
- **Suggested Name**: stop_video_playback
- **Key Calls**: sub_1000A0F0, vtable call (+8 offset)
- **Notes**: Sets dword_10051030+516 to 0 (likely playback state flag).

### Function sub_1000A0C0 (line 16877)
- **Category**: Audio
- **Purpose**: Handles audio subsystem state transition. Sets audio active flag if not already set, initializes audio hardware, and begins playback.
- **Suggested Name**: activate_audio_playback
- **Key Calls**: sub_10018060, sub_1000A160
- **Notes**: dword_10051030+508 is audio active flag. Guards against multiple initializations via boolean check.

### Function sub_1000A0F0 (line 16896)
- **Category**: Audio
- **Purpose**: Cleans up audio playback, stops audio hardware, resets state flags. Calls opening video check and initializes locale-based rendering.
- **Suggested Name**: cleanup_audio_playback
- **Key Calls**: vtable call (+20 offset), sub_1001E600, sub_100192E0
- **Notes**: Checks for "opening.avi" and updates global state dword_1004CCF8 if present. Initializes unk_1004AF3C (possibly font or locale data).

### Function sub_1000A160 (line 16943)
- **Category**: Audio
- **Purpose**: Main playback frame update loop. Polls audio playback status via vtable. Continues rendering frames until playback status becomes non-zero or a2 (likely a timeout/flag) becomes false.
- **Suggested Name**: playback_frame_update_loop
- **Key Calls**: vtable calls (+12 and +16 offsets)
- **Notes**: Implements busy-wait loop for frame-accurate audio sync. Sets dword_10051030+512 flag when complete. Likely blocks rendering until audio ready.

### Function sub_1000A1D0 (line 16983)
- **Category**: Audio
- **Purpose**: Returns audio playback status. Simple conditional wrapper that calls vtable if audio is active.
- **Suggested Name**: get_audio_playback_status
- **Key Calls**: vtable call (+24 offset)
- **Notes**: None

### Function sub_1000A1F0 (line 16998)
- **Category**: Audio
- **Purpose**: Sets audio playback volume based on master volume (dword_1004C784) and user volume control (dword_1004C770). Converts linear volume to decibels via logarithmic formula and applies to audio interface.
- **Suggested Name**: set_audio_volume
- **Key Calls**: vtable call (+60 offset) on dword_1004C5D4
- **Notes**: Volume formula: 20*log10(value/100). Returns -10000 (muted) if calculated volume is zero. Used for game menu volume control.

### Function sub_1000A2A0 (line 17061)
- **Category**: Audio
- **Purpose**: Renders audio data from vgmstream decoder into dual-buffer audio hardware. Handles incomplete frames by padding with silence. Manages circular audio buffer with position tracking.
- **Suggested Name**: render_audio_to_hardware_buffer
- **Key Calls**: render_vgmstream, malloc, memcpy, memset, free, vtable call (+44 and +76 offsets)
- **Notes**: dword_1004C5A4 is audio sample size. Supports partial frame rendering with silence padding. Circular buffer at dword_1004C78C with size dword_1004C77C. Used for both vgmstream and FFmpeg audio paths.
