# FF7 UI Memory Map Analysis

**Version:** 2.0 (Merged Dataset)
**Last Updated:** 2026-01-21 JST
**Session:** 9bfbe481-e8b6-4c52-868e-5e825185a4b4

This directory contains a comprehensive analysis of Final Fantasy VII UI memory addresses extracted from HEXT patch files.

## 🎯 Quick Access

**Start here:** [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Practical guide for using the addresses
**Full analysis:** [comprehensive_analysis_report.md](./comprehensive_analysis_report.md) - Detailed findings

## 📊 Dataset Overview

### Current Dataset (Version 2.0)

- **Total Unique Addresses:** 2,157
- **Total HEXT Files Analyzed:** 555 (497 original + 58 new)
- **Documentation Coverage:** 86.5% (1,865 addresses with comments)
- **Total Comments:** 1,994
- **Categories:** 26

### Version History

**v2.0 (2026-01-21):**
- Merged new dataset of 58 HEXT files
- Added 514 new unique addresses (99.6% discovery rate)
- Total addresses: 2,157
- Enhanced battle UI coverage
- Discovered spacing pattern system

**v1.0 (2026-01-20):**
- Initial analysis of 497 HEXT files
- Total addresses: 1,643

## 📁 Files

### Primary Dataset Files

| File | Size | Description |
|------|------|-------------|
| `ff7_ui_memory_map_merged.json` | 1.3 MB | **Current dataset** - All 2,157 addresses with full metadata |
| `ff7_ui_memory_map.json` | 1.1 MB | Original dataset (1,643 addresses) |

### Documentation Files

| File | Size | Purpose |
|------|------|---------|
| `QUICK_REFERENCE.md` | 11 KB | **Start here** - Practical usage guide with examples |
| `comprehensive_analysis_report.md` | 12 KB | Detailed analysis of findings and discoveries |
| `new_addresses_report.md` | 1.6 KB | Summary of new discoveries from v2.0 |
| `duplicate_analysis.md` | 246 B | Duplicate address analysis |
| `memory_regions_summary.md` | 9.3 KB | Memory region distribution analysis (v1.0) |

### Tools

| File | Description |
|------|-------------|
| `analyze_new_hext.py` | Python script for analyzing and merging HEXT datasets |

## 🎮 Categories

The 2,157 addresses are organized into 26 categories:

| Category | Count | Description |
|----------|-------|-------------|
| PositionY | 708 | Vertical positioning |
| PositionX | 643 | Horizontal positioning |
| Box | 561 | Window/box dimensions |
| Cursor | 241 | Cursor positioning |
| MateriaMenu | 225 | Materia menu UI |
| Text | 185 | Text display |
| Spacing | 174 | Element spacing |
| Bar | 153 | Status bars (HP/MP/ATB) |
| ItemMenu | 141 | Item menu UI |
| MagicMenu | 126 | Magic menu UI |
| + 16 more categories | - | See QUICK_REFERENCE.md |

## 🔍 Key Discoveries (v2.0)

1. **Battle UI Expansion:** 100+ new addresses for HP/MP bars, time bars, and barriers
2. **Spacing Pattern System:** Consistent 3-value pattern (middle/first/third) discovered
3. **Color Customization:** RGB values for battle UI elements
4. **Time Extensions:** Addresses to extend time display to 999 hours
5. **Character-Specific UI:** Cait Sith, Tifa reels box addresses
6. **Status Rotation Control:** Adjust status effect display speed

## 📖 Usage Examples

### Finding Position Addresses

```python
import json

with open('ff7_ui_memory_map_merged.json', 'r') as f:
    data = json.load(f)

# Find all position-related addresses
for addr, info in data.items():
    if 'PositionX' in info['categories']:
        print(f"{addr}: {info['primary_purpose']}")
```

### Filter by Category

```python
# Get all battle-related addresses
battle_addrs = {
    addr: info for addr, info in data.items()
    if 'Battle' in info['categories'] or 'Bar' in info['categories']
}
```

### Generate HEXT Patch

```hext
// Example HEXT patch to adjust time bar
006DD534 = D2  // Time bar selected spacing Y-Axis
006DD539 = 50  // Time bar selected Y-Axis
006DD53F = 30  // Time bar selected X-Axis
```

## 🎯 Use Cases

### UI Translation Projects

Focus on:
- Text positioning (185 addresses)
- Spacing adjustments (174 addresses)
- Box dimensions (561 addresses)

See: `QUICK_REFERENCE.md` → "For UI Translation Projects"

### UI Redesign

Focus on:
- Position X/Y (1,351 addresses)
- Colors (35 addresses)
- Bar dimensions (153 addresses)

See: `QUICK_REFERENCE.md` → "For UI Redesign"

### Accessibility Modifications

Focus on:
- Text size/spacing (185 addresses)
- Cursor visibility (241 addresses)
- Color customization (35 addresses)

See: `QUICK_REFERENCE.md` → "For Accessibility Modifications"

## 🔧 For FF7 Ultima Integration

This dataset is designed for integration with the FF7 Ultima UI Editor module:

1. **Load JSON:** Import `ff7_ui_memory_map_merged.json`
2. **Category Filter:** Use categories for UI organization
3. **Search:** Use `primary_purpose` for text search
4. **Validation:** Use `value_min`/`value_max` for safe ranges
5. **Export:** Generate HEXT patches from user modifications

## 🧪 Data Quality

- **86.5% Documentation Rate:** 1,865 addresses have descriptive comments
- **99.6% Uniqueness:** Only 2 duplicates found in new dataset
- **26 Categories:** Comprehensive categorization for easy filtering
- **Multi-source:** Data from 555 HEXT files across multiple mod projects

## 📚 Additional Resources

- [FF7 HEXT Format Specification](https://github.com/tsunamods-codes/7th-Heaven)
- [FF7 Memory Structure](https://wiki.qhimm.com/view/FF7/Memory_addresses)
- [FF7 Modding Community](https://discord.gg/ff7modding)

## 🤝 Contributing

To contribute new addresses or corrections:

1. Test address in-game to verify behavior
2. Document purpose, value range, and any dependencies
3. Submit via pull request or issue
4. Include HEXT file source if available

## 📜 Version History

**v2.0 (2026-01-21):**
- Added 514 new addresses from 58 HEXT files
- Total: 2,157 addresses
- Discovered spacing pattern system
- Enhanced battle UI coverage

**v1.0 (2026-01-20):**
- Initial release
- 1,643 addresses from 497 HEXT files

## 📄 License

This dataset is compiled from public HEXT patch files distributed with FF7 mods. Individual mod credits retained in `example_files` field of each address entry.

---

**Generated by:** Claude Code
**Session:** 9bfbe481-e8b6-4c52-868e-5e825185a4b4
