# Multi-Language Menu Text Injection - Proof of Concept

**Created:** 2026-01-23 14:35 JST (Friday)
**Session ID:** 2844b4cc-5276-48d1-8630-807bff87b3dc
**Author:** John Zealand-Doyle
**Status:** Proof-of-Concept Design (Not Implemented)

---

## Executive Summary

This document presents a detailed proof-of-concept for implementing runtime German (and other language) text injection into FF7's menu system using FFNx's existing text rendering hooks. The approach leverages FFNx's proven multi-language battle text system and extends it to menu contexts.

**Key Insight:** FFNx already implements German/French/Spanish translation for battle enemy names using direct RAM injection. This same technique can be adapted for menu text with minimal modifications.

---

## Architecture Overview

### Current System (English Only)

```
Game Memory → Static English Text
    ↓
FFNx Hook: field_submit_draw_text_640x480_6E706D_jp()
    ↓
Character-by-character rendering
    ↓
GPU Display
```

### Proposed System (Multi-Language)

```
Game Memory → Static English Text
    ↓
NEW: Translation Lookup Layer
    ├─ Check translation database
    ├─ Hash English string
    ├─ Lookup German translation
    └─ Return translated buffer OR original
    ↓
FFNx Hook: field_submit_draw_text_640x480_6E706D_jp()
    ↓
Character-by-character rendering (unchanged)
    ↓
GPU Display
```

---

## Implementation Strategy

### Phase 1: Translation Database System

#### 1.1 Translation File Format

**File**: `data/lang-de/menu_text_de.dat`

```
Binary Structure (based on scene_text.cpp pattern):

Header:
- Magic: "MENU" (4 bytes)
- Version: 1 (4 bytes, little-endian uint32_t)
- Language Code: "de" (2 bytes)
- Reserved: 0x00 (2 bytes)
- Entry Count: N (4 bytes, little-endian uint32_t)

Per-Entry Structure:
- English Hash: (4 bytes, xxHash32 of English string)
- German Offset: (4 bytes, offset to German string in data section)
- German Length: (2 bytes, string length)
- Reserved: 0x00 (2 bytes)

Data Section:
- Null-terminated German strings (FF-terminated for FF7)
```

**Example Entry:**
```
English: "New Game"
Hash: 0x4A3B2C1D (xxHash32("New Game"))
German: "Neues Spiel"
Offset: 0x00000100 (256 bytes into data section)
Length: 12 bytes (including terminator)

Binary Representation:
1D 2C 3B 4A | 00 01 00 00 | 0C 00 | 00 00
│           │             │       │
│           │             │       └─ Reserved
│           │             └───────── Length
│           └──────────────────────── Offset
└──────────────────────────────────── Hash
```

#### 1.2 Translation Database Loading

**File**: `src/ff7/menu_text.h`

```cpp
#ifndef MENU_TEXT_H
#define MENU_TEXT_H

#include <stdint.h>
#include <unordered_map>
#include <string>
#include <vector>

namespace ff7 {
namespace menu_text {

// Translation entry structure
struct TranslationEntry {
    uint32_t hash;           // xxHash32 of English string
    std::vector<uint8_t> text;  // German text (FF-terminated)
};

// Translation database
class TranslationDatabase {
public:
    TranslationDatabase();
    ~TranslationDatabase();

    // Load translation file
    bool load(const char* filepath);

    // Lookup translation by English string
    const uint8_t* translate(const uint8_t* english_text, size_t& out_length);

    // Check if database is loaded
    bool is_loaded() const { return loaded_; }

private:
    std::unordered_map<uint32_t, TranslationEntry> translations_;
    bool loaded_;

    // Hash function (xxHash32)
    uint32_t hash_string(const uint8_t* str, size_t len);
};

// Global translation database instance
extern TranslationDatabase g_translation_db;

} // namespace menu_text
} // namespace ff7

#endif // MENU_TEXT_H
```

**File**: `src/ff7/menu_text.cpp`

