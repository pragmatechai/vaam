#!/usr/bin/env python
"""
VAAM Image Fix Script
=====================
Downloads real images for products, brands, and news that currently have placeholder references.
Uses Pexels free photos and generates SVG brand logos.
"""
import os
import sys
import django
import urllib.request
import ssl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings
from core.models import (
    Product, ProductCategory, Brand, News, Testimonial,
    ServiceCategory, Service, HeroSlide, SiteSettings
)

MEDIA_ROOT = str(settings.MEDIA_ROOT)

# Disable SSL verification for image downloads (some CDNs have cert issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def download_image(url, save_path):
    """Download image from URL to save_path."""
    full_path = os.path.join(MEDIA_ROOT, save_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    if os.path.exists(full_path) and os.path.getsize(full_path) > 1000:
        print(f"    [SKIP] Already exists: {save_path}")
        return True
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            data = response.read()
            with open(full_path, 'wb') as f:
                f.write(data)
        print(f"    [OK] Downloaded: {save_path} ({len(data)} bytes)")
        return True
    except Exception as e:
        print(f"    [FAIL] {save_path}: {e}")
        return False


def create_product_image_pillow(product_name, save_path, color_rgb=(41, 98, 78)):
    """Create a professional product placeholder image using Pillow."""
    full_path = os.path.join(MEDIA_ROOT, save_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    if os.path.exists(full_path) and os.path.getsize(full_path) > 1000:
        print(f"    [SKIP] Already exists: {save_path}")
        return True
    try:
        from PIL import Image, ImageDraw, ImageFont
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color=color_rgb)
        draw = ImageDraw.Draw(img)

        # Draw gradient overlay
        for y in range(height):
            alpha = int(60 * (y / height))
            draw.line([(0, y), (width, y)], fill=(
                max(0, color_rgb[0] - alpha),
                max(0, color_rgb[1] - alpha),
                max(0, color_rgb[2] - alpha)
            ))

        # Draw pattern lines
        for i in range(0, width + height, 40):
            draw.line([(i, 0), (i - height, height)],
                      fill=(255, 255, 255, 15), width=1)

        # Draw product name text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except (IOError, OSError):
            font = ImageFont.load_default()
            font_small = font

        # Product name - wrap if needed
        words = product_name.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            try:
                bbox = draw.textbbox((0, 0), test_line, font=font)
                tw = bbox[2] - bbox[0]
            except AttributeError:
                tw = len(test_line) * 20
            if tw > width - 80:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        # Center text vertically
        line_height = 42
        total_height = len(lines) * line_height + 30
        start_y = (height - total_height) // 2

        for i, line in enumerate(lines):
            try:
                bbox = draw.textbbox((0, 0), line, font=font)
                tw = bbox[2] - bbox[0]
            except AttributeError:
                tw = len(line) * 20
            x = (width - tw) // 2
            y = start_y + i * line_height
            # Shadow
            draw.text((x + 2, y + 2), line, fill=(0, 0, 0), font=font)
            draw.text((x, y), line, fill=(255, 255, 255), font=font)

        # VAAM branding
        brand_text = "VAAM Trading"
        draw.text((width - 150, height - 40), brand_text, fill=(255, 255, 255, 128), font=font_small)

        img.save(full_path, 'JPEG', quality=85)
        print(f"    [OK] Created: {save_path}")
        return True
    except Exception as e:
        print(f"    [FAIL] Pillow create {save_path}: {e}")
        return False


def create_brand_svg(brand_name, save_path, color="#29624E"):
    """Create a simple SVG brand logo."""
    full_path = os.path.join(MEDIA_ROOT, save_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    if os.path.exists(full_path) and os.path.getsize(full_path) > 100:
        print(f"    [SKIP] Already exists: {save_path}")
        return True
    try:
        # Clean brand name for display
        short_name = brand_name.replace(' (China)', '').replace(' Motor', '').replace(' Technology', '')
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80">
  <rect width="200" height="80" rx="8" fill="white" stroke="#e0e0e0" stroke-width="1"/>
  <text x="100" y="48" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" fill="{color}" text-anchor="middle">{short_name}</text>
</svg>'''
        with open(full_path, 'w') as f:
            f.write(svg)
        print(f"    [OK] Created SVG: {save_path}")
        return True
    except Exception as e:
        print(f"    [FAIL] SVG {save_path}: {e}")
        return False


print("=" * 70)
print("  VAAM Image Fix Script")
print("=" * 70)

# ══════════════════════════════════════════════════════════════════════════
# STEP 1: Fix Product Images
# ══════════════════════════════════════════════════════════════════════════
print("\n[1/4] Fixing product images...")

# Map product slugs/names to Pexels image URLs (free to use)
PRODUCT_IMAGE_URLS = {
    '550w-monocrystalline-solar-panel': {
        'url': 'https://images.pexels.com/photos/9875441/pexels-photo-9875441.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/solar-panel-550w.jpg',
        'color': (25, 80, 120),
    },
    '10kw-hybrid-solar-inverter': {
        'url': 'https://images.pexels.com/photos/9875415/pexels-photo-9875415.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/solar-inverter-10kw.jpg',
        'color': (30, 70, 100),
    },
    'aluminum-rooftop-mounting-system': {
        'url': 'https://images.pexels.com/photos/9875454/pexels-photo-9875454.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/mounting-system-roof.jpg',
        'color': (60, 60, 70),
    },
    '150w-led-street-light': {
        'url': 'https://images.pexels.com/photos/1108572/pexels-photo-1108572.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/led-street-light.jpg',
        'color': (50, 50, 60),
    },
    '60w-solar-garden-light': {
        'url': 'https://images.pexels.com/photos/1108572/pexels-photo-1108572.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/solar-garden-light.jpg',
        'color': (40, 70, 50),
    },
    '4mp-poe-ip-camera': {
        'url': 'https://images.pexels.com/photos/430208/pexels-photo-430208.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/ip-camera-4mp.jpg',
        'color': (40, 40, 50),
    },
    '8-channel-4k-nvr-system': {
        'url': 'https://images.pexels.com/photos/430208/pexels-photo-430208.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/nvr-system-8ch.jpg',
        'color': (30, 30, 45),
    },
    'electric-suv-chinese-brand': {
        'url': 'https://images.pexels.com/photos/3729464/pexels-photo-3729464.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/electric-suv.jpg',
        'color': (35, 55, 75),
    },
    'light-duty-commercial-truck': {
        'url': 'https://images.pexels.com/photos/2199293/pexels-photo-2199293.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/commercial-truck.jpg',
        'color': (60, 50, 40),
    },
    'hrb400-steel-rebar': {
        'url': 'https://images.pexels.com/photos/2760243/pexels-photo-2760243.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/steel-rebar.jpg',
        'color': (70, 60, 50),
    },
    'upvc-water-pipe': {
        'url': 'https://images.pexels.com/photos/5691523/pexels-photo-5691523.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/pvc-pipe.jpg',
        'color': (50, 70, 80),
    },
    'screw-air-compressor-22kw': {
        'url': 'https://images.pexels.com/photos/162553/keys-workshop-mechanic-tools-162553.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/air-compressor.jpg',
        'color': (65, 55, 40),
    },
    '2-ton-electric-forklift': {
        'url': 'https://images.pexels.com/photos/1267338/pexels-photo-1267338.jpeg?auto=compress&cs=tinysrgb&w=800',
        'filename': 'products/electric-forklift.jpg',
        'color': (70, 60, 30),
    },
}

# Also remap products that can use existing server images
PRODUCT_EXISTING_MAP = {
    '550w-monocrystalline-solar-panel': 'products/longi-hi-mo-6.jpg',
    '10kw-hybrid-solar-inverter': 'products/huawei-inverter.jpg',
    'aluminum-rooftop-mounting-system': 'products/mounting-system.jpg',
}

product_fixed = 0
products_with_placeholder = Product.objects.filter(image='products/placeholder.jpg')
print(f"  Found {products_with_placeholder.count()} products with placeholder images")

for product in products_with_placeholder:
    slug = product.slug
    name = product.name_en or product.name or str(product.id)
    print(f"\n  Product: {name} (slug={slug})")

    # First try to use existing server images
    if slug in PRODUCT_EXISTING_MAP:
        existing = PRODUCT_EXISTING_MAP[slug]
        existing_path = os.path.join(MEDIA_ROOT, existing)
        if os.path.exists(existing_path):
            product.image = existing
            product.save(update_fields=['image'])
            print(f"    [OK] Remapped to existing: {existing}")
            product_fixed += 1
            continue

    # Try downloading from Pexels
    if slug in PRODUCT_IMAGE_URLS:
        info = PRODUCT_IMAGE_URLS[slug]
        if download_image(info['url'], info['filename']):
            product.image = info['filename']
            product.save(update_fields=['image'])
            product_fixed += 1
            continue
        # Fallback: create using Pillow
        if create_product_image_pillow(name, info['filename'], info['color']):
            product.image = info['filename']
            product.save(update_fields=['image'])
            product_fixed += 1
            continue
    else:
        # Unknown slug - create generic placeholder
        safe_slug = slug or f"product-{product.id}"
        filename = f"products/{safe_slug}.jpg"
        if create_product_image_pillow(name, filename, (41, 98, 78)):
            product.image = filename
            product.save(update_fields=['image'])
            product_fixed += 1

print(f"\n  ✓ Fixed {product_fixed} product images")


# ══════════════════════════════════════════════════════════════════════════
# STEP 2: Fix Brand Logos
# ══════════════════════════════════════════════════════════════════════════
print("\n[2/4] Fixing brand logos...")

# Map brands to existing SVGs or create new ones
BRAND_EXISTING_MAP = {
    'Longi Solar': 'brands/longi-logo.svg',
    'JA Solar': 'brands/ja-logo.svg',
    'Huawei': 'brands/huawei-logo.svg',
}

BRAND_COLORS = {
    'BYD': '#3F8F2F',
    'CHERY': '#CC0000',
    'Huawei': '#CF0A2C',
    'Hikvision': '#E31937',
    'Dahua Technology': '#003DA5',
    'FOTON Motor': '#00468B',
    'Dongfeng': '#0A2875',
    'Longi Solar': '#00823B',
    'JA Solar': '#005BAA',
    'Cummins (China)': '#C8102E',
}

brand_fixed = 0
brands_with_placeholder = Brand.objects.filter(logo='brands/placeholder.png')
print(f"  Found {brands_with_placeholder.count()} brands with placeholder logos")

for brand in brands_with_placeholder:
    name = brand.name
    print(f"\n  Brand: {name}")

    # Try existing SVG
    if name in BRAND_EXISTING_MAP:
        existing = BRAND_EXISTING_MAP[name]
        existing_path = os.path.join(MEDIA_ROOT, existing)
        if os.path.exists(existing_path):
            brand.logo = existing
            brand.save(update_fields=['logo'])
            print(f"    [OK] Remapped to existing: {existing}")
            brand_fixed += 1
            continue

    # Create SVG logo
    color = BRAND_COLORS.get(name, '#29624E')
    safe_name = name.lower().replace(' ', '-').replace('(', '').replace(')', '')
    svg_path = f"brands/{safe_name}-logo.svg"
    if create_brand_svg(name, svg_path, color):
        brand.logo = svg_path
        brand.save(update_fields=['logo'])
        brand_fixed += 1

print(f"\n  ✓ Fixed {brand_fixed} brand logos")


# ══════════════════════════════════════════════════════════════════════════
# STEP 3: Fix News Images
# ══════════════════════════════════════════════════════════════════════════
print("\n[3/4] Fixing news images...")

# Map news to existing images or download new ones
NEWS_IMAGE_MAP = {
    # Use existing project/product images for relevant news
}

news_fixed = 0
news_with_placeholder = News.objects.filter(image='news/placeholder.jpg')
print(f"  Found {news_with_placeholder.count()} news with placeholder images")

for article in news_with_placeholder:
    title = article.title_en or article.title or ''
    print(f"\n  News: {title[:50]}")

    # Try to find a relevant existing image based on title keywords
    if 'transformer' in title.lower():
        # Use transformer project image
        existing = 'projects/tr-az-1600-main.jpg'
        img_name = 'news/transformer-delivery.jpg'
    elif 'generator' in title.lower():
        existing = 'projects/gen-uz-main.jpg'
        img_name = 'news/generator-delivery.jpg'
    elif 'portfolio' in title.lower() or 'expand' in title.lower():
        existing = 'about/company-about.jpg'
        img_name = 'news/portfolio-expansion.jpg'
    else:
        existing = None
        img_name = None

    if existing:
        existing_path = os.path.join(MEDIA_ROOT, existing)
        target_path = os.path.join(MEDIA_ROOT, img_name)
        if os.path.exists(existing_path):
            # Copy the file to news directory
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            if not os.path.exists(target_path):
                import shutil
                shutil.copy2(existing_path, target_path)
            article.image = img_name
            article.save(update_fields=['image'])
            print(f"    [OK] Copied from: {existing} -> {img_name}")
            news_fixed += 1
            continue

    # Fallback: create with Pillow
    safe_title = title[:30].lower().replace(' ', '-').replace('–', '-')
    filename = f"news/{safe_title}.jpg"
    if create_product_image_pillow(title[:50], filename, (30, 60, 90)):
        article.image = filename
        article.save(update_fields=['image'])
        news_fixed += 1

print(f"\n  ✓ Fixed {news_fixed} news images")


# ══════════════════════════════════════════════════════════════════════════
# STEP 4: Fix Testimonial photos (if any are broken)
# ══════════════════════════════════════════════════════════════════════════
print("\n[4/4] Checking testimonials...")

testimonial_fixed = 0
for t in Testimonial.objects.all():
    name = t.name
    if t.photo and not os.path.exists(os.path.join(MEDIA_ROOT, str(t.photo))):
        print(f"  Testimonial: {name} - photo MISSING: {t.photo}")
        # Clear broken photo reference
        t.photo = ''
        t.save(update_fields=['photo'])
        testimonial_fixed += 1
    elif not t.photo:
        pass  # Empty is OK, templates handle it
    else:
        pass  # File exists

if testimonial_fixed:
    print(f"  ✓ Cleared {testimonial_fixed} broken testimonial photos")
else:
    print("  ✓ No broken testimonial photos")


# ══════════════════════════════════════════════════════════════════════════
# STEP 5: Verify hero slides
# ══════════════════════════════════════════════════════════════════════════
print("\n[BONUS] Checking hero slides...")
for h in HeroSlide.objects.all():
    if h.image:
        path = os.path.join(MEDIA_ROOT, str(h.image))
        if not os.path.exists(path):
            print(f"  WARNING: HeroSlide[{h.id}] image missing: {h.image}")

# ══════════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("  FIX SUMMARY")
print("=" * 70)
print(f"  Products fixed:     {product_fixed}")
print(f"  Brands fixed:       {brand_fixed}")
print(f"  News fixed:         {news_fixed}")
print(f"  Testimonials fixed: {testimonial_fixed}")
print("=" * 70)

# Verify remaining issues
remaining = 0
for p in Product.objects.all():
    if p.image and not os.path.exists(os.path.join(MEDIA_ROOT, str(p.image))):
        remaining += 1
        print(f"  STILL MISSING: Product[{p.id}] {p.image}")

for b in Brand.objects.all():
    if b.logo and not os.path.exists(os.path.join(MEDIA_ROOT, str(b.logo))):
        remaining += 1
        print(f"  STILL MISSING: Brand[{b.id}] {b.logo}")

for n in News.objects.all():
    if n.image and not os.path.exists(os.path.join(MEDIA_ROOT, str(n.image))):
        remaining += 1
        print(f"  STILL MISSING: News[{n.id}] {n.image}")

if remaining:
    print(f"\n  ⚠ {remaining} images still missing!")
else:
    print(f"\n  ✓ All images verified - no missing files!")
