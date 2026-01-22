## Chunk 20 Analysis (Lines 24226-25159)

### Function sub_100146D0 (line 24226)
- **Category**: Utility
- **Purpose**: Maps input codes (1-237) to sequential output values (19-162). This is a sparse lookup table that translates game-specific control codes or input values to a standardized numbering scheme. Returns -1 for unmapped inputs.
- **Suggested Name**: map_control_code_to_index
- **Key Calls**: None (pure switch statement)
- **Notes**: The sparse case structure (cases 1-82 consecutive, then jumps to 86-88, 100-102, etc.) suggests this is mapping non-contiguous input IDs to a linear index. Many input values are skipped, indicating selective input handling.

### Function sub_10014D90 (line 24476)
- **Category**: Utility
- **Purpose**: Validates and stores a byte value from a global location (dword_1004CAE8) into another global (dword_1004CABC). If the byte is 1-3, stores it directly; otherwise defaults to 1. Likely manages a bounded state variable (mode, page, or similar).
- **Suggested Name**: validate_and_store_bounded_state
- **Key Calls**: None (direct memory access)
- **Notes**: The bounded range check (1-3) suggests this is managing a 3-state system, possibly related to naming screen pages or input modes in the Japanese UI.

### Function sub_10014DC0 (line 24506)
- **Category**: Utility
- **Purpose**: Reads a magic value from memory location 0x401004 and returns a classification code (1, 2, 3, 4, or 0). Case 0x99CE0805 has special logic checking if memory[0x919970] == 36. Appears to identify game version or ROM variant.
- **Suggested Name**: get_game_version_code
- **Key Calls**: None (direct memory reads)
- **Notes**: The magic values (0x99CE0805, 0x99EBF805, 0x99DBC805, -1711908859) suggest ROM header checksums or version identifiers. The special case for value 36 at 0x919970 may indicate a specific game mode or region.

### Function sub_10014E10 (line 24556)
- **Category**: Memory
- **Purpose**: Performs runtime code patching via VirtualProtect. Determines game version, sets up function pointers to different memory locations (dword_1004C790, dword_1004CAF4), and injects JMP instructions (0xE9 = -23) to redirect execution to sub_10014D90 and nullsub_1. This is critical initialization for version-specific behavior.
- **Suggested Name**: patch_function_pointers_for_version
- **Key Calls**: VirtualProtect, sub_10014D90, nullsub_1
- **Notes**: This is a sophisticated code patching routine that: (1) saves original bytes/addresses in dword_1004E620, (2) changes memory protection to PAGE_EXECUTE_READWRITE (0x40), (3) overwrites function prologues with JMP instructions. Different game versions have different patch addresses. This enables runtime function replacement without rebuilding code.

### Function sub_10014FF0 (line 24714)
- **Category**: Init
- **Purpose**: One-time initialization routine (guarded by byte_1004CE97). Calls game version detection (sub_10014DC0), sets locale via setlocale(), applies code patches (sub_10014E10), validates launcher communication (sub_10015520), loads graphics (sub_10015710), and shows error dialog if launcher validation fails. Core initialization sequence.
- **Suggested Name**: initialize_game_engine_once
- **Key Calls**: sub_10014DC0, setlocale, sub_10014E10, sub_10015520, sub_10015710, MessageBoxA, exit_0
- **Notes**: The check for sub_10015520() failure with launcher message suggests the game requires communication with FF7_Launcher.exe. This is game anti-piracy/DRM validation.

### Function sub_10015050 (line 24774)
- **Category**: Utility
- **Purpose**: Copies a null-terminated wide-character (UTF-16) string from dword_1004AFB0 to the provided buffer a1. Uses inline small string optimization (SSO) - if size < 8, reads directly from the address, otherwise dereferences as pointer. Reads 2 bytes at a time until null terminator.
- **Suggested Name**: copy_wide_string_sso
- **Key Calls**: None (direct memory reads)
- **Notes**: The SSO pattern is typical of C++ std::wstring implementations. The "< 8" check suggests strings are stored inline if they fit, preventing allocation overhead.

### Function sub_10015080 (line 24804)
- **Category**: Text
- **Purpose**: Converts a wide-character (UTF-16) string to multibyte (likely Shift-JIS) and stores in Dest buffer. Source may be inline or heap-allocated based on SSO logic (size < 8 check). Calls wcstombs with max length 0x104 (260 bytes).
- **Suggested Name**: convert_wide_to_multibyte_string
- **Key Calls**: wcstombs
- **Notes**: Works with Source global (likely a std::wstring). The 260-byte limit (0x104) matches Windows MAX_PATH convention. Critical for converting Japanese strings between UTF-16 (internal) and Shift-JIS (game format).

