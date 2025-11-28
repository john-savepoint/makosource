#!/usr/bin/env python3
"""
Fix WorldMap Module code blocks with contributor annotations

Created: 2025-11-28 13:25:13 JST (Friday)
Context: Italic code lines were contributor additions - preserve context with comments.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re


def fix_worldmap_code_blocks():
    """
    Fix the fragmented code block in FF7_WorldMap_Module.md

    Merges:
    ```c
    code
    ```
    ` `*`code`*\
    ```
    code
    ```

    Into:
    ```c
    code
     code  // contributor addition
    code
    ```
    """

    filepath = 'markdown/FF7_WorldMap_Module.md'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: Find the specific fragmented block
    # This is surgical - we know exactly what we're looking for

    # First fragmented block (Triangle struct)
    pattern1 = r'```c\ntypedef struct\n\{\n uint8 Vertex0Index;\n uint8 Vertex1Index;\n uint8 Vertex2Index;\n```\n` `\*`uint8 WalkabilityInfo:5;`\*\\\n` `\*`uint8 Unknown:3;`\*\\\n``` uint8 uVertex0, vVertex0;\n uint8 uVertex1, vVertex1;\n uint8 uVertex2, vVertex2;\n```\n` `\*`uint16 TextureInfo:9;`\*\\\n` `\*`uint16 Location:7;`\*\\\n`\} WorldMeshTriangle;`'

    replacement1 = '''```c
typedef struct
{
 uint8 Vertex0Index;
 uint8 Vertex1Index;
 uint8 Vertex2Index;
 uint8 WalkabilityInfo:5;  // contributor addition
 uint8 Unknown:3;           // contributor addition
 uint8 uVertex0, vVertex0;
 uint8 uVertex1, vVertex1;
 uint8 uVertex2, vVertex2;
 uint16 TextureInfo:9;      // contributor addition
 uint16 Location:7;         // contributor addition
} WorldMeshTriangle;
```'''

    # Apply fix
    if pattern1 in content:
        content = content.replace(pattern1, replacement1)
        print("✅ Fixed Triangle struct code block")
    else:
        print("⚠️  Triangle pattern not found - trying regex approach...")

        # More flexible regex approach
        content = re.sub(
            r'(```c\ntypedef struct\n\{[^`]+)```\n` `\*`([^`]+)`\*\\\n` `\*`([^`]+)`\*\\\n```\n([^`]+)```\n` `\*`([^`]+)`\*\\\n` `\*`([^`]+)`\*\\\n`(\} \w+;)`',
            lambda m: f'```c\ntypedef struct\n{{\n{m.group(1).split("{")[1]}\n {m.group(2)}  // contributor addition\n {m.group(3)}  // contributor addition\n{m.group(4)}\n {m.group(5)}  // contributor addition\n {m.group(6)}  // contributor addition\n{m.group(7)}\n```',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        print("✅ Applied regex fix")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Fixed: {filepath}")


if __name__ == '__main__':
    print("=" * 70)
    print("Fixing WorldMap Module Code Blocks")
    print("  - Merges fragmented blocks")
    print("  - Marks contributor additions with comments")
    print("=" * 70)
    print()

    fix_worldmap_code_blocks()

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
