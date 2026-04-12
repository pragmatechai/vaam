from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, HeroSlide, CompanyInfo, CompanyFeature, Statistic,
    Certificate, TeamMember, ProductCategory, Product, ProductImage,
    ProductSpecification, ServiceCategory, Service, ProcessStep,
    ProjectCategory, Project, ProjectImage, NewsCategory, News,
    FAQ, Testimonial, Brand, ContactMessage,
    Menu, MenuItem, Page, Country, ProductInquiry,
    Accreditation, CompanyDocument, CaseStudy, ClientReference,
    GalleryCategory, GalleryItem
)


# ============ INLINE MODELS ============
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('title', 'link_type', 'url', 'page', 'parent', 'order', 'is_active')


# ============ ADMIN CLASSES ============
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {'fields': ('site_name', 'site_description', 'logo', 'logo_white', 'logo_admin', 'favicon')}),
        ('Contact', {'fields': ('phone', 'phone2', 'email', 'email2', 'address', 'address2', 'whatsapp', 'working_hours')}),
        ('Social Media', {'fields': ('facebook', 'linkedin', 'instagram', 'youtube', 'twitter')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
        ('Map', {'fields': ('google_maps_embed',)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order', 'is_active', 'image_preview')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not CompanyInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CompanyFeature)
class CompanyFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title',)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'suffix', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image_preview')
    list_editable = ('order',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active', 'photo_preview')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'position')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:50%;" />', obj.photo.url)
        return '-'
    photo_preview.short_description = 'Photo'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_featured', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active', 'is_featured', 'category')
    list_editable = ('order', 'is_active', 'is_featured')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSpecificationInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'order')
    list_filter = ('product',)


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value', 'order')
    list_filter = ('product',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active', 'category')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'is_featured', 'is_active', 'order')
    list_filter = ('is_active', 'is_featured', 'category')
    list_editable = ('order', 'is_active', 'is_featured')
    search_fields = ('title', 'client', 'location')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'alt_text', 'order')


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'is_featured', 'published_at')
    list_filter = ('is_published', 'is_featured', 'category')
    list_editable = ('is_published', 'is_featured')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'is_active', 'order')
    list_filter = ('is_active', 'rating')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'company', 'content')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'logo_preview')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:30px;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_active')
    list_filter = ('location', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'link_type', 'order', 'is_active')
    list_filter = ('menu', 'link_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_footer', 'order')
    list_filter = ('is_published', 'show_in_footer')
    list_editable = ('is_published', 'show_in_footer', 'order')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'flag_icon', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'code')


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'full_name', 'email', 'delivery_country', 'product_category', 'status', 'created_at')
    list_filter = ('status', 'product_category', 'created_at')
    list_editable = ('status',)
    search_fields = ('full_name', 'email', 'delivery_country', 'product_description', 'tracking_number')
    readonly_fields = ('tracking_number', 'full_name', 'email', 'phone', 'company_name', 'delivery_country',
                       'product_category', 'product_description', 'quantity', 'budget_range',
                       'additional_notes', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(Accreditation)
class AccreditationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'issuing_body', 'valid_until', 'order', 'is_active')
    list_filter = ('type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'issuing_body', 'certificate_number')


@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'download_count', 'order', 'is_active')
    list_filter = ('type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('project', 'delivery_time', 'total_value', 'products_sourced', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('project__title', 'challenge', 'solution', 'results')


@admin.register(ClientReference)
class ClientReferenceAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'country', 'industry', 'order', 'is_active', 'logo_preview')
    list_filter = ('is_active', 'country')
    list_editable = ('order', 'is_active')
    search_fields = ('company_name', 'industry')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:30px;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1
    fields = ('title', 'item_type', 'image', 'video_url', 'order', 'is_active')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'item_count')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'item_type', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active', 'item_type', 'category')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'