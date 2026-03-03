from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django import forms as django_forms

from core.models import (
    SiteSettings, HeroSlide, CompanyInfo, CompanyFeature, Statistic,
    Certificate, TeamMember, ProductCategory, Product, ProductImage,
    ProductSpecification, ServiceCategory, Service, ProcessStep,
    ProjectCategory, Project, ProjectImage, NewsCategory, News,
    FAQ, Testimonial, Brand, ContactMessage,
    Menu, MenuItem, Page,
    Country, ProductInquiry
)
from core.forms import (
    SiteSettingsForm, HeroSlideForm, CompanyInfoForm, CompanyFeatureForm,
    StatisticForm, CertificateForm, TeamMemberForm, ProductCategoryForm,
    ProductForm, ProductImageForm, ProductSpecificationForm,
    ServiceCategoryForm, ServiceForm, ProcessStepForm,
    ProjectCategoryForm, ProjectForm, ProjectImageForm,
    NewsCategoryForm, NewsForm, FAQForm, TestimonialForm, BrandForm,
    MenuForm, MenuItemForm, PageForm,
    CountryForm, ProductInquiryAdminForm
)


def _new_msg_count():
    return ContactMessage.objects.filter(status='new').count()


def _new_inquiry_count():
    return ProductInquiry.objects.filter(status='new').count()


# ============ AUTH ============
def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('dashboard:login')


# ============ DASHBOARD HOME ============
@login_required
def dashboard_home(request):
    stats = {
        'products': Product.objects.count(),
        'services': Service.objects.count(),
        'projects': Project.objects.count(),
        'messages': ContactMessage.objects.count(),
        'new_messages': ContactMessage.objects.filter(status='new').count(),
        'news': News.objects.count(),
        'slides': HeroSlide.objects.count(),
        'faqs': FAQ.objects.count(),
        'testimonials': Testimonial.objects.count(),
        'brands': Brand.objects.count(),
        'countries': Country.objects.count(),
        'inquiries': ProductInquiry.objects.count(),
        'new_inquiries': ProductInquiry.objects.filter(status='new').count(),
    }
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    recent_inquiries = ProductInquiry.objects.order_by('-created_at')[:5]
    context = {
        'stats': stats,
        'recent_messages': recent_messages,
        'recent_inquiries': recent_inquiries,
        'new_messages_count': stats['new_messages'],
    }
    return render(request, 'dashboard/home.html', context)


# ============ GENERIC CRUD HELPERS ============
def _list_view(request, model, template, title, create_url_name, search_fields=None, extra_context=None):
    items = model.objects.all()
    q = request.GET.get('q', '').strip()
    if q and search_fields:
        query = Q()
        for field in search_fields:
            query |= Q(**{f'{field}__icontains': q})
        items = items.filter(query)
    context = {
        'items': items,
        'title': title,
        'create_url': reverse(create_url_name),
        'search_query': q,
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    if extra_context:
        context.update(extra_context)
    return render(request, template, context)


def _create_view(request, form_class, template, title, list_url, parent_title=None):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'{title} created successfully.')
            return redirect(list_url)
    else:
        form = form_class()
    context = {
        'form': form,
        'title': f'Add {title}',
        'back_url': reverse(list_url) if ':' in list_url else list_url,
        'parent_title': parent_title or title + 's',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, template, context)


def _edit_view(request, model, form_class, template, title, list_url, pk, parent_title=None):
    item = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'{title} updated successfully.')
            return redirect(list_url)
    else:
        form = form_class(instance=item)
    context = {
        'form': form,
        'item': item,
        'title': f'Edit {title}',
        'back_url': reverse(list_url) if ':' in list_url else list_url,
        'parent_title': parent_title or title + 's',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, template, context)


def _delete_view(request, model, template, title, list_url, pk, parent_title=None):
    item = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{title} deleted successfully.')
        return redirect(list_url)
    context = {
        'item': item,
        'title': f'Delete {title}',
        'back_url': reverse(list_url) if ':' in list_url else list_url,
        'parent_title': parent_title or title + 's',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, template, context)


# ============ PRODUCTS ============
@login_required
def product_list(request):
    return _list_view(request, Product, 'dashboard/products/list.html', 'Products',
                      'dashboard:product_create', ['name', 'short_description', 'category__name'])

