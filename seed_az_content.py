"""
Azerbaijani (az) copy for database content.

Matches on the English text, so it is safe to re-run and skips anything it does
not know; those fields fall back to English. Run it after seed_content_update.py,
which recreates the hero slides.

Usage: python seed_az_content.py
"""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaam_project.settings')
django.setup()

from django.apps import apps  # noqa: E402

SITE_SETTINGS = {
    'site_name_az': 'VAAM Global',
    'meta_title_az': 'VAAM Global – Çindən tədarük, yoxlanmış fabriklər və keyfiyyət yoxlaması',
    'meta_description_az': (
        'Bizneslər üçün Çindən tədarük: generatorlar, paylayıcı transformatorlar, məişət texnikası, '
        'təhlükəsizlik kameraları, avtomobillər, küçə və bağ işıqlandırması, tikinti materialları və '
        'sənaye məhsulları. Yoxlanmış fabriklər, fabrikdə keyfiyyət yoxlaması, gömrük sənədləri.'
    ),
    'meta_keywords_az': (
        'Çindən tədarük, yoxlanmış fabriklər, keyfiyyət yoxlaması, gömrük sənədləri, generatorlar, '
        'transformatorlar, məişət texnikası, təhlükəsizlik kameraları, avtomobillər, küçə işıqlandırması, '
        'tikinti materialları, sənaye məhsulları, VAAM Global'
    ),
    'site_description_az': (
        'VAAM Global, VAAM Import and Export Trading Co., LTD şirkətinin tədarük brendidir. Bizneslər üçün '
        'yoxlanmış Çin fabriklərindən, fabrikdə keyfiyyət yoxlaması və gömrük sənədləri ilə tədarük edirik.'
    ),
}

