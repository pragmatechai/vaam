#!/usr/bin/env python
"""
Download real product images from Pexels for remaining products with generated placeholders.
Uses direct Pexels CDN URLs (free to use under Pexels license).
"""
import os, sys, ssl, urllib.request, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vaam_project.settings'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Product

media_root = str(django.conf.settings.MEDIA_ROOT)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download(url, filename):
    full_path = os.path.join(media_root, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()
            if len(data) < 5000:
                print(f'  FAIL (too small {len(data)}B): {filename}')
                return False
            with open(full_path, 'wb') as f:
                f.write(data)
            print(f'  OK: {filename} ({len(data)} bytes)')
            return True
    except Exception as e:
        print(f'  FAIL: {filename} - {e}')
        return False

# Pexels photo URLs - all free to use
DOWNLOADS = {
    'ip-camera-4mp-poe': {
        'url': 'https://images.pexels.com/photos/430208/pexels-photo-430208.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/ip-camera-4mp-poe.jpg',
    },
    'nvr-8ch-4k': {
        'url': 'https://images.pexels.com/photos/1181467/pexels-photo-1181467.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/nvr-8ch-4k.jpg',
    },
    'electric-vehicle-suv': {
        'url': 'https://images.pexels.com/photos/3729464/pexels-photo-3729464.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/electric-vehicle-suv.jpg',
    },
    'commercial-truck-light-duty': {
        'url': 'https://images.pexels.com/photos/2199293/pexels-photo-2199293.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/commercial-truck-light-duty.jpg',
    },
    'steel-rebar-hrb400': {
        'url': 'https://images.pexels.com/photos/2760243/pexels-photo-2760243.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/steel-rebar-hrb400.jpg',
    },
    'pvc-pipe-upvc': {
        'url': 'https://images.pexels.com/photos/5691523/pexels-photo-5691523.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/pvc-pipe-upvc.jpg',
    },
    'air-compressor-screw-type': {
        'url': 'https://images.pexels.com/photos/162553/keys-workshop-mechanic-tools-162553.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/air-compressor-screw-type.jpg',
    },
    'electric-forklift-2t': {
        'url': 'https://images.pexels.com/photos/1267338/pexels-photo-1267338.jpeg?auto=compress&cs=tinysrgb&w=800',
        'file': 'products/electric-forklift-2t.jpg',
    },
}

print("Downloading real product images from Pexels...")
downloaded = 0
for slug, info in DOWNLOADS.items():
    p = Product.objects.filter(slug=slug).first()
    if not p:
        print(f'  SKIP: Product {slug} not found')
        continue
    if download(info['url'], info['file']):
        p.image = info['file']
        p.save(update_fields=['image'])
        downloaded += 1

print(f"\nDownloaded {downloaded}/{len(DOWNLOADS)} images")

# Verify all products now have valid images
print("\nVerification:")
for p in Product.objects.all():
    if p.image:
        path = os.path.join(media_root, str(p.image))
        status = "OK" if os.path.exists(path) else "MISSING"
        name = p.name_en or p.name or str(p.id)
        if status == "MISSING":
            print(f"  {status}: [{p.id}] {name[:40]} -> {p.image}")
    else:
        name = p.name_en or p.name or str(p.id)
        print(f"  EMPTY: [{p.id}] {name[:40]}")

print("\nDone!")
