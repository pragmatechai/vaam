"""
Seed script: 3 new hero slides
- Slide 1: Solar energy / general sourcing theme
- Slide 2: Diesel generator → links to product detail page
- Slide 3: Completed power project → links to a newly created project
Usage: python manage.py shell < seed_hero_slides.py
  OR:  python seed_hero_slides.py (run via manage.py shell -c "exec(open('seed_hero_slides.py').read())")
"""
import os, sys, django, requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()

from django.core.files.base import ContentFile
from core.models import HeroSlide, Product, Project, ProjectCategory

MEDIA_HERO = BASE_DIR / 'media' / 'hero'
MEDIA_PROJECTS = BASE_DIR / 'media' / 'projects'
MEDIA_HERO.mkdir(parents=True, exist_ok=True)
MEDIA_PROJECTS.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# Helper: download image from Unsplash
# ------------------------------------------------------------------
def download_image(url: str, filename: str, dest_dir: Path) -> str:
    """Download an image and return its relative path (e.g. 'hero/filename.jpg')."""
    dest = dest_dir / filename
    if dest.exists():
        print(f"  [SKIP] {filename} already exists")
    else:
        print(f"  [DL]   Downloading {filename} from Unsplash...")
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; VaamBot/1.0)'}
        r = requests.get(url, headers=headers, timeout=60, stream=True)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  [OK]   {filename} saved ({dest.stat().st_size // 1024} KB)")
    return str(dest_dir.name) + '/' + filename   # e.g. 'hero/slide_solar.jpg'

# ------------------------------------------------------------------
# 1. Ensure a project exists to link from hero slide 3
# ------------------------------------------------------------------
print("\n=== 1. Creating Project (if not exists) ===")
cat, _ = ProjectCategory.objects.get_or_create(
    slug='energy-power',
    defaults={'name': 'Energy & Power', 'order': 1, 'is_active': True}
)
# Translations
for lang, val in [('en', 'Energy & Power'), ('ru', 'Энергетика и электроснабжение'),
                  ('tr', 'Enerji ve Güç'), ('ar', 'الطاقة والكهرباء')]:
    setattr(cat, f'name_{lang}', val)
cat.save()
print(f"  Category: {cat.name} (id={cat.id})")

# ----- Project -----
proj_slug = 'solar-power-plant-50mw-uzbekistan'
proj, proj_created = Project.objects.get_or_create(
    slug=proj_slug,
    defaults={
        'category': cat,
        'title': '50 MW Solar Power Plant – Uzbekistan',
        'short_description': 'End-to-end supply and commissioning of a 50 MW solar power plant '
                             'with monocrystalline panels sourced from leading Chinese manufacturers.',
        'description': (
            'VAAM Trading coordinated the full procurement cycle for a large-scale solar farm '
            'commissioned in 2025. We sourced 186 000 bifacial monocrystalline panels, '
            'central inverters and mounting structures directly from certified Chinese factories. '
            'Logistics, customs clearance, quality inspection and on-site commissioning '
            'support were all handled by our team.'
        ),
        'client': 'Uzbekenergo',
        'location': 'Navoi Region, Uzbekistan',
        'is_featured': True,
        'is_active': True,
        'order': 1,
    }
)
if not proj_created:
    print(f"  Project already exists: {proj.title}")
else:
    # Multi-language fields
    proj.title_en = '50 MW Solar Power Plant – Uzbekistan'
    proj.title_ru = '50 МВт Солнечная электростанция – Узбекистан'
    proj.title_tr = '50 MW Güneş Enerji Santrali – Özbekistan'
    proj.title_ar = 'محطة طاقة شمسية 50 ميغاواط – أوزبكستان'

    proj.short_description_en = (
        'End-to-end supply and commissioning of a 50 MW solar power plant '
        'with monocrystalline panels sourced from leading Chinese manufacturers.'
    )
    proj.short_description_ru = (
        'Полный цикл поставки и ввода в эксплуатацию солнечной электростанции мощностью 50 МВт '
        'с монокристаллическими панелями от ведущих китайских производителей.'
    )
    proj.short_description_tr = (
        'Önde gelen Çinli üreticilerden temin edilen monokristal panellerle '
        '50 MW güneş enerjisi santralinin uçtan uca temini ve devreye alınması.'
    )
    proj.short_description_ar = (
        'التوريد الشامل وتشغيل محطة طاقة شمسية بقدرة 50 ميغاواط '
        'بألواح أحادية البلورية من كبار المصنعين الصينيين.'
    )

    # Download project image
    proj_img_url = (
        'https://images.unsplash.com/photo-1509391366360-2e959784a276'
        '?w=1600&h=900&fit=crop&q=85&auto=format'
    )
    rel_path = download_image(proj_img_url, 'solar_plant_uzbekistan.jpg', MEDIA_PROJECTS)
    proj.image = rel_path
    proj.save()
    print(f"  Project created: {proj.title} (id={proj.id})")

proj_url = proj.get_absolute_url()
print(f"  Project URL: {proj_url}")

# ------------------------------------------------------------------
# 2. Pick a product to link to
# ------------------------------------------------------------------
product = Product.objects.filter(is_active=True, slug='generator-500-kva').first()
if not product:
    product = Product.objects.filter(is_active=True).order_by('order').first()
product_url = product.get_absolute_url() if product else '/products/'
print(f"\n=== 2. Product selected: {product.name if product else 'none'} => {product_url} ===")

# ------------------------------------------------------------------
# 3. Download hero images
# ------------------------------------------------------------------
print("\n=== 3. Downloading hero images ===")

HERO_IMAGES = [
    {
        'filename': 'hero_solar_energy.jpg',
        'url': (
            'https://images.unsplash.com/photo-1508514177221-188b1cf16e9d'
            '?w=1920&h=1080&fit=crop&q=85&auto=format'
        ),
    },
    {
        'filename': 'hero_diesel_generator.jpg',
        'url': (
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64'
            '?w=1920&h=1080&fit=crop&q=85&auto=format'
        ),
    },
    {
        'filename': 'hero_power_project.jpg',
        'url': (
            'https://images.unsplash.com/photo-1466611653911-95081537e5b7'
            '?w=1920&h=1080&fit=crop&q=85&auto=format'
        ),
    },
]

img_paths = []
for item in HERO_IMAGES:
    path = download_image(item['url'], item['filename'], MEDIA_HERO)
    img_paths.append(path)

# ------------------------------------------------------------------
# 4. Create 3 hero slides
# ------------------------------------------------------------------
print("\n=== 4. Creating Hero Slides ===")

# Determine next order value
max_order = HeroSlide.objects.order_by('-order').values_list('order', flat=True).first() or 0

SLIDES = [
    # --- Slide A: Solar energy / general sourcing ---
    {
        'order': max_order + 1,
        'image': img_paths[0],
        'title_en': 'Clean Energy Solutions from China',
        'title_ru': 'Решения в области чистой энергии из Китая',
        'title_tr': 'Çin\'den Temiz Enerji Çözümleri',
        'title_ar': 'حلول الطاقة النظيفة من الصين',
        'subtitle_en': 'Renewable & Industrial Power',
        'subtitle_ru': 'Возобновляемая и промышленная энергетика',
        'subtitle_tr': 'Yenilenebilir ve Endüstriyel Güç',
        'subtitle_ar': 'الطاقة المتجددة والصناعية',
        'description_en': 'We source and deliver solar panels, inverters, transformers and generators directly from certified Chinese factories — on time, on budget.',
        'description_ru': 'Мы поставляем солнечные панели, инверторы, трансформаторы и генераторы напрямую с сертифицированных китайских заводов — в срок и в рамках бюджета.',
        'description_tr': 'Güneş panellerini, invertörleri, transformatörleri ve jeneratörleri sertifikalı Çin fabrikalarından doğrudan temin ediyor ve teslim ediyoruz.',
        'description_ar': 'نقوم بتوريد الألواح الشمسية والمحولات والمولدات مباشرة من المصانع الصينية المعتمدة — في الوقت المحدد وضمن الميزانية.',
        'button1_text_en': 'Explore Products',
        'button1_text_ru': 'Смотреть продукты',
        'button1_text_tr': 'Ürünleri İncele',
        'button1_text_ar': 'استكشف المنتجات',
        'button1_url': '/en/products/',
        'button2_text_en': 'Request a Quote',
        'button2_text_ru': 'Запросить цену',
        'button2_text_tr': 'Teklif Al',
        'button2_text_ar': 'طلب عرض سعر',
        'button2_url': '/en/contact/',
    },
    # --- Slide B: Diesel generator → product detail ---
    {
        'order': max_order + 2,
        'image': img_paths[1],
        'title_en': '500 kVA Industrial Diesel Generator',
        'title_ru': '500 кВА Дизельный Генератор',
        'title_tr': '500 kVA Endüstriyel Dizel Jeneratör',
        'title_ar': 'مولد ديزل صناعي 500 كيلوفولت أمبير',
        'subtitle_en': 'Reliable Backup Power',
        'subtitle_ru': 'Надёжное резервное питание',
        'subtitle_tr': 'Güvenilir Yedek Güç',
        'subtitle_ar': 'طاقة احتيطية موثوقة',
        'description_en': 'High-performance diesel generators up to 2500 kVA — perfect for industrial facilities, hospitals, and data centers. Direct factory pricing from China.',
        'description_ru': 'Высокопроизводительные дизельные генераторы мощностью до 2500 кВА для промышленных объектов, больниц и дата-центров. Цены напрямую с завода.',
        'description_tr': '2500 kVA\'ya kadar yüksek performanslı dizel jeneratörler — endüstriyel tesisler, hastaneler ve veri merkezleri için ideal. Çin fabrikasından doğrudan fiyat.',
        'description_ar': 'مولدات ديزل عالية الأداء تصل إلى 2500 كيلوفولت أمبير — مثالية للمنشآت الصناعية والمستشفيات ومراكز البيانات. أسعار مباشرة من المصنع.',
        'button1_text_en': 'View Product',
        'button1_text_ru': 'Посмотреть продукт',
        'button1_text_tr': 'Ürünü İncele',
        'button1_text_ar': 'عرض المنتج',
        'button1_url': product_url,
        'button2_text_en': 'All Generators',
        'button2_text_ru': 'Все генераторы',
        'button2_text_tr': 'Tüm Jeneratörler',
        'button2_text_ar': 'جميع المولدات',
        'button2_url': '/en/products/',
    },
    # --- Slide C: Completed project ---
    {
        'order': max_order + 3,
        'image': img_paths[2],
        'title_en': '50 MW Solar Power Plant – Uzbekistan',
        'title_ru': '50 МВт СЭС – Узбекистан',
        'title_tr': '50 MW Güneş Santrali – Özbekistan',
        'title_ar': 'محطة شمسية 50 ميغاواط – أوزبكستان',
        'subtitle_en': 'Completed Project',
        'subtitle_ru': 'Завершённый проект',
        'subtitle_tr': 'Tamamlanan Proje',
        'subtitle_ar': 'مشروع مكتمل',
        'description_en': 'We sourced 186 000 bifacial solar panels and all associated equipment for a major solar farm in Uzbekistan — fully commissioned in 2025.',
        'description_ru': '186 000 бифациальных панелей и всё сопутствующее оборудование для крупной солнечной электростанции в Узбекистане — введено в эксплуатацию в 2025 году.',
        'description_tr': 'Özbekistan\'daki büyük bir güneş çiftliği için 186.000 çift yüzlü güneş paneli ve tüm ekipmanları temin ettik — 2025\'te devreye alındı.',
        'description_ar': 'قمنا بتوريد 186,000 لوح شمسي ثنائي الوجه وجميع المعدات المرتبطة لمحطة طاقة شمسية كبرى في أوزبكستان — تم تشغيلها كاملاً في 2025.',
        'button1_text_en': 'See Project Details',
        'button1_text_ru': 'Подробнее о проекте',
        'button1_text_tr': 'Proje Detayları',
        'button1_text_ar': 'تفاصيل المشروع',
        'button1_url': proj_url,
        'button2_text_en': 'All Projects',
        'button2_text_ru': 'Все проекты',
        'button2_text_tr': 'Tüm Projeler',
        'button2_text_ar': 'جميع المشاريع',
        'button2_url': '/en/projects/',
    },
]

for slide_data in SLIDES:
    slug_title = slide_data['title_en']
    existing = HeroSlide.objects.filter(title_en=slug_title).first()
    if existing:
        print(f"  [SKIP] Slide already exists: {slug_title}")
        continue

    slide = HeroSlide(
        order=slide_data['order'],
        is_active=True,
        button1_url=slide_data['button1_url'],
        button2_url=slide_data['button2_url'],
    )
    # Set image path (relative to MEDIA_ROOT)
    slide.image = slide_data['image']

    # Multilingual fields
    for lang in ['en', 'ru', 'tr', 'ar']:
        for field in ['title', 'subtitle', 'description', 'button1_text', 'button2_text']:
            key = f'{field}_{lang}'
            if key in slide_data:
                setattr(slide, key, slide_data[key])

    slide.save()
    print(f"  [OK]  Slide created: {slide.title} (id={slide.id}, order={slide.order})")

print("\n=== DONE ===")
print(f"Total hero slides: {HeroSlide.objects.count()}")
