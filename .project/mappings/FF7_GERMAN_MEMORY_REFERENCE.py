#!/usr/bin/env python3
"""
FF7 German Memory Structure Reference & Decoder
================================================
Created: 2026-01-06 15:30 JST (Tuesday)
Session-ID: 85c271e2-f1ef-4bb6-b5dc-b212b2694001
Author: John Zealand-Doyle

COMPREHENSIVE REFERENCE for decoding FF7 German (ff7_de.exe) memory structures.
This file serves as both documentation AND a working decoder tool.

================================================================================
QUICK REFERENCE
================================================================================

MEMORY REGIONS (File Offsets):
    0x58F700 - 0x58F730   CREDITS markers (ASCII)
    0x58FBB0 - 0x59E000   MENU STRING TABLE (FF7-encoded German text)
    0x591024 - 0x591058   MENU SYSTEM developer markers (ASCII)
    0x595B94 - 0x596400   UI COORDINATE TABLES (binary, NOT text)
    0x5981E8 - 0x5986BE   BINARY/COMPRESSED DATA
    0x598900 - 0x598F00   CHARACTER NAME STRUCTS (132 bytes each)

TERMINATORS:
    0xFF = String terminator (stops decoding)
    0x00 = Space character (middle of string) OR padding (leading bytes)

ENCODING FORMULA:
    Standard: byte + 0x20 = ASCII character (for bytes 0x01-0x5F)
    Special:  German umlauts use specific byte mappings (see GERMAN_CHAR_MAP)

GERMAN CHARACTER MAP:
    0x66 = Ü    0x6A = ä    0x7A = ö    0x7E = ß    0x7F = ü

================================================================================
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import struct
import re

# =============================================================================
# CONSTANTS & MAPPINGS
# =============================================================================

# File offset constants
CREDITS_START = 0x58F700
CREDITS_END = 0x58F730
MENU_TABLE_START = 0x58FBB0
MENU_TABLE_END = 0x59E000
MENU_MARKER_START = 0x591024
MENU_MARKER_END = 0x591058
UI_TABLE_START = 0x595B94
UI_TABLE_END = 0x596400
BINARY_DATA_START = 0x5981E8
BINARY_DATA_END = 0x5986BE
CHAR_STRUCT_START = 0x598900
CHAR_STRUCT_END = 0x598F00
CHAR_STRUCT_SIZE = 132  # 0x84 bytes per character

# Special byte values
TERMINATOR = 0xFF
SPACE = 0x00

# German umlaut mappings (VERIFIED from ff7_de.exe analysis)
# Corrections made 2026-01-07 based on verification against ff7_de.exe:
#   - 0x60: Added 'Ä' (uppercase A-umlaut)
#   - 0x65: Fixed from 'å' to 'Ö' (uppercase O-umlaut)
#   - 0x87: Added alternative 'ß' encoding
GERMAN_CHAR_MAP: Dict[int, str] = {
    # Core German characters
    0x60: 'Ä',  # uppercase A-umlaut
    0x65: 'Ö',  # uppercase O-umlaut (was incorrectly 'å')
    0x66: 'Ü',  # uppercase U-umlaut
    0x6A: 'ä',  # lowercase a-umlaut
    0x7A: 'ö',  # lowercase o-umlaut
    0x7E: 'ß',  # eszett (sharp S)
    0x7F: 'ü',  # lowercase u-umlaut
    0x87: 'ß',  # alternative eszett encoding

    # Extended Latin (for completeness)
    0x61: 'á', 0x62: 'à', 0x63: 'â', 0x64: 'ã',
    0x67: 'ç', 0x68: 'é', 0x69: 'è', 0x6B: 'ë',
    0x6C: 'í', 0x6D: 'ì', 0x6E: 'î', 0x6F: 'ï',
    0x70: 'ñ', 0x71: 'ó', 0x72: 'ò', 0x73: 'ô', 0x74: 'õ',
    0x76: '°', 0x77: '•', 0x78: '£',
}

# Reverse mapping for encoding
GERMAN_ENCODE_MAP: Dict[str, int] = {v: k for k, v in GERMAN_CHAR_MAP.items()}

# Character slot indices (in character structs)
CHARACTER_SLOTS = {
    0x01: 'Barret',
    0x02: 'Tifa',
    0x03: 'Aerith',
    0x04: 'Red XIII',
    0x05: 'Yuffie',
    0x06: 'Cait Sith',
    0x07: 'Vincent',
    0x08: 'Cid',
    0x09: 'Young Cloud',
    0x0A: 'Sephiroth',
}

# Known FF7-encoded character names (for pattern matching)
CHARACTER_NAME_PATTERNS = {
    'CLOUD': bytes([0x23, 0x4C, 0x4F, 0x55, 0x44]),
    'BARRET': bytes([0x22, 0x41, 0x52, 0x52, 0x45, 0x54]),
    'TIFA': bytes([0x34, 0x49, 0x46, 0x41]),
    'AERITH': bytes([0x21, 0x45, 0x52, 0x49, 0x54, 0x48]),
    'RED': bytes([0x32, 0x45, 0x44]),
    'YUFFIE': bytes([0x39, 0x55, 0x46, 0x46, 0x49, 0x45]),
    'CAIT': bytes([0x23, 0x41, 0x49, 0x54]),
    'VINCENT': bytes([0x36, 0x49, 0x4E, 0x43, 0x45, 0x4E, 0x54]),
    'CID': bytes([0x23, 0x49, 0x44]),
    'SEPHIROTH': bytes([0x33, 0x45, 0x50, 0x48, 0x49, 0x52, 0x4F, 0x54, 0x48]),
    'CHOCO': bytes([0x23, 0x48, 0x4F, 0x43, 0x4F]),
}

# =============================================================================
# DATA TYPES
# =============================================================================

class DataType(Enum):
    """Classification of data regions in the menu table."""
    CLEAN_TEXT = "clean_text"          # Actual German menu strings
    UI_TABLE = "ui_table"              # UI coordinate/positioning data
    BINARY_DATA = "binary_data"        # Compressed/encrypted data
    CHARACTER_STRUCT = "character"     # Character name struct
    ASSET_FILENAME = "asset"           # Plain ASCII .tim filenames
    DEVELOPER_MARKER = "developer"     # Debug strings
    FRAGMENT = "fragment"              # Short entries (≤2 chars)
    UNKNOWN = "unknown"


@dataclass
class DecodedEntry:
    """Represents a decoded entry from the string table."""
    index: int
    raw_offset: int
    text_offset: int
    raw_bytes: bytes
    decoded_text: str
    data_type: DataType
    confidence: int
    notes: str


@dataclass
class CharacterStruct:
    """
    Represents a 132-byte character name struct.

    STRUCTURE (132 bytes / 0x84):
    ============================
    Offset  Size  Type      Description
    ------  ----  --------  -----------
    0x00    4     uint32    Character ID (little-endian)
    0x04    1     uint8     Slot Index (01=Barret, 02=Tifa, etc.)
    0x05    1     uint8     Flag (always 0x01)
    0x06    6     uint8[6]  Base Stats: STR, VIT, MAG, SPR, DEX, LCK
    0x0C    6     padding   Zeros
    0x12    1     uint8     Prefix marker (0x01)
    0x13    1     uint8     Position/modifier code
    0x14    var   ff7str    FF7-encoded name (variable length, FF terminated)
    ...     var   padding   0xFF padding to 132 bytes

    THE "GARBAGE" EXPLAINED:
    ========================
    When the struct header is decoded as FF7 text, it produces garbage like:
    "C   !!/-+)%-      !öBarret"

    Breaking this down:
    - "C" = Byte 0x23 decoded (0x23 + 0x20 = 'C') - actually the Character ID
    - "   " = Bytes 0x00 0x00 0x00 - upper bytes of ID (spaces)
    - "!!" = Bytes 0x01 0x01 (slot index + flag) decoded as '!'
    - "/-+)%-" = Stats bytes decoded as punctuation:
        0x0F → '/' (STR=15)
        0x0D → '-' (VIT=13)
        0x0B → '+' (MAG=11)
        0x09 → ')' (SPR=9)
        0x05 → '%' (DEX=5)
        0x0D → '-' (LCK=13)
    - "      " = Padding zeros (spaces)
    - "!ö" = 0x01 0x7A (prefix marker + position code decoded as ö)
    - "Barret" = Actual FF7-encoded name
    """
    offset: int
    char_id: int
    slot_index: int
    slot_name: str
    flag: int
    stats: Dict[str, int]
    name: str
    name_offset: int
    raw_header: bytes


# =============================================================================
# DECODING FUNCTIONS
# =============================================================================

def decode_ff7_byte(b: int) -> str:
    """
    Decode a single FF7-encoded byte to its character representation.

    Args:
        b: Byte value (0x00-0xFF)

    Returns:
        Character string, or [XX] for unknown/special bytes

    Rules:
        0x00 = Space
        0x01-0x5F = byte + 0x20 = ASCII
        0x60-0x7F = German umlauts (see GERMAN_CHAR_MAP)
        0x80-0xFE = Unknown (shown as [XX])
        0xFF = Terminator (shown as [END])
    """
    if b == TERMINATOR:
        return '[END]'
    elif b in GERMAN_CHAR_MAP:
        return GERMAN_CHAR_MAP[b]
    elif b == SPACE:
        return ' '
    elif 0x01 <= b <= 0x5F:
        return chr(b + 0x20)
    else:
        return f'[{b:02X}]'


def decode_ff7_string(data: bytes, stop_at_terminator: bool = True) -> str:
    """
    Decode FF7-encoded bytes to German text.

    Args:
        data: Raw bytes from ff7_de.exe
        stop_at_terminator: If True, stop at 0xFF; if False, decode all bytes

    Returns:
        Decoded German string

    Example:
        >>> decode_ff7_string(bytes([0x2D, 0x7A, 0x43, 0x48, 0x54, 0x45, 0x4E, 0xFF]))
        'Möchten'
    """
    result = []
    for b in data:
        if b == TERMINATOR and stop_at_terminator:
            break
        result.append(decode_ff7_byte(b) if b != TERMINATOR else '')
    return ''.join(result)


def encode_ff7_string(text: str, add_terminator: bool = True) -> bytes:
    """
    Encode German text to FF7 format.

    Args:
        text: German string to encode
        add_terminator: If True, append 0xFF terminator

    Returns:
        FF7 encoded bytes

    Raises:
        ValueError: If text contains unencodable characters
    """
    result = []
    for c in text:
        if c in GERMAN_ENCODE_MAP:
            result.append(GERMAN_ENCODE_MAP[c])
        elif c == ' ':
            result.append(SPACE)
        elif 0x21 <= ord(c) <= 0x7F:
            result.append(ord(c) - 0x20)
        else:
            raise ValueError(f"Cannot encode: {c!r} (U+{ord(c):04X})")
    if add_terminator:
        result.append(TERMINATOR)
    return bytes(result)


def find_text_start(data: bytes) -> int:
    """
    Find where actual text starts (skip leading 0x00 padding).

    FF7 German strings are RIGHT-ALIGNED with leading zeros.
    This finds the first non-zero byte.

    Args:
        data: Raw bytes

    Returns:
        Index of first non-zero byte, or len(data) if all zeros
    """
    for i, b in enumerate(data):
        if b != SPACE:
            return i
    return len(data)


# =============================================================================
# STRUCT PARSING
# =============================================================================

def parse_character_struct(data: bytes, offset: int) -> Optional[CharacterStruct]:
    """
    Parse a 132-byte character name struct.

    Args:
        data: 132 bytes of struct data
        offset: File offset where struct starts

    Returns:
        CharacterStruct object, or None if invalid
    """
    if len(data) < 20:
        return None

    char_id = struct.unpack('<I', data[0:4])[0]
    slot_index = data[4]
    flag = data[5]

    stats = {
        'STR': data[6],
        'VIT': data[7],
        'MAG': data[8],
        'SPR': data[9],
        'DEX': data[10],
        'LCK': data[11],
    }

    # Find name (starts at byte 20)
    name = ""
    name_offset = offset + 20
    if len(data) >= 20:
        name_bytes = data[20:]
        ff_pos = name_bytes.find(bytes([TERMINATOR]))
        if ff_pos > 0:
            name = decode_ff7_string(name_bytes[:ff_pos])

    return CharacterStruct(
        offset=offset,
        char_id=char_id,
        slot_index=slot_index,
        slot_name=CHARACTER_SLOTS.get(slot_index, f'Unknown ({slot_index})'),
        flag=flag,
        stats=stats,
        name=name,
        name_offset=name_offset,
        raw_header=data[:20],
    )


# =============================================================================
# DATA TYPE CLASSIFICATION
# =============================================================================

def classify_region(offset: int, data: bytes, decoded: str) -> Tuple[DataType, int, str]:
    """
    Classify what type of data a region contains.

    Args:
        offset: File offset
        data: Raw bytes
        decoded: FF7-decoded text

    Returns:
        Tuple of (DataType, confidence 0-100, reason string)
    """
    text = decoded.strip()

    # Check for asset filenames (plain ASCII with .tim)
    if b'.tim' in data or b'.TIM' in data:
        return (DataType.ASSET_FILENAME, 100, "contains .tim extension")

    # Check for developer markers
    if b'START OF MENU' in data or b'END OF MENU' in data:
        return (DataType.DEVELOPER_MARKER, 100, "developer marker")

    # Check for character name patterns
    for name, pattern in CHARACTER_NAME_PATTERNS.items():
        if pattern in data:
            return (DataType.CHARACTER_STRUCT, 95, f"contains {name}")

    # Check for binary data (high-byte ratio)
    non_padding = bytes([b for b in data if b != SPACE and b != TERMINATOR])
    if non_padding:
        high_bytes = sum(1 for b in non_padding if b >= 0x80)
        if high_bytes / len(non_padding) > 0.30:
            return (DataType.BINARY_DATA, 90, f"high byte ratio: {high_bytes}/{len(non_padding)}")

    # Check for UI coordinate patterns
    if UI_TABLE_START <= offset <= UI_TABLE_END:
        if len(text) < 15 and re.search(r'[0-9]', text):
            return (DataType.UI_TABLE, 85, "in UI coordinate region")

    # Coordinate pattern: "X X 3Y"
    if re.match(r'^[A-Za-z] [A-Za-z] \d', text):
        return (DataType.UI_TABLE, 90, "coordinate pattern")

    # Fragment (too short)
    if len(text) <= 2 and text.upper() not in ['JA', 'HP', 'MP', 'AP', 'LV', 'OK']:
        return (DataType.FRAGMENT, 80, "too short")

    # Check for clean German text
    if text:
        alpha_count = sum(1 for c in text if c.isalpha() or c in 'äöüÜß')
        if len(text) > 0 and alpha_count / len(text) > 0.5:
            return (DataType.CLEAN_TEXT, 85, f"german ratio: {alpha_count}/{len(text)}")

    return (DataType.UNKNOWN, 50, "no pattern matched")


# =============================================================================
# HEX DUMP UTILITY
# =============================================================================

def hex_dump(data: bytes, offset: int = 0, width: int = 16, show_decoded: bool = True) -> str:
    """
    Create a hex dump with optional FF7 decoding.

    Args:
        data: Bytes to dump
        offset: Starting offset for display
        width: Bytes per line
        show_decoded: If True, show FF7-decoded chars alongside ASCII

    Returns:
        Formatted hex dump string
    """
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)

        line = f"{offset + i:06X}: {hex_part:<{width * 3}}  {ascii_part}"

        if show_decoded:
            ff7_part = ''.join(decode_ff7_byte(b) if b != TERMINATOR else '.' for b in chunk)
            # Truncate [XX] markers for cleaner display
            ff7_clean = re.sub(r'\[\w\w\]', '?', ff7_part)
            line += f"  | {ff7_clean}"

        lines.append(line)

    return '\n'.join(lines)


# =============================================================================
# MAIN EXTRACTION
# =============================================================================

def extract_menu_strings(exe_path: str) -> List[DecodedEntry]:
    """
    Extract all menu strings from ff7_de.exe.

    Args:
        exe_path: Path to ff7_de.exe

    Returns:
        List of DecodedEntry objects for all FF-terminated entries
    """
    with open(exe_path, 'rb') as f:
        f.seek(MENU_TABLE_START)
        data = f.read(MENU_TABLE_END - MENU_TABLE_START)

    entries = []
    current = []
    entry_start = 0
    index = 0

    for i, b in enumerate(data):
        if b == TERMINATOR:
            if current:
                raw = bytes(current)
                raw_offset = MENU_TABLE_START + entry_start

                text_start = find_text_start(raw)
                text_offset = raw_offset + text_start

                decoded = decode_ff7_string(raw[text_start:])
                data_type, confidence, notes = classify_region(raw_offset, raw, decoded)

                entries.append(DecodedEntry(
                    index=index,
                    raw_offset=raw_offset,
                    text_offset=text_offset,
                    raw_bytes=raw,
                    decoded_text=decoded.strip(),
                    data_type=data_type,
                    confidence=confidence,
                    notes=notes,
                ))
                index += 1

            current = []
            entry_start = i + 1
        else:
            if not current:
                entry_start = i
            current.append(b)

    return entries


def extract_character_structs(exe_path: str) -> List[CharacterStruct]:
    """
    Extract all character name structs from ff7_de.exe.

    Args:
        exe_path: Path to ff7_de.exe

    Returns:
        List of CharacterStruct objects
    """
    with open(exe_path, 'rb') as f:
        f.seek(CHAR_STRUCT_START)
        region = f.read(CHAR_STRUCT_END - CHAR_STRUCT_START)

    structs = []
    for i in range(0, len(region), CHAR_STRUCT_SIZE):
        if i + CHAR_STRUCT_SIZE > len(region):
            break

        struct_data = region[i:i + CHAR_STRUCT_SIZE]
        offset = CHAR_STRUCT_START + i

        # Skip empty structs (all 0xFF or 0x00)
        if all(b in (0x00, 0xFF) for b in struct_data):
            continue

        parsed = parse_character_struct(struct_data, offset)
        if parsed and parsed.name:
            structs.append(parsed)

    return structs


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def print_reference():
    """Print the complete encoding reference."""
    print("""
