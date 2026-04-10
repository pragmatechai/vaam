"""
VAAM Production Database Update Script
=======================================
Removes old solar-specific data and replaces with correct diverse trading products.
Keeps: Generators, Distribution Transformers, Client Data, Real Projects.
Updates: Products (all categories), Services, Testimonials, Brands, News.

Run on production:
  cd /home/vaam/app && source venv/bin/activate
  python seed_update_production.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()

from django.utils import timezone
from core.models import (
    ProductCategory, Product, ProductSpecification,
    ServiceCategory, Service,
    Testimonial, Brand,
    NewsCategory, News,
    ProjectCategory, Project,
)

print("=" * 80)
print("  VAAM Production Database Update")
print("  Replacing solar-specific content with correct trading products")
print("=" * 80)


# ════════════════════════════════════════════════════════════════════════════════
# STEP 1: Clean up old solar-specific products (keep generators & transformers)
# ════════════════════════════════════════════════════════════════════════════════
print("\n[1/6] Cleaning old solar-specific products...")

# Slugs from the old seed_data.py that must be removed
OLD_PRODUCT_SLUGS = [
    'longi-hi-mo-6-explorer-580w', 'ja-solar-deepblue-4-pro-555w',
    'trina-solar-vertex-s-plus-445w', 'canadian-solar-hiku7-600w',
    'huawei-sun2000-10ktl-m1', 'sma-sunny-tripower-15000tl',
    'growatt-min-6000tl-xh', 'clenergy-pv-ezrack-solarroof-pro',
    'k2-systems-d-dome-ground-mount', 'huawei-luna2000-15-s0',
    'solar-dc-cable-6mm-100m', 'huawei-smart-dongle-wlan',
]
deleted_count = Product.objects.filter(slug__in=OLD_PRODUCT_SLUGS).delete()[0]
print(f"   ✓ Deleted {deleted_count} old solar-specific products")

# Remove old solar-only categories that are no longer used
OLD_CATEGORY_SLUGS = [
    'solar-inverters', 'mounting-systems', 'energy-storage',
    'solar-cables-connectors', 'monitoring-systems',
]
for slug in OLD_CATEGORY_SLUGS:
    cat = ProductCategory.objects.filter(slug=slug).first()
    if cat:
        cat.products.all().delete()
        cat.delete()
        print(f"   ✓ Deleted old category: {slug}")

# Remove old solar project categories and projects
OLD_PROJECT_CAT_SLUGS = ['residential', 'commercial', 'industrial', 'solar-farm']
for slug in OLD_PROJECT_CAT_SLUGS:
    pc = ProjectCategory.objects.filter(slug=slug).first()
    if pc:
        pc.projects.all().delete()
        pc.delete()
        print(f"   ✓ Deleted old project category: {slug}")

# Delete individual old solar projects by slug
OLD_PROJECT_SLUGS = [
    'villa-solar-mardakan', 'apartment-complex-yasamal',
    'office-tower-port-baku', 'ganjlik-mall-rooftop',
    'factory-solar-sumgait', 'warehouse-solar-kesla',
    'absheron-solar-farm', 'gobustan-pilot-solar',
]
del_projects = Project.objects.filter(slug__in=OLD_PROJECT_SLUGS).delete()[0]
if del_projects:
    print(f"   ✓ Deleted {del_projects} old solar projects")


# ════════════════════════════════════════════════════════════════════════════════
# STEP 2: Ensure correct product categories exist
# ════════════════════════════════════════════════════════════════════════════════
print("\n[2/6] Ensuring product categories...")

CATEGORIES = {
    "solar-panels": {
        "name_en": "Solar Energy Systems", "name_ru": "Системы солнечной энергии",
        "name_tr": "Güneş Enerjisi Sistemleri", "name_ar": "أنظمة الطاقة الشمسية",
        "description_en": "Solar panels, inverters and complete photovoltaic systems sourced from leading manufacturers.",
        "description_ru": "Солнечные панели, инверторы и полные фотовольтаические системы от ведущих производителей.",
        "description_tr": "Lider üreticilerden tedarik edilen güneş panelleri, invertörler ve komple fotovoltaik sistemler.",
        "description_ar": "ألواح شمسية ومحولات وأنظمة كهروضوئية كاملة من الشركات المصنعة الرائدة.",
        "icon": "fas fa-solar-panel", "order": 1,
    },
    "street-garden-lighting": {
        "name_en": "Street & Garden Lighting", "name_ru": "Уличное и садовое освещение",
        "name_tr": "Sokak ve Bahçe Aydınlatması", "name_ar": "إضاءة الشوارع والحدائق",
        "description_en": "Energy-efficient LED street lights, garden lamps and smart outdoor lighting systems.",
        "description_ru": "Энергоэффективные LED уличные фонари, садовые лампы и системы умного наружного освещения.",
        "description_tr": "Enerji verimli LED sokak lambaları, bahçe aydınlatmaları ve akıllı dış mekan aydınlatma sistemleri.",
        "description_ar": "مصابيح شوارع LED موفرة للطاقة ومصابيح حدائق وأنظمة إضاءة خارجية ذكية.",
        "icon": "fas fa-lightbulb", "order": 2,
    },
    "security-cameras": {
        "name_en": "Security Cameras", "name_ru": "Камеры безопасности",
        "name_tr": "Güvenlik Kameraları", "name_ar": "كاميرات الأمن",
        "description_en": "IP cameras, CCTV systems, NVR recorders and complete surveillance solutions.",
        "description_ru": "IP-камеры, системы видеонаблюдения, NVR-рекордеры и комплексные решения безопасности.",
        "description_tr": "IP kameralar, CCTV sistemleri, NVR kayıt cihazları ve komple güvenlik çözümleri.",
        "description_ar": "كاميرات IP وأنظمة CCTV ومسجلات NVR وحلول مراقبة كاملة.",
        "icon": "fas fa-video", "order": 3,
    },
    "automobiles": {
        "name_en": "Automobiles", "name_ru": "Автомобили",
        "name_tr": "Otomobiller", "name_ar": "السيارات",
        "description_en": "New and pre-owned vehicles, spare parts and automotive accessories from Chinese manufacturers.",
        "description_ru": "Новые и б/у автомобили, запасные части и автоаксессуары от китайских производителей.",
        "description_tr": "Çinli üreticilerden yeni ve ikinci el araçlar, yedek parçalar ve otomobil aksesuarları.",
        "description_ar": "سيارات جديدة ومستعملة وقطع غيار وإكسسوارات سيارات من الشركات المصنعة الصينية.",
        "icon": "fas fa-car", "order": 4,
    },
    "construction-materials": {
        "name_en": "Construction Materials", "name_ru": "Строительные материалы",
        "name_tr": "İnşaat Malzemeleri", "name_ar": "مواد البناء",
        "description_en": "Steel products, cement, pipes, fittings and building materials for construction projects.",
        "description_ru": "Стальные изделия, цемент, трубы, фитинги и стройматериалы для строительных проектов.",
        "description_tr": "İnşaat projeleri için çelik ürünler, çimento, borular, bağlantı elemanları ve yapı malzemeleri.",
        "description_ar": "منتجات فولاذية وأسمنت وأنابيب وتجهيزات ومواد بناء لمشاريع التعمير.",
        "icon": "fas fa-hammer", "order": 5,
    },
    "industrial-products": {
        "name_en": "Industrial Products", "name_ru": "Промышленные товары",
        "name_tr": "Endüstriyel Ürünler", "name_ar": "المنتجات الصناعية",
        "description_en": "Industrial equipment, tools, machinery and factory supplies for various sectors.",
        "description_ru": "Промышленное оборудование, инструменты, станки и фабричные материалы для различных секторов.",
        "description_tr": "Çeşitli sektörler için endüstriyel ekipman, aletler, makineler ve fabrika malzemeleri.",
        "description_ar": "معدات صناعية وأدوات وآلات ومستلزمات مصانع لقطاعات مختلفة.",
        "icon": "fas fa-industry", "order": 6,
    },
    "generators": {
        "name_en": "Generators", "name_ru": "Генераторы",
        "name_tr": "Jeneratörler", "name_ar": "المولدات",
        "description_en": "Diesel generator sets from 50 kVA to 500 kVA for residential, commercial and industrial use.",
        "description_ru": "Дизельные генераторные установки мощностью от 50 до 500 кВА для жилых, коммерческих и промышленных объектов.",
        "description_tr": "Konut, ticari ve endüstriyel kullanım için 50 kVA'dan 500 kVA'ya kadar dizel jeneratör grupları.",
        "description_ar": "مجموعات مولدات ديزل من 50 إلى 500 كيلو فولت أمبير للاستخدام السكني والتجاري والصناعي.",
        "icon": "fas fa-bolt", "order": 7,
    },
    "distribution-transformers": {
        "name_en": "Distribution Transformers", "name_ru": "Распределительные трансформаторы",
        "name_tr": "Dağıtım Transformatörleri", "name_ar": "محولات التوزيع",
        "description_en": "S11-series oil-immersed distribution transformers 35/0.4 kV in aluminium and copper winding.",
        "description_ru": "Масляные распределительные трансформаторы серии S11 35/0.4 кВ с алюминиевой и медной обмоткой.",
        "description_tr": "S11 serisi yağ soğutmalı 35/0.4 kV dağıtım transformatörleri, alüminyum ve bakır sargılı.",
        "description_ar": "محولات توزيع مغمورة بالزيت S11 بنسبة 35/0.4 كيلو فولت بأسلاك الألومنيوم والنحاس.",
        "icon": "fas fa-broadcast-tower", "order": 8,
    },
}

for slug, data in CATEGORIES.items():
    cat, created = ProductCategory.objects.get_or_create(slug=slug, defaults={"order": data["order"]})
    for key, val in data.items():
        setattr(cat, key, val)
    cat.is_active = True
    cat.save()
    print(f"   {'✓ Created' if created else '↻ Updated'} category: {data['name_en']}")


# ════════════════════════════════════════════════════════════════════════════════
# STEP 3: Add products for each category (skip generators/transformers - already exist)
# ════════════════════════════════════════════════════════════════════════════════
print("\n[3/6] Adding products for all categories...")

def upsert_product(slug, category_slug, fields, specs):
    """Create or update a product and its specifications."""
    category = ProductCategory.objects.get(slug=category_slug)
    try:
        p = Product.objects.get(slug=slug)
        for k, v in fields.items():
            setattr(p, k, v)
        p.category = category
        p.save()
        action = "updated"
    except Product.DoesNotExist:
        p = Product.objects.create(slug=slug, category=category, image="products/placeholder.jpg", **fields)
        action = "created"

    p.specifications.all().delete()
    for i, spec in enumerate(specs):
        ProductSpecification.objects.create(product=p, order=i, **spec)
    print(f"   {'✓' if action == 'created' else '↻'} {fields.get('name_en', slug)} — {action}")
    return p


# ── Solar Energy Systems ──────────────────────────────────────────────────────

solar_desc = """<p>VAAM Import and Export Trading Co., LTD sources and supplies high-efficiency solar panels from leading Chinese manufacturers. We provide complete photovoltaic solutions including panels, inverters and mounting systems for residential, commercial and industrial applications.</p>
<p><strong>Our Solar Supply Service:</strong></p>
<ul>
<li>Product sourcing from verified manufacturers</li>
<li>Quality inspection before shipment</li>
<li>International logistics and customs clearance</li>
<li>Technical documentation and certificates</li>
<li>After-sales support</li>
</ul>"""

solar_desc_ru = """<p>VAAM Import and Export Trading Co., LTD поставляет высокоэффективные солнечные панели от ведущих китайских производителей. Мы предоставляем полные фотовольтаические решения, включая панели, инверторы и системы крепления для жилых, коммерческих и промышленных объектов.</p>"""
solar_desc_tr = """<p>VAAM Import and Export Trading Co., LTD, lider Çinli üreticilerden yüksek verimli güneş panelleri tedarik etmektedir. Konut, ticari ve endüstriyel uygulamalar için paneller, invertörler ve montaj sistemleri dahil komple fotovoltaik çözümler sunuyoruz.</p>"""
solar_desc_ar = """<p>تورد شركة VAAM للاستيراد والتصدير ألواحاً شمسية عالية الكفاءة من الشركات المصنعة الصينية الرائدة. نقدم حلولاً كهروضوئية كاملة تشمل الألواح والمحولات وأنظمة التركيب للتطبيقات السكنية والتجارية والصناعية.</p>"""

solar_products = [
    {
        "slug": "monocrystalline-solar-panel-550w",
        "fields": {
            "name_en": "550W Monocrystalline Solar Panel",
            "name_ru": "Монокристаллическая солнечная панель 550 Вт",
            "name_tr": "550W Monokristal Güneş Paneli",
            "name_ar": "لوح شمسي أحادي البلورة 550 واط",
            "short_description_en": "High-efficiency 550W monocrystalline solar panel for residential and commercial applications. Sourced from Tier-1 Chinese manufacturers.",
            "short_description_ru": "Высокоэффективная солнечная панель 550 Вт для жилого и коммерческого использования. От ведущих китайских производителей.",
            "short_description_tr": "Konut ve ticari uygulamalar için yüksek verimli 550W monokristal güneş paneli. Tier-1 Çinli üreticilerden tedarik.",
            "short_description_ar": "لوح شمسي أحادي البلورة عالي الكفاءة 550 واط للتطبيقات السكنية والتجارية.",
            "description_en": solar_desc, "description_ru": solar_desc_ru, "description_tr": solar_desc_tr, "description_ar": solar_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 1,
        },
        "specs": [
            {"key_en": "Power Output", "key_ru": "Мощность", "key_tr": "Güç Çıkışı", "key_ar": "القدرة", "value_en": "550W", "value_ru": "550 Вт", "value_tr": "550W", "value_ar": "550 واط"},
            {"key_en": "Cell Type", "key_ru": "Тип ячейки", "key_tr": "Hücre Tipi", "key_ar": "نوع الخلية", "value_en": "Monocrystalline PERC", "value_ru": "Монокристалл PERC", "value_tr": "Monokristal PERC", "value_ar": "أحادي البلورة PERC"},
            {"key_en": "Efficiency", "key_ru": "Эффективность", "key_tr": "Verimlilik", "key_ar": "الكفاءة", "value_en": "21.5%+", "value_ru": "21.5%+", "value_tr": "21.5%+", "value_ar": "+21.5%"},
            {"key_en": "Warranty", "key_ru": "Гарантия", "key_tr": "Garanti", "key_ar": "الضمان", "value_en": "25 years product / 30 years performance", "value_ru": "25 лет на продукт / 30 лет производительность", "value_tr": "25 yıl ürün / 30 yıl performans", "value_ar": "25 سنة منتج / 30 سنة أداء"},
            {"key_en": "Application", "key_ru": "Применение", "key_tr": "Uygulama", "key_ar": "التطبيق", "value_en": "Residential / Commercial / Industrial", "value_ru": "Жилые / Коммерческие / Промышленные", "value_tr": "Konut / Ticari / Endüstriyel", "value_ar": "سكني / تجاري / صناعي"},
            {"key_en": "Supply Origin", "key_ru": "Источник поставки", "key_tr": "Tedarik Kaynağı", "key_ar": "مصدر التوريد", "value_en": "China (Tier-1 Manufacturers)", "value_ru": "Китай (поставщики 1-го уровня)", "value_tr": "Çin (Tier-1 Üreticiler)", "value_ar": "الصين (مصنعون من المستوى الأول)"},
        ],
    },
    {
        "slug": "solar-inverter-10kw-hybrid",
        "fields": {
            "name_en": "10kW Hybrid Solar Inverter",
            "name_ru": "Гибридный солнечный инвертор 10 кВт",
            "name_tr": "10kW Hibrit Güneş İnvertörü",
            "name_ar": "محول شمسي هجين 10 كيلو واط",
            "short_description_en": "10kW hybrid solar inverter with battery support, suitable for residential and small commercial systems.",
            "short_description_ru": "Гибридный солнечный инвертор 10 кВт с поддержкой батарей для жилых и небольших коммерческих систем.",
            "short_description_tr": "Konut ve küçük ticari sistemler için batarya destekli 10kW hibrit güneş invertörü.",
            "short_description_ar": "محول شمسي هجين 10 كيلو واط مع دعم البطارية للأنظمة السكنية والتجارية الصغيرة.",
            "description_en": solar_desc, "description_ru": solar_desc_ru, "description_tr": solar_desc_tr, "description_ar": solar_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 2,
        },
        "specs": [
            {"key_en": "Power", "key_ru": "Мощность", "key_tr": "Güç", "key_ar": "القدرة", "value_en": "10 kW", "value_ru": "10 кВт", "value_tr": "10 kW", "value_ar": "10 كيلو واط"},
            {"key_en": "Type", "key_ru": "Тип", "key_tr": "Tip", "key_ar": "النوع", "value_en": "Hybrid (Grid-tied + Battery)", "value_ru": "Гибридный (сетевой + аккумулятор)", "value_tr": "Hibrit (Şebeke + Batarya)", "value_ar": "هجين (متصل بالشبكة + بطارية)"},
            {"key_en": "Efficiency", "key_ru": "КПД", "key_tr": "Verimlilik", "key_ar": "الكفاءة", "value_en": "98.5%+", "value_ru": "98.5%+", "value_tr": "98.5%+", "value_ar": "+98.5%"},
            {"key_en": "Protection", "key_ru": "Защита", "key_tr": "Koruma", "key_ar": "الحماية", "value_en": "IP65", "value_ru": "IP65", "value_tr": "IP65", "value_ar": "IP65"},
            {"key_en": "Supply Origin", "key_ru": "Источник поставки", "key_tr": "Tedarik Kaynağı", "key_ar": "مصدر التوريد", "value_en": "China", "value_ru": "Китай", "value_tr": "Çin", "value_ar": "الصين"},
        ],
    },
    {
        "slug": "solar-mounting-system-rooftop",
        "fields": {
            "name_en": "Aluminum Rooftop Mounting System",
            "name_ru": "Алюминиевая система крепления на крышу",
            "name_tr": "Alüminyum Çatı Montaj Sistemi",
            "name_ar": "نظام تركيب على السطح من الألومنيوم",
            "short_description_en": "Durable aluminum mounting system for rooftop solar installations. Compatible with various panel sizes.",
            "short_description_ru": "Прочная алюминиевая система крепления для установки солнечных панелей на крыше.",
            "short_description_tr": "Çatı güneş paneli tesisatları için dayanıklı alüminyum montaj sistemi.",
            "short_description_ar": "نظام تركيب من الألومنيوم المتين لتركيبات الألواح الشمسية على السطح.",
            "description_en": solar_desc, "description_ru": solar_desc_ru, "description_tr": solar_desc_tr, "description_ar": solar_desc_ar,
            "price": "Contact for Price", "is_featured": False, "is_active": True, "order": 3,
        },
        "specs": [
            {"key_en": "Material", "key_ru": "Материал", "key_tr": "Malzeme", "key_ar": "المادة", "value_en": "Anodized Aluminum", "value_ru": "Анодированный алюминий", "value_tr": "Anodize Alüminyum", "value_ar": "ألومنيوم مؤنود"},
            {"key_en": "Wind Resistance", "key_ru": "Ветровая нагрузка", "key_tr": "Rüzgar Dayanımı", "key_ar": "مقاومة الرياح", "value_en": "Up to 60 m/s", "value_ru": "До 60 м/с", "value_tr": "60 m/s'ye kadar", "value_ar": "حتى 60 م/ث"},
            {"key_en": "Warranty", "key_ru": "Гарантия", "key_tr": "Garanti", "key_ar": "الضمان", "value_en": "15 years", "value_ru": "15 лет", "value_tr": "15 yıl", "value_ar": "15 سنة"},
            {"key_en": "Supply Origin", "key_ru": "Источник поставки", "key_tr": "Tedarik Kaynağı", "key_ar": "مصدر التوريد", "value_en": "China", "value_ru": "Китай", "value_tr": "Çin", "value_ar": "الصين"},
        ],
    },
]

for prod in solar_products:
    upsert_product(prod["slug"], "solar-panels", prod["fields"], prod["specs"])


# ── Street & Garden Lighting ──────────────────────────────────────────────────

lighting_desc = """<p>VAAM supplies energy-efficient LED lighting products for streets, parks, gardens and public areas. Our products are sourced from certified Chinese manufacturers and meet international quality standards.</p>
<p><strong>Features:</strong></p>
<ul>
<li>High luminous efficiency (150+ lm/W)</li>
<li>IP65/IP66 waterproof protection</li>
<li>Long lifespan (50,000+ hours)</li>
<li>Available in solar-powered and grid-powered models</li>
</ul>"""
lighting_desc_ru = """<p>VAAM поставляет энергоэффективные LED-осветительные продукты для улиц, парков, садов и общественных территорий. Наша продукция от сертифицированных китайских производителей.</p>"""
lighting_desc_tr = """<p>VAAM, sokaklar, parklar, bahçeler ve kamusal alanlar için enerji verimli LED aydınlatma ürünleri tedarik etmektedir. Ürünlerimiz sertifikalı Çinli üreticilerden temin edilmektedir.</p>"""
lighting_desc_ar = """<p>توفر VAAM منتجات إضاءة LED موفرة للطاقة للشوارع والحدائق والمناطق العامة. منتجاتنا من مصنعين صينيين معتمدين.</p>"""

lighting_products = [
    {
        "slug": "led-street-light-150w",
        "fields": {
            "name_en": "150W LED Street Light", "name_ru": "Светодиодный уличный фонарь 150 Вт",
            "name_tr": "150W LED Sokak Lambası", "name_ar": "مصباح شارع LED 150 واط",
            "short_description_en": "High-efficiency 150W LED street light with IP66 waterproof rating. Suitable for main roads and highways.",
            "short_description_ru": "Высокоэффективный LED уличный фонарь 150 Вт с защитой IP66 для магистральных дорог.",
            "short_description_tr": "IP66 su geçirmez korumaya sahip yüksek verimli 150W LED sokak lambası. Ana yollar için uygun.",
            "short_description_ar": "مصباح شارع LED عالي الكفاءة 150 واط بتصنيف IP66 مقاوم للماء. مناسب للطرق الرئيسية.",
            "description_en": lighting_desc, "description_ru": lighting_desc_ru, "description_tr": lighting_desc_tr, "description_ar": lighting_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 1,
        },
        "specs": [
            {"key_en": "Power", "key_ru": "Мощность", "key_tr": "Güç", "key_ar": "القدرة", "value_en": "150W", "value_ru": "150 Вт", "value_tr": "150W", "value_ar": "150 واط"},
            {"key_en": "Luminous Flux", "key_ru": "Световой поток", "key_tr": "Işık Akısı", "key_ar": "التدفق الضوئي", "value_en": "22,500 lm", "value_ru": "22 500 лм", "value_tr": "22.500 lm", "value_ar": "22,500 لومن"},
            {"key_en": "Protection", "key_ru": "Защита", "key_tr": "Koruma", "key_ar": "الحماية", "value_en": "IP66", "value_ru": "IP66", "value_tr": "IP66", "value_ar": "IP66"},
            {"key_en": "Lifespan", "key_ru": "Срок службы", "key_tr": "Ömür", "key_ar": "العمر الافتراضي", "value_en": "50,000 hours", "value_ru": "50 000 часов", "value_tr": "50.000 saat", "value_ar": "50,000 ساعة"},
            {"key_en": "Color Temperature", "key_ru": "Цветовая температура", "key_tr": "Renk Sıcaklığı", "key_ar": "درجة حرارة اللون", "value_en": "5000K / 6000K", "value_ru": "5000К / 6000К", "value_tr": "5000K / 6000K", "value_ar": "5000K / 6000K"},
        ],
    },
    {
        "slug": "solar-garden-light-60w",
        "fields": {
            "name_en": "60W Solar Garden Light", "name_ru": "Солнечный садовый фонарь 60 Вт",
            "name_tr": "60W Solar Bahçe Lambası", "name_ar": "مصباح حديقة شمسي 60 واط",
            "short_description_en": "All-in-one solar garden light with integrated panel and battery. No wiring needed.",
            "short_description_ru": "Автономный солнечный садовый фонарь со встроенной панелью и аккумулятором. Без проводов.",
            "short_description_tr": "Entegre panel ve bataryalı hepsi bir arada solar bahçe lambası. Kablo gerektirmez.",
            "short_description_ar": "مصباح حديقة شمسي متكامل مع لوح وبطارية مدمجة. بدون أسلاك.",
            "description_en": lighting_desc, "description_ru": lighting_desc_ru, "description_tr": lighting_desc_tr, "description_ar": lighting_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 2,
        },
        "specs": [
            {"key_en": "Power", "key_ru": "Мощность", "key_tr": "Güç", "key_ar": "القدرة", "value_en": "60W LED", "value_ru": "60 Вт LED", "value_tr": "60W LED", "value_ar": "60 واط LED"},
            {"key_en": "Solar Panel", "key_ru": "Солнечная панель", "key_tr": "Güneş Paneli", "key_ar": "اللوح الشمسي", "value_en": "25W Monocrystalline", "value_ru": "25 Вт моно", "value_tr": "25W Monokristal", "value_ar": "25 واط أحادي البلورة"},
            {"key_en": "Battery", "key_ru": "Аккумулятор", "key_tr": "Batarya", "key_ar": "البطارية", "value_en": "LiFePO4 25.6V 18Ah", "value_ru": "LiFePO4 25.6В 18Ач", "value_tr": "LiFePO4 25.6V 18Ah", "value_ar": "LiFePO4 25.6V 18Ah"},
            {"key_en": "Working Hours", "key_ru": "Время работы", "key_tr": "Çalışma Süresi", "key_ar": "ساعات العمل", "value_en": "12-14 hours (full charge)", "value_ru": "12-14 часов", "value_tr": "12-14 saat", "value_ar": "12-14 ساعة"},
            {"key_en": "Protection", "key_ru": "Защита", "key_tr": "Koruma", "key_ar": "الحماية", "value_en": "IP65", "value_ru": "IP65", "value_tr": "IP65", "value_ar": "IP65"},
        ],
    },
]

for prod in lighting_products:
    upsert_product(prod["slug"], "street-garden-lighting", prod["fields"], prod["specs"])


# ── Security Cameras ──────────────────────────────────────────────────────────

camera_desc = """<p>VAAM supplies professional security and surveillance equipment from leading Chinese manufacturers. Our products include IP cameras, PTZ cameras, NVR systems and complete CCTV solutions suitable for residential, commercial and public applications.</p>"""
camera_desc_ru = """<p>VAAM поставляет профессиональное оборудование для безопасности и видеонаблюдения от ведущих китайских производителей.</p>"""
camera_desc_tr = """<p>VAAM, lider Çinli üreticilerden profesyonel güvenlik ve gözetim ekipmanları tedarik etmektedir.</p>"""
camera_desc_ar = """<p>توفر VAAM معدات أمن ومراقبة احترافية من الشركات المصنعة الصينية الرائدة.</p>"""

camera_products = [
    {
        "slug": "ip-camera-4mp-poe",
        "fields": {
            "name_en": "4MP PoE IP Camera", "name_ru": "IP-камера 4 Мп PoE",
            "name_tr": "4MP PoE IP Kamera", "name_ar": "كاميرا IP بدقة 4 ميجابكسل PoE",
            "short_description_en": "4MP PoE IP dome camera with night vision and motion detection. Ideal for indoor and outdoor surveillance.",
            "short_description_ru": "Купольная IP-камера 4 Мп PoE с ночным видением и датчиком движения.",
            "short_description_tr": "Gece görüşü ve hareket algılama özellikli 4MP PoE IP dome kamera.",
            "short_description_ar": "كاميرا IP قبة 4 ميجابكسل PoE مع رؤية ليلية وكشف الحركة.",
            "description_en": camera_desc, "description_ru": camera_desc_ru, "description_tr": camera_desc_tr, "description_ar": camera_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 1,
        },
        "specs": [
            {"key_en": "Resolution", "key_ru": "Разрешение", "key_tr": "Çözünürlük", "key_ar": "الدقة", "value_en": "4MP (2560×1440)", "value_ru": "4 Мп (2560×1440)", "value_tr": "4MP (2560×1440)", "value_ar": "4 ميجابكسل (2560×1440)"},
            {"key_en": "Night Vision", "key_ru": "Ночное видение", "key_tr": "Gece Görüşü", "key_ar": "الرؤية الليلية", "value_en": "30m IR", "value_ru": "30м ИК", "value_tr": "30m IR", "value_ar": "30 متر تحت الحمراء"},
            {"key_en": "Power", "key_ru": "Питание", "key_tr": "Güç", "key_ar": "الطاقة", "value_en": "PoE (IEEE 802.3af)", "value_ru": "PoE (IEEE 802.3af)", "value_tr": "PoE (IEEE 802.3af)", "value_ar": "PoE (IEEE 802.3af)"},
            {"key_en": "Protection", "key_ru": "Защита", "key_tr": "Koruma", "key_ar": "الحماية", "value_en": "IP67", "value_ru": "IP67", "value_tr": "IP67", "value_ar": "IP67"},
        ],
    },
    {
        "slug": "nvr-8ch-4k",
        "fields": {
            "name_en": "8-Channel 4K NVR System", "name_ru": "8-канальный 4K NVR видеорегистратор",
            "name_tr": "8 Kanal 4K NVR Sistemi", "name_ar": "نظام NVR 8 قنوات 4K",
            "short_description_en": "8-channel 4K network video recorder with PoE ports. Supports remote monitoring via mobile app.",
            "short_description_ru": "8-канальный 4K сетевой видеорегистратор с PoE портами. Удалённый мониторинг через приложение.",
            "short_description_tr": "PoE portlu 8 kanal 4K ağ video kaydedici. Mobil uygulama ile uzaktan izleme.",
            "short_description_ar": "مسجل فيديو شبكي 8 قنوات 4K مع منافذ PoE. يدعم المراقبة عن بُعد.",
            "description_en": camera_desc, "description_ru": camera_desc_ru, "description_tr": camera_desc_tr, "description_ar": camera_desc_ar,
            "price": "Contact for Price", "is_featured": False, "is_active": True, "order": 2,
        },
        "specs": [
            {"key_en": "Channels", "key_ru": "Каналы", "key_tr": "Kanal", "key_ar": "القنوات", "value_en": "8", "value_ru": "8", "value_tr": "8", "value_ar": "8"},
            {"key_en": "Resolution", "key_ru": "Разрешение", "key_tr": "Çözünürlük", "key_ar": "الدقة", "value_en": "4K (8MP)", "value_ru": "4K (8 Мп)", "value_tr": "4K (8MP)", "value_ar": "4K (8 ميجابكسل)"},
            {"key_en": "HDD", "key_ru": "HDD", "key_tr": "HDD", "key_ar": "القرص الصلب", "value_en": "Up to 8TB", "value_ru": "До 8 ТБ", "value_tr": "8TB'a kadar", "value_ar": "حتى 8 تيرابايت"},
            {"key_en": "PoE Ports", "key_ru": "PoE порты", "key_tr": "PoE Port", "key_ar": "منافذ PoE", "value_en": "8 × PoE+", "value_ru": "8 × PoE+", "value_tr": "8 × PoE+", "value_ar": "8 × PoE+"},
        ],
    },
]

for prod in camera_products:
    upsert_product(prod["slug"], "security-cameras", prod["fields"], prod["specs"])


# ── Automobiles ───────────────────────────────────────────────────────────────

auto_desc = """<p>VAAM provides automobile sourcing and export services from China. We help clients find the right vehicle — whether new or pre-owned — negotiate with dealers and handle all export logistics including documentation and shipping.</p>"""
auto_desc_ru = """<p>VAAM предоставляет услуги по поиску и экспорту автомобилей из Китая.</p>"""
auto_desc_tr = """<p>VAAM, Çin'den otomobil tedarik ve ihracat hizmetleri sunmaktadır.</p>"""
auto_desc_ar = """<p>توفر VAAM خدمات البحث عن السيارات وتصديرها من الصين.</p>"""

