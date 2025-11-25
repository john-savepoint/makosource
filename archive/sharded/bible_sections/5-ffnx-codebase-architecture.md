# 5. FFNX CODEBASE ARCHITECTURE

## 5.1 Repository Structure

```
FFNx/
├── src/                      # C++ source code
│   ├── cfg.cpp               # Configuration parsing (TOML)
│   ├── cfg.h                 # Configuration declarations
│   ├── common.cpp            # Core driver logic, hooks, texture loading
│   ├── common.h              # Common headers
│   ├── globals.h             # Global variables
│   ├── saveload.cpp          # Texture loading pipeline
│   ├── redirect.cpp          # File path redirection
│   ├── hext.cpp              # Hext patch system
│   ├── ff7/                  # FF7-specific code
│   │   ├── menu.cpp          # Menu rendering
│   │   ├── font.cpp          # Font handling (we'll create this)
│   │   ├── font.h            # Font declarations (we'll create this)
│   │   └── ff7_data.h        # Memory addresses, structures
│   └── gl/                   # OpenGL/BGFX rendering
│       ├── gl.cpp            # Main rendering logic
│       └── texture.cpp       # Texture management
├── misc/
│   └── hext/                 # Hext patch files
│       └── ff7/
│           ├── en/           # English version patches
│           │   └── FFNx.JAPANESE_FONT.txt  # We'll create this
│           └── jp/           # Japanese version patches
├── FFNx.toml                 # User configuration file
└── ...
```

## 5.2 Key Subsystems

**Configuration System (cfg.cpp / cfg.h):**
- Parses `FFNx.toml` using TOML11 library
- Exposes settings as global `extern` variables
- Read once at startup, immutable during runtime
- **Our additions:** `font_language`, `font_enable_furigana`, `font_path_override`

**Common Driver Logic (common.cpp):**
- **`DllMain`:** Entry point, initializes FFNx, detects executable
- **`common_init`:** Sets up hooks, loads configuration
- **`common_load_texture`:** Allocates texture memory (**critical intervention point**)
- **`common_palette_changed`:** Handles palette switching requests
- **`dotemuReg*` functions:** Virtual registry for game compatibility

**Texture Pipeline (saveload.cpp):**
- **`load_external_texture`:** Checks for PNG overrides before loading TEX
- **`load_texture_helper`:** PNG decoding, GPU upload
- **`load_texture`:** Main entry point, orchestrates loading

**File Redirection (redirect.cpp):**
- **`attempt_redirection`:** Maps virtual paths to physical paths
- Handles 7th Heaven VFS, mod paths, language paths
- **Our addition:** `flevel.lgp` → `jfleve.lgp` mapping for Japanese

**Rendering Backend (gl/gl.cpp):**
- **`gl_draw_indexed_primitive`:** Main draw call function
- **`gl_bind_texture_set`:** Texture binding logic (**critical hook point**)
- **`gl_set_texture`:** Sets active texture on GPU
- Interfaces with BGFX for cross-platform rendering

## 5.3 Critical Memory Addresses & Structures

**Version-Specific Addresses (US 1.02):**

| Symbol | Address | Type | Description |
|--------|---------|------|-------------|
| `font_info` | `0x99DDA8` | `char*` | Pointer to character width table (256 bytes) |
| `draw_graphics_object` | `0x66E272` | Function | Main text rendering function (approximation) |
| Character processing loop | ~`0x66E2A0` | Code | Loop that reads text bytes (target for Hext) |

**⚠️ CRITICAL WARNING:**
- These addresses are **ONLY VALID** for FF7 US 1.02 executable
- Steam version has **DIFFERENT** addresses (ASLR, different build)
- `ff7_ja.exe` has **COMPLETELY DIFFERENT** addresses
- **ALWAYS use `common_externals` pointers** instead of hardcoded addresses
- FFNx already resolves version-specific addresses at runtime

**FFNx Common Externals Structure:**
```c
struct common_externals {
    // ... many fields ...
    char *font_info;              // Points to width table (version-agnostic)
    void (*create_texture_set)(); // Texture set allocator
    // ... more fields ...
};

extern struct common_externals common_externals;  // Global instance
```

**Accessing Memory Safely:**
```c
// ✅ CORRECT: Use FFNx's version-agnostic pointer
char* width_table = common_externals.font_info;
if (width_table) {
    width_table[0x41] = 0x10;  // Set 'A' width to 16px
}

// ❌ WRONG: Hardcoded address (will crash on different versions)
char* width_table = (char*)0x99DDA8;  // NEVER DO THIS
```

---
