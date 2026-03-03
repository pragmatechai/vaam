"""
Production hero slides seed - uses only stdlib (urllib) for downloading.
Run: /home/vaam/app/venv/bin/python manage.py shell < /tmp/seed_hero_prod.py
"""
import urllib.request
from pathlib import Path

MEDIA_HERO = Path("/home/vaam/app/media/hero")
MEDIA_HERO.mkdir(parents=True, exist_ok=True)

def download(url, filename):
    dest = MEDIA_HERO / filename
    if dest.exists() and dest.stat().st_size > 10000:
        print("  [SKIP]", filename)
        return "hero/" + filename
    print("  [DL]", filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; VaamBot/1.0)"})
    with urllib.request.urlopen(req, timeout=90) as resp, open(dest, "wb") as f:
        while True:
            chunk = resp.read(8192)
            if not chunk:
                break
            f.write(chunk)
    print("  [OK]", filename, dest.stat().st_size // 1024, "KB")
    return "hero/" + filename

print("=== Downloading images ===")
img_solar = download("https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?w=1920&h=1080&fit=crop&q=85&auto=format", "hero_solar_energy.jpg")
img_gen   = download("https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920&h=1080&fit=crop&q=85&auto=format", "hero_diesel_generator.jpg")
img_proj  = download("https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=1920&h=1080&fit=crop&q=85&auto=format", "hero_power_project.jpg")

from core.models import HeroSlide, Product, Project

product = Product.objects.filter(slug="generator-500-kva", is_active=True).first()
product_url = product.get_absolute_url() if product else "/en/products/"
print("Product URL:", product_url)

project = Project.objects.filter(slug="generator-supply-azerbaijan-2022-2025", is_active=True).first()
if not project:
    project = Project.objects.filter(is_active=True).order_by("-id").first()
project_url = project.get_absolute_url() if project else "/en/projects/"
print("Project URL:", project_url)

max_order = HeroSlide.objects.order_by("-order").values_list("order", flat=True).first() or 0

SLIDES = [
    {
        "order": max_order + 1, "image": img_solar,
        "title_en": "Clean Energy Solutions from China",
        "title_ru": "Решения в области чистой энергии из Китая",
        "title_tr": "Cinden Temiz Enerji Cozumleri",
        "title_ar": "حلول الطاقة النظيفة من الصين",
        "subtitle_en": "Renewable & Industrial Power",
        "subtitle_ru": "Возобновляемая и промышленная энергетика",
        "subtitle_tr": "Yenilenebilir ve Endustriyel Guc",
        "subtitle_ar": "الطاقة المتجددة والصناعية",
        "description_en": "We source and deliver solar panels, inverters, transformers and generators directly from certified Chinese factories  on time, on budget.",
        "description_ru": "Мы поставляем солнечные панели, инверторы, трансформаторы и генераторы напрямую с сертифицированных китайских заводов  в срок и в рамках бюджета.",
        "description_tr": "Gunes panellerini, invertorleri, transformatorleri ve jeneratorleri sertifikali Cin fabrikalarindan dogrudan temin ediyor ve teslim ediyoruz.",
        "description_ar": "نوفر الألواح الشمسية والمحولات والمولدات مباشرة من المصانع الصينية المعتمدة.",
        "button1_text_en": "Explore Products", "button1_text_ru": "Смотреть продукты",
        "button1_text_tr": "Urunleri Incele", "button1_text_ar": "استكشف المنتجات",
        "button1_url": "/en/products/",
        "button2_text_en": "Request a Quote", "button2_text_ru": "Запросить цену",
        "button2_text_tr": "Teklif Al", "button2_text_ar": "طلب عرض سعر",
        "button2_url": "/en/contact/",
    },
    {
        "order": max_order + 2, "image": img_gen,
        "title_en": "500 kVA Industrial Diesel Generator",
        "title_ru": "500 кВА Дизельный Генератор",
        "title_tr": "500 kVA Endustriyel Dizel Jenerator",
        "title_ar": "مولد ديزل صناعي 500 كيلوفولت أمبير",
        "subtitle_en": "Reliable Backup Power",
        "subtitle_ru": "Надёжное резервное питание",
        "subtitle_tr": "Guvenilir Yedek Guc",
        "subtitle_ar": "طاقة احتيطية موثوقة",
        "description_en": "High-performance diesel generators up to 2500 kVA  perfect for industrial facilities, hospitals and data centers. Direct factory pricing from China.",
        "description_ru": "Высокопроизводительные дизельные генераторы мощностью до 2500 кВА для промышленных объектов, больниц и дата-центров.",
        "description_tr": "2500 kVAya kadar yuksek performansli dizel jeneratorler  endustriyel tesisler icin ideal. Cin fabrikasindan dogrudan fiyat.",
        "description_ar": "مولدات ديزل عالية الأداء تصل إلى 2500 كيلوفولت أمبير  مثالية للمنشآت الصناعية والمستشفيات.",
        "button1_text_en": "View Product", "button1_text_ru": "Посмотреть продукт",
        "button1_text_tr": "Urunu Incele", "button1_text_ar": "عرض المنتج",
        "button1_url": product_url,
        "button2_text_en": "All Generators", "button2_text_ru": "Все генераторы",
        "button2_text_tr": "Tum Jeneratorler", "button2_text_ar": "جميع المولدات",
        "button2_url": "/en/products/",
    },
    {
        "order": max_order + 3, "image": img_proj,
        "title_en": "Diesel Generator Supply - Azerbaijan",
        "title_ru": "Поставка дизельных генераторов  Азербайджан",
        "title_tr": "Dizel Jenerator Tedariki - Azerbaycan",
        "title_ar": "توريد مولدات الديزل  أذربيجان",
        "subtitle_en": "Completed Project",
        "subtitle_ru": "Завершённый проект",
        "subtitle_tr": "Tamamlanan Proje",
        "subtitle_ar": "مشروع مكتمل",
        "description_en": "Multi-year supply of diesel generator sets to the Republic of Azerbaijan  50 kVA to 500 kVA units sourced from certified Chinese manufacturers.",
        "description_ru": "Многолетняя поставка дизельных генераторных установок в Азербайджанскую Республику  агрегаты от 50 до 500 кВА.",
        "description_tr": "Azerbaycan Cumhuriyetine cok yillik dizel jenerator seti tedari  50 kVAdan 500 kVAya kadar sertifikali Cin ureticilerinden.",
        "description_ar": "توريد متعدد السنوات لمجموعات مولدات الديزل إلى جمهورية أذربيجان.",
        "button1_text_en": "See Project Details", "button1_text_ru": "Подробнее о проекте",
        "button1_text_tr": "Proje Detaylari", "button1_text_ar": "تفاصيل المشروع",
        "button1_url": project_url,
        "button2_text_en": "All Projects", "button2_text_ru": "Все проекты",
        "button2_text_tr": "Tum Projeler", "button2_text_ar": "جميع المشاريع",
        "button2_url": "/en/projects/",
    },
]

print("\n=== Creating Hero Slides ===")
for sd in SLIDES:
    if HeroSlide.objects.filter(title_en=sd["title_en"]).exists():
        print("  [SKIP]", sd["title_en"])
        continue
    slide = HeroSlide(order=sd["order"], is_active=True, button1_url=sd["button1_url"], button2_url=sd["button2_url"])
    slide.image = sd["image"]
    for lang in ["en", "ru", "tr", "ar"]:
        for field in ["title", "subtitle", "description", "button1_text", "button2_text"]:
            k = field + "_" + lang
            if k in sd:
                setattr(slide, k, sd[k])
    slide.save()
    print("  [OK] id=%d order=%d | %s" % (slide.id, slide.order, slide.title_en))

print("\n=== DONE === Total slides:", HeroSlide.objects.count())
for s in HeroSlide.objects.order_by("order"):
    print("  [%d] order=%d img=%s btn1=%s" % (s.id, s.order, s.image, s.button1_url))
