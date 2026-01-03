#!/usr/bin/env python3
"""
Decode German FF7 menu strings from touphScript hex encoding.

Usage:
    python decode_german_touphscript.py [offset] [hex_bytes]

    Example:
    python decode_german_touphscript.py 0x5D8945 "2F 42 4A 45 4B 54"

Output:
    Decoded text with explanation of each byte
"""

import sys
import re

# touphScript character lookup table (0x00-0x7F)
# Based on FF7 PC English version with German extensions
TOUPHSCRIPT = {
    # Control / spacing
    0x00: ' ',        # NULL / space
    0x01: '[?]',      # Unknown control
    0x20: ' ',        # Space

    # Punctuation
    0x21: '!',
    0x22: '"',
    0x23: '#',
    0x24: '$',
    0x25: '%',
    0x26: '&',
    0x27: "'",
    0x28: '(',
    0x29: ')',
    0x2A: '*',
    0x2B: '+',
    0x2C: ',',
    0x2D: '-',
    0x2E: '.',
    0x2F: '/',

    # Numbers
    0x30: '0', 0x31: '1', 0x32: '2', 0x33: '3', 0x34: '4',
    0x35: '5', 0x36: '6', 0x37: '7', 0x38: '8', 0x39: '9',

    # More punctuation
    0x3A: ':', 0x3B: ';', 0x3C: '<', 0x3D: '=', 0x3E: '>', 0x3F: '?', 0x40: '@',

    # Uppercase letters
    0x41: 'A', 0x42: 'B', 0x43: 'C', 0x44: 'D', 0x45: 'E', 0x46: 'F', 0x47: 'G',
    0x48: 'H', 0x49: 'I', 0x4A: 'J', 0x4B: 'K', 0x4C: 'L', 0x4D: 'M', 0x4E: 'N',
    0x4F: 'O', 0x50: 'P', 0x51: 'Q', 0x52: 'R', 0x53: 'S', 0x54: 'T', 0x55: 'U',
    0x56: 'V', 0x57: 'W', 0x58: 'X', 0x59: 'Y', 0x5A: 'Z',

    # More punctuation
    0x5B: '[', 0x5C: '\\', 0x5D: ']', 0x5E: '^', 0x5F: '_', 0x60: '`',

    # Lowercase letters
    0x61: 'a', 0x62: 'b', 0x63: 'c', 0x64: 'd', 0x65: 'e', 0x66: 'f', 0x67: 'g',
    0x68: 'h', 0x69: 'i', 0x6A: 'j', 0x6B: 'k', 0x6C: 'l', 0x6D: 'm', 0x6E: 'n',
    0x6F: 'o', 0x70: 'p', 0x71: 'q', 0x72: 'r', 0x73: 's', 0x74: 't', 0x75: 'u',
    0x76: 'v', 0x77: 'w', 0x78: 'x', 0x79: 'y', 0x7A: 'z',

    # German extensions
    0x7F: 'ü',  # u-umlaut

    # Additional special mappings (to be discovered)
    # 0x80-0xFE: Unknown extensions

    # Terminator
    0xFF: '[END]',
}

# Known German menu items (for quick reference)
KNOWN_ITEMS = {
    (0x2F, 0x42, 0x4A, 0x45, 0x4B, 0x54): 'Objekt (Item)',
    (0x3A, 0x41, 0x55, 0x42, 0x45, 0x52): 'Zauber (Magic)',
    (0x2D, 0x41, 0x54, 0x45, 0x52, 0x49, 0x41): 'Materia',
    (0x21, 0x55, 0x53, 0x52, 0x7F, 0x53, 0x54, 0x45, 0x4E): 'Ausrüsten (Equip)',
    (0x37, 0x45, 0x52, 0x54, 0x45): 'Werte (Status)',
    (0x32, 0x45, 0x49, 0x48, 0x45): 'Reihe (Order)',
    (0x2C, 0x49, 0x4D, 0x49, 0x54): 'Limit',
    (0x2B, 0x4F, 0x4E, 0x46, 0x49, 0x47): 'Konfig (Config)',
    (0x30, 0x28, 0x33): 'PHS',
    (0x33, 0x50, 0x45, 0x49, 0x43, 0x48, 0x45, 0x52, 0x4E): 'Speichern (Save)',
    (0x36, 0x45, 0x52, 0x4C, 0x41, 0x53, 0x53, 0x45, 0x4E): 'Verlassen (Quit)',
}