```cpp
#include "menu_text.h"
#include "../log.h"
#include "../common.h"
#include <fstream>
#include <cstring>

// Include xxHash (already in FFNx dependencies)
extern "C" {
#include <xxhash.h>
}

namespace ff7 {
namespace menu_text {

TranslationDatabase g_translation_db;

TranslationDatabase::TranslationDatabase() : loaded_(false) {}

TranslationDatabase::~TranslationDatabase() {
    translations_.clear();
}

bool TranslationDatabase::load(const char* filepath) {
    ffnx_info("Loading menu translation database: %s\n", filepath);

    std::ifstream file(filepath, std::ios::binary);
    if (!file) {
        ffnx_warning("Translation file not found: %s\n", filepath);
        return false;
    }

    // Read header
    char magic[4];
    file.read(magic, 4);
    if (memcmp(magic, "MENU", 4) != 0) {
        ffnx_error("Invalid translation file magic: %s\n", filepath);
        return false;
    }

    uint32_t version;
    file.read(reinterpret_cast<char*>(&version), 4);
    if (version != 1) {
        ffnx_error("Unsupported translation file version: %u\n", version);
        return false;
    }

    // Read language code
    char lang_code[2];
    file.read(lang_code, 2);
    ffnx_info("Language: %.2s\n", lang_code);

    // Skip reserved bytes
    file.seekg(2, std::ios::cur);

    // Read entry count
    uint32_t entry_count;
    file.read(reinterpret_cast<char*>(&entry_count), 4);
    ffnx_info("Translation entries: %u\n", entry_count);

    // Read entries
    for (uint32_t i = 0; i < entry_count; i++) {
        uint32_t hash, offset;
        uint16_t length;

        file.read(reinterpret_cast<char*>(&hash), 4);
        file.read(reinterpret_cast<char*>(&offset), 4);
        file.read(reinterpret_cast<char*>(&length), 2);
        file.seekg(2, std::ios::cur);  // Skip reserved

        // Store current position
        std::streampos current_pos = file.tellg();

        // Seek to data section
        file.seekg(16 + (entry_count * 12) + offset, std::ios::beg);

        // Read German text
        TranslationEntry entry;
        entry.hash = hash;
        entry.text.resize(length);
        file.read(reinterpret_cast<char*>(entry.text.data()), length);

        // Verify FF terminator
        if (entry.text.back() != 0xFF) {
            ffnx_warning("Entry %u missing FF terminator, adding...\n", i);
            entry.text.push_back(0xFF);
        }

        // Store in map
        translations_[hash] = std::move(entry);

        // Return to entry position
        file.seekg(current_pos, std::ios::beg);
    }

    loaded_ = true;
    ffnx_info("Translation database loaded successfully: %u entries\n", entry_count);
    return true;
}

uint32_t TranslationDatabase::hash_string(const uint8_t* str, size_t len) {
    // Use xxHash32 (fast, collision-resistant)
    return XXH32(str, len, 0);  // Seed = 0
}

const uint8_t* TranslationDatabase::translate(const uint8_t* english_text, size_t& out_length) {
    if (!loaded_) {
        return nullptr;  // Database not loaded
    }

    // Calculate string length (up to 0xFF terminator)
    size_t len = 0;
    while (english_text[len] != 0xFF && len < 256) {
        len++;
    }

    if (len == 0 || len >= 256) {
        return nullptr;  // Invalid string
    }

    // Hash the English string
    uint32_t hash = hash_string(english_text, len);

    // Lookup translation
    auto it = translations_.find(hash);
    if (it == translations_.end()) {
        return nullptr;  // No translation found
    }

    // Return German text
    out_length = it->second.text.size();
    return it->second.text.data();
}

} // namespace menu_text
} // namespace ff7
```

---

## Phase 2: Hook Integration

### 2.1 Text Rendering Hook Wrapper

**File**: `src/ff7/menu_text_hooks.cpp`

```cpp
#include "menu_text.h"
#include "japanese_text.h"  // For original functions
#include "../log.h"
#include <cstring>

namespace ff7 {
namespace menu_text {

// Thread-local translation buffer (avoid allocations per call)
static thread_local uint8_t translation_buffer[256];

/**
 * Wrapper for field_submit_draw_text_640x480_6E706D_jp
 *
 * Intercepts text rendering, checks for German translation,
 * and replaces buffer_text pointer if translation exists.
 */
__int16 __cdecl field_submit_draw_text_with_translation(
    __int16 x,
    __int16 y,
    __int16 right,
    byte *buffer_text,
    float z)
{
    // Try German translation
    size_t german_length = 0;
    const uint8_t* german_text = g_translation_db.translate(
        buffer_text,
        german_length
    );

    if (german_text && german_length > 0) {
        // Translation found - use German text
        if (trace_all || trace_loaders) {
            ffnx_trace("Menu text translated: %u bytes\n", german_length);
        }

        // Safety: Copy to thread-local buffer
        memcpy(translation_buffer, german_text, german_length);

        // Call original function with German text
        return field_submit_draw_text_640x480_6E706D_jp(
            x, y, right,
            translation_buffer,  // German text
            z
        );
    }

    // No translation - use original English text
    return field_submit_draw_text_640x480_6E706D_jp(
        x, y, right,
        buffer_text,  // Original English
        z
    );
}

} // namespace menu_text
} // namespace ff7
```

