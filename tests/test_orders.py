import pytest
from inventory.models import Stock


@pytest.mark.django_db
class TestOrderFlow:
    def test_place_order_deducts_stock(self, api_client, warehouse, product, stock):
        payload = {"warehouse": warehouse.id, "items": [{"product": product.id, "quantity": 5}]}
        response = api_client.post("/api/orders/", payload, format="json")
        assert response.status_code == 201
        stock.refresh_from_db()
        assert stock.quantity == 15  # 20 - 5

    def test_order_default_status_is_pending(self, api_client, warehouse, product, stock):
        payload = {"warehouse": warehouse.id, "items": [{"product": product.id, "quantity": 1}]}
        response = api_client.post("/api/orders/", payload, format="json")
        assert response.data["status"] == "pending"

    def test_over_order_rejected(self, api_client, warehouse, product, stock):
        payload = {"warehouse": warehouse.id, "items": [{"product": product.id, "quantity": 999}]}
        response = api_client.post("/api/orders/", payload, format="json")
        assert response.status_code == 400
        stock.refresh_from_db()
        assert stock.quantity == 20  # unchanged

    def test_order_without_stock_record_rejected(self, api_client, warehouse, product):
        # no Stock fixture used here -> no stock record exists for this product/warehouse
        payload = {"warehouse": warehouse.id, "items": [{"product": product.id, "quantity": 1}]}
        response = api_client.post("/api/orders/", payload, format="json")
        assert response.status_code == 400

    def test_update_order_status_transitions(self, api_client, warehouse, product, stock):
        create = api_client.post(
            "/api/orders/",
            {"warehouse": warehouse.id, "items": [{"product": product.id, "quantity": 2}]},
            format="json",
        )
        order_id = create.data["id"]
        response = api_client.patch(f"/api/orders/{order_id}/update_status/", {"status": "shipped"})
        assert response.status_code == 200
        assert response.data["status"] == "shipped"

    def test_invalid_status_rejected(self, api_client, warehouse, product, stock):
        create = api_client.post(
            "/api/orders/",
            {"warehouse": warehouse.id, "items": [{"product": product.id, "quantity": 1}]},
            format="json",
        )
        order_id = create.data["id"]
        response = api_client.patch(f"/api/orders/{order_id}/update_status/", {"status": "not_a_status"})
        assert response.status_code == 400
