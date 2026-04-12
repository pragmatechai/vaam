"""Add new translation strings for gallery, FAQ, team, certificates, process pages."""
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# New translations to add
NEW_TRANSLATIONS = {
    'ru': {
        'Gallery': 'Галерея',
        'Our Gallery': 'Наша Галерея',
        'Explore our collection of project photos, product images, and company videos.': 'Изучите нашу коллекцию фотографий проектов, изображений продуктов и корпоративных видео.',
        'All': 'Все',
        'No gallery items yet': 'Пока нет элементов галереи',
        'Gallery items will appear here once they are added.': 'Элементы галереи появятся здесь после добавления.',
        'Interested in Our Products?': 'Заинтересованы в наших продуктах?',
        'Send us an inquiry and our team will get back to you within 24 hours.': 'Отправьте нам запрос, и наша команда свяжется с вами в течение 24 часов.',
        'FAQ': 'FAQ',
        'Frequently Asked Questions': 'Часто задаваемые вопросы',
        'Find answers to common questions about our services, processes, and trade operations.': 'Найдите ответы на распространённые вопросы о наших услугах, процессах и торговых операциях.',
        'No FAQs yet': 'Пока нет вопросов',
        'Frequently asked questions will appear here.': 'Часто задаваемые вопросы появятся здесь.',
        'Still have questions?': 'Остались вопросы?',
        'Our team is ready to help you with any questions about our services.': 'Наша команда готова помочь вам с любыми вопросами о наших услугах.',
        'Our Team': 'Наша команда',
        'Meet Our Team': 'Познакомьтесь с нашей командой',
        'The professionals behind VAAM\'s success in global trade and procurement.': 'Профессионалы, стоящие за успехом VAAM в международной торговле и закупках.',
        'Team members coming soon': 'Информация о команде скоро появится',
        'Our team information will be added shortly.': 'Информация о нашей команде будет добавлена в ближайшее время.',
        'Join Our Team': 'Присоединяйтесь к нашей команде',
        'We are always looking for talented professionals to join our growing team.': 'Мы всегда ищем талантливых профессионалов для нашей растущей команды.',
        'Certificates & Quality': 'Сертификаты и качество',
        'Our certifications and accreditations guarantee the highest standards of quality and reliability.': 'Наши сертификаты и аккредитации гарантируют высочайшие стандарты качества и надёжности.',
        'Our Certificates': 'Наши сертификаты',
        'Official certificates that demonstrate our commitment to quality.': 'Официальные сертификаты, подтверждающие наше стремление к качеству.',
        'Accreditations & Licenses': 'Аккредитации и лицензии',
        'Our trade licenses and professional memberships.': 'Наши торговые лицензии и профессиональные членства.',
        'Valid until': 'Действителен до',
        'Company Documents': 'Документы компании',
        'Download our company profile, catalogs, and brochures.': 'Скачайте профиль компании, каталоги и брошюры.',
        'downloads': 'скачиваний',
        'How We Work': 'Как мы работаем',
        'Our Process': 'Наш процесс',
        'Our proven step-by-step process ensures transparent and efficient product sourcing from China.': 'Наш проверенный пошаговый процесс обеспечивает прозрачный и эффективный поиск продукции из Китая.',
        'Step': 'Шаг',
        'Process steps coming soon': 'Этапы процесса скоро появятся',
        'Ready to Start?': 'Готовы начать?',
        'Begin your sourcing journey with VAAM today.': 'Начните свой путь поиска товаров с VAAM уже сегодня.',
        'Company Overview': 'О компании',
        'All Services': 'Все услуги',
        'Request a Quote': 'Запросить цену',
        'Projects': 'Проекты',
        'Quality': 'Качество',
    },
    'tr': {
        'Gallery': 'Galeri',
        'Our Gallery': 'Galerimiz',
        'Explore our collection of project photos, product images, and company videos.': 'Proje fotoğrafları, ürün görselleri ve şirket videolarımızı keşfedin.',
        'All': 'Tümü',
        'No gallery items yet': 'Henüz galeri öğesi yok',
        'Gallery items will appear here once they are added.': 'Galeri öğeleri eklendikten sonra burada görünecektir.',
        'Interested in Our Products?': 'Ürünlerimizle ilgileniyor musunuz?',
        'Send us an inquiry and our team will get back to you within 24 hours.': 'Bize bir talep gönderin, ekibimiz 24 saat içinde size geri dönüş yapacaktır.',
        'FAQ': 'SSS',
        'Frequently Asked Questions': 'Sıkça Sorulan Sorular',
        'Find answers to common questions about our services, processes, and trade operations.': 'Hizmetlerimiz, süreçlerimiz ve ticari operasyonlarımız hakkındaki yaygın soruların cevaplarını bulun.',
        'No FAQs yet': 'Henüz SSS yok',
        'Frequently asked questions will appear here.': 'Sıkça sorulan sorular burada görünecektir.',
        'Still have questions?': 'Hâlâ sorularınız mı var?',
        'Our team is ready to help you with any questions about our services.': 'Ekibimiz hizmetlerimiz hakkındaki sorularınıza yardımcı olmaya hazırdır.',
        'Our Team': 'Ekibimiz',
        'Meet Our Team': 'Ekibimizle Tanışın',
        'The professionals behind VAAM\'s success in global trade and procurement.': 'VAAM\'ın küresel ticaret ve tedarikteki başarısının arkasındaki profesyoneller.',
        'Team members coming soon': 'Ekip bilgileri yakında',
        'Our team information will be added shortly.': 'Ekip bilgilerimiz kısa süre içinde eklenecektir.',
        'Join Our Team': 'Ekibimize Katılın',
        'We are always looking for talented professionals to join our growing team.': 'Büyüyen ekibimize katılacak yetenekli profesyoneller arıyoruz.',
        'Certificates & Quality': 'Sertifikalar ve Kalite',
        'Our certifications and accreditations guarantee the highest standards of quality and reliability.': 'Sertifikalarımız ve akreditasyonlarımız en yüksek kalite ve güvenilirlik standartlarını garanti eder.',
        'Our Certificates': 'Sertifikalarımız',
        'Official certificates that demonstrate our commitment to quality.': 'Kaliteye olan bağlılığımızı gösteren resmi sertifikalar.',
        'Accreditations & Licenses': 'Akreditasyonlar ve Lisanslar',
        'Our trade licenses and professional memberships.': 'Ticaret lisanslarımız ve profesyonel üyeliklerimiz.',
        'Valid until': 'Geçerlilik tarihi',
        'Company Documents': 'Şirket Belgeleri',
        'Download our company profile, catalogs, and brochures.': 'Şirket profilimizi, kataloglarımızı ve broşürlerimizi indirin.',
        'downloads': 'indirme',
        'How We Work': 'Nasıl Çalışırız',
        'Our Process': 'Sürecimiz',
        'Our proven step-by-step process ensures transparent and efficient product sourcing from China.': 'Kanıtlanmış adım adım sürecimiz, Çin\'den şeffaf ve verimli ürün tedariğini sağlar.',
        'Step': 'Adım',
        'Process steps coming soon': 'Süreç adımları yakında',
        'Ready to Start?': 'Başlamaya Hazır mısınız?',
        'Begin your sourcing journey with VAAM today.': 'VAAM ile tedarik yolculuğunuza bugün başlayın.',
        'Company Overview': 'Şirkete Genel Bakış',
        'All Services': 'Tüm Hizmetler',
        'Request a Quote': 'Teklif İsteyin',
        'Projects': 'Projeler',
        'Quality': 'Kalite',
    },
    'ar': {
        'Gallery': 'المعرض',
        'Our Gallery': 'معرضنا',
        'Explore our collection of project photos, product images, and company videos.': 'استكشف مجموعتنا من صور المشاريع وصور المنتجات ومقاطع فيديو الشركة.',
        'All': 'الكل',
        'No gallery items yet': 'لا توجد عناصر في المعرض بعد',
        'Gallery items will appear here once they are added.': 'ستظهر عناصر المعرض هنا بمجرد إضافتها.',
        'Interested in Our Products?': 'مهتم بمنتجاتنا؟',
        'Send us an inquiry and our team will get back to you within 24 hours.': 'أرسل لنا استفسارًا وسيتواصل معك فريقنا خلال 24 ساعة.',
        'FAQ': 'الأسئلة الشائعة',
        'Frequently Asked Questions': 'الأسئلة الشائعة',
        'Find answers to common questions about our services, processes, and trade operations.': 'اعثر على إجابات للأسئلة الشائعة حول خدماتنا وعملياتنا التجارية.',
        'No FAQs yet': 'لا توجد أسئلة شائعة بعد',
        'Frequently asked questions will appear here.': 'ستظهر الأسئلة الشائعة هنا.',
        'Still have questions?': 'لا تزال لديك أسئلة؟',
        'Our team is ready to help you with any questions about our services.': 'فريقنا مستعد لمساعدتك في أي أسئلة حول خدماتنا.',
        'Our Team': 'فريقنا',
        'Meet Our Team': 'تعرف على فريقنا',
        'The professionals behind VAAM\'s success in global trade and procurement.': 'المحترفون وراء نجاح VAAM في التجارة العالمية والمشتريات.',
        'Team members coming soon': 'معلومات الفريق قريبًا',
        'Our team information will be added shortly.': 'سيتم إضافة معلومات فريقنا قريبًا.',
        'Join Our Team': 'انضم إلى فريقنا',
        'We are always looking for talented professionals to join our growing team.': 'نحن نبحث دائمًا عن محترفين موهوبين للانضمام إلى فريقنا المتنامي.',
        'Certificates & Quality': 'الشهادات والجودة',
        'Our certifications and accreditations guarantee the highest standards of quality and reliability.': 'تضمن شهاداتنا واعتماداتنا أعلى معايير الجودة والموثوقية.',
        'Our Certificates': 'شهاداتنا',
        'Official certificates that demonstrate our commitment to quality.': 'شهادات رسمية تثبت التزامنا بالجودة.',
        'Accreditations & Licenses': 'الاعتمادات والتراخيص',
        'Our trade licenses and professional memberships.': 'تراخيصنا التجارية وعضوياتنا المهنية.',
        'Valid until': 'صالح حتى',
        'Company Documents': 'وثائق الشركة',
        'Download our company profile, catalogs, and brochures.': 'قم بتنزيل ملف الشركة والكتالوجات والكتيبات.',
        'downloads': 'تنزيلات',
        'How We Work': 'كيف نعمل',
        'Our Process': 'عمليتنا',
        'Our proven step-by-step process ensures transparent and efficient product sourcing from China.': 'عمليتنا المثبتة خطوة بخطوة تضمن توريد منتجات شفاف وفعال من الصين.',
        'Step': 'خطوة',
        'Process steps coming soon': 'خطوات العملية قريبًا',
        'Ready to Start?': 'مستعد للبدء؟',
        'Begin your sourcing journey with VAAM today.': 'ابدأ رحلة التوريد مع VAAM اليوم.',
        'Company Overview': 'نظرة عامة على الشركة',
        'All Services': 'جميع الخدمات',
        'Request a Quote': 'طلب عرض أسعار',
        'Projects': 'المشاريع',
        'Quality': 'الجودة',
    },
}