auto_products = [
    {
        "slug": "electric-vehicle-suv",
        "fields": {
            "name_en": "Electric SUV (Chinese Brand)", "name_ru": "Электрический внедорожник (китайский бренд)",
            "name_tr": "Elektrikli SUV (Çin Markası)", "name_ar": "سيارة SUV كهربائية (علامة صينية)",
            "short_description_en": "New electric SUV models from leading Chinese EV brands. Full export documentation and logistics support.",
            "short_description_ru": "Новые электрические внедорожники от ведущих китайских производителей EV.",
            "short_description_tr": "Lider Çinli EV markalarından yeni elektrikli SUV modelleri.",
            "short_description_ar": "موديلات سيارات SUV كهربائية جديدة من العلامات الصينية الرائدة.",
            "description_en": auto_desc, "description_ru": auto_desc_ru, "description_tr": auto_desc_tr, "description_ar": auto_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 1,
        },
        "specs": [
            {"key_en": "Type", "key_ru": "Тип", "key_tr": "Tip", "key_ar": "النوع", "value_en": "Electric SUV", "value_ru": "Электрический SUV", "value_tr": "Elektrikli SUV", "value_ar": "SUV كهربائي"},
            {"key_en": "Range", "key_ru": "Запас хода", "key_tr": "Menzil", "key_ar": "المدى", "value_en": "400-600 km (model dependent)", "value_ru": "400-600 км", "value_tr": "400-600 km", "value_ar": "400-600 كم"},
            {"key_en": "Brands", "key_ru": "Бренды", "key_tr": "Markalar", "key_ar": "العلامات", "value_en": "BYD, CHERY, GEELY, NIO", "value_ru": "BYD, CHERY, GEELY, NIO", "value_tr": "BYD, CHERY, GEELY, NIO", "value_ar": "BYD, CHERY, GEELY, NIO"},
            {"key_en": "Export Service", "key_ru": "Экспортный сервис", "key_tr": "İhracat Hizmeti", "key_ar": "خدمة التصدير", "value_en": "Full documentation + logistics", "value_ru": "Полная документация + логистика", "value_tr": "Tam dokümantasyon + lojistik", "value_ar": "توثيق كامل + لوجستيات"},
        ],
    },
    {
        "slug": "commercial-truck-light-duty",
        "fields": {
            "name_en": "Light-Duty Commercial Truck", "name_ru": "Лёгкий коммерческий грузовик",
            "name_tr": "Hafif Ticari Kamyon", "name_ar": "شاحنة تجارية خفيفة",
            "short_description_en": "Light-duty commercial trucks for logistics and distribution. Multiple brands and configurations available.",
            "short_description_ru": "Лёгкие коммерческие грузовики для логистики и дистрибуции.",
            "short_description_tr": "Lojistik ve dağıtım için hafif ticari kamyonlar.",
            "short_description_ar": "شاحنات تجارية خفيفة للوجستيات والتوزيع.",
            "description_en": auto_desc, "description_ru": auto_desc_ru, "description_tr": auto_desc_tr, "description_ar": auto_desc_ar,
            "price": "Contact for Price", "is_featured": False, "is_active": True, "order": 2,
        },
        "specs": [
            {"key_en": "Type", "key_ru": "Тип", "key_tr": "Tip", "key_ar": "النوع", "value_en": "Light-Duty Truck (2-5 ton)", "value_ru": "Лёгкий грузовик (2-5 тонн)", "value_tr": "Hafif Kamyon (2-5 ton)", "value_ar": "شاحنة خفيفة (2-5 طن)"},
            {"key_en": "Fuel", "key_ru": "Топливо", "key_tr": "Yakıt", "key_ar": "الوقود", "value_en": "Diesel / Electric", "value_ru": "Дизель / Электрический", "value_tr": "Dizel / Elektrik", "value_ar": "ديزل / كهربائي"},
            {"key_en": "Brands", "key_ru": "Бренды", "key_tr": "Markalar", "key_ar": "العلامات", "value_en": "FOTON, JAC, DONGFENG", "value_ru": "FOTON, JAC, DONGFENG", "value_tr": "FOTON, JAC, DONGFENG", "value_ar": "FOTON, JAC, DONGFENG"},
        ],
    },
]

