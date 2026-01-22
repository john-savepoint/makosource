# FF7 Developer Markers Analysis

**Created:** 2026-01-06 15:35 JST (Tuesday)
**Session-ID:** 85c271e2-f1ef-4bb6-b5dc-b212b2694001
**Author:** John Zealand-Doyle

---

## Executive Summary

The `ff7_de.exe` (and likely all FF7 executables) contain embedded developer debug markers like "START OF MENU SYSTEM!!!" and "END OF MENU SYSTEM!!!".

**IMPORTANT: These markers are NOT actual boundaries for string data.** They are leftover debug comments from development and do NOT define where menu strings start or end.

---

## Developer Markers Found

| Marker | Offset | Region Size | Contents |
|--------|--------|-------------|----------|
| START OF CREDITS!!! | 0x58F700 | 24 bytes | Just the marker text |
| END OF CREDITS!!! | 0x58F718 | - | - |
| START OF MENU SYSTEM!!! | 0x591024 | 28 bytes | Just the marker text |
| END OF MENU SYSTEM!!! | 0x591040 | - | - |
| START OF WORLD MAP!!! | 0x55CA65 | 36 bytes | Just the marker text |
| END OF WORLD MAP!!! | 0x55CA89 | - | - |

---

## The Problem: Markers Don't Define Boundaries

### What We Expected

When we found "START OF MENU SYSTEM!!!" at 0x591024 and "END OF MENU SYSTEM!!!" at 0x591040, we initially thought these defined where menu strings were located.

### What We Found

**The markers are embedded WITHIN the string table, but actual menu strings extend far beyond them:**

```
STRING DISTRIBUTION (529 clean German strings):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

0x58F700  ← START OF CREDITS marker
0x58F718  ← END OF CREDITS marker
           (no strings in credits region)

0x58FBB0  ← FIRST MENU STRING: "Möchten Sie Final"
    │
    │  79 strings BEFORE the "MENU SYSTEM" marker
    │  Includes: Exit Dialog, Config Menu, Main Menu, Status Screen
    │
0x590E20  ← Last string before marker: "Traurigk."

0x591024  ← START OF MENU SYSTEM!!! marker ─┐
0x591040  ← END OF MENU SYSTEM!!! marker  ──┴─ ZERO strings inside!

0x591094  ← First string AFTER marker: "Drücken Sie auf [O.K.]..."
    │
    │  450 strings AFTER the "END OF MENU SYSTEM" marker!
    │  Includes: Keyboard Config, Battle, Elements, Attributes,
    │            Materia, Items, Dialog Responses, Shops, Save/Load
    │
0x59D150  ← LAST MENU STRING: "Level"
```

### Statistics

- **Strings BEFORE "MENU SYSTEM" marker:** 79 (15%)
- **Strings INSIDE "MENU SYSTEM" marker region:** 0 (0%)
- **Strings AFTER "END OF MENU SYSTEM" marker:** 450 (85%)

---

## Why This Matters

### DO NOT use these markers to:
1. Define extraction boundaries for menu strings
2. Assume strings outside markers are "not menu content"
3. Limit searches to the marker-defined region

### The markers appear to be:
1. Leftover debug comments from Square's development
2. Possibly indicating a planned region that wasn't enforced
3. Perhaps marking a specific subsystem that later expanded
4. Remnants of the original Japanese source code structure

---

## Actual Menu String Boundaries

For German (`ff7_de.exe`):

| Description | Offset | Example String |
|-------------|--------|----------------|
| First menu string | 0x58FBB0 | "Möchten Sie Final" |
| Last menu string | 0x59D150 | "Level" |
| **Total span** | **~54,688 bytes** | |

The actual boundaries should be determined by:
1. Following 0xFF terminators sequentially
2. Analyzing byte patterns for valid FF7-encoded text
3. NOT by relying on developer marker positions

---

## Raw Hex Context

What the "MENU SYSTEM" marker region actually looks like:

```
0x591020: T...START OF MENU SYSTEM!!!.....
0x591040: END OF MENU SYSTEM!!!...-IT.;!""
0x591060: 2%#(%.=.BEENDEN.................
```

The marker is literally just the ASCII text "START OF MENU SYSTEM!!!" followed by "END OF MENU SYSTEM!!!" with null bytes and the next string data immediately after.

---

## Lesson Learned

**Never assume developer debug markers define actual data boundaries.**

These markers are artifacts from development, not runtime boundaries. The game engine doesn't use them - they're just leftover text that happens to be embedded in the executable.

When extracting or analyzing FF7 string data:
1. Use byte pattern analysis
2. Follow FF terminators
3. Validate with actual game content
4. Ignore developer markers for boundary purposes

---

## References

- Session handoff: `SESSION_HANDOFF_2026-01-06-59_GERMAN_INVESTIGATION_001.md`
- Extraction script: `/scripts/german_extraction/extract_german_v3.py`
- Clean strings output: `/scripts/german_extraction/output_v3/clean_text/`
- Categorized analysis: `/scripts/german_extraction/output_v3/clean_text/german_menu_strings_categorized.txt`

---

## Marker Search Command

To find all developer markers in any FF7 executable:

```bash
strings -t x ff7_XX.exe | grep -E "(START|END) OF"
```

Or using Python:
```python
with open('ff7_de.exe', 'rb') as f:
    data = f.read()

for pattern in [b'START OF ', b'END OF ']:
    pos = 0
    while (pos := data.find(pattern, pos)) != -1:
        end = data.find(b'\x00', pos)
        print(f"0x{pos:06X}: {data[pos:end].decode('latin-1')}")
        pos += 1
```
