#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator

Generates HEXT patches to replace English exe strings with German equivalents.
Uses the offset table from touphScript ff7exe.cpp and maps to German text from
eStore's ff7_de.exe.

Created: 2026-01-01 18:40 JST
Session: 2e703ab4-4b5e-4772-8894-ba089b4f437c
Context: Automates creation of HEXT patches for German menu text in FF7 English exe.
         The German exe has strings in same order but at different offsets due to
         longer German text.

Usage:
    python3 generate_german_hext.py --de <de_exe> -o german_menu.txt
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import IntEnum


# =============================================================================
# CONSTANTS - From touphScript ff7exe.cpp (same as Japanese generator)
# =============================================================================

class StringType(IntEnum):
    DEF = 0        # Standard FF7 encoding with FF terminator
    NOFF_TERM = 1  # No FF terminator in file
    RGB = 2        # RGB encoded (ASCII + 0x73)
    UNICODE = 3    # Windows Unicode strings
    FFPADDED = 4   # FF7 encoding padded with FF bytes
    ZEROTERM = 5   # Zero-terminated string

# Import offset tables from the Japanese generator (they're identical - same touphScript source)
# This avoids duplicating 758 entries
import sys
sys.path.insert(0, str(Path(__file__).parent))
from generate_exe_hext import EN_OFFSETS, STRING_LENGTHS, STRING_TYPES

# =============================================================================
# SKIP REGIONS - German-specific
# =============================================================================

# These regions don't need German patches (same as Japanese skip regions)
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry characters (UNICODE type)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals and related
SKIP_REGIONS.update(range(712, 758))   # Chocobo jockey names

# Keyboard region (77-213) - These may need special handling for German
# German keyboards have different labels but FF7 likely keeps English key names
KEYBOARD_REGION = set(range(77, 214))


# =============================================================================
# CHARACTER ENCODING
# =============================================================================

def decode_ff7_english(data: bytes) -> str:
    """Decode English/German FF7 string (Western encoding)."""
    result = []
    for byte in data:
        if byte == 0xFF:
            break
        if byte == 0x00:
            result.append(' ')
        elif 0x01 <= byte <= 0x5F:
            result.append(chr(byte + 0x20))
        elif 0x60 <= byte <= 0x7F:
            # Extended Latin characters (umlauts, etc.)
            # These map to extended ASCII
            result.append(chr(byte + 0x20))
        else:
            result.append(f'[{byte:02X}]')
    return ''.join(result)


def file_offset_to_va(file_offset: int) -> int:
    """Convert file offset to Virtual Address for HEXT."""
    return (file_offset - 0x3B8A00) + 0x3BA000 + 0x400000


# =============================================================================
# GERMAN STRING EXTRACTION
# =============================================================================

def find_german_strings(de_exe_path: Path, start_offset: int = 0x5900F0) -> List[Tuple[int, bytes, str]]:
    """
    Extract German strings from ff7_de.exe.
    Returns list of (offset, raw_bytes, decoded_text).

    German strings start around 0x5900F0 in eStore's ff7_de.exe.
    """
    strings = []

    with open(de_exe_path, 'rb') as f:
        data = f.read()

    pos = start_offset
    max_strings = 800  # Safety limit

    while len(strings) < max_strings and pos < len(data) - 2:
        # Find next 0xFF terminator
        next_ff = data.find(b'\xff', pos)
        if next_ff == -1 or next_ff > pos + 200:  # Max string length
            break

        # Extract string bytes
        string_bytes = data[pos:next_ff + 1]

        # Skip if too short or looks like binary data
        if len(string_bytes) >= 2:
            decoded = decode_ff7_english(string_bytes)
            # Only keep if it has printable content
            printable = sum(1 for c in decoded if c.isalnum())
            if printable >= 1:
                strings.append((pos, string_bytes, decoded))

        # Move to next string (skip 0xFF and any 0x00 padding)
        pos = next_ff + 1
        while pos < len(data) and data[pos] == 0x00:
            pos += 1

    return strings


# =============================================================================
# HEXT GENERATION
# =============================================================================

@dataclass
class PatchEntry:
    """Represents a single HEXT patch entry."""
    index: int
    en_offset: int
    de_text: str
    length: int
    string_type: StringType
    de_bytes: bytes


def generate_hext(de_exe: Path, output: Path, session_id: str) -> None:
    """Generate HEXT patch file for German."""

    # Extract German strings
    print("Extracting German strings from ff7_de.exe...")
    de_strings = find_german_strings(de_exe)
    print(f"Found {len(de_strings)} German strings")

    # Show first few for verification
    print("\nFirst 10 German strings:")
    for i, (offset, raw, text) in enumerate(de_strings[:10]):
        print(f"  {i}: 0x{offset:06X}: '{text[:40]}...' ({len(raw)} bytes)")

    patches = []

    # Match German strings to English offsets by position
    for i, en_offset in enumerate(EN_OFFSETS):
        if i >= len(de_strings):
            print(f"Warning: Ran out of German strings at index {i}")
            break

        if i in SKIP_REGIONS:
            continue

        if i >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[i]
        stype = STRING_TYPES[i] if i < len(STRING_TYPES) else 0

        de_offset, de_bytes, de_text = de_strings[i]

        # Create patch entry
        patches.append(PatchEntry(
            index=i,
            en_offset=en_offset,
            de_text=de_text,
            length=length,
            string_type=StringType(stype),
            de_bytes=de_bytes
        ))

    # Write HEXT file
    print(f"\nWriting {len(patches)} patches to {output}")

    with open(output, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Session: {session_id}\n")
        f.write("#\n")
        f.write(f"# Source DE exe: {de_exe.name}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# Virtual addresses calculated from file offsets:\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("#\n\n")

        for patch in patches:
            va = file_offset_to_va(patch.en_offset)

            # Format bytes - pad with 0x00 if German string is shorter
            hex_bytes = ' '.join(f'{b:02X}' for b in patch.de_bytes)
            if len(patch.de_bytes) < patch.length:
                padding = ' '.join('00' for _ in range(patch.length - len(patch.de_bytes)))
                hex_bytes += ' ' + padding

            f.write(f"# Index {patch.index}: '{patch.de_text[:30]}...'\n")
            f.write(f"# EN offset: 0x{patch.en_offset:06X}, Length: {patch.length}\n")
            f.write(f"{va:06X} = {hex_bytes}\n\n")

    print(f"Done! Generated {len(patches)} patches.")


def main():
    parser = argparse.ArgumentParser(description="Generate German HEXT patches for FF7")
    parser.add_argument("--de", required=True, type=Path, help="Path to ff7_de.exe (eStore version)")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Output HEXT file")
    parser.add_argument("--session-id", default="manual", help="Session ID for tracking")

    args = parser.parse_args()

    if not args.de.exists():
        print(f"Error: German exe not found: {args.de}")
        sys.exit(1)

    generate_hext(args.de, args.output, args.session_id)


if __name__ == "__main__":
    main()