for prod in auto_products:
    upsert_product(prod["slug"], "automobiles", prod["fields"], prod["specs"])


# ── Construction Materials ────────────────────────────────────────────────────

const_desc = """<p>VAAM provides sourcing and supply of construction materials from Chinese manufacturers. We help construction companies and contractors find quality materials at competitive prices with reliable delivery.</p>"""
const_desc_ru = """<p>VAAM обеспечивает поиск и поставку строительных материалов от китайских производителей.</p>"""
const_desc_tr = """<p>VAAM, Çinli üreticilerden inşaat malzemeleri tedarik ve temini hizmeti sunmaktadır.</p>"""
const_desc_ar = """<p>توفر VAAM خدمات البحث عن وتوريد مواد البناء من المصنعين الصينيين.</p>"""

construction_products = [
    {
        "slug": "steel-rebar-hrb400",
        "fields": {
            "name_en": "HRB400 Steel Rebar", "name_ru": "Стальная арматура HRB400",
            "name_tr": "HRB400 Çelik İnşaat Demiri", "name_ar": "حديد تسليح HRB400",
            "short_description_en": "High-strength HRB400 deformed steel rebar for reinforced concrete construction. Available in various diameters.",
            "short_description_ru": "Высокопрочная рифлёная арматура HRB400 для железобетонного строительства.",
            "short_description_tr": "Betonarme inşaat için yüksek mukavemetli HRB400 nervürlü çelik inşaat demiri.",
            "short_description_ar": "حديد تسليح مشوه عالي القوة HRB400 للبناء بالخرسانة المسلحة.",
            "description_en": const_desc, "description_ru": const_desc_ru, "description_tr": const_desc_tr, "description_ar": const_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 1,
        },
        "specs": [
            {"key_en": "Grade", "key_ru": "Марка", "key_tr": "Kalite", "key_ar": "الدرجة", "value_en": "HRB400 / HRB500", "value_ru": "HRB400 / HRB500", "value_tr": "HRB400 / HRB500", "value_ar": "HRB400 / HRB500"},
            {"key_en": "Diameter", "key_ru": "Диаметр", "key_tr": "Çap", "key_ar": "القطر", "value_en": "8mm - 32mm", "value_ru": "8мм - 32мм", "value_tr": "8mm - 32mm", "value_ar": "8مم - 32مم"},
            {"key_en": "Standard", "key_ru": "Стандарт", "key_tr": "Standart", "key_ar": "المعيار", "value_en": "GB 1499.2 / ASTM A615", "value_ru": "GB 1499.2 / ASTM A615", "value_tr": "GB 1499.2 / ASTM A615", "value_ar": "GB 1499.2 / ASTM A615"},
            {"key_en": "MOQ", "key_ru": "Мин. заказ", "key_tr": "Min. Sipariş", "key_ar": "الحد الأدنى", "value_en": "25 tons", "value_ru": "25 тонн", "value_tr": "25 ton", "value_ar": "25 طن"},
        ],
    },
    {
        "slug": "pvc-pipe-upvc",
        "fields": {
            "name_en": "UPVC Water Pipe", "name_ru": "Водопроводная труба UPVC",
            "name_tr": "UPVC Su Borusu", "name_ar": "أنبوب مياه UPVC",
            "short_description_en": "UPVC pressure pipes for water supply and irrigation systems. Various sizes from DN20 to DN630.",
            "short_description_ru": "Напорные трубы UPVC для водоснабжения и ирригации. Размеры от DN20 до DN630.",
            "short_description_tr": "Su temini ve sulama sistemleri için UPVC basınçlı borular. DN20'den DN630'a kadar.",
            "short_description_ar": "أنابيب ضغط UPVC لإمدادات المياه والري. أحجام من DN20 إلى DN630.",
            "description_en": const_desc, "description_ru": const_desc_ru, "description_tr": const_desc_tr, "description_ar": const_desc_ar,
            "price": "Contact for Price", "is_featured": False, "is_active": True, "order": 2,
        },
        "specs": [
            {"key_en": "Material", "key_ru": "Материал", "key_tr": "Malzeme", "key_ar": "المادة", "value_en": "UPVC (Unplasticized PVC)", "value_ru": "UPVC (непластифицированный ПВХ)", "value_tr": "UPVC", "value_ar": "UPVC"},
            {"key_en": "Sizes", "key_ru": "Размеры", "key_tr": "Boyutlar", "key_ar": "الأحجام", "value_en": "DN20 - DN630", "value_ru": "DN20 - DN630", "value_tr": "DN20 - DN630", "value_ar": "DN20 - DN630"},
            {"key_en": "Pressure", "key_ru": "Давление", "key_tr": "Basınç", "key_ar": "الضغط", "value_en": "0.6 - 1.6 MPa", "value_ru": "0.6 - 1.6 МПа", "value_tr": "0.6 - 1.6 MPa", "value_ar": "0.6 - 1.6 ميجا باسكال"},
            {"key_en": "Standard", "key_ru": "Стандарт", "key_tr": "Standart", "key_ar": "المعيار", "value_en": "GB/T 10002 / ISO 1452", "value_ru": "GB/T 10002 / ISO 1452", "value_tr": "GB/T 10002 / ISO 1452", "value_ar": "GB/T 10002 / ISO 1452"},
        ],
    },
]

