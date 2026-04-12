import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

import urllib.request
from pathlib import Path
from django.conf import settings
from core.models import CompanyInfo

MEDIA = Path(settings.MEDIA_ROOT)
c = CompanyInfo.objects.first()
print(f"Current image: {c.image}")

# Download a proper trade/procurement image
url = 'https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=800&h=600&fit=crop&q=85'
dest = MEDIA / 'about' / 'company-trade.jpg'
dest.parent.mkdir(parents=True, exist_ok=True)

if not dest.exists():
    print("Downloading trade/logistics image...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        dest.write_bytes(data)
    os.chmod(str(dest), 0o644)
    print(f"  Downloaded {len(data)//1024}KB")

c.image = 'about/company-trade.jpg'
c.save(update_fields=['image'])
print(f"Updated to: {c.image}")
print(f"File exists: {dest.exists()}")
