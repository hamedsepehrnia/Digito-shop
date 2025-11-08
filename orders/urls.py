from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/create/', views.create_order, name='create_order'),
    path('orders/complete/<int:order_id>/', views.checkout_complete, name='checkout_complete'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('payment/zarinpal/callback/', views.zarinpal_callback, name='zarinpal_callback'),
]