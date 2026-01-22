#!/usr/bin/env python3
"""
FF7 Kernel.bin Comparison Tool
Created: 2024-12-29
Purpose: Compare EN and DE kernel.bin files to find battle-related lookup tables

kernel.bin structure (PC version):
- Consecutive sections, each with:
  - 2 bytes: compressed data size (little-endian)
  - 2 bytes: decompressed data size (little-endian)
  - 2 bytes: section type/flags
  - N bytes: gzip compressed data

Focus on section 3 at offset 0x0F1C for scene block boundary lookup table
"""

import gzip
import struct
import os
from io import BytesIO

# File paths
EN_KERNEL = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/data/lang-en/kernel/KERNEL.BIN"
DE_KERNEL = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/data/lang-de/kernel/KERNEL.BIN"


def read_kernel_sections(filepath):
    """
    Parse kernel.bin and extract all gzip-compressed sections.

    Format per section:
    - 2 bytes: compressed size (little-endian)
    - 2 bytes: decompressed size (little-endian)
    - 2 bytes: section type
    - N bytes: gzip compressed data
    """
    sections = []
    section_info = []

    with open(filepath, 'rb') as f:
        data = f.read()

    print(f"\nParsing: {os.path.basename(filepath)} ({filepath.split('/')[-3]})")
    print(f"Total file size: {len(data)} bytes (0x{len(data):04X})")

    offset = 0
    section_idx = 0

    while offset < len(data) - 6:  # Need at least 6 bytes for header
        # Read section header
        comp_size = struct.unpack('<H', data[offset:offset+2])[0]
        decomp_size = struct.unpack('<H', data[offset+2:offset+4])[0]
        section_type = struct.unpack('<H', data[offset+4:offset+6])[0]

        header_offset = offset
        offset += 6  # Move past header

        # Validate we have enough data
        if offset + comp_size > len(data):
            print(f"Section {section_idx}: Would exceed file at 0x{offset:04X}, stopping")
            break

        if comp_size == 0:
            print(f"Section {section_idx}: Zero size at 0x{header_offset:04X}, stopping")
            break

        section_data = data[offset:offset + comp_size]

        # Check for gzip magic
        if len(section_data) >= 2 and section_data[:2] == b'\x1f\x8b':
            try:
                decompressed = gzip.decompress(section_data)
                sections.append(decompressed)
                section_info.append({
                    'index': section_idx,
                    'header_offset': header_offset,
                    'data_offset': offset,
                    'comp_size': comp_size,
                    'declared_decomp_size': decomp_size,
                    'actual_decomp_size': len(decompressed),
                    'section_type': section_type,
                    'status': 'OK'
                })
                print(f"Section {section_idx:2d}: hdr=0x{header_offset:04X}, comp={comp_size:5d}, "
                      f"decomp={len(decompressed):5d} (declared:{decomp_size:5d}), type=0x{section_type:04X}")
            except Exception as e:
                sections.append(section_data)
                section_info.append({
                    'index': section_idx,
                    'header_offset': header_offset,
                    'data_offset': offset,
                    'comp_size': comp_size,
                    'declared_decomp_size': decomp_size,
                    'actual_decomp_size': 0,
                    'section_type': section_type,
                    'status': f'GZIP ERROR: {e}'
                })
                print(f"Section {section_idx:2d}: hdr=0x{header_offset:04X}, ERROR decompressing: {e}")
        else:
            # Not gzip, store raw
            sections.append(section_data)
            section_info.append({
                'index': section_idx,
                'header_offset': header_offset,
                'data_offset': offset,
                'comp_size': comp_size,
                'declared_decomp_size': decomp_size,
                'actual_decomp_size': comp_size,
                'section_type': section_type,
                'status': 'RAW (no gzip magic)'
            })
            first_bytes = section_data[:8].hex() if len(section_data) >= 8 else section_data.hex()
            print(f"Section {section_idx:2d}: hdr=0x{header_offset:04X}, size={comp_size:5d} "
                  f"(NOT GZIP, starts: {first_bytes})")

        offset += comp_size
        section_idx += 1

        # Safety limit
        if section_idx > 50:
            print("Hit section limit, stopping")
            break

    return sections, section_info


def hex_dump(data, offset=0, length=64, prefix=""):
    """Create a hex dump with ASCII representation."""
    lines = []
    for i in range(0, min(length, len(data)), 16):
        hex_bytes = ' '.join(f'{b:02X}' for b in data[i:i+16])
        ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        lines.append(f"{prefix}0x{offset+i:04X}: {hex_bytes:<48} |{ascii_repr}|")
    return '\n'.join(lines)


