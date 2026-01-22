# FF7 UI Memory Map - Comprehensive Analysis Report

**Generated:** 2026-01-21 JST
**Session:** 9bfbe481-e8b6-4c52-868e-5e825185a4b4
**Version:** 2.0 (Merged Dataset)

---

## Executive Summary

This report documents the analysis and merging of FF7 UI memory addresses from two datasets:

- **Original Dataset:** 1,643 addresses from 497 HEXT files
- **New Dataset:** 516 addresses from 58 HEXT files
- **Merged Total:** 2,157 unique UI memory addresses

### Key Findings

- **514 NEW unique addresses discovered** (99.6% of new dataset was unique)
- **2 duplicate addresses** (already in existing dataset)
- **0 improved metadata** (no overlapping addresses with better descriptions)
- **1,865 addresses with comments** (86.5% documentation rate)
- **292 addresses without comments** (13.5%)
- **1,994 total comments** (0.92 average per address)

---

## Dataset Statistics

### File Analysis

| Metric | Original | New | Total |
|--------|----------|-----|-------|
| HEXT Files | 497 | 58 | 555 |
| Unique Addresses | 1,643 | 516 | 2,157 |
| Duplicates | - | 2 | 2 |
| Coverage Rate | - | 99.6% | - |

### Documentation Quality

| Metric | Count | Percentage |
|--------|-------|------------|
| Addresses with comments | 1,865 | 86.5% |
| Addresses without comments | 292 | 13.5% |
| Total comments | 1,994 | - |
| Avg comments per address | 0.92 | - |

---

## Category Breakdown

The 2,157 addresses are categorized across 26 categories (addresses may belong to multiple categories):

| Rank | Category | Count | Description |
|------|----------|-------|-------------|
| 1 | PositionY | 708 | Vertical positioning (Y-axis) |
| 2 | PositionX | 643 | Horizontal positioning (X-axis) |
| 3 | Box | 561 | Window/box dimensions and properties |
| 4 | Cursor | 241 | Cursor positioning and behavior |
| 5 | MateriaMenu | 225 | Materia menu UI elements |
| 6 | Text | 185 | Text display and formatting |
| 7 | Spacing | 174 | Element spacing and padding |
| 8 | Bar | 153 | Status bars (HP, MP, ATB, etc.) |
| 9 | ItemMenu | 141 | Item menu UI elements |
| 10 | MagicMenu | 126 | Magic menu UI elements |
| 11 | Height | 104 | Element heights |
| 12 | Width | 86 | Element widths |
| 13 | LimitMenu | 83 | Limit break menu UI |
| 14 | Battle | 48 | Battle-specific UI |
| 15 | EquipMenu | 47 | Equipment menu UI |
| 16 | SaveLoadMenu | 44 | Save/Load screen UI |
| 17 | ShopMenu | 43 | Shop interface UI |
| 18 | Avatar | 41 | Character avatar displays |
| 19 | Color | 35 | Color/palette values |
| 20+ | Other | 110+ | Misc categories |

### Category Distribution Visualization

```
PositionY    ████████████████████████████████ 708
PositionX    ████████████████████████████ 643
Box          █████████████████████████ 561
Cursor       ██████████ 241
MateriaMenu  █████████ 225
Text         ████████ 185
Spacing      ███████ 174
Bar          ██████ 153
ItemMenu     ██████ 141
MagicMenu    █████ 126
```

---

## Top 50 Most Interesting New Discoveries

### Battle UI Elements

| Address | Description |
|---------|-------------|
| 006DD0C3 | Hide original name header |
| 006DD14F | Barrier header Y-Axis |
| 006DD534 | Time bar selected spacing Y-Axis |
| 006DD553 | Time bar color allies, charged (RGB values) |
| 006DD580 | Time bar allies charged spacing Y-Axis |
| 006DD5D1 | Time bar allies charging spacing Y-Axis |
| 006DD7BB | Barrier boxes spacing Y-Axis |
| 006DD86A | Alive HP value spacing Y-Axis |
| 006DD89F | Dead HP value spacing Y-Axis |
| 006DD9BE | Alive MP value spacing Y-Axis |
| 006DD9F3 | Dead MP value spacing Y-Axis |

