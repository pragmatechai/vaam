"""Move site data to the VAAM Global brand used on Instagram and TikTok.

Only Instagram and TikTok stay on the site. The old vaamtrading Facebook, LinkedIn,
YouTube and Twitter links are cleared; the header, footer and schema skip empty links.
"""
from django.db import migrations

OLD_NAME = 'VAAM Trading'
NEW_NAME = 'VAAM Global'
LANGS = ('en', 'ru', 'tr', 'ar')

INSTAGRAM = 'https://www.instagram.com/vaamglobal/'
TIKTOK = 'https://www.tiktok.com/@vaamglobal'
RETIRED_NETWORKS = ('facebook', 'linkedin', 'youtube', 'twitter')

COPY = {
    'meta_title': {
        'en': 'VAAM Global – China Sourcing, Verified Factories & QC',
        'ru': 'VAAM Global – Закупки из Китая, проверенные фабрики и контроль качества',
        'tr': "VAAM Global – Çin'den Tedarik, Doğrulanmış Fabrikalar ve Kalite Kontrol",
        'ar': 'VAAM Global – التوريد من الصين ومصانع موثوقة ومراقبة الجودة',
    },
    'meta_description': {
        'en': 'China sourcing for businesses: generators, distribution transformers, household '
              'appliances, security cameras, automobiles, street & garden lighting, construction '
              'materials and industrial products. Verified factories, factory QC, customs docs.',
        'ru': 'Закупки из Китая для бизнеса: генераторы, распределительные трансформаторы, бытовая '
              'техника, камеры безопасности, автомобили, уличное и садовое освещение, стройматериалы '
              'и промышленные товары. Проверенные фабрики, контроль качества на фабрике, таможенные документы.',
        'tr': "İşletmeler için Çin'den tedarik: jeneratörler, dağıtım transformatörleri, ev aletleri, "
              'güvenlik kameraları, otomobiller, sokak ve bahçe aydınlatması, inşaat malzemeleri ve '
              'endüstriyel ürünler. Doğrulanmış fabrikalar, fabrikada kalite kontrol, gümrük belgeleri.',
        'ar': 'التوريد من الصين للشركات: مولدات ومحولات توزيع وأجهزة منزلية وكاميرات أمنية وسيارات '
              'وإضاءة الشوارع والحدائق ومواد البناء والمنتجات الصناعية. مصانع موثوقة ومراقبة الجودة '
              'في المصنع والمستندات الجمركية.',
    },
    'meta_keywords': {
        'en': 'China sourcing, verified factories, factory QC, customs documents, generators, '
              'distribution transformers, household appliances, security cameras, automobiles, '
              'street lighting, construction materials, industrial products, VAAM Global',
        'ru': 'закупки из Китая, проверенные фабрики, контроль качества, таможенные документы, '
              'генераторы, трансформаторы, бытовая техника, камеры безопасности, автомобили, '
              'уличное освещение, стройматериалы, промышленные товары, VAAM Global',
        'tr': "Çin'den tedarik, doğrulanmış fabrikalar, fabrika kalite kontrol, gümrük belgeleri, "
              'jeneratörler, transformatörler, ev aletleri, güvenlik kameraları, otomobiller, '
              'sokak aydınlatması, inşaat malzemeleri, endüstriyel ürünler, VAAM Global',
        'ar': 'التوريد من الصين, مصانع موثوقة, مراقبة الجودة, مستندات جمركية, مولدات, محولات, '
              'أجهزة منزلية, كاميرات أمنية, سيارات, إضاءة الشوارع, مواد البناء, منتجات صناعية, VAAM Global',
    },
    'site_description': {
        'en': 'VAAM Global is the sourcing brand of VAAM Import and Export Trading Co., LTD. '
              'We source from verified Chinese factories for businesses, with factory QC and customs documents.',
        'ru': 'VAAM Global — бренд компании VAAM Import and Export Trading Co., LTD. Мы закупаем товары '
              'для бизнеса на проверенных китайских фабриках с контролем качества и таможенными документами.',
        'tr': "VAAM Global, VAAM Import and Export Trading Co., LTD'nin tedarik markasıdır. İşletmeler için "
              'doğrulanmış Çin fabrikalarından, fabrikada kalite kontrol ve gümrük belgeleriyle tedarik yapıyoruz.',
        'ar': 'VAAM Global هي العلامة التجارية لشركة VAAM Import and Export Trading Co., LTD. نوفر للشركات '
              'المنتجات من مصانع صينية موثوقة مع مراقبة الجودة في المصنع والمستندات الجمركية.',
    },
}

# First hero slide repeats the Instagram/TikTok bio.
HERO_SUBTITLE = {
    'en': 'China sourcing · Verified factories · Factory QC',
    'ru': 'Закупки из Китая · Проверенные фабрики · Контроль качества',
    'tr': "Çin'den Tedarik · Doğrulanmış Fabrikalar · Fabrikada Kalite Kontrol",
    'ar': 'التوريد من الصين · مصانع موثوقة · مراقبة الجودة في المصنع',
}

# Published copy only. Customer-written records (messages, inquiries, testimonials) stay as sent.
CONTENT_FIELDS = {
    'Product': ('meta_title', 'meta_description', 'description', 'short_description'),
    'ProductCategory': ('description',),
    'Service': ('description', 'short_description'),
    'News': ('title', 'summary', 'content'),
    'Project': ('title', 'description'),
    'Page': ('meta_title', 'content'),
    'HeroSlide': ('title', 'description'),
    'CompanyInfo': ('title', 'description'),
    'FAQ': ('question', 'answer'),
    'CaseStudy': ('challenge', 'solution', 'results'),
}


def localized_columns(model, field_name):
    """Return the base column and its translated columns that exist on the model."""
    names = {field.name for field in model._meta.get_fields()}
    candidates = [field_name] + [f'{field_name}_{lang}' for lang in LANGS]
    return [name for name in candidates if name in names]


def apply_brand(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    site, _ = SiteSettings.objects.get_or_create(pk=1)

    site.site_name = NEW_NAME
    for lang in LANGS:
        setattr(site, f'site_name_{lang}', NEW_NAME)
    for field, values in COPY.items():
        setattr(site, field, values['en'])
        for lang, value in values.items():
            setattr(site, f'{field}_{lang}', value)
    site.instagram = INSTAGRAM
    site.tiktok = TIKTOK
    for network in RETIRED_NETWORKS:
        setattr(site, network, '')
    site.save()

    HeroSlide = apps.get_model('core', 'HeroSlide')
    first_slide = HeroSlide.objects.filter(is_active=True).order_by('order', 'pk').first()
    if first_slide:
        values = {f'subtitle_{lang}': text for lang, text in HERO_SUBTITLE.items()}
        HeroSlide.objects.filter(pk=first_slide.pk).update(subtitle=HERO_SUBTITLE['en'], **values)

    for model_name, fields in CONTENT_FIELDS.items():
        model = apps.get_model('core', model_name)
        for field in fields:
            for column in localized_columns(model, field):
                rows = model.objects.filter(**{f'{column}__contains': OLD_NAME})
                for row in rows:
                    new_value = getattr(row, column).replace(OLD_NAME, NEW_NAME)
                    model.objects.filter(pk=row.pk).update(**{column: new_value})


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_sitesettings_tiktok'),
    ]

    operations = [
        # Replaced copy is not restorable; reversing leaves the data as it is.
        migrations.RunPython(apply_brand, migrations.RunPython.noop),
    ]