================================================================================
FF7 GERMAN ENCODING REFERENCE
================================================================================

MEMORY REGIONS (File Offsets in ff7_de.exe):
--------------------------------------------
Region              Start       End         Description
------------------- ----------- ----------- ------------------------------------
CREDITS             0x58F700    0x58F730    ASCII developer markers
MENU TABLE          0x58FBB0    0x59E000    FF7-encoded German text + data
  └─ Quit Dialog    0x58FBB0    ~0x58FC20   "Möchten Sie..."
  └─ Config Menu    0x5900F0    ~0x590C00   "Fensterfarbe", "Sound", etc.
  └─ Main Menu      0x590C68    ~0x591000   "Objekt", "Zauber", etc.
MENU MARKERS        0x591024    0x591058    "START/END OF MENU SYSTEM!!!"
UI TABLES           0x595B94    0x596400    Binary coordinate data (NOT text)
BINARY DATA         0x5981E8    0x5986BE    Compressed/encrypted data
CHAR STRUCTS        0x598900    0x598F00    132-byte character records

ENCODING RULES:
---------------
Byte Range      Decoding
------------    ----------------------------------------
0x00            Space (or padding if leading)
0x01 - 0x5F     byte + 0x20 = ASCII character
0x60 - 0x7F     German umlauts (see mapping below)
0x80 - 0xFE     Unknown/binary (shown as [XX])
0xFF            String TERMINATOR (stops decoding)

