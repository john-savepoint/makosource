# 6. DEEP DIVE: TECHNICAL CONSTRAINTS & SOLUTIONS

## 6.1 Constraint #1: The Geometry vs. Texture Problem ("Squashed Kanji")

**The Single Most Critical Technical Hurdle**

**Symptom:**
You replace an English character's texture (e.g., 'W') with a full-width Kanji (私). In-game, the Kanji appears horizontally compressed, vertically stretched, or "squashed" like a barcode.

**Root Cause Analysis:**

The FF7 engine **separates geometry generation from texture mapping**. This is a two-stage process:

**Stage 1: Geometry Generation (FF7.exe)**
```c
// Pseudocode of what the game does
void DrawCharacter(char character_code) {
    // 1. Look up width from the table in RAM
    char width = font_width_table[character_code];

    // 2. Generate 3D quad vertices
    float x0 = cursor_x;
    float y0 = cursor_y;
    float x1 = cursor_x + width;   // ← Width comes from table
    float y1 = cursor_y + 16;      // Height is fixed 16px

    // 3. Send to renderer
    Vertex vertices[4] = {
        {x0, y0, uv_x0, uv_y0},
        {x1, y0, uv_x1, uv_y0},
        {x1, y1, uv_x1, uv_y1},
        {x0, y1, uv_x0, uv_y1}
    };
    RenderQuad(vertices, current_texture);

    // 4. Advance cursor
    cursor_x += width;
}
```

**Stage 2: Texture Mapping (FFNx)**
```c
// FFNx receives pre-calculated vertices
void gl_draw_indexed_primitive(Vertex* vertices, int count, uint32_t texture) {
    // FFNx has NO CONTROL over vertex positions
    // It can only change the texture being mapped

    // If vertices define a 8px wide quad...
    // But the texture contains a 64px wide Kanji...
    // The GPU will squash the 64px texture into the 8px quad!

    BindTexture(texture);
    DrawTriangles(vertices, count);
}
```

**Example Failure:**
```
English 'W' in USFONT:
- Width table: font_width_table[0x57] = 12  (12 pixels wide)
- Geometry: 12px × 16px quad
- Texture: 12px wide glyph
- Result: ✅ Perfect fit

Japanese '私' replacing 'W':
- Width table: font_width_table[0x57] = 12  (STILL 12! Not updated)
- Geometry: 12px × 16px quad (STILL narrow!)
- Texture: 64px wide Kanji glyph (from jafont_2.png)
- Result: ❌ 64px texture squashed into 12px quad = barcode Kanji
```

**Visual Representation:**
```
Expected (16px quad):        Actual (8px quad):
┌────────────────┐           ┌──────┐
│                │           │      │
│      私        │           │ 私   │  ← Squashed!
│                │           │      │
└────────────────┘           └──────┘
   16px × 16px                  8px × 16px
```

**The Solution:**

**Patch the width table in RAM BEFORE the game generates geometry:**

```c
void PatchFontWidthsForJapanese() {
    if (font_language != "ja") return;

    // Get pointer to width table (version-agnostic)
    char* width_table = common_externals.font_info;
    if (!width_table) {
        ffnx_error("font_info pointer is NULL! Cannot patch widths.\n");
        return;
    }

    ffnx_info("Patching character width table for Japanese mode...\n");

    // Make memory writable
    DWORD oldProtect;
    if (!VirtualProtect(width_table, 256, PAGE_READWRITE, &oldProtect)) {
        ffnx_error("VirtualProtect failed! Error: %d\n", GetLastError());
        return;
    }

    // Overwrite ALL widths with fixed 16px
    for (int i = 0; i < 256; i++) {
        // 0x00-0x1F are control codes, but we set them anyway (unused for geometry)
        width_table[i] = 0x10;  // 16 pixels in hex
    }

    // Restore original memory protection
    VirtualProtect(width_table, 256, oldProtect, &oldProtect);

    ffnx_info("Width table patched: all characters now 16px wide.\n");
}
```

