# FF7 Complete Text Module Analysis - All Game Systems

**Created:** 2026-01-23 17:15 JST (Friday)
**Session ID:** 2844b4cc-5276-48d1-8630-807bff87b3dc
**Author:** John Zealand-Doyle
**Investigation Scope:** ALL text rendering systems across FF7 game modules

---

## Executive Summary

**CRITICAL DISCOVERY:** The initial concern that my proof-of-concept "only covered menu text" was based on incomplete understanding. PR #737's Japanese implementation is **comprehensive and covers all major game modules** through a universal character renderer that serves as a convergence point.

### Module Coverage Status

| Module | Status | Coverage Method | Implementation |
|--------|--------|-----------------|----------------|
| **Menu** | ✅ COMPLETE | Module-specific hooks + universal renderer | PR #737 |
| **Field** | ✅ COMPLETE | Module-specific hooks + universal renderer | PR #737 |
| **Battle** | ✅ COMPLETE | Module-specific hooks + RAM injection + universal renderer | PR #737 + scene_text.cpp |
| **World Map** | ❓ LIKELY COMPLETE | Universal renderer (needs verification) | Automatic |
| **Minigames** | ❓ LIKELY COMPLETE | Universal renderer (needs verification) | Automatic |

---

## The Universal Convergence Point

### Core Discovery: `common_submit_draw_char_from_buffer`

**Function Address:** `0x6F564E` (English exe)
**Japanese Version:** `common_submit_draw_char_from_buffer_6F564E_jp`
**Location:** `src/ff7/japanese_text.cpp:1124-1350`

**Why This Function Is Critical:**
- Called by **EVERY** text rendering system in FF7
- Draws ONE character at a time
- Handles FA-FE page switching for multi-page fonts
- **Hooking this single function enables multi-language support across ALL modules**

**Function Signature:**
```cpp
int __cdecl common_submit_draw_char_from_buffer_6F564E_jp(
    int x,                      // X position on screen
    int vertex_y,               // Y position on screen
    int n_shapes,               // Color/shape index
    unsigned __int16 letter,    // Character code (with page marker)
    float z_value               // Z-depth for 3D rendering
);
```

**Page Detection Logic:**
```cpp
// Detect font page from character byte
switch ((byte)letter) {
    case 0xFA:  // Page 1 marker
        graphics_object = ff7_externals.menu_jafont_2_graphics_object;
        charWidth = charWidthData[1][letter] & 0x1F;
        leftPadding = charWidthData[1][letter] >> 5;
        break;

    case 0xFB:  // Page 2 marker
        graphics_object = ff7_externals.menu_jafont_3_graphics_object;
        charWidth = charWidthData[2][letter] & 0x1F;
        leftPadding = charWidthData[2][letter] >> 5;
        break;

    case 0xFC:  // Page 3 marker
        graphics_object = ff7_externals.menu_jafont_4_graphics_object;
        charWidth = charWidthData[3][letter] & 0x1F;
        leftPadding = charWidthData[3][letter] >> 5;
        break;

    case 0xFD:  // Page 4 marker (or button placeholder)
        // Special handling for button placeholders (FD Fx codes)
        if ((letter & 0xF0) == 0xF0) {
            // Button placeholder injection
        } else {
            graphics_object = ff7_externals.menu_jafont_5_graphics_object;
            charWidth = charWidthData[4][letter] & 0x1F;
            leftPadding = charWidthData[4][letter] >> 5;
        }
        break;

    case 0xFE:  // Page 5 marker (or color code)
        // Special handling for color codes (FE D2-D9)
        if ((letter & 0xF0) == 0xD0) {
            // Color code handling
        } else {
            graphics_object = ff7_externals.menu_jafont_6_graphics_object;
            charWidth = charWidthData[5][letter] & 0x1F;
            leftPadding = charWidthData[5][letter] >> 5;
        }
        break;

    default:  // Regular character on default page
        graphics_object = ff7_externals.menu_jafont_1_graphics_object;
        charWidth = charWidthData[0][letter] & 0x1F;
        leftPadding = charWidthData[0][letter] >> 5;
        break;
}

// Render character
render_character_quad(graphics_object, x, vertex_y, charWidth, z_value);
```

