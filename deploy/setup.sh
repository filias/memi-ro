#!/usr/bin/env bash
# Run on the existing memi.click server (Caddy + uv + memi user already set up).
# Usage: WEBHOOK_SECRET=xxxx bash setup.sh
#
# Safe to run against the already-deployed ro.memi.games: it pulls if the repo
# is already cloned, and does not clobber a running game service on another port.
set -euo pipefail

: "${WEBHOOK_SECRET:?Set WEBHOOK_SECRET (the GitHub webhook secret) before running}"

REPO=https://github.com/filias/memi-ro.git
APP_DIR=/opt/memi-ro

# Clone or update (memi user already exists from the main memi setup)
if [ -d "$APP_DIR/.git" ]; then
    sudo -u memi git -C "$APP_DIR" pull
else
    git clone "$REPO" "$APP_DIR"
    chown -R memi:memi "$APP_DIR"
fi

cd "$APP_DIR"
sudo -u memi uv sync

# App service — only install if there isn't one already (don't disturb a running
# instance that may be bound to a different port).
if [ ! -f /etc/systemd/system/memi-ro.service ]; then
    cp deploy/memi-ro.service /etc/systemd/system/memi-ro.service
    systemctl enable memi-ro
fi

# Webhook service + secret
echo "WEBHOOK_SECRET=${WEBHOOK_SECRET}" > /etc/memi-ro-webhook.env
chmod 600 /etc/memi-ro-webhook.env
cp deploy/memi-ro-webhook.service /etc/systemd/system/memi-ro-webhook.service

systemctl daemon-reload
systemctl enable --now memi-ro-webhook
systemctl restart memi-ro   # pick up the code just pulled

# Add the ro.memi.games block to Caddy if missing. If ro.memi.games is already
# in the Caddyfile (it is, since the site already serves), add the /deploy
# handler to its existing block by hand instead — see the note printed below.
if ! grep -q "ro.memi.games" /etc/caddy/Caddyfile; then
cat >> /etc/caddy/Caddyfile <<'EOF'

ro.memi.games {
    handle /deploy {
        reverse_proxy localhost:9016
    }
    handle {
        reverse_proxy localhost:8093
    }
}
EOF
    systemctl reload caddy
else
    echo ""
    echo ">> ro.memi.games already in /etc/caddy/Caddyfile."
    echo ">> Add this INSIDE its block (before the catch-all reverse_proxy), then"
    echo ">> 'systemctl reload caddy':"
    echo ""
    echo "       handle /deploy {"
    echo "           reverse_proxy localhost:9016"
    echo "       }"
fi

echo ""
echo "Done."
echo "GitHub webhook: https://ro.memi.games/deploy  (content-type json, event push,"
echo "                secret = \$WEBHOOK_SECRET)"
