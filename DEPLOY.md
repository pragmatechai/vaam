# Vaam - Deployment Guide (DigitalOcean)

## Arxitektura

```
GitHub (push to main)
    ↓ GitHub Actions
DigitalOcean Droplet (46.101.102.220)
    ├── Nginx (reverse proxy, :80)
    ├── Gunicorn (WSGI server, :8000)
    ├── PostgreSQL (database)
    └── Django App (/home/vaam/app/)
```

---

## Addım 1: GitHub Secrets əlavə edin

GitHub repo-da **Settings → Secrets and variables → Actions** bölməsinə keçin və bu 3 secret əlavə edin:

| Secret adı | Dəyəri |
|---|---|
| `SERVER_HOST` | `46.101.102.220` |
| `SERVER_USER` | `root` |
| `SSH_PRIVATE_KEY` | SSH private key-nizin tam məzmunu (aşağıda izah edilir) |

### SSH Private Key almaq:

Əgər droplet yaradarkən SSH key seçmisinizsə, həmin key-in **private** hissəsini istifadə edin:

```bash
# Lokaldakı private key-i göstərin (adətən bu yolda olur)
cat ~/.ssh/id_rsa
# və ya
cat ~/.ssh/id_ed25519
```

Bütün məzmunu (`-----BEGIN ... KEY-----` daxil olmaqla) `SSH_PRIVATE_KEY` secret-ə yapışdırın.

**Yeni SSH key yaratmaq lazımdırsa:**

```bash
# Lokal kompüterdə
ssh-keygen -t ed25519 -C "deploy@vaam"

# Public key-i serverə əlavə edin
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@46.101.102.220

# Private key-i GitHub secret-ə əlavə edin
cat ~/.ssh/id_ed25519
```

---

## Addım 2: Serverdə ilk quraşdırma

SSH ilə serverə bağlanın və aşağıdakı əmrləri icra edin:

```bash
# Serverə bağlanın
ssh root@46.101.102.220

# Setup skriptini yükləyin və icra edin
apt update && apt install -y git
git clone https://github.com/pragmatechai/vaam.git /tmp/vaam-setup
bash /tmp/vaam-setup/deploy/server_setup.sh
```

Bu skript avtomatik olaraq bunları edəcək:
- Python, PostgreSQL, Nginx, Git quraşdırır
- Firewall konfiqurasiya edir
- PostgreSQL database və user yaradır
- Layihəni klonlayır
- Virtual environment yaradır
- Django migration, collectstatic, compilemessages icra edir
- Nginx və Gunicorn konfiqurasiya edir
- Systemd service quraşdırır

---

## Addım 3: Serverdə `vaam` user üçün SSH açarı quraşdırın

Deploy script `vaam` user-i ilə `git pull` edir. Bu user-in GitHub-dan pull edə bilməsi üçün:

```bash
# Serverdə root olaraq
su - vaam
cd ~/app

# Git remote-u HTTPS saxlayın (artıq belədir)
git remote -v

# Əgər private repo-dursa, GitHub Personal Access Token lazımdır
# Public repo-dursa heç nə lazım deyil
```

---

## Addım 4: Test edin

```bash
# Saytı yoxlayın
curl http://46.101.102.220

# Servis statusunu yoxlayın
systemctl status vaam
systemctl status nginx

# Logları yoxlayın
tail -f /var/log/gunicorn/error.log
journalctl -u vaam -f
```

---

## Avtomatik Deployment Necə İşləyir

1. Siz `main` branch-a push edirsiniz
2. GitHub Actions workflow tətiqlənir
3. GitHub Actions SSH ilə serverə bağlanır
4. Serverdə `git pull` və `deploy/deploy.sh` icra olunur
5. Deploy script: dependencies yeniləyir → migrations → collectstatic → gunicorn restart

---

## Faydalı Əmrlər (Serverdə)

```bash
# Servisi yenidən başlat
sudo systemctl restart vaam

# Nginx yenidən başlat
sudo systemctl restart nginx

# Logları izlə
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/error.log

# Django shell
cd /home/vaam/app
source venv/bin/activate
python manage.py shell

# Superuser yarat
python manage.py createsuperuser

# Manuel deploy
cd /home/vaam/app
git pull origin main
bash deploy/deploy.sh
```

---

## Fayl Strukturu

```
deploy/
├── deploy.sh           # Hər deployment-də icra olunan skript
├── server_setup.sh     # İlk dəfə server quraşdırma skripti
├── nginx/
│   └── vaam.conf       # Nginx konfiqurasiyası
└── systemd/
    └── vaam.service    # Gunicorn systemd service
.github/
└── workflows/
    └── deploy.yml      # GitHub Actions CI/CD workflow
```
