#!/usr/bin/env python3
"""
QHIMM Forum Scraper - SMF 2.0 Compatible

Created: 2025-12-29 12:49:00 JST (Monday)
Author: John Zealand-Doyle
Session-ID: 5e062ad5-f6c1-44e8-bbd7-332d37b1a441

Purpose:
    Scrapes QHIMM forums (forums.qhimm.com) running SMF 2.0.18 to archive
    20+ years of FF7 modding knowledge. Handles pagination, rate limiting,
    and converts HTML to structured data for later processing.

Usage:
    python smf_scraper.py --board 65           # Scrape FF7 Audio board
    python smf_scraper.py --board 65 --limit 5 # Scrape first 5 topics only
    python smf_scraper.py --topic 12345        # Scrape specific topic
    python smf_scraper.py --all                # Scrape all configured boards

Dependencies:
    pip install requests beautifulsoup4 pyyaml
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, parse_qs, urlparse

import requests
import yaml
from bs4 import BeautifulSoup, NavigableString


@dataclass
class Post:
    """Represents a single forum post."""
    post_id: str
    topic_id: str
    board_id: int
    author: str
    author_id: Optional[str]
    date: str
    date_iso: Optional[str]
    content_html: str
    content_text: str
    post_number: int
    has_attachments: bool
    attachment_urls: list


@dataclass
class Topic:
    """Represents a forum topic/thread."""
    topic_id: str
    board_id: int
    title: str
    author: str
    replies: int
    views: int
    last_post_date: str
    is_sticky: bool
    is_locked: bool
    url: str


@dataclass
class Board:
    """Represents a forum board."""
    board_id: int
    name: str
    category: str
    priority: str
    topic_count: int
    post_count: int


class QHIMMScraper:
    """
    Scraper for QHIMM forums (SMF 2.0).

    Handles:
    - Board listing and pagination
    - Topic listing and pagination
    - Post content extraction
    - Rate limiting and retries
    - Raw HTML archiving
    - SQLite storage
    """

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize scraper with configuration."""
        self.config = self._load_config(config_path)
        self.base_url = self.config["base_url"]
        self.session = self._create_session()
        self.db_conn = None

        # Paths
        self.script_dir = Path(__file__).parent
        self.raw_dir = self.script_dir / self.config["output"]["raw_html_dir"]
        self.markdown_dir = self.script_dir / self.config["output"]["markdown_dir"]
        self.topics_dir = self.script_dir / self.config["output"]["topics_dir"]
        self.db_path = self.script_dir / self.config["output"]["database_path"]

        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        self.topics_dir.mkdir(parents=True, exist_ok=True)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Request counter for session reset
        self._request_count = 0
        self._reset_interval = 50  # Reset session every 50 requests

    def _load_config(self, config_path: str) -> dict:
        """Load YAML configuration file."""
        config_file = Path(__file__).parent / config_path
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _create_session(self) -> requests.Session:
        """Create a requests session with appropriate headers."""
        session = requests.Session()
        session.headers.update({
            "User-Agent": self.config["user_agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",  # Don't keep connections alive to avoid hangs
        })
        return session

    def _reset_session(self):
        """Reset the session to avoid connection issues."""
        self.session.close()
        self.session = self._create_session()

    def _rate_limit(self):
        """Apply rate limiting between requests."""
        time.sleep(self.config["rate_limit"]["delay_seconds"])

    def _fetch_page(self, url: str, retry_count: int = 0) -> Optional[BeautifulSoup]:
        """
        Fetch a page and return parsed BeautifulSoup object.

        Implements retry logic with exponential backoff.
        """
        max_retries = self.config["rate_limit"]["max_retries"]

        try:
            # Reset session periodically to avoid connection issues
            self._request_count += 1
            if self._request_count % self._reset_interval == 0:
                self._reset_session()

            # Use tuple timeout: (connect_timeout, read_timeout)
            response = self.session.get(
                url,
                timeout=(10, self.config["timeout"])
            )
            response.raise_for_status()

            # Check for access denied / login required
            if "You are not allowed to access this section" in response.text:
                print(f"  ⚠️  Access denied for: {url}")
                return None

            if "The topic or board you are looking for" in response.text:
                print(f"  ⚠️  Topic/board not found: {url}")
                return None

            return BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.RequestException as e:
            if retry_count < max_retries:
                retry_delay = self.config["rate_limit"]["retry_delay"] * (2 ** retry_count)
                print(f"  ⚠️  Request failed, retrying in {retry_delay}s: {e}")
                time.sleep(retry_delay)
                return self._fetch_page(url, retry_count + 1)
            else:
                print(f"  ❌ Failed after {max_retries} retries: {e}")
                return None

    def _save_raw_html(self, html: str, filename: str):
        """Save raw HTML to archive directory."""
        filepath = self.raw_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

    # ========== Database Methods ==========

    def init_database(self):
        """Initialize SQLite database with schema."""
        self.db_conn = sqlite3.connect(self.db_path)
        cursor = self.db_conn.cursor()

        # Create tables
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS boards (
                board_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                priority TEXT,
                topic_count INTEGER DEFAULT 0,
                post_count INTEGER DEFAULT 0,
                last_scraped TEXT
            );

            CREATE TABLE IF NOT EXISTS topics (
                topic_id TEXT PRIMARY KEY,
                board_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                author TEXT,
                replies INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                last_post_date TEXT,
                is_sticky INTEGER DEFAULT 0,
                is_locked INTEGER DEFAULT 0,
                url TEXT,
                scraped_at TEXT,
                FOREIGN KEY (board_id) REFERENCES boards(board_id)
            );

            CREATE TABLE IF NOT EXISTS posts (
                post_id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                board_id INTEGER NOT NULL,
                author TEXT,
                author_id TEXT,
                date TEXT,
                date_iso TEXT,
                content_html TEXT,
                content_text TEXT,
                post_number INTEGER,
                has_attachments INTEGER DEFAULT 0,
                attachment_urls TEXT,
                scraped_at TEXT,
                FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
                FOREIGN KEY (board_id) REFERENCES boards(board_id)
            );

            CREATE INDEX IF NOT EXISTS idx_posts_topic ON posts(topic_id);
            CREATE INDEX IF NOT EXISTS idx_topics_board ON topics(board_id);
            CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author);
        """)

        self.db_conn.commit()
        print("✅ Database initialized")

    def save_topic_to_db(self, topic: Topic):
        """Save topic metadata to database."""
        cursor = self.db_conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO topics
            (topic_id, board_id, title, author, replies, views, last_post_date,
             is_sticky, is_locked, url, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            topic.topic_id, topic.board_id, topic.title, topic.author,
            topic.replies, topic.views, topic.last_post_date,
            1 if topic.is_sticky else 0, 1 if topic.is_locked else 0,
            topic.url, datetime.now().isoformat()
        ))
        self.db_conn.commit()

    def save_post_to_db(self, post: Post):
        """Save post to database."""
        cursor = self.db_conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO posts
            (post_id, topic_id, board_id, author, author_id, date, date_iso,
             content_html, content_text, post_number, has_attachments,
             attachment_urls, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post.post_id, post.topic_id, post.board_id, post.author,
            post.author_id, post.date, post.date_iso, post.content_html,
            post.content_text, post.post_number,
            1 if post.has_attachments else 0,
            json.dumps(post.attachment_urls),
            datetime.now().isoformat()
        ))
        self.db_conn.commit()

    # ========== Board Scraping ==========

    def get_board_url(self, board_id: int, offset: int = 0) -> str:
        """Generate URL for a board page."""
        return f"{self.base_url}?board={board_id}.{offset}"

    def scrape_board_topics(self, board_id: int, limit: Optional[int] = None) -> list[Topic]:
        """
        Scrape all topics from a board.

        Args:
            board_id: SMF board ID
            limit: Optional limit on number of topics to scrape

        Returns:
            List of Topic objects
        """
        topics = []
        offset = 0
        topics_per_page = self.config["pagination"]["topics_per_page"]

        # Get board name from config
        board_config = next(
            (b for b in self.config["boards"] if b["id"] == board_id),
            {"name": f"Board {board_id}", "category": "unknown", "priority": "UNKNOWN"}
        )

        print(f"\n{'='*60}")
        print(f"📋 Scraping board: {board_config['name']} (ID: {board_id})")
        print(f"{'='*60}")

        page_num = 1
        while True:
            url = self.get_board_url(board_id, offset)
            print(f"\n[Page {page_num}] Fetching: {url}")

            soup = self._fetch_page(url)
            if not soup:
                break

            # Save raw HTML
            self._save_raw_html(
                str(soup),
                f"board_{board_id}_page_{page_num}.html"
            )

            # Find topic rows - SMF uses table structure
            page_topics = self._extract_topics_from_page(soup, board_id)

            if not page_topics:
                print(f"  No more topics found on page {page_num}")
                break

            for topic in page_topics:
                topics.append(topic)
                self.save_topic_to_db(topic)
                print(f"  ✅ {topic.title[:50]}... ({topic.replies} replies, {topic.views} views)")

                if limit and len(topics) >= limit:
                    print(f"\n⏹️  Reached limit of {limit} topics")
                    return topics

            # Check if there are more pages
            if not self._has_next_page(soup):
                print(f"\n✅ Reached last page of board")
                break

            offset += topics_per_page
            page_num += 1
            self._rate_limit()

        print(f"\n📊 Total topics scraped from board {board_id}: {len(topics)}")
        return topics

    def _extract_topics_from_page(self, soup: BeautifulSoup, board_id: int) -> list[Topic]:
        """Extract topic metadata from a board page."""
        topics = []

        # SMF 2.0 topic list structure
        # Topics are in table rows within tbody
        # Each row has: td.icon1, td.icon2, td.subject, td.stats, td.lastpost
        topic_table = soup.select_one("table.table_grid")
        if not topic_table:
            return topics

        # Get all rows in tbody (skip thead)
        topic_rows = topic_table.select("tbody tr")

        for row in topic_rows:
            try:
                # Find the subject cell
                subject_td = row.select_one("td.subject")
                if not subject_td:
                    continue

                # Find the topic link (in span with id like msg_XXXXX)
                link = subject_td.select_one("span[id^='msg_'] a[href*='topic=']")
                if not link:
                    # Fallback to any topic link
                    link = subject_td.select_one("a[href*='topic=']")
                if not link:
                    continue

                href = link.get("href", "")

                # Extract topic ID from URL
                topic_match = re.search(r'topic=(\d+)', href)
                if not topic_match:
                    continue

                topic_id = topic_match.group(1)
                title = link.get_text(strip=True)

                # Check for sticky (row has stickybg class or icon)
                is_sticky = "stickybg" in row.get("class", []) or \
                           "stickybg" in (subject_td.get("class", []) or []) or \
                           bool(row.select_one("img[src*='sticky']"))
                is_locked = bool(row.select_one("img[src*='locked']"))

                # Get author from "Started by" paragraph
                author = ""
                started_p = subject_td.select_one("p")
                if started_p:
                    author_link = started_p.select_one("a[href*='profile']")
                    if author_link:
                        author = author_link.get_text(strip=True)

                # Get stats from td.stats (contains "X Replies<br/>Y Views")
                stats_td = row.select_one("td.stats")
                replies = 0
                views = 0

                if stats_td:
                    stats_text = stats_td.get_text(separator="|", strip=True)
                    # Format: "3 Replies|27264 Views" or similar
                    parts = stats_text.split("|")
                    for part in parts:
                        part = part.strip()
                        if "Repl" in part:
                            replies = self._parse_number(part.split()[0])
                        elif "View" in part:
                            views = self._parse_number(part.split()[0])

                # Get last post date
                lastpost_td = row.select_one("td.lastpost")
                last_post_date = ""
                if lastpost_td:
                    # Date is typically on its own line, format: 2025-12-09 02:46:42
                    text = lastpost_td.get_text(separator="\n", strip=True)
                    for line in text.split("\n"):
                        line = line.strip()
                        # Look for date pattern YYYY-MM-DD
                        if re.match(r'\d{4}-\d{2}-\d{2}', line):
                            last_post_date = line
                            break

                topic = Topic(
                    topic_id=topic_id,
                    board_id=board_id,
                    title=title,
                    author=author,
                    replies=replies,
                    views=views,
                    last_post_date=last_post_date,
                    is_sticky=is_sticky,
                    is_locked=is_locked,
                    url=href
                )
                topics.append(topic)

            except Exception as e:
                print(f"  ⚠️  Error parsing topic: {e}")
                continue

        return topics

    def _parse_number(self, text: str) -> int:
        """Parse a number from text, handling commas and K/M suffixes."""
        text = text.strip().replace(",", "").replace(" ", "")

        # Handle K suffix (thousands)
        if text.endswith("K"):
            return int(float(text[:-1]) * 1000)
        # Handle M suffix (millions)
        if text.endswith("M"):
            return int(float(text[:-1]) * 1000000)

        try:
            return int(text)
        except ValueError:
            return 0

    def _has_next_page(self, soup: BeautifulSoup) -> bool:
        """Check if there's a next page link."""
        # Look for "next" or "»" links in pagination
        page_links = soup.select("div.pagelinks a, span.pages a")
        for link in page_links:
            text = link.get_text(strip=True)
            if text in ["»", "Next", "next", ">"]:
                return True
            # Also check for numbered pages after current
            if link.get("href") and "start=" in link.get("href", ""):
                # There are more pages
                pass

        # Alternative: check if current page strong exists and there are links after
        current = soup.select_one("div.pagelinks strong, span.pages strong")
        if current:
            next_sibling = current.find_next_sibling("a")
            if next_sibling:
                return True

        return False

    # ========== Topic/Post Scraping ==========

    def get_topic_url(self, topic_id: str, offset: int = 0) -> str:
        """Generate URL for a topic page."""
        return f"{self.base_url}?topic={topic_id}.{offset}"

    def scrape_topic_posts(self, topic_id: str, board_id: int) -> list[Post]:
        """
        Scrape all posts from a topic.

        Args:
            topic_id: SMF topic ID
            board_id: Board ID for reference

        Returns:
            List of Post objects
        """
        posts = []
        offset = 0
        posts_per_page = self.config["pagination"]["posts_per_page"]
        post_number = 1

        page_num = 1
        while True:
            url = self.get_topic_url(topic_id, offset)

            if page_num == 1:
                print(f"\n  📄 Scraping topic {topic_id}...")

            soup = self._fetch_page(url)
            if not soup:
                break

            # Save raw HTML
            self._save_raw_html(
                str(soup),
                f"topic_{topic_id}_page_{page_num}.html"
            )

            # Get topic title on first page
            if page_num == 1:
                title_elem = soup.select_one("h1.display_title, div#forumposts h3")
                if title_elem:
                    print(f"     Title: {title_elem.get_text(strip=True)[:60]}...")

            # Extract posts
            page_posts = self._extract_posts_from_page(soup, topic_id, board_id, post_number)

            if not page_posts:
                if page_num == 1:
                    print(f"     ⚠️  No posts found in topic")
                break

            for post in page_posts:
                posts.append(post)
                self.save_post_to_db(post)

            post_number += len(page_posts)

            # Check for more pages
            if not self._has_next_page(soup):
                break

            offset += posts_per_page
            page_num += 1
            self._rate_limit()

        print(f"     ✅ Scraped {len(posts)} posts")
        return posts

    def _extract_posts_from_page(self, soup: BeautifulSoup, topic_id: str,
                                  board_id: int, start_number: int) -> list[Post]:
        """Extract posts from a topic page."""
        posts = []
        post_number = start_number

        # SMF 2.0 post structure
        post_wrappers = soup.select("div.post_wrapper")

        for wrapper in post_wrappers:
            try:
                # Get post ID from wrapper or link
                post_id = None
                post_link = wrapper.select_one("a[href*='msg']")
                if post_link:
                    msg_match = re.search(r'msg(\d+)', post_link.get("href", ""))
                    if msg_match:
                        post_id = msg_match.group(1)

                if not post_id:
                    # Try to get from id attribute
                    wrapper_id = wrapper.get("id", "")
                    id_match = re.search(r'(\d+)', wrapper_id)
                    post_id = id_match.group(1) if id_match else str(post_number)

                # Author
                author = ""
                author_id = None
                author_elem = wrapper.select_one("div.poster h4 a, div.poster_info h4 a")
                if author_elem:
                    author = author_elem.get_text(strip=True)
                    href = author_elem.get("href", "")
                    uid_match = re.search(r'u=(\d+)', href)
                    if uid_match:
                        author_id = uid_match.group(1)

                # Date
                date_text = ""
                date_iso = None
                date_elem = wrapper.select_one("div.smalltext, div.postarea div.keyinfo div.smalltext")
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    # Try to extract just the date portion
                    date_text = re.sub(r'^(Reply|Topic).*?»\s*', '', date_text)
                    date_text = date_text.strip()

                # Content
                content_elem = wrapper.select_one("div.post div.inner, div.postarea div.post")
                if not content_elem:
                    continue

                content_html = str(content_elem)
                content_text = content_elem.get_text(separator="\n", strip=True)

                # Attachments
                attachments = []
                has_attachments = False
                attach_elems = wrapper.select("div.attachments a, a.bbc_link[href*='attach']")
                for att in attach_elems:
                    href = att.get("href", "")
                    if "attach" in href:
                        attachments.append(href)
                        has_attachments = True

                post = Post(
                    post_id=post_id,
                    topic_id=topic_id,
                    board_id=board_id,
                    author=author,
                    author_id=author_id,
                    date=date_text,
                    date_iso=date_iso,
                    content_html=content_html,
                    content_text=content_text,
                    post_number=post_number,
                    has_attachments=has_attachments,
                    attachment_urls=attachments
                )
                posts.append(post)
                post_number += 1

            except Exception as e:
                print(f"     ⚠️  Error parsing post: {e}")
                continue

        return posts

    # ========== High-Level Operations ==========

    def scrape_board_full(self, board_id: int, limit: Optional[int] = None):
        """
        Scrape a complete board: topics and all their posts.

        Args:
            board_id: SMF board ID
            limit: Optional limit on number of topics
        """
        # First get all topics
        topics = self.scrape_board_topics(board_id, limit)

        if not topics:
            print(f"No topics found for board {board_id}")
            return

        # Then scrape posts for each topic
        print(f"\n{'='*60}")
        print(f"📝 Scraping posts for {len(topics)} topics...")
        print(f"{'='*60}")

        total_posts = 0
        for i, topic in enumerate(topics, 1):
            print(f"\n[{i}/{len(topics)}] Topic: {topic.title[:50]}...")
            posts = self.scrape_topic_posts(topic.topic_id, board_id)
            total_posts += len(posts)
            self._rate_limit()

        print(f"\n{'='*60}")
        print(f"✅ COMPLETE")
        print(f"   Topics scraped: {len(topics)}")
        print(f"   Posts scraped: {total_posts}")
        print(f"   Raw HTML saved to: {self.raw_dir}")
        print(f"   Database: {self.db_path}")
        print(f"{'='*60}")

    def close(self):
        """Clean up resources."""
        if self.db_conn:
            self.db_conn.close()
        self.session.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="QHIMM Forum Scraper - Archive FF7 modding knowledge"
    )
    parser.add_argument(
        "--board", type=int,
        help="Board ID to scrape (e.g., 65 for FF7 Audio)"
    )
    parser.add_argument(
        "--topic", type=str,
        help="Specific topic ID to scrape"
    )
    parser.add_argument(
        "--limit", type=int,
        help="Limit number of topics to scrape"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Scrape all configured boards"
    )
    parser.add_argument(
        "--topics-only", action="store_true",
        help="Only scrape topic metadata, not post contents"
    )

    args = parser.parse_args()

    print("="*60)
    print("QHIMM Forum Scraper")
    print("="*60)
    print(f"Started: {datetime.now().isoformat()}")
    print()

    scraper = QHIMMScraper()
    scraper.init_database()

    try:
        if args.topic:
            # Scrape single topic
            board_id = args.board or 0
            scraper.scrape_topic_posts(args.topic, board_id)

        elif args.board:
            # Scrape single board
            if args.topics_only:
                scraper.scrape_board_topics(args.board, args.limit)
            else:
                scraper.scrape_board_full(args.board, args.limit)

        elif args.all:
            # Scrape all configured boards
            for board in scraper.config["boards"]:
                if args.topics_only:
                    scraper.scrape_board_topics(board["id"], args.limit)
                else:
                    scraper.scrape_board_full(board["id"], args.limit)
        else:
            print("Please specify --board, --topic, or --all")
            print("Example: python smf_scraper.py --board 65 --limit 5")
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Scraping interrupted by user")
    finally:
        scraper.close()

    print(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
