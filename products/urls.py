from django.urls import path, re_path

from products import views

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('bestsellers/', views.bestseller_products, name="bestseller_products"),
    # استفاده از regex برای پشتیبانی از کاراکترهای Unicode (فارسی)
    # [^/]+ هر کاراکتری به جز / را می‌پذیرد (شامل فارسی و Unicode)
    re_path(r"^products/(?P<slug>[^/]+)/$", views.single_product, name="product"),
    re_path(r"^products/(?P<slug>[^/]+)/comment/$", views.add_comment, name="add_comment"),
    path('search/', views.search_products, name="search_products"),
]