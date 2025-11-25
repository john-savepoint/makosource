# 12. RISK MITIGATION & DEBUGGING GUIDE

## 12.1 Common Failure Modes & Solutions

### Failure Mode #1: Crash on Startup

**Symptoms:**
- Game crashes before reaching title screen
- No FFNx.log created
- Windows error: "ff7.exe has stopped working"

**Diagnostic Steps:**

1. **Check DLL Loading:**
```
Use Dependency Walker (depends.exe):
- Open ff7.exe
- Look for AF3DN.P or FFNx.dll
- Check if all dependencies are satisfied
```

2. **Check Event Viewer:**
```
Windows → Event Viewer → Application
Look for:
- Access Violation (0xC0000005)
- DLL Not Found (0xC0000135)
```

3. **Enable Debug Mode:**
```toml
# FFNx.toml
trace_all = true
trace_loaders = true
```

**Common Causes & Fixes:**

| Cause | Symptom | Fix |
|-------|---------|-----|
| Missing DLL dependencies | Error code 0xC0000135 | Install Visual C++ Redistributable |
| Invalid registry paths | Crash after splash screen | Check `dotemuRegQueryValueExA` logic |
| Memory corruption in DllMain | Instant crash | Remove global initializations from DllMain |
| Conflicting drivers | Random crash | Remove other graphics mods |

---

### Failure Mode #2: Crash on Menu Open

**Symptoms:**
- Game runs, reaches title screen
- Crashes when entering menu or name selection
- FFNx.log ends abruptly

**Diagnostic Steps:**

1. **Check Last Log Entry:**
```
FFNx.log:
[INFO] Loading texture: usfont
[INFO] Japanese font detected: forcing allocation...
[CRASH] ← Log ends here
```

2. **Check Allocation:**
```cpp
// Add this debug code before crash point:
ffnx_info("Allocated textures: %d\n", VREF(texture_set, ogl.gl_set->textures));
ffnx_info("Texturehandle ptr: 0x%p\n", VREF(texture_set, texturehandle));
```

**Common Causes & Fixes:**

| Cause | Evidence | Fix |
|-------|----------|-----|
| Buffer overflow in texture loading | Crash after "Loading page 3" | Verify 6-slot allocation happened FIRST |
| NULL texture handle access | Crash in `gl_bind_texture_set` | Add null checks before dereferencing |
| Invalid PNG format | Crash in `load_texture_helper` | Re-export PNGs with correct settings |
| Stack overflow (recursion) | Stack trace shows loop | Check for infinite recursion |

**Fix Template:**

```cpp
// BEFORE loading textures
if (!VREF(texture_set, texturehandle)) {
    ffnx_error("Texturehandle array is NULL!\n");
    return 0;
}

uint32_t allocated_slots = VREF(texture_set, ogl.gl_set->textures);
if (allocated_slots < 6) {
    ffnx_error("Not enough slots! Need 6, have %d\n", allocated_slots);
    return 0;
}

// NOW safe to load
for (int i = 0; i < 6; i++) {
    // Load logic...
}
```

---

### Failure Mode #3: Squashed / Corrupted Text

**Symptoms:**
- Game runs without crashes
- Japanese text appears but is:
  - Horizontally compressed (barcode-like)
  - Vertically stretched
  - Wrong aspect ratio

**Diagnostic:**

1. **Screenshot and Measure:**
   - Take screenshot of squashed character
   - Measure pixel dimensions in image editor
   - Compare to expected 16×16 (or 64×64 in high-res)

2. **Check Width Table:**
```cpp
// Add diagnostic dump
char* table = common_externals.font_info;
for (int i = 0; i < 256; i++) {
    if (table[i] != 0x10) {
        ffnx_warning("Width[0x%02X] = %d (expected 16)\n", i, table[i]);
    }
}
```

**Common Causes:**

