# FF7 Executable String Comparison Report

**Generated:** 2026-01-07 21:11:26 JST
**Session ID:** dd75b404-08f7-4cdc-b7d6-2f78c10a962e

---

## Overview

This report compares two sources of FF7 executable text strings:

1. **TXT File** (touphScript extraction): `0_ff7.exe.txt`
   - Location: `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\ff7_text\`
   - Entries: **767**

2. **CSV File** (manual EN/DE mapping): `ff7_en_de_mapping (1).csv`
   - Location: `C:\Users\johnz\Desktop\`
   - Rows: **746**
   - Unique English texts: **601**

---

## Summary Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| **Exact matches** | 664 | 89.0% |
| **Case differences** | 3 | 0.4% |
| **Encoding differences** | 4 | 0.5% |
| **CSV entries not in TXT** | 75 | 10.1% |
| **TXT entries not in CSV** | 73 | - |

**Overall CSV coverage in TXT:** 671 / 746 (89.9%)

---

## Detailed Analysis

### 1. Case Differences (3 entries)

These entries exist in both files but with different capitalization:

| CSV Text | TXT Text |
|----------|----------|
| `Ability List` | `Ability list` |
| `Equip Effect` | `Equip effect` |
| `Exit` | `EXIT` |


### 2. Encoding Differences (4 entries)

These entries use `[A9]` in CSV vs `…` (ellipsis) in TXT:

| CSV Text | TXT Text |
|----------|----------|
| `I'm not sure but[A9]` | `I'm not sure but…` |
| `I'm not too sure but[A9]` | `I'm not too sure but…` |
| `I'm getting less human[A9]` | `I'm getting less human…` |
| `Hmph. Don't quite get it but[A9]` | `Hmph. Don't quite get it but…` |


### 3. CSV Entries Not Found in TXT (75 entries)

These entries appear in the CSV but have no match in the touphScript extraction.
They may be from a different game version, alternate extraction, or have different formatting.

1. `3Dfx`
2. `Added effect`
3. `Assist`
4. `BLOCK`
5. `Battle Points won`
6. `Bolt`
7. `Buy`
8. `Can I help you?`
9. `Checking Memory Card.`
10. `Chocobo Lure`
11. `Come back again!`
12. `Command`
13. `Configure keyboard.`
14. `Defense   % up`
15. `Dual`
16. `EXP.Plus`
17. `EXT`
18. `Elem./Side effect`
19. `Enemy`
20. `Freshmake`
21. `GL!`
22. `Gil Plus`
23. `Gold`
24. `Growth:`
25. `HP<->MP`
26. `How many?`
27. `L1`
28. `L2`
29. `Limit point 0.`
30. `Local`
31. `Long Range`
32. `Luck   % up`
33. `M.Attack`
34. `M.Defense`
35. `M.Defense %`
36. `Magic   % up`
37. `Magic Materia!`
38. `Mega All`
39. `Mono`
40. `Not enough money!`
41. `Nullify`
42. `Number Stored   /24`
43. `OK, let's go!`
44. `OK?`
45. `Pre-emptive +%`
46. `Press Left/Right to exit.`
47. `Press START to configure.`
48. `R1`
49. `R2`
50. `Really take off?`
51. `SLOT 1`
52. `SLOT 2`
53. `Sell`
54. `Sephiroth`
55. `Slash-All`
56. `Slot:`
57. `Sneak`
58. `Speed   % up`
59. `Square`
60. `Stereo`
61. `Summon Materia!`
62. `Swift`
63. `Thank you!`
64. `Thanks!`
65. `Under`
66. `Usage`
67. `Whatcha got?`
68. `Wide`
69. `Window OFF`
70. `Yes     No`
71. `Yes!`
72. `You kiddin'? Not enough!`
73. `Zero - AW YEAH!`


### 4. TXT Entries Not Found in CSV (73 entries)

These entries appear in the touphScript extraction but are not in the manual CSV mapping.


#### Naming Screen Characters (6 entries)

- `+`
- `,`
- `-`
- `.`
- `:`
- `;`

#### Save Slot Numbers (15 entries)

- `01`
- `02`
- `03`
- `04`
- `05`
- `06`
- `07`
- `08`
- `09`
- `10`
- `11`
- `12`
- `13`
- `14`
- `15`

#### Keyboard Keys (13 entries)

- `APPS`
- `BACK SLASH`
- `EQUALS`
- `GRAVE`
- `LEFT BRACKET`
- `LEFT WIN`
- `MOUSE_B1`
- `MOUSE_B2`
- `MOUSE_B3`
- `RIGHT BRACKET`
- `RIGHT WIN`
- `SEMICOLON`
- `SLASH`

#### Minigame/Snowboard (2 entries)

- `--'--"---`
- `--'--"---`

#### Chocobo Race Names (11 entries)

- `AIMEE`
- `ANDY`
- `GAME`
- `GEORGE`
- `JENNY`
- `JULIA`
- `NANCY`
- `RICA`
- `ROBER`
- `TERRY`
- `TIM`

#### Battle/Status Text (4 entries)

- `1/2 HP&MP.`
- `1/2 MP.`
- `Cover`
- `Cover`

#### Menu/UI (5 entries)

- `Keep goin'?`
- `Load`
- `Reform`
- `Use`
- `Window color`

#### Items/Equipment (5 entries)

- `Enemy Away`
- `Ether`
- `Fire Veil`
- `Ice Crystal`
- `Turbo Ether`

#### Other (12 entries)

- `00'00"000`
- `00'00"000`
- `? ? ?`
- `How much will you raise?`
- `No.`
- `Of course!     No way!`
- `Press [CANCEL] to end.`
- `Sephiroth“……”`
- `Sneak Attack`
- `Sprint Shoes`
- `Swift Bolt`
- `Then, go for it!`


---

## Conclusions

1. **~90% coverage**: The CSV manual mapping covers approximately 90% of the touphScript extraction.

2. **TXT is more complete**: The TXT file includes all extractable strings, including:
   - Single characters for the naming screen (a-z, A-Z, punctuation)
   - Save slot numbers (01-15)
   - All keyboard key names
   - Chocobo race jockey names
   - Minigame/snowboard UI text

3. **CSV focuses on translatable text**: The manual CSV mapping focuses on text that needs translation (menus, dialogue, UI labels) and omits single characters and numbers.

4. **75 CSV entries not in TXT**: These may be:
   - From a different game version
   - Extracted using a different method
   - Have slight formatting differences (spacing, punctuation)

5. **Recommendation**: For a complete string database, merge both sources:
   - Use TXT as the authoritative source for offsets
   - Use CSV for German translations where available
   - Manually add German translations for the 73 TXT-only entries

---

## File Locations

- TXT Source: `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\ff7_text\0_ff7.exe.txt`
- CSV Source: `C:\Users\johnz\Desktop\ff7_en_de_mapping (1).csv`
- This Report: `C:\Users\johnz\Desktop\ff7_string_comparison_report.md`

---

*Report generated by Claude Code*