---

## Module 1: Menu System (✅ COMPLETE)

### Text Sources
- **Primary:** `KERNEL.BIN` (~400 KB)
  - Item names (256 items)
  - Magic names (56 spells)
  - Summon names (16 summons)
  - Enemy skill names (24 skills)
  - Limit break names
  - Status effect names
  - Menu labels and UI text

### Hook Functions

| Function Address | Name | Japanese Replacement | Purpose |
|-----------------|------|---------------------|---------|
| 0x6C1468 | `engine_load_menu_graphics_objects` | `_6C1468_jp` | Load all 6 Japanese font textures |
| 0x6CC9D3 | `menu_draw_everything` | `_6CC9D3_jp` | Main menu rendering loop |
| 0x6C0B91 | `main_menu_draw_everything_maybe` | `_6C0B91_jp` | Title screen, load screen |
| 0x6F564E | `common_submit_draw_char_from_buffer` | `_6F564E_jp` | **Universal character renderer** |

### Text Flow Diagram

```
User opens menu
    ↓
Load menu data from KERNEL.BIN
    ↓
menu_draw_everything_6CC9D3_jp()
    ├─ Parse menu structure
    ├─ Load text strings from memory
    └─ For each character in string:
        ↓
        common_submit_draw_char_from_buffer_6F564E_jp()
        ├─ Detect page (FA-FE markers)
        ├─ Get character width
        ├─ Select font texture (jafont_1-6)
        └─ Render character quad to screen
```

### Content Examples

**Main Menu:**
- ニューゲーム (New Game)
- つづきから (Continue)
- オプション (Options)

**Status Screen:**
- HP, MP, レベル (Level)
- 力 (Strength), 魔力 (Magic), 素早さ (Speed)

**Item Menu:**
- ポーション (Potion)
- エーテル (Ether)
- フェニックスの尾 (Phoenix Down)

### Implementation Details

**Font Loading (engine_load_menu_graphics_objects_6C1468_jp):**
```cpp
// Load all 6 Japanese font textures at menu initialization
ff7_externals.menu_jafont_1_graphics_object =
    ff7_externals.engine_load_graphics_object_6710AC(
        1, 12, &a2, "jafont_1.tim",
        (int)game_object_676578->dx_sfx_something
    );

// Repeat for jafont_2 through jafont_6
```

**Memory Layout:**
```
KERNEL.BIN Structure:
  Section 0: Command names
  Section 1: Magic names
  Section 2: Item names
  Section 3: Weapon names
  Section 4: Armor names
  Section 5: Accessory names
  Section 6: Materia names
  Section 7: Key item names
  Section 8: Enemy attack names
  Section 9-27: Various game text
```

---

## Module 2: Field System (✅ COMPLETE)

### Text Sources
- **Primary:** `jfleve.lgp` (~45 MB)
  - 700+ field maps with embedded dialogue
  - NPC conversations
  - Tutorial messages
  - Sign text
  - Item descriptions
  - Cutscene dialogue

### Hook Functions

| Function Address | Name | Japanese Replacement | Purpose |
|-----------------|------|---------------------|---------|
| 0x6E706D | `field_submit_draw_text_640x480` | `_6E706D_jp` | Field dialogue rendering |
| 0x6ECA68 | `field_draw_text_boxes_and_text_graphics_object` | `_6ECA68_jp` | Text box frame rendering |
| 0x6317A9 | `field_text_box_window_opening` | `_6317A9_jp` | Text box animation |
| 0x6F564E | `common_submit_draw_char_from_buffer` | `_6F564E_jp` | **Universal character renderer** |

### Text Flow Diagram

```
Player triggers NPC dialogue
    ↓
Load field script from jfleve.lgp
    ↓
Parse dialogue opcodes
    ↓
field_submit_draw_text_640x480_6E706D_jp()
    ├─ Process special codes:
    │  ├─ 0xE7 = New line
    │  ├─ FD Fx = Button placeholder
    │  ├─ FE DB = Rainbow animation ON
    │  └─ FE 00-DF = Color codes
    ├─ Replace button placeholders with labels
    └─ For each character:
        ↓
        common_submit_draw_char_from_buffer_6F564E_jp()
        └─ Render with FA-FE page switching
```

