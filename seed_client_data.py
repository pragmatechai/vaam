"""
VAAM Import and Export Trading - Client Data Seed Script
Seeds the database with real client information in 4 languages: EN, RU, TR, AR
Run: python manage.py shell < seed_client_data.py
Or on server: cd /path/to/vaam && source venv/bin/activate && python manage.py shell < seed_client_data.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from core.models import (
    SiteSettings, HeroSlide, CompanyInfo, CompanyFeature, Statistic,
    ProductCategory, ProcessStep, News, NewsCategory, FAQ
)

print("=" * 80)
print("  VAAM Import and Export Trading - Client Data Seeding")
print("=" * 80)

# ============ SITE SETTINGS ============
print("\n[1/8] Updating Site Settings...")
settings, _ = SiteSettings.objects.get_or_create(pk=1)

settings.site_name_en = "VAAM Import and Export Trading Co., LTD"
settings.site_name_ru = "VAAM Import and Export Trading Co., LTD"
settings.site_name_tr = "VAAM Import and Export Trading Co., LTD"
settings.site_name_ar = "VAAM Import and Export Trading Co., LTD"

settings.site_description_en = "VAAM Import and Export Trading Co., Ltd. is an international trading company specializing in sourcing and supplying solar energy systems, garden and street lighting cameras, automobiles, construction materials, and various other products. We research, select, and reliably supply a wide range of products based on customer orders."
settings.site_description_ru = "VAAM Import and Export Trading Co., Ltd. — международная торговая компания, специализирующаяся на поиске и поставке систем солнечной энергии, камер освещения садов и дорог, автомобилей, строительных материалов и других различных товаров. Мы исследуем, выбираем и надежно поставляем широкий ассортимент продукции на основе заказов клиентов."
settings.site_description_tr = "VAAM Import and Export Trading Co., Ltd., güneş enerjisi sistemleri, bahçe ve yol aydınlatma kameraları, otomobiller, inşaat malzemeleri ve diğer çeşitli ürünlerin araştırılması ve tedariki konusunda uzmanlaşmış uluslararası bir ticaret şirketidir. Müşteri siparişlerine göre geniş ürün yelpazesini araştırır, seçer ve güvenilir bir şekilde temin ederiz."
settings.site_description_ar = "شركة VAAM للاستيراد والتصدير هي شركة تجارية دولية متخصصة في البحث عن وتوريد أنظمة الطاقة الشمسية وكاميرات إضاءة الحدائق والطرق والسيارات ومواد البناء ومنتجات أخرى متنوعة. نقوم بالبحث والاختيار والتوريد الموثوق لمجموعة واسعة من المنتجات بناءً على طلبات العملاء."

settings.phone = "+8618690149671"
settings.phone2 = "+8615026032721"
settings.email = "info@vaamglobal.com"
settings.email2 = ""
settings.whatsapp = "8618690149671"

settings.address_en = "Room 688, 103 Huanshi West Road, Liwan District, Guangzhou, 688D"
settings.address_ru = "Комната 688, 103 Huanshi West Road, район Liwan, Гуанчжоу, 688D"
settings.address_tr = "Oda 688, 103 Huanshi West Road, Liwan Bölgesi, Guangzhou, 688D"
settings.address_ar = "غرفة 688، 103 طريق هوانشي الغربي، منطقة ليوان، قوانغتشو، 688D"

settings.working_hours_en = "Mon - Fri: 09:00 - 18:00"
settings.working_hours_ru = "Пн - Пт: 09:00 - 18:00"
settings.working_hours_tr = "Pzt - Cum: 09:00 - 18:00"
settings.working_hours_ar = "الإثنين - الجمعة: 09:00 - 18:00"

settings.meta_title_en = "VAAM Trading | Your Reliable Trading Partner in China"
settings.meta_title_ru = "VAAM Trading | Ваш надежный торговый партнер в Китае"
settings.meta_title_tr = "VAAM Trading | Çin'deki Güvenilir Ticaret Ortağınız"
settings.meta_title_ar = "VAAM Trading | شريكك التجاري الموثوق في الصين"

settings.meta_description_en = "VAAM Import and Export Trading - We find, select and supply products. Solar energy systems, lighting, cameras, automobiles, construction materials and more."
settings.meta_description_ru = "VAAM Import and Export Trading - Находим, выбираем и поставляем продукцию. Системы солнечной энергии, освещение, камеры, автомобили, строительные материалы и многое другое."
settings.meta_description_tr = "VAAM Import and Export Trading - Ürünleri bulur, seçer ve temin ederiz. Güneş enerjisi sistemleri, aydınlatma, kameralar, otomobiller, inşaat malzemeleri ve daha fazlası."
settings.meta_description_ar = "VAAM للاستيراد والتصدير - نجد ونختار ونوفر المنتجات. أنظمة الطاقة الشمسية والإضاءة والكاميرات والسيارات ومواد البناء والمزيد."

settings.save()
print("   ✓ Site settings updated with real client data")

# ============ HERO SLIDES ============
print("\n[2/8] Creating Hero Slides...")
HeroSlide.objects.filter(title_en__icontains="China").delete()

hero1 = HeroSlide.objects.create(
    title_en="Your Reliable Trading Partner in China",
    title_ru="Ваш надежный торговый партнер в Китае",
    title_tr="Çin'deki Güvenilir Ticaret Ortağınız",
    title_ar="شريكك التجاري الموثوق في الصين",
    
    subtitle_en="We Find, Select and Supply Products",
    subtitle_ru="Находим, выбираем и поставляем товары",
    subtitle_tr="Ürünleri Bulur, Seçer ve Temin Ederiz",
    subtitle_ar="نجد ونختار ونوفر المنتجات",
    
    description_en="VAAM Import and Export Trading Co., Ltd. provides professional services in product sourcing, selection, and international supply across various industries. We find the right product at the right price for your business.",
    description_ru="VAAM Import and Export Trading Co., Ltd. предоставляет профессиональные услуги по поиску, подбору и международным поставкам продукции в различных отраслях. Мы находим нужный товар по правильной цене для вашего бизнеса.",
    description_tr="VAAM Import and Export Trading Co., Ltd., çeşitli endüstrilerde ürün tedariki, seçimi ve uluslararası tedarik konularında profesyonel hizmetler sunmaktadır. İşiniz için doğru ürünü doğru fiyata buluyoruz.",
    description_ar="توفر شركة VAAM للاستيراد والتصدير خدمات احترافية في البحث عن المنتجات واختيارها والتوريد الدولي عبر مختلف الصناعات. نجد المنتج المناسب بالسعر المناسب لعملك.",
    
    button1_text_en="Get Quote",
    button1_text_ru="Получить предложение",
    button1_text_tr="Teklif Al",
    button1_text_ar="احصل على عرض",
    button1_url="/contact/",
    
    button2_text_en="Our Products",
    button2_text_ru="Наши продукты",
    button2_text_tr="Ürünlerimiz",
    button2_text_ar="منتجاتنا",
    button2_url="/products/",
    
    image="hero/placeholder.jpg",
    order=1,
    is_active=True
)
print(f"   ✓ Hero slide created: {hero1.title_en}")

# ============ COMPANY INFO ============
print("\n[3/8] Updating Company Information...")
info, _ = CompanyInfo.objects.get_or_create(pk=1)

info.title_en = "About VAAM Trading"
info.title_ru = "О компании VAAM"
info.title_tr = "VAAM Hakkında"
info.title_ar = "حول VAAM"

info.subtitle_en = "Professional Trading Partner Since 2023"
info.subtitle_ru = "Профессиональный торговый партнер с 2023 года"
info.subtitle_tr = "2023'ten Beri Profesyonel Ticaret Ortağı"
info.subtitle_ar = "شريك تجاري محترف منذ 2023"

info.description_en = """VAAM Import and Export Trading Co., Ltd. is a corporate company operating in the field of international trade and strategic procurement since 2023. Our company provides professional services in product sourcing in China, supplier selection, and supply of goods across various industrial sectors.

