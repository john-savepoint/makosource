# FF7 UI Memory Map - Quick Reference Guide

**Version:** 2.0 (Merged Dataset)
**Generated:** 2026-01-21 JST
**Total Addresses:** 2,157

---

## Quick Stats

- **Total UI Addresses:** 2,157
- **Documented (with comments):** 1,865 (86.5%)
- **Categories:** 26
- **Source Files:** 555 HEXT files

---

## Most Common UI Modifications

### 1. Position Adjustments

**Y-Axis (Vertical):** 708 addresses
**X-Axis (Horizontal):** 643 addresses

Common pattern for spacing:
- Middle value: `0xC0`, `0xC9`, or `0xD2`
- First value: `0x6B`
- Third value: Varies by element

Example:
```
006DD534 = D2  // time bar selected spacing Y-Axis
           // Set middle to D2, then first to 6B, then third as value
```

### 2. Menu Boxes

**Total Box Addresses:** 561

Key box types:
- Character boxes (limit, stats, info)
- Menu windows (item, magic, materia)
- Battle UI boxes
- Save/Load boxes

Example:
```
0091D2B0 = XX XX XX XX  // Cait Sith box X, Y, Width, Height
```

### 3. Status Bars

**Total Bar Addresses:** 153

Types:
- HP bars (alive/dead states)
- MP bars (alive/dead states)
- Time bars (selected/charged/charging)
- Limit bars
- Barrier bars (physical/magic)

Example:
```
006DC987 = XX  // HP bars X-Axis
006DC991 = XX  // HP bars Y-Axis
006DC99D = XX  // HP bars length
006DC9A3 = XX  // HP bars height
```

### 4. Cursors

**Total Cursor Addresses:** 241

- Menu cursors
- Selection cursors
- Ghost cursors (disabled options)

Example:
```
006CA914 = XX  // Character selection cursor main menu Y-Axis
```

---

## Battle UI Quick Reference

### Time Bars

| Address | Purpose | Default |
|---------|---------|---------|
| 006DD534 | Time bar selected spacing Y-Axis | D2 |
| 006DD539 | Time bar selected Y-Axis | - |
| 006DD53F | Time bar selected X-Axis | - |
| 006DD50C | Time bar allies selected height | - |
| 006DD553 | Time bar color (charged) RGB | 55 33 00 FF |
| 006DD59B | Time bar color (charging) RGB | 22 16 00 FF |

### HP/MP Bars

| Address | Purpose |
|---------|---------|
| 006DC987 | HP bars X-Axis |
| 006DC991 | HP bars Y-Axis |
| 006DC99D | HP bars length |
| 006DC9A3 | HP bars height |
| 006DCA0B | MP bars X-Axis |
| 006DCA16 | MP bars Y-Axis |
| 006DCA22 | MP bars length |
| 006DCA28 | MP bars height |

### HP/MP Values

| Address | Purpose | Spacing Pattern |
|---------|---------|----------------|
| 006DD86A | Alive HP value spacing Y-Axis | D2, 6B, value |
| 006DD89F | Dead HP value spacing Y-Axis | D2, 6B, value |
| 006DD9BE | Alive MP value spacing Y-Axis | D2, 6B, value |
| 006DD9F3 | Dead MP value spacing Y-Axis | D2, 6B, value |

### Barrier Displays

| Address | Purpose | Spacing Pattern |
|---------|---------|----------------|
| 006DD14F | Barrier header Y-Axis | - |
| 006DD7AB | Barrier boxes palette | - |
| 006DD7BB | Barrier boxes spacing Y-Axis | D2, 6B, value |
| 006DD72F | Barrier physical bar height | - |
| 006DD74C | Barrier physical bar spacing | C0, 6B, value |
| 006DD76D | Barrier magic bar height | - |
| 006DD78A | Barrier magic bar spacing | C9, 6B, value |
| 006DD768 | Barrier magic bar color | 00 00 00 FF |

### Limit Breaks

| Address | Purpose |
|---------|---------|
| 006DD12A | Limit header Y-Axis |
| 006DD6EB | Limit box Y-Axis |
| 006DD6C3 | Limit bar X-Axis |
| 006DD6B9 | Limit bar spacing Y-Axis |
| 006DD693 | Limit bar height |
| 0091D180 | Limit box X, Y, Width, Height |

