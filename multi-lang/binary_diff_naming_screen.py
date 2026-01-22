#!/usr/bin/env python3
"""
Binary Diff of FF7 Naming Screen Code Region
Compares EN and JA executables to find ALL byte differences in the naming screen code region.

File offsets:
- EN: 0x318000 to 0x31A000 (8KB region)
- JA: 0x318000 to 0x31A000 (8KB region)

Session: 35 - Naming Screen Binary Diff
Date: 2025-12-21
"""

import sys
from pathlib import Path
from collections import defaultdict

# File paths
EN_EXE = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe")
JA_EXE = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_ja.exe")

# Region to analyze
START_OFFSET = 0x318000
END_OFFSET = 0x31A000
REGION_SIZE = END_OFFSET - START_OFFSET

# VA calculation formula
def offset_to_va(offset):
    """Convert file offset to virtual address (disassembler format)"""
    return offset - 0x400 + 0x401000

def main():
    print("=" * 80)
    print("FF7 NAMING SCREEN CODE REGION - BINARY DIFF")
    print("=" * 80)
    print(f"Region: 0x{START_OFFSET:06X} to 0x{END_OFFSET:06X} ({REGION_SIZE} bytes)")
    print()

    # Read both regions
    print("Reading executables...")
    try:
        with open(EN_EXE, 'rb') as f:
            f.seek(START_OFFSET)
            en_data = f.read(REGION_SIZE)
    except Exception as e:
        print(f"ERROR reading EN exe: {e}")
        return 1

    try:
        with open(JA_EXE, 'rb') as f:
            f.seek(START_OFFSET)
            ja_data = f.read(REGION_SIZE)
    except Exception as e:
        print(f"ERROR reading JA exe: {e}")
        return 1

    if len(en_data) != REGION_SIZE or len(ja_data) != REGION_SIZE:
        print(f"ERROR: Read {len(en_data)}/{len(ja_data)} bytes, expected {REGION_SIZE}")
        return 1

    print(f"Read {len(en_data)} bytes from EN exe")
    print(f"Read {len(ja_data)} bytes from JA exe")
    print()

    # Find all differences
    print("Comparing bytes...")
    differences = []
    for i in range(REGION_SIZE):
        if en_data[i] != ja_data[i]:
            offset = START_OFFSET + i
            va = offset_to_va(offset)
            differences.append({
                'offset': offset,
                'va': va,
                'en': en_data[i],
                'ja': ja_data[i]
            })

    print(f"Found {len(differences)} differing bytes")
    print()

    # Summary statistics
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total bytes analyzed: {REGION_SIZE}")
    print(f"Bytes that differ:    {len(differences)} ({len(differences)/REGION_SIZE*100:.2f}%)")
    print(f"Bytes identical:      {REGION_SIZE - len(differences)} ({(REGION_SIZE - len(differences))/REGION_SIZE*100:.2f}%)")
    print()

    # List all differences
    print("=" * 80)
    print("ALL DIFFERENCES")
    print("=" * 80)
    print(f"{'File Offset':<12} {'VA (Disasm)':<12} {'EN Value':<10} {'JA Value':<10}")
    print("-" * 80)

    for diff in differences:
        print(f"0x{diff['offset']:06X}    "
              f"0x{diff['va']:08X}   "
              f"0x{diff['en']:02X}       "
              f"0x{diff['ja']:02X}")

    print()

    # Cluster analysis
    print("=" * 80)
    print("CLUSTER ANALYSIS")
    print("=" * 80)
    print("Grouping differences within 16 bytes of each other...")
    print()

    if not differences:
        print("No differences to cluster")
        return 0

    # Group differences into clusters (within 16 bytes = likely same instruction/data)
    CLUSTER_THRESHOLD = 16
    clusters = []
    current_cluster = [differences[0]]

    for i in range(1, len(differences)):
        if differences[i]['offset'] - current_cluster[-1]['offset'] <= CLUSTER_THRESHOLD:
            current_cluster.append(differences[i])
        else:
            clusters.append(current_cluster)
            current_cluster = [differences[i]]
    clusters.append(current_cluster)

    print(f"Found {len(clusters)} clusters")
    print()

    for i, cluster in enumerate(clusters, 1):
        start_offset = cluster[0]['offset']
        end_offset = cluster[-1]['offset']
        start_va = cluster[0]['va']
        end_va = cluster[-1]['va']
        size = len(cluster)

        print(f"Cluster {i}: {size} bytes")
        print(f"  File offset: 0x{start_offset:06X} to 0x{end_offset:06X}")
        print(f"  VA (disasm):  0x{start_va:08X} to 0x{end_va:08X}")
        print(f"  Bytes:")
        for diff in cluster:
            print(f"    0x{diff['offset']:06X} (VA 0x{diff['va']:08X}): "
                  f"EN=0x{diff['en']:02X}, JA=0x{diff['ja']:02X}")

        # Analyze cluster type
        print(f"  Analysis:")

        # Check if it's a sequence of bytes (data change)
        if size > 4:
            print(f"    - LIKELY DATA: {size} consecutive bytes changed")

        # Check if bytes are similar (code change vs data change)
        en_bytes = [d['en'] for d in cluster]
        ja_bytes = [d['ja'] for d in cluster]

        # If only 1-3 bytes, likely instruction parameter change
        if size <= 3:
            print(f"    - LIKELY CODE: Small instruction parameter change")

        # Check for common instruction patterns
        if any(d['en'] in [0x74, 0x75, 0x7E, 0x7F, 0xEB] for d in cluster):
            print(f"    - Contains jump instruction byte (JE/JNE/JMP)")

        if any(d['en'] in range(0x00, 0x10) and d['ja'] in range(0x00, 0x10) for d in cluster):
            print(f"    - Small value change (likely immediate/offset)")

        print()

    # Known important addresses
    print("=" * 80)
    print("KNOWN CRITICAL ADDRESSES")
    print("=" * 80)

    known_addresses = [
        (0x31855B, 0x71915B, "Cancel JE instruction"),
        (0x318C1A, 0x71981A, "Start JE instruction"),
        (0x318627, 0x719227, "Sidebar loop count"),
        (0x31844C, 0x71904C, "Switch 1 bounds"),
        (0x318B0D, 0x71930D, "Switch 2 bounds"),
    ]

    for offset, va, desc in known_addresses:
        # Check if this address has a difference
        matching = [d for d in differences if d['offset'] == offset]
        if matching:
            diff = matching[0]
            print(f"✓ {desc}")
            print(f"  File offset 0x{offset:06X}, VA 0x{va:08X}")
            print(f"  EN=0x{diff['en']:02X}, JA=0x{diff['ja']:02X}")
        else:
            print(f"✗ {desc}")
            print(f"  File offset 0x{offset:06X}, VA 0x{va:08X}")
            print(f"  IDENTICAL in both executables")
        print()

    return 0

if __name__ == '__main__':
    sys.exit(main())
