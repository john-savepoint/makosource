#!/usr/bin/env python3
"""
Final comprehensive code block fixer

Created: 2025-11-28 13:26:11 JST (Friday)
Context: Handles ALL code block patterns - simple inline, italic inline, and fragmented fenced.
         Preserves contributor context with inline comments.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
from pathlib import Path


def merge_and_fix_code_blocks(content):
    """
    Comprehensive code block fixer that handles:
    1. Simple inline code with backslashes
    2. Italic inline code (contributor additions)
    3. Fragmented fenced blocks split by italic lines
    """

    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # ========================================
        # CASE 1: Fenced block (possibly fragmented)
        # ========================================
        if line.startswith('```'):
            lang_match = re.match(r'```(\w*)', line)
            lang = lang_match.group(1) if lang_match else ''

            code_lines = []
            i += 1  # Skip opening fence

            # Collect code and merge fragments
            while i < len(lines):
                current = lines[i]

                # End of fenced block
                if current == '```':
                    i += 1

                    # Look ahead for continuation pattern:
                    # ` `*`code`*\
                    # ```
                    if i < len(lines):
                        next_line = lines[i] if i < len(lines) else ''

                        # Check for italic inline code
                        italic_match = re.match(r'^\` \`\*\`([^`]+)\`\*\\?$', next_line)

                        if italic_match:
                            # Collect all consecutive italic lines
                            while i < len(lines):
                                check_line = lines[i]
                                italic_check = re.match(r'^\` \`\*\`([^`]+)\`\*\\?$', check_line)

                                if italic_check:
                                    # Add as contributor addition
                                    code_content = italic_check.group(1)
                                    code_lines.append(f' {code_content}  // contributor addition')
                                    i += 1
                                elif check_line.startswith('```') and check_line != '```':
                                    # New fence opening - continue merging
                                    i += 1
                                    break
                                elif check_line == '```':
                                    # Another closing fence after inline code
                                    i += 1
                                    break
                                else:
                                    # End of pattern
                                    break
                            continue

                    # No continuation, this is the real end
                    break
                else:
                    code_lines.append(current)
                    i += 1

            # Output merged block
            result.append(f'```{lang}')
            result.extend(code_lines)
            result.append('```')

        # ========================================
        # CASE 2: Inline code blocks (not in fences)
        # ========================================
        elif re.match(r'^`[^`]+`\\?$', line):
            code_lines = []
            start_i = i

            # Collect consecutive code lines
            while i < len(lines):
                current = lines[i]

                # Simple inline code
                simple_match = re.match(r'^`([^`]+)`\\?$', current)
                # Italic inline code (contributor)
                italic_match = re.match(r'^\` \`\*\`([^`]+)\`\*\\?$', current)

                if simple_match:
                    code_lines.append(simple_match.group(1))
                    i += 1
                elif italic_match:
                    code_content = italic_match.group(1)
                    code_lines.append(f' {code_content}  // contributor addition')
                    i += 1
                else:
                    break

            # Convert to fenced block if it looks like code
            if len(code_lines) >= 2:
                code_text = '\n'.join(code_lines)
                is_code = any(keyword in code_text for keyword in [
                    'typedef', 'struct', '{', '}', ';', 'uint', 'int16',
                    'int32', 'int8', '//'
                ])

                if is_code:
                    lang = 'c' if ('typedef' in code_text or 'struct' in code_text) else ''
                    result.append(f'```{lang}')
                    result.extend(code_lines)
                    result.append('```')
                else:
                    # Not code, keep original
                    result.extend(lines[start_i:i])
            else:
                # Single line, keep original
                result.extend(lines[start_i:i])

        # ========================================
        # CASE 3: Regular line
        # ========================================
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
    fixed_content = merge_and_fix_code_blocks(content)

    if original_content != fixed_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        # Count improvements
        orig_fences = original_content.count('```')
        new_fences = fixed_content.count('```')
        blocks_added = (new_fences - orig_fences) // 2

        contrib_lines = fixed_content.count('// contributor addition')

        if blocks_added > 0 or contrib_lines > 0:
            msg = []
            if blocks_added > 0:
                msg.append(f"{blocks_added} blocks")
            if contrib_lines > 0:
                msg.append(f"{contrib_lines} contributor lines")
            print(f"  ✅ Fixed: {', '.join(msg)}")
        else:
            print(f"  ✅ Cleaned code formatting")
        return 1
    else:
        print(f"  ⏭️  No changes needed")
        return 0


def main():
    """Process all markdown files"""

    print("=" * 70)
    print("Comprehensive Code Block Fix")
    print("  - Merges fragmented fenced blocks")
    print("  - Converts inline code to fenced blocks")
    print("  - Marks contributor additions with inline comments")
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
