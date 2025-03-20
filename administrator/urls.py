from django.urls import path
from . import views
from .views import admin_orders_view, update_order_status

app_name = 'administrator'

urlpatterns = [
    path('orders', admin_orders_view, name='admin_orders'),
    path('orders/update/<int:order_id>/<str:status>/', update_order_status, name='update_order_status'),
    path('equipment', views.equipment_list, name='equipment_list'),
    path('update-equipment-status/', views.update_equipment_status, name='update_equipment_status'),
    path('add-equipment/', views.add_equipment, name='add_equipment'),
    path("rental-requests/", views.admin_rental_requests, name="admin_rental_requests"),
    path("approve-rental-request/", views.approve_rental_request, name="approve_rental_request"),
]
