# English→German String Mapping for FF7 HEXT Patch

**Created:** 2026-01-05
**Session:** Current session
**Purpose:** Map 767 English menu strings to their German equivalents by semantic content matching

## Files

- **Input (English):** `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt`
  - 767 strings extracted from ff7_en.exe using touphScript indices
  - Format: `[INDEX] OFFSET LENGTH TYPE | TEXT | HEX_BYTES`

- **Input (German):** `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_offsets.csv`
  - 895 non-empty strings extracted from ff7_de.exe
  - Format: CSV with index, offset, text, padding_bytes, text_bytes, total_bytes

- **Output:** `english_german_mapping.csv`
  - Format: `en_index,en_offset,en_text,de_offset,de_text,confidence,match_method`

- **Script:** `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/scripts/map_english_german.py`

## Mapping Results

```
Total mappings: 767/767 (100% coverage)
Successfully mapped: 606/767 (79.0%)
Unmapped: 161/767 (21.0%)
```

### By Confidence Level

| Confidence | Count | Percentage | Description |
|------------|-------|------------|-------------|
| exact      | 66    | 8.6%       | Identical text match (ATB, Sound, Mono, etc.) |
| high       | 107   | 14.0%      | Known translation pairs + manual group mappings |
| medium     | 433   | 56.5%      | Context-based matching + keyboard block |
| none       | 161   | 21.0%      | No match found |

### By Match Method

| Method         | Count | Percentage | Description |
|----------------|-------|------------|-------------|
| manual_group   | 24    | 3.1%       | Manually mapped known groups (quit dialog, keyboard labels) |
| keyboard_block | 139   | 18.1%      | Keyboard/joystick/mouse keys (packed binary structure) |
| exact          | 66    | 8.6%       | Exact text matches |
| translation    | 83    | 10.8%      | Known translation dictionary matches |
| context        | 294   | 38.3%      | Context-based matching using nearby strings |
| none           | 161   | 21.0%      | No match found |

## Mapping Strategy

### Pass 0: Manual Group Mappings (24 + 139 = 163 mappings)

**Quit Dialog (English 0-4 → German 0-4):**
- "Do you want to quit" → "Möchten Sie Final"
- "playing Final Fantasy VII" → "Fantasy VII verlassen und"
- "and return to Windows?" → "zu Windows zurückkehren?"
- "Yes" → "Ja"
- "No" → "Nein"

**Keyboard Labels (English 61-76 → German 86-101):**
- [OK], [CANCEL], [MENU], [SWITCH], [PAGEUP], [PAGEDOWN], [CAMERA], [TARGET], [ASSIST], [START], [UP], [DOWN], [LEFT], [RIGHT], KEYBOARD, JOYSTICK

**Press Messages (English 58-60 → German 82-85):**
- "Press [CANCEL] to end." → "Mit [ABBRECHEN] beenden."
- "Press [OK] to configure a key." → "Drücken Sie auf [O.K.] um die"
- "Now press the new key." → "Bitte neue Taste drücken"

**Keyboard/Joystick/Mouse Block (English 77-215 → German 102):**
- All 139 keyboard key names, joystick buttons, and mouse buttons map to a single 3276-byte packed binary structure in German
- This includes: ESCAPE, 1-0, MINUS, EQUALS, TAB, Q-P, function keys, numpad, mouse buttons, joystick buttons, etc.
- German has these embedded in one large data block with different encoding

### Pass 1: Exact Matches (66 mappings)

Case-insensitive exact text matches:
- ATB, Sound, Mono, Stereo, Normal, Pause, Gil, Materia, PHS, etc.

### Pass 2: Known Translation Matches (83 mappings)

Using translation dictionary with 95+ known pairs:
- Window color → Fensterfarbe
- Battle speed → Kampftempo
- Battle message → Kampfmeldung
- Item → Objekt
- Magic → Zauber
- Save → Speichern
- Quit → Verlassen
- Status effects: Poison → Gift, Sleep → Schlaf, Confusion → Verwirrung
- Element terms: Attack → Angreifen, Defend → Verteidigen, Absorb → Absorbieren
- Stats: Strength → Stärke, Dexterity → Geschick, Vitality → Vitalität

### Pass 3: Context-Based Matching (294 mappings)

- Uses already-mapped strings as anchors
- Looks for nearby German strings (within 5 positions)
- Matches based on relative position and length similarity
- Particularly effective for sequential menu options and config settings
- Iterative process (10 iterations max) to propagate mappings

