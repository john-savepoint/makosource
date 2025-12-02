#!/usr/bin/env python3
"""
FF7 Game Engine Documentation Scraper

Created: 2025-11-28 12:44:49 JST (Friday)
Context: Scrapes 32 pages from qhimm-modding Fandom wiki and converts from MediaWiki to Markdown.
         This script fetches raw MediaWiki content and prepends level 1 headings for proper hierarchy.

Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c
"""

import os
import re
import time
import urllib.request
import urllib.error
from pathlib import Path


def sanitize_filename(title):
    """
    Convert page title to valid filename.
    Replaces / with _, removes special characters, converts spaces to underscores.

    Examples:
        "FF7/WorldMap Module" -> "FF7_WorldMap_Module"
        "FF7/Battle/Battle Scenes/Battle Script" -> "FF7_Battle_Battle_Scenes_Battle_Script"
    """
    # Replace / with _
    sanitized = title.replace('/', '_')
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Remove or replace other special characters
    sanitized = re.sub(r'[^\w\-_]', '', sanitized)
    return sanitized


def parse_links_file(filepath):
    """
    Parse the pipe-separated links file.
    Returns list of tuples: [(url, page_title), ...]
    """
    pages = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue

            parts = line.split('|')
            if len(parts) >= 2:
                url = parts[0].strip()
                page_title = parts[1].strip()

                # Remove fragment identifiers from URLs (e.g., #PSX_DAT_Format)
                url = url.split('#')[0]

                pages.append((url, page_title))

    return pages


def fetch_mediawiki_raw(url):
    """
    Fetch raw MediaWiki content by appending ?action=raw to URL.
    Returns the raw content as string.
    """
    raw_url = f"{url}?action=raw"

    try:
        # Add user agent to be polite
        req = urllib.request.Request(
            raw_url,
            headers={'User-Agent': 'FF7DocScraper/1.0 (Educational purposes)'}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            return content

    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP Error {e.code}: {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"  ❌ URL Error: {e.reason}")
        return None
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return None


def save_mediawiki_file(content, page_title, output_dir):
    """
    Save MediaWiki content with prepended level 1 heading.

    Args:
        content: Raw MediaWiki content
        page_title: Original page title (e.g., "FF7/WorldMap Module")
        output_dir: Directory to save file (e.g., "raw/")

    Returns:
        Path to saved file or None if failed
    """
    if content is None:
        return None

    # Create level 1 heading in MediaWiki format
    heading = f"= {page_title} =\n\n"

    # Combine heading with content
    full_content = heading + content

    # Create filename
    filename = sanitize_filename(page_title) + '.mediawiki'
    filepath = os.path.join(output_dir, filename)

    # Write file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        return filepath
    except Exception as e:
        print(f"  ❌ Failed to write file: {str(e)}")
        return None


def main():
    """Main scraper execution"""

    # Setup paths
    base_dir = Path(__file__).parent
    links_file = base_dir / 'links to copy in order.txt'
    raw_dir = base_dir / 'raw'

    print("=" * 70)
    print("FF7 Game Engine Documentation Scraper")
    print("=" * 70)
    print()

    # Parse links file
    print(f"📖 Reading links from: {links_file}")
    pages = parse_links_file(links_file)
    print(f"✅ Found {len(pages)} pages to scrape\n")

    # Create output directory if needed
    raw_dir.mkdir(exist_ok=True)

    # Scrape each page
    success_count = 0
    failed_pages = []

    for i, (url, page_title) in enumerate(pages, 1):
        print(f"[{i}/{len(pages)}] {page_title}")
        print(f"  🌐 URL: {url}")

        # Fetch raw MediaWiki content
        content = fetch_mediawiki_raw(url)

        if content:
            # Save with prepended heading
            filepath = save_mediawiki_file(content, page_title, raw_dir)

            if filepath:
                print(f"  ✅ Saved: {os.path.basename(filepath)}")
                success_count += 1
            else:
                failed_pages.append((page_title, "Failed to save file"))
        else:
            failed_pages.append((page_title, "Failed to fetch content"))

        print()

        # Rate limiting: Wait 1.5 seconds between requests
        if i < len(pages):
            time.sleep(1.5)

    # Summary
    print("=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"✅ Successfully scraped: {success_count}/{len(pages)} pages")

    if failed_pages:
        print(f"❌ Failed pages: {len(failed_pages)}")
        for title, reason in failed_pages:
            print(f"  - {title}: {reason}")
    else:
        print("🎉 All pages scraped successfully!")

    print()


if __name__ == '__main__':
    main()
