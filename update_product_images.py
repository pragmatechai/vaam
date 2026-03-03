"""
Script to update product image fields in the database for the new generator
and transformer products.
Run from the project root: python update_product_images.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()

from core.models import Product

IMAGE_MAP = {
    'generator-50-kva': 'products/generator-50-kva.jpg',
    'generator-100-kva': 'products/generator-100-kva.png',
    'generator-150-kva': 'products/generator-150-kva.jpg',
    'generator-300-kva': 'products/generator-300-kva.jpg',
    'generator-375-kva': 'products/generator-375-kva.jpg',
    'generator-500-kva': 'products/generator-500-kva.jpg',
    'transformer-1600-kva-35kv-aluminium': 'products/transformer-1600-kva-al.jpg',
    'transformer-1600-kva-35kv-copper': 'products/transformer-1600-kva-cu.jpg',
    'transformer-2500-kva-35kv-aluminium': 'products/transformer-2500-kva-al.jpg',
    'transformer-2500-kva-35kv-copper': 'products/transformer-2500-kva-cu.jpg',
}

print("Updating product images...")
for slug, image_path in IMAGE_MAP.items():
    count = Product.objects.filter(slug=slug).update(image=image_path)
    if count:
        print(f"  ✓ {slug} → {image_path}")
    else:
        print(f"  ✗ {slug} — NOT FOUND in database")

print("\nDone!")
