#!/usr/bin/env python3
"""
Robust QHIMM Scraper - Handles hangs gracefully.

This version:
- Uses individual requests (no session pooling)
- Short timeouts with retries
- Can be run multiple times to fill gaps
- Skips already-scraped content

Usage:
    python3 robust_scrape.py              # Scrape all boards
    python3 robust_scrape.py --board 37   # Scrape specific board

Created: 2025-12-29 23:55:00 JST
"""

import argparse
import re
import sqlite3
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup


class RobustScraper:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.config = self._load_config()
        self.db_path = self.script_dir / "../database/qhimm.db"
        self.raw_dir = self.script_dir / "../raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _load_config(self):
        with open(self.script_dir / "config.yaml") as f:
            return yaml.safe_load(f)

    def _init_db(self):
        self.conn.executescript("""
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
                scraped_at TEXT
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
                scraped_at TEXT
            );
        """)
        self.conn.commit()

    def fetch(self, url, timeout=15):
        """Fetch URL with fresh connection each time."""
        headers = {
            "User-Agent": "QHIMM-Archiver/1.0",
            "Connection": "close",
        }
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            print(f"    ⚠️ Fetch failed: {e}")
            return None

    def scrape_board_topics(self, board_id):
        """Scrape all topics from a board."""
        base_url = self.config["base_url"]
        offset = 0
        page = 1
        new_topics = 0

        print(f"\n📋 Scraping board {board_id}")

        while True:
            url = f"{base_url}?board={board_id}.{offset}"
            print(f"  [Page {page}] {url}")

            soup = self.fetch(url)
            if not soup:
                print(f"    Failed to fetch page, stopping")
                break

            # Extract topics
            found = 0
            for row in soup.select("table.table_grid tbody tr"):
                subject = row.select_one("td.subject")
                if not subject:
                    continue

                link = subject.select_one("span[id^='msg_'] a[href*='topic=']")
                if not link:
                    link = subject.select_one("a[href*='topic=']")
                if not link:
                    continue

                href = link.get("href", "")
                match = re.search(r'topic=(\d+)', href)
                if not match:
                    continue

                topic_id = match.group(1)
                title = link.get_text(strip=True)

                # Author
                author = ""
                p = subject.select_one("p")
                if p:
                    a = p.select_one("a[href*='profile']")
                    if a:
                        author = a.get_text(strip=True)

                # Stats
                stats = row.select_one("td.stats")
                replies, views = 0, 0
                if stats:
                    text = stats.get_text(separator="|")
                    for part in text.split("|"):
                        if "Repl" in part:
                            replies = int(re.sub(r'\D', '', part) or 0)
                        elif "View" in part:
                            views = int(re.sub(r'\D', '', part) or 0)

                # Last post date
                lastpost = row.select_one("td.lastpost")
                last_date = ""
                if lastpost:
                    for line in lastpost.get_text().split("\n"):
                        if re.match(r'\d{4}-\d{2}-\d{2}', line.strip()):
                            last_date = line.strip()
                            break

                # Sticky
                is_sticky = "stickybg" in " ".join(row.get("class", []))

                # Insert/update
                self.conn.execute("""
                    INSERT OR REPLACE INTO topics
                    (topic_id, board_id, title, author, replies, views,
                     last_post_date, is_sticky, is_locked, url, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                """, (topic_id, board_id, title, author, replies, views,
                      last_date, 1 if is_sticky else 0, href, datetime.now().isoformat()))

                found += 1
                new_topics += 1

            self.conn.commit()

            if found == 0:
                print(f"    No topics found, stopping")
                break

            print(f"    Found {found} topics")

            # Check for more pages
            if not soup.select_one("a.navPages"):
                break

            offset += 20
            page += 1
            time.sleep(2)

        print(f"  ✅ Total new/updated: {new_topics}")
        return new_topics

    def scrape_missing_posts(self, board_id=None):
        """Scrape posts for topics that don't have any."""
        where = f"AND t.board_id = {board_id}" if board_id else ""
        cur = self.conn.execute(f"""
            SELECT t.topic_id, t.board_id, t.title
            FROM topics t
            LEFT JOIN posts p ON t.topic_id = p.topic_id
            WHERE p.post_id IS NULL {where}
        """)
        missing = cur.fetchall()

        if not missing:
            print("✅ All topics have posts")
            return

        print(f"\n📝 Scraping posts for {len(missing)} topics")

        for i, (tid, bid, title) in enumerate(missing, 1):
            print(f"\n  [{i}/{len(missing)}] {title[:50]}...")
            self.scrape_topic_posts(tid, bid)
            time.sleep(2)

    def scrape_topic_posts(self, topic_id, board_id):
        """Scrape all posts from a topic."""
        base_url = self.config["base_url"]
        offset = 0
        post_num = 1

        while True:
            url = f"{base_url}?topic={topic_id}.{offset}"
            soup = self.fetch(url)
            if not soup:
                break

            found = 0
            for wrapper in soup.select("div.post_wrapper"):
                # Post ID
                post_id = None
                link = wrapper.select_one("a[href*='msg']")
                if link:
                    m = re.search(r'msg(\d+)', link.get("href", ""))
                    if m:
                        post_id = m.group(1)
                if not post_id:
                    post_id = f"{topic_id}_{post_num}"

                # Author
                author = ""
                author_elem = wrapper.select_one("div.poster h4 a")
                if author_elem:
                    author = author_elem.get_text(strip=True)

                # Date
                date = ""
                date_elem = wrapper.select_one("div.smalltext")
                if date_elem:
                    date = date_elem.get_text(strip=True)

                # Content
                content_elem = wrapper.select_one("div.post div.inner")
                if not content_elem:
                    continue

                content_html = str(content_elem)
                content_text = content_elem.get_text(separator="\n", strip=True)

                self.conn.execute("""
                    INSERT OR REPLACE INTO posts
                    (post_id, topic_id, board_id, author, date, content_html,
                     content_text, post_number, has_attachments, attachment_urls, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, '[]', ?)
                """, (post_id, topic_id, board_id, author, date, content_html,
                      content_text, post_num, datetime.now().isoformat()))

                post_num += 1
                found += 1

            self.conn.commit()

            if found == 0:
                break

            # Check for more pages
            if not soup.select_one("a.navPages"):
                break

            offset += 20

        print(f"    ✅ {post_num - 1} posts")

    def run_all(self):
        """Scrape all configured boards."""
        for board in self.config["boards"]:
            self.scrape_board_topics(board["id"])
        self.scrape_missing_posts()

    def close(self):
        self.conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board", type=int, help="Specific board to scrape")
    parser.add_argument("--posts-only", action="store_true", help="Only scrape missing posts")
    args = parser.parse_args()

    print("=" * 60)
    print("ROBUST QHIMM SCRAPER")
    print("=" * 60)

    scraper = RobustScraper()

    try:
        if args.posts_only:
            scraper.scrape_missing_posts(args.board)
        elif args.board:
            scraper.scrape_board_topics(args.board)
            scraper.scrape_missing_posts(args.board)
        else:
            scraper.run_all()
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted")
    finally:
        scraper.close()

    print("\n✅ Done")


if __name__ == "__main__":
    main()
