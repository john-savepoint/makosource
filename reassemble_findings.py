#!/usr/bin/env python3
"""
FINDINGS.md Reassembly Script

Reassembles sharded FINDINGS sections back into single document.
Use this after updating individual section files.
"""

from pathlib import Path
import re

def reassemble():
    sections_dir = Path("documentation_management/findings_sections")
    output_file = Path("FINDINGS.md")
    
    # Read index to get file order
    section_files = sorted(sections_dir.glob("[0-9]*.md"))
    
    with open(output_file, "w", encoding="utf-8") as out:
        # Write original metadata from index
        index_file = sections_dir / "00_INDEX.md"
        with open(index_file) as idx:
            in_metadata = False
            metadata_started = False
            for line in idx:
                if "## Original Document Metadata" in line:
                    in_metadata = True
                    continue
                if in_metadata and not metadata_started and line.strip():
                    metadata_started = True
                if in_metadata and metadata_started and line.strip() == "---":
                    out.write(line)  # Write the final separator
                    break
                if in_metadata and metadata_started:
                    out.write(line)
        
        # Write each section (skip extraction metadata)
        for section_file in section_files:
            with open(section_file) as f:
                skip_metadata = True
                for line in f:
                    if skip_metadata and line.strip() == "---":
                        skip_metadata = False
                        next(f)  # Skip blank line after separator
                        continue
                    if not skip_metadata:
                        out.write(line)
            out.write("\n")  # Add spacing between sections
    
    print(f"✓ Reassembled: {output_file}")

if __name__ == "__main__":
    reassemble()