---

## Menu UI Quick Reference

### Main Menu

| Address | Purpose |
|---------|---------|
| 006CA914 | Character selection cursor Y-Axis |
| 006CAC18 | Avatars Y-axis main menu |

### Magic Menu

| Address | Purpose |
|---------|---------|
| 00921110 | Magic menu description box (X, Y, W, H) |
| 00711676 | Magic box scroll bar Y-Axis |
| 006DFC02 | Magic sub menu text palette color |
| 006E0038 | All sub menu MP needed X-Axis |

### Item Menu

| Address | Purpose |
|---------|---------|
| 007151ED | Item Menu - Use Ghost Cursor X-Axis |
| 00715294 | Item Menu - Use Cursor X-Axis |
| 006DEED1 | Item sub menu text X-Axis |
| 006DED13 | Item sub menu colon/value colors |

### Materia Menu

| Address | Purpose |
|---------|---------|
| 00920EF8 | Materia menu description box (X, Y, W, H) |
| 0071B92D | Materia shop text X-Axis |
| 0071B967 | Materia shop icons X-Axis |

### Status/Cure/Ether Sub-Menus

| Address | Purpose | Spacing |
|---------|---------|---------|
| 006E139C | Names spacing Y-Axis | C9, 6B, value |
| 006E185E | Status spacing Y-Axis | D2, 6B, value |
| 006E1487 | Cure alive HP spacing | D2, 6B, value |
| 006E14BC | Cure dead HP spacing | D2, 6B, value |
| 006E1530 | Cure max HP spacing | D2, 6B, value |
| 006E1626 | Ether alive MP spacing | D2, 6B, value |
| 006E165B | Ether dead MP spacing | D2, 6B, value |
| 006E16CF | Ether max MP spacing | D2, 6B, value |
| 006E168C | Ether MP divider spacing | C0, 6B, value |

### Equipment Menu

| Address | Purpose |
|---------|---------|
| - | (See full dataset for equipment addresses) |

### PHS Menu

| Address | Purpose |
|---------|---------|
| 007015C3 | Avatars Y-axis left box |

---

## Save/Load UI

### Save File Select

| Address | Purpose |
|---------|---------|
| 006F54AB | Save file select box text spacing X-Axis |
| 006FEF51 | Save file select box text X-Axis |
| 006FEEB9 | Save file select cursor spacing X-Axis |
| 006FEEBD | Save file select cursor X-Axis |

### Load Screen

| Address | Purpose |
|---------|---------|
| 00721433 | Load save select box text X-Axis |

---

## Shop UI

### All Shops

| Address | Purpose |
|---------|---------|
| 0071ABEF | Buy/sell/exit sell box ghost cursor X-Axis |
| 0071ACC6 | Buy/sell/exit cursor spacing X-Axis |
| 0071ACCA | Buy/sell/exit cursor X-Axis |

---

## Special Features

### Time Display Extension

| Address | Purpose |
|---------|---------|
| 006CA1F6 | Extend time to 999hr on counters |
| 006CAA02 | Disable flashing on first colon |

### Status Rotation

| Address | Purpose |
|---------|---------|
| 006E1792 | Slow down status rotation speed |

### New Game Screen

| Address | Purpose |
|---------|---------|
| 007217C5 | Refresh font spacing at new game screen |
| 007217D1 | New/continue cursor Y-Axis |
| 0072182E | New/continue continue text Y-Axis |
| 009261C0 | New/continue everything X-Axis |
| 00914008 | New/continue cursor spacing Y-Axis |

### Pause Menu

| Address | Purpose |
|---------|---------|
| 006D84F2 | Pause text Y-Axis |
| 006D851B | Pause box Y-Axis |
| 006D8530 | Pause box X-Axis |

### Field Cursor

| Address | Purpose |
|---------|---------|
| 00631382 | Field cursor X-Axis |

---

## Character-Specific UI

### Cait Sith

| Address | Purpose |
|---------|---------|
| 0091D2B0 | Cait Sith box (X, Y, Width, Height) |

### Tifa

| Address | Purpose |
|---------|---------|
| 0091D34A | Tifa reels box (Y, Width, Height) |

---

## Battle Square

