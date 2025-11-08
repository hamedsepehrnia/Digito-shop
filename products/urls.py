from django.urls import path, re_path

from products import views

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('bestsellers/', views.bestseller_products, name="bestseller_products"),
    # Use regex to support Unicode characters (Persian)
    # [^/]+ accepts any character except / (including Persian and Unicode)
    re_path(r"^products/(?P<slug>[^/]+)/$", views.single_product, name="product"),
    re_path(r"^products/(?P<slug>[^/]+)/comment/$", views.add_comment, name="add_comment"),
    path('search/', views.search_products, name="search_products"),
]