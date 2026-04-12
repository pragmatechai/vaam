"""
Add translations for new navigation submenu items to all .po files.
"""
import os

NEW_TRANSLATIONS = {
    "Mission & Vision": {
        "tr": "Misyon & Vizyon",
        "ru": "Миссия и видение",
        "ar": "الرسالة والرؤية",
    },
    "Who we are & what we do": {
        "tr": "Biz kimik və nə edirik",
        "ru": "Кто мы и чем занимаемся",
        "ar": "من نحن وماذا نفعل",
    },
    "Our goals & values": {
        "tr": "Hədəflərimiz və dəyərlərimiz",
        "ru": "Наши цели и ценности",
        "ar": "أهدافنا وقيمنا",
    },
    "Meet the professionals": {
        "tr": "Peşəkarlarla tanış olun",
        "ru": "Познакомьтесь с профессионалами",
        "ar": "تعرف على المحترفين",
    },
    "Standards & accreditations": {
        "tr": "Standartlar və akkreditasiyalar",
        "ru": "Стандарты и аккредитации",
        "ar": "المعايير والاعتمادات",
    },
    "Clients & References": {
        "tr": "Müştərilər və Referanslar",
        "ru": "Клиенты и рекомендации",
        "ar": "العملاء والمراجع",
    },
    "Trusted partnerships": {
        "tr": "Etibarlı tərəfdaşlıqlar",
        "ru": "Надёжные партнёрства",
        "ar": "شراكات موثوقة",
    },
    "Partners & Brands": {
        "tr": "Tərəfdaşlar və Brendlər",
        "ru": "Партнёры и бренды",
        "ar": "الشركاء والعلامات التجارية",
    },
    "Manufacturer partners": {
        "tr": "İstehsalçı tərəfdaşlar",
        "ru": "Партнёры-производители",
        "ar": "شركاء التصنيع",
    },
    "Common questions answered": {
        "tr": "Tez-tez verilən suallar",
        "ru": "Ответы на частые вопросы",
        "ar": "إجابات على الأسئلة الشائعة",
    },
    "Full range of our solutions": {
        "tr": "Həllərimizin tam çeşidi",
        "ru": "Полный спектр наших решений",
        "ar": "مجموعة كاملة من حلولنا",
    },
    "Our step-by-step process": {
        "tr": "Addım-addım prosesimiz",
        "ru": "Наш пошаговый процесс",
        "ar": "عملياتنا خطوة بخطوة",
    },
    "Quality Inspection": {
        "tr": "Keyfiyyət Yoxlaması",
        "ru": "Контроль качества",
        "ar": "فحص الجودة",
    },
    "Factory QC & assurance": {
        "tr": "Fabrik keyfiyyət nəzarəti",
        "ru": "Заводской контроль качества",
        "ar": "مراقبة الجودة والضمان",
    },
    "Get pricing for your order": {
        "tr": "Sifarişiniz üçün qiymət alın",
        "ru": "Получите цену для вашего заказа",
        "ar": "احصل على أسعار لطلبك",
    },
    "Completed deliveries": {
        "tr": "Tamamlanmış tədarüklər",
        "ru": "Завершённые поставки",
        "ar": "عمليات التسليم المكتملة",
    },
    "Photos & videos": {
        "tr": "Foto və videolar",
        "ru": "Фото и видео",
        "ar": "الصور والفيديو",
    },
    "Case Studies": {
        "tr": "İş Nümunələri",
        "ru": "Кейсы",
        "ar": "دراسات الحالة",
    },
    "Success stories": {
        "tr": "Uğur hekayələri",
        "ru": "Истории успеха",
        "ar": "قصص النجاح",
    },
}

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

def add_translations():
    for lang in ["tr", "ru", "ar"]:
        po_path = os.path.join(LOCALE_DIR, lang, "LC_MESSAGES", "django.po")
        if not os.path.exists(po_path):
            print(f"  SKIP {lang}: {po_path} not found")
            continue

        with open(po_path, "r", encoding="utf-8") as f:
            content = f.read()

        added = 0
        for msgid, translations in NEW_TRANSLATIONS.items():
            # Check if msgid already exists
            escaped = msgid.replace('"', '\\"')
            if f'msgid "{escaped}"' in content:
                continue
            msgstr = translations.get(lang, "")
            entry = f'\nmsgid "{escaped}"\nmsgstr "{msgstr}"\n'
            content += entry
            added += 1

        with open(po_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  {lang}: added {added} new translations")

    # Also update EN file (msgstr = msgid for English)
    en_po = os.path.join(LOCALE_DIR, "en", "LC_MESSAGES", "django.po")
    if os.path.exists(en_po):
        with open(en_po, "r", encoding="utf-8") as f:
            content = f.read()
        added = 0
        for msgid in NEW_TRANSLATIONS:
            escaped = msgid.replace('"', '\\"')
            if f'msgid "{escaped}"' in content:
                continue
            entry = f'\nmsgid "{escaped}"\nmsgstr "{escaped}"\n'
            content += entry
            added += 1
        with open(en_po, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  en: added {added} new translations")

if __name__ == "__main__":
    print("Adding nav translations...")
    add_translations()
    print("Done!")
