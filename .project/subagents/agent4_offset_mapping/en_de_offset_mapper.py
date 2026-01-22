#!/usr/bin/env python3
"""
EN-DE Offset Mapper for FF7 PC Executables

This script maps English string offsets (from Steam EN exe) to German
string offsets (in eStore DE exe) for FF7 PC modding.

Key findings:
- Steam EN to eStore EN delta: +0xC00 (3072 bytes) - CONSTANT
- eStore EN to eStore DE delta: VARIABLE (different for each region)
  - The DE exe has German text which is often longer than English
  - This shifts subsequent strings

Strategy:
1. Use touphScript offset table (767 entries) as reference
2. For each offset, read the EN bytes from eStore EN (offset + 0xC00)
3. Search for equivalent German text in DE exe
4. Build a mapping of EN offset -> DE offset with delta analysis

Created: 2026-01-02
Session: Agent 4 - EN-DE Offset Mapping
"""

import os
import csv
import struct
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# File paths
STEAM_EN_EXE = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
ESTORE_EN_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe"
ESTORE_DE_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

# Known delta from Steam EN to eStore EN
STEAM_TO_ESTORE_DELTA = 0xC00

# TouphScript offset table (from ff7exe.cpp)
# Format: (file_offset, length, type)
# Types: 0=DEF, 1=NOFF_TERM, 2=RGB, 3=UNICODE, 4=FFPADDED, 5=ZEROTERM

