import uuid

from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# ============ MENU SYSTEM ============
class Menu(models.Model):
    """A named menu group (e.g. Main Menu, Footer Menu)."""
    LOCATION_CHOICES = [
        ('main', 'Main Navigation'),
        ('footer', 'Footer'),
        ('topbar', 'Top Bar'),
        ('custom', 'Custom'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='main')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.get_location_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_root_items(self):
        return self.items.filter(parent__isnull=True, is_active=True)


class MenuItem(models.Model):
    """A single menu entry, supporting nested sub-menus via self-referencing FK."""
    LINK_TYPE_CHOICES = [
        ('url', 'Custom URL'),
        ('page', 'Page'),
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('products', 'Products'),
        ('projects', 'Projects'),
        ('news', 'News'),
        ('contact', 'Contact'),
    ]
    TARGET_CHOICES = [
        ('_self', 'Same Window'),
        ('_blank', 'New Window'),
    ]
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=200)
    link_type = models.CharField(max_length=20, choices=LINK_TYPE_CHOICES, default='url')
    url = models.CharField(max_length=500, blank=True, help_text='Used when link type is "Custom URL"')
    page = models.ForeignKey('Page', on_delete=models.SET_NULL, null=True, blank=True,
                             help_text='Used when link type is "Page"')
    icon = models.CharField(max_length=100, blank=True, help_text='CSS icon class e.g. fas fa-home')
    target = models.CharField(max_length=10, choices=TARGET_CHOICES, default='_self')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    css_class = models.CharField(max_length=200, blank=True, help_text='Extra CSS classes')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_url(self):
        if self.link_type == 'url':
            return self.url or '#'
        elif self.link_type == 'page' and self.page:
            return self.page.get_absolute_url()
        elif self.link_type in ('home', 'about', 'services', 'products', 'projects', 'news', 'contact'):
            from django.urls import reverse
            return reverse(f'core:{self.link_type}')
        return '#'

    def get_children(self):
        return self.children.filter(is_active=True)

    @property
    def has_children(self):
        return self.children.filter(is_active=True).exists()


# ============ PAGES ============
class Page(models.Model):
    """Dynamic CMS page with rich content."""
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(blank=True, help_text='Page HTML content')
    excerpt = models.TextField(blank=True, help_text='Short summary')
    image = models.ImageField(upload_to='pages/', blank=True, null=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    show_in_footer = models.BooleanField(default=False, help_text='Show link in footer')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:page_detail', kwargs={'slug': self.slug})


# ============ SITE SETTINGS ============
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='VAAM Import and Export Trading')
    site_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Main logo for header and light backgrounds')
    logo_white = models.ImageField(upload_to='site/', blank=True, null=True, help_text='White/light logo for dark backgrounds (footer etc.)')
    logo_admin = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Logo for admin panel sidebar and login page')
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Browser tab icon (recommended: 32x32 or 64x64 PNG)')
    phone = models.CharField(max_length=50, default='+994 50 123 45 67')
    phone2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(default='info@vaamtrading.com')
    email2 = models.EmailField(blank=True)
    address = models.CharField(max_length=300, default='Baku, Azerbaijan')
    address2 = models.CharField(max_length=300, blank=True)
    whatsapp = models.CharField(max_length=50, default='994501234567')
    working_hours = models.CharField(max_length=200, default='Mon-Fri 9:00-18:00')
    google_maps_embed = models.TextField(blank=True, help_text='Google Maps embed iframe URL')
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


# ============ HERO SLIDES ============
class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero/')
    button1_text = models.CharField(max_length=100, blank=True)
    button1_url = models.CharField(max_length=300, blank=True)
    button2_text = models.CharField(max_length=100, blank=True)
    button2_url = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# ============ ABOUT / COMPANY INFO ============
class CompanyInfo(models.Model):
    title = models.CharField(max_length=200, default='About VAAM')
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    values = models.TextField(blank=True)
    history = models.TextField(blank=True)
    year_established = models.PositiveIntegerField(default=2020, help_text='Year company was founded')
    number_of_employees = models.CharField(max_length=50, blank=True, help_text='e.g. 50-100')
    annual_revenue = models.CharField(max_length=200, blank=True, help_text='e.g. $10M+')
    headquarters = models.CharField(max_length=300, blank=True)
    branch_offices = models.TextField(blank=True, help_text='One office per line')
    registration_number = models.CharField(max_length=200, blank=True, help_text='Company registration/tax number')
    video_url = models.URLField(blank=True, help_text='Company introduction video (YouTube)')
    company_profile_pdf = models.FileField(upload_to='company/', blank=True, null=True)

    class Meta:
        verbose_name = 'Company Info'
        verbose_name_plural = 'Company Info'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class CompanyFeature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, help_text='Font Awesome class e.g. fas fa-check')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Statistic(models.Model):
    title = models.CharField(max_length=200)
    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=20, blank=True, help_text='e.g. +, %, K')
    icon = models.CharField(max_length=100, help_text='Font Awesome class')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.value}"


