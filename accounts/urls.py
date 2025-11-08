from django.urls import path
from accounts import views
from .views import send_otp_ajax, verify_otp_ajax

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),
    path("auth/ajax/send-otp/", send_otp_ajax),
    path("auth/ajax/verify-otp/", verify_otp_ajax),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/details/', views.UserDetailsView.as_view(), name='dashboard-details'),
    path('dashboard/favorites/', views.dashboard_favorites, name='dashboard-favorites'),
    path('dashboard/favorites/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('dashboard/address/', views.dashboard_address, name='dashboard-address'),
    path('dashboard/address/add/', views.add_address_modal, name='add_address'),
    path('dashboard/address/edit/<int:pk>/', views.edit_address_modal, name='edit_address'),
    path('dashboard/address/delete/<int:pk>/', views.delete_address, name='delete_address'),
    path('dashboard/orders/', views.dashboard_orders, name='dashboard-orders'),
    path('dashboard/orders/<int:order_id>/', views.dashboard_order_details, name='dashboard-order-details'),
]
