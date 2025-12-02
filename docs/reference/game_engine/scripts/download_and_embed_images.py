#!/usr/bin/env python3
"""
Download images from Fandom wiki and embed in markdown files

Created: 2025-11-28 14:40:49 JST (Friday)
Context: Downloads all referenced images and converts MediaWiki image syntax to Markdown.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import re
import os
import time
import urllib.request
import urllib.error
from pathlib import Path


def extract_image_references(content):
    """
    Extract all [[File:...]] references from content.

    Returns list of (full_match, filename) tuples.
    """
    # Pattern: [[File:filename.ext|...]] or [[File:filename.ext]]
    pattern = r'\[\[File:([^\]|]+?)(?:\|[^\]]+)?\]\]'
    matches = re.findall(pattern, content)
    return matches


def download_image(filename, output_dir):
    """
    Download image from Fandom wiki.

    URL format: https://qhimm-modding.fandom.com/wiki/Special:FilePath/{filename}
    """
    # Clean filename (remove spaces, special chars)
    url = f"https://qhimm-modding.fandom.com/wiki/Special:FilePath/{filename.replace(' ', '_')}"

    output_path = output_dir / filename

    if output_path.exists():
        print(f"  ⏭️  Already exists: {filename}")
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

            print(f"  ✅ Downloaded: {filename} ({len(image_data)} bytes)")
            return True

    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP Error {e.code} for {filename}")
        return False
    except Exception as e:
        print(f"  ❌ Error downloading {filename}: {str(e)}")
        return False


def replace_image_syntax(content, images_dir_name='images'):
    """
    Replace MediaWiki image syntax with Markdown syntax.

    [[File:image.png]] → ![](images/image.png)
    [[File:image.png|alt text|thumb]] → ![alt text](images/image.png)
    """

    def replacer(match):
        full_match = match.group(0)
        filename = match.group(1)

        # Extract alt text if present (look for descriptive text in the syntax)
        alt_text = ""
        if '|' in full_match:
            # Try to extract meaningful alt text (usually before |thumb or |alt=)
            parts = full_match.split('|')
            for part in parts[1:]:
                part = part.strip()
                if part and part not in ['thumb', 'alt=', 'link=', 'left', 'right', 'center']:
                    if not part.startswith('link=') and not part.startswith('alt='):
                        alt_text = part.replace(']]', '').strip()
                        break

        # Use filename without extension as fallback alt text
        if not alt_text:
            alt_text = filename.rsplit('.', 1)[0].replace('_', ' ')

        # Create markdown image reference
        markdown_image = f'![{alt_text}]({images_dir_name}/{filename})'

        return markdown_image

    # Replace all [[File:...]] patterns
    pattern = r'\[\[File:([^\]|]+?)(?:\|[^\]]+)?\]\]'
    updated_content = re.sub(pattern, replacer, content)

    return updated_content


def process_file(filepath, images_dir):
    """Process a single markdown file"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract image references
    image_filenames = extract_image_references(content)

    if not image_filenames:
        return 0, 0

    print(f"\n{filepath.name}:")
    print(f"  Found {len(image_filenames)} image(s)")

    # Download each image
    downloaded = 0
    for filename in image_filenames:
        if download_image(filename, images_dir):
            downloaded += 1
        time.sleep(0.5)  # Rate limiting

    # Replace syntax
    original_content = content
    updated_content = replace_image_syntax(content)

    if original_content != updated_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"  ✅ Updated markdown syntax")

    return len(image_filenames), downloaded


def main():
    """Main execution"""

    print("=" * 70)
    print("Download and Embed Images from Fandom Wiki")
    print("=" * 70)

    # Setup directories
    base_dir = Path(__file__).parent
    images_dir = base_dir / 'images'
    images_dir.mkdir(exist_ok=True)

    print(f"\nImages will be saved to: {images_dir}")
    print()

    # Process all markdown files
    markdown_dir = base_dir / 'markdown'
    total_images = 0
    total_downloaded = 0
    files_with_images = 0

    for filepath in sorted(markdown_dir.glob('*.md')):
        if filepath.name.lower() == 'readme.md':
            continue

        found, downloaded = process_file(filepath, images_dir)
        if found > 0:
            files_with_images += 1
            total_images += found
            total_downloaded += downloaded

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"Files with images: {files_with_images}")
    print(f"Total images found: {total_images}")
    print(f"Successfully downloaded: {total_downloaded}")
    print(f"Failed: {total_images - total_downloaded}")
    print()
    print(f"Images saved to: {images_dir}")
    print()


if __name__ == '__main__':
    main()