def find_lookup_table_patterns(data, section_idx):
    """Search for potential scene block lookup table patterns."""
    patterns_found = []

    # Look for sequence 0x0C (12) repeated
    for i in range(len(data) - 10):
        # Check for runs of 12s (scenes per block)
        if data[i:i+4] == b'\x0c\x0c\x0c\x0c':
            patterns_found.append({
                'type': '12-repeating',
                'offset': i,
                'context': data[max(0,i-4):i+20].hex()
            })

        # Check for incrementing cumulative values (16-bit LE)
        if i + 16 < len(data):
            try:
                vals = struct.unpack('<8H', data[i:i+16])
                # Check if it looks like cumulative scene counts
                if vals[0] == 0 and all(vals[j] <= vals[j+1] for j in range(7)):
                    if 10 <= vals[1] <= 20:  # First increment around 12
                        patterns_found.append({
                            'type': 'cumulative-16bit',
                            'offset': i,
                            'values': vals,
                            'context': data[i:i+32].hex()
                        })
            except:
                pass

        # 8-bit cumulative
        if i + 8 < len(data):
            vals = list(data[i:i+8])
            if vals[0] == 0 and all(vals[j] <= vals[j+1] for j in range(7)):
                if 10 <= vals[1] <= 20:
                    patterns_found.append({
                        'type': 'cumulative-8bit',
                        'offset': i,
                        'values': vals,
                        'context': data[i:i+16].hex()
                    })

    return patterns_found


def compare_sections(en_data, de_data, section_idx):
    """Compare two sections byte by byte."""
    differences = []

    min_len = min(len(en_data), len(de_data))

    for i in range(min_len):
        if en_data[i] != de_data[i]:
            differences.append({
                'offset': i,
                'en': en_data[i],
                'de': de_data[i]
            })

    return {
        'section': section_idx,
        'en_size': len(en_data),
        'de_size': len(de_data),
        'size_diff': len(en_data) - len(de_data),
        'diff_count': len(differences),
        'differences': differences[:100]  # First 100 differences
    }