GERMAN UMLAUT MAPPING:
----------------------
Byte    Char    Example Usage
----    ----    ----------------------------------
0x66    Ü       GRÜN, MENÜ
0x6A    ä       Auswählen, wählen, Fensterfarbe
0x7A    ö       Möchten, können, Löschen
0x7E    ß       muß, daß (old spelling)
0x7F    ü       zurück, für, Menü

DECODING EXAMPLE:
-----------------
Raw bytes: 2D 7A 43 48 54 45 4E FF
           |  |  |  |  |  |  |  └─ 0xFF = terminator
           |  |  |  |  |  |  └──── 0x4E + 0x20 = 'n'
           |  |  |  |  |  └─────── 0x45 + 0x20 = 'e'
           |  |  |  |  └────────── 0x54 + 0x20 = 't'
           |  |  |  └───────────── 0x48 + 0x20 = 'h'
           |  |  └──────────────── 0x43 + 0x20 = 'c'
           |  └─────────────────── 0x7A = 'ö' (special)
           └────────────────────── 0x2D + 0x20 = 'M'
Result: "Möchten"

CHARACTER STRUCT FORMAT (132 bytes):
------------------------------------
Offset  Size  Description
------  ----  --------------------------------------------------
0x00    4     Character ID (uint32, little-endian)
0x04    1     Slot Index: 01=Barret, 02=Tifa, 03=Aerith, etc.
0x05    1     Flag (always 0x01)
0x06    6     Base Stats: STR, VIT, MAG, SPR, DEX, LCK
0x0C    6     Padding (zeros)
0x12    1     Prefix marker (0x01)
0x13    1     Position/modifier code
0x14    var   FF7-encoded name + 0xFF terminator
...     var   0xFF padding to 132 bytes