for prod in construction_products:
    upsert_product(prod["slug"], "construction-materials", prod["fields"], prod["specs"])


# ── Industrial Products ───────────────────────────────────────────────────────

indust_desc = """<p>VAAM sources and supplies industrial equipment, tools and machinery from China for factories, warehouses and industrial facilities across various sectors.</p>"""
indust_desc_ru = """<p>VAAM осуществляет поиск и поставку промышленного оборудования из Китая для фабрик и промышленных объектов.</p>"""
indust_desc_tr = """<p>VAAM, fabrikalar ve endüstriyel tesisler için Çin'den endüstriyel ekipman tedarik etmektedir.</p>"""
indust_desc_ar = """<p>توفر VAAM معدات وأدوات صناعية من الصين للمصانع والمنشآت الصناعية.</p>"""

industrial_products = [
    {
        "slug": "air-compressor-screw-type",
        "fields": {
            "name_en": "Screw Air Compressor 22kW", "name_ru": "Винтовой компрессор 22 кВт",
            "name_tr": "22kW Vidalı Hava Kompresörü", "name_ar": "ضاغط هواء لولبي 22 كيلو واط",
            "short_description_en": "Industrial screw air compressor 22kW for factory and workshop applications. Energy-efficient with low noise.",
            "short_description_ru": "Промышленный винтовой компрессор 22 кВт для фабрик и мастерских. Энергоэффективный.",
            "short_description_tr": "Fabrika ve atölye uygulamaları için 22kW endüstriyel vidalı hava kompresörü.",
            "short_description_ar": "ضاغط هواء لولبي صناعي 22 كيلو واط للمصانع وورش العمل.",
            "description_en": indust_desc, "description_ru": indust_desc_ru, "description_tr": indust_desc_tr, "description_ar": indust_desc_ar,
            "price": "Contact for Price", "is_featured": True, "is_active": True, "order": 1,
        },
        "specs": [
            {"key_en": "Power", "key_ru": "Мощность", "key_tr": "Güç", "key_ar": "القدرة", "value_en": "22 kW / 30 HP", "value_ru": "22 кВт / 30 л.с.", "value_tr": "22 kW / 30 HP", "value_ar": "22 كيلو واط / 30 حصان"},
            {"key_en": "Flow Rate", "key_ru": "Расход воздуха", "key_tr": "Hava Debisi", "key_ar": "معدل التدفق", "value_en": "3.6 m³/min", "value_ru": "3.6 м³/мин", "value_tr": "3.6 m³/dk", "value_ar": "3.6 م³/دقيقة"},
            {"key_en": "Pressure", "key_ru": "Давление", "key_tr": "Basınç", "key_ar": "الضغط", "value_en": "8-13 bar", "value_ru": "8-13 бар", "value_tr": "8-13 bar", "value_ar": "8-13 بار"},
            {"key_en": "Noise Level", "key_ru": "Уровень шума", "key_tr": "Gürültü", "key_ar": "مستوى الضوضاء", "value_en": "≤68 dB(A)", "value_ru": "≤68 дБ(А)", "value_tr": "≤68 dB(A)", "value_ar": "≤68 ديسيبل"},
        ],
    },
    {
        "slug": "electric-forklift-2t",
        "fields": {
            "name_en": "2-Ton Electric Forklift", "name_ru": "Электрический погрузчик 2 тонны",
            "name_tr": "2 Ton Elektrikli Forklift", "name_ar": "رافعة شوكية كهربائية 2 طن",
            "short_description_en": "2-ton capacity electric forklift for warehouses and factories. Zero-emission, low maintenance.",
            "short_description_ru": "Электропогрузчик грузоподъёмностью 2 тонны для складов и фабрик. Нулевой выброс.",
            "short_description_tr": "Depolar ve fabrikalar için 2 ton kapasiteli elektrikli forklift. Sıfır emisyon.",
            "short_description_ar": "رافعة شوكية كهربائية بسعة 2 طن للمستودعات والمصانع. خالية من الانبعاثات.",
            "description_en": indust_desc, "description_ru": indust_desc_ru, "description_tr": indust_desc_tr, "description_ar": indust_desc_ar,
            "price": "Contact for Price", "is_featured": False, "is_active": True, "order": 2,
        },
        "specs": [
            {"key_en": "Capacity", "key_ru": "Грузоподъёмность", "key_tr": "Kapasite", "key_ar": "السعة", "value_en": "2,000 kg", "value_ru": "2 000 кг", "value_tr": "2.000 kg", "value_ar": "2,000 كجم"},
            {"key_en": "Lift Height", "key_ru": "Высота подъёма", "key_tr": "Kaldırma Yüksekliği", "key_ar": "ارتفاع الرفع", "value_en": "3,000 - 6,000 mm", "value_ru": "3 000 - 6 000 мм", "value_tr": "3.000 - 6.000 mm", "value_ar": "3,000 - 6,000 مم"},
            {"key_en": "Battery", "key_ru": "Батарея", "key_tr": "Batarya", "key_ar": "البطارية", "value_en": "Lithium-ion 80V/400Ah", "value_ru": "Литий-ион 80В/400Ач", "value_tr": "Lityum-iyon 80V/400Ah", "value_ar": "ليثيوم أيون 80V/400Ah"},
            {"key_en": "Work Time", "key_ru": "Время работы", "key_tr": "Çalışma Süresi", "key_ar": "وقت العمل", "value_en": "8-10 hours", "value_ru": "8-10 часов", "value_tr": "8-10 saat", "value_ar": "8-10 ساعات"},
        ],
    },
]