### Function sub_100150B0 (line 24834)
- **Category**: File
- **Purpose**: Retrieves the game installation path. If dword_1004AFA4 is set, copies a pre-configured path from memory; otherwise calls SHGetFolderPathW to get "Documents\Square Enix\FINAL FANTASY VII". Stores result in a1 with SSO-aware handling.
- **Suggested Name**: get_game_install_path
- **Key Calls**: SHGetFolderPathW, PathAppendW, wcscpy_s
- **Notes**: Uses CSIDL_PROFILE (32773) to get user profile directory. Handles both configured override paths and default Windows folder locations. Critical for locating game data files.

### Function sub_10015190 (line 24914)
- **Category**: File
- **Purpose**: Processes .ff7 save files. Checks file extension, constructs save file data structure (v8), looks up owner/metadata via sub_10019A80, validates against dword_1004CDD8, then processes save data via sub_10019F40. Uses std::string internal buffer management (v11 >= 0x10 triggers cleanup).
- **Suggested Name**: process_save_file
- **Key Calls**: _stricmp, strlen, sub_100192E0, sub_10019A80, sub_100198D0, sub_10019F40, operator delete
- **Notes**: The 0x10 check is again SSO - cleanup only happens if string was heap-allocated. Variable naming (v2 as Source despite being undefined) suggests IDA decompilation issue.

### Function sub_10015270 (line 24994)
- **Category**: File
- **Purpose**: Validates save file ownership. Looks up owner metadata via sub_10019A80 and verifies it matches dword_1004CDD8 (expected owner). Calls _invalid_parameter_noinfo() if validation fails. Lightweight validation wrapper.
- **Suggested Name**: validate_save_file_owner
- **Key Calls**: sub_10019A80, _invalid_parameter_noinfo
- **Notes**: None

### Function sub_100152B0 (line 25034)
- **Category**: File
- **Purpose**: Validates save file metadata structure. Checks two pointer fields via sub_10019A80 against expected values (dword_1004CDD8 and dword_1004CDF0). If second field doesn't match, calls sub_10019A20 (possibly error handler or repair function). Returns pointer to dword_1004CDF0.
- **Suggested Name**: validate_save_file_metadata
- **Key Calls**: sub_10019A80, sub_10019A20
- **Notes**: None

### Function sub_10015330 (line 25114)
- **Category**: Utility
- **Purpose**: Thread-safe message queueing using mutex and semaphore synchronization. Creates Message object, queues it to dword_1004CDF8 if queue size < 50, signals semaphore and releases mutex. Handles reference counting and cleanup for queued objects. Complex synchronization with interlocked operations.
- **Suggested Name**: enqueue_message_thread_safe
- **Key Calls**: operator new, sub_100114C0, sub_1001E970, sub_10011DB0, WaitForSingleObject, ReleaseMutex, ReleaseSemaphore, _InterlockedExchangeAdd
- **Notes**: Uses Windows synchronization primitives (hMutex, dword_1004CADC semaphore) to manage message queue with 50-item capacity. Reference counting on v11 prevents premature deallocation.

### Function sub_10015430 (line 25244)
- **Category**: Utility
- **Purpose**: Identical to sub_10015330 - thread-safe message queueing with mutex/semaphore synchronization, Message object creation, queue size checking, and reference counting cleanup. Appears to be duplicate code (possibly different message type or priority).
- **Suggested Name**: enqueue_message_thread_safe_alt
- **Key Calls**: operator new, sub_100114C0, sub_1001E970, sub_10011DB0, WaitForSingleObject, ReleaseMutex, ReleaseSemaphore, _InterlockedExchangeAdd
- **Notes**: Code is character-for-character identical to sub_10015330 except missing dword_1004CCF8 assignment at start. Likely generated as separate instantiation or template specialization.

### Function sub_10015520 (line 25342)
- **Category**: Init
- **Purpose**: Initializes IPC (Inter-Process Communication) infrastructure between game and launcher. Opens named semaphores (ff7_launcherCanReadMsgSem, ff7_launcherDidReadMsgSem, etc.), creates mutexes, creates file mapping (ff7_sharedMemoryWithLauncher), maps shared memory, and creates 3 worker threads (StartAddress, sub_10018F50, sub_100190C0). Returns 0 if any step fails. Critical for launcher integration.
- **Suggested Name**: initialize_launcher_ipc
- **Key Calls**: OpenSemaphoreA, CreateMutexA, CreateSemaphoreA, OpenFileMappingA, MapViewOfFile, CreateThread, TerminateThread
- **Notes**: Extensive error checking - returns 0 immediately on any failure. The semaphore/mutex naming convention (ff7_launcherCanReadMsgSem, ff7_gameDidReadMsgSem) indicates bidirectional handshake protocol. Shared memory base at 0x10000 byte offset (dword_1004CAC0 = dword_1004CAC4 + 0x10000) suggests dual-buffer design for launcher↔game communication.
