#!/usr/bin/env python3
"""
QHIMM Content Processor - HTML to Markdown Conversion

Created: 2025-12-29 12:50:00 JST (Monday)
Author: John Zealand-Doyle
Session-ID: 5e062ad5-f6c1-44e8-bbd7-332d37b1a441

Purpose:
    Converts scraped HTML post content to clean Markdown format.
    Handles SMF-specific formatting: quotes, code blocks, spoilers,
    embedded images, and BBCode remnants.

Usage:
    python content_processor.py                    # Process all posts in DB
    python content_processor.py --topic 12345     # Process specific topic
    python content_processor.py --export-markdown # Export to markdown files

Dependencies:
    pip install beautifulsoup4 markdownify
"""

import argparse
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, NavigableString
import markdownify


class ContentProcessor:
    """
    Processes HTML content from QHIMM forum posts into clean Markdown.

    Handles:
    - SMF quote blocks → Markdown blockquotes with attribution
    - Code blocks with syntax detection
    - Spoiler tags
    - Image references
    - BBCode cleanup
    - Link preservation
    """

    def __init__(self, db_path: str = "../database/qhimm.db"):
        """Initialize processor with database connection."""
        self.script_dir = Path(__file__).parent
        self.db_path = self.script_dir / db_path
        self.markdown_dir = self.script_dir / "../markdown"
        self.topics_dir = self.script_dir / "../topics"

        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        self.topics_dir.mkdir(parents=True, exist_ok=True)

        self.db_conn = sqlite3.connect(self.db_path)
        self.db_conn.row_factory = sqlite3.Row

    def html_to_markdown(self, html: str) -> str:
        """
        Convert HTML post content to Markdown.

        Handles SMF-specific elements before using markdownify.
        """
        soup = BeautifulSoup(html, "html.parser")

        # Pre-process SMF-specific elements
        self._process_quotes(soup)
        self._process_code_blocks(soup)
        self._process_spoilers(soup)
        self._process_images(soup)
        self._clean_bbcode_remnants(soup)

        # Convert to markdown using markdownify
        md = markdownify.markdownify(
            str(soup),
            heading_style="ATX",
            bullets="-",
            code_language="",
            strip=["script", "style"]
        )

        # Post-process markdown
        md = self._clean_markdown(md)

        return md

    def _process_quotes(self, soup: BeautifulSoup):
        """
        Convert SMF quote blocks to Markdown blockquotes.

        SMF format:
        <div class="quoteheader">Quote from: Author on Date</div>
        <blockquote class="bbc_standard_quote">Content</blockquote>

        Markdown format:
        > **Author wrote:**
        > Content
        """
        # Find quote headers
        quote_headers = soup.select("div.quoteheader, div.quote_header")

        for header in quote_headers:
            header_text = header.get_text(strip=True)

            # Extract author if present
            author_match = re.search(r'Quote from:\s*([^o][^\n]+?)(?:\s+on|\s*$)', header_text)
            author = author_match.group(1).strip() if author_match else "Quote"

            # Find associated blockquote
            blockquote = header.find_next_sibling("blockquote")
            if blockquote:
                # Create markdown-style quote
                quote_content = blockquote.get_text(separator="\n", strip=True)
                lines = quote_content.split("\n")
                quoted_lines = [f"> {line}" for line in lines]
                quoted_text = f"> **{author} wrote:**\n" + "\n".join(quoted_lines)

                # Replace with text node
                new_elem = soup.new_tag("p")
                new_elem.string = quoted_text
                header.replace_with(new_elem)
                blockquote.decompose()
            else:
                # Just the header, convert to attribution
                header.string = f"> **{author}:**"

    def _process_code_blocks(self, soup: BeautifulSoup):
        """
        Convert SMF code blocks to Markdown fenced code blocks.

        SMF format:
        <div class="codeheader">Code: [Select]</div>
        <code class="bbc_code">Content</code>

        Detects language hints for syntax highlighting.
        """
        # Common code block patterns in QHIMM
        language_hints = {
            r'\b(lua|LUA)\b': 'lua',
            r'\b(hext|HEXT)\b': 'text',  # HEXT patches
            r'^\s*0x[0-9A-Fa-f]+': 'text',  # Hex addresses
            r'\bfunction\s+\w+\s*\(': 'lua',
            r'#include|#define': 'c',
            r'\bdef\s+\w+\s*\(': 'python',
            r'^\s*\d+\s+[0-9A-Fa-f]{2}': 'text',  # Hex dumps
        }

        code_blocks = soup.select("code.bbc_code, pre.bbc_code, div.bbc_code")

        for code in code_blocks:
            content = code.get_text()

            # Detect language
            lang = ""
            for pattern, detected_lang in language_hints.items():
                if re.search(pattern, content, re.MULTILINE):
                    lang = detected_lang
                    break

            # Create fenced code block
            fence = f"```{lang}\n{content}\n```"

            # Replace with pre tag containing the fence
            new_pre = soup.new_tag("pre")
            new_pre.string = fence
            code.replace_with(new_pre)

        # Remove code headers
        for header in soup.select("div.codeheader, div.code_header"):
            header.decompose()

    def _process_spoilers(self, soup: BeautifulSoup):
        """
        Convert SMF spoiler tags to Markdown details blocks.

        SMF format:
        <div class="spoilerheader">Spoiler</div>
        <div class="spoiler">Content</div>

        Markdown format:
        <details>
        <summary>Spoiler</summary>
        Content
        </details>
        """
        spoiler_headers = soup.select("div.spoilerheader, div.spoiler_header")

        for header in spoiler_headers:
            header_text = header.get_text(strip=True) or "Spoiler"

            # Find spoiler content
            spoiler = header.find_next_sibling(class_=re.compile(r'spoiler'))
            if spoiler:
                content = spoiler.get_text(separator="\n", strip=True)

                # Create details element (HTML5, renders in most markdown viewers)
                details_text = f"\n<details>\n<summary>{header_text}</summary>\n\n{content}\n\n</details>\n"

                new_elem = soup.new_tag("div")
                new_elem.string = details_text
                header.replace_with(new_elem)
                spoiler.decompose()

    def _process_images(self, soup: BeautifulSoup):
        """
        Process image tags, preserving URLs for reference.

        Converts to Markdown image syntax: ![alt](url)
        """
        for img in soup.select("img"):
            src = img.get("src", "")
            alt = img.get("alt", "image")

            if not src:
                continue

            # Skip smileys and icons
            if any(x in src.lower() for x in ["smiley", "icon", "avatar"]):
                continue

            # Create markdown image
            md_img = f"![{alt}]({src})"
            img.replace_with(md_img)

    def _clean_bbcode_remnants(self, soup: BeautifulSoup):
        """
        Clean up any remaining BBCode that wasn't converted.

        Common patterns:
        [b]text[/b] → **text**
        [i]text[/i] → *text*
        [url=...]text[/url] → [text](url)
        [color=...]text[/color] → text (color stripped)
        """
        # Get text and process BBCode
        for text_node in soup.find_all(string=True):
            if not isinstance(text_node, NavigableString):
                continue

            text = str(text_node)
            original = text

            # Bold
            text = re.sub(r'\[b\](.*?)\[/b\]', r'**\1**', text, flags=re.IGNORECASE)

            # Italic
            text = re.sub(r'\[i\](.*?)\[/i\]', r'*\1*', text, flags=re.IGNORECASE)

            # Underline (no direct MD equivalent, use bold)
            text = re.sub(r'\[u\](.*?)\[/u\]', r'**\1**', text, flags=re.IGNORECASE)

            # Strike
            text = re.sub(r'\[s\](.*?)\[/s\]', r'~~\1~~', text, flags=re.IGNORECASE)

            # URLs
            text = re.sub(r'\[url=([^\]]+)\](.*?)\[/url\]', r'[\2](\1)', text, flags=re.IGNORECASE)
            text = re.sub(r'\[url\](.*?)\[/url\]', r'[\1](\1)', text, flags=re.IGNORECASE)

            # Color (strip)
            text = re.sub(r'\[color=[^\]]+\](.*?)\[/color\]', r'\1', text, flags=re.IGNORECASE)

            # Size (strip)
            text = re.sub(r'\[size=[^\]]+\](.*?)\[/size\]', r'\1', text, flags=re.IGNORECASE)

            # Lists
            text = re.sub(r'\[list\]', '', text, flags=re.IGNORECASE)
            text = re.sub(r'\[/list\]', '', text, flags=re.IGNORECASE)
            text = re.sub(r'\[\*\]', '- ', text)

            if text != original:
                text_node.replace_with(text)

    def _clean_markdown(self, md: str) -> str:
        """
        Post-process markdown for cleanliness.

        - Remove excessive blank lines
        - Fix spacing around code blocks
        - Normalize whitespace
        """
        # Remove excessive blank lines (more than 2)
        md = re.sub(r'\n{4,}', '\n\n\n', md)

        # Ensure code blocks have proper spacing
        md = re.sub(r'([^\n])\n```', r'\1\n\n```', md)
        md = re.sub(r'```\n([^\n])', r'```\n\n\1', md)

        # Remove trailing whitespace on lines
        md = '\n'.join(line.rstrip() for line in md.split('\n'))

        # Ensure file ends with single newline
        md = md.strip() + '\n'

        return md

    # ========== Database Operations ==========

    def process_all_posts(self):
        """Process all posts in database, updating content_markdown field."""
        cursor = self.db_conn.cursor()

        # Add markdown column if not exists
        cursor.execute("""
            SELECT COUNT(*) FROM pragma_table_info('posts')
            WHERE name='content_markdown'
        """)
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE posts ADD COLUMN content_markdown TEXT")
            self.db_conn.commit()

        # Get all posts
        cursor.execute("SELECT post_id, content_html FROM posts WHERE content_html IS NOT NULL")
        posts = cursor.fetchall()

        print(f"Processing {len(posts)} posts...")

        for i, post in enumerate(posts, 1):
            post_id = post["post_id"]
            html = post["content_html"]

            try:
                markdown = self.html_to_markdown(html)

                cursor.execute("""
                    UPDATE posts SET content_markdown = ? WHERE post_id = ?
                """, (markdown, post_id))

                if i % 100 == 0:
                    print(f"  Processed {i}/{len(posts)} posts...")
                    self.db_conn.commit()

            except Exception as e:
                print(f"  ⚠️  Error processing post {post_id}: {e}")

        self.db_conn.commit()
        print(f"✅ Processed {len(posts)} posts")

    def export_topic_markdown(self, topic_id: str) -> str:
        """
        Export a complete topic as a single Markdown file.

        Includes:
        - Topic metadata header
        - All posts in order
        - Author and date attribution
        """
        cursor = self.db_conn.cursor()

        # Get topic info
        cursor.execute("""
            SELECT * FROM topics WHERE topic_id = ?
        """, (topic_id,))
        topic = cursor.fetchone()

        if not topic:
            return f"Topic {topic_id} not found"

        # Get all posts
        cursor.execute("""
            SELECT * FROM posts
            WHERE topic_id = ?
            ORDER BY post_number
        """, (topic_id,))
        posts = cursor.fetchall()

        # Build markdown document
        lines = []

        # YAML frontmatter
        lines.append("---")
        lines.append(f"topic_id: {topic['topic_id']}")
        lines.append(f"board_id: {topic['board_id']}")
        safe_title = topic['title'].replace('"', "'")
        lines.append(f'title: "{safe_title}"')
        lines.append(f"author: \"{topic['author']}\"")
        lines.append(f"replies: {topic['replies']}")
        lines.append(f"views: {topic['views']}")
        lines.append(f"last_post: \"{topic['last_post_date']}\"")
        lines.append(f"url: \"https://forums.qhimm.com/index.php?topic={topic_id}.0\"")
        lines.append(f"scraped_at: \"{topic['scraped_at']}\"")
        lines.append("---")
        lines.append("")

        # Title
        lines.append(f"# {topic['title']}")
        lines.append("")
        lines.append(f"*Originally posted by **{topic['author']}** • {topic['views']} views • {topic['replies']} replies*")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Posts
        for post in posts:
            # Post header
            lines.append(f"## Post #{post['post_number']} by {post['author']}")
            lines.append(f"*{post['date']}*")
            lines.append("")

            # Post content
            content = post["content_markdown"] if post["content_markdown"] else post["content_text"]
            lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def export_all_topics(self):
        """Export all topics as individual Markdown files."""
        cursor = self.db_conn.cursor()

        cursor.execute("SELECT topic_id, title, board_id FROM topics")
        topics = cursor.fetchall()

        print(f"Exporting {len(topics)} topics...")

        for topic in topics:
            topic_id = topic["topic_id"]
            board_id = topic["board_id"]

            try:
                markdown = self.export_topic_markdown(topic_id)

                # Create board subdirectory
                board_dir = self.topics_dir / f"board_{board_id}"
                board_dir.mkdir(exist_ok=True)

                # Sanitize filename
                safe_title = re.sub(r'[^\w\s-]', '', topic["title"])[:50]
                safe_title = safe_title.strip().replace(' ', '_')
                filename = f"{topic_id}_{safe_title}.md"

                filepath = board_dir / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(markdown)

            except Exception as e:
                print(f"  ⚠️  Error exporting topic {topic_id}: {e}")

        print(f"✅ Exported to {self.topics_dir}")

    def close(self):
        """Close database connection."""
        self.db_conn.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Process QHIMM HTML content to Markdown"
    )
    parser.add_argument(
        "--process", action="store_true",
        help="Process all posts in database"
    )
    parser.add_argument(
        "--topic", type=str,
        help="Export specific topic to markdown"
    )
    parser.add_argument(
        "--export-all", action="store_true",
        help="Export all topics as markdown files"
    )
    parser.add_argument(
        "--test", type=str,
        help="Test conversion on a sample HTML string"
    )

    args = parser.parse_args()

    processor = ContentProcessor()

    try:
        if args.process:
            processor.process_all_posts()

        elif args.topic:
            md = processor.export_topic_markdown(args.topic)
            print(md)

        elif args.export_all:
            processor.process_all_posts()
            processor.export_all_topics()

        elif args.test:
            result = processor.html_to_markdown(args.test)
            print("Input HTML:")
            print(args.test)
            print("\nOutput Markdown:")
            print(result)

        else:
            parser.print_help()

    finally:
        processor.close()


if __name__ == "__main__":
    main()
