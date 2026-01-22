#!/usr/bin/env python3
"""
FF7 UI HEXT Memory Location Analyzer
=====================================

Created: 2026-01-21 01:03:18 JST (Wednesday)
Session-ID: 5ee0effa-d1c4-4e6f-ae21-cce61cbedc2f

Purpose:
--------
Analyzes all HEXT files in FF7 mod directories to extract UI-related memory
locations, their purposes, and value ranges. This helps reverse engineer the
FF7 UI system by aggregating knowledge from hundreds of community mods.

Context:
--------
The FF7 modding community has documented UI memory locations through trial and
error in HEXT patch files. By analyzing all these files, we can create a
comprehensive map of UI memory regions and understand the valid value ranges.

Usage:
------
python ff7_ui_hext_analyzer.py /path/to/FF7Modding/directory
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import csv


class HextAnalyzer:
    """Analyzes HEXT files to extract UI memory locations."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.memory_map: Dict[str, Dict] = defaultdict(lambda: {
            'addresses': set(),
            'comments': [],
            'values': [],
            'files': [],
            'categories': set()
        })
        self.ui_keywords = [
            'menu', 'cursor', 'box', 'bar', 'text', 'position', 'spacing',
            'x-axis', 'y-axis', 'width', 'height', 'color', 'UI', 'avatar',
            'hp', 'mp', 'limit', 'battle', 'field', 'equip', 'magic', 'item',
            'materia', 'status', 'icon', 'dialog', 'window', 'opacity',
            'transparency', 'divider', 'digit', 'gil', 'time', 'exp'
        ]

    def is_ui_related(self, comment: str) -> bool:
        """Check if a comment describes UI-related functionality."""
        comment_lower = comment.lower()
        return any(keyword in comment_lower for keyword in self.ui_keywords)

    def categorize_ui_element(self, comment: str) -> Set[str]:
        """Categorize UI element based on comment."""
        categories = set()
        comment_lower = comment.lower()

        # Menu types
        if 'main menu' in comment_lower:
            categories.add('MainMenu')
        if 'battle' in comment_lower:
            categories.add('Battle')
        if 'field' in comment_lower:
            categories.add('Field')
        if 'item' in comment_lower:
            categories.add('ItemMenu')
        if 'equip' in comment_lower:
            categories.add('EquipMenu')
        if 'magic' in comment_lower:
            categories.add('MagicMenu')
        if 'materia' in comment_lower:
            categories.add('MateriaMenu')
        if 'status' in comment_lower:
            categories.add('StatusMenu')
        if 'limit' in comment_lower:
            categories.add('LimitMenu')
        if 'config' in comment_lower or 'option' in comment_lower:
            categories.add('ConfigMenu')
        if 'save' in comment_lower or 'load' in comment_lower:
            categories.add('SaveLoadMenu')
        if 'shop' in comment_lower:
            categories.add('ShopMenu')
        if 'world' in comment_lower:
            categories.add('WorldMap')

        # UI element types
        if 'cursor' in comment_lower:
            categories.add('Cursor')
        if 'box' in comment_lower or 'window' in comment_lower:
            categories.add('Box')
        if 'bar' in comment_lower:
            categories.add('Bar')
        if 'text' in comment_lower or 'font' in comment_lower:
            categories.add('Text')
        if 'avatar' in comment_lower or 'portrait' in comment_lower:
            categories.add('Avatar')
        if 'icon' in comment_lower:
            categories.add('Icon')
        if 'color' in comment_lower or 'palette' in comment_lower:
            categories.add('Color')
        if 'opacity' in comment_lower or 'transparency' in comment_lower:
            categories.add('Opacity')

        # Position/dimension
        if 'x-axis' in comment_lower or 'x axis' in comment_lower:
            categories.add('PositionX')
        if 'y-axis' in comment_lower or 'y axis' in comment_lower:
            categories.add('PositionY')
        if 'width' in comment_lower:
            categories.add('Width')
        if 'height' in comment_lower:
            categories.add('Height')
        if 'spacing' in comment_lower:
            categories.add('Spacing')

        return categories if categories else {'Uncategorized'}

    def parse_hext_file(self, filepath: Path) -> List[Tuple[str, str, str]]:
        """Parse a HEXT file and extract address, value, comment triplets."""
        results = []
        current_comment = ""

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()

                    # Skip empty lines and target specification
                    if not line or line.startswith('..'):
                        continue

                    # Extract comments
                    if line.startswith('{'):
                        current_comment = line[1:].strip()
                        continue

                    # Parse address = value lines
                    match = re.match(r'^([0-9A-Fa-f]+)\s*=\s*(.+)$', line)
                    if match:
                        address = match.group(1).upper()
                        value = match.group(2).strip()
                        results.append((address, value, current_comment))
                        current_comment = ""  # Reset after use

        except Exception as e:
            print(f"Error parsing {filepath}: {e}", file=sys.stderr)

        return results

    def analyze_file(self, filepath: Path):
        """Analyze a single HEXT file."""
        entries = self.parse_hext_file(filepath)
        relative_path = filepath.relative_to(self.base_path)

        for address, value, comment in entries:
            # Only process UI-related entries
            if not comment or not self.is_ui_related(comment):
                continue

            categories = self.categorize_ui_element(comment)

            # Store information
            self.memory_map[address]['addresses'].add(address)
            self.memory_map[address]['comments'].append(comment)
            self.memory_map[address]['values'].append(value)
            self.memory_map[address]['files'].append(str(relative_path))
            self.memory_map[address]['categories'].update(categories)

    def analyze_all_files(self):
        """Recursively analyze all HEXT files."""
        txt_files = list(self.base_path.rglob("*.txt"))
        print(f"Found {len(txt_files)} .txt files to analyze...")

        for i, filepath in enumerate(txt_files):
            if (i + 1) % 50 == 0:
                print(f"Processed {i + 1}/{len(txt_files)} files...")
            self.analyze_file(filepath)

        print(f"Analysis complete! Found {len(self.memory_map)} unique UI memory addresses.")

    def get_value_range(self, values: List[str]) -> Tuple[int, int, List[str]]:
        """Determine min/max values from hex string values."""
        parsed_values = []

        for value_str in values:
            # Split multiple bytes
            bytes_list = value_str.split()
            for byte in bytes_list:
                try:
                    # Try parsing as hex
                    parsed_values.append(int(byte, 16))
                except ValueError:
                    pass

        if parsed_values:
            return min(parsed_values), max(parsed_values), values
        return 0, 0, values

    def generate_memory_map(self) -> Dict:
        """Generate comprehensive memory map with statistics."""
        result = {}

        for address, data in sorted(self.memory_map.items()):
            min_val, max_val, raw_values = self.get_value_range(data['values'])

            # Get most common comment
            comment_counts = defaultdict(int)
            for comment in data['comments']:
                comment_counts[comment] += 1
            primary_comment = max(comment_counts.items(), key=lambda x: x[1])[0] if comment_counts else "Unknown"

            result[address] = {
                'address': address,
                'address_decimal': int(address, 16),
                'primary_purpose': primary_comment,
                'all_comments': list(set(data['comments'])),
                'categories': sorted(list(data['categories'])),
                'value_min': min_val,
                'value_max': max_val,
                'value_count': len(data['values']),
                'example_values': raw_values[:10],  # First 10 examples
                'occurrence_count': len(data['files']),
                'example_files': list(set(data['files']))[:5]  # First 5 unique files
            }

        return result

    def export_csv(self, output_path: str):
        """Export memory map to CSV."""
        memory_map = self.generate_memory_map()

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Address (Hex)', 'Address (Dec)', 'Primary Purpose',
                'Categories', 'Min Value', 'Max Value', 'Occurrences',
                'Example Values'
            ])

            for addr, data in sorted(memory_map.items()):
                writer.writerow([
                    data['address'],
                    data['address_decimal'],
                    data['primary_purpose'],
                    ', '.join(data['categories']),
                    data['value_min'],
                    data['value_max'],
                    data['occurrence_count'],
                    '; '.join(data['example_values'][:3])
                ])

        print(f"Exported CSV to: {output_path}")

    def export_json(self, output_path: str):
        """Export complete memory map to JSON."""
        memory_map = self.generate_memory_map()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(memory_map, f, indent=2)

        print(f"Exported JSON to: {output_path}")

    def print_summary(self):
        """Print analysis summary."""
        memory_map = self.generate_memory_map()

        print("\n" + "="*80)
        print("FF7 UI MEMORY MAP ANALYSIS SUMMARY")
        print("="*80)
        print(f"\nTotal unique UI memory addresses: {len(memory_map)}")

        # Category breakdown
        category_counts = defaultdict(int)
        for data in memory_map.values():
            for category in data['categories']:
                category_counts[category] += 1

        print("\nAddresses by category:")
        for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            print(f"  {category:20} {count:4} addresses")

        # Address range
        addresses_dec = [data['address_decimal'] for data in memory_map.values()]
        print(f"\nMemory address range:")
        print(f"  Min: 0x{min(addresses_dec):08X} ({min(addresses_dec)})")
        print(f"  Max: 0x{max(addresses_dec):08X} ({max(addresses_dec)})")

        print("\n" + "="*80)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ff7_ui_hext_analyzer.py <path_to_FF7Modding>")
        print("Example: python ff7_ui_hext_analyzer.py /mnt/d/Games/Stand-alone/FF7Modding")
        sys.exit(1)

    base_path = sys.argv[1]

    if not os.path.exists(base_path):
        print(f"Error: Path does not exist: {base_path}")
        sys.exit(1)

    print("="*80)
    print("FF7 UI HEXT Memory Location Analyzer")
    print("="*80)
    print(f"Analyzing: {base_path}\n")

    analyzer = HextAnalyzer(base_path)
    analyzer.analyze_all_files()
    analyzer.print_summary()

    # Export results
    output_dir = Path("./ff7_ui_analysis")
    output_dir.mkdir(exist_ok=True)

    analyzer.export_json(str(output_dir / "ff7_ui_memory_map.json"))
    analyzer.export_csv(str(output_dir / "ff7_ui_memory_map.csv"))

    print(f"\nResults saved to: {output_dir}")


if __name__ == "__main__":
    main()
