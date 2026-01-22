#!/usr/bin/env python3
"""
FF7 German String Decoder
=========================
Created: 2026-01-03 16:15 JST (Saturday)
Session-ID: 629f3c93-f884-439a-91d6-d77e7783bf9c

Utility for decoding and encoding German strings from FF7's ff7_de.exe.

The encoding uses a modified ASCII scheme:
- Standard chars (0x00-0x5F): byte + 0x20 = ASCII character
- German special chars: custom mappings for umlauts and ß
- 0xFF: string terminator

Usage:
    # As a module
    from ff7_german_decoder import decode_ff7_german, encode_ff7_german

    # Decode bytes from exe
    text = decode_ff7_german(bytes([0x2D, 0x7A, 0x43, 0x48, 0x54, 0x45, 0x4E, 0xFF]))
    # Returns: 'Möchten'

    # Encode German text
    encoded = encode_ff7_german('Möchten')
    # Returns: b'\\x2d\\x7a\\x43\\x48\\x54\\x45\\x4e\\xff'

    # Command line: decode hex string
    python ff7_german_decoder.py decode 2d7a434854454eff

    # Command line: encode text
    python ff7_german_decoder.py encode "Möchten"

    # Command line: read from exe at offset
    python ff7_german_decoder.py read /path/to/ff7_de.exe 0x58FBB0 50
"""

from typing import Dict, Optional
import sys

# =============================================================================
# CHARACTER MAPPINGS
# =============================================================================

# German special characters (VERIFIED from ff7_de.exe)
# These override the standard byte + 0x20 formula
FF7_GERMAN_DECODE_MAP: Dict[int, str] = {
    # Core German characters (verified)
    0x66: 'Ü',  # uppercase U-umlaut (in GRÜN, MENÜ buttons)
    0x6A: 'ä',  # lowercase a-umlaut (in Auswählen, wählen)
    0x7A: 'ö',  # lowercase o-umlaut (in Möchten, können)
    0x7E: 'ß',  # eszett (in muß, daß - old spelling)
    0x7F: 'ü',  # lowercase u-umlaut (in zurück, für, Menü)

    # Extended Latin (may appear in some strings)
    0x61: 'á',
    0x62: 'à',
    0x63: 'â',
    0x64: 'ã',
    0x65: 'å',
    0x67: 'ç',
    0x68: 'é',
    0x69: 'è',
    0x6B: 'ë',
    0x6C: 'í',
    0x6D: 'ì',
    0x6E: 'î',
    0x6F: 'ï',
    0x70: 'ñ',
    0x71: 'ó',
    0x72: 'ò',
    0x73: 'ô',
    0x74: 'õ',
    0x76: '°',
    0x77: '•',
    0x78: '£',
}

# Reverse mapping for encoding
FF7_GERMAN_ENCODE_MAP: Dict[str, int] = {
    'Ü': 0x66, 'ä': 0x6A, 'ö': 0x7A, 'ß': 0x7E, 'ü': 0x7F,
    'á': 0x61, 'à': 0x62, 'â': 0x63, 'ã': 0x64, 'å': 0x65,
    'ç': 0x67, 'é': 0x68, 'è': 0x69, 'ë': 0x6B,
    'í': 0x6C, 'ì': 0x6D, 'î': 0x6E, 'ï': 0x6F,
    'ñ': 0x70, 'ó': 0x71, 'ò': 0x72, 'ô': 0x73, 'õ': 0x74,
}

# =============================================================================
# DECODE FUNCTIONS
# =============================================================================

def decode_ff7_german(data: bytes, show_unknown: bool = True) -> str:
    """
    Decode FF7 German encoded bytes to readable text.

    Args:
        data: Raw bytes from ff7_de.exe
        show_unknown: If True, show unknown bytes as [XX]; if False, skip them

    Returns:
        Decoded German string

    Example:
        >>> decode_ff7_german(bytes([0x2D, 0x7A, 0x43, 0x48, 0x54, 0x45, 0x4E, 0xFF]))
        'Möchten'
    """
    result = []
    for b in data:
        if b == 0xFF:
            break  # String terminator
        elif b in FF7_GERMAN_DECODE_MAP:
            result.append(FF7_GERMAN_DECODE_MAP[b])
        elif b == 0x00:
            result.append(' ')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))  # Standard: byte + 0x20 = ASCII
        else:
            if show_unknown:
                result.append(f'[{b:02X}]')
    return ''.join(result)


