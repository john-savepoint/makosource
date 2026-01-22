#!/usr/bin/env python3
"""
Clean German FF7 strings using manual cleaning map
Created: 2026-01-05 19:29 JST
Session: ff862825-4ec7-4a49-a932-e9e5dcc0ea9f

This script:
1. Reads the manual cleaning map
2. For each mapped entry, finds where the clean text starts
3. Calculates the new offset by adding the byte position
4. Outputs cleaned strings with corrected offsets
"""

import re
from manual_cleaning_map import CLEAN_TEXT_MAP

input_file = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_clean_offsets.txt"
output_file = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_strings_manual_cleaned.txt"

def find_text_position(full_text, clean_text):
    """Find the byte position where clean_text starts in full_text"""
    pos = full_text.find(clean_text)
    if pos == -1:
        return None
    return pos

cleaned_entries = []
stats = {
    'total': 0,
    'cleaned': 0,
    'not_found': 0,
    'kept': 0
}

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    # Keep headers and separators
    if line.startswith('#') or line.startswith('='):
        cleaned_entries.append(line.rstrip())
        continue

    if line.strip() == '':
        cleaned_entries.append('')
        continue

    match = re.match(r'\[\s*(\d+)\]\s+(0x[0-9A-F]+)\s+\(([^)]+)\)\s+\|\s+(.+)$', line)
    if not match:
        continue

    stats['total'] += 1
    index = int(match.group(1))
    offset_hex = match.group(2)
    pad_info = match.group(3)
    text = match.group(4).strip()

    # Check if this index is in our manual cleaning map
    if index in CLEAN_TEXT_MAP:
        clean_text = CLEAN_TEXT_MAP[index]

        # Find where the clean text starts
        pos = find_text_position(text, clean_text)

        if pos is not None and pos > 0:
            # Calculate new offset
            original_offset = int(offset_hex, 16)
            new_offset = original_offset + pos
            new_offset_hex = f"0x{new_offset:08X}"

            # Extract clean text from position onwards
            extracted_text = text[pos:].strip()

            stats['cleaned'] += 1
            cleaned_entries.append(f"[{index:>5}] {new_offset_hex} (cleaned) | {extracted_text}")

            print(f"[{index:>3}] Cleaned: removed {pos} bytes")
            print(f"  Expected: {clean_text}")
            print(f"  Got:      {extracted_text[:60]}")
            print(f"  Old offset: {offset_hex} → New offset: {new_offset_hex}")
            print()
        elif pos == 0:
            # Clean text is already at the start
            stats['kept'] += 1
            cleaned_entries.append(f"[{index:>5}] {offset_hex} (already clean) | {text}")
            print(f"[{index:>3}] Already clean at start")
            print()
        else:
            # Clean text not found
            stats['not_found'] += 1
            cleaned_entries.append(f"[{index:>5}] {offset_hex} (NOT FOUND: {clean_text[:20]}) | {text[:80]}")
            print(f"[{index:>3}] WARNING: Could not find '{clean_text}' in text")
            print(f"  Text: {text[:100]}")
            print()
    else:
        # Not in cleaning map, keep as-is
        stats['kept'] += 1
        cleaned_entries.append(f"[{index:>5}] {offset_hex} ({pad_info}) | {text}")

# Write output
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(cleaned_entries))

print("="*70)
print("CLEANING SUMMARY")
print("="*70)
print(f"Total entries:           {stats['total']}")
print(f"Cleaned:                 {stats['cleaned']}")
print(f"Already clean:           {stats['kept'] - (stats['total'] - stats['cleaned'] - stats['not_found'])}")
print(f"Not found (warnings):    {stats['not_found']}")
print(f"Kept unchanged:          {stats['kept']}")
print(f"\nOutput: {output_file}")
