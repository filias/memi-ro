#!/usr/bin/env bash
# Run on the existing memi.click server (Caddy + uv + memi user already set up).
# Usage: WEBHOOK_SECRET=xxxx bash setup.sh
# On a rerun, leave WEBHOOK_SECRET unset to keep the secret already in
# /etc/memi-ro-webhook.env (the one GitHub has).
#
# Safe to run against the already-deployed ro.memi.games: it pulls if the repo
# is already cloned, and does not clobber a running game service on another port.
set -euo pipefail

ENV_FILE=/etc/memi-ro-webhook.env
if [ -z "${WEBHOOK_SECRET:-}" ] && [ ! -f "$ENV_FILE" ]; then
    echo "Set WEBHOOK_SECRET (the GitHub webhook secret) before running" >&2
    exit 1
fi

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
if [ -n "${WEBHOOK_SECRET:-}" ]; then
    echo "WEBHOOK_SECRET=${WEBHOOK_SECRET}" > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
fi
cp deploy/memi-ro-webhook.service /etc/systemd/system/memi-ro-webhook.service

systemctl daemon-reload
systemctl enable memi-ro-webhook
systemctl restart memi-ro-webhook   # pick up a changed secret
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