Our areas of activity include research and order-based supply of solar energy systems, garden and street lighting equipment, security cameras, automobiles, construction materials, and other industrial products. Thanks to our modern management approach and extensive supplier network, we offer quality and competitive solutions to our customers.

Our company operates on the principles of transparency, efficiency, and long-term partnership."""

info.description_ru = """VAAM Import and Export Trading Co., Ltd. - корпоративная компания, работающая в сфере международной торговли и стратегических закупок с 2023 года. Наша компания предоставляет профессиональные услуги по поиску продукции в Китае, подбору поставщиков и поставке товаров в различных промышленных секторах.

Наши направления деятельности включают исследование и поставку по заказу систем солнечной энергии, оборудования для освещения садов и дорог, камер безопасности, автомобилей, строительных материалов и других промышленных товаров. Благодаря современному подходу к управлению и обширной сети поставщиков мы предлагаем нашим клиентам качественные и конкурентоспособные решения.

Наша компания работает на принципах прозрачности, оперативности и долгосрочного партнерства."""

info.description_tr = """VAAM Import and Export Trading Co., Ltd., 2023 yılından bu yana uluslararası ticaret ve stratejik tedarik alanında faaliyet gösteren kurumsal bir şirkettir. Şirketimiz, Çin'de ürün tedariki, tedarikçi seçimi ve çeşitli endüstri sektörlerinde mal temini konusunda profesyonel hizmetler sunmaktadır.

Faaliyet alanlarımız arasında güneş enerjisi sistemleri, bahçe ve yol aydınlatma ekipmanları, güvenlik kameraları, otomobiller, inşaat malzemeleri ve diğer endüstriyel ürünlerin araştırılması ve sipariş bazlı tedariki yer almaktadır. Modern yönetim yaklaşımımız ve geniş tedarikçi ağımız sayesinde müşterilerimize kaliteli ve rekabetçi çözümler sunuyoruz.

Şirketimiz şeffaflık, verimlilik ve uzun vadeli ortaklık ilkeleri doğrultusunda faaliyet göstermektedir."""

info.description_ar = """شركة VAAM للاستيراد والتصدير هي شركة مؤسسية تعمل في مجال التجارة الدولية والمشتريات الاستراتيجية منذ عام 2023. تقدم شركتنا خدمات احترافية في البحث عن المنتجات في الصين واختيار الموردين وتوريد السلع عبر مختلف القطاعات الصناعية.