### 2.2 Hook Installation

**File**: `src/ff7_opengl.cpp` (modify existing hook installation)

```cpp
#include "ff7/menu_text.h"
#include "ff7/menu_text_hooks.h"

// Inside ff7_init_hooks() function (around line 390)

void ff7_init_hooks(struct game_obj *game_object)
{
    // ... existing code ...

    if (ff7_japanese_edition)
    {
        // Japanese mode: use PR #737 hooks
        replace_function(
            ff7_externals.field_submit_draw_text_640x480_6E706D,
            field_submit_draw_text_640x480_6E706D_jp
        );

        // ... other Japanese hooks ...
    }
    else
    {
        // NEW: Multi-language mode for English executable

        // Load German translation database
        bool german_loaded = ff7::menu_text::g_translation_db.load(
            "data/lang-de/menu_text_de.dat"
        );

        if (german_loaded) {
            ffnx_info("German translations enabled\n");

            // Install translation wrapper hook
            replace_function(
                ff7_externals.field_submit_draw_text_640x480_6E706D,
                ff7::menu_text::field_submit_draw_text_with_translation
            );
        }
        else {
            ffnx_info("German translations not available, using English\n");
            // No hook - use original English rendering
        }
    }

    // ... rest of initialization ...
}
```

---

## Phase 3: Translation File Generation

### 3.1 Translation Extraction Tool

**File**: `tools/extract_menu_text.py`

```python
#!/usr/bin/env python3
"""
Extract menu text strings from FF7 English executable.
"""

import struct
import hashlib

# String locations from Hext patch analysis
MENU_STRINGS = [
    {"addr": 0x005183D0, "len": 4, "text": "Yes"},
    {"addr": 0x005183D4, "len": 4, "text": "No"},
    {"addr": 0x005188A8, "len": 48, "text": "Window color"},
    {"addr": 0x005188D8, "len": 48, "text": "Sound"},
    {"addr": 0x00518908, "len": 48, "text": "Controller"},
    # ... 554 more entries from japanese_menu.txt
]

def xxhash32(data):
    """Calculate xxHash32 (simplified - use library in production)"""
    # Use hashlib for demonstration
    return struct.unpack('<I', hashlib.md5(data).digest()[:4])[0]

def extract_strings(exe_path):
    """Extract menu strings from FF7 executable"""
    with open(exe_path, 'rb') as f:
        strings = []
        for entry in MENU_STRINGS:
            # Seek to string location
            f.seek(entry['addr'])

            # Read bytes
            data = f.read(entry['len'])

            # Find FF terminator
            try:
                end = data.index(0xFF)
                text_bytes = data[:end]
            except ValueError:
                text_bytes = data.rstrip(b'\x00')

            # Decode (ASCII for English)
            try:
                text = text_bytes.decode('ascii')
            except UnicodeDecodeError:
                text = entry['text']  # Use known text

            # Calculate hash
            hash_val = xxhash32(text_bytes)

            strings.append({
                'hash': hash_val,
                'english': text,
                'bytes': text_bytes
            })

        return strings

def main():
    strings = extract_strings('ff7_en.exe')

    # Write JSON for translation
    import json
    with open('menu_strings_en.json', 'w', encoding='utf-8') as f:
        json.dump(strings, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(strings)} menu strings")

if __name__ == '__main__':
    main()
```

### 3.2 Translation Database Builder

**File**: `tools/build_translation_db.py`