### Menu Positioning

| Address | Description |
|---------|-------------|
| 006CA914 | Character selection cursor main menu |
| 006CAC18 | Avatars Y-axis main menu |
| 007217D1 | New/continue cursor Y-Axis |
| 0072182E | New/continue continue text Y-Axis |
| 009261C0 | New/continue everything X-Axis |

### Magic/Materia UI

| Address | Description |
|---------|-------------|
| 006DFC02 | Magic sub menu text support symbol palette color |
| 006DE7A8 | Command box text support symbol palette color |
| 006E0038 | All sub menu MP needed X-Axis (centered) |
| 006E139C | Status/cure/ether sub menu names spacing Y-Axis |
| 006E1487 | Cure sub menu alive HP spacing Y-Axis |
| 006E14BC | Cure sub menu dead HP spacing Y-Axis |
| 006E1530 | Cure sub menu max HP spacing Y-Axis |
| 006E1626 | Ether sub menu alive MP spacing Y-Axis |
| 006E165B | Ether sub menu dead MP spacing Y-Axis |
| 006E16CF | Ether sub menu max MP spacing Y-Axis |
| 006E168C | Ether sub menu MP divider spacing Y-Axis |
| 006E185E | Status sub menu status spacing Y-Axis |
| 006E1792 | Slow down status rotation |

### Character Boxes

| Address | Description |
|---------|-------------|
| 0091D180 | Limit box X-Axis, Y-Axis, View Width, View Height |
| 0091D2B0 | Cait Sith box X-Axis, Y-Axis, Viewable Width, Viewable Height |

### Time Display

| Address | Description |
|---------|-------------|
| 006CA1F6 | Extend time to 999hr on counters |
| 006CAA02 | Disable flashing on first colon, only on seconds |

### Materia Colors

| Address | Description |
|---------|-------------|
| 0070B7E7 | Purple materia (MEGAALL/PREEMPT/COUNTER/LONG/CHOCOBO/AWAY/LURE/etc.) |
| 0070B7EC | Purple materia alternate |

### Battle Square

| Address | Description |
|---------|-------------|
| 006E3C35 | Battle Square status text X-Axis (centered regardless of length) |
| 0041C4C0 | Status display control (Resist intentionally not shown) |

### Scroll Bars

| Address | Description |
|---------|-------------|
| 00711676 | Magic box scroll bar Y-Axis |

### Font Spacing

| Address | Description |
|---------|-------------|
| 007217C5 | Refresh font spacing at new game screen |

---

## Address Range Analysis

### Memory Regions

The addresses span several distinct memory regions:

| Region Start | Region End | Count | Primary Purpose |
|--------------|------------|-------|----------------|
| 0x0023xxxx | 0x0023xxxx | 1 | Opening animation |
| 0x0041xxxx | 0x0041xxxx | 1 | Status display control |
| 0x006Cxxxx | 0x006Exxxx | 200+ | Menu UI elements |
| 0x0070xxxx | 0x0071xxxx | 50+ | Materia/Magic UI |
| 0x0072xxxx | 0x0072xxxx | 10+ | New game screen |
| 0x0091xxxx | 0x0092xxxx | 300+ | Battle/menu boxes |

### Highest Concentration Areas

**0x006DD000 - 0x006DE000 region (Battle UI)**
- Contains most battle-related UI addresses
- HP/MP bars, time bars, status displays
- Character names and avatars

**0x006E0000 - 0x006E2000 region (Sub-menus)**
- Magic sub-menu layouts
- Item sub-menu layouts
- Status/cure/ether menu spacing

**0x0091D000 - 0x0092xxxx region (Menu Boxes)**
- Menu box dimensions and positions
- Character selection boxes
- Viewable area calculations

---

## Notable Discoveries

### 1. Comprehensive Battle UI Coverage

The new dataset significantly expands battle UI documentation, including:
- Time bar customization (color, spacing, positioning)
- HP/MP value positioning for alive/dead states
- Barrier and status effect displays
- Character avatar positioning

