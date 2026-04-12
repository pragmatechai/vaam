from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about/team/', views.team_page, name='team'),
    path('about/certificates/', views.certificates_page, name='certificates'),
    path('about/mission/', views.mission_vision, name='mission_vision'),
    path('about/clients/', views.clients_page, name='clients'),
    path('about/partners/', views.brands_page, name='brands'),
    path('services/', views.services, name='services'),
    path('services/process/', views.process_page, name='process'),
    path('services/quality-inspection/', views.quality_inspection, name='quality_inspection'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/case-studies/', views.case_studies, name='case_studies'),
    path('gallery/', views.gallery, name='gallery'),
    path('faq/', views.faq_page, name='faq'),
    path('news/', views.news_list, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('contact/', views.contact, name='contact'),
    path('inquiry/', views.product_inquiry, name='product_inquiry'),
    path('inquiry/track/', views.inquiry_track, name='inquiry_track'),
    path('documents/<int:pk>/download/', views.document_download, name='document_download'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]
