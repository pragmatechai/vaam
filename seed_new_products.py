"""
VAAM - New Products Seed Script
Adds Generators and Distribution Transformer categories with products.
Data is filled in 4 languages: EN, RU, TR, AR
Run on production:
    source venv/bin/activate
    python manage.py shell < seed_new_products.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()

from core.models import ProductCategory, Product, ProductSpecification

print("=" * 80)
print("  VAAM - New Products Seeding (Generators + Distribution Transformers)")
print("=" * 80)

# ─────────────────────────────────────────────
# 1. PRODUCT CATEGORIES
# ─────────────────────────────────────────────
print("\n[1/2] Creating product categories...")

generator_cat, gen_created = ProductCategory.objects.get_or_create(
    slug="generators",
    defaults={
        "name_en": "Generators",
        "name_ru": "Генераторы",
        "name_tr": "Jeneratörler",
        "name_ar": "المولدات",
        "description_en": "Diesel generator sets ranging from 50 kVA to 500 kVA for residential, commercial and industrial applications. Delivered within 25–40 days.",
        "description_ru": "Дизельные генераторные установки мощностью от 50 до 500 кВА для жилых, коммерческих и промышленных объектов. Срок поставки 25–40 дней.",
        "description_tr": "Konut, ticari ve endüstriyel uygulamalar için 50 kVA'dan 500 kVA'ya kadar dizel jeneratör grupları. 25–40 gün içinde teslimat.",
        "description_ar": "مجموعات مولدات ديزل تتراوح من 50 كيلو فولت أمبير إلى 500 كيلو فولت أمبير للتطبيقات السكنية والتجارية والصناعية. التسليم خلال 25-40 يوماً.",
        "icon": "fas fa-bolt",
        "order": 7,
        "is_active": True,
    }
)
if not gen_created:
    # update translations if category already existed
    generator_cat.name_en = "Generators"
    generator_cat.name_ru = "Генераторы"
    generator_cat.name_tr = "Jeneratörler"
    generator_cat.name_ar = "المولدات"
    generator_cat.description_en = "Diesel generator sets ranging from 50 kVA to 500 kVA for residential, commercial and industrial applications. Delivered within 25–40 days."
    generator_cat.description_ru = "Дизельные генераторные установки мощностью от 50 до 500 кВА для жилых, коммерческих и промышленных объектов. Срок поставки 25–40 дней."
    generator_cat.description_tr = "Konut, ticari ve endüstriyel uygulamalar için 50 kVA'dan 500 kVA'ya kadar dizel jeneratör grupları. 25–40 gün içinde teslimat."
    generator_cat.description_ar = "مجموعات مولدات ديزل تتراوح من 50 كيلو فولت أمبير إلى 500 كيلو فولت أمبير للتطبيقات السكنية والتجارية والصناعية. التسليم خلال 25-40 يوماً."
    generator_cat.icon = "fas fa-bolt"
    generator_cat.order = 7
    generator_cat.save()
print(f"   ✓ Generator category: {'created' if gen_created else 'updated'}")

transformer_cat, tr_created = ProductCategory.objects.get_or_create(
    slug="distribution-transformers",
    defaults={
        "name_en": "Distribution Transformers",
        "name_ru": "Распределительные трансформаторы",
        "name_tr": "Dağıtım Transformatörleri",
        "name_ar": "محولات التوزيع",
        "description_en": "Three-phase oil-immersed S11-series distribution transformers with 35/0.4 kV voltage ratio. Available in aluminium and copper winding options for 1600 kVA and 2500 kVA power ratings.",
        "description_ru": "Трёхфазные масляные распределительные трансформаторы серии S11 с соотношением напряжений 35/0,4 кВ. В обмотках из алюминия и меди мощностью 1600 кВА и 2500 кВА.",
        "description_tr": "35/0.4 kV voltaj oranına sahip üç fazlı yağ soğutmalı S11 serisi dağıtım transformatörleri. 1600 kVA ve 2500 kVA güç değerleri için alüminyum ve bakır sargı seçenekleri mevcuttur.",
        "description_ar": "محولات توزيع ثلاثية الأطوار مغمورة بالزيت من سلسلة S11 بنسبة جهد 35/0.4 كيلو فولت. متوفرة بأسلاك الألومنيوم والنحاس بقدرات 1600 كيلو فولت أمبير و2500 كيلو فولت أمبير.",
        "icon": "fas fa-broadcast-tower",
        "order": 8,
        "is_active": True,
    }
)
if not tr_created:
    transformer_cat.name_en = "Distribution Transformers"
    transformer_cat.name_ru = "Распределительные трансформаторы"
    transformer_cat.name_tr = "Dağıtım Transformatörleri"
    transformer_cat.name_ar = "محولات التوزيع"
    transformer_cat.description_en = "Three-phase oil-immersed S11-series distribution transformers with 35/0.4 kV voltage ratio. Available in aluminium and copper winding options for 1600 kVA and 2500 kVA power ratings."
    transformer_cat.description_ru = "Трёхфазные масляные распределительные трансформаторы серии S11 с соотношением напряжений 35/0,4 кВ. В обмотках из алюминия и меди мощностью 1600 кВА и 2500 кВА."
    transformer_cat.description_tr = "35/0.4 kV voltaj oranına sahip üç fazlı yağ soğutmalı S11 serisi dağıtım transformatörleri. 1600 kVA ve 2500 kVA güç değerleri için alüminyum ve bakır sargı seçenekleri mevcuttur."
    transformer_cat.description_ar = "محولات توزيع ثلاثية الأطوار مغمورة بالزيت من سلسلة S11 بنسبة جهد 35/0.4 كيلو فولت. متوفرة بأسلاك الألومنيوم والنحاس بقدرات 1600 كيلو فولت أمبير و2500 كيلو فولت أمبير."
    transformer_cat.icon = "fas fa-broadcast-tower"
    transformer_cat.order = 8
    transformer_cat.save()
print(f"   ✓ Distribution Transformer category: {'created' if tr_created else 'updated'}")


# ─────────────────────────────────────────────
# Helper: create or update product + specs
# ─────────────────────────────────────────────
def upsert_product(slug, category, fields, specs):
    """Create or update a product and replace its specifications."""
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

    # Replace specs
    p.specifications.all().delete()
    for i, spec in enumerate(specs):
        ProductSpecification.objects.create(
            product=p,
            key_en=spec["key_en"], key_ru=spec["key_ru"], key_tr=spec["key_tr"], key_ar=spec["key_ar"],
            value_en=spec["value_en"], value_ru=spec["value_ru"], value_tr=spec["value_tr"], value_ar=spec["value_ar"],
            order=i
        )
    return p, action


# ─────────────────────────────────────────────
# 2. GENERATORS
# ─────────────────────────────────────────────
print("\n[2/2] Creating generator and transformer products...")

generator_desc_en = """<p>VAAM Import and Export Trading Co., LTD supplies high-performance diesel generator sets manufactured to the highest international standards. These generators are built for reliable continuous and standby power in residential, commercial, and industrial environments.</p>
<p><strong>Key Features:</strong></p>
<ul>
<li>Reliable diesel engine with low fuel consumption</li>
<li>Brushless synchronous alternator for clean stable power output</li>
<li>Automatic Voltage Regulator (AVR) for voltage stability</li>
<li>Powder-coated canopy for weather protection and low noise</li>
<li>Delivered ready-to-run within 25–40 days</li>
</ul>"""

generator_desc_ru = """<p>VAAM Import and Export Trading Co., LTD поставляет высокопроизводительные дизельные генераторные установки, изготовленные по высочайшим международным стандартам. Эти генераторы предназначены для надёжного непрерывного и резервного электроснабжения жилых, коммерческих и промышленных объектов.</p>
<p><strong>Ключевые особенности:</strong></p>
<ul>
<li>Надёжный дизельный двигатель с низким расходом топлива</li>
<li>Бесщёточный синхронный генератор для чистого стабильного выхода</li>
<li>Автоматический регулятор напряжения (АРН) для стабилизации напряжения</li>
<li>Порошковое покрытие кожуха для защиты от атмосферных воздействий и низкого уровня шума</li>
<li>Поставляется готовым к работе в течение 25–40 дней</li>
</ul>"""

generator_desc_tr = """<p>VAAM Import and Export Trading Co., LTD, en yüksek uluslararası standartlara göre üretilmiş yüksek performanslı dizel jeneratör grupları tedarik etmektedir. Bu jeneratörler, konut, ticari ve endüstriyel ortamlarda güvenilir sürekli ve yedek güç için tasarlanmıştır.</p>
<p><strong>Temel Özellikler:</strong></p>
<ul>
<li>Düşük yakıt tüketimine sahip güvenilir dizel motor</li>
<li>Temiz kararlı güç çıkışı için fırçasız senkron alternatör</li>
<li>Voltaj kararlılığı için Otomatik Voltaj Regülatörü (AVR)</li>
<li>Hava koruması ve düşük gürültü için toz boyalı konopi</li>
<li>25–40 gün içinde çalışmaya hazır olarak teslim</li>
</ul>"""

generator_desc_ar = """<p>تورد شركة VAAM للاستيراد والتصدير مجموعات مولدات ديزل عالية الأداء مصنوعة وفق أعلى المعايير الدولية. هذه المولدات مصممة لتوفير طاقة مستمرة وموثوقة أو احتياطية في البيئات السكنية والتجارية والصناعية.</p>
<p><strong>الميزات الرئيسية:</strong></p>
<ul>
<li>محرك ديزل موثوق بكفاءة عالية في استهلاك الوقود</li>
<li>مولد متزامن بدون فرش لإخراج طاقة نظيف ومستقر</li>
<li>منظم جهد أوتوماتيكي (AVR) لثبات الجهد</li>
<li>هيكل مطلي بالطلاء للحماية من الطقس وخفض الضوضاء</li>
<li>يُسلَّم جاهزاً للتشغيل خلال 25–40 يوماً</li>
</ul>"""

generators = [
    {
        "slug": "generator-50-kva",
        "kva": "50",
        "kw": "40",
        "order": 1,
        "is_featured": False,
    },
    {
        "slug": "generator-100-kva",
        "kva": "100",
        "kw": "80",
        "order": 2,
        "is_featured": True,
    },
    {
        "slug": "generator-150-kva",
        "kva": "150",
        "kw": "120",
        "order": 3,
        "is_featured": False,
    },
    {
        "slug": "generator-300-kva",
        "kva": "300",
        "kw": "240",
        "order": 4,
        "is_featured": True,
    },
    {
        "slug": "generator-375-kva",
        "kva": "375",
        "kw": "300",
        "order": 5,
        "is_featured": False,
    },
    {
        "slug": "generator-500-kva",
        "kva": "500",
        "kw": "400",
        "order": 6,
        "is_featured": True,
    },
]

for g in generators:
    kva = g["kva"]
    kw = g["kw"]

    fields = {
        "name_en": f"{kva} kVA Diesel Generator",
        "name_ru": f"Дизельный генератор {kva} кВА",
        "name_tr": f"{kva} kVA Dizel Jeneratör",
        "name_ar": f"مولد ديزل {kva} كيلو فولت أمبير",

        "short_description_en": f"Reliable {kva} kVA ({kw} kW) diesel generator set for continuous and standby power. Exported to Azerbaijan, Uzbekistan and other markets. Delivery: 25–40 days.",
        "short_description_ru": f"Надёжная дизельная генераторная установка {kva} кВА ({kw} кВт) для непрерывного и резервного электроснабжения. Экспорт в Азербайджан, Узбекистан и другие рынки. Доставка: 25–40 дней.",
        "short_description_tr": f"Sürekli ve yedek güç için güvenilir {kva} kVA ({kw} kW) dizel jeneratör seti. Azerbaycan, Özbekistan ve diğer pazarlara ihracat. Teslimat: 25–40 gün.",
        "short_description_ar": f"مجموعة مولد ديزل موثوقة بقدرة {kva} كيلو فولت أمبير ({kw} كيلو واط) للطاقة المستمرة والاحتياطية. تصدير إلى أذربيجان وأوزبكستان وأسواق أخرى. التسليم: 25-40 يوماً.",

        "description_en": generator_desc_en,
        "description_ru": generator_desc_ru,
        "description_tr": generator_desc_tr,
        "description_ar": generator_desc_ar,

        "price": "Contact for Price",
        "is_featured": g["is_featured"],
        "is_active": True,
        "order": g["order"],

        "meta_title_en": f"{kva} kVA Diesel Generator | VAAM Trading",
        "meta_title_ru": f"Дизельный генератор {kva} кВА | VAAM Trading",
        "meta_title_tr": f"{kva} kVA Dizel Jeneratör | VAAM Trading",
        "meta_title_ar": f"مولد ديزل {kva} كيلو فولت أمبير | VAAM Trading",

        "meta_description_en": f"Buy {kva} kVA diesel generator set from VAAM Import and Export Trading. Reliable power for industrial and commercial use. Fast delivery within 25–40 days.",
        "meta_description_ru": f"Купите дизельный генератор {kva} кВА от VAAM Import and Export Trading. Надёжное электроснабжение для промышленного и коммерческого использования. Быстрая поставка 25–40 дней.",
        "meta_description_tr": f"VAAM'dan {kva} kVA dizel jeneratör satın alın. Endüstriyel ve ticari kullanım için güvenilir güç. 25–40 gün içinde hızlı teslimat.",
        "meta_description_ar": f"اشترِ مولد ديزل {kva} كيلو فولت أمبير من VAAM للاستيراد والتصدير. طاقة موثوقة للاستخدام الصناعي والتجاري. توصيل سريع خلال 25-40 يوماً.",
    }

    specs = [
        {
            "key_en": "Rated Power",        "key_ru": "Номинальная мощность",      "key_tr": "Nominal Güç",          "key_ar": "القدرة المقننة",
            "value_en": f"{kva} kVA / {kw} kW",  "value_ru": f"{kva} кВА / {kw} кВт",  "value_tr": f"{kva} kVA / {kw} kW",  "value_ar": f"{kva} كيلو فولت أمبير / {kw} كيلو واط",
        },
        {
            "key_en": "Voltage",            "key_ru": "Напряжение",               "key_tr": "Voltaj",               "key_ar": "الجهد",
            "value_en": "400 / 230 V",       "value_ru": "400 / 230 В",            "value_tr": "400 / 230 V",        "value_ar": "400 / 230 فولت",
        },
        {
            "key_en": "Frequency",          "key_ru": "Частота",                  "key_tr": "Frekans",              "key_ar": "التردد",
            "value_en": "50 Hz",             "value_ru": "50 Гц",                  "value_tr": "50 Hz",              "value_ar": "50 هرتز",
        },
        {
            "key_en": "Power Factor",       "key_ru": "Коэффициент мощности",     "key_tr": "Güç Faktörü",          "key_ar": "معامل الطاقة",
            "value_en": "0.8",               "value_ru": "0.8",                    "value_tr": "0.8",                "value_ar": "0.8",
        },
        {
            "key_en": "Engine Type",        "key_ru": "Тип двигателя",            "key_tr": "Motor Tipi",           "key_ar": "نوع المحرك",
            "value_en": "4-stroke Diesel",   "value_ru": "4-тактный дизель",       "value_tr": "4 zamanlı Dizel",    "value_ar": "ديزل 4 أشواط",
        },
        {
            "key_en": "Alternator",         "key_ru": "Генератор переменного тока","key_tr": "Alternatör",          "key_ar": "المولد المتردد",
            "value_en": "Brushless, self-excited", "value_ru": "Бесщёточный, самовозбуждающийся", "value_tr": "Fırçasız, kendinden uyarmalı", "value_ar": "بدون فرش، ذاتي الإثارة",
        },
        {
            "key_en": "Cooling",            "key_ru": "Охлаждение",               "key_tr": "Soğutma",              "key_ar": "التبريد",
            "value_en": "Water-cooled",      "value_ru": "Водяное охлаждение",     "value_tr": "Su soğutmalı",       "value_ar": "تبريد بالماء",
        },
        {
            "key_en": "Starting System",    "key_ru": "Система запуска",          "key_tr": "Çalıştırma Sistemi",   "key_ar": "نظام التشغيل",
            "value_en": "Electric start (12V/24V)", "value_ru": "Электрический пуск (12В/24В)", "value_tr": "Elektrikli start (12V/24V)", "value_ar": "بدء كهربائي (12/24 فولت)",
        },
        {
            "key_en": "Noise Level",        "key_ru": "Уровень шума",             "key_tr": "Gürültü Seviyesi",     "key_ar": "مستوى الضوضاء",
            "value_en": "≤75 dB(A) at 7m",  "value_ru": "≤75 дБ(А) на расстоянии 7м", "value_tr": "7m mesafede ≤75 dB(A)", "value_ar": "≤75 ديسيبل على بُعد 7 أمتار",
        },
        {
            "key_en": "Delivery Time",      "key_ru": "Срок поставки",            "key_tr": "Teslimat Süresi",      "key_ar": "وقت التسليم",
            "value_en": "25–40 days",        "value_ru": "25–40 дней",             "value_tr": "25–40 gün",          "value_ar": "25-40 يوماً",
        },
        {
            "key_en": "Export Markets",     "key_ru": "Рынки экспорта",           "key_tr": "İhracat Pazarları",    "key_ar": "أسواق التصدير",
            "value_en": "Azerbaijan, Uzbekistan", "value_ru": "Азербайджан, Узбекистан", "value_tr": "Azerbaycan, Özbekistan", "value_ar": "أذربيجان، أوزبكستان",
        },
    ]

    p, action = upsert_product(g["slug"], generator_cat, fields, specs)
    print(f"   ✓ {p.name_en} — {action}")


# ─────────────────────────────────────────────
# 3. DISTRIBUTION TRANSFORMERS
# ─────────────────────────────────────────────

transformer_desc_en = """<p>VAAM (Guangzhou) Import and Export Trading Co., Ltd. supplies S11-series three-phase oil-immersed distribution transformers. These transformers conform to IEC 60076 international standards and are suitable for medium-voltage power distribution networks.</p>
<p><strong>Key Features:</strong></p>
<ul>
<li>S11 series — low loss, energy-efficient design</li>
<li>Voltage ratio: 35 kV / 0.4 kV</li>
<li>Available in aluminium or copper winding</li>
<li>ONAN (Oil Natural Air Natural) cooling method</li>
<li>Compliant with IEC 60076, GB 1094 standards</li>
<li>Proven in real projects delivered to Azerbaijan and Russia</li>
</ul>"""

transformer_desc_ru = """<p>VAAM (Guangzhou) Import and Export Trading Co., Ltd. поставляет трёхфазные масляные распределительные трансформаторы серии S11. Эти трансформаторы соответствуют международным стандартам МЭК 60076 и пригодны для среднего напряжения распределительных сетей.</p>
<p><strong>Ключевые особенности:</strong></p>
<ul>
<li>Серия S11 — малопотерная, энергоэффективная конструкция</li>
<li>Коэффициент напряжений: 35 кВ / 0,4 кВ</li>
<li>Доступны в алюминиевой или медной обмотке</li>
<li>Метод охлаждения ONAN (масло/воздух, естественная конвекция)</li>
<li>Соответствует стандартам МЭК 60076, GB 1094</li>
<li>Проверен в реальных проектах, поставленных в Азербайджан и Россию</li>
</ul>"""

transformer_desc_tr = """<p>VAAM (Guangzhou) Import and Export Trading Co., Ltd., S11 serisi üç fazlı yağ soğutmalı dağıtım transformatörleri tedarik etmektedir. Bu transformatörler IEC 60076 uluslararası standartlarına uygundur ve orta gerilim dağıtım şebekeleri için uygundur.</p>
<p><strong>Temel Özellikler:</strong></p>
<ul>
<li>S11 serisi — düşük kayıplı, enerji verimli tasarım</li>
<li>Voltaj oranı: 35 kV / 0.4 kV</li>
<li>Alüminyum veya bakır sargılı olarak mevcuttur</li>
<li>ONAN (Yağ Doğal Hava Doğal) soğutma yöntemi</li>
<li>IEC 60076, GB 1094 standartlarına uygundur</li>
<li>Azerbaycan ve Rusya'ya teslim edilen gerçek projelerde kanıtlanmıştır</li>
</ul>"""

transformer_desc_ar = """<p>تورد شركة VAAM (قوانغتشو) للاستيراد والتصدير محولات التوزيع ثلاثية الأطوار المغمورة بالزيت من سلسلة S11. تتوافق هذه المحولات مع المعايير الدولية IEC 60076 وهي مناسبة لشبكات توزيع الطاقة ذات الجهد المتوسط.</p>
<p><strong>الميزات الرئيسية:</strong></p>
<ul>
<li>سلسلة S11 — تصميم منخفض الفقد وموفر للطاقة</li>
<li>نسبة الجهد: 35 كيلو فولت / 0.4 كيلو فولت</li>
<li>متوفرة بأسلاك الألومنيوم أو النحاس</li>
<li>طريقة التبريد ONAN (زيت طبيعي هواء طبيعي)</li>
<li>مطابقة لمعايير IEC 60076 و GB 1094</li>
<li>مثبتة في مشاريع حقيقية مسلّمة إلى أذربيجان وروسيا</li>
</ul>"""

transformers = [
    {
        "slug": "transformer-1600-kva-35kv-aluminium",
        "kva": "1600",
        "winding_en": "Aluminium",
        "winding_ru": "Алюминий",
        "winding_tr": "Alüminyum",
        "winding_ar": "ألومنيوم",
        "model": "S11-1600/35",
        "order": 1,
        "is_featured": True,
    },
    {
        "slug": "transformer-1600-kva-35kv-copper",
        "kva": "1600",
        "winding_en": "Copper",
        "winding_ru": "Медь",
        "winding_tr": "Bakır",
        "winding_ar": "نحاس",
        "model": "S11-1600/35",
        "order": 2,
        "is_featured": False,
    },
    {
        "slug": "transformer-2500-kva-35kv-aluminium",
        "kva": "2500",
        "winding_en": "Aluminium",
        "winding_ru": "Алюминий",
        "winding_tr": "Alüminyum",
        "winding_ar": "ألومنيوم",
        "model": "S11-2500/35",
        "order": 3,
        "is_featured": True,
    },
    {
        "slug": "transformer-2500-kva-35kv-copper",
        "kva": "2500",
        "winding_en": "Copper",
        "winding_ru": "Медь",
        "winding_tr": "Bakır",
        "winding_ar": "نحاس",
        "model": "S11-2500/35",
        "order": 4,
        "is_featured": False,
    },
]

for t in transformers:
    kva = t["kva"]
    model = t["model"]
    w_en = t["winding_en"]
    w_ru = t["winding_ru"]
    w_tr = t["winding_tr"]
    w_ar = t["winding_ar"]

    fields = {
        "name_en": f"{kva} kVA – 35/0.4 kV Distribution Transformer ({w_en} Winding)",
        "name_ru": f"Распределительный трансформатор {kva} кВА – 35/0,4 кВ (обмотка {w_ru})",
        "name_tr": f"{kva} kVA – 35/0.4 kV Dağıtım Transformatörü ({w_tr} Sargı)",
        "name_ar": f"محول توزيع {kva} كيلو فولت أمبير – 35/0.4 كيلو فولت (سلك {w_ar})",

        "short_description_en": f"S11-series three-phase oil-immersed {kva} kVA distribution transformer with 35/0.4 kV ratio and {w_en.lower()} winding. Supplied to Azerbaijan and Russia.",
        "short_description_ru": f"Трёхфазный масляный распределительный трансформатор серии S11 {kva} кВА с соотношением 35/0,4 кВ и обмоткой из {w_ru.lower()}а. Поставляется в Азербайджан и Россию.",
        "short_description_tr": f"S11 serisi üç fazlı yağ soğutmalı {kva} kVA dağıtım transformatörü, 35/0.4 kV oranı ve {w_tr.lower()} sargılı. Azerbaycan ve Rusya'ya tedarik edilmektedir.",
        "short_description_ar": f"محول توزيع S11 ثلاثي الأطوار مغمور بالزيت بقدرة {kva} كيلو فولت أمبير بنسبة 35/0.4 كيلو فولت وسلك {w_ar}. يُورَّد إلى أذربيجان وروسيا.",

        "description_en": transformer_desc_en,
        "description_ru": transformer_desc_ru,
        "description_tr": transformer_desc_tr,
        "description_ar": transformer_desc_ar,

        "price": "Contact for Price",
        "is_featured": t["is_featured"],
        "is_active": True,
        "order": t["order"],

        "meta_title_en": f"{kva} kVA {w_en} Winding Distribution Transformer | VAAM Trading",
        "meta_title_ru": f"Трансформатор {kva} кВА обмотка {w_ru} | VAAM Trading",
        "meta_title_tr": f"{kva} kVA {w_tr} Sargılı Dağıtım Transformatörü | VAAM Trading",
        "meta_title_ar": f"محول {kva} كيلو فولت أمبير سلك {w_ar} | VAAM Trading",

        "meta_description_en": f"Order {model} {kva} kVA 35/0.4 kV distribution transformer with {w_en.lower()} winding from VAAM. Supplied to Azerbaijan, Russia and international markets.",
        "meta_description_ru": f"Заказать трансформатор {model} {kva} кВА 35/0,4 кВ с обмоткой из {w_ru.lower()}а от VAAM. Поставки в Азербайджан, Россию и международные рынки.",
        "meta_description_tr": f"VAAM'dan {model} {kva} kVA 35/0.4 kV {w_tr.lower()} sargılı dağıtım transformatörü sipariş edin. Azerbaycan, Rusya ve uluslararası pazarlara tedarik.",
        "meta_description_ar": f"اطلب محول {model} بقدرة {kva} كيلو فولت أمبير 35/0.4 كيلو فولت بسلك {w_ar} من VAAM. يُورَّد إلى أذربيجان وروسيا والأسواق الدولية.",
    }

    specs = [
        {
            "key_en": "Model",              "key_ru": "Модель",                   "key_tr": "Model",                "key_ar": "الموديل",
            "value_en": model,               "value_ru": model,                    "value_tr": model,                "value_ar": model,
        },
        {
            "key_en": "Rated Power",        "key_ru": "Номинальная мощность",      "key_tr": "Nominal Güç",          "key_ar": "القدرة المقننة",
            "value_en": f"{kva} kVA",        "value_ru": f"{kva} кВА",             "value_tr": f"{kva} kVA",         "value_ar": f"{kva} كيلو فولت أمبير",
        },
        {
            "key_en": "Voltage Ratio",      "key_ru": "Коэффициент напряжения",    "key_tr": "Voltaj Oranı",         "key_ar": "نسبة الجهد",
            "value_en": "35 kV / 0.4 kV",   "value_ru": "35 кВ / 0,4 кВ",         "value_tr": "35 kV / 0.4 kV",    "value_ar": "35 كيلو فولت / 0.4 كيلو فولت",
        },
        {
            "key_en": "Phases",             "key_ru": "Фазы",                     "key_tr": "Faz Sayısı",           "key_ar": "الأطوار",
            "value_en": "3-phase",           "value_ru": "3-фазный",               "value_tr": "3 fazlı",            "value_ar": "ثلاثي الأطوار",
        },
        {
            "key_en": "Frequency",          "key_ru": "Частота",                  "key_tr": "Frekans",              "key_ar": "التردد",
            "value_en": "50 Hz",             "value_ru": "50 Гц",                  "value_tr": "50 Hz",              "value_ar": "50 هرتز",
        },
        {
            "key_en": "Winding Material",   "key_ru": "Материал обмотки",         "key_tr": "Sargı Malzemesi",      "key_ar": "مادة السلك",
            "value_en": w_en,                "value_ru": w_ru,                     "value_tr": w_tr,                 "value_ar": w_ar,
        },
        {
            "key_en": "Insulation Class",   "key_ru": "Класс изоляции",           "key_tr": "Yalıtım Sınıfı",       "key_ar": "فئة العزل",
            "value_en": "Class A (Oil)",     "value_ru": "Класс А (масляная)",     "value_tr": "Sınıf A (Yağ)",      "value_ar": "الفئة أ (زيت)",
        },
        {
            "key_en": "Cooling Method",     "key_ru": "Метод охлаждения",         "key_tr": "Soğutma Yöntemi",      "key_ar": "طريقة التبريد",
            "value_en": "ONAN",              "value_ru": "ONAN",                   "value_tr": "ONAN",               "value_ar": "ONAN",
        },
        {
            "key_en": "Standard",           "key_ru": "Стандарт",                 "key_tr": "Standart",             "key_ar": "المعيار",
            "value_en": "IEC 60076 / GB 1094", "value_ru": "МЭК 60076 / GB 1094", "value_tr": "IEC 60076 / GB 1094","value_ar": "IEC 60076 / GB 1094",
        },
        {
            "key_en": "Connection Group",   "key_ru": "Группа соединений",        "key_tr": "Bağlantı Grubu",       "key_ar": "مجموعة الاتصال",
            "value_en": "Dyn11",             "value_ru": "Dyn11",                  "value_tr": "Dyn11",              "value_ar": "Dyn11",
        },
        {
            "key_en": "Export Markets",     "key_ru": "Рынки экспорта",           "key_tr": "İhracat Pazarları",    "key_ar": "أسواق التصدير",
            "value_en": "Azerbaijan, Russia", "value_ru": "Азербайджан, Россия",  "value_tr": "Azerbaycan, Rusya",   "value_ar": "أذربيجان، روسيا",
        },
    ]

    p, action = upsert_product(t["slug"], transformer_cat, fields, specs)
    print(f"   ✓ {p.name_en} — {action}")


# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("  ✓ NEW PRODUCTS SEEDING COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\nSummary:")
print(f"  • Product Categories:  2 added (Generators, Distribution Transformers)")
print(f"  • Generator Products:  {len(generators)} added (50/100/150/300/375/500 kVA)")
print(f"  • Transformer Products:{len(transformers)} added (1600/2500 kVA × Aluminium/Copper)")
print(f"  • Languages:           EN, RU, TR, AR")
print(f"  • Images:              Placeholder set — upload real images via admin panel")
print("\nTo run on production server:")
print("  1. Copy this file to the server")
print("  2. source venv/bin/activate")
print("  3. python manage.py shell < seed_new_products.py")
print("=" * 80)
