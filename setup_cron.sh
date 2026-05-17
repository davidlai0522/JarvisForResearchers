#!/usr/bin/env bash
# setup_cron.sh — Install cron jobs for JarvisForResearchers
#
# Installs two jobs:
#   1. Daily paper pipeline   — schedule from discovery.cron_schedule (default 08:00 daily)
#   2. Weekly digest          — schedule from digest.cron_schedule     (default 09:00 Sunday)
#
# Run once:  bash setup_cron.sh
# Remove:    bash setup_cron.sh --remove

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UV="$HOME/.local/bin/uv"
LOG_DIR="$REPO_DIR/logs"
DAILY_TAG="# jarvis-for-researchers-daily"
DIGEST_TAG="# jarvis-for-researchers-digest"

# Read schedules from config.yaml; fall back to safe defaults
DAILY_SCHEDULE=$("$UV" run python3 -c \
  "import yaml; c=yaml.safe_load(open('$REPO_DIR/config.yaml')); print(c.get('discovery',{}).get('cron_schedule','0 8 * * *'))" \
  2>/dev/null || echo "0 8 * * *")

DIGEST_SCHEDULE=$("$UV" run python3 -c \
  "import yaml; c=yaml.safe_load(open('$REPO_DIR/config.yaml')); print(c.get('digest',{}).get('cron_schedule','0 9 * * 0'))" \
  2>/dev/null || echo "0 9 * * 0")

DAILY_JOB="$DAILY_SCHEDULE cd \"$REPO_DIR\" && mkdir -p \"$LOG_DIR\" && \"$UV\" run python pipeline/run.py --daily >> \"$LOG_DIR/daily.log\" 2>&1 $DAILY_TAG"
DIGEST_JOB="$DIGEST_SCHEDULE cd \"$REPO_DIR\" && mkdir -p \"$LOG_DIR\" && \"$UV\" run python pipeline/run.py --digest >> \"$LOG_DIR/digest.log\" 2>&1 $DIGEST_TAG"

if [[ "$1" == "--remove" ]]; then
    crontab -l 2>/dev/null | grep -v "$DAILY_TAG" | grep -v "$DIGEST_TAG" | crontab -
    echo "✅ JarvisForResearchers daily and digest crons removed."
    exit 0
fi

CURRENT_CRONTAB=$(crontab -l 2>/dev/null)
INSTALLED=0

# Daily cron
if echo "$CURRENT_CRONTAB" | grep -q "$DAILY_TAG"; then
    echo "⚠️  Daily cron already installed (skipping)."
else
    CURRENT_CRONTAB=$(printf '%s\n%s' "$CURRENT_CRONTAB" "$DAILY_JOB")
    INSTALLED=$((INSTALLED + 1))
fi

# Weekly digest cron
if echo "$CURRENT_CRONTAB" | grep -q "$DIGEST_TAG"; then
    echo "⚠️  Digest cron already installed (skipping)."
else
    CURRENT_CRONTAB=$(printf '%s\n%s' "$CURRENT_CRONTAB" "$DIGEST_JOB")
    INSTALLED=$((INSTALLED + 1))
fi

if [[ $INSTALLED -gt 0 ]]; then
    mkdir -p "$LOG_DIR"
    echo "$CURRENT_CRONTAB" | crontab -
fi

if echo "$(crontab -l 2>/dev/null)" | grep -q "$DAILY_TAG"; then
    echo "✅ Daily cron — runs at 08:00 every morning."
    echo "   Logs: $LOG_DIR/daily.log"
fi
if echo "$(crontab -l 2>/dev/null)" | grep -q "$DIGEST_TAG"; then
    echo "✅ Digest cron — runs at 09:00 every Sunday."
    echo "   Logs: $LOG_DIR/digest.log"
fi
echo "   Remove both with: bash setup_cron.sh --remove"