### 2. Menu Spacing System

Discovered a consistent spacing pattern used across menus:
- **Middle value** (often 0xC0, 0xC9, or 0xD2)
- **First value** (often 0x6B)
- **Third value** (variable based on menu type)

Example: `time bar selected spacing Y-Axis - set middle to D2, then first to 6B, then third as value`

### 3. Color System

Found RGB color value addresses for UI elements:
- Format: `RR GG BB TT` (Red, Green, Blue, Tint/Alpha)
- Example: `55 33 00 FF` for time bar charged color

### 4. Extended Time Display

Discovered addresses for extending game time display:
- 006CA1F6: Extends time counter to 999 hours
- 006CAA02: Controls colon flashing behavior

### 5. Status Rotation Control

006E1792: Controls status effect rotation speed in menus
- Can slow down rotation for better visibility
- Speeds up when many statuses active

---

## Data Quality Assessment

### Strengths

1. **High uniqueness rate:** 99.6% of new addresses were unique
2. **Good documentation:** 86.5% of addresses have descriptions
3. **Consistent formatting:** HEXT files follow standard format
4. **Contextual comments:** Many comments include implementation details

### Weaknesses

1. **292 addresses without comments** (13.5%)
2. **Some cryptic descriptions:** e.g., "{ character selection cursor main menu"
3. **Inconsistent comment detail:** Some very detailed, others minimal
4. **No validation data:** Can't verify if addresses are correct without testing

### Recommendations for Future Work

1. **Add validation tests:** Test each address in-game to confirm behavior
2. **Standardize comment format:** Create template for address documentation
3. **Add value range documentation:** Document min/max safe values for each address
4. **Create visual reference:** Screenshots showing what each address controls
5. **Document dependencies:** Note which addresses must be changed together

---

## File Sources

### New Dataset File Distribution

| Mod Package | Files | Purpose |
|-------------|-------|---------|
| Tsunamods Retouch 0.83 | 24 | UI retouch mod |
| SYW Unified Menus | Multiple | Unified menu system |
| Modern Icons for ESUI | Multiple | Icon replacements |
| Wolfman Avatars | Multiple | Character avatar mods |
| MiloLeonhart Avatars | Multiple | Alternative avatars |
| Prelude Credits (Strayoff) | Multiple | Credit screen mods |
| Prelude Credits (Grimmy) | Multiple | Alternative credits |

---

## Merged Dataset Structure

Each address entry contains:

```json
{
  "address": "006DD534",
  "address_decimal": 7198004,
  "primary_purpose": "time bar selected spacing Y-Axis",
  "all_comments": [
    "time bar selected spacing Y-Axis - set middle to D2, then first to 6B, then third as value"
  ],
  "categories": ["Bar", "Spacing", "PositionY"],
  "value_min": 0,
  "value_max": 210,
  "value_count": 1,
  "example_values": ["D2"],
  "occurrence_count": 1,
  "example_files": ["169/01/hext/start.txt"]
}
```

---

## Conclusion

This analysis successfully merged two datasets, discovering **514 new UI memory addresses** and expanding the total documented addresses to **2,157**. The new dataset provides particularly valuable coverage of:

1. Battle UI elements
2. Menu spacing systems
3. Color customization
4. Time display extensions
5. Sub-menu layouts

The merged dataset represents the most comprehensive FF7 UI memory address documentation currently available, with 86.5% of addresses having descriptive comments.

---

## Next Steps

1. **Validate addresses:** Test in-game to confirm behavior
2. **Create UI editor:** Build tool using this dataset
3. **Add visual reference:** Screenshot each UI element
4. **Document safe ranges:** Test min/max values
5. **Create HEXT generator:** Tool to generate custom UI patches

---

**Dataset Files:**
- Original: `ff7_ui_memory_map.json` (1,643 addresses)
- New discoveries: `new_addresses_report.md`
- Merged: `ff7_ui_memory_map_merged.json` (2,157 addresses)
- This report: `comprehensive_analysis_report.md`

**Total Documentation Size:**
- 2,157 addresses
- 1,994 comments
- 26 categories
- 555 source files analyzed