```python
#!/usr/bin/env python3
"""
Build binary translation database from JSON translations.
"""

import struct
import json

def build_database(english_json, german_json, output_file):
    """Build .dat file from English/German JSON files"""

    # Load English strings
    with open(english_json, 'r', encoding='utf-8') as f:
        english = json.load(f)

    # Load German translations
    with open(german_json, 'r', encoding='utf-8') as f:
        german = json.load(f)

    # Create translation map
    translations = {}
    for en_entry in english:
        en_text = en_entry['english']

        # Find German translation
        de_entry = next((g for g in german if g['english'] == en_text), None)
        if de_entry:
            translations[en_entry['hash']] = de_entry['german']

    print(f"Building database with {len(translations)} translations")

    # Build binary file
    with open(output_file, 'wb') as f:
        # Header
        f.write(b'MENU')                          # Magic
        f.write(struct.pack('<I', 1))             # Version
        f.write(b'de')                            # Language code
        f.write(struct.pack('<H', 0))             # Reserved
        f.write(struct.pack('<I', len(translations)))  # Entry count

        # Calculate data section offset
        data_offset = 16 + (len(translations) * 12)

        # Write entries
        current_offset = 0
        data_section = bytearray()

        for hash_val, german_text in translations.items():
            # Encode German text (Latin-1 for umlauts)
            german_bytes = german_text.encode('latin-1')
            german_bytes += b'\xFF'  # FF7 terminator

            # Write entry header
            f.write(struct.pack('<I', hash_val))         # Hash
            f.write(struct.pack('<I', current_offset))   # Offset
            f.write(struct.pack('<H', len(german_bytes))) # Length
            f.write(struct.pack('<H', 0))                # Reserved

            # Append to data section
            data_section += german_bytes
            current_offset += len(german_bytes)

        # Write data section
        f.write(data_section)

    print(f"Database written: {output_file}")
    print(f"Total size: {16 + (len(translations) * 12) + len(data_section)} bytes")

def main():
    build_database(
        'menu_strings_en.json',
        'menu_strings_de.json',
        '../data/lang-de/menu_text_de.dat'
    )

if __name__ == '__main__':
    main()
```

---

## Alternative Approach: Direct RAM Injection

### 4.1 RAM Address Mapping

Based on FFNx's `scene_text.cpp` proven approach for enemy names:

**Find menu text RAM addresses** (requires runtime debugging):

```cpp
// Hypothetical menu text RAM addresses (needs verification)
constexpr uint32_t MENU_OPTION_1_ADDR = 0x9AXXXX;  // "New Game"
constexpr uint32_t MENU_OPTION_2_ADDR = 0x9AXXXX;  // "Continue"
constexpr uint32_t MENU_OPTION_3_ADDR = 0x9AXXXX;  // "Options"
// ... etc.
```

### 4.2 Direct Injection Implementation

```cpp
void inject_german_menu_text() {
    // Direct RAM write (like scene_text.cpp does for enemy names)

    const char* new_game_de = "Neues Spiel";
    uint8_t* dest = (uint8_t*)MENU_OPTION_1_ADDR;

    size_t len = strlen(new_game_de);

    // Copy German text
    memcpy(dest, new_game_de, len);

    // FF7 requires 0xFF terminator (not 0x00!)
    for (size_t i = len; i < 32; i++) {
        dest[i] = 0xFF;
    }

    // CRITICAL: Do NOT write beyond byte 32
    // Writing to bytes 32+ overwrites Level field and crashes
}
```

**Advantages:**
- Proven to work (already used for enemy names)
- No hook modifications needed
- Direct memory writes, very fast

**Disadvantages:**
- Requires finding RAM addresses for every menu string
- Less flexible than hook-based approach
- Hard to maintain (addresses may change)

---

## Performance Analysis

### 5.1 Hook-Based Approach

**Per-Frame Overhead:**
```
Translation lookups: 5-20 per frame (menu context)
Hash calculation: ~50 CPU cycles per string
Map lookup: O(1) average, ~100 CPU cycles
Total overhead: ~3,000 CPU cycles per frame

Impact: <0.001ms on modern CPUs (negligible)
```

### 5.2 Memory Footprint

**Translation Database:**
```
Header: 16 bytes
Entries: 559 × 12 bytes = 6,708 bytes
Data: ~15,000 bytes (average 27 bytes per German string)
Total: ~22 KB in RAM

Impact: Negligible (FF7 uses 100+ MB)
```

---

## Testing Strategy

### 6.1 Unit Testing

**Test Cases:**

1. **Translation Lookup**
   - English string exists → German translation returned
   - English string missing → nullptr returned
   - Empty string → nullptr returned
   - String >256 bytes → nullptr returned

2. **Hash Collisions**
   - Verify no collisions in 559 menu strings
   - Test similar strings ("New" vs "New Game")

3. **Buffer Safety**
   - German text fits in allocated space
   - 0xFF terminator present
   - No buffer overruns

### 6.2 Integration Testing

**Test Scenarios:**

1. **Menu Navigation**
   - Main menu displays German text
   - Options menu displays German text
   - Save/Load dialogs display German text

