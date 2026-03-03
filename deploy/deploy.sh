#!/bin/bash
set -e

# =============================================
# Vaam Project - Server Deploy Script
# Designed to be called by root (via GitHub Actions SSH)
# Runs Django commands as 'vaam' user
# =============================================

APP_DIR="/home/vaam/app"
VENV_DIR="$APP_DIR/venv"

echo "=========================================="
echo "  Deploying Vaam Project..."
echo "=========================================="

cd "$APP_DIR"

# Pull latest code (as root, with safe.directory)
echo "[1/6] Pulling latest code..."
git config --global --add safe.directory "$APP_DIR"
git reset --hard HEAD
git clean -fd
git pull origin main

# Install/update dependencies (as vaam user)
echo "[2/6] Installing dependencies..."
sudo -u vaam "$VENV_DIR/bin/pip" install -q -r requirements.txt

# Run database migrations (as vaam user)
echo "[3/6] Running migrations..."
sudo -u vaam "$VENV_DIR/bin/python" manage.py migrate --noinput

# Ensure cache table exists (safe to run repeatedly)
sudo -u vaam "$VENV_DIR/bin/python" manage.py createcachetable 2>/dev/null || true

# Collect static files (as vaam user)
echo "[4/6] Collecting static files..."
sudo -u vaam "$VENV_DIR/bin/python" manage.py collectstatic --noinput

# Compile translation messages (as vaam user)
echo "[5/6] Compiling translations..."
rm -f "$APP_DIR/locale/*/LC_MESSAGES/*.mo"
sudo -u vaam "$VENV_DIR/bin/python" manage.py compilemessages || true

# Restart Gunicorn (as root)
echo "[6/6] Restarting Gunicorn..."
systemctl restart vaam

# Verify service status
systemctl is-active --quiet vaam && echo "✓ Vaam service is running!" || echo "✗ Service failed to start!"

echo "=========================================="
echo "  Deployment complete!"
echo "=========================================="
