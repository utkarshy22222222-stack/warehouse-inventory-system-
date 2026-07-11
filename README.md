# Warehouse Inventory & Order Management System

A backend system modeling core warehouse operations — built with Django and Django REST Framework.
Tracks products, multi-warehouse stock levels, and the full order lifecycle, with stock automatically
deducted on order placement and low-stock alerts.

## Tech Stack
- Python, Django, Django REST Framework
- SQLite (dev) — swappable for PostgreSQL
- JWT Authentication (djangorestframework-simplejwt)
- pytest + pytest-django + pytest-html for automated testing

## Features
- **Products**: full CRUD, unique SKU validation
- **Warehouses**: multiple warehouse locations
- **Stock**: per-warehouse inventory levels, low-stock flagging via `is_low_stock`
- **Orders**: order placement with automatic stock deduction, status lifecycle
  (`pending → shipped → delivered`), and rejection of orders that exceed available stock
- **Auth**: JWT-secured endpoints (all API routes require a valid access token)

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain JWT access/refresh token |
| GET/POST | `/api/warehouses/` | List / create warehouses |
| GET/POST | `/api/products/` | List / create products |
| GET/POST | `/api/stocks/` | List / create stock records |
| GET | `/api/stocks/low_stock/` | List stock at or below threshold |
| GET/POST | `/api/orders/` | List / place orders (auto-deducts stock) |
| PATCH | `/api/orders/{id}/update_status/` | Update order status |

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin panel: `http://127.0.0.1:8000/admin/`
API root: `http://127.0.0.1:8000/api/`

## Running Tests

```bash
pytest tests/ --html=report.html --self-contained-html -v
```

19 automated test cases across three modules:
- `tests/test_products.py` — product CRUD, validation, auth checks
- `tests/test_inventory.py` — stock creation, low-stock detection, duplicate prevention
- `tests/test_orders.py` — order placement, stock deduction, over-order rejection, status transitions

## Why This Project
Built to demonstrate backend system design (schema, REST APIs, business logic like
stock deduction and low-stock alerts) paired with rigorous automated testing —
bridging backend development and QA/test-automation practices.