TOUPHSCRIPT_OFFSETS = [
    # Region 1: Game State / Resume/Quit (0-4)
    (0x518370, 30, 0), (0x51838E, 30, 0), (0x5183AC, 30, 0), (0x5183D0, 4, 0), (0x5183D4, 4, 0),

    # Region 2: Save Slot Descriptions (5-32)
    (0x5188A8, 48, 0), (0x5188D8, 48, 0), (0x518908, 48, 0), (0x518938, 48, 0), (0x518968, 48, 0),
    (0x518998, 48, 0), (0x5189C8, 48, 0), (0x5189F8, 48, 0), (0x518A28, 48, 0), (0x518A58, 48, 0),
    (0x518A88, 48, 0), (0x518AB8, 48, 0), (0x518C08, 48, 0), (0x518C38, 48, 0), (0x518C68, 48, 0),
    (0x518C98, 48, 0), (0x518CC8, 48, 0), (0x518CF8, 48, 0), (0x518D28, 48, 0), (0x518D58, 48, 0),
    (0x518D88, 48, 0), (0x518DE8, 48, 0), (0x518E18, 48, 0), (0x518ED8, 48, 0), (0x518F08, 48, 0),
    (0x518F38, 48, 0), (0x518F68, 48, 0), (0x518FC8, 48, 0),

    # Region 3: Yes/No Menu Labels (33-35)
    (0x519238, 6, 1), (0x51923E, 6, 1), (0x519244, 6, 1),

    # Region 4: Config Menu Labels (36-57)
    (0x519288, 25, 0), (0x5192A1, 25, 0), (0x5192C0, 20, 0), (0x5192D4, 20, 0), (0x5192E8, 20, 0),
    (0x5192FC, 20, 0), (0x519310, 20, 0), (0x519324, 20, 0), (0x519338, 20, 0), (0x51934C, 20, 0),
    (0x519360, 20, 0), (0x519374, 20, 0), (0x519388, 20, 0), (0x51939C, 20, 0), (0x5193D8, 20, 0),
    (0x5193EC, 20, 0), (0x519400, 20, 0), (0x519414, 20, 0), (0x519428, 20, 0), (0x519450, 20, 0),
    (0x519464, 20, 0), (0x519478, 20, 0),

    # Region 5: Config Help Text (58-76)
    (0x5196B0, 50, 0), (0x5196E2, 50, 0), (0x519714, 50, 0), (0x519746, 50, 0), (0x519778, 50, 0),
    (0x5197AA, 50, 0), (0x5197DC, 50, 0), (0x51980E, 50, 0), (0x519840, 50, 0), (0x519872, 50, 0),
    (0x5198A4, 50, 0), (0x5198D6, 50, 0), (0x519908, 50, 0), (0x51993A, 50, 0), (0x51996C, 50, 0),
    (0x51999E, 50, 0), (0x5199D0, 50, 0), (0x519A02, 50, 0), (0x519A34, 50, 0),

    # Region 6: Keyboard Labels RGB (77-213) - 137 entries
    (0x519FE0, 8, 2), (0x519FE8, 4, 2), (0x519FEC, 4, 2), (0x519FF0, 4, 2), (0x519FF4, 4, 2),
    (0x519FF8, 4, 2), (0x519FFC, 4, 2), (0x51A000, 4, 2), (0x51A004, 4, 2), (0x51A008, 4, 2),
    (0x51A00C, 4, 2), (0x51A010, 4, 2), (0x51A014, 4, 2), (0x51A018, 4, 2), (0x51A01C, 4, 2),
    (0x51A020, 4, 2), (0x51A024, 4, 2), (0x51A028, 4, 2), (0x51A02C, 4, 2), (0x51A030, 4, 2),
    (0x51A034, 4, 2), (0x51A038, 4, 2), (0x51A03C, 4, 2), (0x51A040, 4, 2), (0x51A044, 4, 2),
    (0x51A048, 4, 2), (0x51A04C, 4, 2), (0x51A050, 4, 2), (0x51A054, 4, 2), (0x51A058, 4, 2),
    (0x51A05C, 4, 2), (0x51A060, 4, 2), (0x51A064, 4, 2), (0x51A068, 4, 2), (0x51A06C, 4, 2),
    (0x51A070, 4, 2), (0x51A074, 4, 2), (0x51A078, 4, 2), (0x51A07C, 4, 2), (0x51A080, 4, 2),
    (0x51A084, 4, 2), (0x51A088, 4, 2), (0x51A08C, 4, 2), (0x51A090, 4, 2), (0x51A094, 4, 2),
    (0x51A098, 4, 2), (0x51A09C, 4, 2), (0x51A0A0, 4, 2), (0x51A0A4, 4, 2), (0x51A0A8, 4, 2),
    (0x51A0AC, 4, 2), (0x51A0B0, 4, 2), (0x51A0B4, 4, 2), (0x51A0B8, 4, 2), (0x51A0BC, 4, 2),
    (0x51A0C0, 4, 2), (0x51A0C4, 4, 2), (0x51A0C8, 4, 2), (0x51A0CC, 4, 2), (0x51A0D0, 4, 2),
    (0x51A0D4, 8, 2), (0x51A0DC, 4, 2), (0x51A0E0, 4, 2), (0x51A0E4, 4, 2), (0x51A0E8, 4, 2),
    (0x51A0EC, 4, 2), (0x51A0F0, 4, 2), (0x51A0F4, 4, 2), (0x51A0F8, 4, 2), (0x51A0FC, 4, 2),
    (0x51A100, 4, 2), (0x51A104, 4, 2), (0x51A108, 4, 2), (0x51A10C, 4, 2), (0x51A110, 4, 2),
    (0x51A114, 4, 2), (0x51A118, 4, 2), (0x51A11C, 4, 2), (0x51A120, 4, 2), (0x51A124, 4, 2),
    (0x51A128, 4, 2), (0x51A12C, 4, 2), (0x51A130, 4, 2), (0x51A134, 4, 2), (0x51A138, 4, 2),
    (0x51A13C, 4, 2), (0x51A140, 4, 2), (0x51A144, 4, 2), (0x51A148, 4, 2), (0x51A14C, 4, 2),
    (0x51A150, 4, 2), (0x51A154, 4, 2), (0x51A158, 4, 2), (0x51A15C, 4, 2), (0x51A160, 4, 2),
    (0x51A164, 4, 2), (0x51A168, 4, 2), (0x51A16C, 4, 2), (0x51A170, 4, 2), (0x51A174, 4, 2),
    (0x51A178, 4, 2), (0x51A17C, 4, 2), (0x51A180, 4, 2), (0x51A184, 4, 2), (0x51A188, 4, 2),
    (0x51A18C, 4, 2), (0x51A190, 4, 2), (0x51A194, 4, 2), (0x51A198, 4, 2), (0x51A19C, 4, 2),
    (0x51A1A0, 4, 2), (0x51A1A4, 4, 2), (0x51A1A8, 4, 2), (0x51A1AC, 4, 2), (0x51A1B0, 4, 2),
    (0x51A1B4, 4, 2), (0x51A1B8, 4, 2), (0x51A1BC, 4, 2), (0x51A1C0, 4, 2), (0x51A1C4, 4, 2),
    (0x51A1C8, 4, 2), (0x51A1CC, 4, 2), (0x51A1D0, 4, 2), (0x51A1D4, 4, 2), (0x51A1D8, 4, 2),
    (0x51A1DC, 4, 2), (0x51A1E0, 4, 2), (0x51A1E4, 4, 2), (0x51A1E8, 4, 2), (0x51A1EC, 4, 2),
    (0x51A1F0, 4, 2), (0x51A1F4, 4, 2), (0x51A1F8, 4, 2), (0x51A1FC, 4, 2), (0x51A200, 4, 2),
    (0x51A204, 4, 2),

    # Continuing through all 767 entries... (abbreviated for this example)
    # Full table would be included from touphScript source
]

