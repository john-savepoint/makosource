# 4. ASSET SPECIFICATIONS & DATA STRUCTURES

## 4.1 Font Texture Manifest

**Required Assets Location:** `mods/Textures/menu/`

| Filename | Encoding Range | Content Description | Dimensions | Grid Layout |
|----------|----------------|---------------------|------------|-------------|
| `jafont_1.png` | `0x00-0xE6` | Hiragana, Katakana, Numbers, ASCII, Punctuation | 1024×1024 | 16×16 grid (64px glyphs) |
| `jafont_2.png` | `0xFA + [0x00-0xFF]` | Kanji Set A (Battle/Skill/Magic terms) | 1024×1024 | 16×16 grid |
| `jafont_3.png` | `0xFB + [0x00-0xFF]` | Kanji Set B (Character names, locations) | 1024×1024 | 16×16 grid |
| `jafont_4.png` | `0xFC + [0x00-0xFF]` | Kanji Set C (Dialogue, common words) | 1024×1024 | 16×16 grid |
| `jafont_5.png` | `0xFD + [0x00-0xFF]` | Kanji Set D (Rare Kanji, proper nouns) | 1024×1024 | 16×16 grid |
| `jafont_6.png` | `0xFE + [0x00-0xFF]` | Kanji Set E (Extended set, special characters) | 1024×1024 | 16×16 grid |

**Texture Specifications:**
- **Format:** PNG (RGBA8888 recommended for best compatibility)
- **Resolution:** 1024×1024 pixels (enforced by FFNx)
- **Grid:** 16×16 cells = 256 total cells per texture
- **Cell Size:** 64×64 pixels per glyph
- **Color Depth:** 32-bit RGBA (supports anti-aliasing and drop shadows)
- **UV Mapping:** Standard (0,0) = top-left, (1,1) = bottom-right
- **Coordinate Calculation:**
  - Given character index `idx` (0-255):
    - `grid_x = idx % 16`
    - `grid_y = idx / 16`
    - `uv_x0 = grid_x * (1.0 / 16.0)`
    - `uv_y0 = grid_y * (1.0 / 16.0)`
    - `uv_x1 = uv_x0 + (1.0 / 16.0)`
    - `uv_y1 = uv_y0 + (1.0 / 16.0)`

## 4.2 Character Mapping Data

**Master Mapping Table:** `character_tables/character_map_accurate.csv`

**Structure:**
```csv
texture,index,character,unicode
jafont_1,0,バ,U+30D0
jafont_1,1,ば,U+3070
jafont_1,2,ビ,U+30D3
jafont_1,3,び,U+3073
...
jafont_2,0,必,U+5FC5
jafont_2,1,殺,U+6BBA
...
jafont_6,255,,
```

**Fields:**
- `texture`: Which PNG file (`jafont_1` through `jafont_6`)
- `index`: Cell position within the 16×16 grid (0-255)
- `character`: The actual Unicode character (for human readability)
- `unicode`: Unicode code point in U+XXXX format

**Total Characters Mapped:** 1,331 (as of latest mapping)

**Usage Example (Text Encoding):**
```python
# To encode the character '私' (watashi = "I"):
# 1. Look up in CSV: '私' = U+79C1
# 2. Find row: texture=jafont_2, index=12
# 3. Encode as: 0xFA 0x0C
#    - 0xFA = switch to Page 1 (jafont_2)
#    - 0x0C = character index 12 (hex)
```

## 4.3 Japanese File Structure (Critical Differences)

**Directory Layout (ff7_ja.exe expects):**
```
FF7_JA/
├── ff7_ja.exe
├── data/
│   ├── lang-ja/              # ← Japanese-specific path
│   │   ├── menu_ja.lgp       # ← Contains jafont_*.tex
│   │   ├── jfleve.lgp        # ← TYPO! Missing 'l' (should be flevel)
│   │   ├── battle_ja.lgp
│   │   └── movies/
│   │       ├── eidoslogo.avi
│   │       └── ...
│   ├── cd/                   # Shared data
│   └── ...
├── AF3DN.P                   # Japanese driver (proprietary)
└── ...
```

**vs. English File Structure:**
```
FF7_EN/
├── ff7.exe
├── data/
│   ├── menu/
│   │   └── menu_us.lgp       # ← English path
│   ├── field/
│   │   └── flevel.lgp        # ← Correct spelling
│   ├── battle/
│   │   └── battle.lgp
│   └── movies/
│       └── ...
└── ...
```

**Critical File Name Differences (MUST Handle):**

| Component | English Filename | Japanese Filename | Notes |
|-----------|------------------|-------------------|-------|
| Menu/Font | `menu_us.lgp` | `menu_ja.lgp` | Contains font textures |
| Field Maps | `flevel.lgp` | `jfleve.lgp` | **TYPO!** Missing 'l' in Japanese |
| Battle | `battle.lgp` | `battle_ja.lgp` | Standard `_ja` suffix |
| Movies Path | `data/movies/` | `data/lang-ja/movies/` | Nested in lang-ja/ |
| Data Path | `data/` | `data/lang-ja/` | Base path difference |

**Why This Matters:**
- `ff7_ja.exe` requests these specific paths via registry queries
- If FFNx returns English paths, the game crashes immediately
- Our registry virtualization (Section 7.2) must handle this

---
