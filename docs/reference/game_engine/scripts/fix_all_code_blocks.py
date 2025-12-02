#!/usr/bin/env python3
"""
Convert ALL code blocks to fenced format (strips italics)

Created: 2025-11-28 13:22:34 JST (Friday)
Context: Strip italic formatting from code blocks and convert to proper fenced blocks.
         Syntax highlighting will provide better emphasis than inline italics anyway.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def fix_all_code_blocks(content):
    """
    Convert all inline code blocks to fenced blocks, stripping italics.

    Handles:
    - Simple inline code: `code`\
    - Italic inline code: ` `*`code`*\
    """

    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for code block pattern (backtick at start)
        # Matches: `code`\ or ` `*`code`*\
        if re.match(r'^`[^`]*`\\?$', line):
            code_lines = []
            start_i = i

            # Collect all consecutive code lines
            while i < len(lines):
                current = lines[i]

                # Match either:
                # - `code`\
                # - ` `*`code`*\
                simple_match = re.match(r'^`([^`]+)`\\?$', current)
                italic_match = re.match(r'^` `\*`([^`]+)`\*\\?$', current)

                if simple_match:
                    code_lines.append(simple_match.group(1))
                    i += 1
                elif italic_match:
                    # Strip italic formatting, keep the code
                    code_lines.append(' ' + italic_match.group(1))  # Preserve indentation
                    i += 1
                else:
                    break

            # Only convert if we have 2+ lines and it looks like code
            if len(code_lines) >= 2:
                code_text = '\n'.join(code_lines)

                # Detect if this is code
                is_code = any(keyword in code_text for keyword in [
                    'typedef', 'struct', '{', '}', ';', 'uint', 'int16',
                    'int32', 'int8', 'float', 'double', 'void', '//'
                ])

                if is_code:
                    # Determine language
                    if 'typedef' in code_text or 'struct' in code_text:
                        lang = 'c'
                    else:
                        lang = ''

                    # Create fenced block
                    result.append(f'```{lang}')
                    result.extend(code_lines)
                    result.append('```')
                else:
                    # Not code, restore original
                    result.extend(lines[start_i:i])
            else:
                # Single line, keep as-is
                result.extend(lines[start_i:i])
        else:
            result.append(line)
            i += 1

    return '\n'.join(result)


def process_file(filepath):
    """Process a single markdown file"""

    print(f"Processing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixed_content = fix_all_code_blocks(content)

    if original_content != fixed_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        # Count fenced blocks added
        original_fences = original_content.count('```')
        fixed_fences = fixed_content.count('```')
        blocks_added = (fixed_fences - original_fences) // 2

        if blocks_added > 0:
            print(f"  ✅ Converted {blocks_added} code blocks to fenced format")
            return blocks_added
        else:
            print(f"  ✅ Cleaned up code formatting")
            return 1
    else:
        print(f"  ⏭️  No code blocks to fix")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Converting All Code Blocks to Fenced Format")
    print("  - Strips italic formatting (syntax highlighting is better)")
    print("  - Creates proper fenced code blocks")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent / 'markdown'

    total_blocks = 0
    files_changed = 0

    for filepath in sorted(base_dir.glob('*.md')):
        if filepath.name.lower() == 'readme.md':
            continue

        blocks = process_file(filepath)
        if blocks > 0:
            total_blocks += blocks
            files_changed += 1

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"✅ Converted {total_blocks} code blocks across {files_changed} files")
    print()


if __name__ == '__main__':
    main()
