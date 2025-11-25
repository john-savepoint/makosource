# 7. IMPLEMENTATION SPECIFICATION: C++ MODIFICATIONS

## 7.1 Configuration Extension (src/cfg.h, src/cfg.cpp)

**Objective:** Add user-facing toggles to `FFNx.toml` without breaking existing functionality.

**File: src/cfg.h**

Add these declarations **AFTER** existing `extern` declarations:

```cpp
// src/cfg.h

// ... existing externs ...
extern long external_music_volume;
extern bool ff7_advanced_blinking;
extern long display_index;

// [NEW] Japanese Language Support Configuration
extern std::string font_language;         // "en", "ja" - Primary language toggle
extern bool font_enable_furigana;         // true/false - Enable Furigana rendering
extern std::string font_path_override;    // Custom path for font textures (advanced users)
extern bool is_using_japanese_exe;        // Runtime detection flag (set by DllMain)
```

**File: src/cfg.cpp**

Add definitions and parsing logic:

```cpp
// src/cfg.cpp

// [NEW] Definitions (at top with other definitions)
std::string font_language;
bool font_enable_furigana;
std::string font_path_override;
bool is_using_japanese_exe = false;  // Default to false, set during init

void read_cfg()
{
    // ... existing parsing code ...

    // [NEW] Parse font configuration from FFNx.toml
    // Place this BEFORE the "SAFE DEFAULTS" section

    font_language = config["font_language"].value_or("en");

    // Validate font_language value
    if (font_language != "en" && font_language != "ja") {
        ffnx_warning("Invalid font_language '%s'. Defaulting to 'en'.\n",
                     font_language.c_str());
        font_language = "en";
    }

    font_enable_furigana = config["font_enable_furigana"].value_or(false);
    font_path_override = config["font_path_override"].value_or("");

    // Log configuration
    ffnx_info("Font Language: %s\n", font_language.c_str());
    if (font_enable_furigana) {
        ffnx_info("Furigana: Enabled\n");
    }
    if (!font_path_override.empty()) {
        ffnx_info("Font Path Override: %s\n", font_path_override.c_str());
    }

    // ... rest of read_cfg() ...
}
```

**User-Facing Configuration (FFNx.toml):**

Users will add these lines to their `FFNx.toml`:

```toml
###############################################################################
# Japanese Language Support
###############################################################################

# Font language ("en" = English, "ja" = Japanese)
# Default: "en"
font_language = "ja"

# Enable Furigana (reading guides above Kanji)
# Note: Requires special font textures with Furigana data
# Default: false
font_enable_furigana = false

# Custom font texture path (advanced users only)
# Leave empty to use default: mods/Textures/menu/
# Example: "mods/CustomFonts/ja/"
# Default: ""
font_path_override = ""
```

---

## 7.2 Runtime Executable Detection & Registry Hooks (src/common.cpp)

**Objective:** Detect if `ff7_ja.exe` is running and provide correct registry paths.

**Location: DllMain (Entry Point)**

```cpp
// src/common.cpp

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // ... existing initialization ...

        // [NEW] Detect Japanese executable
        char moduleName[MAX_PATH];
        if (GetModuleFileNameA(NULL, moduleName, MAX_PATH)) {
            _strlwr(moduleName);  // Convert to lowercase

            if (strstr(moduleName, "ff7_ja.exe") != NULL) {
                is_using_japanese_exe = true;
                ffnx_info("Detected Japanese executable: ff7_ja.exe\n");

                // Force Japanese language mode
                font_language = "ja";
                ffnx_info("Auto-enabled Japanese language mode.\n");
            }
        }

        // ... rest of initialization ...
        break;
    }
    return TRUE;
}
```

**Location: dotemuRegQueryValueExA (Virtual Registry)**

