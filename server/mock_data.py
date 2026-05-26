"""Mock data loader.

Loads JSON files from server/data/ at import time. Each load is wrapped so
errors include the offending filename. Cross-file invariants (SKU references,
warehouse / category vocabulary, duplicate order IDs) are validated up front
so the API fails fast on bad seed data instead of returning confusing 500s.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

CANONICAL_WAREHOUSES = {'San Francisco', 'London', 'Tokyo'}
CANONICAL_INVENTORY_CATEGORIES = {'Circuit Boards', 'Sensors', 'Actuators', 'Controllers', 'Power Supplies'}


def load_json_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Data file missing: {filepath}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {filepath}: {exc}") from exc


inventory_items = load_json_file('inventory.json')
orders = load_json_file('orders.json')
demand_forecasts = load_json_file('demand_forecasts.json')
backlog_items = load_json_file('backlog_items.json')

spending_data = load_json_file('spending.json')
spending_summary = spending_data['spending_summary']
monthly_spending = spending_data['monthly_spending']
category_spending = spending_data['category_spending']

recent_transactions = load_json_file('transactions.json')
purchase_orders = load_json_file('purchase_orders.json')

# In-memory tasks (no JSON file — survives within one server run only).
tasks = [
    {"id": 1, "title": "Review Q4 inventory levels", "priority": "high", "dueDate": "2025-10-08", "status": "pending"},
    {"id": 2, "title": "Approve Tokyo warehouse orders", "priority": "medium", "dueDate": "2025-10-06", "status": "pending"},
    {"id": 3, "title": "Update reorder points for Circuit Boards", "priority": "medium", "dueDate": "2025-10-10", "status": "pending"},
    {"id": 4, "title": "Review monthly spending report", "priority": "low", "dueDate": "2025-10-15", "status": "pending"},
]


def _validate():
    if not isinstance(inventory_items, list):
        raise RuntimeError("inventory.json must be a list")
    if not isinstance(orders, list):
        raise RuntimeError("orders.json must be a list")

    order_ids = [o["id"] for o in orders]
    if len(order_ids) != len(set(order_ids)):
        duplicates = {oid for oid in order_ids if order_ids.count(oid) > 1}
        raise RuntimeError(f"Duplicate order ids in orders.json: {sorted(duplicates)[:10]}")

    inventory_skus = {item["sku"] for item in inventory_items}
    for forecast in demand_forecasts:
        if forecast.get("item_sku") not in inventory_skus:
            raise RuntimeError(f"demand_forecasts.json references unknown SKU {forecast.get('item_sku')!r}")
    for backlog in backlog_items:
        if backlog.get("item_sku") not in inventory_skus:
            raise RuntimeError(f"backlog_items.json references unknown SKU {backlog.get('item_sku')!r}")

    for item in inventory_items:
        if item.get("warehouse") not in CANONICAL_WAREHOUSES:
            raise RuntimeError(
                f"inventory.json item {item.get('id')} has non-canonical warehouse {item.get('warehouse')!r}"
            )
        if item.get("category") not in CANONICAL_INVENTORY_CATEGORIES:
            raise RuntimeError(
                f"inventory.json item {item.get('id')} has non-canonical category {item.get('category')!r}"
            )

    for order in orders:
        if order.get("warehouse") and order["warehouse"] not in CANONICAL_WAREHOUSES:
            raise RuntimeError(
                f"orders.json order {order.get('id')} has non-canonical warehouse {order.get('warehouse')!r}"
            )

    for tx in recent_transactions:
        if tx.get("warehouse") and tx["warehouse"] not in CANONICAL_WAREHOUSES:
            raise RuntimeError(
                f"transactions.json transaction {tx.get('id')} has non-canonical warehouse {tx.get('warehouse')!r}"
            )


_validate()
