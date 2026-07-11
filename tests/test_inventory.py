import pytest


@pytest.mark.django_db
class TestStockManagement:
    def test_create_stock(self, api_client, warehouse, product):
        payload = {"warehouse": warehouse.id, "product": product.id, "quantity": 30}
        response = api_client.post("/api/stocks/", payload)
        assert response.status_code == 201
        assert response.data["quantity"] == 30

    def test_stock_list_shows_correct_quantity(self, api_client, stock):
        response = api_client.get("/api/stocks/")
        assert response.status_code == 200
        assert response.data[0]["quantity"] == 20

    def test_low_stock_endpoint_excludes_healthy_stock(self, api_client, stock):
        response = api_client.get("/api/stocks/low_stock/")
        assert response.status_code == 200
        assert response.data == []

    def test_low_stock_endpoint_flags_low_quantity(self, api_client, stock):
        stock.quantity = 2  # below threshold of 5
        stock.save()
        response = api_client.get("/api/stocks/low_stock/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["is_low_stock"] is True

    def test_duplicate_stock_record_rejected(self, api_client, warehouse, product, stock):
        payload = {"warehouse": warehouse.id, "product": product.id, "quantity": 5}
        response = api_client.post("/api/stocks/", payload)
        assert response.status_code == 400