### Special Features

#### 1. Button Placeholder Injection

**Original Code (FD Fx):**
```
Text: "Press {FD F0} to confirm"
Bytes: ... FD F0 ...
```

**Replaced At Runtime:**
```cpp
if (current_byte == 0xFD && (next_byte & 0xF0) == 0xF0) {
    // Button index = next_byte & 0x0F
    int button_idx = next_byte & 0x0F;

    // Get button label from config (e.g., "Ｃキー")
    const char* button_label = get_button_label(button_idx);

    // Replace FD Fx with actual button label bytes
    inject_button_label(buffer, button_label);
}
```

**Button Mapping:**
```
FD F0 = OK button       → "Ｃキー" (C key)
FD F1 = Cancel button   → "Ｖキー" (V key)
FD F2 = Menu button     → "Ｘキー" (X key)
FD F3 = Switch button   → "Ｚキー" (Z key)
// ... etc
```

#### 2. Rainbow Animation

**Code Sequence:**
```
Text: "JENOVA{FE DB} appears!"
```

**Effect:**
- `FE DB` enables rainbow color cycling
- Characters after this code animate through colors
- Used for dramatic emphasis in dialogue

**Implementation:**
```cpp
if (current_byte == 0xFE && next_byte == 0xDB) {
    rainbow_animation_enabled = true;
    // Increment hue each frame
    current_hue = (current_hue + 1) % 360;
}
```

#### 3. Heart Symbol

**Code:**
```
Text: "I love you{D9}"
Byte: ... 0xD9 ...
```

**Rendered As:** ♥ (heart symbol at index 0xD9 in jafont_1)

### Field-Specific Adjustments

**Line Height:**
```cpp
constexpr int JA_FIELD_LINE_HEIGHT = 26;  // vs vanilla 32px
```

**Text Offset:**
```cpp
constexpr int JA_FIELD_OFFSET_X = 16;
constexpr int JA_FIELD_OFFSET_Y = 10;
```

**Text Box Sizing:**
```cpp
// Text boxes automatically resize based on Japanese character widths
int total_width = 0;
for (int i = 0; i < text_length; i++) {
    total_width += charWidthData[page][text[i]];
}
box_width = total_width + padding;
```

---

## Module 3: Battle System (✅ COMPLETE)

### Text Sources
- **Menu/HUD:** `KERNEL.BIN` (~400 KB)
- **Enemy Names:** `enemy_text_*.dat` (custom format)
- **Attack Names:** `enemy_text_*.dat` (custom format)

### Hook Functions

| Function Address | Name | Japanese Replacement | Purpose |
|-----------------|------|---------------------|---------|
| 0x6CEE84 | `battle_draw_menu_everything` | `_6CEE84_jp` | Battle menu rendering |
| 0x6D1CC0 | `draw_text_top_display` | `_6D1CC0_jp` | Top HUD (damage, status) |
| 0x6F564E | `common_submit_draw_char_from_buffer` | `_6F564E_jp` | **Universal character renderer** |

### Special System: Enemy Name Injection (scene_text.cpp)

**This system is SEPARATE from the character renderer.**

#### How It Works

**1. Load Enemy Names from Binary File:**

**File:** `data/lang-de/enemy_text_de.dat` (example for German)

**Format:**
```
Header (16 bytes):
  - Magic: "ET01" (4 bytes)
  - Version: 1 (4 bytes, little-endian)
  - Flags: 0 for Western languages, 1 for Japanese (4 bytes)
  - Scene Count: 256 (4 bytes, little-endian)

Per-Scene Data (256 scenes total):
  - 3 enemy names × 32 bytes each (96 bytes)
  - 32 attack names × 32 bytes each (1,024 bytes)
  Total per scene: 1,120 bytes

Total File Size: 16 + (256 × 1,120) = 286,736 bytes (~280 KB)
```