```cpp
// src/common.cpp

__declspec(dllexport) LSTATUS __stdcall dotemuRegQueryValueExA(
    HKEY hKey,
    LPCSTR lpValueName,
    LPDWORD lpReserved,
    LPDWORD lpType,
    LPBYTE lpData,
    LPDWORD lpcbData)
{
    char buf[MAX_PATH];
    LSTATUS ret = ERROR_SUCCESS;

    // Determine if we should use Japanese paths
    bool useJapanesePaths = is_using_japanese_exe || (font_language == "ja");

    /* FF7 Registry Keys */
    if (strcmp(lpValueName, "AppPath") == 0)
    {
        GetCurrentDirectory(*lpcbData, buf);
        strcat(buf, "\\");
        strcpy((CHAR*)lpData, buf);

        if (trace_all || trace_registry) {
            ffnx_trace("AppPath: %s\n", buf);
        }
    }
    else if (strcmp(lpValueName, "DataPath") == 0)
    {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-aware path
        if (useJapanesePaths) {
            strcat(buf, "\\data\\lang-ja\\");
            ffnx_info("DataPath (Japanese): %s\n", buf);
        } else {
            strcat(buf, "\\data\\");
            if (trace_all || trace_registry) {
                ffnx_trace("DataPath (English): %s\n", buf);
            }
        }

        strcpy((CHAR*)lpData, buf);
    }
    else if (strcmp(lpValueName, "MoviePath") == 0)
    {
        GetCurrentDirectory(*lpcbData, buf);

        // [MODIFIED] Language-aware path
        if (useJapanesePaths) {
            strcat(buf, "\\data\\lang-ja\\movies\\");
            ffnx_info("MoviePath (Japanese): %s\n", buf);
        } else {
            strcat(buf, "\\data\\movies\\");
            if (trace_all || trace_registry) {
                ffnx_trace("MoviePath (English): %s\n", buf);
            }
        }

        strcpy((CHAR*)lpData, buf);
    }
    // ... handle other registry keys (CDROM path, etc.) ...
    else
    {
        ret = ERROR_FILE_NOT_FOUND;
    }

    return ret;
}
```

**Also Update Other Registry Functions:**

```cpp
// src/common.cpp

__declspec(dllexport) LSTATUS __stdcall dotemuRegOpenKeyExA(
    HKEY hKey,
    LPCSTR lpSubKey,
    DWORD ulOptions,
    REGSAM samDesired,
    PHKEY phkResult)
{
    // Log for debugging
    if (trace_all || trace_registry) {
        ffnx_trace("RegOpenKeyExA: %s\n", lpSubKey);
    }

    // Always succeed (we fake the registry)
    *phkResult = hKey;
    return ERROR_SUCCESS;
}

// Similar for dotemuRegCloseKey, etc.
```

---

## 7.3 Texture Allocation Override (src/common.cpp)

**Objective:** Force allocation of 6 texture slots for Japanese fonts.

**Location: common_load_texture function (~Line 1450)**

**⚠️ CRITICAL SECTION - Buffer Overflow Prevention**

```cpp
// src/common.cpp

struct texture_set *common_load_texture(
    struct texture_set *_texture_set,
    struct tex_header *_tex_header,
    struct texture_format *texture_format)
{
    // ... existing variable declarations ...
    VOBJ(texture_set, texture_set, _texture_set);
    VOBJ(tex_header, tex_header, _tex_header);

    // no existing texture set, create one
    if (!VPTR(texture_set))
    {
        _texture_set = common_externals.create_texture_set();
        VASS(texture_set, texture_set, _texture_set);
    }

    if(!VREF(texture_set, ogl.gl_set))
    {
        VRASS(texture_set, ogl.gl_set, common_externals.create_texture_format());
    }

    // [NEW] Detect if this is a font texture BEFORE allocation
    bool is_font_texture = false;
    if (VREF(tex_header, file.pc_name)) {
        const char* tex_name = VREF(tex_header, file.pc_name);

        // Check for font texture names (case-insensitive)
        char lower_name[256];
        strncpy(lower_name, tex_name, sizeof(lower_name));
        _strlwr(lower_name);

        if (strstr(lower_name, "usfont") || strstr(lower_name, "jafont")) {
            is_font_texture = true;
            ffnx_info("Font texture detected: %s\n", tex_name);
        }
    }

    // texture handle array may not have been initialized
    if(!VREF(texture_set, texturehandle))
    {
        uint32_t num_textures;

        if (is_font_texture && font_language == "ja") {
            // [CRITICAL OVERRIDE] Force 6 texture slots for Japanese
            num_textures = 6;
            ffnx_info("Japanese mode: Allocating %d texture pages for font.\n", num_textures);
        }
        else {
            // [ORIGINAL LOGIC] Standard palette-based allocation
            num_textures = VREF(tex_header, palettes) > 0
                           ? VREF(tex_header, palettes) * 2
                           : 1;

            if (trace_all || trace_loaders) {
                ffnx_trace("Allocating %d texture slots (palettes=%d).\n",
                           num_textures, VREF(tex_header, palettes));
            }
        }

        // Allocate the array
        VRASS(texture_set, ogl.gl_set->textures, num_textures);
        VRASS(texture_set, texturehandle,
              (uint32_t*)external_calloc(num_textures, sizeof(uint32_t)));

        if (!VREF(texture_set, texturehandle)) {
            ffnx_error("Failed to allocate texture handle array!\n");
            return NULL;
        }

        // ... rest of initialization (stats, etc.) ...
        stats.texture_count++;
    }

    // ... rest of common_load_texture function ...

    return _texture_set;
}
```

