from django.urls import path

from blog import views

urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
]