AZ = {
    # Hero
    'China sourcing · Verified factories · Factory QC': 'Çindən tədarük · Yoxlanmış fabriklər · Keyfiyyət yoxlaması',
    'Your Trusted Sourcing Partner in China': 'Çində etibarlı tədarük tərəfdaşınız',
    'Right Product. Right Price. Reliable Supplier.': 'Doğru məhsul. Doğru qiymət. Etibarlı təchizatçı.',
    'End-to-End Procurement & Quality Control': 'Tam satınalma və keyfiyyətə nəzarət',
    'Direct From Manufacturers': 'Birbaşa istehsalçılardan',
    'From Factory to Your Door': 'Fabrikdən qapınıza qədər',
    'VAAM Import and Export Trading Co., LTD supports international clients with efficient, transparent, and secure product sourcing from China.':
        'VAAM Import and Export Trading Co., LTD beynəlxalq müştərilərə Çindən səmərəli, şəffaf və təhlükəsiz məhsul tədarükündə dəstək olur.',
    'We find, negotiate, and deliver the products you need — working directly with Chinese manufacturers to ensure quality and competitive pricing.':
        'Lazım olan məhsulları tapır, danışıqlar aparır və çatdırırıq — keyfiyyət və rəqabətli qiymət üçün birbaşa Çin istehsalçıları ilə işləyirik.',
    'Supplier selection, quality inspection, customs documentation, and delivery coordination — we handle every step so you can focus on your business.':
        'Təchizatçı seçimi, keyfiyyət yoxlaması, gömrük sənədləri və çatdırılma koordinasiyası — siz biznesinizə fokuslanın, hər addımı biz həll edək.',
    'Get a Quote': 'Qiymət təklifi al',
    'View Products': 'Məhsullara bax',
    'Learn More': 'Ətraflı',
    'Our Services': 'Xidmətlərimiz',
    'Submit Inquiry': 'Sorğu göndər',
    'Contact Us': 'Bizimlə əlaqə',

    # Company features
    'Direct Manufacturer Partnership': 'İstehsalçılarla birbaşa tərəfdaşlıq',
    'Quality Control & Inspection': 'Keyfiyyətə nəzarət və yoxlama',
    'Full Transparency': 'Tam şəffaflıq',
    'Price & Terms Optimization': 'Qiymət və şərtlərin optimallaşdırılması',
    'We work directly with manufacturers in China, eliminating middlemen to ensure the best prices and quality for our clients.':
        'Müştərilərimizə ən yaxşı qiymət və keyfiyyəti təmin etmək üçün vasitəçilər olmadan birbaşa Çin istehsalçıları ilə işləyirik.',
    'Every product is inspected at the factory before shipment. We provide photos, videos, and detailed inspection reports to our clients.':
        'Hər məhsul göndərişdən əvvəl fabrikdə yoxlanılır. Müştərilərimizə foto, video və ətraflı yoxlama hesabatları təqdim edirik.',
    'We keep our clients informed at every stage with real-time updates, real product photos, and clear pricing under EXW and FOB terms.':
        'Müştərilərimizi hər mərhələdə real vaxtda yeniliklər, real məhsul fotoları və EXW, FOB şərtləri üzrə aydın qiymətlərlə məlumatlandırırıq.',
    'We negotiate the best possible prices and commercial terms on your behalf, ensuring maximum value for every order.':
        'Hər sifarişdən maksimum dəyər əldə etmək üçün sizin adınızdan ən yaxşı qiymət və kommersiya şərtləri üzrə danışıqlar aparırıq.',

    # Statistics
    'Core Services': 'Əsas xidmət',
    'Step Order Process': 'Addımlı sifariş prosesi',
    'Year+ Product Warranty': 'İl+ məhsul zəmanəti',
    'Trade Terms (EXW & FOB)': 'Ticarət şərti (EXW və FOB)',

    # Categories
    'Generators': 'Generatorlar',
    'Distribution Transformers': 'Paylayıcı transformatorlar',
    'Household Appliances': 'Məişət texnikası',
    'Security Cameras': 'Təhlükəsizlik kameraları',
    'Automobiles': 'Avtomobillər',
    'Street & Garden Lighting': 'Küçə və bağ işıqlandırması',
    'Construction Materials': 'Tikinti materialları',
    'Industrial Products': 'Sənaye məhsulları',
    'Solar Energy Systems': 'Günəş enerjisi sistemləri',
    'Procurement Services': 'Satınalma xidmətləri',
    'Energy & Power': 'Enerji',

    # Services
    'Product Supply & Procurement': 'Məhsul təchizatı və satınalma',
    'Supplier Selection & Verification': 'Təchizatçı seçimi və yoxlanması',
    'Quality Inspection': 'Keyfiyyət yoxlaması',
    'Logistics & Delivery Coordination': 'Logistika və çatdırılma koordinasiyası',
    'Customs Documentation Support': 'Gömrük sənədləri üzrə dəstək',
    'Technical Consulting': 'Texniki məsləhət',
    'Installation Guidance': 'Quraşdırma üzrə təlimat',
    'After-Sales Service': 'Satışdan sonrakı xidmət',
    'We organize the supply of products in various categories directly from manufacturers in China, tailored to your specific requirements.':
        'Tələblərinizə uyğun olaraq müxtəlif kateqoriyalarda məhsulların birbaşa Çin istehsalçılarından təchizatını təşkil edirik.',
    'Suppliers are carefully selected based on quality, price, production capacity, and reliability. We present multiple alternatives for your evaluation.':
        'Təchizatçılar keyfiyyət, qiymət, istehsal gücü və etibarlılıq əsasında diqqətlə seçilir. Qiymətləndirməniz üçün bir neçə alternativ təqdim edirik.',
    'Products are inspected on-site at the factory before shipment. We provide clients with photos, videos, and detailed inspection reports.':
        'Məhsullar göndərişdən əvvəl fabrikdə yerində yoxlanılır. Müştərilərə foto, video və ətraflı yoxlama hesabatları təqdim edirik.',
    'Products are delivered under EXW or FOB terms. We coordinate handover to your logistics partner and provide reliable forwarding recommendations when needed.':
        'Məhsullar EXW və ya FOB şərtləri ilə təhvil verilir. Logistika tərəfdaşınıza təhvili koordinasiya edir, lazım olduqda etibarlı ekspeditor tövsiyə edirik.',
    'We prepare all necessary export documents including Invoice, Packing List, and other customs paperwork to ensure a smooth import process.':
        'Rahat idxal prosesi üçün invoys, qablaşdırma siyahısı və digər gömrük sənədləri daxil olmaqla bütün ixrac sənədlərini hazırlayırıq.',
    'We provide technical support for choosing the right product. Various manufacturers and alternatives are compared to offer the best solution.':
        'Doğru məhsulun seçimi üçün texniki dəstək göstəririk. Ən yaxşı həlli təklif etmək üçün müxtəlif istehsalçılar və alternativlər müqayisə olunur.',
    'While we do not provide on-site installation, all technical documents and manuals from manufacturers are provided to support your installation process.':
        'Yerində quraşdırma xidməti göstərmirik, lakin quraşdırma prosesinizə dəstək üçün istehsalçıların bütün texniki sənədləri və təlimatları təqdim olunur.',
    'We coordinate warranty claims and technical issues between you and the manufacturer, and assist with spare parts sourcing and ordering.':
        'Zəmanət iddialarını və texniki məsələləri sizinlə istehsalçı arasında koordinasiya edir, ehtiyat hissələrinin tapılmasına və sifarişinə kömək edirik.',

    # Process steps
    'Submit Your Inquiry': 'Sorğunuzu göndərin',
    'Receive Our Proposal': 'Təklifimizi alın',
    'Agreement & Contract': 'Razılaşma və müqavilə',
    'Payment': 'Ödəniş',
    'Production & Quality Check': 'İstehsal və keyfiyyət yoxlaması',
    'Handover (EXW / FOB)': 'Təhvil (EXW / FOB)',
    'Delivery & Receipt': 'Çatdırılma və qəbul',
    'Contact us via website, WhatsApp, or email with details about the products you need.':
        'Lazım olan məhsullar haqqında məlumatla sayt, WhatsApp və ya e-poçt vasitəsilə bizimlə əlaqə saxlayın.',
    'Within 24–48 hours we prepare and present you with pricing, specifications, and delivery timeline.':
        '24–48 saat ərzində qiymət, texniki göstəricilər və çatdırılma müddətini hazırlayıb sizə təqdim edirik.',
    'Terms are agreed upon and a formal contract is prepared and signed by both parties.':
        'Şərtlər razılaşdırılır, rəsmi müqavilə hazırlanır və hər iki tərəf tərəfindən imzalanır.',
    'Standard payment: 30% advance upon order confirmation, 70% balance before shipment via bank transfer (T/T).':
        'Standart ödəniş: sifariş təsdiqləndikdə 30% avans, göndərişdən əvvəl 70% qalıq, bank köçürməsi (T/T) ilə.',
    'Products are prepared and inspected at the factory. You receive photos and videos for confirmation before final payment.':
        'Məhsullar fabrikdə hazırlanır və yoxlanılır. Son ödənişdən əvvəl təsdiq üçün foto və videolar alırsınız.',
    'After full payment, products are handed over to your logistics partner under EXW or FOB terms.':
        'Tam ödənişdən sonra məhsullar EXW və ya FOB şərtləri ilə logistika tərəfdaşınıza təhvil verilir.',
    'You receive your products via your chosen logistics company. We remain available for any after-sales support.':
        'Məhsullarınızı seçdiyiniz logistika şirkəti vasitəsilə alırsınız. Satışdan sonrakı dəstək üçün yanınızdayıq.',

    # Menu
    'Home': 'Ana səhifə',
    'About': 'Haqqımızda',
    'About Us': 'Haqqımızda',
    'Services': 'Xidmətlər',
    'Products': 'Məhsullar',
    'Projects': 'Layihələr',
    'News': 'Xəbərlər',
    'Contact': 'Əlaqə',
    'Main Navigation': 'Əsas naviqasiya',

    # FAQ
    'What is the minimum order quantity?': 'Minimum sifariş miqdarı nə qədərdir?',
    'How long does delivery take?': 'Çatdırılma nə qədər çəkir?',
    'What warranty do you provide?': 'Hansı zəmanəti verirsiniz?',
    'Where are products sourced from?': 'Məhsullar haradan tədarük olunur?',
    'Can I order from a specific brand?': 'Konkret brenddən sifariş verə bilərəmmi?',
    'Are technical datasheets provided?': 'Texniki sənədlər təqdim olunurmu?',
    'How are prices determined?': 'Qiymətlər necə müəyyən olunur?',
    'Do you offer discounts?': 'Endirim edirsinizmi?',
    'What are the payment terms?': 'Ödəniş şərtləri necədir?',
    'What documents are provided with the order?': 'Sifarişlə hansı sənədlər təqdim olunur?',
    'Can you ship to any country?': 'İstənilən ölkəyə göndərə bilərsinizmi?',
    'How is packaging handled?': 'Qablaşdırma necə aparılır?',
    'Is cargo insurance included?': 'Yük sığortası daxildirmi?',
    'How do I make a warranty claim?': 'Zəmanət iddiasını necə təqdim edim?',
    'How are disputes resolved?': 'Mübahisələr necə həll olunur?',
    'Are special terms available for large projects?': 'Böyük layihələr üçün xüsusi şərtlər varmı?',
    'Do you provide on-site technical specialists?': 'Yerində texniki mütəxəssis təqdim edirsinizmi?',
    'Minimum order varies depending on the product. In most cases, 1 unit is possible for testing purposes. Wholesale orders start from 5 units or more. Better pricing is available for bulk orders.':
        'Minimum sifariş məhsuldan asılıdır. Əksər hallarda sınaq üçün 1 ədəd mümkündür. Topdan sifarişlər 5 və daha çox ədəddən başlayır. Böyük sifarişlər üçün daha sərfəli qiymət təklif olunur.',
    'Stock products: 7–10 days. Made-to-order products: 25–40 days. International delivery time depends on the logistics partner chosen by the client.':
        'Anbarda olan məhsullar: 7–10 gün. Sifarişlə hazırlanan məhsullar: 25–40 gün. Beynəlxalq çatdırılma müddəti müştərinin seçdiyi logistika tərəfdaşından asılıdır.',
    'Products come with a minimum 1-year warranty. In some cases, manufacturers offer 2–3 year warranties. Warranty covers manufacturing defects only; normal wear and tear is not included.':
        'Məhsullara minimum 1 il zəmanət verilir. Bəzi hallarda istehsalçılar 2–3 il zəmanət təklif edir. Zəmanət yalnız istehsal qüsurlarını əhatə edir; normal köhnəlmə daxil deyil.',
    'All products are sourced exclusively from China. We work with verified manufacturers and suppliers across the country.':
        'Bütün məhsullar yalnız Çindən tədarük olunur. Ölkə üzrə yoxlanmış istehsalçı və təchizatçılarla işləyirik.',
    'Yes, products can be sourced according to the brand you request. Our company is not limited to specific brands — we find the supplier and brand that best match your requirements, budget, and quality expectations.':
        'Bəli, məhsullar istədiyiniz brendə uyğun tədarük oluna bilər. Şirkətimiz konkret brendlərlə məhdudlaşmır — tələblərinizə, büdcənizə və keyfiyyət gözləntilərinizə ən uyğun təchizatçı və brendi tapırıq.',
    'Yes, technical documents (PDF datasheets) provided by the manufacturer are shared with the client for every product.':
        'Bəli, istehsalçının təqdim etdiyi texniki sənədlər (PDF) hər məhsul üzrə müştəri ilə paylaşılır.',
    'Prices vary depending on the product, order volume, and technical specifications. Each client receives a personalized quote. Prices are primarily presented in US Dollars (USD). Prices are provided under EXW (Ex Works) or FOB (Free on Board) terms and cover only the product cost. Delivery, insurance, and import costs are not included.':
        'Qiymətlər məhsuldan, sifarişin həcmindən və texniki göstəricilərdən asılıdır. Hər müştəri fərdi qiymət təklifi alır. Qiymətlər əsasən ABŞ dolları ilə verilir. Qiymətlər EXW (Ex Works) və ya FOB (Free on Board) şərtləri ilə təqdim olunur və yalnız məhsulun dəyərini əhatə edir. Çatdırılma, sığorta və idxal xərcləri daxil deyil.',
    'Yes, special discounts are available for bulk orders, repeat customers, and long-term partnership agreements.':
        'Bəli, böyük sifarişlər, daimi müştərilər və uzunmüddətli tərəfdaşlıq razılaşmaları üçün xüsusi endirimlər var.',
    'Payments are made by official bank transfer (T/T) only, based on a signed contract. Standard terms: 30% advance after order confirmation, remaining 70% after product approval and before shipment. The advance amount may vary depending on the product and order volume. No credit or installment options are available.':
        'Ödənişlər yalnız imzalanmış müqavilə əsasında rəsmi bank köçürməsi (T/T) ilə aparılır. Standart şərtlər: sifariş təsdiqləndikdən sonra 30% avans, qalan 70% məhsul təsdiqləndikdən sonra və göndərişdən əvvəl. Avansın məbləği məhsuldan və sifarişin həcmindən asılı olaraq dəyişə bilər. Kredit və ya hissə-hissə ödəniş imkanı yoxdur.',
    'We provide: Proforma Invoice, Commercial Invoice, Packing List, Export documents, and Bill of Lading (for FOB shipments). All orders include a formal contract, typically prepared in English.':
        'Təqdim edirik: proforma invoys, kommersiya invoysu, qablaşdırma siyahısı, ixrac sənədləri və konosament (FOB göndərişləri üçün). Bütün sifarişlər adətən ingilis dilində hazırlanan rəsmi müqavilə ilə aparılır.',
    'Yes, products can be shipped from China to any country. Delivery is carried out by the logistics company chosen by the client.':
        'Bəli, məhsullar Çindən istənilən ölkəyə göndərilə bilər. Çatdırılmanı müştərinin seçdiyi logistika şirkəti həyata keçirir.',
    'Products are export-packaged by the manufacturer to international standards: wooden crates, pallets, carton packaging, or container-suitable wrapping as appropriate.':
        'Məhsullar istehsalçı tərəfindən beynəlxalq standartlara uyğun ixrac qablaşdırması ilə hazırlanır: taxta yeşiklər, paletlər, karton qablaşdırma və ya konteynerə uyğun bağlama.',
    'Cargo insurance is the responsibility of the client and is arranged through their chosen logistics partner.':
        'Yük sığortası müştərinin məsuliyyətindədir və seçdiyi logistika tərəfdaşı vasitəsilə təşkil olunur.',
    'Submit photo and video evidence of the issue. After investigation, we coordinate with the manufacturer to provide the most suitable solution: spare parts, replacement, or compensation.':
        'Problemin foto və video sübutlarını təqdim edin. Araşdırmadan sonra ən uyğun həll üçün istehsalçı ilə koordinasiya edirik: ehtiyat hissələri, dəyişdirmə və ya kompensasiya.',
    'Disputes are resolved through mutual agreement first. If necessary, they are handled according to the terms specified in the contract and Chinese legislation.':
        'Mübahisələr əvvəlcə qarşılıqlı razılıqla həll olunur. Lazım gələrsə, müqavilədə göstərilən şərtlərə və Çin qanunvericiliyinə uyğun baxılır.',
    'Yes, special pricing and partnership terms are available for large-volume and long-term projects. Contact us to discuss your specific requirements.':
        'Bəli, böyük həcmli və uzunmüddətli layihələr üçün xüsusi qiymət və tərəfdaşlıq şərtləri var. Tələblərinizi müzakirə etmək üçün bizimlə əlaqə saxlayın.',
    'Our company does not provide on-site technical specialist services. However, manufacturers can provide technical documentation and remote support to assist with installation and operation.':
        'Şirkətimiz yerində texniki mütəxəssis xidməti göstərmir. Lakin istehsalçılar quraşdırma və istismar üçün texniki sənədlər və uzaqdan dəstək təqdim edə bilər.',

    # Company info
    'Professional Sourcing & Procurement Solutions in China': 'Çində peşəkar tədarük və satınalma həlləri',
    'VAAM Import and Export Trading Co., LTD is a professional sourcing and procurement company operating in China. We support international clients in organizing product sourcing from China in an efficient, transparent, and secure manner. Our primary goal is to provide our clients with the right product, at the right price, from reliable suppliers.':
        'VAAM Import and Export Trading Co., LTD Çində fəaliyyət göstərən peşəkar tədarük və satınalma şirkətidir. Beynəlxalq müştərilərə Çindən məhsul tədarükünü səmərəli, şəffaf və təhlükəsiz təşkil etməkdə dəstək oluruq. Əsas məqsədimiz müştərilərimizə doğru məhsulu, doğru qiymətə, etibarlı təchizatçılardan təqdim etməkdir.',
    'Our mission is to make product sourcing from China simpler, safer, and more efficient for businesses, and to build long-term, reliable partnerships.':
        'Missiyamız bizneslər üçün Çindən məhsul tədarükünü daha sadə, təhlükəsiz və səmərəli etmək, uzunmüddətli etibarlı tərəfdaşlıqlar qurmaqdır.',
    'To be the most trusted sourcing partner between China and the world, providing seamless procurement solutions that empower businesses to grow globally.':
        'Bizneslərin qlobal böyüməsinə imkan verən rahat satınalma həlləri ilə Çin və dünya arasında ən etibarlı tədarük tərəfdaşı olmaq.',
    'We operate not just as intermediaries, but as trusted business partners.\n\n• Direct collaboration with manufacturers\n• Supplier verification and selection\n• Price and terms optimization\n• Full control over the order process\n\nWe provide our clients with complete transparency and timely updates at every stage.':
        'Biz sadəcə vasitəçi deyil, etibarlı biznes tərəfdaşı kimi çalışırıq.\n\n• İstehsalçılarla birbaşa əməkdaşlıq\n• Təchizatçıların yoxlanması və seçimi\n• Qiymət və şərtlərin optimallaşdırılması\n• Sifariş prosesinə tam nəzarət\n\nMüştərilərimizə hər mərhələdə tam şəffaflıq və vaxtında məlumat təqdim edirik.',
    '2023 – Company establishment and commencement of international trading activities\n2023 – Formation of supplier network in Chinese market\n2024 – Expansion of activities in solar energy, lighting and construction materials\n2025 – Increase in customer portfolio and international partnerships':
        '2023 – Şirkətin yaradılması və beynəlxalq ticarət fəaliyyətinə başlanması\n2023 – Çin bazarında təchizatçı şəbəkəsinin formalaşması\n2024 – Günəş enerjisi, işıqlandırma və tikinti materialları üzrə fəaliyyətin genişlənməsi\n2025 – Müştəri portfelinin və beynəlxalq tərəfdaşlıqların artması',
}