for prod in industrial_products:
    upsert_product(prod["slug"], "industrial-products", prod["fields"], prod["specs"])


# ════════════════════════════════════════════════════════════════════════════════
# STEP 4: Update Services (replace solar-specific with trading services)
# ════════════════════════════════════════════════════════════════════════════════
print("\n[4/6] Updating services...")

ServiceCategory.objects.all().delete()

svc_categories = [
    {"slug": "sourcing-supply", "name_en": "Sourcing & Supply", "name_ru": "Поиск и поставка",
     "name_tr": "Tedarik ve Temin", "name_ar": "البحث والتوريد", "order": 1},
    {"slug": "logistics-customs", "name_en": "Logistics & Customs", "name_ru": "Логистика и таможня",
     "name_tr": "Lojistik ve Gümrük", "name_ar": "اللوجستيات والجمارك", "order": 2},
    {"slug": "quality-support", "name_en": "Quality & Support", "name_ru": "Качество и поддержка",
     "name_tr": "Kalite ve Destek", "name_ar": "الجودة والدعم", "order": 3},
]

svc_cat_objs = {}
for sc in svc_categories:
    obj = ServiceCategory.objects.create(**sc, is_active=True)
    svc_cat_objs[sc["slug"]] = obj
    print(f"   ✓ Service category: {sc['name_en']}")

