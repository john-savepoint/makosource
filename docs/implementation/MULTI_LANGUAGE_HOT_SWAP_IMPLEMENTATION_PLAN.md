# Multi-Language Hot-Swap Implementation Plan

**Created:** 2025-12-23 15:20 JST (Monday)
**Last Modified:** 2025-12-23 15:20 JST (Monday)
**Version:** 1.0.0
**Author:** John Zealand-Doyle
**Session-ID:** 00f8d68d-0a0e-4b66-831e-20de2642c552

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Context](#project-context)
3. [Problems Encountered](#problems-encountered)
4. [Technical Analysis](#technical-analysis)
5. [Proposed Architecture](#proposed-architecture)
6. [Implementation Phases](#implementation-phases)
7. [File Format Specifications](#file-format-specifications)
8. [FFNx Hook Points](#ffnx-hook-points)
9. [Mod Community Integration](#mod-community-integration)
10. [Risk Assessment](#risk-assessment)
11. [Open Questions](#open-questions)
12. [References & Tools](#references--tools)

---

## Executive Summary

This document outlines the implementation plan for a **language learner's edition** of Final Fantasy VII that supports **instant hot-swapping between 5 languages** (English, Japanese, German, French, Spanish) at any point during gameplay.

### Core Goals

1. **Instant language switching** - Change language mid-dialogue, mid-battle, anywhere
2. **All 5 languages available simultaneously** - No restart required
3. **Mod community compatibility** - English mods work seamlessly
4. **Single executable** - Use US Steam executable for all languages

### Key Innovation

Rather than switching entire data files (which have incompatible structures), we implement a **runtime text injection system** where:
- Base game files use English structure (compatible with US executable)
- Language-specific text is loaded into memory at startup
- FFNx hooks text rendering and injects the correct language dynamically

---

## Project Context

### Target Audience

Language learners who want to:
- Play FF7 while learning Japanese/German/French/Spanish
- Instantly compare translations ("What did that enemy say?")
- Toggle between native language and target language freely
- See dual-language displays where possible

### Why Hot-Swap Matters

Unlike typical localization where users pick a language at install:
- Learners need to **compare** translations constantly
- A battle might prompt "What's 'Fire' in German?" → instant switch
- Field dialogue comparison: "How do they phrase this in Japanese?"
- This is the **core selling point** of the language learner edition

### Current State (as of 2025-12-23)

**Working:**
- `ff7_language` TOML setting (en/ja/de/fr/es)
- LGP file routing for field, menu, CD, world, minigames
- Kernel2.bin loading for all languages (menu text, spell names)
- Japanese naming screen patches guarded by language check
- HEXT patching path selection by language

**Not Working:**
- German battle encounters (wrong enemies/arenas loading)
- Hot-swap capability (requires game restart to change language)
- Scene.bin language routing (structural incompatibility)

---

## Problems Encountered

### Problem 1: Scene.bin Block Distribution Mismatch

**Discovery Date:** 2025-12-23

**Symptom:** German language setting loads wrong battle encounters - "battles from later in the game with weird characters"

**Root Cause Analysis:**

Scene.bin is a compressed archive divided into 8KB blocks. Each block contains multiple GZIP-compressed "scenes" (enemy formations). The number of scenes per block varies by language due to **text length affecting compression ratio**.

| Block | English | Japanese | German |
|-------|---------|----------|--------|
| 0     | 12      | 12       | **11** |
| 1     | 6       | 6        | **7**  |
| 2     | 7       | 7        | 7      |
| 3     | 8       | 8        | 8      |
| 4     | 6       | 6        | 6      |
| 5     | 6       | 6        | 6      |
| 6     | 8       | 8        | **7**  |
| 7     | 8       | 8        | **7**  |
| 8     | 12      | 12       | **13** |
| 9     | 8       | 8        | 8      |

**Why English/Japanese work identically:** Same block distribution (12,6,7,8,6,6,8,8,12,8)

**Why German fails:** Different distribution (11,7,7,8,6,6,7,7,13,8) - when the US executable calculates "Scene #11 is in Block 0", it's actually in Block 1 for German.

**Technical Details (from FF7 Architecture AI):**

> "German text is historically longer. When compressed, the resulting GZIP file is slightly larger. If the German files are larger, fewer fit into the fixed 0x2000 byte bucket before it overflows. The compiler must 'close' the block earlier (at 11 files) and start a new one."

### Problem 2: Scene.bin Contains Critical Localized Text

Scene.bin is not just battle logic - it contains:
- **Enemy Names** (32 bytes at offset 0x0000 per enemy)
- **Enemy Attack Names** (offsets 0x0880-0x0C60, 32 names × 32 bytes)

Using English scene.bin would give:
- ✅ Correct battle encounters
- ❌ English enemy names ("Guard Scorpion" instead of "Wachskorpion")
- ❌ English attack names ("Tail Laser" instead of "Schwanzlaser")

### Problem 3: No Simple File Swap Solution

Options considered and rejected:

| Approach | Why Rejected |
|----------|--------------|
| Swap scene.bin on language change | Game caches data, would need battle reload; different block structures |
| Create German scene.bin with English structure | May not compress small enough; complex rebuild process |
| Single scene.bin with all languages | 4-5x file size; completely different block structure |

---

## Technical Analysis

### FF7 Text Rendering Architecture

Based on FF7 documentation and FFNx codebase analysis:

#### Font System
- **Source:** `WINDOW.BIN` → `USFONT_A.TEX`, `USFONT_B.TEX`
- Font A: Standard alphabet, numbers, basic punctuation
- Font B: Extended characters (umlauts), controller icons, special glyphs
- Different regional versions have different font textures

#### Text Storage Locations

| Text Type | Source File | Hot-Swap Feasible? |
|-----------|-------------|-------------------|
| Field Dialogue | flevel.lgp (per-language variants) | Yes - load different LGP |
| Menu Text | kernel2.bin | Yes - text tables in memory |
| Spell/Item Names | kernel2.bin | Yes - text tables in memory |
| Enemy Names | scene.bin | **Requires injection** |
| Enemy Attack Names | scene.bin | **Requires injection** |
| Battle UI ("Miss", "Critical") | kernel2.bin | Yes - text tables in memory |

### Scene.bin Internal Structure

From Qhimm documentation (Fremen):

```
scene.bin structure:
├── Block 0 (0x2000 bytes)
│   ├── Header: Pointers to scenes (4 bytes each, multiply by 4 for offset)
│   ├── Scene 0 (GZIP compressed)
│   ├── Scene 1 (GZIP compressed)
│   └── ... (until 0xFFFFFFFF terminator or block full)
├── Block 1 (0x2000 bytes)
│   └── ...
└── Block N...

Each Scene contains:
├── Enemy Data (×3 enemies max)
│   ├── Name (32 bytes) ← LOCALIZED
│   ├── Stats, AI, etc.
│   └── Attack Names (32 × 32 bytes) ← LOCALIZED
├── Formation Data (×4 formations)
└── Camera Data
```

**Key Constraint:** Each block MUST be exactly 0x2000 bytes (8KB). Padding with 0xFF if needed.

### Battle ID to Scene Mapping

```
Battle ID / 4 = Scene File ID
Scene File ID → Block lookup → Offset within block
```

The block lookup is either:
- Hardcoded in executable (per-region)
- Read from kernel.bin lookup table at offset 0x0F1C of section 3

---

## Proposed Architecture

### Design Philosophy

**"English Structure, Multi-Language Content"**

1. Use English scene.bin as the base (correct block structure for US executable)
2. Load all language text into a runtime lookup table
3. Hook text rendering to inject correct language dynamically
4. Language changes instantly without reloading any files

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        FFNx Runtime                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────────────────────┐  │
│  │  ff7_language    │───▶│  Text Injection System            │  │
│  │  (TOML setting)  │    │                                    │  │
│  └──────────────────┘    │  ┌────────────────────────────┐   │  │
│                          │  │ enemy_text_table[256]      │   │  │
│  ┌──────────────────┐    │  │   ├── scene[0]             │   │  │
│  │  scene.bin       │    │  │   │   ├── name_en[32]      │   │  │
│  │  (English base)  │───▶│  │   │   ├── name_de[32]      │   │  │
│  └──────────────────┘    │  │   │   ├── name_fr[32]      │   │  │
│                          │  │   │   ├── name_es[32]      │   │  │
│  ┌──────────────────┐    │  │   │   ├── name_ja[32]      │   │  │
│  │  enemy_text/     │───▶│  │   │   └── attacks[32][5]   │   │  │
│  │  ├── de.dat      │    │  │   └── scene[1-255]...      │   │  │
│  │  ├── fr.dat      │    │  └────────────────────────────┘   │  │
│  │  ├── es.dat      │    │                                    │  │
│  │  └── ja.dat      │    │  Hook: render_enemy_name()         │  │
│  └──────────────────┘    │  Hook: render_attack_name()        │  │
│                          └──────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Startup:**
   - Load English scene.bin (battles work correctly)
   - Load enemy_text/*.dat files into `enemy_text_table`
   - Register text rendering hooks

2. **Battle Start:**
   - Game loads scene from English scene.bin (correct structure)
   - Enemy stats, AI, formations all work correctly

3. **Text Rendering:**
   - Game calls `render_enemy_name(scene_id, enemy_idx)`
   - FFNx hook intercepts
   - Looks up `enemy_text_table[scene_id].enemies[enemy_idx].name[ff7_language]`
   - Renders correct language text

4. **Language Change:**
   - User changes `ff7_language` (via menu or hotkey)
   - Next text render uses new language
   - **No file reloading required**

---

## Implementation Phases

### Phase 1: Foundation (Priority: Critical)

**Goal:** Get German battles working with English enemy names

**Tasks:**
1. Revert German scene.bin routing - use English scene.bin for all Western languages
2. Verify battles load correctly for EN/DE/FR/ES
3. Document which text appears in wrong language (enemy names, attacks)

**Acceptance Criteria:**
- All languages load correct battle encounters
- Battle menus show correct language (from kernel2.bin)
- Enemy names show English (acceptable for Phase 1)

### Phase 2: Text Extraction (Priority: High)

**Goal:** Extract all localized text from scene.bin files

**Tasks:**
1. Write Python script to parse scene.bin structure
2. Extract enemy names and attack names from all 5 language versions
3. Generate unified text database (JSON or binary format)
4. Validate extraction accuracy

**Deliverables:**
- `scripts/extract_scene_text.py`
- `data/enemy_text/extracted_text.json`
- Extraction validation report

### Phase 3: Text Injection System (Priority: High)

**Goal:** Runtime text injection in FFNx

**Tasks:**
1. Identify FFNx hook points for enemy name rendering
2. Identify FFNx hook points for attack name rendering
3. Implement `enemy_text_table` data structure
4. Implement text loading from external files
5. Implement rendering hooks
6. Test hot-swap functionality

**Deliverables:**
- `src/ff7/battle/text_injection.cpp`
- `src/ff7/battle/text_injection.h`
- Modified `battle.cpp` with hooks
- `data/lang-XX/battle/enemy_text.dat` files

### Phase 4: Mod Integration (Priority: Medium)

**Goal:** Ensure English mods work seamlessly

**Tasks:**
1. Design override priority system
2. Implement mod detection for scene.bin modifications
3. Allow mods to provide their own enemy_text files
4. Document mod integration for mod authors

**Override Priority:**
```
1. Mod override (direct_mode_path/battle/enemy_text.dat)
2. Language-specific (lang-XX/battle/enemy_text.dat)
3. Base English (from scene.bin)
```

### Phase 5: UI Integration (Priority: Medium)

**Goal:** In-game language switching

**Tasks:**
1. Add language selection to game menu
2. Implement hotkey for quick language toggle
3. Optional: Dual-language display mode
4. Optional: "Show both" tooltip feature

### Phase 6: Field Dialogue Hot-Swap (Priority: Future)

**Goal:** Extend hot-swap to field dialogue

**Tasks:**
1. Investigate flevel.lgp text structure
2. Design unified field text format
3. Implement field text injection system
4. Consider tag-based approach for dialogue: `[EN]Hello[/EN][DE]Hallo[/DE]`

---

## File Format Specifications

### Enemy Text Data File Format

**Filename:** `enemy_text.dat` (per language) or `enemy_text_all.dat` (unified)

**Option A: Per-Language Binary Format**

```c
// enemy_text_XX.dat structure
struct EnemyTextHeader {
    char magic[4];        // "ET01"
    uint16_t version;     // 1
    uint16_t scene_count; // 256
    uint32_t reserved;
};

struct SceneText {
    char enemy_names[3][32];     // 3 enemies × 32 bytes
    char attack_names[32][32];   // 32 attacks × 32 bytes
};

// File layout:
// [Header]
// [SceneText × 256]
```

**Option B: Unified JSON Format (for development/debugging)**

```json
{
    "version": "1.0",
    "scenes": [
        {
            "scene_id": 0,
            "enemies": [
                {
                    "name": {
                        "en": "Guard Scorpion",
                        "de": "Wachskorpion",
                        "fr": "Scorpion gardien",
                        "es": "Escorpión guardián",
                        "ja": "ガードスコーピオン"
                    },
                    "attacks": [
                        {
                            "en": "Rifle",
                            "de": "Gewehr",
                            ...
                        },
                        ...
                    ]
                }
            ]
        }
    ]
}
```

### FFNx Configuration Extension

```toml
# FFNx.toml additions

# Enable multi-language text injection system
enable_text_injection = true

# Path to enemy text data files
# Files expected: {path}/enemy_text_en.dat, enemy_text_de.dat, etc.
enemy_text_path = "data/battle"

# Hot-swap mode: instant language switching without reload
enable_hot_swap = true

# Dual-language display (show both languages)
# Options: "off", "tooltip", "inline"
dual_language_mode = "off"
```

---

## FFNx Hook Points

### Existing Relevant Code

**File:** `src/ff7/battle/battle.cpp`

Current `load_scene_bin_chunk` handles scene loading - this is where we intercept.

**File:** `src/ff7.h` (externals)

```cpp
// Line 2863 - Battle formation ID pointer
WORD *battle_formation_id;

// Line 713 - Formation ID in battle data
uint16_t formationID;
```

### Required New Hooks

#### 1. Enemy Name Rendering Hook

**Target:** Function that renders enemy name in battle UI

**Research needed:** Find the function address in `ff7_externals` that:
- Takes enemy index as parameter
- Reads name from scene data
- Passes to text rendering system

**Hook implementation:**
```cpp
void ff7_render_enemy_name_hook(int enemy_idx, char* dest_buffer) {
    uint16_t scene_id = current_battle_scene_id;
    const char* lang = ff7_language.c_str();

    if (text_injection_enabled && enemy_text_table) {
        const char* name = get_enemy_name(scene_id, enemy_idx, lang);
        if (name) {
            strncpy(dest_buffer, name, 31);
            dest_buffer[31] = '\0';
            return;
        }
    }

    // Fallback to original behavior
    original_render_enemy_name(enemy_idx, dest_buffer);
}
```

#### 2. Attack Name Rendering Hook

**Target:** Function that displays attack name when enemy uses ability

**Hook implementation:**
```cpp
void ff7_render_attack_name_hook(int attack_idx, char* dest_buffer) {
    uint16_t scene_id = current_battle_scene_id;
    const char* lang = ff7_language.c_str();

    if (text_injection_enabled && enemy_text_table) {
        const char* name = get_attack_name(scene_id, attack_idx, lang);
        if (name) {
            strncpy(dest_buffer, name, 31);
            dest_buffer[31] = '\0';
            return;
        }
    }

    original_render_attack_name(attack_idx, dest_buffer);
}
```

#### 3. Scene ID Tracking

Need to track which scene is currently loaded:

```cpp
// In load_scene_bin_chunk or battle init
uint16_t current_battle_scene_id = 0;

void on_battle_scene_loaded(int scene_id) {
    current_battle_scene_id = scene_id;
    if (trace_all || trace_battle_text)
        ffnx_trace("Battle scene loaded: %d\n", scene_id);
}
```

---

## Mod Community Integration

### Challenge

The mod community creates English-only mods. Their workflow:
1. Mod modifies `flevel.lgp` or `scene.bin`
2. Places in `direct/` or `mods/` directory
3. FFNx loads mod files via override system

Our language system must not break this.

### Solution: Override Priority Chain

```
Priority (highest to lowest):
1. direct_mode_path overrides (user mods)
2. Language-specific text injection
3. Base game files (English structure)
```

**For scene.bin specifically:**
- Mods can replace entire scene.bin → their version is used
- Our text injection still works (hooks rendering, not file loading)
- Mod's English text shows when `ff7_language = "en"`
- Other languages use our injection data

**For enemy_text.dat:**
- Mods can provide their own: `direct/battle/enemy_text.dat`
- This allows mods to add custom enemy names in multiple languages

### Documentation for Mod Authors

Create a guide explaining:
1. How the multi-language system works
2. How to make mods compatible
3. How to provide multi-language support for custom content
4. File format specifications for `enemy_text.dat`

---

## Risk Assessment

### High Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| Can't find text rendering hook points | Blocks entire feature | Research battle module more; ask FFNx community |
| Performance impact of hook system | Noticeable lag in battles | Optimize lookup; use hash tables; cache current scene text |
| Text encoding issues (Japanese chars) | Garbled text | Use FF7's native encoding; test thoroughly |

### Medium Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| Mod compatibility issues | Breaks popular mods | Extensive testing with common mods; community feedback |
| File format changes needed | Rework required | Design format carefully upfront; version field for future changes |
| Memory usage increase | Crash on low-end systems | Lazy loading; configurable feature toggle |

### Low Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| Different enemy names in different regions | Minor text mismatches | Document differences; manual review |
| Font missing glyphs | Some chars not displayed | Verify font coverage; provide fallback |

---

## Open Questions

### Technical Questions

1. **Where exactly is enemy name rendering in FFNx/FF7?**
   - Need to trace through battle module code
   - May need to ask FFNx Discord community

2. **How does FF7 handle text encoding for Japanese?**
   - Shift-JIS? Custom encoding?
   - Need to verify compatibility with our injection system

3. **Is there a battle scene ID variable we can access?**
   - Need to track which scene is active for text lookup
   - May already exist in `ff7_externals`

4. **What about attack animations that display text?**
   - Limit breaks, summons, etc.
   - Same hook system or different?

### Design Questions

1. **Should we support dual-language display?**
   - "Guard Scorpion / Wachskorpion" in name display
   - Useful for learning but clutters UI

2. **How to handle language hotkey?**
   - Cycle through languages?
   - Quick toggle between two?
   - Configurable in TOML?

3. **What about kernel2.bin hot-swap?**
   - Currently requires restart
   - Can we reload text sections?

### Process Questions

1. **Testing strategy for 5 languages × all battles?**
   - Automated testing possible?
   - Community beta testing needed

2. **How to handle community contributions?**
   - Translation corrections
   - New language support

---

## References & Tools

### Scene.bin Tools

- **[Proud Clod](https://sourceforge.net/projects/proudclod/)** - Full enemy/scene editor
- **[ff7tools](https://github.com/cebix/ff7tools)** - Includes `unscene` for extraction
- **Scene Reader** - Win32 extraction tool
- **SceneFix** - Updates kernel.bin lookup table

### Documentation

- [FF7 Battle Scenes Wiki](https://wiki.ffrtt.ru/index.php/FF7/Battle/Battle_Scenes)
- [Qhimm Forums - Scene.bin Format](https://forums.qhimm.com/)
- [FF7 Flat Wiki - Battle Scenes](https://ff7-mods.github.io/ff7-flat-wiki/FF7/Battle/Battle_Scenes.html)

### FFNx Resources

- [FFNx GitHub Repository](https://github.com/julianxhokaxhiu/FFNx)
- [FFNx Discord](https://discord.gg/N6M6pKS) - Community support

### Related Project Files

- `/mnt/c/FFNx/src/ff7/battle/battle.cpp` - Current battle module code
- `/mnt/c/FFNx/src/ff7/file.cpp` - File routing implementation
- `/mnt/c/FFNx/src/ff7/kernel.cpp` - Kernel loading (reference for text tables)

---

## Changelog

### Version 1.0.0 (2025-12-23)

- Initial document creation
- Documented German battle bug root cause
- Proposed text injection architecture
- Defined implementation phases
- Specified file formats

---

## Next Session Checklist

- [ ] Research enemy name rendering function in FFNx/FF7
- [ ] Find battle text hook points in `ff7_externals`
- [ ] Create scene.bin text extraction script
- [ ] Extract text from all 5 language scene.bin files
- [ ] Prototype text injection with single enemy
- [ ] Test hot-swap with prototype
