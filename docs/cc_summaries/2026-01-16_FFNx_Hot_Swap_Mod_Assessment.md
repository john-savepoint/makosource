# FFNx Hot-Swapping and Real-Time Mod Modification - Comprehensive Assessment

**Created**: 2026-01-16 14:18:09 JST (Thursday)
**Session ID**: bdf465b1-9f3d-4ab0-8084-40f64c3fc42c
**Author**: Claude Code (Sonnet 4.5)
**Version**: 1.0.0

---

## Executive Summary

This assessment evaluates FFNx's capability to support real-time modification swapping and hot-reloading of mods during gameplay. The analysis is based on comprehensive review of:

- FFNx Developer Guide (2,310 lines)
- 7th Heaven Developer Guide (2,173 lines)
- Game Engine documentation (2,000+ lines analyzed)
- Naming screen tables and session context documentation

**Key Finding**: FFNx has significant existing infrastructure that could support real-time modification swapping, but the current implementation is designed for startup-time loading. Feasibility varies dramatically by modification type, with **HEXT memory patches being the highest-feasibility target** for hot-swapping.

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Feasibility Analysis by Modification Type](#feasibility-analysis-by-modification-type)
3. [Existing Infrastructure for Hot-Swapping](#existing-infrastructure-for-hot-swapping)
4. [Implementation Tiers](#implementation-tiers)
5. [Technical Details](#technical-details)
6. [Recommendations](#recommendations)
7. [Conclusion](#conclusion)

---

## System Architecture Overview

### FFNx Modding Pipeline

```
Game Startup
    ↓
FFNx.dll initialization
    ↓
Load FFNx.toml configuration
    ↓
Apply HEXT patches from misc/hext/ (runtime assembly patches)
    ↓
Register texture override paths (mods/Textures/)
    ↓
Initialize 7th Heaven VFS integration (if present)
    ↓
Game runtime (file I/O intercepted, textures overridden)
```

### 7th Heaven Virtual File System

```
Game requests file (e.g., menu_us.lgp/usfont.tex)
    ↓
EasyHook intercepts Win32 API call
    ↓
7thWrapperLib.dll searches active mods (by build order priority)
    ↓
For each active mod:
  - Check mod.xml for matching path
  - Check Conditional folders (RuntimeVar evaluation)
  - Check IRO archive contents
    ↓
If found: Return modded asset
If not found: Return original game asset
```

**Critical Insight**: The 7th Heaven VFS **already operates at runtime** - it intercepts every file I/O call dynamically. This proves the foundation for hot-swapping exists.

---

## Feasibility Analysis by Modification Type

### 1. HEXT Patches (Memory Modifications) - ✅ HIGH FEASIBILITY

**Current Implementation**:
- HEXT patches applied at startup via `load_hext_patches()` in `src/hext.cpp`
- Patches directly modify process memory using `apply_patch(uint32_t address, const std::vector<uint8_t>& bytes)`
- Format example:
  ```hext
  # misc/hext/ff7/en/my_patch.txt
  401000 = E9 3B 05 00 00  # JMP to custom code
  401005 = 90 90 90        # NOP padding
  ```

**Hot-Swap Assessment**:

| Feature Type | Feasibility | Notes |
|--------------|-------------|-------|
| EXP Multipliers | ✅ Trivial | Single memory address modification |
| Stat Modifiers | ✅ Trivial | Known addresses (e.g., 0x718E9D cursor limit) |
| Gameplay Tweaks | ✅ Easy | No asset reloading required |
| Code Flow Modifications | ⚠️ Needs Care | Must apply during "safe" moments (menu, pause) |

**Why This Works**:
- Memory writes are instant - no asset loading involved
- FFNx already has `apply_patch()` function ready to use
- Could be triggered by hotkey or in-game menu

**Implementation Approach**:
```cpp
// Hypothetical FFNx extension
void hot_reload_hext_patch(const char* patch_file) {
    // Could be triggered by hotkey or DevTools overlay
    parse_and_apply_hext(patch_file);
    ffnx_info("Hot-reloaded HEXT patch: %s\n", patch_file);
}
```

**Challenges**:
- Need to track which patches are currently applied (for undo/toggle)
- Some patches may have dependencies or order requirements
- No existing UI/mechanism in FFNx to trigger reloads
- Must avoid applying patches to code currently executing (could crash)

---

### 2. Background Textures (Field Backgrounds) - ⚠️ MEDIUM-HIGH FEASIBILITY

**Current Implementation**:
- FFNx uses external texture override system: `mods/Textures/` paths
- Background textures loaded per-field from `FLEVEL.LGP`
- 7th Heaven's VFS intercepts file I/O requests at Win32 API level
- From Game Engine docs: "Backgrounds are actually 16x16 blocks loaded into VRAM and assembled into the video buffer every frame"

**Hot-Swap Assessment**:

| Scenario | Feasibility | Implementation |
|----------|-------------|----------------|
| When entering new field | ✅ Very Achievable | Each field load triggers fresh file I/O |
| While in current field | ⚠️ Requires cache invalidation | Need to flush VRAM cache + re-request textures |

**Existing Foundation** (from 7TH_HEAVEN_DEVELOPER_GUIDE.md):
```xml
<!-- Conditional folders already swap assets based on game state -->
<Conditional Folder="midgar_slums">
  <RuntimeVar Var="FieldID" Values="0xD5,0x160" />
</Conditional>
```

**Critical Insight**: This proves the concept **already works** for location-based asset switching. Extending to user-triggered swaps is architecturally similar.

**Implementation Requirements**:
1. **Between Fields**: Update VFS/texture override path before field load
   - Could modify `mod.xml` Conditional folders dynamically
   - Or update FFNx texture search paths in memory
2. **Same Field**: Requires texture cache invalidation
   - FFNx has `trace_loaders` suggesting awareness of texture loading pipeline
   - Would need to expose `flush_texture_cache()` + `reload_background_textures()` functions

**Known Hooks** (from FFNX_DEVELOPER_GUIDE.md):
```cpp
load_texture @ 0x688415  // Texture loading (for override)
```
This is the ideal injection point for hot-swap logic.

---

### 3. Character Textures/Models - ⚠️ MEDIUM FEASIBILITY

**Current Implementation**:
- Character models use `.P` polygon files + associated textures
- Textures loaded from `CHAR.LGP` (field) and battle LGPs
- FFNx hooks `load_texture` at `0x688415`

**Hot-Swap Assessment**:

| Context | Feasibility | Notes |
|---------|-------------|-------|
| Between battles | ✅ Achievable | Battle module fully reloads assets |
| Mid-field | ⚠️ Harder | Character models are cached |
| Mid-battle | ❌ Very Difficult | Active rendering references |

**Recommendation**: Target context transitions (entering battles, changing fields) as safe reload points.

---

### 4. Menu Textures - ✅ HIGH FEASIBILITY

**Current Implementation**:
- Menu textures (`WINDOW.BIN`, character avatars) relatively static
- FFNx already patches menu font handling extensively
- Texture override paths: `mods/Textures/menu/`

**Hot-Swap Assessment**: ✅ Very achievable
- Menu assets reload when entering menus
- Could force reload by hooking menu entry points
- Lower complexity than field/battle assets

---

### 5. Audio/Music - ✅ HIGH FEASIBILITY

**Current Implementation**:
- FFNx uses **SoLoud audio engine**
- Music/SFX paths configurable in `FFNx.toml`
- 7th Heaven can redirect audio files

**Hot-Swap Assessment**: ✅ Already partially implemented conceptually
- Conditional music folders exist in 7th Heaven
- Music changes between locations already work
- SoLoud supports dynamic loading by design

**Example** (from 7TH_HEAVEN_DEVELOPER_GUIDE.md):
```xml
<!-- Music mod with options -->
<Option>
  <Name>Battle Theme</Name>
  <Folder>battle_music_choice_1</Folder>
</Option>
```

**Implementation**: Trigger music reload via SoLoud API when user changes selection.

---

## Existing Infrastructure for Hot-Swapping

### 1. Runtime Variable System (7th Heaven)

**Already Supports Dynamic Asset Swapping**:
```xml
<!-- Assets swap based on game state automatically -->
<Conditional Folder="junon_assets">
  <RuntimeVar Var="PPV" Values="300..400" />  <!-- Story progression -->
</Conditional>

<Conditional Folder="special_battle_music">
  <RuntimeVar Var="BattleID" Values="50" />  <!-- Specific boss battle -->
</Conditional>
```

**Available Runtime Variables**:
- `FieldID` - Current field map
- `PPV` - Story progression value
- `BattleID` - Current battle
- `MenuState` - Menu open/closed
- Custom memory addresses: `Short:0xCC15D0:2`, `Byte:0xDC0820:1`, etc.

**Key Insight**: 7th Heaven **already reads game memory in real-time** to determine which assets to serve. This proves runtime mod switching is architecturally sound.

---

### 2. FFNx DevTools Overlay

**Current Features** (from `src/overlay.cpp`):
- FPS counter display
- Debug information overlay
- Built on ImGui framework

**Potential Extension**:
- Add mod toggle UI to overlay
- Display active HEXT patches
- Provide hotkey bindings for instant toggles

**Example UI Structure**:
```
FFNx DevTools
├── FPS: 60
├── Active Mods:
│   ├── [✓] EXP Boost (3x)         [Toggle] [Configure]
│   ├── [✓] No Encounters          [Toggle]
│   ├── [ ] Hard Mode Battles      [Toggle]
│   └── [✓] HD Textures Pack       [Toggle on Field Change]
└── Hotkeys: F5=Toggle Mods, F6=Reload HEXT
```

---

### 3. Existing Hooks and Entry Points

**From FFNX_DEVELOPER_GUIDE.md**:

| Hook Function | Address | Purpose | Hot-Swap Opportunity |
|---------------|---------|---------|---------------------|
| `engine_exit` | `0x40FF38` | Cleanup before exit | N/A |
| `swirl_main_loop` | `0x40EBEB` | Battle swirl effect | **Safe point for battle mod swaps** |
| `load_texture` | `0x688415` | Texture loading | **Intercept for texture override changes** |
| `draw_graphics_object` | `0x66E272` | Character rendering | Font/character texture changes |

**Additional Safe Points**:
- Screen transitions (field → field, field → battle)
- Menu entry/exit
- Save/load operations

---

### 4. 7th Heaven's VFS Interception

**How It Works**:
```
Game calls: fopen("data/menu/menu_us.lgp", "rb")
    ↓
EasyHook intercepts at Win32 API level
    ↓
7thWrapperLib queries active mods (by build order)
    ↓
Returns modded file handle OR original file
```

**Critical for Hot-Swapping**:
- **Every file I/O is intercepted dynamically** - not just at startup
- If mod configuration changes, next file request reflects new state
- This means asset hot-swapping could work by:
  1. User triggers mod toggle
  2. Update 7th Heaven's internal mod state
  3. Force asset reload (field change, menu re-entry, etc.)
  4. Next file I/O requests serve new assets automatically

---

## Implementation Tiers

### Tier 1: Quick Wins (Low Effort, High Impact)

| Feature | Effort | Implementation Complexity | User Value |
|---------|--------|--------------------------|------------|
| **HEXT patch hotkey reload** | Low | Just re-call `load_hext_patches()` | High |
| **EXP multiplier toggle** | Low | Single memory address change | Very High |
| **Encounter rate modifier** | Low | Known memory addresses | High |
| **Menu texture swap on menu entry** | Low-Medium | Hook menu initialization | Medium |

**Example Implementation: EXP Multiplier Toggle**
```cpp
// FFNx extension (hypothetical)
void toggle_exp_multiplier(int multiplier) {
    // Address for EXP calculation (example - would need to find actual address)
    const uint32_t EXP_MULTIPLIER_ADDR = 0x9AB058;  // Hypothetical

    uint8_t new_value = (uint8_t)multiplier;
    apply_patch(EXP_MULTIPLIER_ADDR, {new_value});

    ffnx_info("EXP multiplier set to %dx\n", multiplier);
}

// Triggered by hotkey in input.cpp
if (key_pressed(VK_F5) && key_held(VK_SHIFT)) {
    static int multiplier = 1;
    multiplier = (multiplier % 5) + 1;  // Cycle 1x → 5x
    toggle_exp_multiplier(multiplier);
}
```

---

### Tier 2: Moderate Effort

| Feature | Effort | Requirements | Notes |
|---------|--------|--------------|-------|
| **Texture pack switcher (on field change)** | Medium | Extend conditional folder logic | Leverage existing RuntimeVar system |
| **Audio/music mod toggle** | Medium | SoLoud API integration | SoLoud already supports dynamic loading |
| **Font/UI theme swap** | Medium | Extend font infrastructure | FFNx already has multi-page font system |
| **DevTools overlay mod manager** | Medium | ImGui UI development | Foundation exists in `overlay.cpp` |

**Example: Field Background Pack Switcher**

User wants to swap between "Vanilla", "HD Remaster", "Retro Pixel" background packs without restarting game.

**Approach**:
1. Store multiple texture packs in separate directories:
   ```
   mods/Textures/backgrounds/vanilla/
   mods/Textures/backgrounds/hd_remaster/
   mods/Textures/backgrounds/retro_pixel/
   ```

2. Add config variable to FFNx.toml:
   ```toml
   active_background_pack = "hd_remaster"
   ```

3. On field load, check `active_background_pack` and adjust texture search path

4. Provide hotkey to cycle packs (change config var + reload field)

---

### Tier 3: Significant Effort

| Feature | Effort | Challenges | Recommendation |
|---------|--------|-----------|----------------|
| **Live background swap (same field)** | High | VRAM cache invalidation, potential visual glitches | Low priority - field change is acceptable |
| **Model swapping mid-gameplay** | High | Complex object lifecycle management | Low priority - context change is acceptable |
| **Full mod profile switching** | High | Comprehensive state management, file conflicts | Medium priority - valuable for A/B testing |

---

## Technical Details

### HEXT Patch State Tracking

**Challenge**: Currently, FFNx applies HEXT patches at startup with no tracking. To support toggling, need to track:
- Which patches are applied
- Original byte values (for reversal)
- Dependencies between patches

**Proposed Structure**:
```cpp
struct AppliedPatch {
    uint32_t address;
    std::vector<uint8_t> original_bytes;
    std::vector<uint8_t> patched_bytes;
    std::string patch_name;
    bool is_active;
};

std::vector<AppliedPatch> g_active_patches;

void toggle_patch(const char* patch_name) {
    for (auto& patch : g_active_patches) {
        if (patch.patch_name == patch_name) {
            if (patch.is_active) {
                // Restore original bytes
                apply_patch(patch.address, patch.original_bytes);
                patch.is_active = false;
            } else {
                // Re-apply patch
                apply_patch(patch.address, patch.patched_bytes);
                patch.is_active = true;
            }
            return;
        }
    }
}
```

---

### Texture Cache Invalidation

**Current State**:
- FFNx caches textures in VRAM after loading
- From FFNX_DEVELOPER_GUIDE.md: `trace_loaders` config suggests loader awareness

**Required Functions**:
```cpp
// Hypothetical FFNx extensions
void flush_texture_cache_for_field(uint16_t field_id);
void reload_current_field_textures();

// Usage in hot-swap scenario
void user_requested_texture_pack_change(const char* new_pack) {
    // Update FFNx config
    set_active_texture_pack(new_pack);

    // If in a field, force reload
    if (in_field_mode()) {
        flush_texture_cache_for_field(get_current_field_id());
        reload_current_field_textures();
    }

    ffnx_info("Texture pack changed to: %s\n", new_pack);
}
```

---

### Safe Modification Points

**Screen Transitions** (highest safety):
- Field → Field
- Field → Battle
- Battle → Field
- Menu entry/exit

**Execution Flow**:
```
User presses hotkey to toggle mod
    ↓
If safe point (menu, transition):
  → Apply change immediately
    ↓
Else:
  → Queue change for next safe point
  → Display notification: "Mod will apply on next field/battle"
```

---

## Recommendations

### Short-Term (Low-Hanging Fruit)

1. **Add HEXT Hotkey Reload**
   - Implement `reload_hext_patches()` function
   - Bind to F5 or configurable hotkey
   - Display notification on reload
   - **Effort**: 1-2 days
   - **Value**: Immediate QoL for modders testing HEXT patches

2. **EXP/Stats Modifier Presets**
   - Create preset HEXT patches (1x, 2x, 3x, 5x, 10x EXP)
   - Add to DevTools overlay as buttons
   - **Effort**: 2-3 days
   - **Value**: Highly requested feature

3. **Encounter Rate Toggle**
   - Known memory address for encounter rate
   - Simple toggle in overlay
   - **Effort**: 1 day
   - **Value**: Common user request

---

### Medium-Term (Infrastructure Building)

4. **DevTools Overlay Mod Manager**
   - Extend existing `overlay.cpp`
   - Display active mods, HEXT patches
   - Toggle controls
   - **Effort**: 1-2 weeks
   - **Value**: Foundation for all other hot-swap features

5. **Conditional Folder Runtime Toggle**
   - Allow users to manually trigger conditional folder switches
   - Example: Force "Midgar" texture pack even when not in Midgar
   - **Effort**: 1 week
   - **Value**: Testing and content creation workflows

---

### Long-Term (Comprehensive System)

6. **Mod Profile System**
   - Save/load complete mod configurations
   - Switch between "Vanilla+", "HD Remaster", "Difficulty Mod" profiles
   - Handle file conflicts and dependencies
   - **Effort**: 1 month
   - **Value**: User experience transformation

7. **Hot-Swap API for Mod Developers**
   - Expose hot-swap functions to mod developers
   - Allow mods to declare hot-swap support
   - Provide callbacks for pre/post swap
   - **Effort**: 2-3 weeks
   - **Value**: Ecosystem enabler

---

## Conclusion

### Summary Table

| Category | Hot-Swap Feasibility | Current Support | Recommended Priority |
|----------|---------------------|-----------------|---------------------|
| **HEXT memory patches** | ✅ High | Infrastructure exists, needs UI trigger | **HIGHEST** |
| **EXP/stat multipliers** | ✅ High | Subset of HEXT | **HIGHEST** |
| **Menu textures** | ✅ High | Reload on menu entry | High |
| **Audio/music** | ✅ High | SoLoud engine supports dynamic loading | High |
| **Field backgrounds** | ⚠️ Medium-High | Works on field change, needs cache flush for same-field | Medium |
| **Character models** | ⚠️ Medium | Works on context change | Medium |
| **Live mid-scene swaps** | ❌ Low | Would require significant new work | Low |

---

### Key Insights

1. **You're Correct About HEXT Being Low-Hanging Fruit**:
   - The `apply_patch()` infrastructure exists
   - Memory modifications are instant (no asset loading)
   - Just needs UI trigger mechanism
   - EXP multipliers, encounter rates, stat boosts are all trivial to implement

2. **7th Heaven Already Does Runtime Switching**:
   - Conditional folders prove the VFS operates dynamically
   - RuntimeVar system reads game memory in real-time
   - Every file I/O is intercepted at runtime, not just startup
   - Foundation exists - just needs user-facing controls

3. **Asset Hot-Swapping Has Different Tiers**:
   - **Easy**: Swap on context change (field transition, menu entry)
   - **Medium**: Swap same-field (requires cache invalidation)
   - **Hard**: Swap mid-render (complex state management)

4. **Safe Implementation Path**:
   - Start with Tier 1 (HEXT toggles) - immediate value
   - Build DevTools overlay UI - foundation for all features
   - Extend to Tier 2 (texture/audio swaps on transitions)
   - Tier 3 (live swaps) only if user demand justifies complexity

---

### Final Answer to Your Question

**"Can FFNx support hot-swapping of mods?"**

**Yes, absolutely - with varying levels of effort**:

- **HEXT patches (EXP multipliers, etc.)**: Could be implemented **this week**. Just needs hotkey trigger and minimal UI.

- **Asset swaps on transitions**: Could be implemented **within a month**. Leverage existing conditional folder system, add user controls.

- **Live same-scene asset swaps**: Could be implemented **within a few months**. Requires cache invalidation work but architecturally feasible.

**The infrastructure is largely there** - it's primarily a matter of:
1. Adding runtime triggers (hotkeys, overlay UI)
2. Implementing patch/asset state tracking
3. Identifying safe execution points

Your instinct about HEXT being the easiest starting point is **100% correct**. An EXP multiplier toggle could literally be added to FFNx with ~50 lines of code.

---

## References

### Documents Analyzed

1. **FFNX_DEVELOPER_GUIDE.md** (2,310 lines)
   - HEXT patching system (Section 10)
   - Texture override system (Section 7)
   - Hook points and addresses
   - DevTools overlay architecture

2. **7TH_HEAVEN_DEVELOPER_GUIDE.md** (2,173 lines)
   - Virtual File System architecture (Section 2)
   - RuntimeVar conditional loading (Section 8.1)
   - Mod load order system (Section 6)
   - VFS interception mechanism

3. **GameEngine.md** (2,000+ lines analyzed)
   - Background rendering system
   - VRAM block loading
   - Field/battle asset lifecycle

4. **SESSION_CONTEXT_19-28_NAMING_SCREEN.md** (1,251 lines)
   - Memory structure documentation
   - Address references for game state

5. **naming_screen_tables.txt** (362 lines)
   - Character encoding and font systems

---

### Related Files

- `src/hext.cpp`, `src/hext.h` - HEXT patch loader implementation
- `src/patch.cpp`, `src/patch.h` - Memory patching utilities
- `src/overlay.cpp`, `src/overlay.h` - DevTools overlay (ImGui)
- `src/common.cpp` - Texture loading and override system
- `misc/hext/ff7/` - HEXT patch files directory

---

**End of Assessment**

For questions or to discuss implementation, reference this session: `bdf465b1-9f3d-4ab0-8084-40f64c3fc42c`
