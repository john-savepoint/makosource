#!/usr/bin/env python3
"""
Analyze Cancel and Start button code in detail.

Focus on occurrence #2 (Cancel) and #4 (Start) from previous search.
Looking for differences between EN and JP executables.

Created: 2025-12-21
"""

import sys

def hex_dump_with_disasm_hints(filepath, offset, size=64):
    """Show hex dump with disassembly hints."""
    with open(filepath, 'rb') as f:
        f.seek(offset)
        data = f.read(size)

    lines = []
    i = 0
    while i < len(data):
        chunk_offset = offset + i
        va = chunk_offset - 0x400 + 0x401000

        # Read bytes
        b = data[i:i+16]
        hex_bytes = ' '.join(f'{x:02X}' for x in b)

        # Try to identify instruction
        hint = ""
        if i < len(data) and data[i] == 0x85 and i+1 < len(data) and data[i+1] == 0xC0:
            hint = "  ; TEST EAX,EAX"
        elif i < len(data) and data[i] == 0x74 and i+1 < len(data):
            jump_offset = data[i+1] if data[i+1] < 128 else data[i+1] - 256
            hint = f"  ; JE +{jump_offset:02X}"
        elif i < len(data) and data[i] == 0xEB and i+1 < len(data):
            jump_offset = data[i+1] if data[i+1] < 128 else data[i+1] - 256
            hint = f"  ; JMP +{jump_offset:02X}"
        elif i < len(data) and data[i] == 0xC7 and i+1 < len(data) and data[i+1] == 0x05:
            if i+9 < len(data):
                addr = int.from_bytes(data[i+2:i+6], 'little')
                val = int.from_bytes(data[i+6:i+10], 'little')
                hint = f"  ; MOV [{addr:08X}], {val}"
        elif i < len(data) and data[i] == 0xE8 and i+4 < len(data):
            call_offset = int.from_bytes(data[i+1:i+5], 'little', signed=True)
            target = va + 5 + call_offset
            hint = f"  ; CALL {target:08X}"

        lines.append(f'{chunk_offset:06X} ({va:08X}): {hex_bytes:<48}{hint}')
        i += min(16, len(data) - i)

    return '\n'.join(lines)

EN_EXE = '/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe'
JP_EXE = '/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_ja.exe'

print("="*80)
print("CANCEL BUTTON CODE ANALYSIS (Occurrence #2)")
print("="*80)
print()

# Cancel button code in EN
en_cancel_offset = 0x318551  # Start of button check CALL
print("ENGLISH EXE - Cancel button region:")
print("File offset: 0x318551 (VA: 0x719151)")
print()
print(hex_dump_with_disasm_hints(EN_EXE, en_cancel_offset, 64))
print()

# Cancel button code in JP
jp_cancel_offset = 0x319151  # EN + 0xC00
print("JAPANESE EXE - Cancel button region:")
print("File offset: 0x319151 (VA: 0x719D51)")
print()
print(hex_dump_with_disasm_hints(JP_EXE, jp_cancel_offset, 64))
print()

print("="*80)
print("START BUTTON CODE ANALYSIS (Occurrence #4)")
print("="*80)
print()

# Start button code in EN
en_start_offset = 0x318C12  # Start of button check CALL
print("ENGLISH EXE - Start button region:")
print("File offset: 0x318C12 (VA: 0x719812)")
print()
print(hex_dump_with_disasm_hints(EN_EXE, en_start_offset, 64))
print()

# Start button code in JP
jp_start_offset = 0x319812  # EN + 0xC00
print("JAPANESE EXE - Start button region:")
print("File offset: 0x319812 (VA: 0x71A412)")
print()
print(hex_dump_with_disasm_hints(JP_EXE, jp_start_offset, 64))
print()

print("="*80)
print("BYTE-BY-BYTE COMPARISON - CANCEL")
print("="*80)
print()

with open(EN_EXE, 'rb') as f:
    f.seek(en_cancel_offset)
    en_cancel_bytes = f.read(64)

with open(JP_EXE, 'rb') as f:
    f.seek(jp_cancel_offset)
    jp_cancel_bytes = f.read(64)

differences = []
for i in range(min(len(en_cancel_bytes), len(jp_cancel_bytes))):
    if en_cancel_bytes[i] != jp_cancel_bytes[i]:
        en_va = (en_cancel_offset + i) - 0x400 + 0x401000
        jp_va = (jp_cancel_offset + i) - 0x400 + 0x401000
        differences.append((i, en_cancel_offset + i, en_cancel_bytes[i], jp_cancel_offset + i, jp_cancel_bytes[i], en_va))

if differences:
    print("Differences found:")
    for i, en_off, en_byte, jp_off, jp_byte, va in differences:
        print(f"  Offset +{i:02X}: EN 0x{en_off:06X} = {en_byte:02X}, JP 0x{jp_off:06X} = {jp_byte:02X} (VA: {va:08X})")
else:
    print("✓ No differences in Cancel button code")

print()
print("="*80)
print("BYTE-BY-BYTE COMPARISON - START")
print("="*80)
print()

with open(EN_EXE, 'rb') as f:
    f.seek(en_start_offset)
    en_start_bytes = f.read(64)

with open(JP_EXE, 'rb') as f:
    f.seek(jp_start_offset)
    jp_start_bytes = f.read(64)

differences = []
for i in range(min(len(en_start_bytes), len(jp_start_bytes))):
    if en_start_bytes[i] != jp_start_bytes[i]:
        en_va = (en_start_offset + i) - 0x400 + 0x401000
        jp_va = (jp_start_offset + i) - 0x400 + 0x401000
        differences.append((i, en_start_offset + i, en_start_bytes[i], jp_start_offset + i, jp_start_bytes[i], en_va))

if differences:
    print("Differences found:")
    for i, en_off, en_byte, jp_off, jp_byte, va in differences:
        print(f"  Offset +{i:02X}: EN 0x{en_off:06X} = {en_byte:02X}, JP 0x{jp_off:06X} = {jp_byte:02X} (VA: {va:08X})")
else:
    print("✓ No differences in Start button code")

print()
print("="*80)
print("KEY FINDINGS")
print("="*80)
print()
print(f"1. Total sidebar_flag writes: EN=4, JP=4 (SAME COUNT)")
print(f"2. All offsets differ by +0xC00 (expected JA exe offset)")
print()
if differences:
    print("3. CRITICAL DIFFERENCES FOUND between EN and JP:")
    print("   These bytes may explain why Cancel patch breaks Start in EN!")
else:
    print("3. No structural differences found in these regions")
    print("   The Cancel/Start issue might be in the button check functions")
    print("   or in shared state that these functions access")
