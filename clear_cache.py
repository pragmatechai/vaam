import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
import django
django.setup()

from django.core.cache import cache

keys = ['ctx_site_settings_en', 'ctx_site_settings_tr', 'ctx_site_settings_ru', 'ctx_site_settings_ar']
for k in keys:
    cache.delete(k)
    print(f"Cleared: {k}")

print("Done. All site context caches cleared.")
