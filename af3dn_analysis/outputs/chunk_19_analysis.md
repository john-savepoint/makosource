## Chunk 19 Analysis (Lines 23645-24225)

### Function sub_100139F0 (line 23645)
- **Category**: Graphics
- **Purpose**: Renders a complex UI panel with multiple text elements and selection indicators. Sets up scaling matrices, calculates viewport rectangles, and draws layered 2D sprites with different colors for character selection or menu display.
- **Suggested Name**: render_character_selection_panel
- **Key Calls**: D3DXMatrixScaling, OffsetRect, dword_1004CB20 (sprite drawing function at offset 60), dword_1004CB28 (transform setup), sub_100193F0 (string conversion/handling)
- **Notes**: Extremely complex rendering function with repetitive matrix setup, rectangle calculations, and sprite drawing calls. Uses multiple string buffers (v46, v50, v54, v58, v62) that are conditionally allocated and deallocated. Checks v0[19] to toggle between two color states (-1 vs -11184811). References dword_100492F0 for scaling factor.

### Function sub_100143B0 (line 23968)
- **Category**: Input
- **Purpose**: Checks input state from gamepad/keyboard for six buttons and compares current state against previous frame state. Triggers callbacks if state changes and manages resource cleanup/reallocation.
- **Suggested Name**: handle_input_state_change
- **Key Calls**: sub_10019830 (input retrieval), sub_10011130 (input check), sub_100123A0 (cleanup), operator delete
- **Notes**: Reads input states for buttons 5, 6, 9, 10 using sub_10019830. Stores previous state in word_1004CE94 and byte_1004CE96. If input state changes and *((_DWORD *)v0 + 19) is set, calls a function pointer at v0[18]. Otherwise deletes and resets dword_1004CD14 on state change.

### Function sub_10014540 (line 24113)
- **Category**: Utility
- **Purpose**: Retrieves high-resolution performance counter time and calculates delta time between frames. Handles pause state to track elapsed time accurately.
- **Suggested Name**: get_performance_delta_time
- **Key Calls**: QueryPerformanceFrequency, QueryPerformanceCounter
- **Notes**: Uses Windows performance counter API to measure time. Manages pause state via dword_1004CBC4 and dword_1004CD18. Stores baseline time in dbl_1004CD20, current time in dbl_1004CD30, and delta in dbl_1004CD28. Returns delta time when paused, absolute time when running.

### Function sub_100145D0 (line 24165)
- **Category**: Utility
- **Purpose**: Removes an element from a linked list structure by searching for a node with matching value (a1) and unlinking it using sub_10019E00.
- **Suggested Name**: remove_linked_list_element
- **Key Calls**: sub_10019E00 (unlink operation), _invalid_parameter_noinfo (error handling)
- **Notes**: Iterates through linked list starting at dword_1004CE4C until finding node where [offset+8] equals a1. Performs multiple validity checks comparing list state before/after. Uses v9 array as temporary storage for unlink operation parameters.

### Function sub_10014640 (line 24218)
- **Category**: Utility
- **Purpose**: Extracts up to 16 elements from a linked list into a flat array at address a1. Returns the actual count of elements extracted (max 16).
- **Suggested Name**: extract_linked_list_to_array
- **Key Calls**: _invalid_parameter_noinfo (error validation)
- **Notes**: Iterates through dword_1004CE4C linked list, storing i[2] (data at offset 8) into destination array. Performs boundary checks (max 16 elements) and validity checks on list integrity. Uses dword_1004CE50 to store count, returns min(count, 16). Called for exporting list contents to fixed-size array.
