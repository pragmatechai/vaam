from django import forms
from django.conf import settings
from .models import (
    SiteSettings, HeroSlide, CompanyInfo, CompanyFeature, Statistic,
    Certificate, TeamMember, ProductCategory, Product, ProductImage,
    ProductSpecification, ServiceCategory, Service, ProcessStep,
    ProjectCategory, Project, ProjectImage, NewsCategory, News,
    FAQ, Testimonial, Brand, ContactMessage,
    Menu, MenuItem, Page, Country, ProductInquiry
)

# Reusable Tailwind widget class
TW_INPUT = 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 outline-none transition text-sm'
TW_SELECT = 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 outline-none transition text-sm bg-white'
TW_TEXTAREA = 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 outline-none transition text-sm'
TW_CHECKBOX = 'w-4 h-4 text-primary-600 border-slate-300 rounded focus:ring-primary-500'
TW_FILE = 'w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-medium file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100 cursor-pointer'

LANG_CODES = [code for code, _ in settings.LANGUAGES]
LANG_SUFFIXES = tuple(f'_{code}' for code in LANG_CODES)


def _get_translatable_field_names(model_class):
    """Get the original (proxy) field names that have translations."""
    try:
        from modeltranslation.translator import translator
        opts = translator.get_options_for_model(model_class)
        # opts.fields is a tuple of field names, not a dict
        return set(opts.fields)
    except Exception:
        return set()


def tw_widgets(model_class):
    """Generate Tailwind-styled widgets for all model fields including translation fields."""
    widgets = {}
    for field in model_class._meta.get_fields():
        if not hasattr(field, 'formfield') or field.formfield() is None:
            continue
        ff = field.formfield()
        if isinstance(ff.widget, forms.Textarea):
            widgets[field.name] = forms.Textarea(attrs={'class': TW_TEXTAREA, 'rows': 4})
        elif isinstance(ff.widget, forms.Select):
            widgets[field.name] = forms.Select(attrs={'class': TW_SELECT})
        elif isinstance(ff.widget, forms.CheckboxInput):
            widgets[field.name] = forms.CheckboxInput(attrs={'class': TW_CHECKBOX})
        elif isinstance(ff.widget, forms.FileInput):
            widgets[field.name] = forms.ClearableFileInput(attrs={'class': TW_FILE})
        elif isinstance(ff.widget, (forms.NumberInput,)):
            widgets[field.name] = forms.NumberInput(attrs={'class': TW_INPUT})
        elif isinstance(ff.widget, forms.DateInput):
            widgets[field.name] = forms.DateInput(attrs={'class': TW_INPUT, 'type': 'date'})
        elif isinstance(ff.widget, forms.DateTimeInput):
            widgets[field.name] = forms.DateTimeInput(attrs={'class': TW_INPUT, 'type': 'datetime-local'})
        elif isinstance(ff.widget, forms.EmailInput):
            widgets[field.name] = forms.EmailInput(attrs={'class': TW_INPUT})
        elif isinstance(ff.widget, forms.URLInput):
            widgets[field.name] = forms.URLInput(attrs={'class': TW_INPUT})
        else:
            widgets[field.name] = forms.TextInput(attrs={'class': TW_INPUT})
    return widgets