def parse_hex_string(hex_str):
    """Convert hex string to tuple of byte values."""
    # Remove common formatting
    hex_str = hex_str.replace('0x', '').replace('0X', '')
    hex_str = hex_str.replace(',', ' ').replace('-', ' ')

    # Split and convert
    hex_parts = hex_str.split()
    try:
        return tuple(int(part, 16) for part in hex_parts if part)
    except ValueError:
        return None


def decode_bytes(byte_tuple):
    """Decode tuple of bytes to string and explanation."""
    if not byte_tuple:
        return None, None, None

    # Check if it's a known item
    known = KNOWN_ITEMS.get(byte_tuple)

    # Decode character by character
    decoded_chars = []
    explanations = []

    for byte_val in byte_tuple:
        if byte_val == 0xFF:
            decoded_chars.append('[END]')
            explanations.append(f'0x{byte_val:02X}: String terminator')
            break

        char = TOUPHSCRIPT.get(byte_val, f'[0x{byte_val:02X}]')
        decoded_chars.append(char)

        if byte_val < 0x20:
            explanations.append(f'0x{byte_val:02X}: Control code')
        elif byte_val == 0x20:
            explanations.append(f'0x{byte_val:02X}: Space')
        elif 0x21 <= byte_val <= 0x2F:
            explanations.append(f'0x{byte_val:02X}: {char} (punctuation)')
        elif 0x30 <= byte_val <= 0x39:
            explanations.append(f'0x{byte_val:02X}: {char} (digit)')
        elif 0x41 <= byte_val <= 0x5A:
            explanations.append(f'0x{byte_val:02X}: {char} (uppercase)')
        elif 0x61 <= byte_val <= 0x7A:
            explanations.append(f'0x{byte_val:02X}: {char} (lowercase)')
        elif byte_val == 0x7F:
            explanations.append(f'0x{byte_val:02X}: {char} (German umlaut)')
        else:
            explanations.append(f'0x{byte_val:02X}: {char} (extended)')

    decoded_text = ''.join(decoded_chars).replace('[END]', '')

    return decoded_text, explanations, known


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # Interactive mode
        print("=" * 80)
        print("FF7 German touphScript Decoder")
        print("=" * 80)
        print()

        while True:
            try:
                hex_input = input("Enter hex bytes (or 'quit' to exit): ").strip()
                if hex_input.lower() in ('quit', 'exit', 'q'):
                    break

                byte_tuple = parse_hex_string(hex_input)
                if byte_tuple is None:
                    print("ERROR: Invalid hex format")
                    continue

                decoded_text, explanations, known = decode_bytes(byte_tuple)

                print()
                print("DECODED TEXT:")
                print(f"  Result: {decoded_text}")
                if known:
                    print(f"  Match: {known}")

                print("\nBYTE-BY-BYTE ANALYSIS:")
                for expl in explanations:
                    print(f"  {expl}")
                print()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"ERROR: {e}")

    else:
        # Command line mode
        hex_input = ' '.join(sys.argv[1:])

        byte_tuple = parse_hex_string(hex_input)
        if byte_tuple is None:
            print("ERROR: Invalid hex format")
            sys.exit(1)

        decoded_text, explanations, known = decode_bytes(byte_tuple)

        print()
        print("=" * 80)
        print("DECODED TEXT")
        print("=" * 80)
        print(f"Result: {decoded_text}")
        if known:
            print(f"Known Item: {known}")

        print()
        print("=" * 80)
        print("BYTE-BY-BYTE BREAKDOWN")
        print("=" * 80)
        for expl in explanations:
            print(expl)
        print()


if __name__ == '__main__':
    main()
