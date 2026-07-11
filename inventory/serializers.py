from rest_framework import serializers
from django.db import transaction
from .models import Warehouse, Product, Stock, Order, OrderItem


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "location", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "sku", "name", "description", "price", "low_stock_threshold", "created_at"]


class StockSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source="product.sku", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Stock
        fields = ["id", "warehouse", "warehouse_name", "product", "product_sku",
                   "quantity", "is_low_stock", "updated_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_sku", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "warehouse", "status", "items", "created_at", "updated_at"]
        read_only_fields = ["status"]

    def validate(self, data):
        warehouse = data["warehouse"]
        for item in data["items"]:
            product = item["product"]
            quantity = item["quantity"]
            try:
                stock = Stock.objects.get(warehouse=warehouse, product=product)
            except Stock.DoesNotExist:
                raise serializers.ValidationError(
                    f"No stock record for product '{product.sku}' at warehouse '{warehouse.name}'."
                )
            if stock.quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for '{product.sku}': requested {quantity}, available {stock.quantity}."
                )
        return data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            stock = Stock.objects.select_for_update().get(warehouse=order.warehouse, product=product)
            stock.quantity -= quantity
            stock.save()
        return order