FIELDS = {
    'HeroSlide': ('title', 'subtitle', 'description', 'button1_text', 'button2_text'),
    'CompanyInfo': ('subtitle', 'description', 'mission', 'vision', 'values', 'history'),
    'CompanyFeature': ('title', 'description'),
    'Statistic': ('title',),
    'ProductCategory': ('name',),
    'ServiceCategory': ('name',),
    'Service': ('title', 'short_description'),
    'ProcessStep': ('title', 'description'),
    'ProjectCategory': ('name',),
    'Menu': ('title',),
    'MenuItem': ('title',),
    'FAQ': ('question', 'answer'),
}


def normalize(text):
    return (text or '').replace('\r\n', '\n').replace('%%', '%').strip()


def apply():
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.get_or_create(pk=1)
    SiteSettings.objects.filter(pk=1).update(**SITE_SETTINGS)

    updated = missed = 0
    for model_name, fields in FIELDS.items():
        model = apps.get_model('core', model_name)
        for row in model.objects.all():
            changes = {}
            for field in fields:
                english = normalize(getattr(row, f'{field}_en'))
                if english in AZ:
                    changes[f'{field}_az'] = AZ[english]
                elif english:
                    missed += 1
            if changes:
                model.objects.filter(pk=row.pk).update(**changes)
                updated += 1
    return updated, missed


if __name__ == '__main__':
    done, unknown = apply()
    print(f'az content: {done} rows updated, {unknown} fields left on English fallback')
