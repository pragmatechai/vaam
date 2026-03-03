import json
import logging
import threading

from django.conf import settings as django_settings
from django.core.mail import mail_managers
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import (
    SiteSettings, HeroSlide, CompanyInfo, CompanyFeature, Statistic,
    Certificate, TeamMember, ProductCategory, Product,
    ServiceCategory, Service, ProcessStep,
    ProjectCategory, Project, NewsCategory, News,
    FAQ, Testimonial, Brand, ContactMessage, Page,
    Country, ProductInquiry
)
from .forms import ContactMessageForm, ProductInquiryForm

logger = logging.getLogger('core')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _send_mail_async(subject, message):
    """Send a mail_managers notification in a background thread so the view
    returns immediately without waiting for SMTP."""
    def _send():
        try:
            mail_managers(subject=subject, message=message, fail_silently=True)
        except Exception:
            logger.exception('Background email send failed')
    t = threading.Thread(target=_send, daemon=True)
    t.start()

def _get_company_info():
    """Return the singleton CompanyInfo or None. Avoids repeated try/except."""
    return CompanyInfo.objects.filter(pk=1).first()


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def home(request):
    slides = HeroSlide.objects.filter(is_active=True)
    slides_json = json.dumps([
        {
            'img': slide.image.url if slide.image else '',
            'sub': slide.subtitle or '',
            'title': slide.title,
            'text': slide.description or '',
            'b1': {'t': slide.button1_text or 'Learn More', 'h': slide.button1_url or reverse('core:products')},
            'b2': {'t': slide.button2_text or 'Contact Us', 'h': slide.button2_url or reverse('core:contact')},
        }
        for slide in slides
    ])

    # Build home_projects: featured first, fill with recent if needed
    featured_ids = list(
        Project.objects.filter(is_active=True, is_featured=True).values_list('id', flat=True)[:6]
    )
    home_projects = list(
        Project.objects.filter(is_active=True, is_featured=True).select_related('category')[:6]
    )
    if len(home_projects) < 3:
        extra = list(
            Project.objects.filter(is_active=True)
            .exclude(id__in=featured_ids)
            .select_related('category')
            .order_by('-created_at')[:6 - len(home_projects)]
        )
        home_projects = home_projects + extra

    context = {
        'active_page': 'home',
        'slides': slides,
        'slides_json': slides_json,
        'company_info': _get_company_info(),
        'features': CompanyFeature.objects.filter(is_active=True)[:4],
        'services': Service.objects.filter(is_active=True)[:3],
        'process_steps': ProcessStep.objects.filter(is_active=True)[:4],
        'statistics': Statistic.objects.filter(is_active=True)[:4],
        'home_projects': home_projects,
        'featured_products_list': Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:6],
        'latest_news': News.objects.filter(is_published=True).select_related('category')[:3],
        'testimonials': Testimonial.objects.filter(is_active=True)[:4],
        'brands': Brand.objects.filter(is_active=True),
        'countries': Country.objects.filter(is_active=True),
        'product_categories': ProductCategory.objects.filter(is_active=True),
        'inquiry_form': ProductInquiryForm(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'active_page': 'about',
        'company_info': _get_company_info(),
        'features': CompanyFeature.objects.filter(is_active=True),
        'statistics': Statistic.objects.filter(is_active=True),
        'certificates': Certificate.objects.all(),
        'team_members': TeamMember.objects.filter(is_active=True),
        'brands': Brand.objects.filter(is_active=True),
    }
    return render(request, 'core/about.html', context)


def services(request):
    context = {
        'active_page': 'services',
        'services': Service.objects.filter(is_active=True).select_related('category'),
        'process_steps': ProcessStep.objects.filter(is_active=True),
        'faqs': FAQ.objects.filter(is_active=True),
    }
    return render(request, 'core/services.html', context)


def products(request):
    categories = ProductCategory.objects.filter(is_active=True)
    active_category = request.GET.get('category', '')
    product_list = Product.objects.filter(is_active=True).select_related('category')
    if active_category:
        product_list = product_list.filter(category__slug=active_category)

    paginator = Paginator(product_list, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'active_page': 'products',
        'categories': categories,
        'products': page_obj,
        'active_category': active_category,
        'page_obj': page_obj,
    }
    return render(request, 'core/products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images', 'specifications'),
        slug=slug, is_active=True
    )
    related_products = (
        Product.objects
        .filter(category=product.category, is_active=True)
        .exclude(pk=product.pk)
        .select_related('category')
        .only('slug', 'name', 'short_description', 'image', 'category')
    )[:3]

    _saved_data = request.session.pop('inquiry_form_data', None)
    _saved_errors = request.session.pop('inquiry_form_errors', None)
    context = {
        'active_page': 'products',
        'product': product,
        'related_products': related_products,
        # Restore saved form data when redirected back after validation error
        'inquiry_saved_data': json.dumps(_saved_data) if _saved_data else '',
        'inquiry_saved_errors': json.dumps(_saved_errors) if _saved_errors else '{}',
    }
    return render(request, 'core/product_detail.html', context)