@login_required
def product_create(request):
    return _create_view(request, ProductForm, 'dashboard/products/form.html', 'Product',
                        'dashboard:product_list')

@login_required
def product_edit(request, pk):
    return _edit_view(request, Product, ProductForm, 'dashboard/products/form.html', 'Product',
                      'dashboard:product_list', pk)

@login_required
def product_delete(request, pk):
    return _delete_view(request, Product, 'dashboard/products/delete.html', 'Product',
                        'dashboard:product_list', pk)


# ============ PRODUCT CATEGORIES ============
@login_required
def product_category_list(request):
    return _list_view(request, ProductCategory, 'dashboard/categories/list.html', 'Product Categories',
                      'dashboard:product_category_create', ['name'],
                      extra_context={'edit_url_name': 'dashboard:product_category_edit',
                                     'delete_url_name': 'dashboard:product_category_delete'})

@login_required
def product_category_create(request):
    return _create_view(request, ProductCategoryForm, 'dashboard/categories/form.html', 'Product Category',
                        'dashboard:product_category_list', 'Product Categories')

@login_required
def product_category_edit(request, pk):
    return _edit_view(request, ProductCategory, ProductCategoryForm, 'dashboard/categories/form.html',
                      'Product Category', 'dashboard:product_category_list', pk, 'Product Categories')

@login_required
def product_category_delete(request, pk):
    return _delete_view(request, ProductCategory, 'dashboard/categories/delete.html', 'Product Category',
                        'dashboard:product_category_list', pk, 'Product Categories')


# ============ SERVICES ============
@login_required
def service_list(request):
    return _list_view(request, Service, 'dashboard/services/list.html', 'Services',
                      'dashboard:service_create', ['title', 'short_description'])

@login_required
def service_create(request):
    return _create_view(request, ServiceForm, 'dashboard/services/form.html', 'Service',
                        'dashboard:service_list')

@login_required
def service_edit(request, pk):
    return _edit_view(request, Service, ServiceForm, 'dashboard/services/form.html', 'Service',
                      'dashboard:service_list', pk)

@login_required
def service_delete(request, pk):
    return _delete_view(request, Service, 'dashboard/services/delete.html', 'Service',
                        'dashboard:service_list', pk)


# ============ SERVICE CATEGORIES ============
@login_required
def service_category_list(request):
    return _list_view(request, ServiceCategory, 'dashboard/categories/list.html', 'Service Categories',
                      'dashboard:service_category_create', ['name'],
                      extra_context={'edit_url_name': 'dashboard:service_category_edit',
                                     'delete_url_name': 'dashboard:service_category_delete'})

@login_required
def service_category_create(request):
    return _create_view(request, ServiceCategoryForm, 'dashboard/categories/form.html', 'Service Category',
                        'dashboard:service_category_list', 'Service Categories')

@login_required
def service_category_edit(request, pk):
    return _edit_view(request, ServiceCategory, ServiceCategoryForm, 'dashboard/categories/form.html',
                      'Service Category', 'dashboard:service_category_list', pk, 'Service Categories')

@login_required
def service_category_delete(request, pk):
    return _delete_view(request, ServiceCategory, 'dashboard/categories/delete.html', 'Service Category',
                        'dashboard:service_category_list', pk, 'Service Categories')


# ============ PROJECTS ============
@login_required
def project_list(request):
    return _list_view(request, Project, 'dashboard/projects/list.html', 'Projects',
                      'dashboard:project_create', ['title', 'short_description', 'client', 'location'])

@login_required
def project_create(request):
    return _create_view(request, ProjectForm, 'dashboard/projects/form.html', 'Project',
                        'dashboard:project_list')

@login_required
def project_edit(request, pk):
    return _edit_view(request, Project, ProjectForm, 'dashboard/projects/form.html', 'Project',
                      'dashboard:project_list', pk)

@login_required
def project_delete(request, pk):
    return _delete_view(request, Project, 'dashboard/projects/delete.html', 'Project',
                        'dashboard:project_list', pk)


# ============ PROJECT CATEGORIES ============
@login_required
def project_category_list(request):
    return _list_view(request, ProjectCategory, 'dashboard/categories/list.html', 'Project Categories',
                      'dashboard:project_category_create', ['name'],
                      extra_context={'edit_url_name': 'dashboard:project_category_edit',
                                     'delete_url_name': 'dashboard:project_category_delete'})

