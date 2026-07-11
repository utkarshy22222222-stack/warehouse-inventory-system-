from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, ProductViewSet, StockViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"warehouses", WarehouseViewSet)
router.register(r"products", ProductViewSet)
router.register(r"stocks", StockViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = router.urls
