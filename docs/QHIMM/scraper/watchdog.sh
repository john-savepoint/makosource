#!/bin/bash
# Watchdog script - monitors auto_scrape.py and restarts if stuck
# Run: ./watchdog.sh
# Stop: Ctrl+C or kill the watchdog process

cd "$(dirname "$0")"
LOG="../scrape_log.txt"
TIMEOUT=60  # seconds to wait before assuming stuck

echo "╔════════════════════════════════════════════════════════════╗"
echo "║              QHIMM SCRAPER WATCHDOG                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Monitoring auto_scrape.py - will restart if stuck for ${TIMEOUT}s"
echo "Press Ctrl+C to stop"
echo ""

while true; do
    # Check if scraper already running, attach to it instead of killing
    EXISTING_PID=$(pgrep -f "auto_scrape.py" | head -1)
    if [ -n "$EXISTING_PID" ]; then
        echo "[$(date '+%H:%M:%S')] Attaching to existing scraper PID $EXISTING_PID"
        PID=$EXISTING_PID
    else
        echo "[$(date '+%H:%M:%S')] Starting new scraper..."
        python3 -u auto_scrape.py >> "$LOG" 2>&1 &
        PID=$!
    fi

    # Monitor the log file for activity
    LAST_SIZE=$(stat -c%s "$LOG" 2>/dev/null || echo 0)
    STUCK_COUNT=0

    while kill -0 $PID 2>/dev/null; do
        sleep 10

        NEW_SIZE=$(stat -c%s "$LOG" 2>/dev/null || echo 0)

        if [ "$NEW_SIZE" -eq "$LAST_SIZE" ]; then
            STUCK_COUNT=$((STUCK_COUNT + 1))
            echo "[$(date '+%H:%M:%S')] No output for $((STUCK_COUNT * 10))s..."

            if [ $STUCK_COUNT -ge $((TIMEOUT / 10)) ]; then
                echo "[$(date '+%H:%M:%S')] ⚠️ Stuck detected! Restarting..."
                kill -9 $PID 2>/dev/null
                break
            fi
        else
            STUCK_COUNT=0
            LAST_SIZE=$NEW_SIZE
            # Show last line of progress
            tail -1 "$LOG" | head -c 60
            echo ""
        fi
    done

    # Check if process exited normally
    if ! kill -0 $PID 2>/dev/null; then
        wait $PID
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 0 ]; then
            echo "[$(date '+%H:%M:%S')] ✅ Scraper completed successfully!"
            break
        else
            echo "[$(date '+%H:%M:%S')] Process exited with code $EXIT_CODE, restarting..."
        fi
    fi

    sleep 5
done

echo ""
echo "Watchdog finished"
