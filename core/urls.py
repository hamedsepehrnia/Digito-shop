from django.urls import path

from core import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('rules/', views.RulesPageView.as_view(), name='rules'),
    path('faq/', views.FaqPageView.as_view(), name='faq'),
    path('contact/', views.contact_us, name='contact'),

]