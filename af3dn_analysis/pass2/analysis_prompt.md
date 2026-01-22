# AF3DN.P Pass 2: Detailed Analysis of Key Japanese Text Functions

## Context

You are analyzing the **core Japanese text rendering and naming screen functions** from Square Enix's AF3DN.P graphics driver for Final Fantasy VII PC (2013 Japanese eStore version).

These functions implement:
1. **Naming Screen** - Character name entry UI with Hiragana/Katakana/EISUU pages
2. **Japanese Text Rendering** - Shift-JIS text display with 6 font texture pages
3. **Character Table Lookup** - Mapping cursor position to character codes

## Your Task

For each function, provide:

1. **Detailed Algorithm Description** - Step-by-step what the function does
2. **Data Structure Analysis** - What structures/arrays it accesses and their layout
3. **Call Graph** - What functions it calls and is called by
4. **Key Variables** - Important globals and their purpose
5. **FFNx Porting Notes** - How this could be implemented in FFNx mod

## Known Information

### Key Globals
- `dword_1004CB78` - JP/EN locale flag (0=EN, non-zero=JP)
- `dword_1004CCF8` - Naming screen state/data pointer
- `dword_1004CBBC` - Cached character ID from last lookup
- `unk_10051880` - Character table array (5-DWORD structs, 20 bytes each)
- `dword_1004CCD0-CCE4` - Font texture page pointers (pages 0x00, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE)
- `dword_10050660` - Function pointer for state initialization

### Naming Screen Layout
- 3 pages: Hiragana (9×10), Katakana (9×10), EISUU (5×10)
- Sidebar buttons: スペース, さくじょ, けってい, デフォルト, キャンセル
- Character data at offset 0x410B8 (Hiragana), 0x41112 (Katakana), 0x4116C (EISUU) in JP binary

### Font Texture Pages
- jafont_1 (0x00-0xFF): Kana, numbers, Latin, symbols
- jafont_2-6 (0xFA-0xFE XX): Kanji pages

## Output Format

For each function:

```markdown
## Function: sub_XXXXXXXX
**Suggested Name**: descriptive_name

### Algorithm
1. Step one...
2. Step two...

### Data Structures
- `offset+N`: Description of field
- Array at `address`: Layout and purpose

### Call Graph
- **Calls**: func1, func2
- **Called by**: parent_func

### Key Variables
- `dword_XXXXXXXX`: Purpose

### FFNx Porting Notes
How to implement this in FFNx...
```

Analyze ALL functions in the provided code.
