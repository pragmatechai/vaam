#!/usr/bin/env python
"""Quick final verification of all image files."""
import os, sys, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'vaam_project.settings'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import (
    Product, ProductCategory, Brand, News, Testimonial,
    Service, Project, ProjectImage, HeroSlide, SiteSettings, CompanyInfo
)

media_root = str(django.conf.settings.MEDIA_ROOT)
missing = []
ok = []
empty = []

def check(model_name, obj_id, field_name, field_value):
    if not field_value:
        empty.append(f"{model_name}[{obj_id}].{field_name}")
        return
    try:
        path = field_value.path
    except:
        path = os.path.join(media_root, str(field_value))
    if os.path.exists(path):
        ok.append(f"{model_name}[{obj_id}].{field_name} = {field_value}")
    else:
        missing.append(f"{model_name}[{obj_id}].{field_name} = {field_value}")

# Check all image fields
for p in Product.objects.all():
    check('Product', p.id, 'image', p.image)

for b in Brand.objects.all():
    check('Brand', b.id, 'logo', b.logo)

for n in News.objects.all():
    check('News', n.id, 'image', n.image)

for t in Testimonial.objects.all():
    check('Testimonial', t.id, 'photo', t.photo)

for h in HeroSlide.objects.all():
    check('HeroSlide', h.id, 'image', h.image)

for p in Project.objects.all():
    check('Project', p.id, 'image', p.image)

for pi in ProjectImage.objects.all():
    check('ProjectImage', pi.id, 'image', pi.image)

ss = SiteSettings.objects.first()
if ss:
    for f in ['logo', 'logo_white', 'favicon']:
        if hasattr(ss, f):
            check('SiteSettings', ss.id, f, getattr(ss, f))

ci = CompanyInfo.objects.first()
if ci:
    check('CompanyInfo', ci.id, 'image', ci.image)

print("=" * 60)
print("FINAL IMAGE VERIFICATION")
print("=" * 60)
print(f"\n  OK:      {len(ok)}")
print(f"  MISSING: {len(missing)}")
print(f"  EMPTY:   {len(empty)}")

if missing:
    print(f"\nMISSING FILES:")
    for m in missing:
        print(f"  ❌ {m}")

if empty:
    print(f"\nEMPTY FIELDS (no image set):")
    for e in empty:
        print(f"  ⚪ {e}")

if not missing:
    print(f"\n✅ All image files exist on disk!")