**When to Call:**
- **MUST** be called during `ff7_init_hooks` (in `src/ff7_opengl.cpp`)
- **MUST** be called AFTER `ff7_data(game_object)` (which sets up `common_externals`)
- **MUST** be called BEFORE any text rendering occurs

**Side Effects:**
- ✅ Fixes Kanji squashing
- ⚠️ Makes English text look "spaced out" (each letter becomes 16px wide)
- ⚠️ May cause text to overflow dialog boxes if mixing English/Japanese
- ✅ Necessary trade-off for correct rendering

---

## 6.2 Constraint #2: The Texture Allocation & Palette System

**Understanding FFNx's Texture Management**

**The Palette Swapping Mechanism:**

FFNx inherits a **palette-swapping system** from the PlayStation version of FF7. This allows multiple color variations of the same texture without duplicating geometry.

**How It Works:**
```c
struct texture_set {
    uint32_t* texturehandle;  // Array of GPU texture handles
    uint32_t palette_index;   // Currently active palette (0-based)
};

// When the game wants to change color:
void common_palette_changed(texture_set* tex, uint32_t new_palette) {
    tex->palette_index = new_palette;
    // Bind the corresponding texture handle
    gl_set_texture(tex->texturehandle[new_palette]);
}
```

**Example (Character Sprites):**
```
Cloud sprite might have:
- texturehandle[0] = Normal color scheme
- texturehandle[1] = Poison (green tint)
- texturehandle[2] = Berserk (red tint)
```

**Our Exploitation:**

We **hijack this system** for font page switching:
```
Font texture_set:
- texturehandle[0] = jafont_1.png (base page)
- texturehandle[1] = jafont_2.png (Kanji A)
- texturehandle[2] = jafont_3.png (Kanji B)
- texturehandle[3] = jafont_4.png (Kanji C)
- texturehandle[4] = jafont_5.png (Kanji D)
- texturehandle[5] = jafont_6.png (Kanji E)
```

**The Allocation Problem:**

**Current FFNx Logic (src/common.cpp:~1457):**
```c
// Determine number of texture slots to allocate
uint32_t num_textures = VREF(tex_header, palettes) > 0
                        ? VREF(tex_header, palettes) * 2
                        : 1;

// Allocate array
VRASS(texture_set, texturehandle,
      (uint32_t*)external_calloc(num_textures, sizeof(uint32_t)));
```

**English USFONT.TEX Header:**
```
palettes = 1
→ num_textures = 1 * 2 = 2
→ Allocates array: texturehandle[0..1]
```

**If We Try to Load 6 Textures Without Override:**
```c
for (int i = 0; i < 6; i++) {
    texture_set->texturehandle[i] = LoadTexture(...);
    // ❌ When i=2: BUFFER OVERFLOW!
    // ❌ When i=3, 4, 5: Writing to unallocated memory
    // ❌ Result: Segmentation fault / heap corruption
}
```

**The Fix - Force Allocation Override:**

```c
// Inside common_load_texture, BEFORE the allocation block
bool is_font_texture = false;
if (VREF(tex_header, file.pc_name)) {
    const char* name = VREF(tex_header, file.pc_name);
    if (strstr(name, "usfont") || strstr(name, "jafont")) {
        is_font_texture = true;
    }
}

if (!VREF(texture_set, texturehandle)) {
    uint32_t num_textures_to_alloc;

    if (is_font_texture && font_language == "ja") {
        // [OVERRIDE] Force 6 slots for Japanese
        num_textures_to_alloc = 6;
        ffnx_info("Japanese font detected: forcing allocation of 6 texture pages.\n");
    } else {
        // [ORIGINAL] Standard behavior
        num_textures_to_alloc = VREF(tex_header, palettes) > 0
                                 ? VREF(tex_header, palettes) * 2
                                 : 1;
    }

    // Allocate with correct size
    VRASS(texture_set, ogl.gl_set->textures, num_textures_to_alloc);
    VRASS(texture_set, texturehandle,
          (uint32_t*)external_calloc(num_textures_to_alloc, sizeof(uint32_t)));
}
```

