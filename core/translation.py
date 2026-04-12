"""
Model translation registration for django-modeltranslation.
Each model's translatable text fields are registered here.
Creates _en, _ru, _tr, _ar columns for each registered field.
"""
from modeltranslation.translator import translator, TranslationOptions

from .models import (
    SiteSettings, HeroSlide, CompanyInfo, CompanyFeature, Statistic,
    Certificate, TeamMember, ProductCategory, Product, ProductImage,
    ProductSpecification, ServiceCategory, Service, ProcessStep,
    ProjectCategory, Project, NewsCategory, News,
    FAQ, Testimonial, Brand, ContactMessage,
    Menu, MenuItem, Page, Country, ProductInquiry,
    Accreditation, CompanyDocument, CaseStudy, ClientReference,
    GalleryCategory, GalleryItem
)


class SiteSettingsTranslation(TranslationOptions):
    fields = ('site_name', 'site_description', 'address', 'address2',
              'working_hours', 'meta_title', 'meta_description', 'meta_keywords')


class HeroSlideTranslation(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'button1_text', 'button2_text')


class CompanyInfoTranslation(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'mission', 'vision', 'values', 'history',
              'headquarters', 'branch_offices')


class CompanyFeatureTranslation(TranslationOptions):
    fields = ('title', 'description')


class StatisticTranslation(TranslationOptions):
    fields = ('title',)


class CertificateTranslation(TranslationOptions):
    fields = ('title', 'description')


class TeamMemberTranslation(TranslationOptions):
    fields = ('name', 'position', 'bio')


class ProductCategoryTranslation(TranslationOptions):
    fields = ('name', 'description')


class ProductTranslation(TranslationOptions):
    fields = ('name', 'short_description', 'description', 'meta_title', 'meta_description',
              'min_order_quantity', 'lead_time', 'warranty')


class ProductImageTranslation(TranslationOptions):
    fields = ('alt_text',)


class ProductSpecificationTranslation(TranslationOptions):
    fields = ('key', 'value')


class ServiceCategoryTranslation(TranslationOptions):
    fields = ('name',)


class ServiceTranslation(TranslationOptions):
    fields = ('title', 'short_description', 'description', 'features')


class ProcessStepTranslation(TranslationOptions):
    fields = ('title', 'description')


class ProjectCategoryTranslation(TranslationOptions):
    fields = ('name',)


class ProjectTranslation(TranslationOptions):
    fields = ('title', 'short_description', 'description', 'client', 'location')


class NewsCategoryTranslation(TranslationOptions):
    fields = ('name',)


class NewsTranslation(TranslationOptions):
    fields = ('title', 'summary', 'content', 'author', 'meta_title', 'meta_description')


class FAQTranslation(TranslationOptions):
    fields = ('question', 'answer')


class TestimonialTranslation(TranslationOptions):
    fields = ('name', 'position', 'company', 'content')


class BrandTranslation(TranslationOptions):
    fields = ('name',)


class CountryTranslation(TranslationOptions):
    fields = ('name', 'description')


class ProductInquiryTranslation(TranslationOptions):
    fields = ()


class MenuTranslation(TranslationOptions):
    fields = ('title',)


class MenuItemTranslation(TranslationOptions):
    fields = ('title',)


class PageTranslation(TranslationOptions):
    fields = ('title', 'content', 'excerpt', 'meta_title', 'meta_description')


class AccreditationTranslation(TranslationOptions):
    fields = ('title', 'issuing_body', 'description')


class CompanyDocumentTranslation(TranslationOptions):
    fields = ('title', 'description')


class CaseStudyTranslation(TranslationOptions):
    fields = ('challenge', 'solution', 'results', 'client_testimonial')


class ClientReferenceTranslation(TranslationOptions):
    fields = ('company_name', 'industry')


# Register all translations
translator.register(SiteSettings, SiteSettingsTranslation)
translator.register(HeroSlide, HeroSlideTranslation)
translator.register(CompanyInfo, CompanyInfoTranslation)
translator.register(CompanyFeature, CompanyFeatureTranslation)
translator.register(Statistic, StatisticTranslation)
translator.register(Certificate, CertificateTranslation)
translator.register(TeamMember, TeamMemberTranslation)
translator.register(ProductCategory, ProductCategoryTranslation)
translator.register(Product, ProductTranslation)
translator.register(ProductImage, ProductImageTranslation)
translator.register(ProductSpecification, ProductSpecificationTranslation)
translator.register(ServiceCategory, ServiceCategoryTranslation)
translator.register(Service, ServiceTranslation)
translator.register(ProcessStep, ProcessStepTranslation)
translator.register(ProjectCategory, ProjectCategoryTranslation)
translator.register(Project, ProjectTranslation)
translator.register(NewsCategory, NewsCategoryTranslation)
translator.register(News, NewsTranslation)
translator.register(FAQ, FAQTranslation)
translator.register(Testimonial, TestimonialTranslation)
translator.register(Brand, BrandTranslation)
translator.register(Country, CountryTranslation)
translator.register(ProductInquiry, ProductInquiryTranslation)
translator.register(Menu, MenuTranslation)
translator.register(MenuItem, MenuItemTranslation)
translator.register(Page, PageTranslation)
translator.register(Accreditation, AccreditationTranslation)
translator.register(CompanyDocument, CompanyDocumentTranslation)
translator.register(CaseStudy, CaseStudyTranslation)
translator.register(ClientReference, ClientReferenceTranslation)


class GalleryCategoryTranslation(TranslationOptions):
    fields = ('name', 'description')


class GalleryItemTranslation(TranslationOptions):
    fields = ('title', 'description')


translator.register(GalleryCategory, GalleryCategoryTranslation)
translator.register(GalleryItem, GalleryItemTranslation)