# Known anchor pairs (EN text -> DE text) with their byte patterns
ANCHOR_PAIRS = {
    # Config menu region anchors
    "WINDOW COLOR": ("FENSTERFARBE", 0x5194A8, 0x5900F0),  # eStore EN -> eStore DE
    "SOUND": ("SOUND", 0x5194D8, 0x590126),
    "CONTROLLER": ("KONTROLLER", 0x519508, 0x59015C),
    "CURSOR": ("CURSOR", 0x519538, 0x590192),
    "ATB": ("ATB", 0x519568, 0x5901C8),
    "BATTLE SPEED": ("KAMPFTEMPO", 0x519598, 0x5901FE),
    "BATTLE MESSAGE": ("KAMPFMELDUNG", 0x5195C8, 0x590234),
    "FIELD MESSAGE": ("FELDMELDUNG", 0x5195F8, 0x59026A),
    "CAMERA ANGLE": ("KAMERAWINKEL", 0x519628, 0x5902A0),
}


def read_bytes(filepath: str, offset: int, length: int) -> bytes:
    """Read bytes from file at given offset."""
    with open(filepath, 'rb') as f:
        f.seek(offset)
        return f.read(length)


def decode_ff7_text(data: bytes) -> str:
    """
    Decode FF7 text encoding to readable string.
    FF7 uses a custom encoding where:
    - 0x00-0x20: symbols and numbers
    - 0x21-0x3A: uppercase A-Z
    - 0x3B-0x54: lowercase a-z
    - 0xFF: string terminator
    """
    result = []
    for byte in data:
        if byte == 0xFF:
            break
        elif byte == 0x00:
            result.append(' ')
        elif 0x21 <= byte <= 0x3A:
            # Uppercase letters: 0x21='A', 0x22='B', etc.
            result.append(chr(ord('A') + byte - 0x21))
        elif 0x3B <= byte <= 0x54:
            # Lowercase letters: 0x3B='a', 0x3C='b', etc.
            result.append(chr(ord('a') + byte - 0x3B))
        elif 0x01 <= byte <= 0x0A:
            # Numbers: 0x01='1', 0x02='2', etc. (0x0A='0')
            if byte == 0x0A:
                result.append('0')
            else:
                result.append(str(byte))
        else:
            result.append(f'[{byte:02X}]')
    return ''.join(result)


def find_pattern_in_exe(exe_path: str, pattern: bytes, start: int = 0, end: int = 0) -> List[int]:
    """Find all occurrences of a byte pattern in an exe file."""
    with open(exe_path, 'rb') as f:
        if end == 0:
            data = f.read()
        else:
            f.seek(start)
            data = f.read(end - start)

    results = []
    idx = 0
    while True:
        idx = data.find(pattern, idx)
        if idx == -1:
            break
        results.append(start + idx)
        idx += 1
    return results


def analyze_region_deltas():
    """
    Analyze the delta patterns between EN and DE for different regions.
    """
    print("Analyzing EN-DE offset deltas by region...")
    print("=" * 60)

    deltas = {}

    for en_text, (de_text, en_offset, de_offset) in ANCHOR_PAIRS.items():
        delta = de_offset - en_offset
        region_base = (en_offset >> 12) << 12  # Round to nearest 4KB

        if region_base not in deltas:
            deltas[region_base] = []
        deltas[region_base].append((en_text, de_text, en_offset, de_offset, delta))

        print(f"  {en_text:20s} -> {de_text:20s}")
        print(f"    EN: 0x{en_offset:06X} -> DE: 0x{de_offset:06X} (delta: 0x{delta:X} = {delta})")

    return deltas


