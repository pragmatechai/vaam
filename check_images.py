#!/usr/bin/env python
"""Check all image fields in the database and verify files exist on disk."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings
from core.models import (
    HeroSlide, Product, ProductCategory, ProductImage, Service, ServiceCategory,
    Project, ProjectImage, ProjectCategory, Brand, News, NewsCategory,
    Testimonial, CompanyInfo, CompanyFeature, ProcessStep, SiteSettings,
    Certificate, Statistic, TeamMember
)

MEDIA_ROOT = str(settings.MEDIA_ROOT)
STATIC_ROOT = str(getattr(settings, 'STATIC_ROOT', ''))

def check_file(field_value):
    if not field_value:
        return "EMPTY"
    try:
        path = field_value.path
    except Exception:
        path = os.path.join(MEDIA_ROOT, str(field_value))
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = f"OK ({size}B)" if exists else "MISSING"
    return f"{status} -> {field_value}"

print("=" * 70)
print("IMAGE AUDIT REPORT")
print("=" * 70)

print(f"\nMEDIA_ROOT: {MEDIA_ROOT}")
print(f"STATIC_ROOT: {STATIC_ROOT}")

# List media directory
print(f"\n--- Media directory contents ---")
if os.path.exists(MEDIA_ROOT):
    for root, dirs, files in os.walk(MEDIA_ROOT):
        level = root.replace(MEDIA_ROOT, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for f in files[:15]:
            fpath = os.path.join(root, f)
            fsize = os.path.getsize(fpath)
            print(f'{subindent}{f} ({fsize}B)')
        if len(files) > 15:
            print(f'{subindent}... and {len(files)-15} more files')
else:
    print("  MEDIA_ROOT does not exist!")

print("\n" + "=" * 70)
print("DATABASE IMAGE FIELDS")
print("=" * 70)

print("\n--- SITE SETTINGS ---")
ss = SiteSettings.objects.first()
if ss:
    for field in ['logo', 'logo_white', 'logo_admin', 'favicon']:
        if hasattr(ss, field):
            print(f"  {field}: {check_file(getattr(ss, field))}")

print("\n--- HERO SLIDES ---")
for h in HeroSlide.objects.all():
    print(f"  [{h.id}]")
    for field in ['image', 'background_image']:
        if hasattr(h, field):
            print(f"    {field}: {check_file(getattr(h, field))}")

print("\n--- COMPANY INFO ---")
for ci in CompanyInfo.objects.all():
    print(f"  [{ci.id}]")
    for field in ['image', 'company_profile_pdf']:
        if hasattr(ci, field):
            print(f"    {field}: {check_file(getattr(ci, field))}")

print("\n--- PRODUCT CATEGORIES ---")
for c in ProductCategory.objects.all():
    name = getattr(c, 'name_en', '') or getattr(c, 'name', '') or ''
    print(f"  [{c.id}] {name[:40]}")
    for field in ['image', 'icon']:
        if hasattr(c, field):
            print(f"    {field}: {check_file(getattr(c, field))}")

print("\n--- PRODUCTS ---")
for p in Product.objects.all():
    name = getattr(p, 'name_en', '') or getattr(p, 'name', '') or ''
    print(f"  [{p.id}] {name[:40]}")
    for field in ['image']:
        if hasattr(p, field):
            print(f"    {field}: {check_file(getattr(p, field))}")

print("\n--- PRODUCT IMAGES ---")
for pi in ProductImage.objects.all():
    print(f"  [{pi.id}] product_id={pi.product_id}")
    print(f"    image: {check_file(pi.image)}")

print("\n--- SERVICE CATEGORIES ---")
for sc in ServiceCategory.objects.all():
    name = getattr(sc, 'name_en', '') or getattr(sc, 'name', '') or ''
    print(f"  [{sc.id}] {name[:40]}")
    for field in ['image', 'icon']:
        if hasattr(sc, field):
            print(f"    {field}: {check_file(getattr(sc, field))}")

print("\n--- SERVICES ---")
for s in Service.objects.all():
    title = getattr(s, 'title_en', '') or getattr(s, 'title', '') or ''
    print(f"  [{s.id}] {title[:40]}")
    for field in ['icon', 'image']:
        if hasattr(s, field):
            print(f"    {field}: {check_file(getattr(s, field))}")

print("\n--- PROJECTS ---")
for p in Project.objects.all():
    title = getattr(p, 'title_en', '') or getattr(p, 'title', '') or ''
    print(f"  [{p.id}] {title[:40]}")
    for field in ['image', 'thumbnail']:
        if hasattr(p, field):
            print(f"    {field}: {check_file(getattr(p, field))}")

print("\n--- PROJECT IMAGES ---")
for pi in ProjectImage.objects.all():
    print(f"  [{pi.id}] project_id={pi.project_id}")
    print(f"    image: {check_file(pi.image)}")

print("\n--- BRANDS ---")
for b in Brand.objects.all():
    print(f"  [{b.id}] {b.name}")
    for field in ['logo']:
        if hasattr(b, field):
            print(f"    {field}: {check_file(getattr(b, field))}")

print("\n--- NEWS ---")
for n in News.objects.all():
    title = getattr(n, 'title_en', '') or getattr(n, 'title', '') or ''
    print(f"  [{n.id}] {title[:40]}")
    for field in ['image']:
        if hasattr(n, field):
            print(f"    {field}: {check_file(getattr(n, field))}")

print("\n--- TESTIMONIALS ---")
for t in Testimonial.objects.all():
    print(f"  [{t.id}] {t.client_name}")
    for field in ['client_photo', 'company_logo']:
        if hasattr(t, field):
            print(f"    {field}: {check_file(getattr(t, field))}")

print("\n--- PROCESS STEPS ---")
for s in ProcessStep.objects.all():
    title = getattr(s, 'title_en', '') or getattr(s, 'title', '') or ''
    print(f"  [{s.id}] {title[:40]}")
    for field in ['icon']:
        if hasattr(s, field):
            print(f"    {field}: {check_file(getattr(s, field))}")

print("\n--- CERTIFICATES ---")
for c in Certificate.objects.all():
    name = getattr(c, 'name_en', '') or getattr(c, 'name', '') or ''
    print(f"  [{c.id}] {name[:40]}")
    for field in ['image']:
        if hasattr(c, field):
            print(f"    {field}: {check_file(getattr(c, field))}")

print("\n--- STATISTICS ---")
for s in Statistic.objects.all():
    label = getattr(s, 'label_en', '') or getattr(s, 'label', '') or ''
    print(f"  [{s.id}] {label[:40]}")
    for field in ['icon']:
        if hasattr(s, field):
            print(f"    {field}: {check_file(getattr(s, field))}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
missing = []
empty = []
ok = []

def collect(model_name, obj_id, field_name, field_value):
    if not field_value:
        empty.append((model_name, obj_id, field_name))
        return
    try:
        path = field_value.path
    except Exception:
        path = os.path.join(MEDIA_ROOT, str(field_value))
    if os.path.exists(path):
        ok.append((model_name, obj_id, field_name, str(field_value)))
    else:
        missing.append((model_name, obj_id, field_name, str(field_value)))

for h in HeroSlide.objects.all():
    for f in ['image', 'background_image']:
        if hasattr(h, f): collect('HeroSlide', h.id, f, getattr(h, f))

for p in Product.objects.all():
    collect('Product', p.id, 'image', p.image)

for pi in ProductImage.objects.all():
    collect('ProductImage', pi.id, 'image', pi.image)

for c in ProductCategory.objects.all():
    for f in ['image', 'icon']:
        if hasattr(c, f): collect('ProductCategory', c.id, f, getattr(c, f))

for sc in ServiceCategory.objects.all():
    for f in ['image', 'icon']:
        if hasattr(sc, f): collect('ServiceCategory', sc.id, f, getattr(sc, f))

for s in Service.objects.all():
    for f in ['icon', 'image']:
        if hasattr(s, f): collect('Service', s.id, f, getattr(s, f))

for p in Project.objects.all():
    for f in ['image', 'thumbnail']:
        if hasattr(p, f): collect('Project', p.id, f, getattr(p, f))

for pi in ProjectImage.objects.all():
    collect('ProjectImage', pi.id, 'image', pi.image)

for b in Brand.objects.all():
    collect('Brand', b.id, 'logo', b.logo)

for n in News.objects.all():
    collect('News', n.id, 'image', n.image)

for t in Testimonial.objects.all():
    collect('Testimonial', t.id, 'photo', t.client_photo)
    if hasattr(t, 'company_logo'):
        collect('Testimonial', t.id, 'company_logo', t.company_logo)

if ss:
    for f in ['logo', 'logo_white', 'logo_admin', 'favicon']:
        if hasattr(ss, f): collect('SiteSettings', ss.id, f, getattr(ss, f))

for s in ProcessStep.objects.all():
    if hasattr(s, 'icon'): collect('ProcessStep', s.id, 'icon', s.icon)

for c in Certificate.objects.all():
    if hasattr(c, 'image'): collect('Certificate', c.id, 'image', c.image)

for ci in CompanyInfo.objects.all():
    collect('CompanyInfo', ci.id, 'image', ci.image)

for item in missing:
    print(f"  MISSING: {item[0]}[{item[1]}].{item[2]} = {item[3]}")

print(f"\nOK: {len(ok)} | MISSING: {len(missing)} | EMPTY: {len(empty)}")