def projects(request):
    categories = ProjectCategory.objects.filter(is_active=True)
    active_category = request.GET.get('category', '')
    project_list = Project.objects.filter(is_active=True).select_related('category')
    if active_category:
        project_list = project_list.filter(category__slug=active_category)

    paginator = Paginator(project_list, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'active_page': 'projects',
        'categories': categories,
        'projects': page_obj,
        'active_category': active_category,
        'page_obj': page_obj,
    }
    return render(request, 'core/projects.html', context)


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related('images'),
        slug=slug, is_active=True
    )
    related_projects = Project.objects.filter(
        is_active=True, category=project.category
    ).exclude(pk=project.pk).select_related('category')[:3]

    context = {
        'active_page': 'projects',
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'core/project_detail.html', context)


def news_list(request):
    categories = NewsCategory.objects.filter(is_active=True)
    active_category = request.GET.get('category', '')
    articles = News.objects.filter(is_published=True).select_related('category')
    if active_category:
        articles = articles.filter(category__slug=active_category)

    paginator = Paginator(articles, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'active_page': 'news',
        'articles': page_obj,
        'categories': categories,
        'active_category': active_category,
        'page_obj': page_obj,
    }
    return render(request, 'core/news.html', context)


def news_detail(request, slug):
    article = get_object_or_404(
        News.objects.select_related('category'),
        slug=slug, is_published=True
    )
    related_articles = News.objects.filter(
        is_published=True
    ).exclude(pk=article.pk).select_related('category').only(
        'slug', 'title', 'summary', 'image', 'published_at', 'category'
    )[:3]

    context = {
        'active_page': 'news',
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'core/news_detail.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            obj = form.save()
            # Notify site managers via email
            _send_mail_async(
                    subject=f'New Contact Message: {obj.subject}',
                    message=(
                        f'Name: {obj.full_name}\n'
                        f'Email: {obj.email}\n'
                        f'Phone: {obj.phone}\n\n'
                        f'{obj.message}'
                    ),
                )
            messages.success(request, _('Your message has been sent successfully! We will get back to you soon.'))
            return redirect('core:contact')
    else:
        form = ContactMessageForm()

    context = {
        'active_page': 'contact',
        'form': form,
        'testimonials': Testimonial.objects.filter(is_active=True),
        'faqs': FAQ.objects.filter(is_active=True),
    }
    return render(request, 'core/contact.html', context)


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    context = {
        'active_page': f'page_{page.slug}',
        'page': page,
    }
    return render(request, 'core/page_detail.html', context)


def product_inquiry(request):
    """Handle product sourcing inquiry form submission."""
    if request.method == 'POST':
        form = ProductInquiryForm(request.POST)
        next_url = request.POST.get('next', '').strip()
        product_name = request.POST.get('product_name', '').strip()

        if form.is_valid():
            obj = form.save()
            # Notify site managers
            _send_mail_async(
                    subject=f'New Product Inquiry: {product_name or obj.delivery_country}',
                    message=(
                        f'Product: {product_name or obj.product_description[:80]}\n'
                        f'Name: {obj.full_name}\n'
                        f'Email: {obj.email}\n'
                        f'Phone: {obj.phone}\n'
                        f'Company: {obj.company_name}\n'
                        f'Delivery Country: {obj.delivery_country}\n'
                        f'Quantity: {obj.quantity}\n'
                        f'Budget: {obj.budget_range}\n\n'
                        f'Description:\n{obj.product_description}\n\n'
                        f'Notes:\n{obj.additional_notes}'
                    ),
                )
            messages.success(request, _('Your product inquiry has been submitted successfully! Our team will review your request and contact you shortly.'))
            # Redirect back to referring product page if safe
            if next_url:
                from django.utils.http import url_has_allowed_host_and_scheme
                if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(f'{next_url}?inquiry_sent=1#inquiry-section')
            # For standalone inquiry page: redirect back to the same page with ?sent=1
            return redirect(reverse('core:product_inquiry') + '?sent=1')
        else:
            messages.error(request, _('Please correct the errors below. Make sure all required fields are filled in.'))
            # Redirect back to product page if available
            if next_url:
                from django.utils.http import url_has_allowed_host_and_scheme
                if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    # Persist form data + errors in session so inline form can be re-filled
                    request.session['inquiry_form_data'] = {
                        k: v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken'
                    }
                    request.session['inquiry_form_errors'] = {
                        field: list(errs) for field, errs in form.errors.items()
                    }
                    return redirect(f'{next_url}?inquiry_error=1#inquiry-section')
    else:
        form = ProductInquiryForm()

    context = {
        'active_page': 'inquiry',
        'form': form,
        'product_categories': ProductCategory.objects.filter(is_active=True),
    }
    return render(request, 'core/product_inquiry.html', context)
