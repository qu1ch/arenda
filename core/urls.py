from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
                  path('', views.core, name='core'),
                  path('catalog', views.catalog, name='catalog'),
                  path('equipment/<int:equipment_id>/order/', views.equipment_order, name='equipment_order'),
                  path('order/success/', views.order_success, name='order_success'),
                  path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)