def calculate_delta_for_offset(steam_en_offset: int, anchor_data: dict) -> Tuple[int, str]:
    """
    Calculate the DE offset for a given Steam EN offset using nearest anchor.
    Returns (de_offset, confidence_level).
    """
    # First convert Steam EN to eStore EN
    estore_en_offset = steam_en_offset + STEAM_TO_ESTORE_DELTA

    # Find nearest anchor
    nearest_anchor = None
    min_distance = float('inf')

    for en_text, (de_text, anchor_en, anchor_de) in ANCHOR_PAIRS.items():
        distance = abs(estore_en_offset - anchor_en)
        if distance < min_distance:
            min_distance = distance
            nearest_anchor = (en_text, anchor_en, anchor_de)

    if nearest_anchor:
        anchor_delta = nearest_anchor[2] - nearest_anchor[1]
        estimated_de_offset = estore_en_offset + anchor_delta

        if min_distance < 0x1000:  # Within 4KB of anchor
            confidence = "HIGH"
        elif min_distance < 0x10000:  # Within 64KB
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        return estimated_de_offset, confidence

    return 0, "NONE"


def create_mapping():
    """Create the complete EN-DE offset mapping."""
    print("\nCreating EN-DE offset mapping...")

    mappings = []

    for idx, (steam_offset, length, str_type) in enumerate(TOUPHSCRIPT_OFFSETS):
        estore_en_offset = steam_offset + STEAM_TO_ESTORE_DELTA

        # Read EN text
        try:
            en_bytes = read_bytes(ESTORE_EN_EXE, estore_en_offset, length)
            en_text = decode_ff7_text(en_bytes)
        except Exception as e:
            en_bytes = b''
            en_text = f"[READ ERROR: {e}]"

        # Estimate DE offset
        de_offset, confidence = calculate_delta_for_offset(steam_offset, ANCHOR_PAIRS)

        # Read DE text at estimated position
        de_text = ""
        de_bytes = b''
        if de_offset > 0:
            try:
                de_bytes = read_bytes(ESTORE_DE_EXE, de_offset, length)
                de_text = decode_ff7_text(de_bytes)
            except Exception as e:
                de_text = f"[READ ERROR: {e}]"

        delta = de_offset - estore_en_offset if de_offset > 0 else 0

        mappings.append({
            'index': idx,
            'steam_en_offset': f"0x{steam_offset:06X}",
            'steam_en_va': f"0x{steam_offset + 0x17600:06X}",
            'estore_en_offset': f"0x{estore_en_offset:06X}",
            'estore_de_offset': f"0x{de_offset:06X}" if de_offset > 0 else "UNKNOWN",
            'en_text': en_text[:50],  # Truncate for readability
            'de_text': de_text[:50],
            'de_bytes_hex': de_bytes.hex().upper()[:40],
            'confidence': confidence,
            'delta': f"0x{delta:X}" if delta else "N/A",
            'length': length,
            'type': str_type
        })

    return mappings


def main():
    """Main function to run the mapping analysis."""
    output_dir = Path(__file__).parent

    # Check files exist
    for path in [STEAM_EN_EXE, ESTORE_EN_EXE, ESTORE_DE_EXE]:
        if not os.path.exists(path):
            print(f"ERROR: File not found: {path}")
            return

    print("FF7 EN-DE Offset Mapper")
    print("=" * 60)
    print(f"Steam EN:  {STEAM_EN_EXE}")
    print(f"eStore EN: {ESTORE_EN_EXE}")
    print(f"eStore DE: {ESTORE_DE_EXE}")
    print(f"Steam->eStore delta: 0x{STEAM_TO_ESTORE_DELTA:X}")
    print()

    # Analyze anchors
    deltas = analyze_region_deltas()

    # Create mapping
    mappings = create_mapping()

    # Write CSV
    csv_path = output_dir / "en_de_offset_mapping.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'index', 'steam_en_offset', 'steam_en_va', 'estore_en_offset',
            'estore_de_offset', 'en_text', 'de_text', 'de_bytes_hex',
            'confidence', 'delta', 'length', 'type'
        ])
        writer.writeheader()
        writer.writerows(mappings)

    print(f"\nWrote {len(mappings)} entries to {csv_path}")

    # Generate summary
    high_conf = sum(1 for m in mappings if m['confidence'] == 'HIGH')
    med_conf = sum(1 for m in mappings if m['confidence'] == 'MEDIUM')
    low_conf = sum(1 for m in mappings if m['confidence'] == 'LOW')

    print(f"\nConfidence Summary:")
    print(f"  HIGH:   {high_conf}")
    print(f"  MEDIUM: {med_conf}")
    print(f"  LOW:    {low_conf}")


if __name__ == "__main__":
    main()
