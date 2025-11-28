#!/usr/bin/env python3
"""
Extract images from raw MediaWiki and download them

Created: 2025-11-28 14:40:49 JST (Friday)
Context: Extracts image references from raw MediaWiki files, downloads them,
         and adds them to the corresponding markdown files.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
import os
import time
import urllib.request
import urllib.error
from pathlib import Path


def extract_images_from_mediawiki(filepath):
    """
    Extract image references from raw MediaWiki file.

    Returns: list of (filename, context) tuples
    context is the surrounding text to help locate where to insert
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: [[File:filename.ext|...]] or [[File:filename.ext]]
    pattern = r'\[\[File:([^\]|]+?)(?:\|[^\]]+)?\]\]'

    images = []
    for match in re.finditer(pattern, content):
        filename = match.group(1)
        # Get some context (20 chars before and after)
        start = max(0, match.start() - 20)
        end = min(len(content), match.end() + 20)
        context = content[start:end]

        images.append({
            'filename': filename,
            'full_match': match.group(0),
            'context': context,
            'position': match.start()
        })

    return images


def download_image(filename, output_dir):
    """Download image from Fandom wiki"""

    url = f"https://qhimm-modding.fandom.com/wiki/Special:FilePath/{filename.replace(' ', '_')}"
    output_path = output_dir / filename

    if output_path.exists():
        print(f"    ⏭️  Already exists: {filename}")
        return True

    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'FF7DocImageDownloader/1.0'}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            image_data = response.read()

            with open(output_path, 'wb') as f:
                f.write(image_data)

            print(f"    ✅ Downloaded: {filename} ({len(image_data)} bytes)")
            return True

    except urllib.error.HTTPError as e:
        print(f"    ❌ HTTP {e.code}: {filename}")
        return False
    except Exception as e:
        print(f"    ❌ Error: {filename} - {str(e)}")
        return False


def add_images_to_markdown(md_filepath, images, images_dir_name='images'):
    """
    Add image references to markdown file.

    Since we can't reliably match context, we'll add all images
    at the end of the file with a section header.
    """

    if not images:
        return False

    with open(md_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if images section already exists
    if '## Images' in content:
        print(f"    ⏭️  Images section already exists")
        return False

    # Add images section at the end
    images_section = "\n\n---\n\n## Images\n\n"

    for img in images:
        filename = img['filename']
        alt_text = filename.rsplit('.', 1)[0].replace('_', ' ')
        images_section += f"![{alt_text}]({images_dir_name}/{filename})\n\n"

    updated_content = content + images_section

    with open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    return True


def main():
    """Main execution"""

    print("=" * 70)
    print("Extract and Download Images from MediaWiki Files")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent
    raw_dir = base_dir / 'raw'
    markdown_dir = base_dir / 'markdown'
    images_dir = base_dir / 'images'

    images_dir.mkdir(exist_ok=True)

    total_files = 0
    total_images = 0
    total_downloaded = 0

    # Process each MediaWiki file
    for raw_file in sorted(raw_dir.glob('*.mediawiki')):
        # Find corresponding markdown file
        md_name = raw_file.stem + '.md'
        md_file = markdown_dir / md_name

        if not md_file.exists():
            continue

        # Extract images from raw file
        images = extract_images_from_mediawiki(raw_file)

        if not images:
            continue

        print(f"{raw_file.stem}:")
        print(f"  Found {len(images)} image(s)")

        total_files += 1
        total_images += len(images)

        # Download images
        downloaded = 0
        for img in images:
            if download_image(img['filename'], images_dir):
                downloaded += 1
            time.sleep(0.5)  # Rate limiting

        total_downloaded += downloaded

        # Add to markdown
        if add_images_to_markdown(md_file, images):
            print(f"  ✅ Added images section to markdown")

        print()

    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"Files with images: {total_files}")
    print(f"Total images found: {total_images}")
    print(f"Successfully downloaded: {total_downloaded}")
    print(f"Failed: {total_images - total_downloaded}")
    print()
    print(f"Images saved to: {images_dir}/")
    print()


if __name__ == '__main__':
    main()