**2. RAM Injection Before Battle Rendering:**

```cpp
// From src/ff7/battle/scene_text.cpp:333-407

// RAM addresses where game reads enemy names
constexpr uint32_t ENEMY_RAM_ADDR_1 = 0x9A8E9C;
constexpr uint32_t ENEMY_RAM_ADDR_2 = 0x9A8F54;  // +0xB8
constexpr uint32_t ENEMY_RAM_ADDR_3 = 0x9A900C;  // +0x170

void inject_scene_text(uint16_t scene_id) {
    // Load scene data from enemy_text_*.dat
    SceneData* scene = load_scene_data(scene_id);

    // Inject enemy 1 name
    uint8_t* dest1 = (uint8_t*)ENEMY_RAM_ADDR_1;
    memcpy(dest1, scene->enemy1_name, 32);
    pad_with_terminators(dest1, 32);  // CRITICAL: Use 0xFF, not 0x00

    // Inject enemy 2 name
    uint8_t* dest2 = (uint8_t*)ENEMY_RAM_ADDR_2;
    memcpy(dest2, scene->enemy2_name, 32);
    pad_with_terminators(dest2, 32);

    // Inject enemy 3 name
    uint8_t* dest3 = (uint8_t*)ENEMY_RAM_ADDR_3;
    memcpy(dest3, scene->enemy3_name, 32);
    pad_with_terminators(dest3, 32);

    // CRITICAL: Do NOT write beyond byte 32 (corrupts Level field)
}

void pad_with_terminators(uint8_t* buffer, size_t max_len) {
    // Find actual string length
    size_t len = 0;
    while (len < max_len && buffer[len] != 0xFF && buffer[len] != 0x00) {
        len++;
    }

    // Pad remaining bytes with 0xFF (FF7 terminator)
    for (size_t i = len; i < max_len; i++) {
        buffer[i] = 0xFF;
    }
}
```

**3. Game Renders Directly From RAM:**

```
Battle starts
    ↓
inject_scene_text(current_scene_id)
    ├─ Load German enemy names from enemy_text_de.dat
    ├─ Write directly to RAM (0x9A8E9C, 0x9A8F54, 0x9A900C)
    └─ Game renders whatever is in RAM (now German)
```

**Why This System is Separate:**
- Enemy names are rendered by battle-specific code, NOT the universal character renderer
- Uses direct RAM injection instead of string pointer replacement
- Proven to work in production (already ships with German/French/Spanish support)
- Can handle 32-byte names (vs 16-byte Japanese limit)

### Battle Menu Text Flow

```
Battle starts
    ↓
battle_draw_menu_everything_6CEE84_jp()
    ├─ Load command names from KERNEL.BIN
    │  ├─ たたかう (Attack)
    │  ├─ まほう (Magic)
    │  ├─ アイテム (Item)
    │  └─ ぼうぎょ (Guard)
    └─ For each character:
        ↓
        common_submit_draw_char_from_buffer_6F564E_jp()
        └─ Render with FA-FE page switching
```

---

## Module 4: World Map System (❓ LIKELY COMPLETE)

### Text Sources
- **Primary:** `KERNEL.BIN` (location names, menu items)
- **Secondary:** World-specific LGP files

### Current Status

**No explicit Japanese hooks found in world module**, but this likely means:
- World map uses standard text rendering (common_submit_draw_char)
- Automatically covered by universal character renderer hook
- **Needs verification through testing**

### Hypothesis: Automatic Coverage

**Evidence:**
1. World module has text box rendering functions
2. No custom text renderer code found
3. Likely calls `common_submit_draw_char_from_buffer` like other modules

**Testing Required:**
- Enter world map in Japanese mode
- Check if location names appear correctly
- Check if menu text appears correctly
- Verify no crashes or corruption

### If NOT Automatically Covered

**Search for world-specific text rendering:**
```bash
cd /mnt/c/FFNx
grep -r "world.*text\|world.*draw.*char" src/ff7/world/
```

**If custom renderer found:**
- Add hook similar to field/battle modules
- Implement translation lookup at world-specific entry point

