#!/usr/bin/env bash
# setup_bot_service.sh — Install a systemd user service for the Telegram bot.
#
# The bot process itself is extremely lightweight when idle (~30 MB RAM,
# negligible CPU) — it only spawns the heavy LLM pipeline on demand.
#
# Run once:  bash setup_bot_service.sh
# Remove:    bash setup_bot_service.sh --remove
# Status:    systemctl --user status jarvis-telegram-bot
# Logs:      journalctl --user -u jarvis-telegram-bot -f

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UV="$HOME/.local/bin/uv"
SERVICE_NAME="jarvis-telegram-bot"
SERVICE_FILE="$HOME/.config/systemd/user/${SERVICE_NAME}.service"

# ── Removal ───────────────────────────────────────────────────────────────────
if [[ "$1" == "--remove" ]]; then
    systemctl --user stop    "$SERVICE_NAME" 2>/dev/null
    systemctl --user disable "$SERVICE_NAME" 2>/dev/null
    rm -f "$SERVICE_FILE"
    systemctl --user daemon-reload
    echo "✅ Telegram bot service removed."
    exit 0
fi

# ── Pre-flight ────────────────────────────────────────────────────────────────
if [[ ! -f "$REPO_DIR/.env" ]]; then
    echo "⚠️  No .env file found at $REPO_DIR/.env"
    echo "   Create one with at least:"
    echo "     TELEGRAM_BOT_TOKEN=<your token from @BotFather>"
    echo "   Then re-run this script."
    exit 1
fi

if [[ ! -x "$UV" ]]; then
    echo "❌ uv not found at $UV — please install it first."
    exit 1
fi

# ── Write service unit ────────────────────────────────────────────────────────
mkdir -p "$HOME/.config/systemd/user"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=JarvisForResearchers Telegram Bot
Documentation=https://github.com/davidlai0522/jarvisforresearchers
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${REPO_DIR}
ExecStart=${UV} run python telegram_bot.py
Restart=on-failure
RestartSec=15s
# Avoid a tight restart loop (max 5 restarts in 2 minutes)
StartLimitBurst=5
StartLimitIntervalSec=120
StandardOutput=journal
StandardError=journal
# Load TELEGRAM_BOT_TOKEN and other secrets from .env
EnvironmentFile=${REPO_DIR}/.env

[Install]
WantedBy=default.target
EOF

# ── Enable & start ────────────────────────────────────────────────────────────
systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME"
systemctl --user start  "$SERVICE_NAME"

# ── Enable linger so the service survives logout ──────────────────────────────
loginctl enable-linger "$(whoami)" 2>/dev/null && \
    echo "  ✓ Linger enabled — bot will start at boot even without login." || \
    echo "  ⚠️  Could not enable linger (may need sudo). The bot will only run while you're logged in."

echo ""
echo "✅ Telegram bot service installed and started."
echo ""
echo "   Check status : systemctl --user status  $SERVICE_NAME"
echo "   Follow logs  : journalctl --user -u $SERVICE_NAME -f"
echo "   Stop         : systemctl --user stop     $SERVICE_NAME"
echo "   Restart      : systemctl --user restart  $SERVICE_NAME"
echo "   Remove       : bash setup_bot_service.sh --remove"
