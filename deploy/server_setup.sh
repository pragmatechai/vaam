#!/bin/bash
set -e

# =============================================
# Vaam Project - Initial Server Setup
# Run this ONCE on a fresh Ubuntu droplet
# =============================================

SERVER_IP="46.101.102.220"
DB_NAME="vaam_db"
DB_USER="vaam_user"
DB_PASSWORD="Qartdere1@"
APP_USER="vaam"
APP_DIR="/home/$APP_USER/app"
GITHUB_REPO="https://github.com/pragmatechai/vaam.git"

echo "=========================================="
echo "  Vaam - Initial Server Setup"
echo "=========================================="

# --- 1. System Updates ---
echo "[1/10] Updating system packages..."
apt update && apt upgrade -y

# --- 2. Install required packages ---
echo "[2/10] Installing packages..."
apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib \
    nginx \
    git \
    gettext \
    libpq-dev \
    curl \
    ufw

# --- 3. Configure Firewall ---
echo "[3/10] Configuring firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# --- 4. Setup PostgreSQL ---
echo "[4/10] Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "Database already exists"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || echo "User already exists"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'Asia/Baku';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"

# --- 5. Create app user ---
echo "[5/10] Creating application user..."
id -u $APP_USER &>/dev/null || useradd -m -s /bin/bash $APP_USER
usermod -aG www-data $APP_USER

# --- 6. Clone repository ---
echo "[6/10] Cloning repository..."
if [ ! -d "$APP_DIR" ]; then
    sudo -u $APP_USER git clone $GITHUB_REPO $APP_DIR
else
    cd $APP_DIR
    sudo -u $APP_USER git pull origin main
fi

# --- 7. Setup Python virtual environment ---
echo "[7/10] Setting up Python environment..."
sudo -u $APP_USER python3 -m venv $APP_DIR/venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt

# --- 8. Create .env file ---
echo "[8/10] Creating environment file..."
cat > $APP_DIR/.env << EOF
DJANGO_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$SERVER_IP
DB_ENGINE=django.db.backends.postgresql
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
EOF
chown $APP_USER:$APP_USER $APP_DIR/.env
chmod 600 $APP_DIR/.env

# --- 9. Run Django setup ---
echo "[9/10] Running Django setup..."
cd $APP_DIR
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py migrate --noinput
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py collectstatic --noinput
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py compilemessages || true

# Create superuser (interactive)
echo ""
echo ">>> Creating Django superuser..."
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py createsuperuser || true

# --- 10. Setup Nginx & Gunicorn ---
echo "[10/10] Configuring Nginx & Gunicorn..."

# Create gunicorn log directory
mkdir -p /var/log/gunicorn
chown $APP_USER:www-data /var/log/gunicorn

# Create media directory
mkdir -p $APP_DIR/media
chown -R $APP_USER:www-data $APP_DIR/media
chmod -R 775 $APP_DIR/media

# Create staticfiles directory
mkdir -p $APP_DIR/staticfiles
chown -R $APP_USER:www-data $APP_DIR/staticfiles

# Copy Nginx config
cp $APP_DIR/deploy/nginx/vaam.conf /etc/nginx/sites-available/vaam
ln -sf /etc/nginx/sites-available/vaam /etc/nginx/sites-enabled/vaam
rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
nginx -t

# Copy systemd service
cp $APP_DIR/deploy/systemd/vaam.service /etc/systemd/system/vaam.service
systemctl daemon-reload
systemctl enable vaam
systemctl start vaam

# Restart Nginx
systemctl restart nginx

# --- Setup sudoers for deploy script ---
echo "$APP_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart vaam, /bin/systemctl is-active vaam" > /etc/sudoers.d/vaam
chmod 440 /etc/sudoers.d/vaam

echo ""
echo "=========================================="
echo "  ✓ Setup Complete!"
echo "=========================================="
echo ""
echo "  App URL:     http://$SERVER_IP"
echo "  Admin URL:   http://$SERVER_IP/dashboard/"
echo ""
echo "  Next steps:"
echo "  1. Add SSH key to GitHub Secrets (see DEPLOY.md)"
echo "  2. Push to 'main' branch to auto-deploy"
echo ""