@login_required
def project_category_create(request):
    return _create_view(request, ProjectCategoryForm, 'dashboard/categories/form.html', 'Project Category',
                        'dashboard:project_category_list', 'Project Categories')

@login_required
def project_category_edit(request, pk):
    return _edit_view(request, ProjectCategory, ProjectCategoryForm, 'dashboard/categories/form.html',
                      'Project Category', 'dashboard:project_category_list', pk, 'Project Categories')

@login_required
def project_category_delete(request, pk):
    return _delete_view(request, ProjectCategory, 'dashboard/categories/delete.html', 'Project Category',
                        'dashboard:project_category_list', pk, 'Project Categories')


# ============ NEWS ============
@login_required
def news_list(request):
    return _list_view(request, News, 'dashboard/news/list.html', 'News',
                      'dashboard:news_create', ['title', 'summary', 'author'])

@login_required
def news_create(request):
    return _create_view(request, NewsForm, 'dashboard/news/form.html', 'News Article',
                        'dashboard:news_list', 'News')

@login_required
def news_edit(request, pk):
    return _edit_view(request, News, NewsForm, 'dashboard/news/form.html', 'News Article',
                      'dashboard:news_list', pk, 'News')

@login_required
def news_delete(request, pk):
    return _delete_view(request, News, 'dashboard/news/delete.html', 'News Article',
                        'dashboard:news_list', pk, 'News')


# ============ NEWS CATEGORIES ============
@login_required
def news_category_list(request):
    return _list_view(request, NewsCategory, 'dashboard/categories/list.html', 'News Categories',
                      'dashboard:news_category_create', ['name'],
                      extra_context={'edit_url_name': 'dashboard:news_category_edit',
                                     'delete_url_name': 'dashboard:news_category_delete'})

@login_required
def news_category_create(request):
    return _create_view(request, NewsCategoryForm, 'dashboard/categories/form.html', 'News Category',
                        'dashboard:news_category_list', 'News Categories')

@login_required
def news_category_edit(request, pk):
    return _edit_view(request, NewsCategory, NewsCategoryForm, 'dashboard/categories/form.html',
                      'News Category', 'dashboard:news_category_list', pk, 'News Categories')

@login_required
def news_category_delete(request, pk):
    return _delete_view(request, NewsCategory, 'dashboard/categories/delete.html', 'News Category',
                        'dashboard:news_category_list', pk, 'News Categories')


