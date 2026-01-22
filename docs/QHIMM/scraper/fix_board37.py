#!/usr/bin/env python3
"""
Fix Board 37 (7th Heaven) - Re-scrape to get all topics.

The original scrape used wrong pagination (50 instead of 20),
so we missed topics between pages.

This script re-scrapes all topic listings for board 37.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from smf_scraper import QHIMMScraper

def main():
    print("=" * 60)
    print("FIXING BOARD 37 (7th Heaven)")
    print("=" * 60)

    scraper = QHIMMScraper()
    scraper.init_database()

    # Re-scrape board 37 topics (will update existing, add missing)
    print("\nRe-scraping all topics from board 37...")
    topics = scraper.scrape_board_topics(37)

    print(f"\nTotal topics found: {len(topics)}")

    # Now find topics without posts
    cursor = scraper.db_conn.cursor()
    cursor.execute('''
        SELECT t.topic_id, t.board_id, t.title
        FROM topics t
        LEFT JOIN posts p ON t.topic_id = p.topic_id
        WHERE p.post_id IS NULL AND t.board_id = 37
    ''')
    missing = cursor.fetchall()

    print(f"Topics missing posts: {len(missing)}")

    if missing:
        print("\nScraping posts for missing topics...")
        for i, (tid, bid, title) in enumerate(missing, 1):
            print(f"\n[{i}/{len(missing)}] {title[:50]}...")
            try:
                scraper.scrape_topic_posts(tid, bid)
                scraper._rate_limit()
            except Exception as e:
                print(f"  Error: {e}")

    scraper.close()
    print("\n✅ Board 37 fix complete!")

if __name__ == "__main__":
    main()
