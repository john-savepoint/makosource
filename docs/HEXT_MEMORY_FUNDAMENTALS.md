# HEXT Memory Patching Fundamentals

**Created:** 2025-12-06 00:42 JST (Saturday)
**Session-ID:** c245e7c0-ec73-4933-b925-5976860e742c
**Purpose:** Reference guide explaining how HEXT patching works, from basic concepts to practical application

---

## Table of Contents

1. [Bits and Bytes](#bits-and-bytes)
2. [Hexadecimal Notation](#hexadecimal-notation)
3. [Reading a Hex Dump](#reading-a-hex-dump)
4. [File Offset vs Virtual Address](#file-offset-vs-virtual-address)
5. [The VA Calculation Formula](#the-va-calculation-formula)
6. [How HEXT Patching Works](#how-hext-patching-works)
7. [String Length and Overflow](#string-length-and-overflow)
8. [FF7 Text Encoding](#ff7-text-encoding)
9. [Common Offset Errors](#common-offset-errors)

---

## Bits and Bytes

A **bit** is the smallest unit of data: either 0 or 1.

A **byte** is 8 bits grouped together. One byte can represent values from 0 to 255:

```
00000000 = 0
00000001 = 1
00000010 = 2
00000011 = 3
...
11111111 = 255
```

Every file on your computer - text documents, images, executables - is just a sequence of bytes.

---

## Hexadecimal Notation

Writing binary like `11111111` is tedious. Decimal doesn't show bit patterns clearly. Hexadecimal (base-16) solves this.

Hex uses 16 digits: `0-9` and `A-F`:

```
Decimal:  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15
Hex:      0  1  2  3  4  5  6  7  8  9   A   B   C   D   E   F
```

One hex digit = exactly 4 bits. Two hex digits = 8 bits = 1 byte:

```
Binary:     1111 1111
Hex:           F    F
Decimal:         255
```

### The 0x Prefix

The `0x` prefix means "this number is hexadecimal":

```
10    = ten (decimal)
0x10  = sixteen (hexadecimal)
0b10  = two (binary)
```

In HEXT files, the `0x` is omitted because hex is assumed:
```
920C0C = 5B 6D 67 99 FF
```

In documentation and code, we include it for clarity.

---

## Reading a Hex Dump

A hex dump (from tools like `xxd`) shows the raw bytes inside a file:

```
0051f670: 2152 5241 4e47 45ff 0000 0000 0000 0000  !RRANGE.........
```

This has three parts:

### Part 1: Address (left)
```
0051f670:
```
This line shows bytes starting at file position `0x51F670`.

### Part 2: Hex Bytes (middle)
```
2152 5241 4e47 45ff 0000 0000 0000 0000
```
The actual raw data. Each pair is one byte:
- `21` = byte value 33
- `52` = byte value 82
- `FF` = byte value 255 (string terminator in FF7)
- `00` = byte value 0 (null/padding)

### Part 3: ASCII Interpretation (right)
```
!RRANGE.........
```
What those bytes would look like as standard text. **Ignore this for FF7** - the game uses its own encoding, so this column shows garbage.

### Counting Positions

Each line shows 16 bytes. To find the exact position of a byte:

```
0051f680: 0000 0000 2558 4348 414e 4745 ff00 0000
          ^^^^ ^^^^                               positions +0 to +3
                    ^^^^ ^^^^                     positions +4 to +7
                              ^^^^ ^^^^           positions +8 to +11
                                        ^^^^ ^^^^ positions +12 to +15
```

If the line starts at `0x51F680`:
- Position +0 (`00`) is at `0x51F680`
- Position +4 (`25`) is at `0x51F684`
- Position +8 (`41`) is at `0x51F688`

---

## File Offset vs Virtual Address

These are two different ways to locate the same data.

### File Offset

The position in the exe file on disk, measured in bytes from the start.

```
"ARRANGE" is at file offset 0x51F60C
```

This means: go to byte number 5,305,868 in ff7_en.exe.

### Virtual Address (VA)

When you run the game, Windows loads the exe into RAM. It doesn't load it at address 0 - it places it at a specific memory location.

```
"ARRANGE" is at VA 0x920C0C
```

This means: when the game is running, that string lives at memory address 0x920C0C.

### Why They Differ

Windows doesn't copy the file byte-for-byte to memory position 0. It:

1. Picks a base address (`0x400000` for FF7)
2. Reads the exe's sections (.text for code, .data for data, etc.)
3. Places each section at specific memory addresses

The exe file contains a map saying where each section should go. The positions end up different between disk and memory.

### Analogy: Moving House

- **File on disk** = boxes in a moving truck, numbered 1, 2, 3...
- **Memory** = your new house with specific rooms

Box #50 contains kitchen stuff, but you don't put it at "position 50" in your house - you put it in the kitchen. HEXT patches the house (memory), so we need house addresses (VA), not box numbers (file offset).

---

## The VA Calculation Formula

```
VA = 0x400000 + 0x3BA000 + (FileOffset - 0x3B8A00)
     ────────   ────────   ─────────────────────
        │          │              │
        │          │              └── position within .data section
        │          │
        │          └── where .data section sits relative to base
        │
        └── base address where Windows loads the exe
```

### Breaking It Down

**Step 1: Find position within .data section**

The .data section (where menu strings live) starts at file offset `0x3B8A00`.

If our string is at file offset `0x51F60C`, how far into .data is it?

```
0x51F60C - 0x3B8A00 = 0x16700C
```

The string is `0x16700C` bytes after .data begins.

(We subtract because the string comes *after* .data starts. Like asking "how far past the 100m signpost are you if you're at 150m?" → 150 - 100 = 50m)

**Step 2: Find where .data lives in memory**

```
Base address + .data offset = 0x400000 + 0x3BA000 = 0x7BA000
```

**Step 3: Add position within .data**

```
0x7BA000 + 0x16700C = 0x920C0C
```

The string lives at memory address `0x920C0C`.

### Quick Reference

| Value | Meaning |
|-------|---------|
| `0x400000` | Base address where FF7 loads |
| `0x3BA000` | Offset of .data section in memory |
| `0x3B8A00` | Offset of .data section in file |

---

## How HEXT Patching Works

HEXT is simple: it overwrites bytes in memory.

When the game starts:

1. Windows loads `ff7_en.exe` into memory
2. "ARRANGE" ends up at memory address `0x920C0C`
3. FFNx reads your HEXT file
4. For each line like `920C0C = 5B 6D 67 99 FF 00 00 00`:
   - Go to memory address `0x920C0C`
   - Overwrite the bytes there with `5B 6D 67 99 FF 00 00 00`
5. Now that address contains "せいとん" instead of "ARRANGE"
6. Game runs with modified memory
7. When the game draws the menu, it reads from `0x920C0C` and finds Japanese text

That's it. Find address, overwrite bytes.

---

## String Length and Overflow

If you write more bytes than the original string, you'll overwrite whatever comes next in memory.

### Example

```
Memory layout:
ARRANGE.........EXCHANGE........
        ^^^^^^^^
        padding (null bytes)
```

If "ARRANGE" is 8 bytes and you write 20 bytes, you'd corrupt "EXCHANGE".

### Why It Usually Works

FF7's strings have padding between them. If English uses 8 bytes but 16 are allocated, you have room for longer Japanese text.

### The Safe Approach

We extract bytes from the actual Japanese exe (`ff7_ja.exe`). Since Square already made a Japanese version that works, those strings are guaranteed to fit.

When writing patches, match the original length:

```
# ARRANGE (せいとん) - 5 bytes, original 8
920C0C = 5B 6D 67 99 FF 00 00 00
                       ^^^^^^^^
                       padding to fill original 8 bytes
```

---

## FF7 Text Encoding

FF7 does **not** use standard ASCII. It has its own character encoding.

### English Encoding

FF7 English = ASCII minus `0x20`:

```
Standard ASCII:  A = 0x41,  B = 0x42,  C = 0x43 ...
FF7 English:     A = 0x21,  B = 0x22,  C = 0x23 ...
```

So when a hex dump shows:
```
0051f60c: 2152 5241 4e47 45ff  !RRANGE.
```

The right side shows `!RRANGE` (ASCII interpretation), but FF7 reads it as `ARRANGE`.

### Japanese Encoding

Japanese uses the jafont texture files:

- **jafont_1** (single byte): Index 0-255 → byte value directly
- **jafont_2** (two bytes): `FA` + index
- **jafont_3** (two bytes): `FB` + index
- **jafont_4** (two bytes): `FC` + index
- **jafont_5** (two bytes): `FD` + index
- **jafont_6** (two bytes): `FE` + index

Example: せいとん = `5B 6D 67 99`
- `5B` = せ (jafont_1, index 91)
- `6D` = い (jafont_1, index 109)
- `67` = と (jafont_1, index 103)
- `99` = ん (jafont_1, index 153)

### String Terminator

All FF7 strings end with `0xFF`. Everything after is padding (`0x00`) or the next string.

---

## Common Offset Errors

The most frequent mistake: assuming a string starts at the hex dump line address.

### The Problem

```
0051f680: 0000 0000 2558 4348 414e 4745 ff00 0000  ....%XCHANGE....
```

Seeing `0051f680:` and thinking "EXCHANGE is at 0x51F680".

**Wrong.** The string starts 4 bytes in, at `0x51F684`.

### The Rule

Always count from the line address to the first non-zero byte:

1. Line address: `0x51F680`
2. First 4 bytes are `00 00 00 00` (padding)
3. String starts at byte 5: `0x51F680 + 4 = 0x51F684`

### Why Strings Have Padding

FF7 stores strings in variable-sized slots with irregular padding. Some start right at slot boundaries, others are offset by 2, 4, or more bytes. There's no consistent pattern - you must check each one.

---

## Quick Reference Card

### Convert File Offset to VA

```python
def file_to_va(file_offset):
    return (file_offset - 0x3B8A00) + 0x3BA000 + 0x400000
```

### HEXT File Format

```
# Comment
VA_ADDRESS = BYTE BYTE BYTE ...

# Example
920C0C = 5B 6D 67 99 FF 00 00 00
```

### Key Addresses

| What | Value |
|------|-------|
| FF7 base address | `0x400000` |
| .data section (memory) | `0x7BA000` |
| .data section (file) | `0x3B8A00` |

### Jafont Prefixes

| Prefix | Texture |
|--------|---------|
| (none) | jafont_1 |
| `FA` | jafont_2 |
| `FB` | jafont_3 |
| `FC` | jafont_4 |
| `FD` | jafont_5 |
| `FE` | jafont_6 |

### String Terminator

`FF` = end of string

---

## Tools

### exe_string_dumper.py

Located at: `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/exe_string_dumper.py`

Dumps strings from the exe with correct positions and proper FF7 decoding:

```bash
# English exe only
python3 exe_string_dumper.py "ff7_en.exe" 0x51F500 0x500

# With Japanese comparison
python3 exe_string_dumper.py "ff7_en.exe" 0x51F500 0x500 --ja "ff7_ja.exe"

# With raw hex dump
python3 exe_string_dumper.py "ff7_en.exe" 0x51F500 0x500 --raw
```

This tool finds exact string positions, eliminating the offset errors that come from manually reading xxd output.

---

*End of document*
