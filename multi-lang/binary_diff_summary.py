#!/usr/bin/env python3
"""
Binary Diff Summary - Focus on key findings
"""

import sys
from pathlib import Path

EN_EXE = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe")
JA_EXE = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_ja.exe")

START_OFFSET = 0x318000
END_OFFSET = 0x31A000
REGION_SIZE = END_OFFSET - START_OFFSET

def offset_to_va(offset):
    return offset - 0x400 + 0x401000

def main():
    # Read regions
    with open(EN_EXE, 'rb') as f:
        f.seek(START_OFFSET)
        en_data = f.read(REGION_SIZE)

    with open(JA_EXE, 'rb') as f:
        f.seek(START_OFFSET)
        ja_data = f.read(REGION_SIZE)

    # Find differences
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

    print("=" * 80)
    print("BINARY DIFF SUMMARY")
    print("=" * 80)
    print(f"Total bytes:    {REGION_SIZE}")
    print(f"Bytes differ:   {len(differences)} ({len(differences)/REGION_SIZE*100:.2f}%)")
    print(f"Bytes same:     {REGION_SIZE - len(differences)} ({(REGION_SIZE - len(differences))/REGION_SIZE*100:.2f}%)")
    print()

    # Cluster analysis
    CLUSTER_THRESHOLD = 16
    clusters = []
    if differences:
        current_cluster = [differences[0]]
        for i in range(1, len(differences)):
            if differences[i]['offset'] - current_cluster[-1]['offset'] <= CLUSTER_THRESHOLD:
                current_cluster.append(differences[i])
            else:
                clusters.append(current_cluster)
                current_cluster = [differences[i]]
        clusters.append(current_cluster)

    print(f"Found {len(clusters)} clusters (differences within 16 bytes)")
    print()

    # Show first 20 clusters
    print("FIRST 20 CLUSTERS:")
    print("-" * 80)
    for i, cluster in enumerate(clusters[:20], 1):
        start_offset = cluster[0]['offset']
        end_offset = cluster[-1]['offset']
        start_va = cluster[0]['va']
        size = len(cluster)

        print(f"Cluster {i}: {size} bytes at file offset 0x{start_offset:06X} (VA 0x{start_va:08X})")
        if size <= 10:
            for diff in cluster:
                print(f"  0x{diff['offset']:06X}: EN=0x{diff['en']:02X} JA=0x{diff['ja']:02X}")
        else:
            print(f"  [Large cluster - {size} consecutive bytes differ]")
        print()

    # Check known addresses
    print("=" * 80)
    print("KNOWN CRITICAL ADDRESSES")
    print("=" * 80)

    known_addresses = [
        (0x31855B, 0x71915B, "Cancel JE instruction"),
        (0x318576, 0x719176, "Cancel cursor position"),
        (0x318C1A, 0x71981A, "Start JE instruction"),
        (0x318C35, 0x719835, "Start cursor position"),
        (0x318627, 0x719227, "Sidebar loop count"),
        (0x31844C, 0x71904C, "Switch 1 bounds"),
        (0x318B0D, 0x71930D, "Switch 2 bounds"),
        (0x31867A, 0x71927A, "Loop limit"),
        (0x319579, 0x71A179, "Unknown 1"),
        (0x3199A4, 0x71A5A4, "Unknown 2"),
        (0x318019, 0x718C19, "Unknown 3"),
        (0x3180E8, 0x718CE8, "Unknown 4"),
    ]

    for offset, va, desc in known_addresses:
        matching = [d for d in differences if d['offset'] == offset]
        if matching:
            diff = matching[0]
            status = "DIFFERS"
            detail = f"EN=0x{diff['en']:02X}, JA=0x{diff['ja']:02X}"
        else:
            status = "IDENTICAL"
            detail = f"Both have 0x{en_data[offset - START_OFFSET]:02X}"

        print(f"{status:<10} {desc}")
        print(f"           File offset 0x{offset:06X}, VA 0x{va:08X}: {detail}")
        print()

    return 0

if __name__ == '__main__':
    sys.exit(main())