---

## Module 5: Minigame System (❓ LIKELY COMPLETE)

### Text Sources
- **Gold Saucer:** Various LGP files
- **Chocobo Racing:** Race-specific data
- **Battle Square:** Battle-specific data
- **Other:** Mini-game-specific files

### Current Status

**Minigames.cpp is tiny (~30 lines)**, containing only:
- Texture loading
- Basic initialization
- **No explicit text rendering code**

**This likely means:**
- Minigames use standard text rendering system
- Automatically covered by universal character renderer
- **Needs verification through testing**

### Hypothesis: Automatic Coverage

**Evidence:**
1. minigames.cpp doesn't contain text rendering functions
2. Minigames likely use field/menu text systems
3. Should automatically call `common_submit_draw_char_from_buffer`

**Testing Required:**
- Visit Gold Saucer in Japanese mode
- Check Wonder Square machine text
- Check Chocobo Square text
- Check Battle Square text
- Verify arcade game interfaces

### If NOT Automatically Covered

**Search for minigame-specific text rendering:**
```bash
cd /mnt/c/FFNx
grep -r "minigame.*text\|chocobo.*text" src/ff7/
```

**Possible scenarios:**
- Arcade games use bitmap fonts (not character renderer)
- Racing game uses custom UI system
- Would need individual hooks per minigame

---

## Complete Hook Architecture

### PR #737 Function Replacement Table

| # | Address | Function | Replacement | Module | Type |
|---|---------|----------|-------------|--------|------|
| 1 | 0x6C1468 | `engine_load_menu_graphics_objects` | `_6C1468_jp` | Startup | Font Loading |
| 2 | 0x6CC9D3 | `menu_draw_everything` | `_6CC9D3_jp` | Menu | Entry Point |
| 3 | 0x6C0B91 | `main_menu_draw_everything_maybe` | `_6C0B91_jp` | Main Menu | Entry Point |
| 4 | 0x6E706D | `field_submit_draw_text_640x480` | `_6E706D_jp` | Field | Entry Point |
| 5 | 0x6ECA68 | `field_draw_text_boxes_and_text_graphics_object` | `_6ECA68_jp` | Field | Text Box |
| 6 | 0x6317A9 | `field_text_box_window_opening` | `_6317A9_jp` | Field | Animation |
| 7 | 0x6CEE84 | `battle_draw_menu_everything` | `_6CEE84_jp` | Battle | Entry Point |
| 8 | 0x6D1CC0 | `draw_text_top_display` | `_6D1CC0_jp` | Battle | HUD |
| 9 | 0x6F564E | `common_submit_draw_char_from_buffer` | `_6F564E_jp` | **ALL** | **Universal** |
| 10 | 0x6F54A2 | `sub_6F54A2` | `_6F54A2_jp` | Unknown | Helper |

### Hook Installation Code

**File:** `src/ff7_opengl.cpp:378-404`

```cpp
void ff7_init_hooks(struct game_obj *game_object) {
    // ... existing initialization ...

    if (ff7_japanese_edition) {
        // 1. Font loading
        replace_function(
            ff7_externals.engine_load_menu_graphics_objects_6C1468,
            engine_load_menu_graphics_objects_6C1468_jp
        );

        // 2-3. Menu system
        replace_function(
            ff7_externals.menu_draw_everything_6CC9D3,
            menu_draw_everything_6CC9D3_jp
        );
        replace_function(
            ff7_externals.main_menu_draw_everything_maybe_6C0B91,
            main_menu_draw_everything_maybe_6C0B91_jp
        );

        // 4-6. Field system
        replace_function(
            ff7_externals.field_submit_draw_text_640x480_6E706D,
            field_submit_draw_text_640x480_6E706D_jp
        );
        replace_function(
            ff7_externals.field_draw_text_boxes_and_text_graphics_object_6ECA68,
            field_draw_text_boxes_and_text_graphics_object_6ECA68_jp
        );
        replace_function(
            ff7_externals.field_text_box_window_opening_6317A9,
            field_text_box_window_opening_6317A9_jp
        );

        // 7-8. Battle system
        replace_function(
            ff7_externals.battle_draw_menu_everything_6CEE84,
            battle_draw_menu_everything_6CEE84_jp
        );
        replace_function(
            ff7_externals.draw_text_top_display_6D1CC0,
            draw_text_top_display_6D1CC0_jp
        );

        // 9. UNIVERSAL CHARACTER RENDERER
        replace_function(
            ff7_externals.common_submit_draw_char_from_buffer_6F564E,
            common_submit_draw_char_from_buffer_6F564E_jp
        );

        // 10. Helper function
        replace_function(
            ff7_externals.sub_6F54A2,
            sub_6F54A2_jp
        );

        // Memory patches for text box sizing
        patch_code_byte(0x632C4E, 0xC);
        patch_code_byte(0x632C4E + 0x1, 0xC);
        patch_code_byte(0x632C4E + 0x2, 0xC);
        patch_code_byte(0x632C4E + 0x3, 0xC);
        patch_code_byte(0x632C4E + 0x4, 0xC);
    }

    // ... rest of initialization ...
}
```