| Cause | Check | Fix |
|-------|-------|-----|
| Width patch didn't apply | Log missing "Patched width table" | Verify `PatchFontWidthsForJapanese()` is called |
| Applied to wrong address | Characters still variable width | Use `common_externals.font_info`, not hardcoded |
| VirtualProtect failed | Log shows "VirtualProtect failed" | Run as administrator |
| Wrong executable version | Widths correct for some chars, wrong for others | Confirm EXE version matches address map |

**Forced Diagnostic Mode:**

```cpp
void VerifyWidthPatch() {
    char* table = common_externals.font_info;
    if (!table) {
        MessageBoxA(NULL, "font_info is NULL!", "Error", MB_OK);
        return;
    }

    bool all_16px = true;
    for (int i = 0x20; i < 0x100; i++) {
        if (table[i] != 0x10) {
            all_16px = false;
            break;
        }
    }

    if (all_16px) {
        MessageBoxA(NULL, "Width patch SUCCESS!", "Info", MB_OK);
    } else {
        MessageBoxA(NULL, "Width patch FAILED!", "Error", MB_OK);
    }
}
```

---

### Failure Mode #4: Wrong Texture Displayed

**Symptoms:**
- Text appears but with wrong characters
- FA codes show Page 0 characters instead of Page 1
- Random texture pages displayed

**Diagnostic:**

1. **Check g_currentFontPage Value:**
```cpp
// In gl_bind_texture_set
ffnx_info("g_currentFontPage = %d\n", g_currentFontPage);
ffnx_info("Expected page for 0xFA = 1\n");
```

2. **Verify Assembly Hook:**
```
Use debugger:
- Set breakpoint at Hext injection address
- Input text with 0xFA byte
- Check if breakpoint hits
- Verify AL register = 0xFA
- Step through and watch g_currentFontPage change
```

**Common Causes:**

| Cause | Evidence | Fix |
|-------|-------|-----|
| Hext patch wrong address | Breakpoint never hits | Re-find address with debugger |
| Math error in hook | g_currentFontPage = wrong value | Check SUB/INC logic |
| Hook not reading g_currentFontPage | Always shows Page 0 | Verify address in `MOV [addr], AL` |
| Race condition | Flickers between pages | Add synchronization |

**Correct Page Calculation:**

```assembly
; When AL = 0xFA:
SUB AL, 0xFA    ; AL = 0xFA - 0xFA = 0x00
INC AL          ; AL = 0x00 + 1 = 0x01 ✅
                ; g_currentFontPage = 1 (correct for Page 1)

; When AL = 0xFE:
SUB AL, 0xFA    ; AL = 0xFE - 0xFA = 0x04
INC AL          ; AL = 0x04 + 1 = 0x05 ✅
                ; g_currentFontPage = 5 (correct for Page 5)
```

**If Pages are Off by One:**

```assembly
; WRONG version (missing INC):
SUB AL, 0xFA
; AL = 0 for FA, but we want page 1!

; CORRECT:
SUB AL, 0xFA
INC AL          ; ← Don't forget this!
```

---

## 12.2 Memory Debugging Tools

**Tool 1: Cheat Engine**

```
Download: https://cheatengine.org/

Usage for Finding Addresses:
1. Attach to ff7.exe
2. Search: "Unknown initial value" (4-byte)
3. Modify game state (open menu)
4. Search: "Changed value"
5. Repeat until 1-5 candidates
6. Right-click → "Find out what accesses this address"
7. Trigger action → See backtrace
```

**Tool 2: x64dbg**

```
Download: https://x64dbg.com/

Usage for Assembly Debugging:
1. Open ff7.exe
2. Ctrl+G → Enter address (e.g., 0x66E2A0)
3. Set breakpoint (F2)
4. Run (F9)
5. When hit, examine:
   - Registers (AL, ESI, EBP)
   - Stack
   - Memory at ESI (string pointer)
6. Step instruction by instruction (F7)
```

**Tool 3: API Monitor**

```
Download: http://www.rohitab.com/apimonitor

Usage for Registry Call Debugging:
1. Launch API Monitor
2. Select: Kernel32.dll → Registry functions
3. Monitor ff7.exe
4. See all RegQueryValueEx calls
5. Verify our dotemuRegQueryValueExA is called
6. Check returned paths
```

