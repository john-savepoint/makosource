#!/usr/bin/env python3
"""
Search for sidebar_flag memory write pattern in FF7 executables.

Pattern: C7 05 D4 1E 92 00 01 00 00 00
This is: MOV DWORD PTR [921ED4], 1

Created: 2025-12-21
Purpose: Find all occurrences of sidebar_flag write in EN and JP executables
"""

import sys

def find_pattern_in_file(filepath, pattern_bytes):
    """Find all occurrences of a byte pattern in a file."""
    with open(filepath, 'rb') as f:
        data = f.read()

    pattern_len = len(pattern_bytes)
    occurrences = []

    pos = 0
    while True:
        idx = data.find(pattern_bytes, pos)
        if idx == -1:
            break
        occurrences.append(idx)
        pos = idx + 1

    return occurrences

def hex_dump_context(filepath, offset, before=16, after=32):
    """Show hex dump around an offset."""
    with open(filepath, 'rb') as f:
        f.seek(max(0, offset - before))
        data = f.read(before + len(PATTERN) + after)

    start_offset = max(0, offset - before)
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_bytes = ' '.join(f'{b:02X}' for b in chunk)
        ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        lines.append(f'{start_offset + i:08X}: {hex_bytes:<48} {ascii_repr}')

    return '\n'.join(lines)

# Pattern: MOV [921ED4], 1
PATTERN = bytes([0xC7, 0x05, 0xD4, 0x1E, 0x92, 0x00, 0x01, 0x00, 0x00, 0x00])

EN_EXE = '/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe'
JP_EXE = '/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_ja.exe'

print("="*80)
print("SIDEBAR_FLAG PATTERN SEARCH")
print("="*80)
print(f"Pattern: {' '.join(f'{b:02X}' for b in PATTERN)}")
print(f"Meaning: MOV DWORD PTR [921ED4], 1 (set sidebar_flag to 1)")
print()

print("="*80)
print("ENGLISH EXE (ff7_en.exe)")
print("="*80)
en_occurrences = find_pattern_in_file(EN_EXE, PATTERN)
print(f"Found {len(en_occurrences)} occurrence(s)")
print()

for i, offset in enumerate(en_occurrences, 1):
    va = offset - 0x400 + 0x401000  # Convert file offset to VA
    print(f"Occurrence #{i}:")
    print(f"  File offset (hex dump): 0x{offset:06X}")
    print(f"  Virtual Address (disassembler): 0x{va:08X}")
    print()
    print("  Context (hex dump):")
    print(hex_dump_context(EN_EXE, offset))
    print()

print("="*80)
print("JAPANESE EXE (ff7_ja.exe)")
print("="*80)
jp_occurrences = find_pattern_in_file(JP_EXE, PATTERN)
print(f"Found {len(jp_occurrences)} occurrence(s)")
print()

for i, offset in enumerate(jp_occurrences, 1):
    va = offset - 0x400 + 0x401000  # Convert file offset to VA
    print(f"Occurrence #{i}:")
    print(f"  File offset (hex dump): 0x{offset:06X}")
    print(f"  Virtual Address (disassembler): 0x{va:08X}")
    print()
    print("  Context (hex dump):")
    print(hex_dump_context(JP_EXE, offset))
    print()

print("="*80)
print("SUMMARY")
print("="*80)
print(f"English EXE: {len(en_occurrences)} occurrence(s)")
print(f"Japanese EXE: {len(jp_occurrences)} occurrence(s)")
print()

if len(en_occurrences) != len(jp_occurrences):
    print("⚠️ DIFFERENT COUNT - This indicates structural differences!")
    print()
    if len(en_occurrences) > len(jp_occurrences):
        print(f"EN has {len(en_occurrences) - len(jp_occurrences)} more occurrence(s)")
        print("This might explain why Cancel patch breaks Start button in EN exe")
    else:
        print(f"JP has {len(jp_occurrences) - len(en_occurrences)} more occurrence(s)")
else:
    print("✓ Same count in both executables")
    print()
    print("Offset comparison:")
    for i in range(len(en_occurrences)):
        en_offset = en_occurrences[i]
        jp_offset = jp_occurrences[i]
        diff = jp_offset - en_offset
        print(f"  Occurrence #{i+1}: EN 0x{en_offset:06X}, JP 0x{jp_offset:06X}, diff +0x{diff:X}")