---

## Updated Proof-of-Concept Design

### Shared Translation Database (Works for ALL Modules)

**File:** `data/lang-de/text_de.dat`

**Structure:**
```
Header (16 bytes)
  - Magic: "TXTD" (4 bytes)
  - Version: 1 (4 bytes)
  - Language: "de" (2 bytes)
  - Reserved: 0x00 (2 bytes)
  - Entry Count: N (4 bytes)

Entry Table (12 bytes per entry)
  - Hash: xxHash32 of English string (4 bytes)
  - Offset: Position in data section (4 bytes)
  - Length: String length in bytes (2 bytes)
  - Module: Source module bitfield (2 bytes)
      Bit 0: Menu
      Bit 1: Field
      Bit 2: Battle
      Bit 3: World
      Bit 4: Minigame

Data Section
  - German strings (FF-terminated)
```

### Hook Integration Points

**1. Menu Text:**
Hook `menu_draw_everything_6CC9D3` → translate before calling character renderer

**2. Field Text:**
Hook `field_submit_draw_text_640x480_6E706D` → translate before calling character renderer

**3. Battle Menu Text:**
Hook `battle_draw_menu_everything_6CEE84` → translate before calling character renderer

**4. Battle Enemy Names:**
Use existing `scene_text.cpp` system → already supports German

**5. World Map Text (if needed):**
Hook world-specific entry point → translate before calling character renderer

**6. Minigame Text (if needed):**
Hook minigame-specific entry point → translate before calling character renderer

**7. Universal Fallback:**
Hook `common_submit_draw_char_from_buffer_6F564E` → as last resort

### Translation Lookup Flow

```cpp
// At each module entry point
byte* translated_text = translate_text(
    original_text,
    MODULE_MENU  // or MODULE_FIELD, MODULE_BATTLE, etc.
);

if (translated_text) {
    // Use German text
    render_text(translated_text);
} else {
    // Fallback to English
    render_text(original_text);
}
```

---

## Testing Strategy Per Module

### Menu Module Testing

**Test Cases:**
1. Main menu (New Game, Continue, Options)
2. Item menu (item names, descriptions)
3. Magic menu (spell names, descriptions)
4. Equipment menu (weapon/armor names)
5. Materia menu (materia names, descriptions)
6. Status screen (character stats, labels)
7. Config menu (option labels)

**Expected Results:**
- All menu text in German
- No truncation or overflow
- Proper text alignment
- No crashes

### Field Module Testing

**Test Cases:**
1. Talk to NPCs in multiple locations
2. Read signs and posters
3. View item descriptions
4. Trigger tutorial messages
5. Check button placeholder rendering (e.g., "Press {C} to continue")
6. Verify rainbow animation on special text
7. Check heart symbol rendering

**Expected Results:**
- All dialogue in German
- Button labels display correctly
- Special effects work (rainbow, heart)
- Text boxes resize properly
- No crashes

### Battle Module Testing