def add_translations_to_po(lang_code, translations):
    po_path = os.path.join(BASE_DIR, 'locale', lang_code, 'LC_MESSAGES', 'django.po')
    if not os.path.exists(po_path):
        print(f"[SKIP] {po_path} not found")
        return

    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()

    added = 0
    for msgid, msgstr in translations.items():
        # Check if already exists
        escaped_msgid = msgid.replace('"', '\\"')
        if f'msgid "{escaped_msgid}"' in content:
            continue

        entry = f'\n#: auto-generated\nmsgid "{escaped_msgid}"\nmsgstr "{msgstr.replace(chr(34), chr(92)+chr(34))}"\n'
        content += entry
        added += 1

    with open(po_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[{lang_code}] Added {added} new translations")


def compile_po_to_mo(lang_code):
    """Pure Python .po → .mo compiler."""
    import struct
    import array

    po_path = os.path.join(BASE_DIR, 'locale', lang_code, 'LC_MESSAGES', 'django.po')
    mo_path = os.path.join(BASE_DIR, 'locale', lang_code, 'LC_MESSAGES', 'django.mo')

    if not os.path.exists(po_path):
        return

    messages = []
    with open(po_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    msgid = None
    msgstr = None
    current = None

    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('#'):
            continue
        if line.startswith('msgid '):
            if msgid is not None and msgstr is not None:
                messages.append((msgid, msgstr))
            msgid = line[6:].strip().strip('"')
            msgstr = None
            current = 'id'
        elif line.startswith('msgstr '):
            msgstr = line[7:].strip().strip('"')
            current = 'str'
        elif line.startswith('"') and line.endswith('"'):
            val = line[1:-1]
            if current == 'id':
                msgid = (msgid or '') + val
            elif current == 'str':
                msgstr = (msgstr or '') + val
        elif line.strip() == '':
            if msgid is not None and msgstr is not None:
                messages.append((msgid, msgstr))
            msgid = None
            msgstr = None
            current = None

    if msgid is not None and msgstr is not None:
        messages.append((msgid, msgstr))

    # Filter out empty translations and the metadata entry
    output = []
    for mid, mstr in messages:
        mid = mid.replace('\\n', '\n').replace('\\"', '"')
        mstr = mstr.replace('\\n', '\n').replace('\\"', '"')
        if mid == '':
            output.append((b'', mstr.encode('utf-8')))
        elif mstr:
            output.append((mid.encode('utf-8'), mstr.encode('utf-8')))

    output.sort(key=lambda x: x[0])

    # Write .mo file
    num_strings = len(output)
    ids = b''
    strs = b''
    id_offsets = []
    str_offsets = []

    for mid, mstr in output:
        id_offsets.append((len(mid), len(ids)))
        ids += mid + b'\x00'
        str_offsets.append((len(mstr), len(strs)))
        strs += mstr + b'\x00'

    keystart = 7 * 4
    valuestart = keystart + num_strings * 8
    ids_start = valuestart + num_strings * 8

    koffsets = []
    voffsets = []
    for length, offset in id_offsets:
        koffsets.append(length)
        koffsets.append(offset + ids_start)
    for length, offset in str_offsets:
        voffsets.append(length)
        voffsets.append(offset + ids_start + len(ids))

    with open(mo_path, 'wb') as f:
        f.write(struct.pack('Iiiiiii',
            0x950412de,  # magic
            0,           # version
            num_strings, # number of strings
            keystart,    # offset of table with original strings
            valuestart,  # offset of table with translations
            0,           # size of hashing table
            0,           # offset of hashing table
        ))
        f.write(array.array('i', koffsets).tobytes())
        f.write(array.array('i', voffsets).tobytes())
        f.write(ids)
        f.write(strs)

    print(f"[{lang_code}] Compiled .mo ({num_strings} strings)")


if __name__ == '__main__':
    for lang in ['ru', 'tr', 'ar']:
        add_translations_to_po(lang, NEW_TRANSLATIONS[lang])
        compile_po_to_mo(lang)
    print("\nDone!")
