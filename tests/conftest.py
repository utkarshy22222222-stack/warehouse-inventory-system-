import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from inventory.models import Warehouse, Product, Stock


@pytest.fixture
def user(db):
    return User.objects.create_user(username="tester", password="testpass123")


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def warehouse(db):
    return Warehouse.objects.create(name="Test Warehouse", location="Lucknow")


@pytest.fixture
def product(db):
    return Product.objects.create(sku="SKU100", name="Test Widget", price="49.99", low_stock_threshold=5)


@pytest.fixture
def stock(db, warehouse, product):
    return Stock.objects.create(warehouse=warehouse, product=product, quantity=20)
