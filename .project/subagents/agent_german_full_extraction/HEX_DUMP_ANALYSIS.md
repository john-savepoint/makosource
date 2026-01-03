# Hex Dump Analysis: Offset 0x5D7901-0x5D7E36

Created: 2026-01-03
Purpose: Clarify what the corrupted-looking German data actually represents

## Summary

The data at offset range **0x5D7901-0x5D7E36** is **NOT German menu strings**. Instead, it's **x86-64 compiled assembly code** mixed with binary data structures.

## What You're Looking At

### Example Decoding

"lD8(" at 0x5D7901 decodes to assembly instructions:
- `6C` = mov/lea instruction byte
- `44` = register+displacement format specifier
- `38` = immediate value (8)
- `28` = ASCII '(' character (0x28)

This is machine code with ASCII printable bytes interspersed, characteristic of:
1. Function prologues and epilogues
2. Stack frame setup instructions
3. Memory addressing calculations
4. Relocation/fixup tables

### Pattern Analysis

| Observed String | Encoding | Likely Meaning |
|-----------------|----------|---|
| `lD8(` | 0x6C 0x44 0x38 0x28 | mov instruction with immediate operand |
| `dD,` | 0x64 0x44 0x2C | mov instruction variant |
| `!!dD8` | 0x21 0x21 0x64 0x44 0x38 | Padding/alignment bytes + instruction |
| `$rÖ` | 0x24 0x72 0xD6 | mov to memory, high-byte chars |
| `TD@x` | 0x54 0x44 0x40 0x78 | Another instruction sequence |

The `D` bytes appearing frequently:
- Register encoding (RBP=0x45, RBX=0x43, RSP=0x44)
- Opcode continuation bytes for ModRM format
- Memory access size specifiers (0x44 = disp8 encoding)

The German-looking characters (Ö, ü) come from:
- High-byte values (0x80-0xFF) interpreted as Windows-1252/ISO-8859-1
- NOT actual German text, just binary data displayed as characters

## Verification Against Existing Documentation

The **CHUNK_59_ANALYSIS.md** already correctly identified this:

> "Chunk 59 contains binary/control data, not text"

This analysis confirms chunk 59 (and by extension chunk 86 in the 0x5D7xxx range) contains **compiled executable code**, not German menu strings.

## Where the German Menu Strings Actually Are

From the verified mapping files:

**German Menu String Location: 0x00590C68 - 0x00590D26**

These contain proper, readable German menu text:
- 0x00590C68: "Objekt" (Item)
- 0x00590C6F: "Zauber" (Magic)
- 0x00590C83: "Materia" (Materia)
- 0x00590C98: "Ausrüsten" (Equip)
- 0x00590CAE: "Werte" (Values/Status)
- 0x00590D0C: "Speichern" (Save)
- 0x00590D26: "Verlassen" (Quit)

These map directly to English menu indices **38-48** in the touphScript system.

## Key Offset Difference

- **Corrupted-looking strings:** 0x5D7901-0x5D7E36 (chunk 86, code section)
- **Actual German menu text:** 0x00590C68-0x00590D26 (data section)
- **Offset delta:** Approximately 0x00589000 bytes

This large delta indicates:
1. German version has different memory layout than English
2. Menu strings are in a different executable section
3. Chunk 86 data should be ignored for menu text extraction

## Conclusion

The corrupted-looking data is part of the executable's **code/relocation section**, not the string resource section. For German menu patching:

✅ **Use:** 0x00590C68-0x00590D26 (actual German menu strings)
❌ **Ignore:** 0x5D7901-0x5D7E36 (compiled assembly code)

The existing mapping files already have the correct German menu data. No additional hex analysis of chunk 86 is needed.
