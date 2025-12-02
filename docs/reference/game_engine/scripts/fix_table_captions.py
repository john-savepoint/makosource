#!/usr/bin/env python3
"""
Fix table caption placement in converted Markdown files

Created: 2025-11-28 13:12:46 JST (Friday)
Context: Pandoc places MediaWiki table captions AFTER tables in Markdown.
         This script moves them BEFORE tables to match original layout.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
import os
from pathlib import Path


def fix_table_captions(content):
    """
    Find patterns where table captions appear after tables and move them before.

    Pattern to match:
    | header | header |
    |:--:|:--:|
    | data | data |

    : Caption text here

    Should become:
    *Caption text here*

    | header | header |
    |:--:|:--:|
    | data | data |
    """

    # Pattern: table followed by definition list (caption)
    # This regex matches:
    # 1. A table (multiple lines starting with |)
    # 2. Followed by blank line
    # 3. Followed by ": caption text"

    pattern = r'(\|[^\n]+\|\n(?:\|[^\n]+\|\n)+)\n(:\s+(.+))\n'

    def replacer(match):
        table = match.group(1)
        full_caption = match.group(2)
        caption_text = match.group(3)

        # Format caption as emphasized text before table
        return f"*{caption_text}*\n\n{table}\n"

    # Apply replacement
    fixed = re.sub(pattern, replacer, content)

    return fixed


def process_file(filepath):
    """Process a single markdown file"""

    print(f"Processing: {filepath.name}")

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix captions
    original_content = content
    fixed_content = fix_table_captions(content)

    # Check if changes were made
    if original_content != fixed_content:
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        # Count how many captions were moved
        changes = content.count('\n: ') - fixed_content.count('\n: ')
        print(f"  ✅ Fixed {changes} table caption(s)")
        return changes
    else:
        print(f"  ⏭️  No captions to fix")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Fixing Table Caption Placement")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent / 'markdown'

    total_changes = 0
    files_changed = 0

    # Process all .md files (except readme.md)
    for filepath in sorted(base_dir.glob('*.md')):
        if filepath.name.lower() == 'readme.md':
            continue

        changes = process_file(filepath)
        if changes > 0:
            total_changes += changes
            files_changed += 1

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"✅ Fixed {total_changes} table captions across {files_changed} files")
    print()


if __name__ == '__main__':
    main()
