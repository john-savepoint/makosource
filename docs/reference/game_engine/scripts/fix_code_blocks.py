#!/usr/bin/env python3
"""
Fix code block formatting in converted Markdown files

Created: 2025-11-28 13:15:12 JST (Friday)
Context: Pandoc converts MediaWiki indented code to inline backticks with backslashes.
         This script converts them to proper fenced code blocks.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def fix_code_blocks(content):
    """
    Convert inline code with backslashes to proper fenced code blocks.

    Pattern to match:
    `typedef struct`\
    `{`\
    `  uint16 NumberOfTriangles;`\
    `  uint16 NumberOfVertices;`\
    `} WorldMeshHeader;`

    Should become:
    ```c
    typedef struct
    {
      uint16 NumberOfTriangles;
      uint16 NumberOfVertices;
    } WorldMeshHeader;
    ```
    """

    # Pattern: Multiple consecutive lines of backtick-enclosed code with backslashes
    # Matches: `code`\ followed by newline, repeated multiple times
    pattern = r'(`[^`\n]+`\\\n)+'

    def replacer(match):
        code_block = match.group(0)

        # Extract code lines
        lines = re.findall(r'`([^`]+)`', code_block)

        # Skip if it's just a single line (probably actual inline code)
        if len(lines) < 2:
            return code_block

        # Check if this looks like C/C++ code (typedef, struct, braces, semicolons)
        code_text = '\n'.join(lines)
        is_code = any(keyword in code_text for keyword in [
            'typedef', 'struct', '{', '}', ';', 'uint', 'int16', 'int32'
        ])

        if not is_code:
            return code_block

        # Create fenced code block
        # Determine language based on content
        if 'typedef' in code_text or 'struct' in code_text:
            lang = 'c'
        else:
            lang = ''

        fenced = f'```{lang}\n{code_text}\n```'

        return fenced

    # Apply replacement
    fixed = re.sub(pattern, replacer, content, flags=re.MULTILINE)

    return fixed


def process_file(filepath):
    """Process a single markdown file"""

    print(f"Processing: {filepath.name}")

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix code blocks
    original_content = content
    fixed_content = fix_code_blocks(content)

    # Check if changes were made
    if original_content != fixed_content:
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        # Count how many code blocks were converted
        original_blocks = len(re.findall(r'`[^`]+`\\', original_content))
        fixed_blocks = len(re.findall(r'`[^`]+`\\', fixed_content))
        changes = (original_blocks - fixed_blocks) // 2  # Rough estimate

        print(f"  ✅ Converted ~{changes} code blocks to fenced format")
        return changes
    else:
        print(f"  ⏭️  No code blocks to fix")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Fixing Code Block Formatting")
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
    print(f"✅ Converted ~{total_changes} code blocks across {files_changed} files")
    print()


if __name__ == '__main__':
    main()