class TranslatedModelForm(forms.ModelForm):
    """Base form that hides proxy fields and keeps only _lang fields for translated models."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        proxy_fields = _get_translatable_field_names(self._meta.model)
        for field_name in list(proxy_fields):
            if field_name in self.fields:
                del self.fields[field_name]
        # Apply TW styling to any fields that may not have widgets set
        for name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                if isinstance(field.widget, forms.Textarea):
                    field.widget.attrs['class'] = TW_TEXTAREA
                    field.widget.attrs.setdefault('rows', 4)
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = TW_SELECT
                elif isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = TW_CHECKBOX
                elif isinstance(field.widget, forms.ClearableFileInput):
                    field.widget.attrs['class'] = TW_FILE
                else:
                    field.widget.attrs['class'] = TW_INPUT


class SiteSettingsForm(TranslatedModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = tw_widgets(SiteSettings)


class HeroSlideForm(TranslatedModelForm):
    class Meta:
        model = HeroSlide
        fields = '__all__'
        widgets = tw_widgets(HeroSlide)


class CompanyInfoForm(TranslatedModelForm):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
        widgets = tw_widgets(CompanyInfo)


class CompanyFeatureForm(TranslatedModelForm):
    class Meta:
        model = CompanyFeature
        fields = '__all__'
        widgets = tw_widgets(CompanyFeature)


class StatisticForm(TranslatedModelForm):
    class Meta:
        model = Statistic
        fields = '__all__'
        widgets = tw_widgets(Statistic)


class CertificateForm(TranslatedModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
        widgets = tw_widgets(Certificate)


class TeamMemberForm(TranslatedModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'
        widgets = tw_widgets(TeamMember)


class ProductCategoryForm(TranslatedModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        widgets = tw_widgets(ProductCategory)


class ProductForm(TranslatedModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = tw_widgets(Product)


class ProductImageForm(TranslatedModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'
        widgets = tw_widgets(ProductImage)


class ProductSpecificationForm(TranslatedModelForm):
    class Meta:
        model = ProductSpecification
        fields = '__all__'
        widgets = tw_widgets(ProductSpecification)


class ServiceCategoryForm(TranslatedModelForm):
    class Meta:
        model = ServiceCategory
        fields = '__all__'
        widgets = tw_widgets(ServiceCategory)


class ServiceForm(TranslatedModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = tw_widgets(Service)


class ProcessStepForm(TranslatedModelForm):
    class Meta:
        model = ProcessStep
        fields = '__all__'
        widgets = tw_widgets(ProcessStep)


class ProjectCategoryForm(TranslatedModelForm):
    class Meta:
        model = ProjectCategory
        fields = '__all__'
        widgets = tw_widgets(ProjectCategory)


class ProjectForm(TranslatedModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = tw_widgets(Project)


class ProjectImageForm(TranslatedModelForm):
    class Meta:
        model = ProjectImage
        fields = '__all__'
        widgets = tw_widgets(ProjectImage)


class NewsCategoryForm(TranslatedModelForm):
    class Meta:
        model = NewsCategory
        fields = '__all__'
        widgets = tw_widgets(NewsCategory)


class NewsForm(TranslatedModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = tw_widgets(News)


class FAQForm(TranslatedModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = tw_widgets(FAQ)


class TestimonialForm(TranslatedModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'
        widgets = tw_widgets(Testimonial)


class BrandForm(TranslatedModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        widgets = tw_widgets(Brand)


class MenuForm(TranslatedModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = tw_widgets(Menu)


class MenuItemForm(TranslatedModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
        widgets = tw_widgets(MenuItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show page titles in the dropdown
        if 'page' in self.fields:
            self.fields['page'].queryset = Page.objects.filter(is_published=True)
            self.fields['page'].required = False
        # Show parent items nicely
        if 'parent' in self.fields:
            self.fields['parent'].required = False


class PageForm(TranslatedModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = tw_widgets(Page)


class ContactMessageForm(forms.ModelForm):
    """Front-end contact form (subset of fields)."""
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'First Name *'}),
            'last_name': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': TW_INPUT, 'placeholder': 'Email Address *'}),
            'phone': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Phone Number'}),
            'subject': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Subject *'}),
            'message': forms.Textarea(attrs={'class': TW_TEXTAREA, 'placeholder': 'Your Message *', 'rows': 5}),
        }


class CountryForm(TranslatedModelForm):
    class Meta:
        model = Country
        fields = '__all__'
        widgets = tw_widgets(Country)


class ProductInquiryForm(forms.ModelForm):
    """Front-end product inquiry/sourcing request form."""
    class Meta:
        model = ProductInquiry
        fields = ['full_name', 'email', 'phone', 'company_name', 'delivery_country',
                  'product_category', 'product_description', 'quantity', 'budget_range', 'additional_notes']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Full Name *'}),
            'email': forms.EmailInput(attrs={'class': TW_INPUT, 'placeholder': 'Email Address *'}),
            'phone': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Phone Number'}),
            'company_name': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Company Name'}),
            'delivery_country': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Delivery Country *'}),
            'product_category': forms.Select(attrs={'class': TW_SELECT}),
            'product_description': forms.Textarea(attrs={'class': TW_TEXTAREA, 'placeholder': 'Describe the product(s) you need *', 'rows': 4}),
            'quantity': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Estimated Quantity'}),
            'budget_range': forms.TextInput(attrs={'class': TW_INPUT, 'placeholder': 'Budget Range (e.g. $5,000 - $10,000)'}),
            'additional_notes': forms.Textarea(attrs={'class': TW_TEXTAREA, 'placeholder': 'Additional Requirements or Notes', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active categories; add empty default option
        self.fields['product_category'].queryset = ProductCategory.objects.filter(is_active=True)
        self.fields['product_category'].empty_label = '— Select Category (optional) —'
        self.fields['product_category'].required = False


class ProductInquiryAdminForm(TranslatedModelForm):
    class Meta:
        model = ProductInquiry
        fields = '__all__'
        widgets = tw_widgets(ProductInquiry)