**Critical Timing:**
- ✅ MUST happen BEFORE any `texturehandle[i]` writes
- ✅ MUST check filename, NOT just rely on config (English might load usfont)
- ✅ MUST allocate EXACTLY 6 (not dynamic based on actual files found)

---

## 6.3 Constraint #3: Registry Virtualization & File Pathing

**The Problem:**

The 2013 Steam/eStore executables were designed to run in a **sandboxed environment** (DRM protection). They don't use the Windows Registry directly. Instead, they call **virtual registry functions** that the driver provides.

**The Virtual Registry System:**

```c
// ff7.exe (or ff7_ja.exe) calls these:
LSTATUS RegOpenKeyExA(HKEY hKey, LPCSTR lpSubKey, ...);
LSTATUS RegQueryValueExA(HKEY hKey, LPCSTR lpValueName, ...);

// But these redirect to:
LSTATUS dotemuRegOpenKeyExA(HKEY hKey, LPCSTR lpSubKey, ...);  // FFNx provides this
LSTATUS dotemuRegQueryValueExA(HKEY hKey, LPCSTR lpValueName, ...);  // FFNx provides this

// FFNx exports these functions (see misc/FFNx.def)
```

**What the Game Queries:**

```c
// The game asks for these registry keys:
RegQueryValueExA(hKey, "AppPath", ...)    // Where is FF7 installed?
RegQueryValueExA(hKey, "DataPath", ...)   // Where is data folder?
RegQueryValueExA(hKey, "MoviePath", ...)  // Where are movies?
```

**Current FFNx Implementation (English-only):**

```c
// src/common.cpp
__declspec(dllexport) LSTATUS __stdcall
dotemuRegQueryValueExA(HKEY hKey, LPCSTR lpValueName, ...) {
    char buf[MAX_PATH];

    if (strcmp(lpValueName, "DataPath") == 0) {
        GetCurrentDirectory(sizeof(buf), buf);
        strcat(buf, "\\data\\");  // ← HARDCODED ENGLISH PATH
        strcpy((CHAR*)lpData, buf);
        return ERROR_SUCCESS;
    }

    // Similar for MoviePath...
}
```

**Why This Breaks for ff7_ja.exe:**

```
ff7_ja.exe requests "DataPath"
→ FFNx returns "C:\FF7\data\"
→ ff7_ja.exe looks for "C:\FF7\data\menu_ja.lgp"
→ File doesn't exist (it's in "C:\FF7\data\lang-ja\menu_ja.lgp")
→ Crash: "Cannot load required data"
```

**The Solution - Language-Aware Paths:**

```c
__declspec(dllexport) LSTATUS __stdcall
dotemuRegQueryValueExA(HKEY hKey, LPCSTR lpValueName, LPDWORD lpReserved,
                       LPDWORD lpType, LPBYTE lpData, LPDWORD lpcbData) {
    char buf[MAX_PATH];
    LSTATUS ret = ERROR_SUCCESS;

    // [NEW] Detect which executable is running
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    _strlwr(exePath);  // Convert to lowercase for easier comparison

    bool isJapaneseExe = (strstr(exePath, "ff7_ja.exe") != NULL);

    /* FF7 Registry Queries */
    if (strcmp(lpValueName, "AppPath") == 0) {
        GetCurrentDirectory(*lpcbData, buf);
        strcat(buf, "\\");
        strcpy((CHAR*)lpData, buf);
    }
    else if (strcmp(lpValueName, "DataPath") == 0) {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-specific path
        if (isJapaneseExe) {
            strcat(buf, "\\data\\lang-ja\\");  // Japanese path
        } else {
            strcat(buf, "\\data\\");           // English path
        }

        strcpy((CHAR*)lpData, buf);
    }
    else if (strcmp(lpValueName, "MoviePath") == 0) {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-specific path
        if (isJapaneseExe) {
            strcat(buf, "\\data\\lang-ja\\movies\\");  // Japanese path
        } else {
            strcat(buf, "\\data\\movies\\");           // English path
        }

        strcpy((CHAR*)lpData, buf);
    }
    // ... other registry keys ...

    return ret;
}
```

