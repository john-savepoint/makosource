#!/bin/bash
# QHIMM Scrape Progress Monitor
# Run: ./monitor.sh (or bash monitor.sh)
# Created: 2025-12-29 23:24:00 JST

cd "$(dirname "$0")"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           QHIMM FORUM SCRAPE - PROGRESS MONITOR            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if scraper is running
if pgrep -f "smf_scraper" > /dev/null; then
    echo "🟢 STATUS: Scraper is RUNNING"
else
    echo "🔴 STATUS: Scraper is NOT RUNNING (finished or stopped)"
fi
echo ""

# Database stats
echo "📊 DATABASE STATS:"
python3 -c "
import sqlite3
from pathlib import Path
db = Path('database/qhimm.db')
if not db.exists():
    print('  Database not found!')
    exit()
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM topics')
topics = cur.fetchone()[0]
cur.execute('SELECT COUNT(*) FROM posts')
posts = cur.fetchone()[0]
cur.execute('SELECT COUNT(DISTINCT board_id) FROM topics')
boards = cur.fetchone()[0]
print(f'  Topics: {topics:,}')
print(f'  Posts:  {posts:,}')
print(f'  Boards: {boards}')
print()
print('  By Board:')
cur.execute('''
    SELECT board_id, COUNT(*) as cnt
    FROM topics
    GROUP BY board_id
    ORDER BY cnt DESC
''')
for bid, cnt in cur.fetchall():
    print(f'    Board {bid}: {cnt:,} topics')
"
echo ""

# Latest log entries
echo "📝 LATEST ACTIVITY:"
if [ -f "scrape_log.txt" ]; then
    tail -8 scrape_log.txt | sed 's/^/  /'
else
    echo "  No log file found"
fi
echo ""

# Disk usage
echo "💾 STORAGE USED:"
echo -n "  Raw HTML: " && du -sh raw/ 2>/dev/null | cut -f1 || echo "0"
echo -n "  Database: " && du -sh database/qhimm.db 2>/dev/null | cut -f1 || echo "0"
echo ""

# Estimated progress (rough)
echo "⏱️  ESTIMATED PROGRESS:"
python3 -c "
import sqlite3
conn = sqlite3.connect('database/qhimm.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM topics')
topics = cur.fetchone()[0]
# Rough estimate: ~2300 total topics expected
estimated_total = 2300
pct = min(100, (topics / estimated_total) * 100)
bar_len = 30
filled = int(bar_len * pct / 100)
bar = '█' * filled + '░' * (bar_len - filled)
print(f'  [{bar}] {pct:.1f}%')
print(f'  ({topics:,} / ~{estimated_total:,} estimated topics)')
"
echo ""
echo "Run again with: ./monitor.sh"