def decode_byte(b: int) -> str:
    """Decode a single byte to its character representation."""
    if b == 0xFF:
        return '[END]'
    elif b in FF7_GERMAN_DECODE_MAP:
        return FF7_GERMAN_DECODE_MAP[b]
    elif b == 0x00:
        return ' '
    elif 0x01 <= b <= 0x5F:
        return chr(b + 0x20)
    else:
        return f'[{b:02X}]'


# =============================================================================
# ENCODE FUNCTIONS
# =============================================================================

def encode_ff7_german(text: str, add_terminator: bool = True) -> bytes:
    """
    Encode German text to FF7 format.

    Args:
        text: German string to encode
        add_terminator: If True, append 0xFF terminator

    Returns:
        FF7 encoded bytes

    Raises:
        ValueError: If text contains unencodable characters

    Example:
        >>> encode_ff7_german('Möchten')
        b'\\x2d\\x7a\\x43\\x48\\x54\\x45\\x4e\\xff'
    """
    result = []
    for c in text:
        if c in FF7_GERMAN_ENCODE_MAP:
            result.append(FF7_GERMAN_ENCODE_MAP[c])
        elif c == ' ':
            result.append(0x00)
        elif 0x21 <= ord(c) <= 0x7F:
            result.append(ord(c) - 0x20)
        else:
            raise ValueError(f"Cannot encode character: {c!r} (U+{ord(c):04X})")
    if add_terminator:
        result.append(0xFF)
    return bytes(result)


def can_encode(text: str) -> bool:
    """Check if text can be encoded to FF7 German format."""
    try:
        encode_ff7_german(text, add_terminator=False)
        return True
    except ValueError:
        return False


# =============================================================================
# FILE OPERATIONS
# =============================================================================

def read_string_at(filepath: str, offset: int, max_length: int = 256) -> tuple[bytes, str]:
    """
    Read and decode a string from an exe file at the given offset.

    Args:
        filepath: Path to ff7_de.exe
        offset: File offset to read from
        max_length: Maximum bytes to read

    Returns:
        Tuple of (raw_bytes, decoded_string)
    """
    with open(filepath, 'rb') as f:
        f.seek(offset)
        raw = f.read(max_length)

    # Find terminator
    term_pos = raw.find(b'\xff')
    if term_pos != -1:
        raw = raw[:term_pos + 1]

    decoded = decode_ff7_german(raw)
    return raw, decoded


def extract_strings(filepath: str, start: int, end: int) -> list[tuple[int, bytes, str]]:
    """
    Extract all strings from a region of the exe.

    Args:
        filepath: Path to ff7_de.exe
        start: Start offset
        end: End offset

    Returns:
        List of (offset, raw_bytes, decoded_string) tuples
    """
    with open(filepath, 'rb') as f:
        f.seek(start)
        region = f.read(end - start)

    strings = []
    current_string = []
    string_start = 0

    for i, b in enumerate(region):
        if b == 0xFF:
            if current_string:
                raw = bytes(current_string)
                decoded = decode_ff7_german(raw)
                # Only include if it looks like text (has letters)
                if any(c.isalpha() for c in decoded):
                    strings.append((start + string_start, raw, decoded))
                current_string = []
            string_start = i + 1
        else:
            if not current_string:
                string_start = i
            current_string.append(b)

    return strings


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def print_help():
    """Print usage help."""
    print("""
FF7 German String Decoder
=========================

Usage:
    python ff7_german_decoder.py decode <hex_string>
        Decode a hex string to German text
        Example: python ff7_german_decoder.py decode 2d7a434854454eff

    python ff7_german_decoder.py encode <text>
        Encode German text to FF7 hex format
        Example: python ff7_german_decoder.py encode "Möchten"

    python ff7_german_decoder.py read <exe_path> <offset> [length]
        Read and decode a string from exe at offset
        Example: python ff7_german_decoder.py read ff7_de.exe 0x58FBB0 50

    python ff7_german_decoder.py extract <exe_path> <start> <end>
        Extract all strings from exe region
        Example: python ff7_german_decoder.py extract ff7_de.exe 0x58FB00 0x5A0000

    python ff7_german_decoder.py charmap
        Print the complete character map

German Special Characters:
    ä = 0x6A    Ü = 0x66    ß = 0x7E
    ö = 0x7A    ü = 0x7F
""")


