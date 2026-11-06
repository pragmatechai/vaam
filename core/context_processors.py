from django.conf import settings as django_settings
from django.core.cache import cache
from django.utils.translation import get_language

from .models import SiteSettings, Service, Menu, Page


def clear_site_cache():
    """Clear all cached context processor data (call after saving menus, settings, etc.)."""
    for lang_code, _ in django_settings.LANGUAGES:
        cache.delete(f'ctx_site_settings_{lang_code}')


def site_url(request):
    """Public origin used for absolute URLs (no trailing slash)."""
    return {'site_url': django_settings.SITE_URL or request.build_absolute_uri('/').rstrip('/')}


def site_settings(request):
    """Make site settings, footer services, dynamic menus, and footer pages available in all templates.

    Results are cached per-language for 5 minutes to avoid hitting the database on every request.
    """
    lang = get_language() or 'en'
    cache_key = f'ctx_site_settings_{lang}'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        s = SiteSettings.get_settings()
    except Exception:
        s = None

    # Dynamic menus – keyed by location for easy template access
    menus = {}
    for menu in Menu.objects.filter(is_active=True).prefetch_related(
        'items', 'items__children', 'items__page'
    ):
        menus[menu.location] = menu

    footer_pages = list(Page.objects.filter(is_published=True, show_in_footer=True))

    result = {
        'settings': s,
        'footer_services': list(Service.objects.filter(is_active=True)[:5]),
        'dynamic_menus': menus,
        'footer_pages': footer_pages,
    }

    cache.set(cache_key, result, 300)  # Cache for 5 minutes
    return result