services_data = [
    {
        "cat": "sourcing-supply",
        "slug": "product-sourcing",
        "title_en": "Product Sourcing & Research", "title_ru": "Поиск и подбор продукции",
        "title_tr": "Ürün Araştırması ve Tedarik", "title_ar": "البحث عن المنتجات وتوفيرها",
        "short_description_en": "We research, find and select the best products matching your requirements from our extensive Chinese supplier network.",
        "short_description_ru": "Исследуем, находим и выбираем лучшие продукты из нашей обширной сети поставщиков в Китае.",
        "short_description_tr": "Geniş Çin tedarikçi ağımızdan gereksinimlerinize uygun en iyi ürünleri araştırır, bulur ve seçeriz.",
        "short_description_ar": "نبحث ونجد ونختار أفضل المنتجات من شبكة الموردين الواسعة في الصين.",
        "description_en": "<p>Our team conducts thorough market research in China to find products that meet your exact specifications, quality standards, and budget. We leverage our extensive network of verified suppliers across Guangzhou, Shenzhen, Yiwu, and other major manufacturing hubs.</p>",
        "description_ru": "<p>Наша команда проводит тщательное исследование рынка Китая для поиска продукции, соответствующей вашим требованиям.</p>",
        "description_tr": "<p>Ekibimiz, tam spesifikasyonlarınıza uygun ürünleri bulmak için Çin pazarında kapsamlı araştırma yapar.</p>",
        "description_ar": "<p>يجري فريقنا أبحاثاً شاملة في السوق الصيني للعثور على المنتجات التي تلبي متطلباتكم.</p>",
        "icon": "fas fa-search", "order": 1,
        "features_en": "Market research across Chinese manufacturing hubs\nSupplier comparison (price, quality, capacity)\nSample procurement and evaluation\nNegotiation on behalf of customer\nRegular supply agreement setup",
        "features_ru": "Исследование рынка\nСравнение поставщиков\nЗакупка и оценка образцов\nПереговоры от имени клиента\nРегулярные контракты",
        "features_tr": "Çin üretim merkezlerinde pazar araştırması\nTedarikçi karşılaştırması\nNumune tedarik ve değerlendirme\nMüşteri adına müzakere\nDüzenli tedarik anlaşması",
        "features_ar": "أبحاث السوق\nمقارنة الموردين\nشراء وتقييم العينات\nالتفاوض نيابة عن العميل\nاتفاقيات توريد منتظمة",
    },
    {
        "cat": "sourcing-supply",
        "slug": "supplier-selection",
        "title_en": "Supplier Verification & Selection", "title_ru": "Проверка и выбор поставщиков",
        "title_tr": "Tedarikçi Doğrulama ve Seçimi", "title_ar": "التحقق من الموردين واختيارهم",
        "short_description_en": "We verify and audit Chinese suppliers to ensure reliability, quality, and compliance with international standards.",
        "short_description_ru": "Проверяем и аудитируем китайских поставщиков для обеспечения надёжности и качества.",
        "short_description_tr": "Güvenilirlik ve kalite standartlarını sağlamak için Çinli tedarikçileri doğrular ve denetleriz.",
        "short_description_ar": "نتحقق من الموردين الصينيين ونراجعهم لضمان الموثوقية والجودة.",
        "description_en": "<p>Before any order, we conduct factory visits, review certifications, assess production capacity and check trade references. This ensures you work only with verified, reliable manufacturers.</p>",
        "description_ru": "<p>Перед каждым заказом проводим визиты на заводы и проверяем сертификаты.</p>",
        "description_tr": "<p>Her siparişten önce fabrika ziyaretleri yaparak sertifikaları ve üretim kapasitesini değerlendiririz.</p>",
        "description_ar": "<p>قبل أي طلب، نقوم بزيارات المصانع ومراجعة الشهادات وتقييم القدرة الإنتاجية.</p>",
        "icon": "fas fa-clipboard-check", "order": 2,
        "features_en": "Factory visits and on-site audits\nCertification verification (ISO, CE, etc.)\nProduction capacity assessment\nTrade reference checks\nSupplier risk evaluation",
        "features_ru": "Визиты на заводы\nПроверка сертификатов\nОценка производственной мощности\nПроверка торговых рекомендаций\nОценка рисков",
        "features_tr": "Fabrika ziyaretleri\nSertifika doğrulama\nÜretim kapasitesi değerlendirmesi\nTicari referans kontrolü\nTedarikçi risk değerlendirmesi",
        "features_ar": "زيارات المصانع\nالتحقق من الشهادات\nتقييم القدرة الإنتاجية\nفحص المراجع التجارية\nتقييم مخاطر الموردين",
    },
    {
        "cat": "logistics-customs",
        "slug": "international-logistics",
        "title_en": "International Logistics & Shipping", "title_ru": "Международная логистика и доставка",
        "title_tr": "Uluslararası Lojistik ve Nakliye", "title_ar": "اللوجستيات الدولية والشحن",
        "short_description_en": "Complete logistics management from Chinese factories to your destination — sea freight, air freight, and land transport.",
        "short_description_ru": "Полное управление логистикой от фабрик Китая до пункта назначения.",
        "short_description_tr": "Çin fabrikalarından varış noktanıza kadar tam lojistik yönetimi.",
        "short_description_ar": "إدارة لوجستية كاملة من المصانع الصينية إلى وجهتك.",
        "description_en": "<p>We handle all aspects of international shipping from China including container booking, freight forwarding, insurance, and delivery scheduling. We offer FOB, CIF, and DDP terms depending on your needs.</p>",
        "description_ru": "<p>Мы управляем всеми аспектами международной доставки из Китая.</p>",
        "description_tr": "<p>Çin'den uluslararası nakliyenin tüm yönlerini yönetiyoruz.</p>",
        "description_ar": "<p>نتعامل مع جميع جوانب الشحن الدولي من الصين.</p>",
        "icon": "fas fa-ship", "order": 3,
        "features_en": "Sea freight (FCL / LCL)\nAir freight for urgent orders\nLand transport and last-mile delivery\nCargo insurance\nReal-time shipment tracking\nIncoterms: FOB / CIF / DDP",
        "features_ru": "Морские перевозки (FCL/LCL)\nАвиафрахт\nНаземный транспорт\nСтрахование грузов\nОтслеживание в реальном времени\nIncoterms: FOB/CIF/DDP",
        "features_tr": "Deniz taşımacılığı (FCL/LCL)\nAcil siparişler için hava kargo\nKara taşımacılığı\nKargo sigortası\nGerçek zamanlı takip\nIncoterms: FOB/CIF/DDP",
        "features_ar": "الشحن البحري (FCL/LCL)\nالشحن الجوي للطلبات العاجلة\nالنقل البري\nتأمين البضائع\nتتبع الشحنات\nIncoterms: FOB/CIF/DDP",
    },
    {
        "cat": "logistics-customs",
        "slug": "customs-clearance",
        "title_en": "Customs Clearance Support", "title_ru": "Поддержка таможенного оформления",
        "title_tr": "Gümrük İşlemleri Desteği", "title_ar": "دعم التخليص الجمركي",
        "short_description_en": "We assist with export documentation, customs declarations, and import clearance procedures in destination countries.",
        "short_description_ru": "Помощь с экспортной документацией, таможенными декларациями и импортным оформлением.",
        "short_description_tr": "İhracat belgeleri, gümrük beyannameleri ve ithalat işlemlerinde yardım sağlıyoruz.",
        "short_description_ar": "نساعد في وثائق التصدير والبيانات الجمركية وإجراءات التخليص.",
        "description_en": "<p>Navigating customs procedures between China and destination countries can be complex. We handle all export documentation from the Chinese side and provide guidance for import clearance in Azerbaijan, Uzbekistan, Russia, and other markets.</p>",
        "description_ru": "<p>Мы оформляем всю экспортную документацию со стороны Китая.</p>",
        "description_tr": "<p>Çin tarafındaki tüm ihracat belgelerini hazırlıyoruz.</p>",
        "description_ar": "<p>نتولى جميع وثائق التصدير من الجانب الصيني.</p>",
        "icon": "fas fa-file-alt", "order": 4,
        "features_en": "Export documentation preparation\nCustoms declaration filing\nCertificate of Origin (CO)\nCommercial invoice and packing list\nHS code classification\nImport guidance for destination country",
        "features_ru": "Подготовка экспортной документации\nТаможенные декларации\nСертификат происхождения\nСчёт-фактура\nКлассификация HS кодов\nКонсультации по импорту",
        "features_tr": "İhracat belgeleri hazırlama\nGümrük beyannamesi\nMenşe belgesi\nFatura ve paketleme listesi\nHS kodu sınıflandırması\nİthalat rehberliği",
        "features_ar": "إعداد وثائق التصدير\nإيداع البيانات الجمركية\nشهادة المنشأ\nالفاتورة التجارية\nتصنيف رموز HS\nإرشادات الاستيراد",
    },
    {
        "cat": "quality-support",
        "slug": "quality-inspection",
        "title_en": "Quality Inspection & Control", "title_ru": "Контроль качества",
        "title_tr": "Kalite Kontrolü ve Denetimi", "title_ar": "فحص الجودة والرقابة",
        "short_description_en": "Pre-shipment quality inspection at the factory to ensure products meet your specifications before export.",
        "short_description_ru": "Предотгрузочный контроль качества на заводе для обеспечения соответствия вашим требованиям.",
        "short_description_tr": "İhracat öncesi fabrikada kalite kontrolü yaparak ürünlerin spesifikasyonlarınıza uygun olmasını sağlıyoruz.",
        "short_description_ar": "فحص الجودة قبل الشحن في المصنع لضمان مطابقة المنتجات لمواصفاتكم.",
        "description_en": "<p>Our quality team conducts on-site inspections at the factory before shipment. We check product specifications, packaging, labeling, and overall condition according to your requirements and international standards.</p>",
        "description_ru": "<p>Наша команда проводит проверки на заводе перед отгрузкой.</p>",
        "description_tr": "<p>Kalite ekibimiz sevkiyat öncesi fabrikada yerinde denetim yapar.</p>",
        "description_ar": "<p>يقوم فريق الجودة لدينا بإجراء عمليات فحص في المصنع قبل الشحن.</p>",
        "icon": "fas fa-search-plus", "order": 5,
        "features_en": "Pre-production inspection (PPI)\nDuring-production inspection (DPI)\nPre-shipment inspection (PSI)\nContainer loading inspection (CLI)\nTest report verification\nPhoto and video documentation",
        "features_ru": "Предпроизводственная инспекция\nИнспекция в процессе производства\nПредотгрузочная инспекция\nИнспекция загрузки контейнера\nПроверка тестовых отчётов\nФото и видеодокументация",
        "features_tr": "Üretim öncesi denetim\nÜretim sırası denetim\nSevkiyat öncesi denetim\nKonteyner yükleme denetimi\nTest raporu doğrulama\nFoto ve video dokümantasyonu",
        "features_ar": "فحص ما قبل الإنتاج\nفحص أثناء الإنتاج\nفحص ما قبل الشحن\nفحص تحميل الحاوية\nالتحقق من تقارير الاختبار\nتوثيق بالصور والفيديو",
    },
    {
        "cat": "quality-support",
        "slug": "after-sales-service",
        "title_en": "After-Sales Service & Support", "title_ru": "Послепродажное обслуживание",
        "title_tr": "Satış Sonrası Hizmet ve Destek", "title_ar": "خدمة ومساعدة ما بعد البيع",
        "short_description_en": "Ongoing support after delivery including warranty claims, technical assistance, and reorder management.",
        "short_description_ru": "Поддержка после доставки: гарантийные обращения, техническая помощь, повторные заказы.",
        "short_description_tr": "Teslimat sonrası garanti talepleri, teknik destek ve yeniden sipariş yönetimi.",
        "short_description_ar": "دعم مستمر بعد التسليم يشمل مطالبات الضمان والمساعدة الفنية.",
        "description_en": "<p>Our relationship doesn't end at delivery. We provide after-sales support including warranty claim handling with manufacturers, technical documentation, spare parts sourcing, and streamlined reorder processes for repeat customers.</p>",
        "description_ru": "<p>Наши отношения не заканчиваются при доставке.</p>",
        "description_tr": "<p>İlişkimiz teslimatla bitmez.</p>",
        "description_ar": "<p>علاقتنا لا تنتهي عند التسليم.</p>",
        "icon": "fas fa-headset", "order": 6,
        "features_en": "Warranty claim processing with manufacturers\nTechnical documentation and manuals\nSpare parts sourcing\nReorder management for repeat customers\nInstallation guidance (remote)\nLong-term partnership programs",
        "features_ru": "Обработка гарантийных обращений\nТехническая документация\nПоиск запасных частей\nУправление повторными заказами\nКонсультации по установке\nДолгосрочное партнёрство",
        "features_tr": "Garanti talep işleme\nTeknik dokümantasyon\nYedek parça tedarik\nTekrar sipariş yönetimi\nKurulum rehberliği\nUzun vadeli ortaklık programları",
        "features_ar": "معالجة مطالبات الضمان\nالوثائق الفنية\nتوريد قطع الغيار\nإدارة إعادة الطلب\nإرشادات التركيب\nبرامج شراكة طويلة الأجل",
    },
]

