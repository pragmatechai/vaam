"""
URL configuration for vaam_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView, TemplateView
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import sitemaps

# Dashboard URLs (no language prefix)
urlpatterns = [
    path('admin/', RedirectView.as_view(url='/dashboard/', permanent=True)),
    path('dashboard/', include('dashboard.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
]

# Front-end URLs (with language prefix: /en/, /ru/, /tr/, /ar/)
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
