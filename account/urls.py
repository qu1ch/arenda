from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account_view, name='account'),
    path('account/change-phone/', views.change_phone_number, name='change_phone_number'),
    path('change_phone', views.change_phone_number_view, name='change_phone_number_view'),
    path('account/change-email/', views.change_email, name='change_email'),
    path('change_email', views.change_email_view, name='change_email_view'),
    path('account/change-password/', views.change_password, name='change_password'),
    path('change_password', views.change_password_view, name='change_password_view'),
    path("my-orders", views.user_orders, name="user_orders"),
    path('equipment', views.equipment_list, name='equipment_list'),
    path('add_equipment', views.add_equipment, name='add_equipment'),
    path("rental-request/", views.create_rental_request, name="create_rental_request"),
    path('orders/', views.orders, name='orders'),

]
