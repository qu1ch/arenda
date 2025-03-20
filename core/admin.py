from .models import Category, Equipment, Worker, Order
from django.contrib import admin
from .models import FreeEquipment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_hour')
    list_filter = ('category',)
    search_fields = ('name',)
    fieldsets = (
        ('Основная информация', {'fields': ('name', 'category', 'price_per_hour', 'image')}),
        ('Дополнительные параметры', {'fields': ('lifting_capacity', 'boom_reach', 'lift_height', 'body_volume')}),
    )


class FreeEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment', 'status', 'lifting_capacity', 'boom_reach', 'lift_height', 'body_volume')
    list_filter = ('status',)
    search_fields = ('name', 'equipment__name')

admin.site.register(FreeEquipment, FreeEquipmentAdmin)
admin.site.register(Worker)
admin.site.register(Order)
