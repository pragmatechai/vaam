import importlib
import json
import re

from django.core.cache import cache
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import activate

from .models import HeroSlide, Product, ProductCategory, SiteSettings

SITE_URL = 'https://vaamglobal.com'
INSTAGRAM = 'https://www.instagram.com/vaamglobal/'
TIKTOK = 'https://www.tiktok.com/@vaamglobal'


def jsonld_blocks(html):
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    return [json.loads(block) for block in re.findall(pattern, html, re.S)]


@override_settings(SITE_URL=SITE_URL)
class BrandAndSeoTests(TestCase):
    def setUp(self):
        cache.clear()
        activate('en')
        site = SiteSettings.get_settings()
        site.site_name = 'VAAM Global'
        site.meta_title = 'VAAM Global – China Sourcing, Verified Factories & QC'
        site.meta_description = 'Verified factories, factory QC, customs docs.'
        site.instagram = INSTAGRAM
        site.tiktok = TIKTOK
        site.address = 'Room 688, "Huanshi" Road, Guangzhou'
        site.save()

    def tearDown(self):
        cache.clear()

    def home(self):
        return self.client.get(reverse('core:home')).content.decode()

    def test_home_title_uses_brand_title(self):
        self.assertIn(
            '<title>VAAM Global – China Sourcing, Verified Factories &amp; QC</title>',
            self.home(),
        )

    def test_share_image_is_https_png(self):
        html = self.home()
        for tag in ('property="og:image"', 'name="twitter:image"'):
            url = re.search(rf'<meta {tag} content="([^"]+)"', html).group(1)
            self.assertTrue(url.startswith(f'{SITE_URL}/'), url)
            self.assertTrue(url.endswith('.png'), url)

    def test_absolute_urls_ignore_request_scheme(self):
        html = self.home()
        self.assertIn(f'<meta property="og:url" content="{SITE_URL}/en/">', html)
        self.assertIn(f'<link rel="canonical" href="{SITE_URL}/en/">', html)
        self.assertIn(f'hreflang="ru" href="{SITE_URL}/ru/"', html)
        self.assertNotIn('content="http://', html)

    def test_single_valid_organization_with_social_profiles(self):
        blocks = jsonld_blocks(self.home())
        orgs = [b for b in blocks if b.get('@type') == 'Organization']
        self.assertEqual(len(orgs), 1)
        org = orgs[0]
        self.assertEqual(org['name'], 'VAAM Global')
        self.assertEqual(org['url'], f'{SITE_URL}/')
        self.assertTrue(org['logo'].startswith(f'{SITE_URL}/'))
        self.assertTrue(org['logo'].endswith('.png'))
        self.assertEqual(org['sameAs'], [INSTAGRAM, TIKTOK])
        self.assertEqual(org['address']['addressLocality'], 'Room 688, "Huanshi" Road, Guangzhou')

    def test_tiktok_link_in_header_and_footer(self):
        self.assertEqual(self.home().count(f'href="{TIKTOK}"'), 2)

    def test_home_has_one_h1_with_slides(self):
        for order in range(3):
            HeroSlide.objects.create(title=f'Slide {order}', image='hero/x.jpg', order=order)
        self.assertEqual(self.home().count('<h1'), 1)

    def test_home_has_one_h1_without_slides(self):
        self.assertEqual(self.home().count('<h1'), 1)

    def test_unproven_trust_claims_removed(self):
        self.assertNotIn('ISO Certified', self.home())
        inquiry = self.client.get(reverse('core:product_inquiry')).content.decode()
        self.assertNotIn('50+', inquiry)

    def test_brand_copy_has_no_old_name_or_solar_in_metadata(self):
        html = self.home()
        head = html[:html.index('</head>')]
        self.assertNotIn('VAAM Trading', html)
        self.assertNotIn('solar', head.lower())

    def test_robots_points_to_https_sitemap(self):
        body = self.client.get('/robots.txt').content.decode()
        self.assertIn(f'Sitemap: {SITE_URL}/sitemap.xml', body)

    def test_sitemap_uses_https(self):
        body = self.client.get('/sitemap.xml').content.decode()
        self.assertIn('<loc>https://', body)
        self.assertNotIn('<loc>http://', body)


