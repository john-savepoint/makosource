#!/usr/bin/env python3
"""
HEXT UI Memory Address Analyzer - New Dataset Merger
Created: 2026-01-21 JST
Session: 9bfbe481-e8b6-4c52-868e-5e825185a4b4

Purpose: Analyze new HEXT UI patch files, compare with existing dataset,
         and generate merged comprehensive UI memory map.

Context: Previously analyzed 497 HEXT files yielding 1,643 unique UI addresses.
         This script processes a new directory of 58 HEXT files to find additional
         addresses and merge with existing data.
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Configuration
NEW_HEXT_DIR = "/mnt/d/Games/Stand-alone/FF7Modding/UI_new_2026-21-01"
EXISTING_JSON = "/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/ff7_ui_memory_map.json"
OUTPUT_DIR = "/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis"

# Category keywords for auto-categorization
CATEGORY_KEYWORDS = {
    'PositionX': ['x-axis', 'x axis', 'horizontal', 'left', 'right'],
    'PositionY': ['y-axis', 'y axis', 'vertical', 'top', 'bottom'],
    'Width': ['width', 'w-axis'],
    'Height': ['height', 'h-axis'],
    'Box': ['box', 'window'],
    'Cursor': ['cursor', 'pointer'],
    'Bar': ['bar', 'gauge'],
    'Menu': ['menu'],
    'Spacing': ['spacing', 'padding', 'margin'],
    'Text': ['text', 'font', 'letter'],
    'Color': ['color', 'rgb', 'palette'],
    'LimitMenu': ['limit menu', 'limit break'],
    'EquipMenu': ['equip', 'equipment'],
    'ItemMenu': ['item menu'],
    'MateriaMenu': ['materia'],
    'BattleMenu': ['battle menu'],
    'FieldMenu': ['field menu'],
    'SaveMenu': ['save menu'],
}

def normalize_address(addr: str) -> str:
    """Normalize address to 8-char uppercase hex format (00XXXXXX)."""
    addr = addr.strip().upper()
    # Remove any 0x prefix
    if addr.startswith('0X'):
        addr = addr[2:]
    # Pad to 8 characters
    addr = addr.zfill(8)
    return addr

def parse_hext_line(line: str) -> Tuple[str, str, str]:
    """
    Parse HEXT line and extract address, value, and comment.

    Returns: (address, value, comment) or (None, None, None) if not a valid HEXT line
    """
    line = line.strip()

    # Skip empty lines, comments, and file headers
    if not line or line.startswith('#') or line.startswith('//') or line.startswith('..'):
        return None, None, None

    # Match HEXT format: ADDRESS = VALUE [// comment]
    # Example: "914008 = 26" or "9261C0 = 1E 00 3B 01 // some comment"
    match = re.match(r'^([0-9A-Fa-f]+)\s*=\s*([0-9A-Fa-f\s]+)\s*(?://\s*(.+))?$', line)

    if not match:
        return None, None, None

    address = normalize_address(match.group(1))
    value = match.group(2).strip()
    comment = match.group(3).strip() if match.group(3) else ""

    return address, value, comment

def categorize_comment(comment: str) -> List[str]:
    """Auto-categorize based on comment keywords."""
    categories = []
    comment_lower = comment.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in comment_lower:
                categories.append(category)
                break

    return categories

def parse_hext_file(file_path: str) -> Dict[str, Dict]:
    """Parse a single HEXT file and extract all addresses."""
    addresses = {}

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        previous_line = ""

        for i, line in enumerate(lines):
            addr, value, comment = parse_hext_line(line)

            if addr is None:
                # Keep track of non-HEXT lines as potential comments
                previous_line = line.strip()
                continue

            # If we have an address but no inline comment, check previous line
            if not comment and previous_line:
                # Previous line might be a comment for this address
                # Skip if it looks like a file header
                if not previous_line.startswith('..') and not previous_line.startswith('#'):
                    comment = previous_line

            if addr not in addresses:
                addresses[addr] = {
                    'values': [],
                    'comments': [],
                    'files': []
                }

            addresses[addr]['values'].append(value)
            if comment:
                addresses[addr]['comments'].append(comment)
            addresses[addr]['files'].append(file_path)

            # Reset previous line after using it
            previous_line = ""

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return addresses

def analyze_new_directory():
    """Analyze all HEXT files in new directory."""
    print(f"Analyzing new directory: {NEW_HEXT_DIR}")

    # Find all .txt files
    txt_files = list(Path(NEW_HEXT_DIR).rglob('*.txt'))
    print(f"Found {len(txt_files)} HEXT files\n")

    all_addresses = {}

    for i, file_path in enumerate(txt_files, 1):
        if i % 10 == 0:
            print(f"Processing file {i}/{len(txt_files)}...")

        file_addresses = parse_hext_file(str(file_path))

        # Merge addresses
        for addr, data in file_addresses.items():
            if addr not in all_addresses:
                all_addresses[addr] = {
                    'values': [],
                    'comments': [],
                    'files': []
                }

            all_addresses[addr]['values'].extend(data['values'])
            all_addresses[addr]['comments'].extend(data['comments'])
            all_addresses[addr]['files'].extend(data['files'])

    print(f"\nExtracted {len(all_addresses)} unique addresses from new files")
    return all_addresses

def load_existing_dataset():
    """Load existing ff7_ui_memory_map.json."""
    print(f"\nLoading existing dataset: {EXISTING_JSON}")

    with open(EXISTING_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} existing addresses")
    return data

def merge_datasets(existing: Dict, new: Dict):
    """Merge new addresses with existing dataset."""
    print("\n=== MERGING DATASETS ===\n")

    merged = dict(existing)  # Start with existing data
    new_count = 0
    improved_count = 0
    duplicate_count = 0

    new_addresses = []
    improved_addresses = []
    duplicate_addresses = []

    for addr, new_data in new.items():
        if addr not in merged:
            # New address discovered
            new_count += 1

            # Determine primary purpose from comments
            primary_purpose = ""
            if new_data['comments']:
                # Use the longest/most descriptive comment
                primary_purpose = max(new_data['comments'], key=len)

            # Get unique comments
            unique_comments = list(set(new_data['comments']))

            # Auto-categorize
            categories = []
            for comment in unique_comments:
                categories.extend(categorize_comment(comment))
            categories = list(set(categories))  # Remove duplicates

            # Parse values to find min/max
            value_ints = []
            for val in new_data['values']:
                # Try to parse hex values
                hex_bytes = val.split()
                for hb in hex_bytes:
                    try:
                        value_ints.append(int(hb, 16))
                    except:
                        pass

            merged[addr] = {
                "address": addr,
                "address_decimal": int(addr, 16),
                "primary_purpose": primary_purpose,
                "all_comments": unique_comments,
                "categories": categories,
                "value_min": min(value_ints) if value_ints else 0,
                "value_max": max(value_ints) if value_ints else 0,
                "value_count": len(set(new_data['values'])),
                "example_values": list(set(new_data['values']))[:5],
                "occurrence_count": len(new_data['files']),
                "example_files": [os.path.relpath(f, NEW_HEXT_DIR) for f in list(set(new_data['files']))[:3]]
            }

            new_addresses.append((addr, primary_purpose))

        else:
            # Address exists - check if we have better metadata
            duplicate_count += 1

            old_comments = set(merged[addr].get('all_comments', []))
            new_comments = set(new_data['comments'])

            # Check if new comments are more descriptive
            combined_comments = old_comments | new_comments

            if len(combined_comments) > len(old_comments):
                improved_count += 1

                # Update with better metadata
                merged[addr]['all_comments'] = list(combined_comments)

                # Update primary purpose if new one is longer/better
                if new_data['comments']:
                    new_primary = max(new_data['comments'], key=len)
                    old_primary = merged[addr].get('primary_purpose', '')

                    if len(new_primary) > len(old_primary):
                        improved_addresses.append((addr, old_primary, new_primary))
                        merged[addr]['primary_purpose'] = new_primary

                # Re-categorize with combined comments
                categories = merged[addr].get('categories', [])
                for comment in new_data['comments']:
                    categories.extend(categorize_comment(comment))
                merged[addr]['categories'] = list(set(categories))

                # Update value ranges
                old_values = merged[addr].get('example_values', [])
                combined_values = list(set(old_values + new_data['values']))
                merged[addr]['example_values'] = combined_values[:5]
                merged[addr]['value_count'] = len(combined_values)

            duplicate_addresses.append((addr, merged[addr].get('primary_purpose', 'Unknown')))

    print(f"NEW addresses found: {new_count}")
    print(f"IMPROVED metadata: {improved_count}")
    print(f"DUPLICATE addresses: {duplicate_count}")
    print(f"TOTAL merged addresses: {len(merged)}")

    return merged, {
        'new': new_addresses,
        'improved': improved_addresses,
        'duplicates': duplicate_addresses,
        'stats': {
            'new_count': new_count,
            'improved_count': improved_count,
            'duplicate_count': duplicate_count,
            'total_count': len(merged)
        }
    }

def generate_reports(analysis_data: Dict):
    """Generate detailed analysis reports."""

    # Report 1: New Addresses Report
    report_file = os.path.join(OUTPUT_DIR, 'new_addresses_report.md')

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 UI Memory Map - New Addresses Discovery Report\n\n")
        f.write(f"**Generated:** 2026-01-21 JST\n")
        f.write(f"**Session:** 9bfbe481-e8b6-4c52-868e-5e825185a4b4\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **New addresses discovered:** {analysis_data['stats']['new_count']}\n")
        f.write(f"- **Improved metadata:** {analysis_data['stats']['improved_count']}\n")
        f.write(f"- **Duplicate addresses:** {analysis_data['stats']['duplicate_count']}\n")
        f.write(f"- **Total unique addresses:** {analysis_data['stats']['total_count']}\n\n")

        f.write("## Top 20 New Discoveries\n\n")
        f.write("| Address | Decimal | Purpose |\n")
        f.write("|---------|---------|----------|\n")

        for addr, purpose in sorted(analysis_data['new'][:20]):
            decimal = int(addr, 16)
            f.write(f"| {addr} | {decimal} | {purpose[:60]} |\n")

        f.write("\n## All New Addresses by Category\n\n")

        # Group by category
        categorized = defaultdict(list)
        for addr, purpose in analysis_data['new']:
            categorized['Uncategorized'].append((addr, purpose))

        for category, items in sorted(categorized.items()):
            if items:
                f.write(f"\n### {category} ({len(items)} addresses)\n\n")
                for addr, purpose in sorted(items[:10]):
                    f.write(f"- **{addr}**: {purpose}\n")

    print(f"\nGenerated: {report_file}")

    # Report 2: Duplicate Analysis
    dup_file = os.path.join(OUTPUT_DIR, 'duplicate_analysis.md')

    with open(dup_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 UI Memory Map - Duplicate Analysis\n\n")
        f.write(f"**Generated:** 2026-01-21 JST\n\n")

        f.write("## Summary\n\n")
        f.write(f"Total duplicate addresses: {analysis_data['stats']['duplicate_count']}\n\n")

        f.write("## Addresses with Improved Metadata\n\n")
        f.write("| Address | Old Description | New Description |\n")
        f.write("|---------|----------------|----------------|\n")

        for addr, old_desc, new_desc in analysis_data['improved'][:50]:
            f.write(f"| {addr} | {old_desc[:30]} | {new_desc[:30]} |\n")

    print(f"Generated: {dup_file}")

def main():
    """Main execution flow."""
    print("=" * 80)
    print("FF7 UI Memory Map - New Dataset Merger")
    print("=" * 80)

    # Step 1: Analyze new directory
    new_addresses = analyze_new_directory()

    # Step 2: Load existing dataset
    existing_data = load_existing_dataset()

    # Step 3: Merge datasets
    merged_data, analysis = merge_datasets(existing_data, new_addresses)

    # Step 4: Save merged dataset
    output_file = os.path.join(OUTPUT_DIR, 'ff7_ui_memory_map_merged.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved merged dataset: {output_file}")

    # Step 5: Generate reports
    generate_reports(analysis)

    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
