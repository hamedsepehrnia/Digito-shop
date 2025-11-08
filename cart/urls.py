from django.urls import path

from cart import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/update-session/<str:item_key>/', views.update_session_cart_item, name='update_session_cart_item'),
    path('cart/remove-session/<str:item_key>/', views.remove_session_cart_item, name='remove_session_cart_item'),
]