class Certificate(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='certificates/')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# ============ PRODUCT CATEGORIES & PRODUCTS ============
class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/categories/', blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Product Categories'
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    price = models.CharField(max_length=100, blank=True, help_text='Optional price display')
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    min_order_quantity = models.CharField(max_length=100, blank=True, help_text='e.g. 10 units')
    lead_time = models.CharField(max_length=100, blank=True, help_text='e.g. 15-30 days')
    origin_country = models.CharField(max_length=100, blank=True, default='China')
    warranty = models.CharField(max_length=200, blank=True, help_text='e.g. 2 years manufacturer warranty')
    datasheet = models.FileField(upload_to='products/datasheets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:product_detail', kwargs={'slug': self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.key}: {self.value}"


# ============ SERVICES ============
class ServiceCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Service Categories'
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text='Font Awesome class')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    features = models.TextField(blank=True, help_text='One feature per line')
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:services')


# ============ PROCESS STEPS ============
class ProcessStep(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order}: {self.title}"


# ============ PROJECTS ============
class ProjectCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Project Categories'
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/')
    client = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    date_completed = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:project_detail', kwargs={'slug': self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


# ============ NEWS ============
class NewsCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'News Categories'
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class News(models.Model):
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    title = models.CharField(max_length=400)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/')
    author = models.CharField(max_length=200, default='VAAM Team')
    reading_time = models.PositiveIntegerField(default=5, help_text='Minutes')
    is_published = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    published_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:news_detail', kwargs={'slug': self.slug})


# ============ FAQ ============
class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


# ============ TESTIMONIALS ============
class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    video_url = models.URLField(blank=True, help_text='YouTube/Vimeo testimonial video')
    company_logo = models.ImageField(upload_to='testimonials/logos/', blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True,
                                help_text='Related project for context')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.company}"


# ============ BRAND / PARTNER LOGOS ============
class Brand(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='brands/')
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# ============ CONTACT MESSAGES ============
class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


# ============ COUNTRIES (Served Markets) ============
class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, blank=True, help_text='ISO country code e.g. AZ, TR, RU')
    flag_icon = models.CharField(max_length=100, blank=True, help_text='Flag emoji or CSS class')
    image = models.ImageField(upload_to='countries/', blank=True, null=True, help_text='Country flag or representative image')
    description = models.TextField(blank=True, help_text='Short note about operations in this country')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


# ============ PRODUCT INQUIRY (Sourcing Request Form) ============
class ProductInquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Reviewing'),
        ('quoted', 'Quoted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    tracking_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    delivery_country = models.CharField(max_length=200, help_text='Country where product will be delivered')
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='inquiries', help_text='Product category of interest'
    )
    product_description = models.TextField(help_text='Detailed description of the product(s) needed')
    quantity = models.CharField(max_length=200, blank=True, help_text='Estimated quantity needed')
    budget_range = models.CharField(max_length=200, blank=True, help_text='Approximate budget range')
    additional_notes = models.TextField(blank=True, help_text='Any additional requirements or notes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)
    admin_response = models.TextField(blank=True, help_text='Response sent to the client')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.delivery_country} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = f"VAAM-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


# ============ ACCREDITATION / LICENSES ============
class Accreditation(models.Model):
    """Trade licenses, certifications, memberships, awards"""
    TYPES = [
        ('license', 'Business License'),
        ('certification', 'Certification'),
        ('membership', 'Membership'),
        ('award', 'Award'),
        ('insurance', 'Insurance'),
    ]
    title = models.CharField(max_length=300)
    type = models.CharField(max_length=20, choices=TYPES, default='certification')
    issuing_body = models.CharField(max_length=300, help_text='e.g. ISO, Chamber of Commerce')
    certificate_number = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='accreditations/', blank=True, null=True)
    description = models.TextField(blank=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, help_text='Verification URL')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


# ============ COMPANY DOCUMENTS ============
class CompanyDocument(models.Model):
    """Downloadable company profile, brochure, catalog"""
    TYPES = [
        ('profile', 'Company Profile'),
        ('catalog', 'Product Catalog'),
        ('brochure', 'Brochure'),
        ('certificate', 'Certificate'),
        ('report', 'Annual Report'),
    ]
    title = models.CharField(max_length=300)
    type = models.CharField(max_length=20, choices=TYPES, default='profile')
    file = models.FileField(upload_to='documents/')
    thumbnail = models.ImageField(upload_to='documents/thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True)
    download_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# ============ CASE STUDIES ============
class CaseStudy(models.Model):
    """Detailed project case study with results and metrics"""
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='case_study')
    challenge = models.TextField(help_text='What was the client challenge?')
    solution = models.TextField(help_text='How did VAAM solve it?')
    results = models.TextField(help_text='Measurable outcomes')
    delivery_time = models.CharField(max_length=100, blank=True, help_text='e.g. 45 days')
    total_value = models.CharField(max_length=100, blank=True, help_text='e.g. $250,000')
    products_sourced = models.PositiveIntegerField(default=0)
    client_testimonial = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Case Studies'

    def __str__(self):
        return f"Case Study: {self.project.title}"


# ============ CLIENT REFERENCES ============
class ClientReference(models.Model):
    """Client logos for trust display"""
    company_name = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='clients/')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.CharField(max_length=200, blank=True)
    testimonial = models.ForeignKey(Testimonial, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.company_name