### Pass 4: Fill Remaining (161 unmapped)

Strings that couldn't be matched:
- Character names (proper nouns): CLOUD, BARRET, TIFA, AERIS, RED XIII, YUFFIE, CAIT SITH, VINCENT, etc.
- Some specialized menu items not in translation dictionary
- Items requiring manual review

## Key Insights

### Structural Differences

1. **Keyboard Data Packing:**
   - English: Individual strings for each key (77-215)
   - German: Single packed binary block (index 102, 3276 bytes)
   - Solution: Map all English keyboard strings to German block with note

2. **Group Order:**
   - Within logical groups (config menu, main menu), strings ARE in same order
   - BUT groups themselves may be at different positions
   - Cannot assume English index N = German index N

3. **Text Splitting:**
   - Some long English strings split across multiple German entries
   - Example: "Press [OK] to configure a key." split into two German strings

### Translation Patterns

- German text generally longer than English (compound words)
- Menu shortcuts preserved: [O.K.], [ABBRECHEN], [MENÜ]
- Technical terms often similar: Controller/Kontroller, Cursor/Cursor
- Status effects have German equivalents: Poison/Gift, Fury/Zorn

## Usage Notes

### For HEXT Patch Creation

1. **High Confidence (exact + high):** Use directly (173 mappings, 22.5%)
2. **Medium Confidence:** Review context, especially keyboard block (433 mappings, 56.5%)
3. **None:** Requires manual translation or decision to skip (161 mappings, 21.0%)

### Keyboard Block Handling

All English strings 77-215 point to German offset 0x591508 with note:
```
[KEYBOARD_DATA_BLOCK: key_name]
```

This indicates the German equivalent is embedded in the binary keyboard structure. When creating HEXT patches, you may need to:
- Parse the German keyboard block structure
- Extract individual key names
- Map to correct positions in English structure

### Character Names

Character names (indices 700+) are mostly unmapped as they are proper nouns. Decision needed:
- Keep English names in patch?
- Use official German localization names?
- Create custom translations?

## Quality Assurance

### Spot Checks Performed

✅ Quit dialog (0-4): All correctly mapped
✅ Config menu (5-37): Sequential mapping preserved
✅ Main menu (38-48): Key items correctly translated
✅ Keyboard labels (61-76): All correctly mapped
✅ Status effects: Known translations applied

### Known Issues

1. **Keyboard block:** Requires special handling in HEXT creation
2. **Split strings:** Some English strings map to partial German strings
3. **Context matches:** Medium confidence items should be spot-checked
4. **Character names:** Large unmapped block at end (intentional)

## Recommendations

### For Next Steps

1. **Manual review:** Check all "medium" confidence context matches (294 items)
2. **Character names:** Decide on translation strategy for proper nouns
3. **Keyboard block:** Develop parser for German binary keyboard structure
4. **Split strings:** Identify and document all split translations
5. **HEXT creation:** Use high confidence mappings first, validate with game testing

### For Improvement

1. **Fuzzy matching:** Add Levenshtein distance for similar spellings
2. **Phrase matching:** Detect partial phrase matches (not just full string)
3. **Positional hints:** Use offset proximity as additional matching hint
4. **German structure analysis:** Deep dive into keyboard block structure
5. **Validation:** Cross-reference with official German FF7 if available

## Statistics Summary

```
Total English strings: 767
Total German strings: 895

Mapping Coverage:
├─ Successfully mapped: 606 (79.0%)
│  ├─ Exact matches:      66 ( 8.6%)
│  ├─ High confidence:   107 (14.0%)
│  └─ Medium confidence: 433 (56.5%)
└─ Unmapped:           161 (21.0%)

Match Methods:
├─ Manual groups:       24 ( 3.1%) - Hand-curated known groups
├─ Keyboard block:     139 (18.1%) - Binary structure mapping
├─ Exact matches:       66 ( 8.6%) - Identical text
├─ Translation dict:    83 (10.8%) - Known translations
├─ Context-based:      294 (38.3%) - Position-based matching
└─ None:               161 (21.0%) - Requires manual work
```

## Credits

- **Mapping script:** Python 3 with semantic content matching
- **English extraction:** touphScript indices
- **German extraction:** Clean offset CSV
- **Translation dictionary:** 95+ known English↔German pairs
- **Context algorithm:** Iterative neighbor-based propagation
