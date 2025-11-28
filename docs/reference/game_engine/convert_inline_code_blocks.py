#!/usr/bin/env python3
"""
Convert inline code blocks to fenced blocks (handles contributor italics)

Created: 2025-11-28 13:26:11 JST (Friday)
Context: Single-pass conversion of ALL inline code patterns to fenced blocks.
         Handles mixed inline/italic code in one block.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def convert_inline_to_fenced(content):
    """
    Convert all inline code blocks (with or without italics) to fenced blocks.

    Handles:
    - `simple code`\
    - ` `*`italic code`*\  (contributor additions)

    All converted in ONE pass to ONE fenced block.
    """

    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for START of inline code block
        # Matches: `code`\ OR ` `*`code`*\
        # Need to check for EITHER pattern to start collection
        is_inline_code_start = (
            re.match(r'^`[^`]+`\\?$', line) or  # Simple inline code
            re.match(r'^` `\*`[^`]+`\*\\?$', line)  # Italic inline code
        )

        if is_inline_code_start:
            code_lines = []
            start_i = i

            # Collect ALL consecutive code lines (simple OR italic)
            while i < len(lines):
                current = lines[i]

                # Pattern 1: Simple inline code
                simple_match = re.match(r'^`([^`]+)`\\?$', current)
                # Pattern 2: Italic inline code (contributor)
                italic_match = re.match(r'^\` \`\*\`([^`]+)\`\*\\?$', current)

                if simple_match:
                    code_lines.append(simple_match.group(1))
                    i += 1
                elif italic_match:
                    # Mark as contributor addition
                    code_content = italic_match.group(1)
                    code_lines.append(f' {code_content}  // contributor addition')
                    i += 1
                else:
                    # Not code anymore
                    break

            # Convert to fenced block if this looks like code (2+ lines)
            if len(code_lines) >= 2:
                code_text = '\n'.join(code_lines)

                # Detect if this is code
                is_code = any(keyword in code_text for keyword in [
                    'typedef', 'struct', '{', '}', ';', 'uint', 'int16',
                    'int32', 'int8', 'void', '//'
                ])

                if is_code:
                    # Determine language
                    lang = 'c' if ('typedef' in code_text or 'struct' in code_text) else ''

                    # Create fenced block
                    result.append(f'```{lang}')
                    result.extend(code_lines)
                    result.append('```')
                else:
                    # Not code, keep original
                    result.extend(lines[start_i:i])
            else:
                # Single line, keep as-is
                result.extend(lines[start_i:i])
        else:
            # Not inline code
            result.append(line)
            i += 1

    return '\n'.join(result)


def process_file(filepath):
    """Process a single markdown file"""

    print(f"Processing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixed_content = convert_inline_to_fenced(content)

    if original_content != fixed_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        # Count stats
        blocks_added = (fixed_content.count('```') - original_content.count('```')) // 2
        contrib_lines = fixed_content.count('// contributor addition')

        if blocks_added > 0:
            msg = f"{blocks_added} code blocks"
            if contrib_lines > 0:
                msg += f", {contrib_lines} contributor lines marked"
            print(f"  ✅ {msg}")
            return 1
        else:
            print(f"  ✅ Cleaned formatting")
            return 1
    else:
        print(f"  ⏭️  No changes needed")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Converting Inline Code Blocks to Fenced Blocks")
    print("  - Handles simple and italic inline code")
    print("  - Marks contributor additions with comments")
    print("  - Single-pass clean conversion")
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
