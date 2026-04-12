#!/usr/bin/env python
"""
Fix hero slide images with proper high-quality backgrounds.
Downloads professional images and updates DB records.
"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

import urllib.request
from pathlib import Path
from django.conf import settings
from core.models import HeroSlide

MEDIA = Path(settings.MEDIA_ROOT)
HERO_DIR = MEDIA / 'hero'
HERO_DIR.mkdir(parents=True, exist_ok=True)

# High-quality Unsplash images - royalty-free, 1920x1080 landscape
IMAGES = [
    {
        'url': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=1920&h=1080&fit=crop&q=85',
        'filename': 'hero-trade-1.jpg',
        'desc': 'Global shipping containers / trade',
    },
    {
        'url': 'https://images.unsplash.com/photo-1553413077-190dd305871c?w=1920&h=1080&fit=crop&q=85',
        'filename': 'hero-trade-2.jpg',
        'desc': 'Warehouse / logistics operations',
    },
    {
        'url': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=1920&h=1080&fit=crop&q=85',
        'filename': 'hero-trade-3.jpg',
        'desc': 'Industrial construction / machinery',
    },
]

slides = list(HeroSlide.objects.filter(is_active=True).order_by('id'))
if len(slides) == 0:
    print("No active slides found!")
    sys.exit(1)

for i, img_info in enumerate(IMAGES):
    if i >= len(slides):
        break
    slide = slides[i]
    dest = HERO_DIR / img_info['filename']

    if not dest.exists():
        print(f"  Downloading {img_info['desc']}...")
        try:
            req = urllib.request.Request(img_info['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                dest.write_bytes(data)
            os.chmod(str(dest), 0o644)
            print(f"    Downloaded {len(data)//1024}KB -> {dest.name}")
        except Exception as e:
            print(f"    FAILED: {e}")
            continue
    else:
        print(f"  {dest.name} already exists ({dest.stat().st_size//1024}KB)")

    slide.image = f'hero/{img_info["filename"]}'
    slide.save(update_fields=['image'])
    print(f"    Slide {slide.id} updated -> hero/{img_info['filename']}")

print("\nVerification:")
for s in HeroSlide.objects.filter(is_active=True):
    img_path = MEDIA / str(s.image) if s.image else None
    exists = img_path.exists() if img_path else False
    size = img_path.stat().st_size // 1024 if exists else 0
    print(f"  Slide {s.id}: {s.image} ({size}KB) exists={exists}")

print("\nDone!")
