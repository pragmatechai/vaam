#!/usr/bin/env python
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import HeroSlide
slides = HeroSlide.objects.filter(is_active=True)
print(f"Total active slides: {slides.count()}")
for s in slides:
    print(f"  ID={s.id} | image='{s.image}' | has_file={bool(s.image)} | title='{s.title}'")
    if s.image:
        import pathlib
        full = pathlib.Path(s.image.path) if hasattr(s.image, 'path') else None
        if full:
            print(f"    path={full} | exists={full.exists()}")
