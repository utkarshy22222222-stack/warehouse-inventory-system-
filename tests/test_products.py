import pytest


@pytest.mark.django_db
class TestProductCRUD:
    def test_create_product(self, api_client):
        payload = {"sku": "SKU200", "name": "New Widget", "price": "19.99", "low_stock_threshold": 5}
        response = api_client.post("/api/products/", payload)
        assert response.status_code == 201
        assert response.data["sku"] == "SKU200"

    def test_list_products(self, api_client, product):
        response = api_client.get("/api/products/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_retrieve_product(self, api_client, product):
        response = api_client.get(f"/api/products/{product.id}/")
        assert response.status_code == 200
        assert response.data["sku"] == product.sku

    def test_update_product(self, api_client, product):
        response = api_client.patch(f"/api/products/{product.id}/", {"name": "Updated Widget"})
        assert response.status_code == 200
        assert response.data["name"] == "Updated Widget"

    def test_delete_product(self, api_client, product):
        response = api_client.delete(f"/api/products/{product.id}/")
        assert response.status_code == 204

    def test_duplicate_sku_rejected(self, api_client, product):
        payload = {"sku": product.sku, "name": "Duplicate", "price": "10.00", "low_stock_threshold": 5}
        response = api_client.post("/api/products/", payload)
        assert response.status_code == 400

    def test_negative_price_rejected(self, api_client):
        payload = {"sku": "SKU300", "name": "Bad Price", "price": "-5.00", "low_stock_threshold": 5}
        response = api_client.post("/api/products/", payload)
        assert response.status_code == 400

    def test_unauthenticated_access_denied(self):
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.get("/api/products/")
        assert response.status_code == 401
