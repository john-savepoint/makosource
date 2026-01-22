#!/usr/bin/env python3
"""
Resume QHIMM Scrape - Fills in missing posts and continues with remaining boards.

Created: 2025-12-29 23:45:00 JST
Session-ID: 5e062ad5-f6c1-44e8-bbd7-332d37b1a441

Usage:
    python3 resume_scrape.py
"""

import sqlite3
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from smf_scraper import QHIMMScraper

def main():
    print("=" * 60)
    print("QHIMM SCRAPE - RESUME MODE")
    print("=" * 60)

    scraper = QHIMMScraper()
    scraper.init_database()

    cursor = scraper.db_conn.cursor()

    # Step 1: Find topics missing posts
    print("\n📋 Step 1: Checking for topics missing posts...")
    cursor.execute('''
        SELECT t.topic_id, t.board_id, t.title
        FROM topics t
        LEFT JOIN posts p ON t.topic_id = p.topic_id
        WHERE p.post_id IS NULL
    ''')
    missing_topics = cursor.fetchall()

    if missing_topics:
        print(f"   Found {len(missing_topics)} topics missing posts")
        for topic_id, board_id, title in missing_topics:
            print(f"\n   Scraping: {title[:50]}...")
            try:
                scraper.scrape_topic_posts(topic_id, board_id)
                scraper._rate_limit()
            except Exception as e:
                print(f"   ⚠️ Error: {e}")
                continue
    else:
        print("   ✅ All existing topics have posts")

    # Step 2: Find boards not yet scraped
    print("\n📋 Step 2: Checking for boards not yet scraped...")
    cursor.execute('SELECT DISTINCT board_id FROM topics')
    scraped_boards = {row[0] for row in cursor.fetchall()}

    all_boards = [b["id"] for b in scraper.config["boards"]]
    remaining_boards = [b for b in all_boards if b not in scraped_boards]

    print(f"   Boards already scraped: {scraped_boards}")
    print(f"   Boards remaining: {remaining_boards}")

    # Step 3: Scrape remaining boards
    if remaining_boards:
        print(f"\n📋 Step 3: Scraping {len(remaining_boards)} remaining boards...")
        for board_id in remaining_boards:
            board_config = next(
                (b for b in scraper.config["boards"] if b["id"] == board_id),
                {"name": f"Board {board_id}"}
            )
            print(f"\n{'='*60}")
            print(f"Starting board: {board_config['name']} (ID: {board_id})")
            try:
                scraper.scrape_board_full(board_id)
            except Exception as e:
                print(f"⚠️ Error on board {board_id}: {e}")
                continue
    else:
        print("   ✅ All boards have been scraped")

    # Summary
    cursor.execute('SELECT COUNT(*) FROM topics')
    total_topics = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM posts')
    total_posts = cursor.fetchone()[0]

    print("\n" + "=" * 60)
    print("RESUME COMPLETE")
    print("=" * 60)
    print(f"Total topics: {total_topics}")
    print(f"Total posts: {total_posts}")

    scraper.close()

if __name__ == "__main__":
    main()