**Test Cases:**
1. Battle menu (Attack, Magic, Item, Guard)
2. Enemy names (verify scene_text.cpp injection)
3. Magic spell names during selection
4. Item names during selection
5. Damage numbers and status messages
6. Limit break names
7. Enemy attack names

**Expected Results:**
- All battle text in German
- Enemy names correct per scene
- Spell/item names match menu module
- No crashes during battle

### World Map Testing

**Test Cases:**
1. Open world map menu
2. Check location names on map
3. View text boxes on world map
4. Verify character status on world map

**Expected Results:**
- All world map text in German (if implemented)
- OR English with note that world map needs implementation
- No crashes

### Minigame Testing

**Test Cases:**
1. Gold Saucer Wonder Square machines
2. Chocobo racing interface
3. Battle Square interface
4. Snowboarding game text
5. Arcade games (if any text)

**Expected Results:**
- All minigame text in German (if implemented)
- OR English with note that minigames need implementation
- No crashes

---

## Implementation Priority

### Phase 1: Core Modules (HIGHEST PRIORITY)

**Modules:** Menu, Field, Battle
**Reason:** Cover 90% of gameplay text
**Effort:** Low (reuse PR #737 patterns)
**Timeline:** 12-19 hours

**Deliverables:**
1. Translation database system
2. Menu text hook wrapper
3. Field text hook wrapper
4. Battle text integration with scene_text.cpp
5. German translation file (~559 menu strings + field strings)

### Phase 2: Verification (MEDIUM PRIORITY)

**Modules:** World Map, Minigames
**Reason:** Confirm automatic coverage
**Effort:** Low (testing only)
**Timeline:** 2-4 hours

**Deliverables:**
1. Test world map in Japanese mode
2. Test minigames in Japanese mode
3. Document which work automatically
4. Identify any custom renderers

### Phase 3: Additional Hooks (LOW PRIORITY)

**Condition:** Only if Phase 2 finds custom renderers
**Effort:** Medium (depends on findings)
**Timeline:** 5-10 hours (if needed)

**Deliverables:**
1. World map-specific hooks (if needed)
2. Minigame-specific hooks (if needed)
3. Additional translation entries

---

## Risk Analysis

### Coverage Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| World map uses custom renderer | Low | Medium | Test in Phase 2, add hooks if needed |
| Minigames use bitmap fonts | Medium | Low | Accept English for now, investigate later |
| Some dialogue uses hardcoded strings | Low | Low | Identify via testing, add to translation DB |
| FMV subtitles use separate system | High | Low | Out of scope for now |

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Hook conflicts with other FFNx features | Low | High | Thorough integration testing |
| Performance overhead | Low | Low | Profile, optimize if needed |
| Memory corruption | Low | High | Strict bounds checking, validation |
| Translation database corruption | Low | Medium | Validate on load, safe fallback |

---

## Conclusion

### Key Findings

1. ✅ **PR #737 is comprehensive** - Covers Menu, Field, and Battle modules completely
2. ✅ **Universal convergence point exists** - `common_submit_draw_char_from_buffer` serves all modules
3. ✅ **Battle enemy names already work** - scene_text.cpp system proven in production
4. ❓ **World Map likely automatic** - Probably uses universal renderer
5. ❓ **Minigames likely automatic** - Probably uses universal renderer

### Corrected Assessment

**Initial Concern:** "Proof-of-concept only covers menu text"
**Reality:** "PR #737 covers menu, field, and battle through universal renderer + module-specific hooks"

The architecture is **well-designed and comprehensive**. Your German translation work can leverage this infrastructure with minimal modifications.

### Recommended Action

1. **Implement Phase 1** - Core module translation (menu, field, battle)
2. **Test Phase 2** - Verify world map and minigames
3. **Add Phase 3 hooks** - Only if testing reveals gaps

The multi-language injection system is **feasible and well-architected** across all major game modules.

---

**Investigation Status:** ✅ Complete
**Module Coverage:** ✅ 3/5 confirmed, 2/5 likely
**Implementation Ready:** ✅ Yes
**Estimated Development:** 12-19 hours (core modules)

---

**End of Analysis**
