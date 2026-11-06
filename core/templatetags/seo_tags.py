"""
SEO template tags for multilingual hreflang URL generation.
"""
import json

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

LANG_CODES = [code for code, _ in settings.LANGUAGES]


@register.simple_tag(takes_context=True)
def alternate_url(context, lang_code):
    """
    Return the absolute URL of the current page translated to the given language.

    URL structure (i18n_patterns with prefix_default_language=True):
        /en/products/slug/
        /ru/products/slug/
    So we just replace the first path segment with the target lang_code.
    """
    request = context.get('request')
    if not request:
        return ''
    path = request.path  # e.g. /en/products/slug/
    # Split into at most 3 parts: ['', 'en', 'products/slug/']
    parts = path.split('/', 2)
    if len(parts) >= 2 and parts[1] in LANG_CODES:
        parts[1] = lang_code
        new_path = '/'.join(parts)
    else:
        new_path = f'/{lang_code}/{path.lstrip("/")}'
    return f"{context.get('site_url', '')}{new_path}"


@register.simple_tag(takes_context=True)
def organization_jsonld(context):
    """Return the site's single Organization JSON-LD object."""
    site = context.get('settings')
    origin = context.get('site_url', '')
    data = {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': getattr(site, 'site_name', 'VAAM Global'),
        'url': f'{origin}/',
        'logo': f"{origin}{static('images/logo/android-chrome-192x192.png')}",
    }
    if site:
        data['contactPoint'] = [{
            '@type': 'ContactPoint',
            'telephone': site.phone,
            'email': site.email,
            'contactType': 'customer service',
            'availableLanguage': ['English', 'Russian', 'Turkish', 'Arabic'],
        }]
        if site.address:
            data['address'] = {'@type': 'PostalAddress', 'addressLocality': site.address}
        profiles = (site.facebook, site.linkedin, site.instagram, site.tiktok, site.youtube, site.twitter)
        same_as = [url for url in profiles if url]
        if same_as:
            data['sameAs'] = same_as
    # '<' is escaped so stored text cannot close the surrounding <script> tag.
    return mark_safe(json.dumps(data, ensure_ascii=False).replace('<', '\\u003c'))
