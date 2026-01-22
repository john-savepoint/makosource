#!/usr/bin/env python3
"""
FF7 Memory Region Analyzer with IDA Pro Integration
====================================================

Created: 2026-01-21 01:10:00 JST (Wednesday)
Session-ID: 5ee0effa-d1c4-4e6f-ae21-cce61

 Purpose:
--------
Groups UI memory addresses into coherent regions and provides analysis
for reverse engineering with IDA Pro.

Usage:
------
python ff7_memory_region_analyzer.py ff7_ui_analysis/ff7_ui_memory_map.json
"""

import json
import sys
from collections import defaultdict
from typing import Dict, List, Tuple


class MemoryRegionAnalyzer:
    """Analyzes memory addresses and groups them into coherent regions."""

    def __init__(self, memory_map_path: str):
        with open(memory_map_path, 'r') as f:
            self.memory_map = json.load(f)

        self.regions = []

    def group_by_proximity(self, max_gap: int = 0x1000):
        """Group addresses by proximity (within max_gap bytes)."""
        # Sort addresses
        sorted_addrs = sorted(self.memory_map.items(),
                             key=lambda x: x[1]['address_decimal'])

        current_region = {
            'start_addr': None,
            'end_addr': None,
            'addresses': [],
            'categories': set(),
            'primary_purposes': []
        }

        for addr_hex, data in sorted_addrs:
            addr_dec = data['address_decimal']

            if current_region['start_addr'] is None:
                # First address
                current_region['start_addr'] = addr_dec
                current_region['end_addr'] = addr_dec
                current_region['addresses'].append(data)
                current_region['categories'].update(data['categories'])
                current_region['primary_purposes'].append(data['primary_purpose'])
            elif addr_dec - current_region['end_addr'] <= max_gap:
                # Within gap, add to current region
                current_region['end_addr'] = addr_dec
                current_region['addresses'].append(data)
                current_region['categories'].update(data['categories'])
                current_region['primary_purposes'].append(data['primary_purpose'])
            else:
                # Gap too large, save current region and start new one
                self.regions.append(current_region)

                current_region = {
                    'start_addr': addr_dec,
                    'end_addr': addr_dec,
                    'addresses': [data],
                    'categories': set(data['categories']),
                    'primary_purposes': [data['primary_purpose']]
                }

        # Don't forget the last region
        if current_region['start_addr'] is not None:
            self.regions.append(current_region)

    def analyze_regions(self):
        """Analyze and categorize regions."""
        print(f"\nFound {len(self.regions)} memory regions\n")
        print("="*120)

        for i, region in enumerate(self.regions):
            size = region['end_addr'] - region['start_addr']
            count = len(region['addresses'])

            print(f"\nREGION {i+1}: 0x{region['start_addr']:08X} - 0x{region['end_addr']:08X}")
            print(f"  Size: {size} bytes (0x{size:X})")
            print(f"  Address count: {count}")
            print(f"  Categories: {', '.join(sorted(region['categories']))}")

            # Get most common purposes
            purpose_counts = defaultdict(int)
            for purpose in region['primary_purposes']:
                purpose_counts[purpose] += 1

            top_purposes = sorted(purpose_counts.items(),
                                 key=lambda x: -x[1])[:5]

            print(f"  Common purposes:")
            for purpose, count in top_purposes:
                print(f"    [{count:3}x] {purpose[:80]}")

            # Identify region type
            categories = region['categories']
            region_type = "Mixed UI"

            if 'MainMenu' in categories and count > 10:
                region_type = "Main Menu System"
            elif 'Battle' in categories and count > 10:
                region_type = "Battle UI System"
            elif 'ItemMenu' in categories:
                region_type = "Item Menu System"
            elif 'MateriaMenu' in categories and count > 10:
                region_type = "Materia Menu System"
            elif 'Field' in categories:
                region_type = "Field/Dialog System"
            elif 'Cursor' in categories and 'Box' in categories:
                region_type = "UI Layout System"

            print(f"  Likely region type: {region_type}")
            print("-"*120)

    def generate_ida_script(self, output_path: str):
        """Generate IDA Pro Python script to annotate these addresses."""
        with open(output_path, 'w') as f:
            f.write('''"""
FF7 UI Memory Location Annotations for IDA Pro
Generated automatically from HEXT analysis

Usage in IDA Pro:
    File -> Script file... -> Select this file
"""

import idaapi
import idc

def annotate_ui_locations():
    """Add comments to all known UI memory locations."""

''')

            for addr_hex, data in sorted(self.memory_map.items()):
                addr_dec = data['address_decimal']
                purpose = data['primary_purpose'].replace('"', '\\"')
                categories = ', '.join(data['categories'])

                f.write(f'''    # {addr_hex}: {purpose[:50]}
    idc.set_cmt(0x{addr_hex}, "[UI] {purpose}", 0)
    idc.set_name(0x{addr_hex}, "ui_{addr_hex}", idaapi.SN_NOWARN)
''')

            f.write('''
    print("Annotated {} UI memory locations")

if __name__ == "__main__":
    annotate_ui_locations()
'''.format(len(self.memory_map)))

        print(f"\nGenerated IDA Pro script: {output_path}")

    def export_region_summary(self, output_path: str):
        """Export region summary for documentation."""
        with open(output_path, 'w') as f:
            f.write("# FF7 UI Memory Regions Summary\n\n")
            f.write(f"Total unique addresses analyzed: {len(self.memory_map)}\n")
            f.write(f"Total memory regions: {len(self.regions)}\n\n")

            for i, region in enumerate(self.regions):
                size = region['end_addr'] - region['start_addr']
                count = len(region['addresses'])

                f.write(f"## Region {i+1}\n\n")
                f.write(f"- **Address Range**: `0x{region['start_addr']:08X}` - `0x{region['end_addr']:08X}`\n")
                f.write(f"- **Size**: {size} bytes (0x{size:X})\n")
                f.write(f"- **UI Elements**: {count} addresses\n")
                f.write(f"- **Categories**: {', '.join(sorted(region['categories']))}\n\n")

                # Sample addresses from this region
                f.write("### Sample Addresses:\n\n")
                for addr in region['addresses'][:10]:
                    f.write(f"- `0x{addr['address']:08s}`: {addr['primary_purpose']}\n")

                if len(region['addresses']) > 10:
                    f.write(f"- ... and {len(region['addresses']) - 10} more\n")

                f.write("\n---\n\n")

        print(f"Exported region summary: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python ff7_memory_region_analyzer.py <memory_map.json>")
        sys.exit(1)

    memory_map_path = sys.argv[1]

    print("="*120)
    print("FF7 Memory Region Analyzer")
    print("="*120)

    analyzer = MemoryRegionAnalyzer(memory_map_path)
    analyzer.group_by_proximity(max_gap=0x2000)  # Group addresses within 8KB
    analyzer.analyze_regions()

    analyzer.generate_ida_script("ff7_ui_analysis/ida_annotate_ui.py")
    analyzer.export_region_summary("ff7_ui_analysis/memory_regions_summary.md")


if __name__ == "__main__":
    main()
