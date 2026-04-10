#!/usr/bin/env python
"""Quick remap: use real existing photos for solar products instead of generated ones."""
import os, sys, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'vaam_project.settings'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Product

remaps = {
    'monocrystalline-solar-panel-550w': 'products/longi-hi-mo-6.jpg',
    'solar-inverter-10kw-hybrid': 'products/huawei-inverter.jpg',
    'solar-mounting-system-rooftop': 'products/mounting-system.jpg',
    'solar-garden-light-60w': 'products/ground-mount.jpg',
    'led-street-light-150w': 'products/solar-cables.jpg',
}

media_root = str(django.conf.settings.MEDIA_ROOT)

for slug, img in remaps.items():
    p = Product.objects.filter(slug=slug).first()
    if p:
        full_path = os.path.join(media_root, img)
        if os.path.exists(full_path):
            p.image = img
            p.save(update_fields=['image'])
            print(f'OK: {slug} -> {img}')
        else:
            print(f'SKIP (file not found): {img}')
    else:
        print(f'NOT FOUND: {slug}')

print('Done!')
