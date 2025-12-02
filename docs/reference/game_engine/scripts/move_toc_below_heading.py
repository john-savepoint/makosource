#!/usr/bin/env python3
"""
Move TOC to below the main heading

Created: 2025-11-28 13:37:21 JST (Friday)
Context: TOC should appear after the H1 heading for better readability.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def move_toc_below_heading(content):
    """
    Move TOC from top of file to below the H1 heading.

    Before:
    - [TOC items...]
      - [Sub items...]

    # Heading

    After:
    # Heading

    - [TOC items...]
      - [Sub items...]
    """

    lines = content.split('\n')

    # Find TOC lines (start with -)
    toc_lines = []
    first_non_toc_idx = 0

    for i, line in enumerate(lines):
        if line.startswith('-') or line.startswith('  -'):
            toc_lines.append(line)
        elif line.strip() == '':
            # Empty line, could be part of TOC section
            if toc_lines:  # Only add if we've started collecting TOC
                toc_lines.append(line)
        else:
            # First non-TOC, non-empty line
            first_non_toc_idx = i
            break

    # Find H1 heading
    h1_idx = None
    for i in range(first_non_toc_idx, len(lines)):
        if lines[i].startswith('# '):
            h1_idx = i
            break

    if not toc_lines or h1_idx is None:
        # No TOC or no H1, return unchanged
        return content

    # Remove TOC from top
    remaining_lines = lines[first_non_toc_idx:]

    # Find H1 in remaining lines
    new_h1_idx = None
    for i, line in enumerate(remaining_lines):
        if line.startswith('# '):
            new_h1_idx = i
            break

    if new_h1_idx is None:
        return content

    # Reconstruct: H1, blank line, TOC, blank line, rest
    result = []
    result.append(remaining_lines[new_h1_idx])  # H1 heading
    result.append('')  # Blank line
    result.extend(toc_lines)  # TOC
    result.append('')  # Blank line after TOC
    result.extend(remaining_lines[new_h1_idx + 1:])  # Rest of content

    return '\n'.join(result)


def process_file(filepath):
    """Process a single markdown file"""

    print(f"Processing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixed_content = move_toc_below_heading(content)

    if original_content != fixed_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        print(f"  ✅ Moved TOC below heading")
        return 1
    else:
        print(f"  ⏭️  No changes needed")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Moving TOC Below Headings")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent / 'markdown'
    files_changed = 0

    for filepath in sorted(base_dir.glob('*.md')):
        if filepath.name.lower() == 'readme.md':
            continue

        changed = process_file(filepath)
        files_changed += changed

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"✅ Fixed {files_changed} files")
    print()


if __name__ == '__main__':
    main()