def print_charmap():
    """Print the complete character map."""
    print("\nFF7 German Character Map")
    print("=" * 60)
    print("\nStandard range (0x00-0x5F): byte + 0x20 = ASCII\n")

    for row_start in range(0, 0x60, 0x10):
        chars = []
        for offset in range(16):
            b = row_start + offset
            if b == 0x00:
                chars.append('SPC')
            elif 0x01 <= b <= 0x5F:
                chars.append(chr(b + 0x20))
            else:
                chars.append('?')
        print(f"0x{row_start:02X}: " + " | ".join(f"{c:3}" for c in chars))

    print("\nGerman special characters (0x60+):\n")
    for row_start in range(0x60, 0x80, 0x10):
        chars = []
        for offset in range(16):
            b = row_start + offset
            if b in FF7_GERMAN_DECODE_MAP:
                chars.append(FF7_GERMAN_DECODE_MAP[b])
            else:
                chars.append('?')
        print(f"0x{row_start:02X}: " + " | ".join(f"{c:3}" for c in chars))

    print("\nKey German mappings:")
    print("  0x66 = Ü (uppercase)")
    print("  0x6A = ä (lowercase)")
    print("  0x7A = ö (lowercase)")
    print("  0x7E = ß (eszett)")
    print("  0x7F = ü (lowercase)")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == 'decode':
        if len(sys.argv) < 3:
            print("Error: Missing hex string")
            return
        hex_str = sys.argv[2].replace(' ', '').replace('0x', '')
        try:
            data = bytes.fromhex(hex_str)
            decoded = decode_ff7_german(data)
            print(f"Decoded: {decoded}")
        except ValueError as e:
            print(f"Error: Invalid hex string - {e}")

    elif command == 'encode':
        if len(sys.argv) < 3:
            print("Error: Missing text to encode")
            return
        text = sys.argv[2]
        try:
            encoded = encode_ff7_german(text)
            print(f"Encoded: {encoded.hex()}")
            print(f"Bytes: {' '.join(f'{b:02X}' for b in encoded)}")
        except ValueError as e:
            print(f"Error: {e}")

    elif command == 'read':
        if len(sys.argv) < 4:
            print("Error: Missing exe path and/or offset")
            return
        exe_path = sys.argv[2]
        offset = int(sys.argv[3], 0)  # Handles both decimal and 0x hex
        length = int(sys.argv[4], 0) if len(sys.argv) > 4 else 100
        try:
            raw, decoded = read_string_at(exe_path, offset, length)
            print(f"Offset: 0x{offset:06X}")
            print(f"Raw: {raw.hex()}")
            print(f"Decoded: {decoded}")
        except FileNotFoundError:
            print(f"Error: File not found - {exe_path}")
        except Exception as e:
            print(f"Error: {e}")

    elif command == 'extract':
        if len(sys.argv) < 5:
            print("Error: Missing exe path, start, or end offset")
            return
        exe_path = sys.argv[2]
        start = int(sys.argv[3], 0)
        end = int(sys.argv[4], 0)
        try:
            strings = extract_strings(exe_path, start, end)
            print(f"Found {len(strings)} strings:\n")
            for offset, raw, decoded in strings[:50]:  # Limit output
                print(f"0x{offset:06X}: {decoded[:60]}")
            if len(strings) > 50:
                print(f"\n... and {len(strings) - 50} more")
        except FileNotFoundError:
            print(f"Error: File not found - {exe_path}")
        except Exception as e:
            print(f"Error: {e}")

    elif command == 'charmap':
        print_charmap()

    elif command in ('help', '-h', '--help'):
        print_help()

    else:
        print(f"Unknown command: {command}")
        print_help()


if __name__ == '__main__':
    main()
