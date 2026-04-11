"""
VAAM Content Update Seed Script
================================
Populates database with accurate company data from content.md
with translations in all 4 project languages: en, ru, tr, ar.

Run: python manage.py shell < seed_content_update.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()

from core.models import (
    CompanyInfo, CompanyFeature, HeroSlide,
    Service, ServiceCategory, ProcessStep, FAQ
)

print("=" * 60)
print("  VAAM Content Update — Seeding accurate company data")
print("=" * 60)

# ============================================================
# 1. COMPANY INFO
# ============================================================
print("\n[1/6] Updating CompanyInfo...")
info, _ = CompanyInfo.objects.get_or_create(pk=1)

# -- title --
info.title_en = "VAAM Import and Export Trading Co., LTD"
info.title_ru = "VAAM Import and Export Trading Co., LTD"
info.title_tr = "VAAM Import and Export Trading Co., LTD"
info.title_ar = "VAAM Import and Export Trading Co., LTD"

# -- subtitle --
info.subtitle_en = "Professional Sourcing & Procurement Solutions in China"
info.subtitle_ru = "Профессиональные решения по поиску и закупке товаров в Китае"
info.subtitle_tr = "Çin'de Profesyonel Tedarik ve Satın Alma Çözümleri"
info.subtitle_ar = "حلول التوريد والمشتريات المهنية في الصين"

# -- description --
info.description_en = (
    "VAAM Import and Export Trading Co., LTD is a professional sourcing and procurement company operating in China. "
    "We support international clients in organizing product sourcing from China in an efficient, transparent, and secure manner. "
    "Our primary goal is to provide our clients with the right product, at the right price, from reliable suppliers."
)
info.description_ru = (
    "VAAM Import and Export Trading Co., LTD — профессиональная компания по поиску и закупке товаров, работающая в Китае. "
    "Мы помогаем международным клиентам организовать закупку продукции из Китая эффективно, прозрачно и безопасно. "
    "Наша главная цель — обеспечить клиентов нужным товаром по оптимальной цене от надёжных поставщиков."
)
info.description_tr = (
    "VAAM Import and Export Trading Co., LTD, Çin'de faaliyet gösteren profesyonel bir tedarik ve satın alma şirketidir. "
    "Uluslararası müşterilerimize Çin'den ürün tedarikini verimli, şeffaf ve güvenli bir şekilde organize etmede destek oluyoruz. "
    "Temel amacımız — müşterilerimize doğru ürünü, doğru fiyata, güvenilir tedarikçilerden temin etmektir."
)
info.description_ar = (
    "شركة VAAM للاستيراد والتصدير والتجارة المحدودة هي شركة متخصصة في التوريد والمشتريات تعمل في الصين. "
    "نحن ندعم العملاء الدوليين في تنظيم توريد المنتجات من الصين بطريقة فعالة وشفافة وآمنة. "
    "هدفنا الرئيسي هو توفير المنتج المناسب لعملائنا بالسعر المناسب من موردين موثوقين."
)

# -- mission --
info.mission_en = (
    "Our mission is to make product sourcing from China simpler, safer, and more efficient for businesses, "
    "and to build long-term, reliable partnerships."
)
info.mission_ru = (
    "Наша миссия — сделать закупку товаров из Китая более простой, безопасной и эффективной для бизнеса, "
    "а также выстраивать долгосрочные и надёжные партнёрские отношения."
)
info.mission_tr = (
    "Misyonumuz — işletmeler için Çin'den ürün tedarikini daha basit, güvenli ve verimli hale getirmek "
    "ve uzun vadeli, güvenilir iş birlikleri kurmaktır."
)
info.mission_ar = (
    "مهمتنا هي جعل توريد المنتجات من الصين أبسط وأكثر أماناً وكفاءة للشركات، "
    "وبناء شراكات طويلة الأمد وموثوقة."
)

# -- vision --
info.vision_en = (
    "To be the most trusted sourcing partner between China and the world, "
    "providing seamless procurement solutions that empower businesses to grow globally."
)
info.vision_ru = (
    "Стать самым надёжным партнёром по закупкам между Китаем и миром, "
    "предоставляя безупречные решения по снабжению, которые помогают бизнесу расти глобально."
)
info.vision_tr = (
    "Çin ile dünya arasında en güvenilir tedarik ortağı olmak, "
    "işletmelerin küresel ölçekte büyümesini sağlayan kusursuz satın alma çözümleri sunmak."
)
info.vision_ar = (
    "أن نكون الشريك الأكثر موثوقية في التوريد بين الصين والعالم، "
    "وتقديم حلول مشتريات سلسة تمكّن الشركات من النمو عالمياً."
)

# -- values --
info.values_en = (
    "We operate not just as intermediaries, but as trusted business partners.\n\n"
    "• Direct collaboration with manufacturers\n"
    "• Supplier verification and selection\n"
    "• Price and terms optimization\n"
    "• Full control over the order process\n\n"
    "We provide our clients with complete transparency and timely updates at every stage."
)
info.values_ru = (
    "Мы работаем не просто как посредники, а как надёжные бизнес-партнёры.\n\n"
    "• Прямое сотрудничество с производителями\n"
    "• Проверка и отбор поставщиков\n"
    "• Оптимизация цен и условий\n"
    "• Полный контроль над процессом заказа\n\n"
    "Мы обеспечиваем клиентам полную прозрачность и оперативную информацию на каждом этапе."
)
info.values_tr = (
    "Yalnızca aracı olarak değil, güvenilir bir iş ortağı olarak faaliyet gösteriyoruz.\n\n"
    "• Üreticilerle doğrudan iş birliği\n"
    "• Tedarikçi doğrulama ve seçimi\n"
    "• Fiyat ve koşulların optimizasyonu\n"
    "• Sipariş sürecinin tam kontrolü\n\n"
    "Her aşamada müşterilerimize tam şeffaflık ve zamanında bilgi sunuyoruz."
)
info.values_ar = (
    "نحن نعمل ليس فقط كوسطاء، بل كشركاء أعمال موثوقين.\n\n"
    "• التعاون المباشر مع المصنعين\n"
    "• التحقق من الموردين واختيارهم\n"
    "• تحسين الأسعار والشروط\n"
    "• السيطرة الكاملة على عملية الطلب\n\n"
    "نقدم لعملائنا الشفافية الكاملة والمعلومات الفورية في كل مرحلة."
)

info.headquarters_en = "China"
info.headquarters_ru = "Китай"
info.headquarters_tr = "Çin"
info.headquarters_ar = "الصين"

info.save()
print("  ✓ CompanyInfo updated")

# ============================================================
# 2. COMPANY FEATURES (4 key differentiators)
# ============================================================
print("\n[2/6] Updating CompanyFeatures...")
CompanyFeature.objects.all().delete()

features_data = [
    {
        'icon': 'fas fa-industry',
        'order': 1,
        'title_en': 'Direct Manufacturer Partnership',
        'title_ru': 'Прямое сотрудничество с производителями',
        'title_tr': 'Doğrudan Üretici İş Birliği',
        'title_ar': 'شراكة مباشرة مع المصنعين',
        'description_en': 'We work directly with manufacturers in China, eliminating middlemen to ensure the best prices and quality for our clients.',
        'description_ru': 'Мы работаем напрямую с производителями в Китае, исключая посредников, чтобы обеспечить лучшие цены и качество для наших клиентов.',
        'description_tr': 'Çin\'deki üreticilerle doğrudan çalışarak aracıları ortadan kaldırıyor, müşterilerimize en iyi fiyat ve kaliteyi sağlıyoruz.',
        'description_ar': 'نعمل مباشرة مع المصنعين في الصين، مما يلغي الوسطاء لضمان أفضل الأسعار والجودة لعملائنا.',
    },
    {
        'icon': 'fas fa-shield-alt',
        'order': 2,
        'title_en': 'Quality Control & Inspection',
        'title_ru': 'Контроль качества и инспекция',
        'title_tr': 'Kalite Kontrol ve Denetim',
        'title_ar': 'مراقبة الجودة والتفتيش',
        'description_en': 'Every product is inspected at the factory before shipment. We provide photos, videos, and detailed inspection reports to our clients.',
        'description_ru': 'Каждый товар проверяется на заводе перед отправкой. Мы предоставляем фотографии, видео и подробные акты инспекции клиентам.',
        'description_tr': 'Her ürün sevkiyat öncesinde fabrikada denetlenir. Müşterilerimize fotoğraf, video ve detaylı denetim raporları sunuyoruz.',
        'description_ar': 'يتم فحص كل منتج في المصنع قبل الشحن. نقدم لعملائنا صوراً وفيديوهات وتقارير فحص مفصلة.',
    },
    {
        'icon': 'fas fa-eye',
        'order': 3,
        'title_en': 'Full Transparency',
        'title_ru': 'Полная прозрачность',
        'title_tr': 'Tam Şeffaflık',
        'title_ar': 'شفافية كاملة',
        'description_en': 'We keep our clients informed at every stage with real-time updates, real product photos, and clear pricing under EXW and FOB terms.',
        'description_ru': 'Мы информируем клиентов на каждом этапе: актуальные обновления, реальные фото продукции и прозрачные цены на условиях EXW и FOB.',
        'description_tr': 'Her aşamada müşterilerimizi anlık güncellemeler, gerçek ürün fotoğrafları ve EXW/FOB koşullarıyla net fiyatlarla bilgilendiriyoruz.',
        'description_ar': 'نبقي عملاءنا على اطلاع في كل مرحلة من خلال تحديثات فورية وصور حقيقية للمنتجات وأسعار واضحة بشروط EXW و FOB.',
    },
    {
        'icon': 'fas fa-tags',
        'order': 4,
        'title_en': 'Price & Terms Optimization',
        'title_ru': 'Оптимизация цен и условий',
        'title_tr': 'Fiyat ve Koşul Optimizasyonu',
        'title_ar': 'تحسين الأسعار والشروط',
        'description_en': 'We negotiate the best possible prices and commercial terms on your behalf, ensuring maximum value for every order.',
        'description_ru': 'Мы договариваемся о лучших ценах и коммерческих условиях от имени клиента, обеспечивая максимальную выгоду для каждого заказа.',
        'description_tr': 'Sizin adınıza en iyi fiyatları ve ticari koşulları müzakere ederek her sipariş için maksimum değeri sağlıyoruz.',
        'description_ar': 'نتفاوض على أفضل الأسعار والشروط التجارية نيابة عنكم، مما يضمن أقصى قيمة لكل طلب.',
    },
]

for f_data in features_data:
    CompanyFeature.objects.create(**f_data)
print(f"  ✓ {len(features_data)} features created")

# ============================================================
# 3. HERO SLIDES
# ============================================================
print("\n[3/6] Updating HeroSlides...")
HeroSlide.objects.all().delete()

slides_data = [
    {
        'order': 1,
        'title_en': 'Your Trusted Sourcing Partner in China',
        'title_ru': 'Ваш надёжный партнёр по закупкам в Китае',
        'title_tr': 'Çin\'deki Güvenilir Tedarik Ortağınız',
        'title_ar': 'شريكك الموثوق للتوريد في الصين',
        'subtitle_en': 'Professional Procurement Solutions',
        'subtitle_ru': 'Профессиональные решения по закупкам',
        'subtitle_tr': 'Profesyonel Tedarik Çözümleri',
        'subtitle_ar': 'حلول مشتريات احترافية',
        'description_en': 'VAAM Import and Export Trading Co., LTD supports international clients with efficient, transparent, and secure product sourcing from China.',
        'description_ru': 'VAAM Import and Export Trading Co., LTD помогает международным клиентам с эффективной, прозрачной и безопасной закупкой товаров из Китая.',
        'description_tr': 'VAAM Import and Export Trading Co., LTD, uluslararası müşterilere Çin\'den verimli, şeffaf ve güvenli ürün tedariki konusunda destek sağlar.',
        'description_ar': 'تدعم شركة VAAM للاستيراد والتصدير العملاء الدوليين في توريد المنتجات من الصين بكفاءة وشفافية وأمان.',
        'button1_text_en': 'Get a Quote',
        'button1_text_ru': 'Получить предложение',
        'button1_text_tr': 'Teklif Alın',
        'button1_text_ar': 'احصل على عرض سعر',
        'button1_url': '/en/contact/',
        'button2_text_en': 'Our Services',
        'button2_text_ru': 'Наши услуги',
        'button2_text_tr': 'Hizmetlerimiz',
        'button2_text_ar': 'خدماتنا',
        'button2_url': '/en/services/',
        'image': 'hero/slide1.jpg',
    },
    {
        'order': 2,
        'title_en': 'Right Product. Right Price. Reliable Supplier.',
        'title_ru': 'Нужный товар. Лучшая цена. Надёжный поставщик.',
        'title_tr': 'Doğru Ürün. Doğru Fiyat. Güvenilir Tedarikçi.',
        'title_ar': 'المنتج المناسب. السعر المناسب. المورد الموثوق.',
        'subtitle_en': 'Direct From Manufacturers',
        'subtitle_ru': 'Напрямую от производителей',
        'subtitle_tr': 'Doğrudan Üreticilerden',
        'subtitle_ar': 'مباشرة من المصنعين',
        'description_en': 'We find, negotiate, and deliver the products you need — working directly with Chinese manufacturers to ensure quality and competitive pricing.',
        'description_ru': 'Мы находим, согласовываем и доставляем нужную вам продукцию — работая напрямую с китайскими производителями для обеспечения качества и конкурентных цен.',
        'description_tr': 'İhtiyacınız olan ürünleri bulur, müzakere eder ve teslim ederiz — kalite ve rekabetçi fiyat için Çinli üreticilerle doğrudan çalışırız.',
        'description_ar': 'نجد ونتفاوض ونسلم المنتجات التي تحتاجها — نعمل مباشرة مع المصنعين الصينيين لضمان الجودة والأسعار التنافسية.',
        'button1_text_en': 'View Products',
        'button1_text_ru': 'Смотреть продукцию',
        'button1_text_tr': 'Ürünleri Görün',
        'button1_text_ar': 'عرض المنتجات',
        'button1_url': '/en/products/',
        'button2_text_en': 'Submit Inquiry',
        'button2_text_ru': 'Отправить запрос',
        'button2_text_tr': 'Sorgu Gönderin',
        'button2_text_ar': 'إرسال استفسار',
        'button2_url': '/en/inquiry/',
        'image': 'hero/slide2.jpg',
    },
    {
        'order': 3,
        'title_en': 'End-to-End Procurement & Quality Control',
        'title_ru': 'Полный цикл закупок и контроль качества',
        'title_tr': 'Uçtan Uca Tedarik ve Kalite Kontrol',
        'title_ar': 'المشتريات الشاملة ومراقبة الجودة',
        'subtitle_en': 'From Factory to Your Door',
        'subtitle_ru': 'От завода до вашей двери',
        'subtitle_tr': 'Fabrikadan Kapınıza',
        'subtitle_ar': 'من المصنع إلى بابك',
        'description_en': 'Supplier selection, quality inspection, customs documentation, and delivery coordination — we handle every step so you can focus on your business.',
        'description_ru': 'Выбор поставщика, проверка качества, таможенная документация и координация доставки — мы берём на себя каждый этап, чтобы вы могли сосредоточиться на бизнесе.',
        'description_tr': 'Tedarikçi seçimi, kalite denetimi, gümrük belgeleri ve teslimat koordinasyonu — siz işinize odaklanın, her adımı biz yönetiyoruz.',
        'description_ar': 'اختيار المورد، فحص الجودة، التوثيق الجمركي، وتنسيق التسليم — نتولى كل خطوة حتى تتمكن من التركيز على عملك.',
        'button1_text_en': 'Learn More',
        'button1_text_ru': 'Подробнее',
        'button1_text_tr': 'Daha Fazla',
        'button1_text_ar': 'اعرف المزيد',
        'button1_url': '/en/about/',
        'button2_text_en': 'Contact Us',
        'button2_text_ru': 'Свяжитесь с нами',
        'button2_text_tr': 'Bize Ulaşın',
        'button2_text_ar': 'اتصل بنا',
        'button2_url': '/en/contact/',
        'image': 'hero/slide3.jpg',
    },
]

for s_data in slides_data:
    HeroSlide.objects.create(**s_data)
print(f"  ✓ {len(slides_data)} hero slides created")

# ============================================================
# 4. SERVICES (8 services from content.md)
# ============================================================
print("\n[4/6] Updating Services...")
Service.objects.all().delete()
ServiceCategory.objects.all().delete()

# Create a general category
cat, _ = ServiceCategory.objects.get_or_create(
    slug='procurement-services',
    defaults={
        'name_en': 'Procurement Services',
        'name_ru': 'Услуги по закупкам',
        'name_tr': 'Tedarik Hizmetleri',
        'name_ar': 'خدمات التوريد',
        'order': 1,
    }
)

services_data = [
    {
        'slug': 'product-supply',
        'icon': 'fas fa-boxes-stacked',
        'order': 1,
        'title_en': 'Product Supply & Procurement',
        'title_ru': 'Поставка и закупка продукции',
        'title_tr': 'Ürün Tedariki ve Temini',
        'title_ar': 'توريد وشراء المنتجات',
        'short_description_en': 'We organize the supply of products in various categories directly from manufacturers in China, tailored to your specific requirements.',
        'short_description_ru': 'Мы организуем поставку продукции различных категорий напрямую от производителей в Китае, с учётом ваших конкретных требований.',
        'short_description_tr': 'Müşterilerimizin taleplerine uygun olarak Çin\'deki üreticilerden çeşitli kategorilerde doğrudan ürün tedarikini organize ediyoruz.',
        'short_description_ar': 'ننظم توريد المنتجات في فئات مختلفة مباشرة من المصنعين في الصين، وفقاً لمتطلباتكم المحددة.',
        'description_en': 'VAAM Import and Export Trading Co., LTD organizes the supply of products in various categories directly from manufacturers in China, tailored to client requirements. We find the brand and manufacturer that best suits your needs and present the most optimal option.',
        'description_ru': 'VAAM Import and Export Trading Co., LTD организует поставку продукции различных категорий напрямую от производителей в Китае по запросу клиента. Мы находим бренд и производителя, наиболее соответствующего вашим потребностям, и предлагаем оптимальный вариант.',
        'description_tr': 'VAAM Import and Export Trading Co., LTD, müşteri taleplerine uygun olarak Çin\'deki üreticilerden çeşitli kategorilerde doğrudan ürün tedarikini organize eder. İhtiyacınıza en uygun marka ve üreticiyi bularak en optimal seçeneği sunarız.',
        'description_ar': 'تنظم شركة VAAM للاستيراد والتصدير توريد المنتجات في فئات مختلفة مباشرة من المصنعين في الصين وفقاً لمتطلبات العميل. نجد العلامة التجارية والمصنع الأنسب لاحتياجاتكم ونقدم الخيار الأمثل.',
        'features_en': 'Sourcing from verified manufacturers\nBrand and supplier matching\nBulk and sample orders\nMulti-category procurement',
        'features_ru': 'Закупка у проверенных производителей\nПодбор бренда и поставщика\nОптовые и пробные заказы\nЗакупки в разных категориях',
        'features_tr': 'Doğrulanmış üreticilerden tedarik\nMarka ve tedarikçi eşleştirme\nToptan ve numune siparişleri\nÇoklu kategori tedariki',
        'features_ar': 'التوريد من مصنعين معتمدين\nمطابقة العلامة التجارية والمورد\nطلبات بالجملة وعينات\nالمشتريات متعددة الفئات',
    },
    {
        'slug': 'supplier-selection',
        'icon': 'fas fa-search',
        'order': 2,
        'title_en': 'Supplier Selection & Verification',
        'title_ru': 'Выбор и проверка поставщиков',
        'title_tr': 'Tedarikçi Seçimi ve Doğrulama',
        'title_ar': 'اختيار الموردين والتحقق منهم',
        'short_description_en': 'Suppliers are carefully selected based on quality, price, production capacity, and reliability. We present multiple alternatives for your evaluation.',
        'short_description_ru': 'Поставщики тщательно отбираются по критериям качества, цены, производственных мощностей и надёжности. Мы предлагаем несколько альтернатив для оценки.',
        'short_description_tr': 'Tedarikçiler kalite, fiyat, üretim kapasitesi ve güvenilirlik temelinde titizlikle seçilir. Değerlendirmeniz için birden fazla alternatif sunuyoruz.',
        'short_description_ar': 'يتم اختيار الموردين بعناية بناءً على الجودة والسعر والقدرة الإنتاجية والموثوقية. نقدم بدائل متعددة لتقييمكم.',
        'description_en': 'Suppliers are carefully selected based on quality, price, production capacity, and reliability. We present multiple alternatives tailored to your requirements so you can make the best informed decision.',
        'description_ru': 'Поставщики тщательно отбираются по критериям качества, цены, производственных мощностей и надёжности. Мы предлагаем несколько альтернатив с учётом ваших требований для принятия взвешенного решения.',
        'description_tr': 'Tedarikçiler kalite, fiyat, üretim kapasitesi ve güvenilirlik temelinde titizlikle seçilir. Taleplerinize uygun birden fazla alternatif sunarak en doğru kararı vermenizi sağlıyoruz.',
        'description_ar': 'يتم اختيار الموردين بعناية بناءً على الجودة والسعر والقدرة الإنتاجية والموثوقية. نقدم بدائل متعددة مصممة وفقاً لمتطلباتكم لاتخاذ القرار الأفضل.',
        'features_en': 'Factory capability assessment\nQuality and compliance checks\nMultiple supplier comparison\nRisk evaluation and due diligence',
        'features_ru': 'Оценка возможностей завода\nПроверка качества и соответствия\nСравнение нескольких поставщиков\nОценка рисков и аудит',
        'features_tr': 'Fabrika yetkinlik değerlendirmesi\nKalite ve uyumluluk kontrolleri\nÇoklu tedarikçi karşılaştırması\nRisk değerlendirmesi ve durum tespiti',
        'features_ar': 'تقييم قدرات المصنع\nفحوصات الجودة والامتثال\nمقارنة موردين متعددين\nتقييم المخاطر والعناية الواجبة',
    },
    {
        'slug': 'quality-inspection',
        'icon': 'fas fa-clipboard-check',
        'order': 3,
        'title_en': 'Quality Inspection',
        'title_ru': 'Проверка качества',
        'title_tr': 'Kalite Denetimi',
        'title_ar': 'فحص الجودة',
        'short_description_en': 'Products are inspected on-site at the factory before shipment. We provide clients with photos, videos, and detailed inspection reports.',
        'short_description_ru': 'Товары проверяются на месте на заводе перед отгрузкой. Мы предоставляем клиентам фотографии, видео и детальные акты проверки.',
        'short_description_tr': 'Ürünler sevkiyat öncesinde fabrikada yerinde denetlenir. Müşterilerimize fotoğraf, video ve detaylı denetim raporları sunuyoruz.',
        'short_description_ar': 'يتم فحص المنتجات في الموقع بالمصنع قبل الشحن. نقدم لعملائنا صوراً وفيديوهات وتقارير فحص مفصلة.',
        'description_en': 'Products are inspected on-site at the factory before shipment. Clients receive photos, videos, and a comprehensive inspection report to ensure full confidence in the quality of their order.',
        'description_ru': 'Товары проверяются на месте на заводе перед отгрузкой. Клиенты получают фотографии, видео и полный отчёт об инспекции для полной уверенности в качестве заказа.',
        'description_tr': 'Ürünler sevkiyat öncesinde fabrikada yerinde denetlenir. Müşteriler, siparişlerinin kalitesine tam güven duymak için fotoğraf, video ve kapsamlı denetim raporu alır.',
        'description_ar': 'يتم فحص المنتجات في الموقع بالمصنع قبل الشحن. يحصل العملاء على صور وفيديوهات وتقرير فحص شامل لضمان الثقة الكاملة في جودة طلبهم.',
        'features_en': 'Pre-shipment factory inspection\nPhoto and video documentation\nDetailed inspection reports\nPackaging quality control',
        'features_ru': 'Предотгрузочная инспекция на заводе\nФото- и видеодокументация\nДетальные отчёты о проверке\nКонтроль качества упаковки',
        'features_tr': 'Sevkiyat öncesi fabrika denetimi\nFotoğraf ve video belgeleme\nDetaylı denetim raporları\nAmbalaj kalite kontrolü',
        'features_ar': 'تفتيش المصنع قبل الشحن\nتوثيق بالصور والفيديو\nتقارير فحص مفصلة\nمراقبة جودة التغليف',
    },
    {
        'slug': 'logistics-delivery',
        'icon': 'fas fa-truck-fast',
        'order': 4,
        'title_en': 'Logistics & Delivery Coordination',
        'title_ru': 'Логистика и координация доставки',
        'title_tr': 'Lojistik ve Teslimat Koordinasyonu',
        'title_ar': 'اللوجستيات وتنسيق التسليم',
        'short_description_en': 'Products are delivered under EXW or FOB terms. We coordinate handover to your logistics partner and provide reliable forwarding recommendations when needed.',
        'short_description_ru': 'Продукция поставляется на условиях EXW или FOB. Мы координируем передачу вашему логистическому партнёру и при необходимости рекомендуем надёжных экспедиторов.',
        'short_description_tr': 'Ürünler EXW veya FOB koşullarıyla teslim edilir. Lojistik ortağınıza devir koordinasyonu sağlar, gerektiğinde güvenilir nakliye partnerlerini öneriyoruz.',
        'short_description_ar': 'يتم تسليم المنتجات بشروط EXW أو FOB. ننسق التسليم لشريككم اللوجستي ونقدم توصيات بشركات شحن موثوقة عند الحاجة.',
        'description_en': 'Our company does not provide international shipping services directly. Products are delivered under EXW (Ex Works) or FOB (Free on Board) terms to your chosen logistics partner. When needed, we can recommend reliable forwarding partners.',
        'description_ru': 'Наша компания не осуществляет международную доставку напрямую. Продукция поставляется на условиях EXW (самовывоз с завода) или FOB (до порта Китая) вашему выбранному логистическому партнёру. При необходимости мы можем рекомендовать надёжных экспедиторов.',
        'description_tr': 'Şirketimiz doğrudan uluslararası nakliye hizmeti sunmamaktadır. Ürünler EXW (fabrikadan teslim) veya FOB (Çin limanına kadar) koşullarıyla seçtiğiniz lojistik ortağınıza teslim edilir. Gerektiğinde güvenilir nakliye partnerleri önerebiliriz.',
        'description_ar': 'لا تقدم شركتنا خدمات الشحن الدولي مباشرة. يتم تسليم المنتجات بشروط EXW (تسليم المصنع) أو FOB (تسليم ميناء الصين) لشريككم اللوجستي المختار. عند الحاجة، يمكننا التوصية بشركاء شحن موثوقين.',
        'features_en': 'EXW and FOB delivery terms\nLogistics partner coordination\nReliable forwarding recommendations\nProduct tracking until FOB stage',
        'features_ru': 'Условия поставки EXW и FOB\nКоординация с логистическим партнёром\nРекомендации надёжных экспедиторов\nОтслеживание до стадии FOB',
        'features_tr': 'EXW ve FOB teslimat koşulları\nLojistik partner koordinasyonu\nGüvenilir nakliye önerileri\nFOB aşamasına kadar ürün takibi',
        'features_ar': 'شروط تسليم EXW و FOB\nتنسيق مع الشريك اللوجستي\nتوصيات بشركات شحن موثوقة\nتتبع المنتج حتى مرحلة FOB',
    },
    {
        'slug': 'customs-clearance',
        'icon': 'fas fa-file-invoice',
        'order': 5,
        'title_en': 'Customs Documentation Support',
        'title_ru': 'Поддержка таможенного оформления',
        'title_tr': 'Gümrük Belgelendirme Desteği',
        'title_ar': 'دعم التوثيق الجمركي',
        'short_description_en': 'We prepare all necessary export documents including Invoice, Packing List, and other customs paperwork to ensure a smooth import process.',
        'short_description_ru': 'Мы подготавливаем все необходимые экспортные документы, включая инвойс, упаковочный лист и прочие таможенные документы для беспроблемного импорта.',
        'short_description_tr': 'Sorunsuz bir ithalat süreci için Invoice, Packing List ve diğer gümrük belgeleri dahil tüm gerekli ihracat belgelerini hazırlıyoruz.',
        'short_description_ar': 'نعد جميع مستندات التصدير اللازمة بما في ذلك الفاتورة وقائمة التعبئة والأوراق الجمركية الأخرى لضمان عملية استيراد سلسة.',
        'description_en': 'VAAM Import and Export Trading Co., LTD provides comprehensive customs documentation support. All necessary documents (Invoice, Packing List, and other export documents) are prepared and provided. We offer operational support during the import process to ensure customs procedures are carried out correctly, quickly, and without issues.',
        'description_ru': 'VAAM Import and Export Trading Co., LTD обеспечивает комплексную поддержку таможенного оформления. Все необходимые документы (инвойс, упаковочный лист и другие экспортные документы) подготавливаются и предоставляются. Мы оказываем оперативную поддержку в процессе импорта для правильного, быстрого и беспроблемного прохождения таможенных процедур.',
        'description_tr': 'VAAM Import and Export Trading Co., LTD kapsamlı gümrük belgelendirme desteği sağlar. Tüm gerekli belgeler (Invoice, Packing List ve diğer ihracat belgeleri) hazırlanır ve sunulur. İthalat sürecinde gümrük prosedürlerinin doğru, hızlı ve sorunsuz yürütülmesi için operasyonel destek sunuyoruz.',
        'description_ar': 'توفر شركة VAAM للاستيراد والتصدير دعماً شاملاً للتوثيق الجمركي. يتم إعداد وتقديم جميع المستندات اللازمة (الفاتورة وقائمة التعبئة ومستندات التصدير الأخرى). نقدم دعماً تشغيلياً خلال عملية الاستيراد لضمان تنفيذ الإجراءات الجمركية بشكل صحيح وسريع وبدون مشاكل.',
        'features_en': 'Commercial Invoice preparation\nPacking List documentation\nExport documents and certificates\nImport process coordination',
        'features_ru': 'Подготовка коммерческого инвойса\nОформление упаковочного листа\nЭкспортные документы и сертификаты\nКоординация процесса импорта',
        'features_tr': 'Commercial Invoice hazırlığı\nPacking List belgeleme\nİhracat belgeleri ve sertifikaları\nİthalat süreci koordinasyonu',
        'features_ar': 'إعداد الفاتورة التجارية\nتوثيق قائمة التعبئة\nمستندات وشهادات التصدير\nتنسيق عملية الاستيراد',
    },
    {
        'slug': 'technical-consulting',
        'icon': 'fas fa-headset',
        'order': 6,
        'title_en': 'Technical Consulting',
        'title_ru': 'Техническое консультирование',
        'title_tr': 'Teknik Danışmanlık',
        'title_ar': 'الاستشارات الفنية',
        'short_description_en': 'We provide technical support for choosing the right product. Various manufacturers and alternatives are compared to offer the best solution.',
        'short_description_ru': 'Мы оказываем техническую поддержку при выборе подходящего товара. Сравниваем различных производителей и альтернативы для предложения лучшего решения.',
        'short_description_tr': 'Doğru ürünün seçimi için teknik destek sağlıyoruz. Çeşitli üreticiler ve alternatifler karşılaştırılarak en iyi çözüm sunulur.',
        'short_description_ar': 'نقدم الدعم الفني لاختيار المنتج المناسب. تتم مقارنة مختلف المصنعين والبدائل لتقديم أفضل حل.',
        'description_en': 'Technical support is provided to help select the most suitable product for your needs. We compare various manufacturers and alternatives to propose the most optimal solution for your specific requirements and budget.',
        'description_ru': 'Техническая поддержка помогает выбрать наиболее подходящий товар для ваших нужд. Мы сравниваем различных производителей и альтернативы, чтобы предложить оптимальное решение под ваши требования и бюджет.',
        'description_tr': 'İhtiyaçlarınıza en uygun ürünün seçilmesi için teknik destek sağlanır. Çeşitli üreticiler ve alternatifler karşılaştırılarak özel gereksinimleriniz ve bütçeniz için en optimal çözüm sunulur.',
        'description_ar': 'يتم تقديم الدعم الفني للمساعدة في اختيار المنتج الأنسب لاحتياجاتكم. نقارن بين مختلف المصنعين والبدائل لاقتراح الحل الأمثل وفقاً لمتطلباتكم وميزانيتكم.',
        'features_en': 'Product specification analysis\nManufacturer comparison\nOptimal solution recommendation\nTechnical documentation review',
        'features_ru': 'Анализ спецификаций продукции\nСравнение производителей\nРекомендация оптимального решения\nОбзор технической документации',
        'features_tr': 'Ürün teknik şartname analizi\nÜretici karşılaştırması\nOptimal çözüm önerisi\nTeknik dokümantasyon incelemesi',
        'features_ar': 'تحليل مواصفات المنتج\nمقارنة المصنعين\nتوصية بالحل الأمثل\nمراجعة الوثائق الفنية',
    },
    {
        'slug': 'installation-support',
        'icon': 'fas fa-tools',
        'order': 7,
        'title_en': 'Installation Guidance',
        'title_ru': 'Поддержка при монтаже',
        'title_tr': 'Kurulum Desteği',
        'title_ar': 'دعم التركيب',
        'short_description_en': 'While we do not provide on-site installation, all technical documents and manuals from manufacturers are provided to support your installation process.',
        'short_description_ru': 'Хотя мы не предоставляем монтаж на месте, вся техническая документация и инструкции от производителей передаются для поддержки вашего процесса установки.',
        'short_description_tr': 'Yerinde kurulum hizmeti sunmasak da, kurulum sürecinizi desteklemek için üreticilerin tüm teknik belgeleri ve kılavuzları tarafınıza sağlanır.',
        'short_description_ar': 'على الرغم من أننا لا نوفر التركيب في الموقع، يتم تقديم جميع الوثائق الفنية والأدلة من المصنعين لدعم عملية التركيب لديكم.',
        'description_en': 'Our company does not provide on-site installation services. However, all technical documents and instruction manuals provided by the manufacturer are forwarded to the client to support their installation process.',
        'description_ru': 'Наша компания не предоставляет услуги по монтажу на месте. Однако вся техническая документация и инструкции по эксплуатации от производителя передаются клиенту для поддержки процесса установки.',
        'description_tr': 'Şirketimiz yerinde kurulum hizmeti sunmamaktadır. Ancak, üretici tarafından sağlanan tüm teknik belgeler ve kullanım kılavuzları, kurulum sürecini desteklemek için müşteriye iletilir.',
        'description_ar': 'لا تقدم شركتنا خدمات التركيب في الموقع. ومع ذلك، يتم تسليم جميع الوثائق الفنية وأدلة التعليمات المقدمة من المصنع إلى العميل لدعم عملية التركيب.',
        'features_en': 'Manufacturer technical manuals\nInstallation guidelines\nProduct specifications\nRemote technical support coordination',
        'features_ru': 'Технические руководства производителя\nИнструкции по установке\nСпецификации продукции\nКоординация удалённой технической поддержки',
        'features_tr': 'Üretici teknik kılavuzları\nKurulum yönergeleri\nÜrün teknik şartnameleri\nUzaktan teknik destek koordinasyonu',
        'features_ar': 'أدلة المصنع الفنية\nإرشادات التركيب\nمواصفات المنتج\nتنسيق الدعم الفني عن بُعد',
    },
    {
        'slug': 'after-sales-service',
        'icon': 'fas fa-handshake',
        'order': 8,
        'title_en': 'After-Sales Service',
        'title_ru': 'Послепродажное обслуживание',
        'title_tr': 'Satış Sonrası Hizmet',
        'title_ar': 'خدمة ما بعد البيع',
        'short_description_en': 'We coordinate warranty claims and technical issues between you and the manufacturer, and assist with spare parts sourcing and ordering.',
        'short_description_ru': 'Мы координируем гарантийные обращения и технические вопросы между вами и производителем, помогаем с поиском и заказом запасных частей.',
        'short_description_tr': 'Garanti talepleri ve teknik sorunlarda sizinle üretici arasında koordinasyon sağlıyor, yedek parça tedariki ve siparişinde destek oluyoruz.',
        'short_description_ar': 'ننسق مطالبات الضمان والمسائل الفنية بينكم وبين المصنع، ونساعد في توريد قطع الغيار وطلبها.',
        'description_en': 'We ensure coordination between the client and the manufacturer for warranty and technical issues. Support is provided for finding and ordering spare parts, ensuring timely resolution of any post-purchase concerns.',
        'description_ru': 'Мы обеспечиваем координацию между клиентом и производителем по гарантийным и техническим вопросам. Оказывается поддержка в поиске и заказе запасных частей, обеспечивая своевременное решение любых вопросов после покупки.',
        'description_tr': 'Garanti ve teknik konularda müşteri ile üretici arasında koordinasyonu sağlıyoruz. Yedek parçaların bulunması ve siparişi konusunda destek sağlanarak satın alma sonrası herhangi bir sorunun zamanında çözümü garanti edilir.',
        'description_ar': 'نضمن التنسيق بين العميل والمصنع بشأن مسائل الضمان والأمور الفنية. يتم تقديم الدعم لإيجاد وطلب قطع الغيار، مما يضمن حل أي مخاوف بعد الشراء في الوقت المناسب.',
        'features_en': 'Warranty claim coordination\nManufacturer-client communication\nSpare parts sourcing\nTechnical issue resolution',
        'features_ru': 'Координация гарантийных обращений\nСвязь между производителем и клиентом\nПоиск запасных частей\nРешение технических вопросов',
        'features_tr': 'Garanti talebi koordinasyonu\nÜretici-müşteri iletişimi\nYedek parça tedariki\nTeknik sorun çözümü',
        'features_ar': 'تنسيق مطالبات الضمان\nالتواصل بين المصنع والعميل\nتوريد قطع الغيار\nحل المشكلات الفنية',
    },
]

for s_data in services_data:
    slug = s_data.pop('slug')
    Service.objects.create(category=cat, slug=slug, **s_data)
print(f"  ✓ {len(services_data)} services created")

# ============================================================
# 5. PROCESS STEPS (7-step order process from section 4.1)
# ============================================================
print("\n[5/6] Updating ProcessSteps...")
ProcessStep.objects.all().delete()

steps_data = [
    {
        'order': 1,
        'icon': 'fas fa-paper-plane',
        'title_en': 'Submit Your Inquiry',
        'title_ru': 'Отправьте запрос',
        'title_tr': 'Sorgunuzu Gönderin',
        'title_ar': 'أرسل استفسارك',
        'description_en': 'Contact us via website, WhatsApp, or email with details about the products you need.',
        'description_ru': 'Свяжитесь с нами через сайт, WhatsApp или электронную почту с информацией о нужной вам продукции.',
        'description_tr': 'İhtiyacınız olan ürünlerle ilgili detayları web sitesi, WhatsApp veya e-posta yoluyla bize iletin.',
        'description_ar': 'تواصل معنا عبر الموقع الإلكتروني أو واتساب أو البريد الإلكتروني مع تفاصيل المنتجات التي تحتاجها.',
    },
    {
        'order': 2,
        'icon': 'fas fa-file-invoice-dollar',
        'title_en': 'Receive Our Proposal',
        'title_ru': 'Получите наше предложение',
        'title_tr': 'Teklifimizi Alın',
        'title_ar': 'استلم عرضنا',
        'description_en': 'Within 24–48 hours we prepare and present you with pricing, specifications, and delivery timeline.',
        'description_ru': 'В течение 24–48 часов мы подготовим и представим вам цены, спецификации и сроки поставки.',
        'description_tr': '24–48 saat içinde fiyat, teknik özellikler ve teslimat süresini içeren teklifimizi hazırlayıp sunarız.',
        'description_ar': 'خلال 24-48 ساعة نعد ونقدم لكم الأسعار والمواصفات والجدول الزمني للتسليم.',
    },
    {
        'order': 3,
        'icon': 'fas fa-handshake',
        'title_en': 'Agreement & Contract',
        'title_ru': 'Согласование и контракт',
        'title_tr': 'Anlaşma ve Sözleşme',
        'title_ar': 'الاتفاق والعقد',
        'description_en': 'Terms are agreed upon and a formal contract is prepared and signed by both parties.',
        'description_ru': 'Условия согласовываются, и официальный контракт подготавливается и подписывается обеими сторонами.',
        'description_tr': 'Koşullar üzerinde anlaşılır ve resmi sözleşme her iki tarafça hazırlanıp imzalanır.',
        'description_ar': 'يتم الاتفاق على الشروط ويتم إعداد عقد رسمي وتوقيعه من كلا الطرفين.',
    },
    {
        'order': 4,
        'icon': 'fas fa-credit-card',
        'title_en': 'Payment',
        'title_ru': 'Оплата',
        'title_tr': 'Ödeme',
        'title_ar': 'الدفع',
        'description_en': 'Standard payment: 30% advance upon order confirmation, 70% balance before shipment via bank transfer (T/T).',
        'description_ru': 'Стандартная оплата: 30% аванс при подтверждении заказа, 70% остаток перед отгрузкой банковским переводом (T/T).',
        'description_tr': 'Standart ödeme: Sipariş onayında %30 avans, sevkiyattan önce %70 bakiye banka havalesi (T/T) ile.',
        'description_ar': 'الدفع القياسي: 30% دفعة مقدمة عند تأكيد الطلب، 70% الرصيد قبل الشحن عبر التحويل البنكي (T/T).',
    },
    {
        'order': 5,
        'icon': 'fas fa-cogs',
        'title_en': 'Production & Quality Check',
        'title_ru': 'Производство и проверка качества',
        'title_tr': 'Üretim ve Kalite Kontrolü',
        'title_ar': 'الإنتاج وفحص الجودة',
        'description_en': 'Products are prepared and inspected at the factory. You receive photos and videos for confirmation before final payment.',
        'description_ru': 'Продукция подготавливается и инспектируется на заводе. Вы получаете фото и видео для подтверждения перед финальной оплатой.',
        'description_tr': 'Ürünler fabrikada hazırlanır ve denetlenir. Final ödeme öncesinde onayınız için fotoğraf ve video alırsınız.',
        'description_ar': 'يتم تحضير المنتجات وفحصها في المصنع. تتلقون صوراً وفيديوهات للتأكيد قبل الدفعة النهائية.',
    },
    {
        'order': 6,
        'icon': 'fas fa-box-open',
        'title_en': 'Handover (EXW / FOB)',
        'title_ru': 'Передача (EXW / FOB)',
        'title_tr': 'Teslim (EXW / FOB)',
        'title_ar': 'التسليم (EXW / FOB)',
        'description_en': 'After full payment, products are handed over to your logistics partner under EXW or FOB terms.',
        'description_ru': 'После полной оплаты продукция передаётся вашему логистическому партнёру на условиях EXW или FOB.',
        'description_tr': 'Tam ödeme sonrası ürünler EXW veya FOB koşullarıyla lojistik ortağınıza teslim edilir.',
        'description_ar': 'بعد الدفع الكامل، يتم تسليم المنتجات لشريككم اللوجستي بشروط EXW أو FOB.',
    },
    {
        'order': 7,
        'icon': 'fas fa-check-circle',
        'title_en': 'Delivery & Receipt',
        'title_ru': 'Доставка и получение',
        'title_tr': 'Teslimat ve Teslim Alma',
        'title_ar': 'التوصيل والاستلام',
        'description_en': 'You receive your products via your chosen logistics company. We remain available for any after-sales support.',
        'description_ru': 'Вы получаете продукцию через выбранную логистическую компанию. Мы остаёмся на связи для послепродажной поддержки.',
        'description_tr': 'Seçtiğiniz lojistik şirketi aracılığıyla ürünlerinizi teslim alırsınız. Satış sonrası destek için her zaman yanınızdayız.',
        'description_ar': 'تستلمون منتجاتكم عبر شركة الشحن التي اخترتموها. نبقى متاحين لأي دعم ما بعد البيع.',
    },
]

for st_data in steps_data:
    ProcessStep.objects.create(**st_data)
print(f"  ✓ {len(steps_data)} process steps created")

# ============================================================
# 6. FAQs (comprehensive from all content sections)
# ============================================================
print("\n[6/6] Updating FAQs...")
FAQ.objects.all().delete()

faqs_data = [
    # --- Product FAQs ---
    {
        'order': 1,
        'question_en': 'What is the minimum order quantity?',
        'question_ru': 'Каков минимальный объём заказа?',
        'question_tr': 'Minimum sipariş miktarı nedir?',
        'question_ar': 'ما هو الحد الأدنى لكمية الطلب؟',
        'answer_en': 'Minimum order varies depending on the product. In most cases, 1 unit is possible for testing purposes. Wholesale orders start from 5 units or more. Better pricing is available for bulk orders.',
        'answer_ru': 'Минимальный заказ зависит от продукта. В большинстве случаев возможен заказ 1 единицы для тестирования. Оптовые заказы начинаются от 5 единиц и выше. Для крупных заказов предлагаются лучшие цены.',
        'answer_tr': 'Minimum sipariş ürüne göre değişir. Çoğu durumda test amacıyla 1 adet sipariş mümkündür. Toptan siparişler 5 adet ve üzerinden başlar. Büyük siparişlerde daha uygun fiyatlar geçerlidir.',
        'answer_ar': 'يختلف الحد الأدنى للطلب حسب المنتج. في معظم الحالات، يمكن طلب وحدة واحدة لأغراض الاختبار. تبدأ طلبات الجملة من 5 وحدات فأكثر. تتوفر أسعار أفضل للطلبات بالجملة.',
    },
    {
        'order': 2,
        'question_en': 'How long does delivery take?',
        'question_ru': 'Сколько времени занимает доставка?',
        'question_tr': 'Teslimat ne kadar sürer?',
        'question_ar': 'كم يستغرق التسليم؟',
        'answer_en': 'Stock products: 7–10 days. Made-to-order products: 25–40 days. International delivery time depends on the logistics partner chosen by the client.',
        'answer_ru': 'Складские товары: 7–10 дней. Товары под заказ: 25–40 дней. Срок международной доставки зависит от логистического партнёра, выбранного клиентом.',
        'answer_tr': 'Stok ürünler: 7–10 gün. Siparişle üretim: 25–40 gün. Uluslararası teslimat süresi müşterinin seçtiği lojistik ortağına bağlıdır.',
        'answer_ar': 'المنتجات المتوفرة في المخزون: 7-10 أيام. المنتجات المصنعة حسب الطلب: 25-40 يوماً. يعتمد وقت التسليم الدولي على شريك الشحن الذي يختاره العميل.',
    },
    {
        'order': 3,
        'question_en': 'What warranty do you provide?',
        'question_ru': 'Какую гарантию вы предоставляете?',
        'question_tr': 'Ne tür garanti sunuyorsunuz?',
        'question_ar': 'ما الضمان الذي تقدمونه؟',
        'answer_en': 'Products come with a minimum 1-year warranty. In some cases, manufacturers offer 2–3 year warranties. Warranty covers manufacturing defects only; normal wear and tear is not included.',
        'answer_ru': 'На продукцию предоставляется минимальная гарантия 1 год. В некоторых случаях производители предлагают гарантию 2–3 года. Гарантия распространяется только на производственные дефекты; нормальный износ не покрывается.',
        'answer_tr': 'Ürünlere minimum 1 yıl garanti verilir. Bazı durumlarda üreticiler 2–3 yıl garanti sunar. Garanti yalnızca üretim hatalarını kapsar; normal kullanıma bağlı aşınma dahil değildir.',
        'answer_ar': 'تأتي المنتجات بضمان لا يقل عن سنة واحدة. في بعض الحالات، يقدم المصنعون ضماناً لمدة 2-3 سنوات. يغطي الضمان عيوب التصنيع فقط؛ التآكل الطبيعي غير مشمول.',
    },
    {
        'order': 4,
        'question_en': 'Where are products sourced from?',
        'question_ru': 'Откуда поставляется продукция?',
        'question_tr': 'Ürünler nereden tedarik ediliyor?',
        'question_ar': 'من أين يتم توريد المنتجات؟',
        'answer_en': 'All products are sourced exclusively from China. We work with verified manufacturers and suppliers across the country.',
        'answer_ru': 'Вся продукция поставляется исключительно из Китая. Мы работаем с проверенными производителями и поставщиками по всей стране.',
        'answer_tr': 'Tüm ürünler yalnızca Çin\'den tedarik edilmektedir. Ülke genelinde doğrulanmış üreticiler ve tedarikçilerle çalışıyoruz.',
        'answer_ar': 'يتم توريد جميع المنتجات حصرياً من الصين. نعمل مع مصنعين وموردين معتمدين في جميع أنحاء البلاد.',
    },
    {
        'order': 5,
        'question_en': 'Can I order from a specific brand?',
        'question_ru': 'Могу ли я заказать товар конкретного бренда?',
        'question_tr': 'Belirli bir markadan sipariş verebilir miyim?',
        'question_ar': 'هل يمكنني الطلب من علامة تجارية محددة؟',
        'answer_en': 'Yes, products can be sourced according to the brand you request. Our company is not limited to specific brands — we find the supplier and brand that best match your requirements, budget, and quality expectations.',
        'answer_ru': 'Да, продукция может быть закуплена по запрашиваемому вами бренду. Наша компания не ограничена конкретными брендами — мы находим поставщика и бренд, наилучшим образом соответствующие вашим требованиям, бюджету и ожиданиям по качеству.',
        'answer_tr': 'Evet, talep ettiğiniz markaya uygun ürünler tedarik edilebilir. Şirketimiz belirli markalarla sınırlı değildir — gereksinimlerinize, bütçenize ve kalite beklentilerinize en uygun tedarikçi ve markayı buluruz.',
        'answer_ar': 'نعم، يمكن توريد المنتجات وفقاً للعلامة التجارية التي تطلبونها. شركتنا غير محدودة بعلامات تجارية معينة — نجد المورد والعلامة التجارية الأنسب لمتطلباتكم وميزانيتكم وتوقعات الجودة.',
    },
    {
        'order': 6,
        'question_en': 'Are technical datasheets provided?',
        'question_ru': 'Предоставляются ли технические паспорта?',
        'question_tr': 'Teknik veri sayfaları sağlanıyor mu?',
        'question_ar': 'هل يتم توفير أوراق البيانات الفنية؟',
        'answer_en': 'Yes, technical documents (PDF datasheets) provided by the manufacturer are shared with the client for every product.',
        'answer_ru': 'Да, техническая документация (PDF-паспорта), предоставленная производителем, передаётся клиенту по каждому товару.',
        'answer_tr': 'Evet, üretici tarafından sağlanan teknik belgeler (PDF veri sayfaları) her ürün için müşteriyle paylaşılır.',
        'answer_ar': 'نعم، يتم مشاركة الوثائق الفنية (أوراق البيانات بصيغة PDF) المقدمة من المصنع مع العميل لكل منتج.',
    },
    # --- Pricing FAQs ---
    {
        'order': 7,
        'question_en': 'How are prices determined?',
        'question_ru': 'Как определяются цены?',
        'question_tr': 'Fiyatlar nasıl belirlenir?',
        'question_ar': 'كيف يتم تحديد الأسعار؟',
        'answer_en': 'Prices vary depending on the product, order volume, and technical specifications. Each client receives a personalized quote. Prices are primarily presented in US Dollars (USD). Prices are provided under EXW (Ex Works) or FOB (Free on Board) terms and cover only the product cost. Delivery, insurance, and import costs are not included.',
        'answer_ru': 'Цены зависят от продукта, объёма заказа и технических характеристик. Каждый клиент получает индивидуальное предложение. Цены преимущественно указываются в долларах США (USD). Цены предоставляются на условиях EXW (самовывоз с завода) или FOB (до порта) и включают только стоимость товара. Доставка, страхование и расходы на импорт не включены.',
        'answer_tr': 'Fiyatlar ürüne, sipariş hacmine ve teknik özelliklere göre değişir. Her müşteriye özel teklif sunulur. Fiyatlar öncelikle ABD Doları (USD) üzerinden sunulmaktadır. Fiyatlar EXW (fabrikadan teslim) veya FOB (limana teslim) koşullarıyla yalnızca ürün bedelini kapsar. Teslimat, sigorta ve ithalat masrafları dahil değildir.',
        'answer_ar': 'تختلف الأسعار حسب المنتج وحجم الطلب والمواصفات الفنية. يتلقى كل عميل عرض سعر مخصص. تُقدم الأسعار بشكل أساسي بالدولار الأمريكي (USD). تُقدم الأسعار بشروط EXW (تسليم المصنع) أو FOB (تسليم الميناء) وتغطي تكلفة المنتج فقط. تكاليف التوصيل والتأمين والاستيراد غير مشمولة.',
    },
    {
        'order': 8,
        'question_en': 'Do you offer discounts?',
        'question_ru': 'Предоставляются ли скидки?',
        'question_tr': 'İndirim sunuyor musunuz?',
        'question_ar': 'هل تقدمون خصومات؟',
        'answer_en': 'Yes, special discounts are available for bulk orders, repeat customers, and long-term partnership agreements.',
        'answer_ru': 'Да, специальные скидки предоставляются для крупных заказов, постоянных клиентов и при долгосрочном сотрудничестве.',
        'answer_tr': 'Evet, büyük hacimli siparişlerde, sürekli müşterilere ve uzun vadeli iş birliği anlaşmalarında özel indirimler uygulanır.',
        'answer_ar': 'نعم، تتوفر خصومات خاصة للطلبات بالجملة والعملاء الدائمين واتفاقيات الشراكة طويلة الأمد.',
    },
    # --- Payment FAQs ---
    {
        'order': 9,
        'question_en': 'What are the payment terms?',
        'question_ru': 'Каковы условия оплаты?',
        'question_tr': 'Ödeme koşulları nedir?',
        'question_ar': 'ما هي شروط الدفع؟',
        'answer_en': 'Payments are made by official bank transfer (T/T) only, based on a signed contract. Standard terms: 30% advance after order confirmation, remaining 70% after product approval and before shipment. The advance amount may vary depending on the product and order volume. No credit or installment options are available.',
        'answer_ru': 'Оплата производится только банковским переводом (T/T) на основании подписанного контракта. Стандартные условия: 30% аванс после подтверждения заказа, оставшиеся 70% после утверждения товара и до отгрузки. Размер аванса может варьироваться в зависимости от продукта и объёма заказа. Кредит и рассрочка не предоставляются.',
        'answer_tr': 'Ödemeler yalnızca imzalı sözleşmeye dayalı olarak resmi banka havalesi (T/T) ile yapılır. Standart koşullar: Sipariş onayından sonra %30 avans, ürün onayı ve sevkiyat öncesi kalan %70. Avans tutarı ürüne ve sipariş hacmine bağlı olarak değişebilir. Kredi veya taksit seçeneği sunulmamaktadır.',
        'answer_ar': 'تتم المدفوعات عبر التحويل البنكي الرسمي (T/T) فقط، بناءً على عقد موقع. الشروط القياسية: 30% دفعة مقدمة بعد تأكيد الطلب، 70% المتبقية بعد الموافقة على المنتج وقبل الشحن. قد يختلف مبلغ الدفعة المقدمة حسب المنتج وحجم الطلب. لا تتوفر خيارات الائتمان أو التقسيط.',
    },
    {
        'order': 10,
        'question_en': 'What documents are provided with the order?',
        'question_ru': 'Какие документы предоставляются с заказом?',
        'question_tr': 'Siparişle birlikte hangi belgeler sağlanır?',
        'question_ar': 'ما المستندات المقدمة مع الطلب؟',
        'answer_en': 'We provide: Proforma Invoice, Commercial Invoice, Packing List, Export documents, and Bill of Lading (for FOB shipments). All orders include a formal contract, typically prepared in English.',
        'answer_ru': 'Мы предоставляем: проформа-инвойс, коммерческий инвойс, упаковочный лист, экспортные документы и коносамент (для поставок FOB). Все заказы сопровождаются официальным контрактом, обычно на английском языке.',
        'answer_tr': 'Sunduğumuz belgeler: Proforma Invoice, Commercial Invoice, Packing List, ihracat belgeleri ve Bill of Lading (FOB sevkiyatlarında). Tüm siparişler genellikle İngilizce hazırlanan resmi sözleşme ile düzenlenir.',
        'answer_ar': 'نقدم: فاتورة أولية، فاتورة تجارية، قائمة تعبئة، مستندات تصدير، وبوليصة شحن (لشحنات FOB). تتضمن جميع الطلبات عقداً رسمياً يُعد عادةً باللغة الإنجليزية.',
    },
    # --- Shipping FAQs ---
    {
        'order': 11,
        'question_en': 'Can you ship to any country?',
        'question_ru': 'Возможна ли доставка в любую страну?',
        'question_tr': 'Herhangi bir ülkeye gönderim yapılabilir mi?',
        'question_ar': 'هل يمكنكم الشحن إلى أي دولة؟',
        'answer_en': 'Yes, products can be shipped from China to any country. Delivery is carried out by the logistics company chosen by the client.',
        'answer_ru': 'Да, продукция может быть отправлена из Китая в любую страну. Доставка осуществляется логистической компанией, выбранной клиентом.',
        'answer_tr': 'Evet, ürünler Çin\'den herhangi bir ülkeye gönderilebilir. Teslimat müşterinin seçtiği lojistik şirketi aracılığıyla gerçekleştirilir.',
        'answer_ar': 'نعم، يمكن شحن المنتجات من الصين إلى أي دولة. يتم التوصيل عبر شركة الشحن التي يختارها العميل.',
    },
    {
        'order': 12,
        'question_en': 'How is packaging handled?',
        'question_ru': 'Как осуществляется упаковка?',
        'question_tr': 'Ambalajlama nasıl yapılır?',
        'question_ar': 'كيف يتم التغليف؟',
        'answer_en': 'Products are export-packaged by the manufacturer to international standards: wooden crates, pallets, carton packaging, or container-suitable wrapping as appropriate.',
        'answer_ru': 'Продукция упаковывается производителем для экспорта в соответствии с международными стандартами: деревянные ящики, паллеты, картонная упаковка или контейнерная обёртка.',
        'answer_tr': 'Ürünler uluslararası standartlara uygun ihracat ambalajıyla üretici tarafından paketlenir: tahta sandık, palet, karton ambalaj veya konteynere uygun paketleme.',
        'answer_ar': 'يتم تغليف المنتجات من قبل المصنع للتصدير وفقاً للمعايير الدولية: صناديق خشبية، منصات نقل، تغليف كرتون، أو تغليف مناسب للحاويات.',
    },
    {
        'order': 13,
        'question_en': 'Is cargo insurance included?',
        'question_ru': 'Включена ли страховка груза?',
        'question_tr': 'Kargo sigortası dahil mi?',
        'question_ar': 'هل يشمل تأمين الشحن؟',
        'answer_en': 'Cargo insurance is the responsibility of the client and is arranged through their chosen logistics partner.',
        'answer_ru': 'Страхование груза — ответственность клиента и осуществляется через выбранного логистического партнёра.',
        'answer_tr': 'Kargo sigortası müşterinin sorumluluğundadır ve seçilen lojistik ortağı aracılığıyla yapılır.',
        'answer_ar': 'تأمين الشحن هو مسؤولية العميل ويتم ترتيبه من خلال شريك الشحن المختار.',
    },
    # --- Warranty & Disputes ---
    {
        'order': 14,
        'question_en': 'How do I make a warranty claim?',
        'question_ru': 'Как подать гарантийную заявку?',
        'question_tr': 'Garanti talebini nasıl yapabilirim?',
        'question_ar': 'كيف أقدم مطالبة ضمان؟',
        'answer_en': 'Submit photo and video evidence of the issue. After investigation, we coordinate with the manufacturer to provide the most suitable solution: spare parts, replacement, or compensation.',
        'answer_ru': 'Предоставьте фото- и видеодоказательства проблемы. После расследования мы координируем с производителем наиболее подходящее решение: запасные части, замена или компенсация.',
        'answer_tr': 'Sorunla ilgili fotoğraf ve video kanıtlarını sunun. İnceleme sonrası üretici ile en uygun çözüm koordine edilir: yedek parça, değişim veya tazminat.',
        'answer_ar': 'قدّم صوراً وفيديوهات كدليل على المشكلة. بعد التحقيق، ننسق مع المصنع لتقديم الحل الأنسب: قطع غيار، استبدال، أو تعويض.',
    },
    {
        'order': 15,
        'question_en': 'How are disputes resolved?',
        'question_ru': 'Как решаются споры?',
        'question_tr': 'Anlaşmazlıklar nasıl çözülür?',
        'question_ar': 'كيف يتم حل النزاعات؟',
        'answer_en': 'Disputes are resolved through mutual agreement first. If necessary, they are handled according to the terms specified in the contract and Chinese legislation.',
        'answer_ru': 'Споры решаются прежде всего путём взаимного согласия. При необходимости — в соответствии с условиями, указанными в контракте, и китайским законодательством.',
        'answer_tr': 'Anlaşmazlıklar öncelikle karşılıklı mutabakat ile çözülür. Gerektiğinde sözleşmede belirtilen koşullar ve Çin mevzuatına uygun şekilde ele alınır.',
        'answer_ar': 'يتم حل النزاعات من خلال الاتفاق المتبادل أولاً. عند الضرورة، يتم التعامل معها وفقاً للشروط المحددة في العقد والتشريعات الصينية.',
    },
    # --- Special Conditions ---
    {
        'order': 16,
        'question_en': 'Are special terms available for large projects?',
        'question_ru': 'Предусмотрены ли специальные условия для крупных проектов?',
        'question_tr': 'Büyük projeler için özel koşullar var mı?',
        'question_ar': 'هل تتوفر شروط خاصة للمشاريع الكبيرة؟',
        'answer_en': 'Yes, special pricing and partnership terms are available for large-volume and long-term projects. Contact us to discuss your specific requirements.',
        'answer_ru': 'Да, для крупных и долгосрочных проектов предусмотрены специальные цены и условия сотрудничества. Свяжитесь с нами для обсуждения ваших требований.',
        'answer_tr': 'Evet, büyük hacimli ve uzun vadeli projeler için özel fiyatlandırma ve iş birliği koşulları sunulmaktadır. Özel gereksinimlerinizi görüşmek için bizimle iletişime geçin.',
        'answer_ar': 'نعم، تتوفر أسعار وشروط شراكة خاصة للمشاريع الكبيرة وطويلة الأمد. تواصلوا معنا لمناقشة متطلباتكم المحددة.',
    },
    # --- Technical specialist (Section 6.4) ---
    {
        'order': 17,
        'question_en': 'Do you provide on-site technical specialists?',
        'question_ru': 'Предоставляете ли вы технических специалистов на место?',
        'question_tr': 'Yerinde teknik uzman gönderiyor musunuz?',
        'question_ar': 'هل توفرون متخصصين فنيين في الموقع؟',
        'answer_en': 'Our company does not provide on-site technical specialist services. However, manufacturers can provide technical documentation and remote support to assist with installation and operation.',
        'answer_ru': 'Наша компания не предоставляет услуги технических специалистов на месте. Однако производители могут предоставить техническую документацию и удалённую поддержку для помощи при монтаже и эксплуатации.',
        'answer_tr': 'Şirketimiz yerinde teknik uzman hizmeti sunmamaktadır. Ancak üreticiler, kurulum ve işletme konusunda yardımcı olmak için teknik dokümantasyon ve uzaktan destek sağlayabilir.',
        'answer_ar': 'لا تقدم شركتنا خدمات المتخصصين الفنيين في الموقع. ومع ذلك، يمكن للمصنعين تقديم الوثائق الفنية والدعم عن بُعد للمساعدة في التركيب والتشغيل.',
    },
]

for f_data in faqs_data:
    FAQ.objects.create(**f_data)
print(f"  ✓ {len(faqs_data)} FAQs created")

# ============================================================
# 7. STATISTICS (updated for sourcing company profile)
# ============================================================
print("\n[7/7] Updating Statistics...")
Statistic.objects.all().delete()

stats_data = [
    {
        'title_en': 'Core Services',
        'title_ru': 'Основных услуг',
        'title_tr': 'Temel Hizmet',
        'title_ar': 'خدمات أساسية',
        'value': 8, 'suffix': '', 'icon': 'fas fa-concierge-bell', 'order': 1,
    },
    {
        'title_en': 'Step Order Process',
        'title_ru': 'Шагов процесса заказа',
        'title_tr': 'Adımlık Sipariş Süreci',
        'title_ar': 'خطوات عملية الطلب',
        'value': 7, 'suffix': '', 'icon': 'fas fa-list-ol', 'order': 2,
    },
    {
        'title_en': 'Year+ Product Warranty',
        'title_ru': 'Год+ гарантии на продукцию',
        'title_tr': 'Yıl+ Ürün Garantisi',
        'title_ar': 'سنة+ ضمان المنتج',
        'value': 1, 'suffix': '+', 'icon': 'fas fa-shield-alt', 'order': 3,
    },
    {
        'title_en': 'Trade Terms (EXW & FOB)',
        'title_ru': 'Торговых условия (EXW и FOB)',
        'title_tr': 'Ticaret Koşulu (EXW ve FOB)',
        'title_ar': 'شروط تجارية (EXW و FOB)',
        'value': 2, 'suffix': '', 'icon': 'fas fa-handshake', 'order': 4,
    },
]

for s_data in stats_data:
    Statistic.objects.create(**s_data)
print(f"  ✓ {len(stats_data)} statistics created")

# ============================================================
print("\n" + "=" * 60)
print("  ✅ Content update complete!")
print("  Updated: CompanyInfo, Features, HeroSlides,")
print("           Services, ProcessSteps, FAQs, Statistics")
print("  Languages: EN, RU, TR, AR")
print("=" * 60)