for svc in services_data:
    cat_key = svc.pop("cat")
    Service.objects.create(category=svc_cat_objs[cat_key], is_active=True, **svc)
    print(f"   ✓ Service: {svc['title_en']}")


# ════════════════════════════════════════════════════════════════════════════════
# STEP 5: Update Testimonials, Brands, News
# ════════════════════════════════════════════════════════════════════════════════
print("\n[5/6] Updating testimonials, brands, news...")

# ── Testimonials ──
Testimonial.objects.all().delete()
testimonials = [
    {
        "name": "Elvin Mammadov", "position_en": "Procurement Manager", "position_ru": "Менеджер по закупкам",
        "position_tr": "Satın Alma Müdürü", "position_ar": "مدير المشتريات",
        "company": "AzEnergy LLC, Azerbaijan",
        "content_en": "VAAM supplied us with diesel generators ranging from 50 to 500 kVA. The quality of the equipment, timely delivery and professional documentation exceeded our expectations. We highly recommend them as a reliable trading partner.",
        "content_ru": "VAAM поставила нам дизельные генераторы мощностью от 50 до 500 кВА. Качество оборудования, своевременная доставка и профессиональная документация превзошли наши ожидания.",
        "content_tr": "VAAM bize 50'den 500 kVA'ya kadar dizel jeneratörler tedarik etti. Ekipman kalitesi, zamanında teslimat ve profesyonel dokümantasyon beklentilerimizi aştı.",
        "content_ar": "زودتنا VAAM بمولدات ديزل تتراوح من 50 إلى 500 كيلو فولت أمبير. جودة المعدات والتسليم في الوقت المحدد تجاوزت توقعاتنا.",
        "rating": 5, "order": 1,
    },
    {
        "name": "Rustam Karimov", "position_en": "General Director", "position_ru": "Генеральный директор",
        "position_tr": "Genel Müdür", "position_ar": "المدير العام",
        "company": "UzPower Systems, Uzbekistan",
        "content_en": "We have been working with VAAM for over 2 years on generator supply projects. Their team in China is responsive, prices are competitive, and they handle all customs documentation efficiently. A trustworthy partner for Central Asian markets.",
        "content_ru": "Мы сотрудничаем с VAAM более 2 лет по проектам поставки генераторов. Их команда в Китае оперативна, цены конкурентоспособны.",
        "content_tr": "Jeneratör tedarik projeleri kapsamında VAAM ile 2 yılı aşkındır çalışıyoruz. Çin'deki ekipleri hızlı, fiyatları rekabetçi.",
        "content_ar": "نعمل مع VAAM منذ أكثر من عامين في مشاريع توريد المولدات. فريقهم في الصين سريع الاستجابة والأسعار تنافسية.",
        "rating": 5, "order": 2,
    },
    {
        "name": "Dmitry Volkov", "position_en": "Chief Engineer", "position_ru": "Главный инженер",
        "position_tr": "Baş Mühendis", "position_ar": "كبير المهندسين",
        "company": "RusTransEnergy, Russia",
        "content_en": "VAAM delivered S11-series distribution transformers for our projects. The transformers met IEC standards and arrived with full test certificates. Their quality inspection process gave us confidence in every shipment.",
        "content_ru": "VAAM поставила распределительные трансформаторы серии S11 для наших проектов. Трансформаторы соответствуют стандартам МЭК и прибыли с полными сертификатами испытаний.",
        "content_tr": "VAAM projelerimiz için S11 serisi dağıtım transformatörleri teslim etti. Transformatörler IEC standartlarına uygundu ve tam test sertifikalarıyla geldi.",
        "content_ar": "قدمت VAAM محولات توزيع من سلسلة S11 لمشاريعنا. المحولات استوفت معايير IEC ووصلت مع شهادات اختبار كاملة.",
        "rating": 5, "order": 3,
    },
    {
        "name": "Farid Hasanli", "position_en": "Project Coordinator", "position_ru": "Координатор проектов",
        "position_tr": "Proje Koordinatörü", "position_ar": "منسق المشاريع",
        "company": "BakuBuild Construction, Azerbaijan",
        "content_en": "We ordered construction materials and industrial equipment through VAAM. Their product sourcing in China saved us significant costs compared to local suppliers, while maintaining high quality standards.",
        "content_ru": "Мы заказывали строительные материалы и промышленное оборудование через VAAM. Их поиск продукции в Китае значительно сэкономил наши расходы.",
        "content_tr": "VAAM aracılığıyla inşaat malzemeleri ve endüstriyel ekipman sipariş ettik. Çin'deki ürün tedarikleri, yerel tedarikçilere kıyasla önemli maliyet tasarrufu sağladı.",
        "content_ar": "طلبنا مواد بناء ومعدات صناعية من خلال VAAM. بحثهم عن المنتجات في الصين وفر لنا تكاليف كبيرة.",
        "rating": 5, "order": 4,
    },
]

