from django.contrib import admin
from .models import Warehouse, Product, Stock, Order, OrderItem


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "created_at")
    search_fields = ("name", "location")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price", "low_stock_threshold")
    search_fields = ("sku", "name")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "is_low_stock", "updated_at")
    list_filter = ("warehouse",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "warehouse", "status", "created_at")
    list_filter = ("status", "warehouse")
    inlines = [OrderItemInline]
