from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Warehouse, Product, Stock, Order
from .serializers import (
    WarehouseSerializer, ProductSerializer, StockSerializer, OrderSerializer
)


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related("product", "warehouse").all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """GET /api/stocks/low_stock/ - list all stock records at or below threshold."""
        low = [s for s in self.get_queryset() if s.is_low_stock]
        serializer = self.get_serializer(low, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        """PATCH /api/orders/{id}/update_status/ - move order through pending -> shipped -> delivered."""
        order = self.get_object()
        new_status = request.data.get("status")
        valid_statuses = dict(Order.STATUS_CHOICES)
        if new_status not in valid_statuses:
            return Response({"error": f"Invalid status. Choose from {list(valid_statuses)}."},
                             status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)