class TranslatedBrandTests(TestCase):
    def test_translated_page_uses_new_brand(self):
        cache.clear()
        html = self.client.get('/ru/about/').content.decode()
        self.assertNotIn('VAAM Trading', html)
        self.assertIn('VAAM Global', html)


class BrandDataMigrationTests(TestCase):
    """Runs the data step against historical models, as `migrate` does."""

    def setUp(self):
        cache.clear()
        self.migration = importlib.import_module('core.migrations.0011_vaam_global_brand')
        state = MigrationExecutor(connection).loader.project_state([('core', '0010_sitesettings_tiktok')])
        self.apps = state.apps
        self.SiteSettings = self.apps.get_model('core', 'SiteSettings')

    def test_rebrands_settings_and_keeps_only_instagram_and_tiktok(self):
        self.SiteSettings.objects.update_or_create(pk=1, defaults={
            'site_name': 'VAAM Import and Export Trading Co., LTD',
            'instagram': 'https://instagram.com/vaamtrading',
            'facebook': 'https://facebook.com/vaamtrading',
            'linkedin': 'https://linkedin.com/company/vaamtrading',
            'youtube': 'https://youtube.com/@vaamtrading',
            'twitter': 'https://twitter.com/vaamtrading',
        })

        self.migration.apply_brand(self.apps, None)

        row = self.SiteSettings.objects.values().get(pk=1)
        for lang in ('', '_en', '_ru', '_tr', '_ar'):
            self.assertEqual(row[f'site_name{lang}'], 'VAAM Global')
            self.assertIn('VAAM Global', row[f'meta_title{lang}'])
            self.assertTrue(row[f'meta_description{lang}'])
            self.assertTrue(row[f'meta_keywords{lang}'])
            self.assertTrue(row[f'site_description{lang}'])
        self.assertNotIn('olar', row['meta_description_en'])
        self.assertEqual(row['instagram'], INSTAGRAM)
        self.assertEqual(row['tiktok'], TIKTOK)
        for network in ('facebook', 'linkedin', 'youtube', 'twitter'):
            self.assertEqual(row[network], '')

    def test_first_hero_slide_uses_social_bio(self):
        HeroSlide = self.apps.get_model('core', 'HeroSlide')
        second = HeroSlide.objects.create(title='B', image='hero/b.jpg', order=2, subtitle='Keep me', subtitle_en='Keep me')
        first = HeroSlide.objects.create(title='A', image='hero/a.jpg', order=1, subtitle='Old', subtitle_en='Old')

        self.migration.apply_brand(self.apps, None)

        row = HeroSlide.objects.values().get(pk=first.pk)
        self.assertEqual(row['subtitle'], 'China sourcing · Verified factories · Factory QC')
        self.assertEqual(row['subtitle_en'], 'China sourcing · Verified factories · Factory QC')
        for lang in ('ru', 'tr', 'ar'):
            self.assertTrue(row[f'subtitle_{lang}'])
        self.assertEqual(HeroSlide.objects.values().get(pk=second.pk)['subtitle_en'], 'Keep me')

    def test_creates_settings_on_empty_database(self):
        self.SiteSettings.objects.all().delete()
        self.migration.apply_brand(self.apps, None)
        self.assertEqual(self.SiteSettings.objects.get(pk=1).instagram, INSTAGRAM)

    def test_replaces_old_name_in_content(self):
        category = ProductCategory.objects.create(name='Appliances', slug='appliances')
        product = Product.objects.create(name='TV', slug='tv', category=category, description='x')
        HistoricalProduct = self.apps.get_model('core', 'Product')
        HistoricalProduct.objects.filter(pk=product.pk).update(
            meta_title_en='55 TV | VAAM Trading', meta_title_ru='ТВ | VAAM Trading',
        )

        self.migration.apply_brand(self.apps, None)

        row = HistoricalProduct.objects.values('meta_title_en', 'meta_title_ru').get(pk=product.pk)
        self.assertEqual(row['meta_title_en'], '55 TV | VAAM Global')
        self.assertEqual(row['meta_title_ru'], 'ТВ | VAAM Global')