تشمل مجالات نشاطنا البحث والتوريد حسب الطلب لأنظمة الطاقة الشمسية ومعدات إضاءة الحدائق والطرق وكاميرات الأمان والسيارات ومواد البناء والمنتجات الصناعية الأخرى. بفضل نهج الإدارة الحديث وشبكة الموردين الواسعة، نقدم لعملائنا حلولاً عالية الجودة وتنافسية.

تعمل شركتنا على مبادئ الشفافية والكفاءة والشراكة طويلة الأجل."""

# Mission
info.mission_en = "To create a reliable supply platform in China for our customers, implementing the product sourcing and supply process in a secure, fast and efficient manner."
info.mission_ru = "Создать для наших клиентов надежную платформу поставок в Китае, обеспечивая процесс поиска и поставки продукции безопасным, быстрым и эффективным способом."
info.mission_tr = "Müşterilerimiz için Çin'de güvenilir bir tedarik platformu oluşturarak, ürün tedarik ve temin sürecini güvenli, hızlı ve etkili bir şekilde gerçekleştirmek."
info.mission_ar = "إنشاء منصة توريد موثوقة في الصين لعملائنا، وتنفيذ عملية البحث عن المنتجات وتوريدها بطريقة آمنة وسريعة وفعالة."

# Vision
info.vision_en = "To become a trusted and recognized regional brand in international trade, building a professional service model for product supply from China and ensuring sustainable development."
info.vision_ru = "Стать доверенным и признанным региональным брендом в международной торговле, создавая профессиональную модель обслуживания поставок продукции из Китая и обеспечивая устойчивое развитие."
info.vision_tr = "Uluslararası ticarette güvenilir ve tanınan bölgesel bir marka olmak, Çin'den ürün tedariki konusunda profesyonel bir hizmet modeli kurarak sürdürülebilir gelişimi sağlamak."
info.vision_ar = "أن نصبح علامة تجارية إقليمية موثوقة ومعترف بها في التجارة الدولية، وبناء نموذج خدمة احترافي لتوريد المنتجات من الصين وضمان التنمية المستدامة."

# Values
info.values_en = """• Reliability and Transparency
• Customer-Centric Approach
• Quality Control
• Fast and Accurate Service
• Long-Term Cooperation
• Professionalism and Development"""

info.values_ru = """• Надежность и прозрачность
• Клиентоориентированный подход
• Контроль качества
• Быстрое и точное обслуживание
• Долгосрочное сотрудничество
• Профессионализм и развитие"""

info.values_tr = """• Güvenilirlik ve Şeffaflık
• Müşteri Odaklı Yaklaşım
• Kalite Kontrolü
• Hızlı ve Doğru Hizmet
• Uzun Vadeli İş Birliği
• Profesyonellik ve Gelişim"""

info.values_ar = """• الموثوقية والشفافية
• النهج الموجه للعميل
• مراقبة الجودة
• خدمة سريعة ودقيقة
• التعاون طويل الأجل
• الاحتراف والتطوير"""

# History
info.history_en = """2023 – Company establishment and commencement of international trading activities
2023 – Formation of supplier network in Chinese market
2024 – Expansion of activities in solar energy, lighting and construction materials
2025 – Increase in customer portfolio and international partnerships"""

info.history_ru = """2023 – Основание компании и начало деятельности в сфере международной торговли
2023 – Формирование сети поставщиков на китайском рынке
2024 – Расширение деятельности в области солнечной энергии, освещения и строительных материалов
2025 – Увеличение клиентского портфеля и международных партнерств"""

info.history_tr = """2023 – Şirketin kurulması ve uluslararası ticaret faaliyetlerine başlanması
2023 – Çin pazarında tedarikçi ağının oluşturulması
2024 – Güneş enerjisi, aydınlatma ve inşaat malzemeleri alanında faaliyetlerin genişletilmesi
2025 – Müşteri portföyü ve uluslararası iş birliklerinin artırılması"""

info.history_ar = """2023 – تأسيس الشركة وبدء أنشطة التجارة الدولية
2023 – تشكيل شبكة الموردين في السوق الصيني
2024 – توسيع الأنشطة في مجال الطاقة الشمسية والإضاءة ومواد البناء
2025 – زيادة محفظة العملاء والشراكات الدولية"""

info.save()
print("   ✓ Company information updated")

# ============ COMPANY FEATURES ============
print("\n[4/8] Creating Company Features (Strengths)...")
CompanyFeature.objects.all().delete()

features_data = [
    {
        "order": 1,
        "icon": "fas fa-network-wired",
        "title_en": "Reliable Supplier Network",
        "title_ru": "Надежная сеть поставщиков",
        "title_tr": "Güvenilir Tedarikçi Ağı",
        "title_ar": "شبكة موردين موثوقة",
        "description_en": "With our extensive and reliable supplier network in China and international markets, we offer you only quality and competitive products.",
        "description_ru": "Благодаря обширной и надежной сети поставщиков в Китае и на международных рынках, мы предлагаем вам только качественную и конкурентоспособную продукцию.",
        "description_tr": "Çin ve uluslararası pazarlarda geniş ve güvenilir tedarikçi ağımız ile size yalnızca kaliteli ve rekabetçi ürünler sunuyoruz.",
        "description_ar": "من خلال شبكة الموردين الواسعة والموثوقة في الصين والأسواق الدولية، نقدم لك منتجات عالية الجودة وتنافسية فقط.",
    },
    {
        "order": 2,
        "icon": "fas fa-clipboard-check",
        "title_en": "Custom Order and Supply Service",
        "title_ru": "Индивидуальный заказ и обслуживание поставок",
        "title_tr": "Özel Sipariş ve Tedarik Hizmeti",
        "title_ar": "خدمة الطلب والتوريد المخصصة",
        "description_en": "We find the product that suits your needs, compare prices and quality, and supply it reliably.",
        "description_ru": "Мы находим товар, соответствующий вашим потребностям, сравниваем цены и качество и надежно поставляем его.",
        "description_tr": "İhtiyaçlarınıza uygun ürünü buluyor, fiyat ve kalite karşılaştırması yapıyor ve güvenilir bir şekilde temin ediyoruz.",
        "description_ar": "نجد المنتج الذي يناسب احتياجاتك، ونقارن الأسعار والجودة، ونوفره بشكل موثوق.",
    },
    {
        "order": 3,
        "icon": "fas fa-shipping-fast",
        "title_en": "Fast and Efficient Work Process",
        "title_ru": "Быстрый и эффективный рабочий процесс",
        "title_tr": "Hızlı ve Verimli İş Süreci",
        "title_ar": "عملية عمل سريعة وفعالة",
        "description_en": "We manage all stages from order to supply quickly and flexibly, minimizing time loss.",
        "description_ru": "Мы оперативно и гибко управляем всеми этапами от заказа до поставки, минимизируя потери времени.",
        "description_tr": "Siparişten tedarike kadar tüm aşamaları hızlı ve esnek bir şekilde yönetiyor, zaman kaybını minimuma indiriyoruz.",
        "description_ar": "نقوم بإدارة جميع المراحل من الطلب إلى التوريد بسرعة ومرونة، مما يقلل من فقدان الوقت.",
    },
    {
        "order": 4,
        "icon": "fas fa-smile",
        "title_en": "Focus on Customer Satisfaction",
        "title_ru": "Фокус на удовлетворенности клиентов",
        "title_tr": "Müşteri Memnuniyetine Odaklanma",
        "title_ar": "التركيز على رضا العملاء",
        "description_en": "In every project, we prioritize customer satisfaction and build long-term, reliable partnerships.",
        "description_ru": "В каждом проекте мы ставим удовлетворенность клиента в приоритет и строим долгосрочное надежное партнерство.",
        "description_tr": "Her projede müşteri memnuniyetini öncelik olarak belirliyor ve uzun vadeli, güvenilir ortaklıklar kuruyoruz.",
        "description_ar": "في كل مشروع، نعطي الأولوية لرضا العملاء ونبني شراكات موثوقة طويلة الأجل.",
    },
    {
        "order": 5,
        "icon": "fas fa-boxes",
        "title_en": "Wide Product Portfolio",
        "title_ru": "Широкий портфель продукции",
        "title_tr": "Geniş Ürün Portföyü",
        "title_ar": "محفظة منتجات واسعة",
        "description_en": "With our wide range covering solar energy systems, street and garden lights, automobiles, construction materials and other industrial products, we meet all your needs.",
        "description_ru": "Благодаря широкому ассортименту, включающему системы солнечной энергии, уличные и садовые светильники, автомобили, строительные материалы и другие промышленные товары, мы удовлетворяем все ваши потребности.",
        "description_tr": "Güneş enerjisi sistemleri, sokak ve bahçe lambaları, otomobiller, inşaat malzemeleri ve diğer endüstriyel ürünleri kapsayan geniş ürün yelpazemiz ile tüm ihtiyaçlarınızı karşılıyoruz.",
        "description_ar": "من خلال مجموعتنا الواسعة التي تغطي أنظمة الطاقة الشمسية وأضواء الشوارع والحدائق والسيارات ومواد البناء والمنتجات الصناعية الأخرى، نلبي جميع احتياجاتك.",
    },
    {
        "order": 6,
        "icon": "fas fa-shield-alt",
        "title_en": "Transparency and Quality Guarantee",
        "title_ru": "Прозрачность и гарантия качества",
        "title_tr": "Şeffaflık ve Kalite Garantisi",
        "title_ar": "الشفافية وضمان الجودة",
        "description_en": "Transparent pricing, quality inspection and reliable delivery are ensured in every order, minimizing risks.",
        "description_ru": "В каждом заказе обеспечиваются прозрачные цены, проверка качества и надежная доставка, минимизируя риски.",
        "description_tr": "Her siparişte şeffaf fiyatlandırma, kalite kontrolü ve güvenilir teslimat sağlanarak riskler minimize edilir.",
        "description_ar": "يتم ضمان التسعير الشفاف وفحص الجودة والتسليم الموثوق في كل طلب، مما يقلل المخاطر.",
    },
]

for feature_data in features_data:
    CompanyFeature.objects.create(**feature_data, is_active=True)
print(f"   ✓ Created {len(features_data)} company features")

# ============ STATISTICS ============
print("\n[5/8] Creating Statistics...")
Statistic.objects.all().delete()

statistics_data = [
    {
        "order": 1,
        "value": 50,
        "suffix": "+",
        "icon": "fas fa-project-diagram",
        "title_en": "Completed Projects",
        "title_ru": "Завершенных проектов",
        "title_tr": "Tamamlanan Proje",
        "title_ar": "المشاريع المنجزة",
    },
    {
        "order": 2,
        "value": 30,
        "suffix": "+",
        "icon": "fas fa-users",
        "title_en": "Satisfied Customers",
        "title_ru": "Довольных клиентов",
        "title_tr": "Memnun Müşteri",
        "title_ar": "العملاء الراضون",
    },
    {
        "order": 3,
        "value": 1,
        "suffix": "+",
        "icon": "fas fa-calendar-alt",
        "title_en": "Years of Experience",
        "title_ru": "Лет опыта",
        "title_tr": "Yıllık Deneyim",
        "title_ar": "سنوات من الخبرة",
    },
    {
        "order": 4,
        "value": 5,
        "suffix": " MW+",
        "icon": "fas fa-bolt",
        "title_en": "Installed Power",
        "title_ru": "Установленная мощность",
        "title_tr": "Kurulu Güç",
        "title_ar": "الطاقة المركبة",
    },
    {
        "order": 5,
        "value": 3,
        "suffix": "+",
        "icon": "fas fa-globe",
        "title_en": "Countries Covered",
        "title_ru": "Охваченных стран",
        "title_tr": "Kapsanan Ülke",
        "title_ar": "البلدان المشمولة",
    },
]

for stat_data in statistics_data:
    Statistic.objects.create(**stat_data, is_active=True)
print(f"   ✓ Created {len(statistics_data)} statistics")

# ============ PRODUCT CATEGORIES ============
print("\n[6/8] Creating Product Categories...")
ProductCategory.objects.all().delete()

categories_data = [
    {
        "order": 1,
        "icon": "fas fa-solar-panel",
        "slug": "solar-panels",
        "name_en": "Solar Panels",
        "name_ru": "Солнечные панели",
        "name_tr": "Güneş Panelleri",
        "name_ar": "الألواح الشمسية",
        "description_en": "High-efficiency solar panels and additional equipment for residential and industrial use.",
        "description_ru": "Высокоэффективные солнечные панели и дополнительное оборудование для жилого и промышленного использования.",
        "description_tr": "Ev ve endüstriyel kullanım için yüksek verimli güneş panelleri ve ek ekipman.",
        "description_ar": "ألواح شمسية عالية الكفاءة ومعدات إضافية للاستخدام السكني والصناعي.",
    },
    {
        "order": 2,
        "icon": "fas fa-lightbulb",
        "slug": "street-garden-lighting",
        "name_en": "Street and Garden Lighting",
        "name_ru": "Уличное и садовое освещение",
        "name_tr": "Sokak ve Bahçe Aydınlatması",
        "name_ar": "إضاءة الشوارع والحدائق",
        "description_en": "Energy-efficient street and garden lighting systems for public and private areas.",
        "description_ru": "Энергоэффективные системы уличного и садового освещения для общественных и частных территорий.",
        "description_tr": "Kamu ve özel alanlar için enerji verimli sokak ve bahçe aydınlatma sistemleri.",
        "description_ar": "أنظمة إضاءة الشوارع والحدائق الموفرة للطاقة للمناطق العامة والخاصة.",
    },
    {
        "order": 3,
        "icon": "fas fa-video",
        "slug": "security-cameras",
        "name_en": "Security Cameras",
        "name_ru": "Камеры безопасности",
        "name_tr": "Güvenlik Kameraları",
        "name_ar": "كاميرات الأمن",
        "description_en": "High-quality, modern technology cameras for security and surveillance.",
        "description_ru": "Высококачественные современные камеры для безопасности и наблюдения.",
        "description_tr": "Güvenlik ve gözetim için yüksek kaliteli, modern teknoloji kameralar.",
        "description_ar": "كاميرات عالية الجودة وتقنية حديثة للأمن والمراقبة.",
    },
    {
        "order": 4,
        "icon": "fas fa-car",
        "slug": "automobiles",
        "name_en": "Automobiles",
        "name_ru": "Автомобили",
        "name_tr": "Otomobiller",
        "name_ar": "السيارات",
        "description_en": "Supply of various car models and accessories for individual and corporate needs.",
        "description_ru": "Поставка различных моделей автомобилей и аксессуаров для индивидуальных и корпоративных нужд.",
        "description_tr": "Bireysel ve kurumsal ihtiyaçlar için çeşitli otomobil modelleri ve aksesuarların tedariki.",
        "description_ar": "توريد نماذج سيارات ومواد ملحقة مختلفة للاحتياجات الفردية والشركات.",
    },
    {
        "order": 5,
        "icon": "fas fa-hammer",
        "slug": "construction-materials",
        "name_en": "Construction Materials",
        "name_ru": "Строительные материалы",
        "name_tr": "İnşaat Malzemeleri",
        "name_ar": "مواد البناء",
        "description_en": "Quality materials and accessories for various construction projects.",
        "description_ru": "Качественные материалы и аксессуары для различных строительных проектов.",
        "description_tr": "Çeşitli inşaat projeleri için kaliteli malzemeler ve aksesuarlar.",
        "description_ar": "مواد وملحقات عالية الجودة لمشاريع البناء المختلفة.",
    },
    {
        "order": 6,
        "icon": "fas fa-industry",
        "slug": "industrial-products",
        "name_en": "Industrial Products",
        "name_ru": "Промышленные товары",
        "name_tr": "Endüstriyel Ürünler",
        "name_ar": "المنتجات الصناعية",
        "description_en": "Equipment and materials for factories, warehouses and other industrial areas.",
        "description_ru": "Оборудование и материалы для заводов, складов и других промышленных объектов.",
        "description_tr": "Fabrikalar, depolar ve diğer endüstriyel alanlar için ekipman ve malzemeler.",
        "description_ar": "معدات ومواد للمصانع والمستودعات والمناطق الصناعية الأخرى.",
    },
]

for cat_data in categories_data:
    ProductCategory.objects.create(**cat_data, is_active=True)
print(f"   ✓ Created {len(categories_data)} product categories")

# ============ PROCESS STEPS ============
print("\n[7/8] Creating Process Steps...")
ProcessStep.objects.all().delete()

steps_data = [
    {
        "order": 1,
        "icon": "fas fa-comments",
        "title_en": "Consultation and Order Reception",
        "title_ru": "Консультация и прием заказа",
        "title_tr": "Danışma ve Sipariş Alma",
        "title_ar": "الاستشارة واستلام الطلب",
        "description_en": "We carefully listen to customer needs, identify project requirements and offer the most suitable solutions.",
        "description_ru": "Мы внимательно слушаем потребности клиентов, определяем требования проекта и предлагаем наиболее подходящие решения.",
        "description_tr": "Müşterinin ihtiyaçlarını dikkatlice dinler, proje gereksinimlerini belirler ve en uygun çözümleri sunarız.",
        "description_ar": "نستمع بعناية لاحتياجات العملاء، ونحدد متطلبات المشروع ونقدم الحلول الأنسب.",
    },
    {
        "order": 2,
        "icon": "fas fa-search",
        "title_en": "Product Research and Selection",
        "title_ru": "Исследование и подбор продукции",
        "title_tr": "Ürün Araştırması ve Seçimi",
        "title_ar": "البحث واختيار المنتج",
        "description_en": "We research products suitable for the order in the Chinese market, compare quality and prices.",
        "description_ru": "Исследуем товары, подходящие для заказа, на китайском рынке, сравниваем качество и цены.",
        "description_tr": "Siparişe uygun ürünleri Çin pazarında araştırır, kalite ve fiyat karşılaştırması yaparız.",
        "description_ar": "نبحث عن المنتجات المناسبة للطلب في السوق الصيني، ونقارن الجودة والأسعار.",
    },
    {
        "order": 3,
        "icon": "fas fa-truck",
        "title_en": "Supply and Import",
        "title_ru": "Поставка и импорт",
        "title_tr": "Tedarik ve İthalat",
        "title_ar": "التوريد والاستيراد",
        "description_en": "We supply selected products from reliable suppliers and deliver them to the customer via international logistics.",
        "description_ru": "Поставляем выбранную продукцию от надежных поставщиков и доставляем клиенту через международную логистику.",
        "description_tr": "Seçilen ürünleri güvenilir tedarikçilerden temin eder ve uluslararası lojistik yoluyla müşteriye teslim ederiz.",
        "description_ar": "نوفر المنتجات المختارة من موردين موثوقين ونسلمها للعميل عبر اللوجستيات الدولية.",
    },
    {
        "order": 4,
        "icon": "fas fa-check-circle",
        "title_en": "Quality Inspection",
        "title_ru": "Проверка качества",
        "title_tr": "Kalite Kontrolü",
        "title_ar": "فحص الجودة",
        "description_en": "Before delivery, we check the quality of products and eliminate any inconsistencies.",
        "description_ru": "Перед доставкой проверяем качество товаров и устраняем любые несоответствия.",
        "description_tr": "Teslimat öncesi ürünlerin kalitesini kontrol eder, herhangi bir uyumsuzluğu gideririz.",
        "description_ar": "قبل التسليم، نفحص جودة المنتجات ونزيل أي تناقضات.",
    },
    {
        "order": 5,
        "icon": "fas fa-boxes",
        "title_en": "Delivery and Installation Support",
        "title_ru": "Доставка и поддержка установки",
        "title_tr": "Teslimat ve Kurulum Desteği",
        "title_ar": "التسليم ودعم التركيب",
        "description_en": "Products are delivered to the customer and installation and technical support are provided upon request.",
        "description_ru": "Продукция доставляется клиенту, по запросу предоставляется установка и техническая поддержка.",
        "description_tr": "Ürünler müşteriye teslim edilir ve talep üzerine kurulum ve teknik destek sağlanır.",
        "description_ar": "يتم تسليم المنتجات للعميل وتقديم دعم التركيب والدعم الفني عند الطلب.",
    },
    {
        "order": 6,
        "icon": "fas fa-headset",
        "title_en": "After-Sales Service",
        "title_ru": "Послепродажное обслуживание",
        "title_tr": "Satış Sonrası Hizmet",
        "title_ar": "خدمة ما بعد البيع",
        "description_en": "We monitor customer satisfaction, provide necessary instructions, technical assistance and additional support.",
        "description_ru": "Отслеживаем удовлетворенность клиентов, предоставляем необходимые инструкции, техническую помощь и дополнительную поддержку.",
        "description_tr": "Müşteri memnuniyetini izler, gerekli talimatları, teknik yardımı ve ek desteği sağlarız.",
        "description_ar": "نراقب رضا العملاء، ونقدم التعليمات اللازمة والمساعدة الفنية والدعم الإضافي.",
    },
]

for step_data in steps_data:
    ProcessStep.objects.create(**step_data, is_active=True)
print(f"   ✓ Created {len(steps_data)} process steps")

# ============ FAQ ============
print("\n[8/8] Creating FAQs...")
FAQ.objects.all().delete()

faqs_data = [
    {
        "order": 1,
        "question_en": "How can I place an order for products?",
        "question_ru": "Как я могу разместить заказ на продукцию?",
        "question_tr": "Ürünleri nasıl sipariş edebilirim?",
        "question_ar": "كيف يمكنني تقديم طلب للمنتجات؟",
        "answer_en": "You can place an order via the website or by contacting our sales representative directly. We offer products tailored to customer needs.",
        "answer_ru": "Вы можете разместить заказ через сайт или напрямую связавшись с нашим торговым представителем. Мы предлагаем товары, адаптированные к потребностям клиентов.",
        "answer_tr": "Site üzerinden veya doğrudan satış temsilcimizle iletişime geçerek sipariş verebilirsiniz. Müşteri ihtiyaçlarına uygun ürünler sunuyoruz.",
        "answer_ar": "يمكنك تقديم طلب عبر الموقع أو بالاتصال مباشرة بممثل المبيعات لدينا. نقدم منتجات مصممة خصيصًا لاحتياجات العملاء.",
    },
    {
        "order": 2,
        "question_en": "What is the delivery time for products?",
        "question_ru": "Каков срок доставки продукции?",
        "question_tr": "Ürünlerin teslimat süresi ne kadardır?",
        "question_ar": "ما هي مدة تسليم المنتجات؟",
        "answer_en": "Delivery time varies between 7-30 business days depending on the product and quantity. Exact information is provided after order confirmation.",
        "answer_ru": "Срок доставки варьируется от 7 до 30 рабочих дней в зависимости от товара и количества. Точная информация предоставляется после подтверждения заказа.",
        "answer_tr": "Teslimat süresi ürün ve miktara bağlı olarak 7-30 iş günü arasında değişir. Sipariş onaylandıktan sonra kesin bilgi verilir.",
        "answer_ar": "يختلف وقت التسليم بين 7-30 يوم عمل حسب المنتج والكمية. يتم تقديم معلومات دقيقة بعد تأكيد الطلب.",
    },
    {
        "order": 3,
        "question_en": "Do you guarantee the quality of the products you supply?",
        "question_ru": "Вы гарантируете качество поставляемой продукции?",
        "question_tr": "Tedarik ettiğiniz ürünlerin kalitesini garanti ediyor musunuz?",
        "question_ar": "هل تضمنون جودة المنتجات التي توفرونها؟",
        "answer_en": "Yes, all our products undergo quality inspection and are provided with compliance guarantee.",
        "answer_ru": "Да, вся наша продукция проходит проверку качества и предоставляется с гарантией соответствия.",
        "answer_tr": "Evet, tüm ürünlerimiz kalite kontrolünden geçer ve uygunluk garantisi ile sağlanır.",
        "answer_ar": "نعم، جميع منتجاتنا تخضع لفحص الجودة وتُقدم مع ضمان المطابقة.",
    },
    {
        "order": 4,
        "question_en": "Do you also ship products to foreign countries?",
        "question_ru": "Вы также отправляете товары в зарубежные страны?",
        "question_tr": "Yurt dışı ülkelere de ürün gönderiyor musunuz?",
        "question_ar": "هل ترسلون المنتجات أيضًا إلى الدول الأجنبية؟",
        "answer_en": "Yes, we supply products to various countries through our international logistics network.",
        "answer_ru": "Да, мы поставляем товары в различные страны через нашу международную логистическую сеть.",
        "answer_tr": "Evet, uluslararası lojistik ağımız aracılığıyla çeşitli ülkelere ürün tedariki gerçekleştiriyoruz.",
        "answer_ar": "نعم، نقوم بتوريد المنتجات إلى بلدان مختلفة من خلال شبكة اللوجستيات الدولية لدينا.",
    },
    {
        "order": 5,
        "question_en": "Do you also provide services for individual projects?",
        "question_ru": "Вы также оказываете услуги для индивидуальных проектов?",
        "question_tr": "Bireysel projeler için de hizmet veriyor musunuz?",
        "question_ar": "هل تقدمون خدمات للمشاريع الفردية أيضًا؟",
        "answer_en": "Yes, we have special product research and supply services for individual orders and projects.",
        "answer_ru": "Да, у нас есть специальные услуги по исследованию и поставке продукции для индивидуальных заказов и проектов.",
        "answer_tr": "Evet, bireysel siparişler ve projeler için özel ürün araştırması ve tedarik hizmetimiz mevcuttur.",
        "answer_ar": "نعم، لدينا خدمات بحث وتوريد خاصة للطلبات والمشاريع الفردية.",
    },
    {
        "order": 6,
        "question_en": "Is there technical support for products?",
        "question_ru": "Есть ли техническая поддержка для продукции?",
        "question_tr": "Ürünler için teknik destek var mı?",
        "question_ar": "هل يوجد دعم فني للمنتجات؟",
        "answer_en": "Yes, we provide after-sales technical support and installation assistance.",
        "answer_ru": "Да, мы предоставляем послепродажную техническую поддержку и помощь в установке.",
        "answer_tr": "Evet, satış sonrası teknik destek ve kurulum yardımı sağlıyoruz.",
        "answer_ar": "نعم، نقدم الدعم الفني بعد البيع ومساعدة التركيب.",
    },
    {
        "order": 7,
        "question_en": "How are prices determined?",
        "question_ru": "Как определяются цены?",
        "question_tr": "Fiyatlar nasıl belirlenir?",
        "question_ar": "كيف يتم تحديد الأسعار؟",
        "answer_en": "Prices vary according to product category, quantity and supply source. We offer you the most optimal option.",
        "answer_ru": "Цены варьируются в зависимости от категории товара, количества и источника поставки. Мы предлагаем вам наиболее оптимальный вариант.",
        "answer_tr": "Fiyatlar ürün kategorisi, miktarı ve tedarik kaynağına göre değişir. Size en uygun seçeneği sunuyoruz.",
        "answer_ar": "تختلف الأسعار حسب فئة المنتج والكمية ومصدر التوريد. نقدم لك الخيار الأمثل.",
    },
    {
        "order": 8,
        "question_en": "Can I get consultation before ordering?",
        "question_ru": "Могу ли я получить консультацию перед заказом?",
        "question_tr": "Sipariş öncesi danışmanlık alabilir miyim?",
        "question_ar": "هل يمكنني الحصول على استشارة قبل الطلب؟",
        "answer_en": "Of course, we provide free consultation for product selection and strategy suitable for your project.",
        "answer_ru": "Конечно, мы предоставляем бесплатные консультации по выбору продукции и стратегии, подходящей для вашего проекта.",
        "answer_tr": "Elbette, projenize uygun ürün seçimi ve strateji için ücretsiz danışmanlık hizmeti veriyoruz.",
        "answer_ar": "بالطبع، نقدم استشارة مجانية لاختيار المنتجات والاستراتيجية المناسبة لمشروعك.",
    },
]

for faq_data in faqs_data:
    FAQ.objects.create(**faq_data, is_active=True)
print(f"   ✓ Created {len(faqs_data)} FAQs")

# ============ NEWS (OPTIONAL) ============
print("\n[OPTIONAL] Creating sample news article...")
news_cat, _ = NewsCategory.objects.get_or_create(
    slug="company-news",
    defaults={
        "name_en": "Company News",
        "name_ru": "Новости компании",
        "name_tr": "Şirket Haberleri",
        "name_ar": "أخبار الشركة",
        "order": 1,
    }
)

News.objects.filter(slug__icontains="street-garden").delete()
news1 = News.objects.create(
    category=news_cat,
    slug="new-street-garden-lighting-projects",
    
    title_en="New Street and Garden Lighting Projects",
    title_ru="Новые проекты по уличному и садовому освещению",
    title_tr="Yeni Sokak ve Bahçe Aydınlatma Projeleri",
    title_ar="مشاريع إضاءة الشوارع والحدائق الجديدة",
    
    summary_en="VAAM offers innovative solutions in city and garden lighting systems.",
    summary_ru="VAAM предлагает инновационные решения в системах городского и садового освещения.",
    summary_tr="VAAM, şehir ve bahçe aydınlatma sistemlerinde yenilikçi çözümler sunuyor.",
    summary_ar="تقدم VAAM حلولاً مبتكرة في أنظمة إضاءة المدن والحدائق.",
    
    content_en="This year, VAAM completed several street and garden lighting projects in public and private areas. Energy-efficient and durable lighting systems ensured both security and aesthetic appearance.",
    content_ru="В этом году VAAM завершила несколько проектов по уличному и садовому освещению на общественных и частных территориях. Энергоэффективные и долговечные системы освещения обеспечили как безопасность, так и эстетический вид.",
    content_tr="Bu yıl VAAM, kamu ve özel alanlarda birkaç sokak ve bahçe aydınlatma projesini tamamladı. Enerji verimli ve dayanıklı aydınlatma sistemleri hem güvenliği hem de estetik görünümü sağladı.",
    content_ar="هذا العام، أكملت VAAM عدة مشاريع لإضاءة الشوارع والحدائق في المناطق العامة والخاصة. ضمنت أنظمة الإضاءة الموفرة للطاقة والمتينة كلاً من الأمن والمظهر الجمالي.",
    
    image="news/placeholder.jpg",
    author="VAAM Team",
    reading_time=3,
    is_published=True,
    is_featured=True,
    published_at=timezone.now()
)
print(f"   ✓ Created news article: {news1.title_en}")

# ============ SUMMARY ============
print("\n" + "=" * 80)
print("  ✓ CLIENT DATA SEEDING COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\nSummary:")
print(f"  • Site Settings:        Updated")
print(f"  • Hero Slides:          1 created")
print(f"  • Company Info:         Updated (Mission, Vision, Values, History)")
print(f"  • Company Features:     {len(features_data)} created")
print(f"  • Statistics:           {len(statistics_data)} created")
print(f"  • Product Categories:   {len(categories_data)} created")
print(f"  • Process Steps:        {len(steps_data)} created")
print(f"  • FAQs:                 {len(faqs_data)} created")
print(f"  • News:                 1 created")
print("\nAll data has been added in 4 languages: EN, RU, TR, AR")
print("\nTo run this script on production server:")
print("  1. Upload this file to the server")
print("  2. cd /path/to/vaam")
print("  3. source venv/bin/activate")
print("  4. python manage.py shell < seed_client_data.py")
print("=" * 80)
