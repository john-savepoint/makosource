#!/usr/bin/env python3
"""
Auto-Scraper with Watchdog - Automatically restarts if stuck.

This script:
1. Scrapes all configured boards
2. Detects when no new content is being added (stuck)
3. Automatically moves to next board or restarts
4. Handles the SMF "overflow page" issue

Usage:
    python3 auto_scrape.py

Created: 2025-12-30 00:58:00 JST
Session-ID: 5e062ad5-f6c1-44e8-bbd7-332d37b1a441
"""

import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)


class AutoScraper:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.config = self._load_config()
        self.db_path = self.script_dir / "../database/qhimm.db"
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
        self.last_topic_ids = set()  # Track to detect duplicates/stuck

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

    def fetch(self, url, retries=3):
        """Fetch URL using subprocess for guaranteed timeout."""
        import subprocess
        import json

        fetch_script = f'''
import requests
import json
import sys
try:
    resp = requests.get("{url}", headers={{"User-Agent": "QHIMM-Archiver/1.0", "Connection": "close"}}, timeout=(5, 15))
    print(json.dumps({{"status": resp.status_code, "text": resp.text}}))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
'''
        for attempt in range(retries):
            try:
                result = subprocess.run(
                    ["python3", "-c", fetch_script],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0 and result.stdout.strip():
                    data = json.loads(result.stdout.strip())
                    if "error" in data:
                        print(f"    ⚠️ Fetch error (attempt {attempt+1}/{retries}): {data['error']}")
                    elif data.get("status") == 200:
                        return BeautifulSoup(data["text"], "html.parser")
                    else:
                        print(f"    ⚠️ HTTP {data.get('status')} (attempt {attempt+1}/{retries})")
                else:
                    print(f"    ⚠️ No output (attempt {attempt+1}/{retries})")
            except subprocess.TimeoutExpired:
                print(f"    ⚠️ Hard timeout 30s (attempt {attempt+1}/{retries})", flush=True)
            except Exception as e:
                print(f"    ⚠️ Error (attempt {attempt+1}/{retries}): {e}", flush=True)
            if attempt < retries - 1:
                time.sleep(2)
        return None

    def get_topic_count(self, board_id):
        """Get current topic count for a board."""
        cur = self.conn.execute(
            "SELECT COUNT(*) FROM topics WHERE board_id = ?", (board_id,))
        return cur.fetchone()[0]

    def scrape_board(self, board_id, board_name):
        """Scrape all topics from a board with stuck detection."""
        print(f"\n{'='*60}")
        print(f"📋 Board {board_id}: {board_name}")
        print(f"{'='*60}")

        offset = 0
        page = 1
        consecutive_duplicates = 0
        consecutive_zero_new = 0  # Track consecutive pages with 0 new topics
        max_duplicates = 3  # Stop after 3 pages of all duplicates
        max_zero_new = 5  # Stop after 5 consecutive pages with 0 new topics (already scraped)

        while True:
            url = f"{self.config['base_url']}?board={board_id}.{offset}"
            print(f"  [Page {page}] offset={offset}")

            soup = self.fetch(url)
            if not soup:
                print("    Failed to fetch, skipping board")
                break

            # Extract topics
            new_count = 0
            page_topic_ids = set()

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
                page_topic_ids.add(topic_id)

                # Check if we already have this topic
                cur = self.conn.execute(
                    "SELECT 1 FROM topics WHERE topic_id = ?", (topic_id,))
                if cur.fetchone():
                    continue  # Already have it

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

                # Insert
                self.conn.execute("""
                    INSERT INTO topics
                    (topic_id, board_id, title, author, replies, views, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (topic_id, board_id, title, author, replies, views,
                      datetime.now().isoformat()))
                new_count += 1

            self.conn.commit()

            # Check for stuck condition (same topics as last page)
            if page_topic_ids == self.last_topic_ids:
                consecutive_duplicates += 1
                print(f"    ⚠️ Same topics as previous page ({consecutive_duplicates}/{max_duplicates})")
                if consecutive_duplicates >= max_duplicates:
                    print(f"    ✅ Board complete (detected overflow)")
                    break
            else:
                consecutive_duplicates = 0

            self.last_topic_ids = page_topic_ids

            if new_count == 0 and len(page_topic_ids) == 0:
                print(f"    ✅ No topics found, board complete")
                break

            # Check for consecutive pages with 0 new topics (board already fully scraped)
            if new_count == 0 and len(page_topic_ids) > 0:
                consecutive_zero_new += 1
                print(f"    +0 new topics (all {len(page_topic_ids)} already in DB, {consecutive_zero_new}/{max_zero_new})")
                if consecutive_zero_new >= max_zero_new:
                    print(f"    ✅ Board fully scraped (no new topics for {max_zero_new} pages)")
                    break
            else:
                consecutive_zero_new = 0
                print(f"    +{new_count} new topics")

            offset += 20
            page += 1
            time.sleep(0.5)  # Reduced from 2s for faster scraping

            # Safety limit
            if page > 200:
                print(f"    ⚠️ Safety limit reached")
                break

        total = self.get_topic_count(board_id)
        print(f"  📊 Total topics for board {board_id}: {total}")

    def scrape_posts_for_board(self, board_id):
        """Scrape posts for topics that don't have any."""
        cur = self.conn.execute("""
            SELECT t.topic_id, t.title
            FROM topics t
            LEFT JOIN posts p ON t.topic_id = p.topic_id
            WHERE t.board_id = ? AND p.post_id IS NULL
        """, (board_id,))
        missing = cur.fetchall()

        if not missing:
            print(f"  ✅ All topics have posts")
            return

        print(f"  📝 Scraping posts for {len(missing)} topics...")

        for i, (tid, title) in enumerate(missing, 1):
            print(f"    [{i}/{len(missing)}] {title[:40]}...")
            self.scrape_topic_posts(tid, board_id)
            time.sleep(0.5)  # Reduced from 2s

    def scrape_topic_posts(self, topic_id, board_id):
        """Scrape all posts from a topic."""
        offset = 0
        post_num = 1

        while True:
            url = f"{self.config['base_url']}?topic={topic_id}.{offset}"
            soup = self.fetch(url)
            if not soup:
                break

            found = 0
            for wrapper in soup.select("div.post_wrapper"):
                post_id = None
                link = wrapper.select_one("a[href*='msg']")
                if link:
                    m = re.search(r'msg(\d+)', link.get("href", ""))
                    if m:
                        post_id = m.group(1)
                if not post_id:
                    post_id = f"{topic_id}_{post_num}"

                author = ""
                author_elem = wrapper.select_one("div.poster h4 a")
                if author_elem:
                    author = author_elem.get_text(strip=True)

                date = ""
                date_elem = wrapper.select_one("div.smalltext")
                if date_elem:
                    date = date_elem.get_text(strip=True)

                content_elem = wrapper.select_one("div.post div.inner")
                if not content_elem:
                    continue

                self.conn.execute("""
                    INSERT OR IGNORE INTO posts
                    (post_id, topic_id, board_id, author, date, content_html,
                     content_text, post_number, has_attachments, attachment_urls, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, '[]', ?)
                """, (post_id, topic_id, board_id, author, date,
                      str(content_elem), content_elem.get_text(separator="\n", strip=True),
                      post_num, datetime.now().isoformat()))

                post_num += 1
                found += 1

            self.conn.commit()

            if found == 0:
                break
            if not soup.select_one("a.navPages"):
                break

            offset += 20

        print(f"      {post_num - 1} posts")

    def run(self):
        """Run the full scrape."""
        print("=" * 60)
        print("QHIMM AUTO-SCRAPER")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 60)

        for board in self.config["boards"]:
            bid = board["id"]
            name = board["name"]

            # Scrape topics
            self.scrape_board(bid, name)

            # Scrape posts
            self.scrape_posts_for_board(bid)

        # Final stats
        print("\n" + "=" * 60)
        print("SCRAPE COMPLETE")
        print("=" * 60)

        cur = self.conn.execute("SELECT COUNT(*) FROM topics")
        print(f"Total topics: {cur.fetchone()[0]}")
        cur = self.conn.execute("SELECT COUNT(*) FROM posts")
        print(f"Total posts: {cur.fetchone()[0]}")

        self.conn.close()


if __name__ == "__main__":
    try:
        scraper = AutoScraper()
        scraper.run()
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
