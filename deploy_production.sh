#!/bin/bash
# ══════════════════════════════════════════════════════════════════════════════
# VAAM - Direct Production Deploy Script (SSH, no GitHub Actions)
# ══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   bash deploy_production.sh                  # Full deploy (code + migrate + seed + restart)
#   bash deploy_production.sh --code-only      # Only deploy code (no seed)
#   bash deploy_production.sh --seed-only      # Only run seed script (no code deploy)
#   bash deploy_production.sh --migrate-only   # Only run migrations
#
# Prerequisites:
#   - SSH access to the server (key-based auth)
#   - Server: 46.101.102.220
#   - App path: /home/vaam/app
#   - Venv: /home/vaam/app/venv
#
# ══════════════════════════════════════════════════════════════════════════════

set -e

# ── Configuration ─────────────────────────────────────────────────────────────
SERVER_IP="46.101.102.220"
SERVER_USER="root"
APP_DIR="/home/vaam/app"
VENV_DIR="$APP_DIR/venv"
BRANCH="main"
SERVICE_NAME="vaam"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ── Helper functions ──────────────────────────────────────────────────────────
log_step() { echo -e "\n${BLUE}[$1]${NC} $2"; }
log_ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
log_warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
log_err()  { echo -e "  ${RED}✗${NC} $1"; }

remote_exec() {
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "${SERVER_USER}@${SERVER_IP}" "$1"
}

remote_as_vaam() {
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "${SERVER_USER}@${SERVER_IP}" \
        "cd $APP_DIR && sudo -u vaam $VENV_DIR/bin/python $1"
}

# ── Parse arguments ───────────────────────────────────────────────────────────
MODE="full"
if [ "$1" == "--code-only" ]; then
    MODE="code"
elif [ "$1" == "--seed-only" ]; then
    MODE="seed"
elif [ "$1" == "--migrate-only" ]; then
    MODE="migrate"
fi

echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  VAAM Production Deploy (Direct SSH)${NC}"
echo -e "${GREEN}  Server: ${SERVER_IP}  |  Mode: ${MODE}${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"

# ── Step 0: Test SSH connection ───────────────────────────────────────────────
log_step "0" "Testing SSH connection..."
if remote_exec "echo 'SSH OK'" > /dev/null 2>&1; then
    log_ok "SSH connection successful"
else
    log_err "Cannot connect to ${SERVER_IP}. Check SSH key and network."
    exit 1
fi

# ── Step 1: Deploy code ──────────────────────────────────────────────────────
if [ "$MODE" == "full" ] || [ "$MODE" == "code" ]; then
    log_step "1" "Deploying code to production..."

    # Upload new/changed files
    log_step "1a" "Uploading seed_update_production.py..."
    scp -o StrictHostKeyChecking=no seed_update_production.py "${SERVER_USER}@${SERVER_IP}:${APP_DIR}/"
    log_ok "Seed script uploaded"

    # Pull latest code from git
    log_step "1b" "Pulling latest code from git..."
    remote_exec "cd $APP_DIR && git config --global --add safe.directory $APP_DIR && git stash && git pull origin $BRANCH"
    log_ok "Code pulled from $BRANCH"

    # Install dependencies
    log_step "1c" "Installing Python dependencies..."
    remote_exec "cd $APP_DIR && sudo -u vaam $VENV_DIR/bin/pip install -q -r requirements.txt"
    log_ok "Dependencies installed"
fi

# ── Step 2: Run migrations ───────────────────────────────────────────────────
if [ "$MODE" == "full" ] || [ "$MODE" == "migrate" ]; then
    log_step "2" "Running database migrations..."
    remote_exec "cd $APP_DIR && sudo -u vaam $VENV_DIR/bin/python manage.py migrate --noinput"
    log_ok "Migrations applied"

    # Create cache table (safe to run repeatedly)
    remote_exec "cd $APP_DIR && sudo -u vaam $VENV_DIR/bin/python manage.py createcachetable 2>/dev/null || true"
fi

# ── Step 3: Run seed/update script ────────────────────────────────────────────
if [ "$MODE" == "full" ] || [ "$MODE" == "seed" ]; then
    log_step "3" "Running production database update (seed_update_production.py)..."

    # First upload the latest version
    scp -o StrictHostKeyChecking=no seed_update_production.py "${SERVER_USER}@${SERVER_IP}:${APP_DIR}/"

    # Run the seed script
    remote_exec "cd $APP_DIR && sudo -u vaam $VENV_DIR/bin/python seed_update_production.py"
    log_ok "Database updated with correct product data"
fi

# ── Step 4: Collect static files ──────────────────────────────────────────────
if [ "$MODE" == "full" ] || [ "$MODE" == "code" ]; then
    log_step "4" "Collecting static files..."
    remote_exec "cd $APP_DIR && sudo -u vaam $VENV_DIR/bin/python manage.py collectstatic --noinput"
    log_ok "Static files collected"
fi

# ── Step 5: Compile translations ─────────────────────────────────────────────
if [ "$MODE" == "full" ] || [ "$MODE" == "code" ]; then
    log_step "5" "Compiling translations..."
    remote_exec "cd $APP_DIR && rm -f locale/*/LC_MESSAGES/*.mo && sudo -u vaam $VENV_DIR/bin/python manage.py compilemessages 2>/dev/null || true"
    log_ok "Translations compiled"
fi

# ── Step 6: Restart services ─────────────────────────────────────────────────
log_step "6" "Restarting services..."
remote_exec "systemctl restart $SERVICE_NAME"

# Verify service is running
if remote_exec "systemctl is-active --quiet $SERVICE_NAME"; then
    log_ok "Gunicorn ($SERVICE_NAME) is running"
else
    log_err "Service failed to start! Check: ssh $SERVER_USER@$SERVER_IP journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi

# ── Step 7: Health check ─────────────────────────────────────────────────────
log_step "7" "Running health checks..."

# Check if the site responds
HTTP_CODE=$(remote_exec "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/ -H 'Host: vaamglobal.com'" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" == "200" ] || [ "$HTTP_CODE" == "301" ] || [ "$HTTP_CODE" == "302" ]; then
    log_ok "Site responding (HTTP $HTTP_CODE)"
else
    log_warn "Site returned HTTP $HTTP_CODE — may need investigation"
fi

# Check database connectivity
remote_exec "cd $APP_DIR && sudo -u vaam $VENV_DIR/bin/python -c \"
import django; import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()
from core.models import Product, Service
print(f'  Products: {Product.objects.filter(is_active=True).count()}')
print(f'  Services: {Service.objects.count()}')
print(f'  ✓ Database OK')
\""
log_ok "Health checks passed"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ DEPLOYMENT COMPLETED SUCCESSFULLY!${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${BLUE}Site:${NC}      https://vaamglobal.com"
echo -e "  ${BLUE}Server:${NC}    ${SERVER_IP}"
echo -e "  ${BLUE}Mode:${NC}      ${MODE}"
echo -e "  ${BLUE}Branch:${NC}    ${BRANCH}"
echo ""
echo -e "  ${YELLOW}Useful commands:${NC}"
echo -e "    ssh ${SERVER_USER}@${SERVER_IP} journalctl -u ${SERVICE_NAME} -n 50   # Service logs"
echo -e "    ssh ${SERVER_USER}@${SERVER_IP} systemctl status ${SERVICE_NAME}       # Service status"
echo -e "    bash deploy_production.sh --seed-only                                  # Re-run seed only"
echo ""