for t in testimonials:
    Testimonial.objects.create(**t, is_active=True)
    print(f"   ✓ Testimonial: {t['name']}")


# ── Brands ──
Brand.objects.all().delete()
brands = [
    ("BYD", "https://www.byd.com", 1),
    ("CHERY", "https://www.cheryinternational.com", 2),
    ("Huawei", "https://www.huawei.com", 3),
    ("Hikvision", "https://www.hikvision.com", 4),
    ("Dahua Technology", "https://www.dahuasecurity.com", 5),
    ("FOTON Motor", "https://www.foton-global.com", 6),
    ("Dongfeng", "https://www.dongfeng-global.com", 7),
    ("Longi Solar", "https://www.longi.com", 8),
    ("JA Solar", "https://www.jasolar.com", 9),
    ("Cummins (China)", "https://www.cummins.com", 10),
]
for name, url, order in brands:
    Brand.objects.create(name_en=name, name_ru=name, name_tr=name, name_ar=name,
                         url=url, order=order, logo="brands/placeholder.png", is_active=True)
    print(f"   ✓ Brand: {name}")


# ── News (clean old solar-specific, add trading news) ──
News.objects.filter(slug__in=[
    'azerbaijan-sets-2030-target-2gw-solar', 'vaam-opens-new-distribution-center',
    'understanding-n-type-topcon-solar-cells', 'solar-panel-prices-record-low-2025',
    'vaam-achieves-iso-9001-certification', 'cop30-solar-adoption-developing-markets',
]).delete()

news_cat, _ = NewsCategory.objects.get_or_create(
    slug="company-news",
    defaults={"name_en": "Company News", "name_ru": "Новости компании",
              "name_tr": "Şirket Haberleri", "name_ar": "أخبار الشركة", "order": 1}
)

news_articles = [
    {
        "slug": "vaam-expands-product-portfolio-2025",
        "title_en": "VAAM Expands Product Portfolio with New Categories",
        "title_ru": "VAAM расширяет ассортимент новыми категориями",
        "title_tr": "VAAM Yeni Kategorilerle Ürün Portföyünü Genişletiyor",
        "title_ar": "VAAM توسع محفظة منتجاتها بفئات جديدة",
        "summary_en": "VAAM Trading adds street lighting, security cameras, and construction materials to its product range alongside existing energy equipment.",
        "summary_ru": "VAAM Trading добавляет уличное освещение, камеры безопасности и стройматериалы к своему ассортименту.",
        "summary_tr": "VAAM Trading, mevcut enerji ekipmanlarının yanı sıra sokak aydınlatması, güvenlik kameraları ve inşaat malzemeleri ekledi.",
        "summary_ar": "VAAM Trading تضيف إضاءة الشوارع وكاميرات الأمن ومواد البناء إلى مجموعة منتجاتها.",
        "content_en": "<p>VAAM Import and Export Trading Co., Ltd. is pleased to announce the expansion of our product portfolio to include street and garden lighting systems, security cameras and surveillance equipment, construction materials, and industrial products. This expansion reflects growing demand from our clients in Azerbaijan, Uzbekistan, Russia and other markets for a wider range of quality products sourced from China.</p><p>Our established supply chain network and quality inspection processes ensure the same high standards across all product categories.</p>",
        "content_ru": "<p>VAAM рада объявить о расширении ассортимента продукции.</p>",
        "content_tr": "<p>VAAM, ürün portföyünün genişletildiğini duyurmaktan memnuniyet duyar.</p>",
        "content_ar": "<p>يسعد VAAM أن تعلن عن توسيع محفظة منتجاتها.</p>",
        "reading_time": 3, "is_featured": True,
    },
    {
        "slug": "generator-delivery-uzbekistan-2025",
        "title_en": "Successful Generator Delivery to Uzbekistan",
        "title_ru": "Успешная поставка генераторов в Узбекистан",
        "title_tr": "Özbekistan'a Başarılı Jeneratör Teslimatı",
        "title_ar": "تسليم ناجح للمولدات إلى أوزبكستان",
        "summary_en": "VAAM completes another batch of diesel generator deliveries to the Republic of Uzbekistan, ranging from 100 to 500 kVA.",
        "summary_ru": "VAAM завершает очередную партию поставок дизельных генераторов в Республику Узбекистан.",
        "summary_tr": "VAAM, Özbekistan Cumhuriyeti'ne 100'den 500 kVA'ya kadar dizel jeneratör teslimatını tamamladı.",
        "summary_ar": "أكملت VAAM دفعة أخرى من تسليمات مولدات الديزل إلى جمهورية أوزبكستان.",
        "content_en": "<p>VAAM Import and Export Trading Co., Ltd. has successfully completed a multi-unit diesel generator delivery to the Republic of Uzbekistan. The shipment included 100 kVA, 300 kVA, and 500 kVA units, all delivered within the 25–40 day commitment with full technical documentation and factory test reports.</p>",
        "content_ru": "<p>VAAM успешно завершила поставку дизельных генераторов в Узбекистан.</p>",
        "content_tr": "<p>VAAM, Özbekistan'a çok birimli dizel jeneratör teslimatını başarıyla tamamladı.</p>",
        "content_ar": "<p>أكملت VAAM بنجاح تسليم مولدات ديزل متعددة إلى أوزبكستان.</p>",
        "reading_time": 2, "is_featured": True,
    },
    {
        "slug": "transformer-delivery-azerbaijan-2025",
        "title_en": "Distribution Transformers Delivered to Azerbaijan",
        "title_ru": "Распределительные трансформаторы доставлены в Азербайджан",
        "title_tr": "Dağıtım Transformatörleri Azerbaycan'a Teslim Edildi",
        "title_ar": "تسليم محولات التوزيع إلى أذربيجان",
        "summary_en": "VAAM delivers S11-series 1600 kVA and 2500 kVA distribution transformers with both aluminium and copper winding options to Azerbaijan.",
        "summary_ru": "VAAM поставляет трансформаторы серии S11 мощностью 1600 кВА и 2500 кВА в Азербайджан.",
        "summary_tr": "VAAM, S11 serisi 1600 kVA ve 2500 kVA dağıtım transformatörlerini Azerbaycan'a teslim etti.",
        "summary_ar": "سلّمت VAAM محولات توزيع من سلسلة S11 بقدرة 1600 و2500 كيلو فولت أمبير إلى أذربيجان.",
        "content_en": "<p>VAAM (Guangzhou) Import and Export Trading Co., Ltd. has completed the delivery of S11-series three-phase oil-immersed distribution transformers to the Republic of Azerbaijan. The order included 1600 kVA and 2500 kVA units in both aluminium and copper winding configurations, all conforming to IEC 60076 international standards.</p>",
        "content_ru": "<p>VAAM завершила поставку трансформаторов серии S11 в Азербайджан.</p>",
        "content_tr": "<p>VAAM, S11 serisi dağıtım transformatörlerinin Azerbaycan'a teslimatını tamamladı.</p>",
        "content_ar": "<p>أتمت VAAM تسليم محولات التوزيع من سلسلة S11 إلى أذربيجان.</p>",
        "reading_time": 2, "is_featured": False,
    },
]

for article in news_articles:
    News.objects.get_or_create(
        slug=article["slug"],
        defaults={
            **article,
            "category": news_cat,
            "image": "news/placeholder.jpg",
            "author": "VAAM Team",
            "is_published": True,
            "published_at": timezone.now(),
        }
    )
    print(f"   ✓ News: {article['title_en']}")


# ════════════════════════════════════════════════════════════════════════════════
# STEP 6: Clean up unused old categories
# ════════════════════════════════════════════════════════════════════════════════
print("\n[6/6] Final cleanup...")

# Remove old news categories
for slug in ['industry-news', 'technology', 'market-insights']:
    nc = NewsCategory.objects.filter(slug=slug).first()
    if nc and nc.news_set.count() == 0:
        nc.delete()
        print(f"   ✓ Removed empty news category: {slug}")

# Remove old service categories
for slug in ['consultation-design', 'supply-distribution', 'installation', 'maintenance-support']:
    sc = ServiceCategory.objects.filter(slug=slug).first()
    if sc and sc.services.count() == 0:
        sc.delete()
        print(f"   ✓ Removed empty service category: {slug}")


# ════════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("  ✓ PRODUCTION DATABASE UPDATE COMPLETED!")
print("=" * 80)
print(f"\n  Product Categories:  {ProductCategory.objects.filter(is_active=True).count()}")
print(f"  Products:            {Product.objects.filter(is_active=True).count()}")
print(f"  Service Categories:  {ServiceCategory.objects.count()}")
print(f"  Services:            {Service.objects.count()}")
print(f"  Testimonials:        {Testimonial.objects.count()}")
print(f"  Brands:              {Brand.objects.count()}")
print(f"  News:                {News.objects.filter(is_published=True).count()}")
print(f"  Projects:            {Project.objects.filter(is_active=True).count()}")
print("\n  All data available in EN, RU, TR, AR languages")
print("=" * 80)