**Validation Logic:**

Add safety checks to verify allocation succeeded:

```cpp
// Later in common_load_texture, before loading textures:
if (is_font_texture && font_language == "ja") {
    uint32_t allocated_count = VREF(texture_set, ogl.gl_set->textures);
    if (allocated_count < 6) {
        ffnx_error("CRITICAL: Font texture allocation failed! Expected 6, got %d\n",
                   allocated_count);
        return NULL;  // Abort to prevent corruption
    }
}
```

---

## 7.4 Multi-Page Texture Loader (src/saveload.cpp)

**Objective:** Load all 6 Japanese font textures when requested.

**Location: load_external_texture function**

```cpp
// src/saveload.cpp

uint32_t load_external_texture(
    const char* name,
    uint32_t* width,
    uint32_t* height,
    struct texture_set* texture_set)
{
    // ... existing code ...

    // [NEW] Special handler for Japanese fonts
    // This MUST execute BEFORE the standard texture loading logic
    if (font_language == "ja" && (strstr(name, "usfont") || strstr(name, "jafont"))) {
        ffnx_info("Japanese font loading initiated for: %s\n", name);

        // Determine base path
        std::string base_path;
        if (!font_path_override.empty()) {
            base_path = font_path_override;
            ffnx_info("Using custom font path: %s\n", base_path.c_str());
        } else {
            base_path = mod_path + "/menu/";
        }

        // Load all 6 pages
        bool all_loaded = true;
        uint32_t first_handle = 0;

        for (int i = 0; i < 6; i++) {
            char filename[1024];

            // Construct filename: jafont_1.png, jafont_2.png, etc.
            // Note: Files are 1-indexed (jafont_1), array is 0-indexed (i=0)
            _snprintf(filename, sizeof(filename), "%sjafont_%d.png",
                      base_path.c_str(), i + 1);

            // Normalize path (convert / to \ on Windows)
            normalize_path(filename);

            // Load texture from disk
            uint32_t w, h;
            uint32_t tex_handle = load_texture_helper(filename, &w, &h, true, true);

            if (tex_handle) {
                // Store in the texture set array
                // Note: We're directly writing to the texturehandle array we allocated
                VREF(texture_set, texturehandle[i]) = tex_handle;

                // Store dimensions (all pages should be same size)
                if (i == 0) {
                    *width = w;
                    *height = h;
                    first_handle = tex_handle;
                }

                ffnx_info("Loaded Japanese font page %d: %s (%dx%d)\n",
                          i + 1, filename, w, h);
            }
            else {
                ffnx_error("FAILED to load Japanese font page %d: %s\n",
                           i + 1, filename);
                all_loaded = false;

                // [CRITICAL DECISION] Fail-fast or continue?
                // Option A: Abort completely
                // return 0;

                // Option B: Continue and hope the page isn't needed
                // (Current behavior - risky but allows partial functionality)
            }
        }

        if (!all_loaded) {
            ffnx_warning("Not all Japanese font pages loaded. Text may appear corrupted.\n");
        } else {
            ffnx_info("Successfully loaded all 6 Japanese font pages.\n");
        }

        // Return the first page's handle (base page with Hiragana/Katakana)
        return first_handle;
    }

    // ... existing standard texture loading logic ...

    return 0;  // Not found
}
```

**Error Handling Improvement:**

Add a validation function:

