"""
Django sitemaps — auto-generates /sitemap.xml for search engines.
Covers static pages, products, projects, and news articles.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product, Project, News, Page


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'
    i18n = True  # generates a URL per language

    def items(self):
        return ['home', 'about', 'services', 'products', 'projects', 'news', 'contact']

    def location(self, item):
        return reverse(f'core:{item}')


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    i18n = True

    def items(self):
        return Product.objects.filter(is_active=True).only('slug', 'updated_at')

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    i18n = True

    def items(self):
        return Project.objects.filter(is_active=True).only('slug', 'created_at')

    def lastmod(self, obj):
        return obj.created_at


class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6
    i18n = True

    def items(self):
        return News.objects.filter(is_published=True).only('slug', 'updated_at')

    def lastmod(self, obj):
        return obj.updated_at


class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    i18n = True

    def items(self):
        return Page.objects.filter(is_published=True).only('slug', 'updated_at')

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'projects': ProjectSitemap,
    'news': NewsSitemap,
    'pages': PageSitemap,
}
