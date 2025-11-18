#!/usr/bin/env python3
"""
FINDINGS.md Document Sharding Script

Created: 2025-11-18 17:15:00 JST (Tuesday)
Session-ID: 596059e7-f5a7-4892-bce3-daf9c7c0a824
Author: John Zealand-Doyle
Purpose: Split the massive FINDINGS.md file into smaller, manageable sections
         based on its natural heading structure.

Context:
The original FINDINGS.md file is 3,274 lines long, making it difficult for AI
agents to process efficiently and for humans to navigate specific sections.
This script intelligently divides the document into logical chunks based on
major section headings (## level).

Design Philosophy:
- Preserve document structure and metadata
- Create self-contained section files
- Maintain cross-reference capability
- Enable easy section updates without touching entire document
- Generate an index/manifest for navigation
"""

import re
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentSection:
    """Represents a logical section of the FINDINGS document."""
    title: str
    level: int  # Heading level (2 for ##, 3 for ###, etc.)
    start_line: int
    end_line: int
    content: List[str]
    filename: str  # Generated filename for this section


class FindingsShardingTool:
    """
    Intelligently shards the FINDINGS.md document into smaller, focused files.

    Strategy:
    - Split on ## level headings (major sections)
    - Preserve all content including session discoveries
    - Maintain metadata and cross-references
    - Generate manifest file for navigation
    """

    def __init__(self, input_file: Path, output_dir: Path):
        self.input_file = input_file
        self.output_dir = output_dir
        self.sections: List[DocumentSection] = []
        self.metadata: List[str] = []  # Document header/metadata

    def parse_document(self) -> None:
        """Parse the FINDINGS.md file and identify section boundaries."""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_section = None
        metadata_end = 0

        # Extract metadata (everything before first ## heading)
        for i, line in enumerate(lines):
            if re.match(r'^##\s+', line):
                metadata_end = i
                break
            self.metadata.append(line)

        # Parse sections
        for i, line in enumerate(lines[metadata_end:], start=metadata_end):
            # Check for ## level headings (major sections)
            heading_match = re.match(r'^(#{2,})\s+(.+)$', line)

            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                # Only split on ## level (level 2) headings
                if level == 2:
                    # Save previous section if exists
                    if current_section:
                        current_section.end_line = i - 1
                        current_section.content = lines[current_section.start_line:i]
                        self.sections.append(current_section)

                    # Create new section
                    filename = self._generate_filename(title)
                    current_section = DocumentSection(
                        title=title,
                        level=level,
                        start_line=i,
                        end_line=-1,  # Will be set when next section starts
                        content=[],
                        filename=filename
                    )

        # Don't forget the last section
        if current_section:
            current_section.end_line = len(lines)
            current_section.content = lines[current_section.start_line:]
            self.sections.append(current_section)

    def _generate_filename(self, title: str) -> str:
        """
        Generate a clean filename from section title.

        Examples:
            "Session 2 Critical Discoveries" -> "02_session_2_critical_discoveries.md"
            "The Core Technical Problem" -> "03_core_technical_problem.md"
        """
        # Convert to lowercase and replace spaces with underscores
        clean_title = title.lower()
        clean_title = re.sub(r'[^\w\s-]', '', clean_title)
        clean_title = re.sub(r'[-\s]+', '_', clean_title)

        # Add section number prefix for ordering
        section_num = len(self.sections) + 1
        return f"{section_num:02d}_{clean_title}.md"

    def write_sections(self) -> None:
        """Write each section to its own file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for section in self.sections:
            output_file = self.output_dir / section.filename

            with open(output_file, 'w', encoding='utf-8') as f:
                # Write section header with metadata
                f.write(f"# {section.title}\n\n")
                f.write(f"**Extracted From**: FINDINGS.md\n")
                f.write(f"**Section Lines**: {section.start_line}-{section.end_line}\n")
                f.write(f"**Extraction Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
                f.write(f"**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824\n\n")
                f.write("---\n\n")

                # Write content (skip the heading line since we already wrote it)
                f.writelines(section.content[1:])

            print(f"✓ Created: {section.filename} ({len(section.content)} lines)")

    def write_manifest(self) -> None:
        """Generate a manifest/index file for navigation."""
        manifest_file = self.output_dir / "00_INDEX.md"

        with open(manifest_file, 'w', encoding='utf-8') as f:
            f.write("# FINDINGS.md - Document Index\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
            f.write(f"**Source File**: {self.input_file.name}\n")
            f.write(f"**Total Sections**: {len(self.sections)}\n")
            f.write(f"**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824\n\n")
            f.write("---\n\n")

            # Write original metadata
            f.write("## Original Document Metadata\n\n")
            f.writelines(self.metadata)
            f.write("\n---\n\n")

            # Write table of contents
            f.write("## Section Index\n\n")
            f.write("| # | Section Title | Filename | Lines | Size |\n")
            f.write("|---|---------------|----------|-------|------|\n")

            for i, section in enumerate(self.sections, start=1):
                line_count = section.end_line - section.start_line
                size_kb = len(''.join(section.content).encode('utf-8')) / 1024
                f.write(f"| {i:02d} | {section.title} | `{section.filename}` | {line_count} | {size_kb:.1f}KB |\n")

            f.write("\n---\n\n")

            # Write navigation guide
            f.write("## Quick Navigation Guide\n\n")
            f.write("### By Topic\n\n")

            # Group sections by topic
            topics = {
                "Research Sessions": [],
                "Technical Analysis": [],
                "Tools & Resources": [],
                "Implementation": [],
                "Community": []
            }

            for section in self.sections:
                title_lower = section.title.lower()
                if 'session' in title_lower:
                    topics["Research Sessions"].append(section)
                elif any(word in title_lower for word in ['tool', 'documentation', 'resources']):
                    topics["Tools & Resources"].append(section)
                elif any(word in title_lower for word in ['approach', 'implementation', 'roadmap', 'modification']):
                    topics["Implementation"].append(section)
                elif any(word in title_lower for word in ['community', 'contact']):
                    topics["Community"].append(section)
                else:
                    topics["Technical Analysis"].append(section)

            for topic, sections in topics.items():
                if sections:
                    f.write(f"**{topic}**:\n")
                    for section in sections:
                        f.write(f"- [{section.title}]({section.filename})\n")
                    f.write("\n")

            f.write("\n---\n\n")
            f.write("## Usage Notes\n\n")
            f.write("- Each section file is self-contained with metadata\n")
            f.write("- Files are numbered for sequential reading\n")
            f.write("- Cross-references between sections maintained\n")
            f.write("- AI agents can load specific sections as needed\n")
            f.write("- Human readers can jump to relevant topics quickly\n")

        print(f"✓ Created: 00_INDEX.md (manifest file)")

    def write_reassembly_script(self) -> None:
        """Create a script to reassemble the sharded files back into one document."""
        reassembly_script = self.output_dir.parent / "reassemble_findings.py"

        with open(reassembly_script, 'w', encoding='utf-8') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('"""\n')
            f.write('FINDINGS.md Reassembly Script\n\n')
            f.write('Reassembles sharded FINDINGS sections back into single document.\n')
            f.write('Use this after updating individual section files.\n')
            f.write('"""\n\n')
            f.write('from pathlib import Path\n')
            f.write('import re\n\n')
            f.write('def reassemble():\n')
            f.write('    sections_dir = Path("documentation_management/findings_sections")\n')
            f.write('    output_file = Path("FINDINGS.md")\n')
            f.write('    \n')
            f.write('    # Read index to get file order\n')
            f.write('    section_files = sorted(sections_dir.glob("[0-9]*.md"))\n')
            f.write('    \n')
            f.write('    with open(output_file, "w", encoding="utf-8") as out:\n')
            f.write('        # Write original metadata from index\n')
            f.write('        index_file = sections_dir / "00_INDEX.md"\n')
            f.write('        with open(index_file) as idx:\n')
            f.write('            in_metadata = False\n')
            f.write('            for line in idx:\n')
            f.write('                if "## Original Document Metadata" in line:\n')
            f.write('                    in_metadata = True\n')
            f.write('                    continue\n')
            f.write('                if in_metadata and line.strip() == "---":\n')
            f.write('                    break\n')
            f.write('                if in_metadata:\n')
            f.write('                    out.write(line)\n')
            f.write('        \n')
            f.write('        # Write each section (skip extraction metadata)\n')
            f.write('        for section_file in section_files:\n')
            f.write('            with open(section_file) as f:\n')
            f.write('                skip_metadata = True\n')
            f.write('                for line in f:\n')
            f.write('                    if skip_metadata and line.strip() == "---":\n')
            f.write('                        skip_metadata = False\n')
            f.write('                        next(f)  # Skip blank line after separator\n')
            f.write('                        continue\n')
            f.write('                    if not skip_metadata:\n')
            f.write('                        out.write(line)\n')
            f.write('            out.write("\\n")  # Add spacing between sections\n')
            f.write('    \n')
            f.write('    print(f"✓ Reassembled: {output_file}")\n\n')
            f.write('if __name__ == "__main__":\n')
            f.write('    reassemble()\n')

        reassembly_script.chmod(0o755)
        print(f"✓ Created: {reassembly_script.name} (reassembly script)")

    def execute(self) -> None:
        """Execute the complete sharding process."""
        print(f"\n{'='*60}")
        print(f"FINDINGS.md Document Sharding Tool")
        print(f"{'='*60}\n")

        print(f"Input file: {self.input_file}")
        print(f"Output directory: {self.output_dir}\n")

        print("Step 1: Parsing document structure...")
        self.parse_document()
        print(f"✓ Found {len(self.sections)} major sections\n")

        print("Step 2: Writing section files...")
        self.write_sections()
        print()

        print("Step 3: Generating manifest...")
        self.write_manifest()
        print()

        print("Step 4: Creating reassembly script...")
        self.write_reassembly_script()
        print()

        print(f"{'='*60}")
        print(f"Sharding complete!")
        print(f"{'='*60}\n")

        print(f"Total files created: {len(self.sections) + 2}")
        print(f"  - {len(self.sections)} section files")
        print(f"  - 1 index file (00_INDEX.md)")
        print(f"  - 1 reassembly script (reassemble_findings.py)")
        print()
        print(f"Next steps:")
        print(f"  1. Review section files in: {self.output_dir}")
        print(f"  2. Check index at: {self.output_dir / '00_INDEX.md'}")
        print(f"  3. To reassemble: python reassemble_findings.py")


def main():
    """Main execution function."""
    # Define paths
    project_root = Path(__file__).parent.parent
    input_file = project_root / "FINDINGS.md"
    output_dir = project_root / "documentation_management" / "findings_sections"

    # Validate input file exists
    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}")
        return 1

    # Execute sharding
    sharding_tool = FindingsShardingTool(input_file, output_dir)
    sharding_tool.execute()

    return 0


if __name__ == "__main__":
    exit(main())
