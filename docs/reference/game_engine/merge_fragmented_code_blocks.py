#!/usr/bin/env python3
"""
Merge fragmented code blocks and strip inline italics

Created: 2025-11-28 13:22:34 JST (Friday)
Context: Pandoc creates fragmented fenced blocks when encountering inline italics.
         This script merges them into single clean blocks.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def merge_fragmented_blocks(content):
    """
    Merge fragmented code blocks separated by italic inline code.

    Pattern:
    ```c
    code
    ```
    ` `*`code`*\
    ```
    more code
    ```

    Becomes:
    ```c
    code
     code
    more code
    ```
    """

    # Split into lines for processing
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line starts a fenced code block
        if line.startswith('```'):
            lang_match = re.match(r'```(\w*)', line)
            lang = lang_match.group(1) if lang_match else ''

            code_block_lines = []
            i += 1  # Skip opening fence

            # Collect all code until we find the end or a fragment
            while i < len(lines):
                current = lines[i]

                # Check if this is the closing fence
                if current == '```':
                    i += 1

                    # Look ahead - is there inline italic code followed by another fence?
                    inline_and_fence_ahead = False
                    j = i
                    inline_code_lines = []

                    while j < len(lines):
                        ahead = lines[j]

                        # Check for italic inline code
                        italic_match = re.match(r'^\` \`\*\`([^`]+)\`\*\\?$', ahead)
                        if italic_match:
                            # Strip italic formatting, add to collection
                            inline_code_lines.append(' ' + italic_match.group(1))
                            j += 1
                        elif ahead.startswith('```') and ahead != '```':
                            # Another opening fence - this is a fragment continuation
                            inline_and_fence_ahead = True
                            i = j + 1  # Skip the opening fence
                            break
                        elif ahead == '```':
                            # Just a closing fence, not a fragment
                            break
                        else:
                            # Some other content
                            break

                    if inline_and_fence_ahead:
                        # Add the inline code lines (stripped of italics)
                        code_block_lines.extend(inline_code_lines)
                        # Continue collecting from the next fragment
                        continue
                    else:
                        # This was the real end of the block
                        break
                else:
                    code_block_lines.append(current)
                    i += 1

            # Output the merged block
            result.append(f'```{lang}')
            result.extend(code_block_lines)
            result.append('```')
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
    fixed_content = merge_fragmented_blocks(content)

    if original_content != fixed_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        print(f"  ✅ Merged fragmented code blocks")
        return 1
    else:
        print(f"  ⏭️  No fragmented blocks found")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Merging Fragmented Code Blocks")
    print("  - Combines blocks split by italic formatting")
    print("  - Strips italic emphasis (relies on syntax highlighting)")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent / 'markdown'

    total_files = 0

    for filepath in sorted(base_dir.glob('*.md')):
        if filepath.name.lower() == 'readme.md':
            continue

        changes = process_file(filepath)
        total_files += changes

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"✅ Fixed {total_files} files")
    print()


if __name__ == '__main__':
    main()