```cpp
// src/saveload.cpp (helper function)

bool validate_font_texture_set(struct texture_set* tex_set) {
    if (!tex_set || !VREF(tex_set, texturehandle)) {
        ffnx_error("Texture set validation failed: NULL pointer\n");
        return false;
    }

    uint32_t allocated = VREF(tex_set, ogl.gl_set->textures);
    if (allocated < 6) {
        ffnx_error("Texture set validation failed: only %d slots allocated (need 6)\n",
                   allocated);
        return false;
    }

    // Check if all handles are valid
    for (int i = 0; i < 6; i++) {
        uint32_t handle = VREF(tex_set, texturehandle[i]);
        if (handle == 0) {
            ffnx_warning("Texture slot %d is empty (handle=0)\n", i);
        }
    }

    return true;
}

// Call after loading:
if (font_language == "ja") {
    if (!validate_font_texture_set(texture_set)) {
        ffnx_error("Font texture set validation failed!\n");
    }
}
```

---

## 7.5 File Redirection for Japanese Variants (src/redirect.cpp)

**Objective:** Handle the `jfleve.lgp` typo and other Japanese file naming quirks.

**Location: attempt_redirection function**

```cpp
// src/redirect.cpp

int attempt_redirection(const char* input_path, char* output_path) {
    // ... existing redirection logic (mod paths, 7th Heaven VFS, etc.) ...

    // [NEW] Japanese file name corrections
    // This should be checked BEFORE the final "file not found" return

    if (font_language == "ja" || is_using_japanese_exe) {
        // Handle the "jfleve" typo (missing 'l' in flevel)
        if (strstr(input_path, "flevel.lgp") || strstr(input_path, "FLEVEL.LGP")) {
            std::string ja_variant = input_path;
            size_t pos;

            // Try lowercase variant
            pos = ja_variant.find("flevel.lgp");
            if (pos != std::string::npos) {
                ja_variant.replace(pos, 10, "jfleve.lgp");
            } else {
                // Try uppercase variant
                pos = ja_variant.find("FLEVEL.LGP");
                if (pos != std::string::npos) {
                    ja_variant.replace(pos, 10, "JFLEVE.LGP");
                }
            }

            if (fileExists(ja_variant.c_str())) {
                strcpy(output_path, ja_variant.c_str());
                ffnx_info("Redirected field archive: %s → %s\n",
                          input_path, output_path);
                return 0;  // Success
            }
        }

        // Handle menu archive variants
        if (strstr(input_path, "menu_us.lgp") || strstr(input_path, "MENU_US.LGP")) {
            std::string ja_variant = input_path;
            size_t pos;

            pos = ja_variant.find("menu_us.lgp");
            if (pos != std::string::npos) {
                ja_variant.replace(pos, 11, "menu_ja.lgp");
            } else {
                pos = ja_variant.find("MENU_US.LGP");
                if (pos != std::string::npos) {
                    ja_variant.replace(pos, 11, "MENU_JA.LGP");
                }
            }

            if (fileExists(ja_variant.c_str())) {
                strcpy(output_path, ja_variant.c_str());
                ffnx_info("Redirected menu archive: %s → %s\n",
                          input_path, output_path);
                return 0;
            }
        }

        // Handle battle archive variants
        if (strstr(input_path, "battle.lgp") || strstr(input_path, "BATTLE.LGP")) {
            // Only redirect if NOT already "battle_ja"
            if (!strstr(input_path, "battle_ja") && !strstr(input_path, "BATTLE_JA")) {
                std::string ja_variant = input_path;
                size_t pos;

                pos = ja_variant.find("battle.lgp");
                if (pos != std::string::npos) {
                    ja_variant.replace(pos, 10, "battle_ja.lgp");
                } else {
                    pos = ja_variant.find("BATTLE.LGP");
                    if (pos != std::string::npos) {
                        ja_variant.replace(pos, 10, "BATTLE_JA.LGP");
                    }
                }

                if (fileExists(ja_variant.c_str())) {
                    strcpy(output_path, ja_variant.c_str());
                    ffnx_info("Redirected battle archive: %s → %s\n",
                              input_path, output_path);
                    return 0;
                }
            }
        }
    }

    // ... existing final fallback logic ...
    return -1;  // File not found
}
```

**Complete Japanese File Mapping Table:**

For reference, here's the complete mapping:

```cpp
// Documentation comment in redirect.cpp

/*
 * Japanese File Name Mapping
 *
 * English          →  Japanese           Notes
 * ================================================================
 * flevel.lgp       →  jfleve.lgp        TYPO! Missing 'l'
 * menu_us.lgp      →  menu_ja.lgp       Standard _ja suffix
 * battle.lgp       →  battle_ja.lgp     Standard _ja suffix
 * data/            →  data/lang-ja/     Path handled by registry
 * movies/          →  lang-ja/movies/   Path handled by registry
 */
```

