# 8. IMPLEMENTATION SPECIFICATION: ASSEMBLY HOOKS

## 8.1 The Text Parser Hook Concept

**Objective:** Intercept the game's text byte stream to detect FA-FE page markers.

**Current Game Logic (Simplified):**

```c
// Pseudocode of FF7's text rendering loop
void RenderTextString(const char* text) {
    const char* ptr = text;

    while (*ptr != 0x00) {  // Loop until NULL terminator
        char current_byte = *ptr;

        // Skip control codes (0x00-0x1F)
        if (current_byte < 0x20) {
            HandleControlCode(current_byte);
            ptr++;
            continue;
        }

        // Render the character
        DrawCharacter(current_byte);
        ptr++;
    }
}
```

**Our Modification:**

```c
// Modified logic (injected via Assembly)
void RenderTextString(const char* text) {
    const char* ptr = text;

    while (*ptr != 0x00) {
        char current_byte = *ptr;

        // [NEW] Check for page markers (FA-FE)
        if (current_byte >= 0xFA && current_byte <= 0xFE) {
            // Calculate page index: FA→1, FB→2, FC→3, FD→4, FE→5
            uint8_t page_index = current_byte - 0xFA + 1;

            // Update global state (FFNx will read this)
            g_currentFontPage = page_index;

            // Skip to next byte (the actual character index)
            ptr++;
            current_byte = *ptr;  // Now load the character
        } else {
            // Normal character, use page 0
            g_currentFontPage = 0;
        }

        // Skip control codes
        if (current_byte < 0x20) {
            HandleControlCode(current_byte);
            ptr++;
            continue;
        }

        // Render the character (with updated page index)
        DrawCharacter(current_byte);
        ptr++;
    }
}
```

---

## 8.2 Finding the Injection Point

**⚠️ CRITICAL: Address Discovery Process**

The exact memory address for the hook varies by executable version. Here's how to find it:

**Step 1: Set Up Debugging Tools**