**Tool 4: Process Monitor (ProcMon)**

```
Download: https://docs.microsoft.com/sysinternals

Usage for File Access Debugging:
1. Run ProcMon as admin
2. Filter: Process Name is ff7.exe
3. Filter: Operation contains "Open" or "Read"
4. Start game
5. See exactly which files are requested
6. Check if jfleve.lgp vs flevel.lgp
```

---

## 12.3 Debugging Checklist

When something goes wrong, work through this checklist systematically:

**Phase 1: Environment Verification**

- [ ] FFNx installed correctly (AF3DN.P in game directory)
- [ ] FFNx.log is being created
- [ ] Config file (FFNx.toml) is readable
- [ ] `font_language` is set correctly
- [ ] Font textures exist in `mods/Textures/menu/`
- [ ] File permissions are correct (not read-only)

**Phase 2: Initialization Verification**

- [ ] DllMain executed (check log for "FFNx initialized")
- [ ] `is_using_japanese_exe` detected correctly
- [ ] `read_cfg()` parsed settings (check log)
- [ ] Registry hooks returning correct paths (check log)
- [ ] `ff7_data()` completed (common_externals populated)

**Phase 3: Texture Loading Verification**

- [ ] `common_load_texture` called for font
- [ ] 6 texture slots allocated (check log)
- [ ] All 6 PNGs loaded successfully (check log)
- [ ] Texture handles are non-zero
- [ ] No errors in FFNx.log

**Phase 4: Geometry Verification**

- [ ] `PatchFontWidthsForJapanese()` called
- [ ] `common_externals.font_info` is not NULL
- [ ] VirtualProtect succeeded
- [ ] Width table contains all 0x10 values
- [ ] Log shows "patched successfully"

**Phase 5: Assembly Hook Verification**

- [ ] Hext patch file exists in correct location
- [ ] Addresses in Hext match executable version
- [ ] `g_currentFontPage` address is correct
- [ ] Breakpoint at hook location hits
- [ ] `g_currentFontPage` changes when FA byte is encountered

**Phase 6: Renderer Verification**

- [ ] `gl_bind_texture_set` detects Japanese font (6 textures)
- [ ] Reads `g_currentFontPage` correctly
- [ ] Binds correct texture handle
- [ ] Draw call succeeds
- [ ] Character appears on screen

**Phase 7: Runtime Verification**

- [ ] No memory leaks (check Task Manager over time)
- [ ] No crashes after 30 minutes
- [ ] Performance is acceptable
- [ ] All text systems work (menu, dialogue, battle)

---

## 12.4 Performance Profiling

**Measuring Overhead:**

```cpp
// src/gl/gl.cpp

#include <chrono>

void gl_bind_texture_set(struct texture_set *_texture_set) {
    auto start = std::chrono::high_resolution_clock::now();

    // ... existing logic ...

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    if (duration.count() > 100) {  // Flag if > 100 microseconds
        ffnx_warning("Slow texture bind: %lld μs\n", duration.count());
    }
}
```

**Expected Performance:**

| Operation | Target Time | Acceptable Limit |
|-----------|-------------|------------------|
| Texture bind | < 50 μs | < 100 μs |
| Width table patch | < 1 ms | < 5 ms |
| Texture loading (all 6) | < 500 ms | < 1000 ms |
| Per-character draw | < 100 μs | < 500 μs |

**If Performance is Poor:**

1. **Profile the Bottleneck:**
   - Add timing to each function
   - Identify slowest operation

2. **Common Optimizations:**
   - Cache texture handles (don't reload every frame)
   - Use texture atlases (already done via 6 pages)
   - Reduce logging in release builds
   - Use faster PNG decoder

3. **Release vs Debug:**
```cpp
#ifdef _DEBUG
    // Extensive logging, validation
#else
    // Minimal logging, skip checks
#endif
```

---