**Additional Considerations:**

**Option 1: Exe Detection (Current approach)**
- Pro: Automatic, no user configuration needed
- Pro: Works even if user forgets to set `font_language`
- Con: Requires both exe files to coexist

**Option 2: Config-Based (Alternative)**
```c
if (font_language == "ja") {
    strcat(buf, "\\data\\lang-ja\\");
}
```
- Pro: Works with single exe (ff7.exe) in Japanese mode
- Con: User MUST set `font_language = "ja"` in config
- Con: Crash if misconfigured

**Recommendation:** Use **BOTH** for redundancy:
```c
bool useJapanesePaths = isJapaneseExe || (font_language == "ja");
```

---

## 6.4 Constraint #4: The "JFLEVE" Typo & File Redirection

**The Discovery:**

During asset analysis, a **typo** was found in the Japanese file structure:
- English: `field/flevel.lgp` (correct spelling)
- Japanese: `field/jfleve.lgp` (missing 'l' - likely a packaging error)

**Why This Matters:**

If the English executable runs in Japanese mode, it might request `flevel.lgp`, but the actual file is `jfleve.lgp`. Without redirection, the load fails silently.

**The File Redirection System:**

FFNx has a file redirection layer in `src/redirect.cpp`:

```c
// Simplified version of attempt_redirection
int attempt_redirection(const char* in_path, char* out_path) {
    // 1. Check if file exists as requested
    if (fileExists(in_path)) {
        strcpy(out_path, in_path);
        return 0;  // Found
    }

    // 2. Try mod paths
    char mod_path[MAX_PATH];
    sprintf(mod_path, "mods/%s", in_path);
    if (fileExists(mod_path)) {
        strcpy(out_path, mod_path);
        return 0;
    }

    // 3. Try 7th Heaven VFS
    // ... (complex logic)

    // [NEW] 4. Try Japanese filename variations
    if (font_language == "ja" && strstr(in_path, "flevel.lgp")) {
        // Try the typo'd version
        std::string ja_path = std::string(in_path);
        size_t pos = ja_path.find("flevel.lgp");
        if (pos != std::string::npos) {
            ja_path.replace(pos, strlen("flevel.lgp"), "jfleve.lgp");
            if (fileExists(ja_path.c_str())) {
                strcpy(out_path, ja_path.c_str());
                ffnx_info("Redirected flevel.lgp → jfleve.lgp\n");
                return 0;
            }
        }
    }

    return -1;  // Not found
}
```

**Complete Japanese File Manifest:**

| Component | English | Japanese | Redirection Needed? |
|-----------|---------|----------|---------------------|
| Menu/Font | `menu_us.lgp` | `menu_ja.lgp` | ❌ No (different names) |
| Field Maps | `flevel.lgp` | `jfleve.lgp` | ✅ **YES** (typo) |
| Battle | `battle.lgp` | `battle_ja.lgp` | ❌ No (different names) |
| Movies | `movies/` | `lang-ja/movies/` | ❌ No (handled by registry) |

**Implementation Location:**

Add to `src/redirect.cpp` in the `attempt_redirection` function, **before** the final `return -1`:

```c
// [NEW] Japanese file name corrections
if (font_language == "ja") {
    // Handle the jfleve typo
    if (strstr(in_path, "flevel.lgp") || strstr(in_path, "FLEVEL.LGP")) {
        std::string ja_variant = in_path;

        // Try lowercase typo
        size_t pos = ja_variant.find("flevel.lgp");
        if (pos == std::string::npos) {
            // Try uppercase typo
            pos = ja_variant.find("FLEVEL.LGP");
            if (pos != std::string::npos) {
                ja_variant.replace(pos, 10, "JFLEVE.LGP");
            }
        } else {
            ja_variant.replace(pos, 10, "jfleve.lgp");
        }

        if (fileExists(ja_variant.c_str())) {
            strcpy(out_path, ja_variant.c_str());
            return 0;
        }
    }
}
```

---