- Install **x64dbg** (https://x64dbg.com/) or **Cheat Engine** (https://cheatengine.org/)
- Launch FF7 with FFNx installed
- Attach debugger to `ff7.exe` process

**Step 2: Locate Font Texture Loading**

```
1. Set breakpoint on CreateTextureA or D3DCreateTexture
2. Run game until breakpoint hits
3. Check call stack for function that requested the texture
4. If texture name contains "usfont", note the return address
```

**Step 3: Trace Back to Text Rendering**

```
1. From texture load, step back through call stack
2. Look for function named similar to:
   - draw_graphics_object
   - render_text
   - display_string
3. Note the function's start address (e.g., 0x66E272)
```

**Step 4: Find the Character Processing Loop**

```assembly
; Inside the text rendering function, look for this pattern:

LODSB              ; Load byte from [ESI] into AL, increment ESI
CMP AL, 0x00       ; Check for NULL terminator
JE EndOfString     ; If 0, jump to end
CMP AL, 0x1F       ; Check if control code
JBE ControlCode    ; If <= 0x1F, handle control code
CALL DrawChar      ; Otherwise, draw the character
JMP LoopStart      ; Repeat

; The injection point is RIGHT AFTER LODSB
; and BEFORE the first CMP
```

**Step 5: Verify the Address**

```
1. Set breakpoint at the LODSB instruction
2. Start a new game and enter a name
3. Breakpoint should hit repeatedly as name is rendered
4. Verify AL register contains ASCII values of your name
5. Note the address (e.g., 0x66E2A0)
```

**Known Addresses (Reference Only - DO NOT HARDCODE):**

| Version | Text Render Function | Character Loop | Notes |
|---------|---------------------|----------------|-------|
| US 1.02 | `0x66E272` | `~0x66E2A0` | Approximation |
| Steam (2013) | **Different** | **Different** | Use debugger |
| ff7_ja.exe | **Different** | **Different** | Use debugger |

**⚠️ WARNING:** These addresses are **APPROXIMATIONS** and may be incorrect. **ALWAYS verify with a debugger.**

---

## 8.3 The Hext Patch Implementation

**Create New File: misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt**

```hext
# FFNx Japanese Font Support - Text Parser Hook
#
# This patch intercepts the character processing loop to detect
# FA-FE page marker bytes and update the global font page variable.
#
# Target: FF7.exe (US 1.02)
# Location: Character processing loop inside text rendering function
#
# ⚠️ CRITICAL: The address below (0x66E2A0) is a PLACEHOLDER.
# You MUST replace it with the actual address found via debugger.
#
# Register assumptions (verify with debugger):
#   AL  = Current character byte (just loaded by LODSB)
#   ESI = String pointer (points to next character)
#   EBP = Stack frame pointer

# Set base offset (MUST match your debugger findings)
# Replace 0x66E2A0 with the actual address of the injection point
+0x66E2A0

# ================================================================
# INJECTED CODE STARTS HERE
# ================================================================

# Save original instruction that we're overwriting
# (This MUST be copied from the actual game code at this address)
# Example: If the original code was "CMP AL, 0x00", you'd put:
# CMP AL, 0x00

# Check if character byte is >= 0xFA (page marker range)
CMP AL, 0xFA
JB NormalCharacter     # If below 0xFA, it's a normal character

# ---- Page Marker Detected ----

# Calculate page index: FA→1, FB→2, FC→3, FD→4, FE→5
SUB AL, 0xFA           # AL = AL - 0xFA (FA→0, FB→1, etc.)
INC AL                 # AL = AL + 1 (0→1, 1→2, etc.)

# Store in global variable
# ⚠️ PLACEHOLDER: 0xCC0000 is a TEMPORARY address
# You MUST allocate a proper address (see section 8.4)
MOV BYTE PTR [0xCC0000], AL

# Advance to next byte (the actual character index)
INC ESI                # ESI now points to character index byte
MOV AL, [ESI]          # Load character index into AL

# Jump to the character drawing code
# (This address MUST match the location right after the original CMP)
JMP 0x66E2B0           # PLACEHOLDER - adjust to match actual code

# ---- Normal Character (no page marker) ----
NormalCharacter:

# Reset page index to 0 (base page)
MOV BYTE PTR [0xCC0000], 0

# Continue with original code flow
# (The game's original instruction goes here)
# Example:
# CMP AL, 0x1F
# (Replace with actual instruction)

# ================================================================
# INJECTED CODE ENDS HERE
# ================================================================
```

**Hext Syntax Reference:**

```hext
+0xADDRESS       # Set absolute address for following code
=BYTES           # Write raw bytes
JMP ADDR         # x86 jump instruction
CMP AL, VAL      # x86 compare instruction
MOV [ADDR], REG  # x86 move instruction
```

**⚠️ CRITICAL WARNINGS:**

1. **DO NOT USE 0xCC0000 IN PRODUCTION**
   - This is a placeholder address
   - It may conflict with game memory
   - Could cause random crashes
   - See Section 8.4 for proper allocation

2. **VERIFY ALL ADDRESSES**
   - Hext patches are **NOT** position-independent
   - Wrong addresses = instant crash
   - Test thoroughly after any game patch/update

3. **BACKUP ORIGINAL INSTRUCTIONS**
   - You're overwriting game code
   - Must recreate original behavior
   - Incorrect restoration = broken game logic

---

## 8.4 Global Variable Allocation for g_currentFontPage

**The Problem:**

The Hext patch needs to write to a memory address that:
1. Is safe (won't conflict with game data)
2. Is readable by FFNx C++ code
3. Persists across function calls

**Solution Options:**

**Option A: Static Allocation in FFNx DLL (Recommended)**

```cpp
// src/globals.h
#pragma pack(push, 1)
extern "C" {
    // Export this variable so the Hext patch can find it
    __declspec(dllexport) uint8_t g_currentFontPage;
}
#pragma pack(pop)

// src/common.cpp
uint8_t g_currentFontPage = 0;  // Default to page 0

// To get the address (for Hext patch):
// In DllMain:
void* page_ptr = &g_currentFontPage;
ffnx_info("g_currentFontPage address: 0x%p\n", page_ptr);
// Output: "g_currentFontPage address: 0x10AB1234"
// Use this address in the Hext patch!
```

**Hext patch update:**
```hext
# Replace 0xCC0000 with the actual address logged above
MOV BYTE PTR [0x10AB1234], AL  # Example address
```

**Option B: Allocate in Game Memory Space**

```cpp
// src/common.cpp
uint8_t* g_currentFontPage_ptr = nullptr;

void AllocateFontPageVariable() {
    // Find unused memory in the game's address space
    // FF7's executable typically loads at 0x400000
    // We can use space right after the .data section

    // Example: Allocate at a known safe address
    // (This requires memory map analysis)
    DWORD safe_address = 0xCC0000;  // Example

    g_currentFontPage_ptr = (uint8_t*)safe_address;

    // Make it writable
    DWORD oldProtect;
    VirtualProtect(g_currentFontPage_ptr, 1, PAGE_READWRITE, &oldProtect);

    // Initialize
    *g_currentFontPage_ptr = 0;

    ffnx_info("Allocated g_currentFontPage at: 0x%p\n", g_currentFontPage_ptr);
}
```

**Option C: Use Existing Game Variable (Advanced)**

If you find an unused byte in the game's memory (via debugger inspection), you can repurpose it:

```cpp
// Example: If you find that address 0x99DDFF is always 0 and never read
#define GAME_UNUSED_BYTE ((uint8_t*)0x99DDFF)

// In FFNx code:
uint8_t current_page = *GAME_UNUSED_BYTE;

// In Hext patch:
MOV BYTE PTR [0x99DDFF], AL
```

**Recommendation:**

Use **Option A** (Static DLL Export) because:
- ✅ Guaranteed safe (no conflicts)
- ✅ Easy to access from C++
- ✅ Portable across game versions
- ✅ No risk of overwriting game data

**Complete Implementation:**

```cpp
// src/globals.h
#ifndef GLOBALS_H
#define GLOBALS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Japanese font support
__declspec(dllexport) extern uint8_t g_currentFontPage;

#ifdef __cplusplus
}
#endif

#endif // GLOBALS_H
```

```cpp
// src/common.cpp
#include "globals.h"

uint8_t g_currentFontPage = 0;

// In DllMain or common_init:
void LogGlobalAddresses() {
    ffnx_info("=== FFNx Global Variable Addresses ===\n");
    ffnx_info("g_currentFontPage: 0x%p\n", (void*)&g_currentFontPage);
    ffnx_info("=======================================\n");
    ffnx_info("Use the address above in your Hext patch!\n");
}
```

**Finding the Address at Runtime:**

After compiling and running FFNx, check the log file:

```
FFNx.log:
[INFO] g_currentFontPage: 0x10AB1234
```

Update your Hext patch:

```hext
# Use the logged address
MOV BYTE PTR [0x10AB1234], AL
```

---