def main():
    print("=" * 80)
    print("FF7 Kernel.bin Comparison: EN vs DE")
    print("=" * 80)

    # Parse both kernel files
    en_sections, en_info = read_kernel_sections(EN_KERNEL)
    print("\n" + "-" * 80)
    de_sections, de_info = read_kernel_sections(DE_KERNEL)

    print("\n" + "=" * 80)
    print("SECTION SIZE COMPARISON")
    print("=" * 80)
    print(f"{'Section':^8} {'EN Size':^10} {'DE Size':^10} {'Diff':^8} {'EN Type':^10} {'DE Type':^10}")
    print("-" * 60)

    for i in range(min(len(en_sections), len(de_sections))):
        en_size = len(en_sections[i])
        de_size = len(de_sections[i])
        en_type = en_info[i]['section_type'] if i < len(en_info) else 0
        de_type = de_info[i]['section_type'] if i < len(de_info) else 0
        diff = en_size - de_size
        diff_str = f"{diff:+d}" if diff != 0 else "0"
        print(f"{i:^8} {en_size:^10} {de_size:^10} {diff_str:^8} 0x{en_type:04X}    0x{de_type:04X}")

    # SECTION 2 ANALYSIS - Found scene block lookup table at offset 0x0F1C
    print("\n" + "=" * 80)
    print("SECTION 2 ANALYSIS - SCENE BLOCK LOOKUP TABLE FOUND!")
    print("=" * 80)

    if len(en_sections) > 2 and len(de_sections) > 2:
        en_s2 = en_sections[2]
        de_s2 = de_sections[2]

        print(f"\nEN Section 2 size: {len(en_s2)} bytes (0x{len(en_s2):04X})")
        print(f"DE Section 2 size: {len(de_s2)} bytes (0x{len(de_s2):04X})")

        # Check offset 0x0F1C - CONFIRMED scene block boundary location
        target_offset = 0x0F1C

        print(f"\n{'='*60}")
        print("SCENE BLOCK BOUNDARY TABLE @ OFFSET 0x0F1C")
        print(f"{'='*60}")

        if target_offset < len(en_s2):
            print("\nEN kernel.bin Section 2 @ 0x0F1C (128 bytes):")
            print(hex_dump(en_s2[target_offset:target_offset+128], target_offset, 128))

            # Interpret the data as cumulative scene counts (8-bit)
            lookup_data_en = list(en_s2[target_offset:target_offset+128])
            print(f"\nEN Cumulative scene counts (first 64 values):")
            print(f"  {lookup_data_en[:64]}")

            # Calculate scenes per block (differences between consecutive values)
            scenes_per_block_en = []
            for i in range(1, min(64, len(lookup_data_en))):
                if lookup_data_en[i] != 255:  # 0xFF is likely padding
                    scenes_per_block_en.append(lookup_data_en[i] - lookup_data_en[i-1])
                else:
                    break
            print(f"\nEN Scenes per block (differences): {scenes_per_block_en}")

        if target_offset < len(de_s2):
            print("\nDE kernel.bin Section 2 @ 0x0F1C (128 bytes):")
            print(hex_dump(de_s2[target_offset:target_offset+128], target_offset, 128))

            # Interpret the data
            lookup_data_de = list(de_s2[target_offset:target_offset+128])
            print(f"\nDE Cumulative scene counts (first 64 values):")
            print(f"  {lookup_data_de[:64]}")

            # Calculate scenes per block
            scenes_per_block_de = []
            for i in range(1, min(64, len(lookup_data_de))):
                if lookup_data_de[i] != 255:
                    scenes_per_block_de.append(lookup_data_de[i] - lookup_data_de[i-1])
                else:
                    break
            print(f"\nDE Scenes per block (differences): {scenes_per_block_de}")

        # Direct comparison of lookup tables
        print(f"\n{'='*60}")
        print("DIRECT EN vs DE COMPARISON AT 0x0F1C")
        print(f"{'='*60}")

        for i in range(min(64, len(en_s2) - target_offset, len(de_s2) - target_offset)):
            en_val = en_s2[target_offset + i]
            de_val = de_s2[target_offset + i]
            if en_val != de_val:
                print(f"  Offset 0x{target_offset+i:04X} (block {i}): EN={en_val:3d} (0x{en_val:02X}), DE={de_val:3d} (0x{de_val:02X}), diff={en_val-de_val:+d}")

    # Focus on Section 3 at offset 0x0F1C (original)
    print("\n" + "=" * 80)
    print("SECTION 3 ANALYSIS (Battle-related data)")
    print("=" * 80)

    if len(en_sections) > 3 and len(de_sections) > 3:
        en_s3 = en_sections[3]
        de_s3 = de_sections[3]

        print(f"\nEN Section 3 size: {len(en_s3)} bytes (0x{len(en_s3):04X})")
        print(f"DE Section 3 size: {len(de_s3)} bytes (0x{len(de_s3):04X})")

        # Compare section 3
        comparison = compare_sections(en_s3, de_s3, 3)
        print(f"\nSection 3 byte differences: {comparison['diff_count']}")

        if comparison['diff_count'] > 0:
            print("\nDifferences in Section 3:")
            for diff in comparison['differences'][:20]:
                print(f"  Offset 0x{diff['offset']:04X}: EN=0x{diff['en']:02X} DE=0x{diff['de']:02X}")

        # Dump first 128 bytes of section 3 to see structure
        print("\n--- Section 3 First 128 bytes ---")
        print(hex_dump(en_s3[:128], 0, 128))

    # Also check other sections for scene-related data
    print("\n" + "=" * 80)
    print("SEARCHING ALL SECTIONS FOR SCENE LOOKUP PATTERNS")
    print("=" * 80)

    for i, section in enumerate(en_sections):
        if len(section) > 0:
            patterns = find_lookup_table_patterns(section, i)
            if patterns:
                print(f"\nSection {i}: Found {len(patterns)} patterns")
                for p in patterns[:5]:
                    print(f"  Type: {p['type']}, Offset: 0x{p['offset']:04X}")
                    if 'values' in p:
                        print(f"    Values: {p['values']}")

    # Binary comparison of full files
    print("\n" + "=" * 80)
    print("COMPARING ALL SECTIONS FOR DIFFERENCES")
    print("=" * 80)

    total_diffs = 0
    for i in range(min(len(en_sections), len(de_sections))):
        comparison = compare_sections(en_sections[i], de_sections[i], i)
        if comparison['diff_count'] > 0 or comparison['size_diff'] != 0:
            print(f"\nSection {i}: {comparison['diff_count']} byte differences, size diff: {comparison['size_diff']}")
            if comparison['differences']:
                print("  First 10 differences:")
                for diff in comparison['differences'][:10]:
                    print(f"    0x{diff['offset']:04X}: EN=0x{diff['en']:02X} DE=0x{diff['de']:02X}")
        total_diffs += comparison['diff_count']

    print(f"\n{'=' * 80}")
    print(f"Total byte differences across all sections: {total_diffs}")

    # Final summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"EN kernel.bin: {len(en_sections)} sections extracted")
    print(f"DE kernel.bin: {len(de_sections)} sections extracted")


if __name__ == '__main__':
    main()