WHY "GARBAGE" APPEARS:
----------------------
The struct header bytes, when incorrectly decoded as FF7 text:

Raw: 23 00 00 00 01 01 0F 0D 0B 09 05 0D 00 00 00 00 00 00 01 7A ...
     ↓
Decoded as text: "C   !!/-+)%-      !ö..."

- 0x23 → 'C' (should be: Character ID = 35)
- 0x00 → ' ' (should be: upper ID bytes)
- 0x01 → '!' (should be: slot index)
- 0x0F → '/' (should be: STR stat = 15)
- etc.

The "garbage" IS the binary struct header being misinterpreted as text!
""")


def main():
    import sys

    if len(sys.argv) < 2:
        print_reference()
        print("\nUsage:")
        print("  python FF7_GERMAN_MEMORY_REFERENCE.py reference")
        print("  python FF7_GERMAN_MEMORY_REFERENCE.py decode <hex>")
        print("  python FF7_GERMAN_MEMORY_REFERENCE.py encode <text>")
        print("  python FF7_GERMAN_MEMORY_REFERENCE.py dump <exe> <offset> [length]")
        print("  python FF7_GERMAN_MEMORY_REFERENCE.py extract <exe>")
        print("  python FF7_GERMAN_MEMORY_REFERENCE.py chars <exe>")
        return

    cmd = sys.argv[1].lower()

    if cmd == 'reference':
        print_reference()

    elif cmd == 'decode':
        if len(sys.argv) < 3:
            print("Error: Missing hex string")
            return
        hex_str = sys.argv[2].replace(' ', '').replace('0x', '')
        data = bytes.fromhex(hex_str)
        decoded = decode_ff7_string(data)
        print(f"Decoded: {decoded}")

    elif cmd == 'encode':
        if len(sys.argv) < 3:
            print("Error: Missing text")
            return
        text = sys.argv[2]
        encoded = encode_ff7_string(text)
        print(f"Encoded: {encoded.hex()}")
        print(f"Bytes: {' '.join(f'{b:02X}' for b in encoded)}")

    elif cmd == 'dump':
        if len(sys.argv) < 4:
            print("Error: Missing exe path and offset")
            return
        exe_path = sys.argv[2]
        offset = int(sys.argv[3], 0)
        length = int(sys.argv[4], 0) if len(sys.argv) > 4 else 256

        with open(exe_path, 'rb') as f:
            f.seek(offset)
            data = f.read(length)

        print(f"Hex dump at 0x{offset:06X}:")
        print(hex_dump(data, offset))

    elif cmd == 'extract':
        if len(sys.argv) < 3:
            print("Error: Missing exe path")
            return
        exe_path = sys.argv[2]
        entries = extract_menu_strings(exe_path)

        clean = [e for e in entries if e.data_type == DataType.CLEAN_TEXT]
        print(f"Found {len(entries)} total entries, {len(clean)} clean text\n")

        print("First 20 clean strings:")
        for e in clean[:20]:
            print(f"  [{e.index:4d}] 0x{e.text_offset:06X}: {e.decoded_text[:50]}")

    elif cmd == 'chars':
        if len(sys.argv) < 3:
            print("Error: Missing exe path")
            return
        exe_path = sys.argv[2]
        structs = extract_character_structs(exe_path)

        print(f"Found {len(structs)} character structs:\n")
        for s in structs:
            print(f"  0x{s.offset:06X}: {s.slot_name:12} - \"{s.name}\"")
            print(f"    Stats: STR={s.stats['STR']:2}, VIT={s.stats['VIT']:2}, "
                  f"MAG={s.stats['MAG']:2}, SPR={s.stats['SPR']:2}, "
                  f"DEX={s.stats['DEX']:2}, LCK={s.stats['LCK']:2}")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == '__main__':
    main()