# ============ MESSAGES ============
@login_required
def message_list(request):
    items = ContactMessage.objects.all()
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    if q:
        items = items.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(email__icontains=q) | Q(subject__icontains=q)
        )
    if status_filter:
        items = items.filter(status=status_filter)
    context = {
        'items': items,
        'title': 'Messages',
        'search_query': q,
        'status_filter': status_filter,
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/messages/list.html', context)

@login_required
def message_detail(request, pk):
    item = get_object_or_404(ContactMessage, pk=pk)
    if item.status == 'new':
        item.status = 'read'
        item.save()
    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        if new_status in dict(ContactMessage.STATUS_CHOICES):
            item.status = new_status
            item.admin_notes = admin_notes
            item.save()
            messages.success(request, 'Message updated successfully.')
            return redirect('dashboard:message_detail', pk=pk)
    context = {
        'item': item,
        'title': 'Message Detail',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/messages/detail.html', context)

@login_required
def message_delete(request, pk):
    return _delete_view(request, ContactMessage, 'dashboard/messages/delete.html', 'Message',
                        'dashboard:message_list', pk)


# ============ HERO SLIDES ============
@login_required
def hero_slide_list(request):
    return _list_view(request, HeroSlide, 'dashboard/hero_slides/list.html', 'Hero Slides',
                      'dashboard:hero_slide_create', ['title', 'subtitle'])

@login_required
def hero_slide_create(request):
    return _create_view(request, HeroSlideForm, 'dashboard/hero_slides/form.html', 'Hero Slide',
                        'dashboard:hero_slide_list')

@login_required
def hero_slide_edit(request, pk):
    return _edit_view(request, HeroSlide, HeroSlideForm, 'dashboard/hero_slides/form.html', 'Hero Slide',
                      'dashboard:hero_slide_list', pk)

@login_required
def hero_slide_delete(request, pk):
    return _delete_view(request, HeroSlide, 'dashboard/hero_slides/delete.html', 'Hero Slide',
                        'dashboard:hero_slide_list', pk)


# ============ BRANDS ============
@login_required
def brand_list(request):
    return _list_view(request, Brand, 'dashboard/brands/list.html', 'Brands',
                      'dashboard:brand_create', ['name'])

@login_required
def brand_create(request):
    return _create_view(request, BrandForm, 'dashboard/brands/form.html', 'Brand',
                        'dashboard:brand_list')

@login_required
def brand_edit(request, pk):
    return _edit_view(request, Brand, BrandForm, 'dashboard/brands/form.html', 'Brand',
                      'dashboard:brand_list', pk)

@login_required
def brand_delete(request, pk):
    return _delete_view(request, Brand, 'dashboard/brands/delete.html', 'Brand',
                        'dashboard:brand_list', pk)


# ============ COMPANY INFO ============
@login_required
def company_info(request):
    try:
        obj = CompanyInfo.objects.get(pk=1)
    except CompanyInfo.DoesNotExist:
        obj = None
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company info updated successfully.')
            return redirect('dashboard:company_info')
    else:
        form = CompanyInfoForm(instance=obj)
    context = {
        'form': form,
        'title': 'Company Info',
        'back_url': '/dashboard/',
        'parent_title': 'Dashboard',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/settings/company_info.html', context)


# ============ COMPANY FEATURES ============
@login_required
def feature_list(request):
    return _list_view(request, CompanyFeature, 'dashboard/features/list.html', 'Company Features',
                      'dashboard:feature_create', ['title', 'description'])

@login_required
def feature_create(request):
    return _create_view(request, CompanyFeatureForm, 'dashboard/features/form.html', 'Feature',
                        'dashboard:feature_list', 'Company Features')

@login_required
def feature_edit(request, pk):
    return _edit_view(request, CompanyFeature, CompanyFeatureForm, 'dashboard/features/form.html',
                      'Feature', 'dashboard:feature_list', pk, 'Company Features')

@login_required
def feature_delete(request, pk):
    return _delete_view(request, CompanyFeature, 'dashboard/features/delete.html', 'Feature',
                        'dashboard:feature_list', pk, 'Company Features')


# ============ STATISTICS ============
@login_required
def statistic_list(request):
    return _list_view(request, Statistic, 'dashboard/statistics/list.html', 'Statistics',
                      'dashboard:statistic_create', ['title'])

@login_required
def statistic_create(request):
    return _create_view(request, StatisticForm, 'dashboard/statistics/form.html', 'Statistic',
                        'dashboard:statistic_list')

@login_required
def statistic_edit(request, pk):
    return _edit_view(request, Statistic, StatisticForm, 'dashboard/statistics/form.html',
                      'Statistic', 'dashboard:statistic_list', pk)

@login_required
def statistic_delete(request, pk):
    return _delete_view(request, Statistic, 'dashboard/statistics/delete.html', 'Statistic',
                        'dashboard:statistic_list', pk)


# ============ PROCESS STEPS ============
@login_required
def process_step_list(request):
    return _list_view(request, ProcessStep, 'dashboard/process_steps/list.html', 'Process Steps',
                      'dashboard:process_step_create', ['title', 'description'])

@login_required
def process_step_create(request):
    return _create_view(request, ProcessStepForm, 'dashboard/process_steps/form.html', 'Process Step',
                        'dashboard:process_step_list')

@login_required
def process_step_edit(request, pk):
    return _edit_view(request, ProcessStep, ProcessStepForm, 'dashboard/process_steps/form.html',
                      'Process Step', 'dashboard:process_step_list', pk)

@login_required
def process_step_delete(request, pk):
    return _delete_view(request, ProcessStep, 'dashboard/process_steps/delete.html', 'Process Step',
                        'dashboard:process_step_list', pk)


# ============ SITE SETTINGS ============
@login_required
def site_settings(request):
    settings_obj = SiteSettings.get_settings()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('dashboard:site_settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)
    context = {
        'form': form,
        'title': 'Site Settings',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/settings/form.html', context)


# ============ FAQs ============
@login_required
def faq_list(request):
    return _list_view(request, FAQ, 'dashboard/faqs/list.html', 'FAQs',
                      'dashboard:faq_create', ['question', 'answer'])

@login_required
def faq_create(request):
    return _create_view(request, FAQForm, 'dashboard/faqs/form.html', 'FAQ',
                        'dashboard:faq_list')

@login_required
def faq_edit(request, pk):
    return _edit_view(request, FAQ, FAQForm, 'dashboard/faqs/form.html', 'FAQ',
                      'dashboard:faq_list', pk)

@login_required
def faq_delete(request, pk):
    return _delete_view(request, FAQ, 'dashboard/faqs/delete.html', 'FAQ',
                        'dashboard:faq_list', pk)


# ============ TESTIMONIALS ============
@login_required
def testimonial_list(request):
    return _list_view(request, Testimonial, 'dashboard/testimonials/list.html', 'Testimonials',
                      'dashboard:testimonial_create', ['name', 'company', 'content'])

@login_required
def testimonial_create(request):
    return _create_view(request, TestimonialForm, 'dashboard/testimonials/form.html', 'Testimonial',
                        'dashboard:testimonial_list')

@login_required
def testimonial_edit(request, pk):
    return _edit_view(request, Testimonial, TestimonialForm, 'dashboard/testimonials/form.html', 'Testimonial',
                      'dashboard:testimonial_list', pk)

@login_required
def testimonial_delete(request, pk):
    return _delete_view(request, Testimonial, 'dashboard/testimonials/delete.html', 'Testimonial',
                        'dashboard:testimonial_list', pk)


# ============ MENUS ============
@login_required
def menu_list(request):
    return _list_view(request, Menu, 'dashboard/menus/list.html', 'Menus',
                      'dashboard:menu_create', ['title', 'location'])

@login_required
def menu_create(request):
    return _create_view(request, MenuForm, 'dashboard/menus/form.html', 'Menu',
                        'dashboard:menu_list')

@login_required
def menu_edit(request, pk):
    return _edit_view(request, Menu, MenuForm, 'dashboard/menus/form.html', 'Menu',
                      'dashboard:menu_list', pk)

@login_required
def menu_delete(request, pk):
    return _delete_view(request, Menu, 'dashboard/menus/delete.html', 'Menu',
                        'dashboard:menu_list', pk)


# ============ MENU ITEMS ============
@login_required
def menu_item_list(request, menu_pk):
    menu_obj = get_object_or_404(Menu, pk=menu_pk)
    items = MenuItem.objects.filter(menu=menu_obj).select_related('parent', 'page')
    q = request.GET.get('q', '').strip()
    if q:
        items = items.filter(Q(title__icontains=q))
    context = {
        'items': items,
        'menu_obj': menu_obj,
        'title': f'Menu Items – {menu_obj.title}',
        'create_url': reverse('dashboard:menu_item_create', args=[menu_pk]),
        'search_query': q,
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/menus/item_list.html', context)

@login_required
def menu_item_create(request, menu_pk):
    menu_obj = get_object_or_404(Menu, pk=menu_pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.menu = menu_obj
            item.save()
            messages.success(request, 'Menu item created successfully.')
            return redirect('dashboard:menu_item_list', menu_pk=menu_pk)
    else:
        form = MenuItemForm(initial={'menu': menu_obj})
    # Limit parent choices to items in same menu
    form.fields['parent'].queryset = MenuItem.objects.filter(menu=menu_obj)
    form.fields['menu'].initial = menu_obj
    form.fields['menu'].widget = django_forms.HiddenInput()
    context = {
        'form': form,
        'menu_obj': menu_obj,
        'title': f'Add Menu Item – {menu_obj.title}',
        'back_url': reverse('dashboard:menu_item_list', args=[menu_pk]),
        'parent_title': f'Menu Items – {menu_obj.title}',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/menus/item_form.html', context)

@login_required
def menu_item_edit(request, menu_pk, pk):
    menu_obj = get_object_or_404(Menu, pk=menu_pk)
    item = get_object_or_404(MenuItem, pk=pk, menu=menu_obj)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully.')
            return redirect('dashboard:menu_item_list', menu_pk=menu_pk)
    else:
        form = MenuItemForm(instance=item)
    form.fields['parent'].queryset = MenuItem.objects.filter(menu=menu_obj).exclude(pk=pk)
    form.fields['menu'].widget = django_forms.HiddenInput()
    context = {
        'form': form,
        'item': item,
        'menu_obj': menu_obj,
        'title': f'Edit Menu Item – {item.title}',
        'back_url': reverse('dashboard:menu_item_list', args=[menu_pk]),
        'parent_title': f'Menu Items – {menu_obj.title}',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/menus/item_form.html', context)

@login_required
def menu_item_delete(request, menu_pk, pk):
    menu_obj = get_object_or_404(Menu, pk=menu_pk)
    item = get_object_or_404(MenuItem, pk=pk, menu=menu_obj)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item deleted successfully.')
        return redirect('dashboard:menu_item_list', menu_pk=menu_pk)
    context = {
        'item': item,
        'menu_obj': menu_obj,
        'title': f'Delete Menu Item',
        'back_url': reverse('dashboard:menu_item_list', args=[menu_pk]),
        'parent_title': f'Menu Items – {menu_obj.title}',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/menus/item_delete.html', context)


# ============ PAGES ============
@login_required
def page_list(request):
    return _list_view(request, Page, 'dashboard/pages/list.html', 'Pages',
                      'dashboard:page_create', ['title', 'slug', 'content'])

@login_required
def page_create(request):
    return _create_view(request, PageForm, 'dashboard/pages/form.html', 'Page',
                        'dashboard:page_list')

@login_required
def page_edit(request, pk):
    return _edit_view(request, Page, PageForm, 'dashboard/pages/form.html', 'Page',
                      'dashboard:page_list', pk)

@login_required
def page_delete(request, pk):
    return _delete_view(request, Page, 'dashboard/pages/delete.html', 'Page',
                        'dashboard:page_list', pk)


# ============ COUNTRIES ============
@login_required
def country_list(request):
    return _list_view(request, Country, 'dashboard/countries/list.html', 'Countries',
                      'dashboard:country_create', ['name', 'code', 'description'])

@login_required
def country_create(request):
    return _create_view(request, CountryForm, 'dashboard/countries/form.html', 'Country',
                        'dashboard:country_list', parent_title='Countries')

@login_required
def country_edit(request, pk):
    return _edit_view(request, Country, CountryForm, 'dashboard/countries/form.html', 'Country',
                      'dashboard:country_list', pk, parent_title='Countries')

@login_required
def country_delete(request, pk):
    return _delete_view(request, Country, 'dashboard/countries/delete.html', 'Country',
                        'dashboard:country_list', pk, parent_title='Countries')


# ============ PRODUCT INQUIRIES ============
@login_required
def inquiry_list(request):
    items = ProductInquiry.objects.all()
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    if q:
        items = items.filter(
            Q(full_name__icontains=q) | Q(email__icontains=q) |
            Q(company_name__icontains=q) | Q(delivery_country__icontains=q) |
            Q(product_description__icontains=q)
        )
    if status_filter:
        items = items.filter(status=status_filter)
    context = {
        'items': items,
        'title': 'Product Inquiries',
        'search_query': q,
        'status_filter': status_filter,
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/inquiries/list.html', context)

@login_required
def inquiry_detail(request, pk):
    item = get_object_or_404(ProductInquiry, pk=pk)
    if item.status == 'new':
        item.status = 'reviewing'
        item.save()
    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        if new_status in dict(ProductInquiry.STATUS_CHOICES):
            item.status = new_status
            item.admin_notes = admin_notes
            item.save()
            messages.success(request, 'Inquiry updated successfully.')
            return redirect('dashboard:inquiry_detail', pk=pk)
    context = {
        'item': item,
        'title': 'Inquiry Detail',
        'new_messages_count': _new_msg_count(),
        'new_inquiries_count': _new_inquiry_count(),
    }
    return render(request, 'dashboard/inquiries/detail.html', context)

@login_required
def inquiry_delete(request, pk):
    return _delete_view(request, ProductInquiry, 'dashboard/inquiries/delete.html', 'Inquiry',
                        'dashboard:inquiry_list', pk, parent_title='Product Inquiries')