2. **String Length Handling**
   - Short strings (3-4 chars)
   - Medium strings (10-15 chars)
   - Long strings (30+ chars)

3. **Fallback Behavior**
   - German DB not loaded → English text
   - Translation missing → English text
   - Corrupted DB file → English text (safe fallback)

---

## File Structure Summary

```
FFNx/
├── src/
│   └── ff7/
│       ├── menu_text.h           [NEW] Translation database API
│       ├── menu_text.cpp         [NEW] Translation database implementation
│       ├── menu_text_hooks.cpp   [NEW] Hook wrapper functions
│       └── ff7_opengl.cpp        [MODIFY] Add hook installation (5 lines)
├── data/
│   └── lang-de/
│       └── menu_text_de.dat      [NEW] Binary translation database
└── tools/
    ├── extract_menu_text.py      [NEW] String extractor
    └── build_translation_db.py   [NEW] Database builder
```

---

## Implementation Roadmap

### Phase 1: Infrastructure (2-4 hours)
- [ ] Create `menu_text.h` and `menu_text.cpp`
- [ ] Implement translation database loader
- [ ] Add unit tests for hash/lookup functions
- [ ] Test with sample 10-entry database

### Phase 2: Hook Integration (2-3 hours)
- [ ] Create `menu_text_hooks.cpp`
- [ ] Modify `ff7_opengl.cpp` hook installation
- [ ] Test hook interception (log calls)
- [ ] Verify fallback to English works

### Phase 3: Translation Database (4-6 hours)
- [ ] Write `extract_menu_text.py`
- [ ] Extract all 559 menu strings from hext file
- [ ] Translate strings to German (manual or MT)
- [ ] Write `build_translation_db.py`
- [ ] Generate `menu_text_de.dat`

### Phase 4: Testing (3-4 hours)
- [ ] Test main menu
- [ ] Test options menu
- [ ] Test battle menu
- [ ] Test save/load dialogs
- [ ] Verify no crashes or corruption

### Phase 5: Optimization (1-2 hours)
- [ ] Profile translation lookup performance
- [ ] Optimize hash function if needed
- [ ] Add caching for frequently-used strings

**Total Estimated Time: 12-19 hours**

---

## Risk Analysis

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Buffer overflow in German text | Medium | High | Strict bounds checking, 32-byte limit |
| Hash collisions | Low | Medium | Use xxHash32, verify no collisions |
| Performance degradation | Low | Low | Profile, optimize if >0.1ms overhead |
| Incompatibility with Japanese mode | Low | Medium | Keep separate code paths |
| Memory corruption | Low | High | Use safe memcpy, validate lengths |

### Integration Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Conflicts with other FFNx features | Medium | Medium | Test with all features enabled |
| FFNx version updates breaking hooks | Medium | Medium | Document exact hook locations |
| Corrupted translation database | Low | Low | Validate DB on load, fallback to English |

---

## Future Extensions

### Multi-Language Support

**French/Spanish:**
- Reuse same infrastructure
- Add `menu_text_fr.dat` and `menu_text_es.dat`
- Modify config to select language

**Chinese/Japanese:**
- Extend to support FA-FE multi-page encoding
- Generate additional font textures
- Update parser for extended page markers

### Runtime Language Switching

```cpp
void switch_language(const char* lang_code) {
    g_translation_db.load(
        std::string("data/lang-") + lang_code + "/menu_text_" + lang_code + ".dat"
    );
}
```

### Mod Support

- Allow mods to provide translation files
- Merge multiple translation databases
- Priority system for conflicting translations

---

## Conclusion

This proof-of-concept demonstrates a **practical, low-risk approach** to implementing multi-language menu text in FF7 using FFNx's existing infrastructure. The design:

1. ✅ **Reuses proven patterns** from FFNx's battle text translation system
2. ✅ **Minimal code changes** (<500 lines of new code)
3. ✅ **No executable modifications** (pure FFNx plugin)
4. ✅ **Safe fallbacks** (English if translation missing)
5. ✅ **Performance-conscious** (<0.001ms overhead)
6. ✅ **Extensible** (easy to add more languages)

The next step is to **implement Phase 1** (infrastructure) and validate the translation database loading mechanism with a small test dataset.

---

**Implementation Status:** Design Complete, Ready for Development
**Estimated Development Time:** 12-19 hours
**Risk Level:** Low (proven patterns, safe fallbacks)
**Dependencies:** FFNx PR #737 codebase, xxHash library (already present)

---

**End of Proof-of-Concept**