---

## 7.6 Character Width Table Patch (src/ff7/font.cpp, src/ff7/font.h)

**Objective:** Fix the "Squashed Kanji" problem by overwriting the width table in RAM.

**Create New File: src/ff7/font.h**

```cpp
// src/ff7/font.h
#pragma once

#include "../common.h"

/**
 * Patches the in-memory character width table for Japanese mode.
 *
 * This function overwrites the width table (originally from KERNEL.BIN)
 * to use fixed 16px widths for all characters, preventing Kanji from
 * being squashed into narrow English character widths.
 *
 * MUST be called during ff7_init_hooks, AFTER ff7_data() has run.
 */
void PatchFontWidthsForJapanese();
```

**Create New File: src/ff7/font.cpp**

```cpp
// src/ff7/font.cpp

#include "font.h"
#include "../globals.h"
#include "../log.h"
#include "../ff7_data.h"
#include <windows.h>

void PatchFontWidthsForJapanese()
{
    // Only patch if Japanese mode is enabled
    if (font_language != "ja") {
        if (trace_all || trace_fonts) {
            ffnx_trace("Font width patching skipped (not in Japanese mode).\n");
        }
        return;
    }

    ffnx_info("Attempting to patch character width table for Japanese...\n");

    // Get pointer to width table (version-agnostic)
    // This pointer is set by FFNx during ff7_data() initialization
    char* font_width_table = common_externals.font_info;

    if (!font_width_table) {
        ffnx_error("CRITICAL: font_info pointer is NULL! Cannot patch widths.\n");
        ffnx_error("This usually means ff7_data() hasn't run yet, or the game version is unsupported.\n");
        return;
    }

    // Log the memory address (for debugging)
    ffnx_info("Width table located at: 0x%p\n", (void*)font_width_table);

    // Make the memory region writable
    DWORD oldProtect;
    if (!VirtualProtect(font_width_table, 256, PAGE_READWRITE, &oldProtect)) {
        DWORD error = GetLastError();
        ffnx_error("VirtualProtect failed! Error code: %d\n", error);
        ffnx_error("Cannot modify width table. Text will be squashed.\n");
        return;
    }

    // Overwrite ALL widths with fixed 16px
    for (int i = 0; i < 256; i++) {
        // Characters 0x00-0x1F are control codes (not rendered)
        // but we set them anyway for consistency
        font_width_table[i] = 0x10;  // 16 pixels (0x10 in hex)
    }

    // Optional: Set special widths for specific characters
    // (Uncomment if you want narrower spaces, for example)
    /*
    font_width_table[0x20] = 0x08;  // Space = 8px (half width)
    font_width_table[0x00] = 0x00;  // NULL terminator = 0px
    */

    // Restore original memory protection
    VirtualProtect(font_width_table, 256, oldProtect, &oldProtect);

    ffnx_info("Successfully patched character width table.\n");
    ffnx_info("All characters now use 16px width for Japanese rendering.\n");
}
```

**Integration: Modify src/ff7_opengl.cpp**

```cpp
// src/ff7_opengl.cpp

#include "ff7/font.h"  // [NEW] Add this include

void ff7_init_hooks(struct game_obj *_game_object)
{
    // ... existing code ...

    // Initialize FF7 data structures
    ff7_data(game_object);

    // [NEW] Apply Japanese font patches
    // MUST be called AFTER ff7_data() because it relies on common_externals.font_info
    PatchFontWidthsForJapanese();

    // ... rest of initialization ...
}
```

**Testing the Width Patch:**

Add a diagnostic function (optional, for debugging):

```cpp
// src/ff7/font.cpp

void DumpWidthTable() {
    if (font_language != "ja") return;

    char* table = common_externals.font_info;
    if (!table) return;

    ffnx_info("=== Character Width Table Dump ===\n");
    for (int i = 0; i < 256; i += 16) {
        char line[256];
        int pos = 0;
        pos += sprintf(line + pos, "0x%02X: ", i);
        for (int j = 0; j < 16; j++) {
            pos += sprintf(line + pos, "%02X ", (unsigned char)table[i + j]);
        }
        ffnx_info("%s\n", line);
    }
    ffnx_info("===================================\n");
}

// Call in PatchFontWidthsForJapanese() after patching:
// DumpWidthTable();
```

---
