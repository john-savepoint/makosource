# FF7 Japanese Mod - Beginner's Guide (Simple Explanations)

**For**: People confused by all the jargon
**Goal**: Understand what we're doing in simple terms
**Time**: 10 minutes to read

---

## The Problem (In Plain English)

**Scenario**: You're making a mod for Final Fantasy VII to display Japanese text instead of English.

**The Challenge**: FF7 was originally made for a 1998 computer that only understood English letters. When Square Enix wanted to sell it in Japan (2013), they had to completely rewrite how the game stores and displays text.

**Why?** Because:
- English has 26 letters + punctuation = ~200 characters total ✓ (fits easily)
- Japanese has 2,000+ kanji + hiragana + katakana = ~2,300 characters ✗ (doesn't fit!)

---

## The File Types (What Holds What?)

Think of FF7's data like a **filing cabinet**:

```
Cabinet = FF7 Game Folder
├── Drawer 1 = menu_us.lgp (English fonts)
│   └── Files inside:
│       ├── USFONT_H.TEX (font with all English letters)
│       ├── window.bin (tells game where each letter is)
│       └── (other menu graphics)
│
├── Drawer 2 = flevel.lgp (English dialogue)
│   └── Files inside:
│       ├── Field_1.field (Tifa's room scene)
│       │   └── Contains the text "Talk to me Cloud"
│       ├── Field_2.field (Midgar sector 7)
│       │   └── Contains the text "Welcome to Seventh Heaven"
│       └── (hundreds more scenes)
│
└── Drawer 3 = KERNEL.BIN (all the game data)
    └── Contains:
        ├── Item names
        ├── Ability names
        ├── Menu text
        └── More encoded data
```

### LGP Files = Compressed Folders

**LGP** is just a file format Square Enix invented. It's like a ZIP file, but custom-made for Final Fantasy.

**To understand LGP files**:
```
Think of it like this:

menu_us.lgp = 1 ZIP file = a folder that contains:
              ├── USFONT_H.TEX
              ├── USFONT_L.TEX
              ├── window.bin
              └── (other files)

To use the files inside, you must:
1. Extract the LGP (unzip it) → get individual files
2. Edit the files (change the images)
3. Repack the LGP (re-zip it)
```

**Tool to do this**: `ulgp` (the LGP extraction/repacking tool)

### TEX Files = Font Pictures

**TEX** is a picture format (like PNG, but Square Enix's version).

**What's inside a TEX file**?

```
Think of it like a POSTER covered with letters:

USFONT_H.TEX = A 1024×1024 pixel poster with all English letters
├── Top-left corner: Letter 'A'
├── Next to it: Letter 'B'
├── Next to that: Letter 'C'
└── ... continues for all 256 possible characters

When game needs to show "HELLO":
1. Game says "Give me character H" (that's index 0x48)
2. FFNx looks at USFONT_H.TEX position 0x48
3. Finds the letter 'H' in the image
4. Displays it on screen
```

**For Japanese**:

```
Instead of 1 poster, we have 6 posters:

jafont_1.tex = Poster 1: All the hiragana, katakana, numbers
jafont_2.tex = Poster 2: First batch of kanji characters
jafont_3.tex = Poster 3: Second batch of kanji characters
jafont_4.tex = Poster 4: Third batch of kanji characters
jafont_5.tex = Poster 5: Fourth batch of kanji characters
jafont_6.tex = Poster 6: Fifth batch of kanji characters

When game needs to show Japanese "必":
1. Game sees code: FA 00
2. FA = "Look at poster 2" (jafont_2.tex)
3. 00 = "Position 0 on that poster"
4. FFNx finds the kanji and displays it
```

### BIN Files = Encoded Game Data

**BIN** is a file containing game information **in a format humans can't easily read**.

Think of it like this:

```
KERNEL.BIN = A book written in a SECRET CODE

When you first get it, you see: 1F 8B 08 1A 00 00 00 00...
(looks like gibberish)

Steps to read it:
1. Decompress it (use gunzip) → now it's readable text bytes
2. Decode it (use FF Text format) → now you see actual characters

The result: Item names, enemy names, menu text, etc.
```

**Why separate files?**
- `menu_us.lgp` = Only the PICTURES (fonts and graphics)
- `flevel.lgp` = Only the DIALOGUE (story text by location)
- `KERNEL.BIN` = Everything ELSE (items, abilities, stats)

This separation makes it easy for translators. They only change `KERNEL.BIN` text, fonts stay the same.

---

## How Text Works In FF7 (The Core Concept)

### The English System

**How does the game store text?**

Not like this:
```
"Hello World"  ← Game DOESN'T store it this way (uses too much memory)
```

But like this:
```
48 65 6C 6C 6F 57 6F 72 6C 64  ← Hex codes for each letter
```

Which means:
```
48 = Letter 'H'
65 = Letter 'e'
6C = Letter 'l'
6C = Letter 'l'
6F = Letter 'o'
57 = Letter 'W'
6F = Letter 'o'
72 = Letter 'r'
6C = Letter 'l'
64 = Letter 'd'
```

**How does the game display it?**

```
Game reads: 48 65 6C 6C 6F...
            ↓
Each number = "Position in font picture"
            ↓
Position 0x48 in USFONT_H.TEX = Picture of letter 'H'
            ↓
Display 'H' on screen
```

### The Japanese Challenge

Japanese needs **2,300 different characters**, but the hex code system only goes 00-FF (256 maximum).

**Solution**: Reuse codes FA-FF as "switcher" codes:

```
FA = "Switch to poster #2 (jafont_2.tex)"
FB = "Switch to poster #3 (jafont_3.tex)"
FC = "Switch to poster #4 (jafont_4.tex)"
FD = "Switch to poster #5 (jafont_5.tex)"
FE = "Switch to poster #6 (jafont_6.tex)"

Example: The word "必殺技" becomes:
FA 00 FA 01 FA 02

Which means:
FA = Switch to poster 2
00 = Show position 0 from poster 2 = 必

FA = Switch to poster 2
01 = Show position 1 from poster 2 = 殺

FA = Switch to poster 2
02 = Show position 2 from poster 2 = 技
```

---

## Why French/German/Spanish Don't Have This Problem

### The Font Texture Comparison

```
English:
├── Has: A-Z, a-z, 0-9, .,!? and accented letters (é, ü, ñ)
├── Total needed: ~200 characters
├── Available space: 256 character slots
├── Font file: menu_us.lgp (1.7 MB with USFONT_H.TEX inside)
└── ✓ FITS EASILY!

French:
├── Has: A-Z, a-z, 0-9, .,!? and accented letters (é, è, ê, ë, ç, etc)
├── Total needed: ~200 characters
├── Available space: 256 character slots
├── Font file: menu_fr.lgp (1.7 MB, SAME as English!)
└── ✓ FITS EASILY!

German:
├── Has: A-Z, a-z, 0-9, .,!? and accented letters (ü, ö, ä, ß)
├── Total needed: ~200 characters
├── Available space: 256 character slots
├── Font file: menu_gm.lgp (1.7 MB, SAME as English!)
└── ✓ FITS EASILY!

Spanish:
├── Has: A-Z, a-z, 0-9, .,!? and accented letters (á, é, í, ó, ú, ñ, ¿, ¡)
├── Total needed: ~200 characters
├── Available space: 256 character slots
├── Font file: menu_sp.lgp (1.7 MB, SAME as English!)
└── ✓ FITS EASILY!

Japanese:
├── Has: A-Z, a-z, 0-9, hiragana, katakana, 2,136 kanji, symbols
├── Total needed: ~2,300 characters
├── Available space (single file): 256 character slots
├── ✗ DOESN'T FIT!
└── Solution: Use 6 font files (6 × 256 = 1,536 slots, need 1,331)
    └── Font archive: menu_ja.lgp (26.8 MB with 6 jafont_*.tex files!)
```

### Why This Matters

**Important realization**: When we modify FFNx for Japanese support, **French/German/Spanish don't need ANY changes**. They work exactly the same as English because they fit in a single font texture.

This means:
- ✅ English continues working
- ✅ French continues working
- ✅ German continues working
- ✅ Spanish continues working
- ⏳ Japanese needs special handling ONLY (6 textures + FA-FE codes)

---

## Our Solution (Path C) Explained Simply

### What We're Building

```
Old system (English only):
Game → FFNx Driver → Shows English from USFONT_H.TEX

New system (English + Japanese):
Game → FFNx Driver (ENHANCED) → Shows English from USFONT_H.TEX
                                ├── Recognizes FA-FE codes
                                └── Shows Japanese from jafont_1-6.tex
```

### The Three Strategies We Could Use

**Strategy A**: "Easy but limited"
- Just swap the font files (use jafont instead of USFONT)
- Problem: Game still doesn't understand FA-FE codes
- Result: Japanese text appears as boxes/garbled

**Strategy B**: "Copy Square's work"
- Use their AF3DN.P driver directly
- Problem: Proprietary, can't modify, no source code
- Result: Works but not maintainable

**Strategy C** (CHOSEN): "Build it ourselves"
- Study AF3DN.P to understand how it works
- Rewrite that logic in FFNx (open source)
- Now it's maintainable, improvable, community-owned
- Result: Works AND sustainable

### What We're Allowed to Do with AF3DN.P

**You have legal authority to:**
- ✅ Copy code from AF3DN.P if needed
- ✅ Use AF3DN.P's implementation directly
- ✅ Replicate its approach exactly in code
- ✅ Study it as a complete reference

**But we're choosing a smarter approach:**
- Write fresh code in FFNx (modern architecture)
- Understand AF3DN.P's proven design
- Implement the same logic in FFNx's system
- Keep code clean and maintainable long-term

**Why our code will be different even if we understand AF3DN.P perfectly:**

```
AF3DN.P (2013 DirectX 9 driver):
└── Uses old DirectX APIs
    └── DirectX 9 specific patterns
        └── Legacy C++ code style

Our FFNx extension (modern multi-backend):
└── Uses BGFX abstraction layer
    └── Works across DirectX 11/12, Vulkan, OpenGL
        └── Modern C++ patterns
```

**Same logic, different architecture** = code necessarily looks different.

Think of it like building:
- ✅ Study how Ferrari's V12 engine works
- ✅ You're allowed to copy it completely
- ✅ But we choose to build a modern electric motor instead
- ✅ Same performance, different (better) technology

---

## Timeline (What Happens When?)

```
Week 1-2: Test Phase
├── Prove FFNx texture override works
├── Try swapping English/Japanese fonts
└── Document what breaks (encoding issues)

Week 3-4: Study AF3DN.P
├── Understand the 6-texture loading system
├── Document the FA-FE code logic
└── Design our FFNx extension

Week 5-10: Build FFNx Extension
├── Write code to load 6 font textures
├── Add FA-FE code recognition
├── Test with Japanese text
└── Fix bugs

Week 11-14: Integration & Release
├── Connect to game executable
├── Test full game with Japanese
├── Package for distribution
└── Release to community
```

---

## Success Looks Like

```
BEFORE (English game):
├── Menu shows: "ITEMS" "MAGIC" "EQUIPMENT"
└── Dialogue shows: "Nice to meet you, Cloud"

AFTER (With our mod):
├── Menu shows: "アイテム" "魔法" "装備" (Japanese)
└── Dialogue shows: "初めまして、クラウド" (Japanese)

AND:
├── English still works perfectly
├── Fonts render beautifully
├── Game doesn't crash
├── Community can install it easily via 7th Heaven
└── Other modders can extend it further
```

---

## Key Takeaways

1. **LGP files** = Compressed folders holding game assets
2. **TEX files** = Pictures of letters/kanji (like a font)
3. **BIN files** = Encoded game data (compressed and coded)
4. **FLEVEL.LGP** = Dialogue for each game scene
5. **French/German/Spanish** = Use single font (same as English)
6. **Japanese** = Needs 6 fonts because 2,300 characters don't fit in 256 slots
7. **FA-FE codes** = "Smart switches" that tell the game which font to use
8. **AF3DN.P** = Square's example implementation we're learning from
9. **Path C** = Build our own open-source solution based on what we learned
10. **Goal** = Make Japanese support work in FFNx (legally, sustainably, beautifully)

---

**Next**: Read PROJECT_OVERVIEW.md for technical details, or TEST_PROCEDURE.md to start hands-on work!