| Address | Purpose |
|---------|---------|
| 006E3C35 | Battle Square status text X-Axis (centered) |
| 006E395B | Battle Square reel height |
| 0041C4C0 | Status display control (Resist) |
| 0091D3F8 | Battle arena box (Width, Height) |

---

## Color Values Reference

### RGB Format

Format: `BB GG RR TT` (Blue, Green, Red, Tint/Alpha)

Examples:
- `55 33 00 FF` - Time bar charged (brownish)
- `22 16 00 FF` - Time bar charging (darker brown)
- `00 00 00 FF` - Barrier magic bar (black)

---

## Spacing System Pattern

Many UI elements use a consistent 3-value spacing system:

**Pattern:** `MIDDLE FIRST THIRD`

Common middle values:
- `C0` (192) - Standard spacing
- `C9` (201) - Slightly wider spacing
- `D2` (210) - Wide spacing

Common first value:
- `6B` (107) - Standard offset

Third value:
- Varies by specific element

**Example usage:**
```
// Allies name spacing
006DD496 = C0  // Middle value
// Then set first to 6B
// Then set third to desired value
```

---

## Memory Regions

### Main UI Region: 0x006C0000 - 0x007F0000

- **0x006C0000 - 0x006D0000:** Main menu UI
- **0x006D0000 - 0x006E0000:** Battle UI elements
- **0x006E0000 - 0x006F0000:** Sub-menu layouts
- **0x006F0000 - 0x007F0000:** Save/Load/Shop UI

### Data Tables: 0x00910000 - 0x00930000

- **0x00910000 - 0x00920000:** Menu box definitions
- **0x00920000 - 0x00930000:** Description boxes

### Special Regions

- **0x00230000:** Opening animation
- **0x00410000:** Status display logic
- **0x00630000:** Field UI
- **0x00720000:** New game screen

---

## Common HEXT Patterns

### Single Byte Value
```
ADDRESS = VALUE
006DD534 = D2
```

### Multi-Byte Value (Little-Endian)
```
ADDRESS = BYTE1 BYTE2 BYTE3 BYTE4
009261C0 = 1E 00 3B 01
```

### Box Dimensions (X, Y, Width, Height)
```
0091D2B0 = XX YY WW HH
```

### RGB Color (Blue, Green, Red, Tint)
```
006DD553 = 55 33 00 FF
```

---

## Best Practices

### Before Modifying Addresses

1. **Backup original values:** Always note the original value before changing
2. **Test incrementally:** Change one value at a time
3. **Document changes:** Keep notes on what each change does
4. **Use safe ranges:** Some addresses have valid ranges

### Common Mistakes to Avoid

1. **Wrong byte order:** FF7 uses little-endian for multi-byte values
2. **Hex vs Decimal:** HEXT files use hexadecimal values
3. **Overlapping elements:** Moving one element may require adjusting others
4. **Missing dependencies:** Some addresses work together (e.g., position + spacing)

### Testing Workflow

1. Create HEXT file with changes
2. Load in 7th Heaven mod manager
3. Launch game and check UI
4. Adjust values and reload
5. Document final working values

---

## Using This Dataset

### For UI Translation Projects

Focus on these categories:
- Text positioning (185 addresses)
- Spacing adjustments (174 addresses)
- Box dimensions (561 addresses)

### For UI Redesign

Focus on these categories:
- Position X/Y (1,351 addresses)
- Colors (35 addresses)
- Bar dimensions (153 addresses)

### For Accessibility Modifications

Focus on these categories:
- Text size/spacing (185 addresses)
- Cursor visibility (241 addresses)
- Color customization (35 addresses)

---

## Additional Resources

- **Full Dataset:** `ff7_ui_memory_map_merged.json`
- **Analysis Report:** `comprehensive_analysis_report.md`
- **New Addresses:** `new_addresses_report.md`
- **Duplicates:** `duplicate_analysis.md`

---

## Contributing

If you discover new addresses or corrections:

1. Document the address, value, and purpose
2. Test in-game to verify behavior
3. Note any dependencies or side effects
4. Submit via GitHub or modding community

---

**Last Updated:** 2026-01-21 JST
**Maintainer:** Session 9bfbe481-e8b6-4c52-868e-5e825185a4b4
