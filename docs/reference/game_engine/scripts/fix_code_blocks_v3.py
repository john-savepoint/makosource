#!/usr/bin/env python3
"""
Fix code block formatting with inline italics (Version 3)

Created: 2025-11-28 13:19:11 JST (Friday)
Context: MediaWiki allows italics in code blocks, Markdown doesn't.
         This version handles code blocks that Pandoc split due to inline formatting.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def merge_broken_code_blocks(content):
    """
    Merge code blocks that Pandoc split due to inline italic formatting.

    Handles patterns like:
    ```c
    normal code
    ```
    ` `*`italic code`*\
    ```
    more normal code
    ```

    Converts to single block with comment markers for emphasis.
    """

    # Pattern: fenced code block followed by inline code with italics, followed by another fence
    pattern = r'(```\w*\n(?:[^`]|`[^`])+?\n```)\n((?:` `\*`[^`]+`\*\\\n)+)(```\n(?:[^`]|`[^`])+?\n```)'

    def merge_blocks(match):
        first_block = match.group(1)
        inline_italic = match.group(2)
        last_block = match.group(3)

        # Extract language from first block
        lang_match = re.match(r'```(\w*)\n', first_block)
        lang = lang_match.group(1) if lang_match else ''

        # Extract code from first block
        first_code = re.search(r'```\w*\n(.+)\n```', first_block, re.DOTALL).group(1)

        # Convert inline italic lines to code with emphasis markers
        italic_lines = re.findall(r'` `\*`([^`]+)`\*\\', inline_italic)
        italic_code = '\n'.join(f' {line}  // ← emphasized' for line in italic_lines)

        # Extract code from last block (remove opening fence)
        last_code = re.search(r'```\n(.+)\n```', last_block, re.DOTALL).group(1)

        # Merge all parts
        merged = f'```{lang}\n{first_code}\n{italic_code}\n{last_code}\n```'

        return merged

    # Apply merging
    fixed = re.sub(pattern, merge_blocks, content, flags=re.DOTALL)

    return fixed


def fix_remaining_inline_code(content):
    """
    Fix any remaining inline code blocks (sequences of backtick lines)
    """

    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for inline code pattern (but not in existing fenced blocks)
        if re.match(r'^`[^`]+`\\?$', line) and '```' not in line:
            # Look ahead to see if this is part of a code block
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

            # Only convert if we have multiple lines and it looks like code
            if len(code_lines) >= 2:
                code_text = '\n'.join(code_lines)
                is_code = any(keyword in code_text for keyword in [
                    'typedef', 'struct', '{', '}', ';', 'uint', 'int16'
                ])

                if is_code:
                    lang = 'c' if 'typedef' in code_text or 'struct' in code_text else ''
                    result.append(f'```{lang}')
                    result.extend(code_lines)
                    result.append('```')
                else:
                    result.extend(lines[start_i:i])
            else:
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

    original_content = content

    # Step 1: Merge broken code blocks
    content = merge_broken_code_blocks(content)

    # Step 2: Fix remaining inline code
    content = fix_remaining_inline_code(content)

    # Check if changes were made
    if original_content != content:
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Fixed code blocks")
        return 1
    else:
        print(f"  ⏭️  No fixes needed")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Fixing Code Block Formatting (Version 3)")
    print("  - Merges blocks split by italic formatting")
    print("  - Converts italic lines to emphasized comments")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent / 'markdown'

    total_changes = 0

    # Process all .md files (except readme.md)
    for filepath in sorted(base_dir.glob('*.md')):
        if filepath.name.lower() == 'readme.md':
            continue

        changes = process_file(filepath)
        total_changes += changes

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"✅ Fixed {total_changes} files")
    print()


if __name__ == '__main__':
    main()
