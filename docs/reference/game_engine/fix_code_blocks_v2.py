#!/usr/bin/env python3
"""
Fix code block formatting in converted Markdown files (Version 2)

Created: 2025-11-28 13:15:12 JST (Friday)
Context: Improved version that properly handles all inline code patterns.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def fix_code_blocks(content):
    """
    Convert inline code with backslashes to proper fenced code blocks.

    Handles both:
    - Lines ending with `\
    - Lines without backslash at the end
    """

    # Find sequences of backtick-wrapped lines (with or without backslash)
    # This matches multiple consecutive lines like:
    # `line1`\
    # `line2`\
    # `line3`
    # OR
    # `line1`
    # `line2`
    # But NOT single isolated lines

    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line starts a code block pattern
        if re.match(r'^`[^`]+`\\?$', line):
            # Collect all consecutive code lines
            code_lines = []
            start_i = i

            while i < len(lines):
                current = lines[i]
                match = re.match(r'^`([^`]+)`\\?$', current)

                if match:
                    code_lines.append(match.group(1))
                    i += 1
                else:
                    break

            # Only convert if we have multiple lines (2+)
            if len(code_lines) >= 2:
                # Check if this looks like code
                code_text = '\n'.join(code_lines)
                is_code = any(keyword in code_text for keyword in [
                    'typedef', 'struct', '{', '}', ';', 'uint', 'int16', 'int32',
                    'int8', 'float', 'double', 'void', '//'
                ])

                if is_code:
                    # Determine language
                    if 'typedef' in code_text or 'struct' in code_text:
                        lang = 'c'
                    else:
                        lang = ''

                    # Create fenced code block
                    result.append(f'```{lang}')
                    result.extend(code_lines)
                    result.append('```')
                else:
                    # Not code, keep original
                    result.extend(lines[start_i:i])
            else:
                # Single line, keep original
                result.extend(lines[start_i:i])
        else:
            result.append(line)
            i += 1

    return '\n'.join(result)


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

        # Count fenced code blocks added
        original_fences = original_content.count('```')
        fixed_fences = fixed_content.count('```')
        blocks_added = (fixed_fences - original_fences) // 2

        print(f"  ✅ Converted {blocks_added} code blocks to fenced format")
        return blocks_added
    else:
        print(f"  ⏭️  No code blocks to fix")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Fixing Code Block Formatting (Version 2)")
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
    print(f"✅ Converted {total_changes} code blocks across {files_changed} files")
    print()


if __name__ == '__main__':
    main()
