"""Generate sample orders aligned with the canonical inventory and warehouses.

Reads inventory.json to use real SKUs/categories so generated orders are
consistent with the rest of the dataset.
"""
import json
import os
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

with open(os.path.join(DATA_DIR, 'inventory.json'), 'r') as f:
    inventory = json.load(f)

products = [
    {
        'sku': item['sku'],
        'name': item['name'],
        'category': item['category'],
        'price': item['unit_cost'],
    }
    for item in inventory
]

customers = [
    "Acme Manufacturing Corp", "TechBuild Industries", "Global Parts Ltd",
    "Precision Tools Inc", "Industrial Solutions Inc", "MegaCorp Industries",
    "BuildTech Co", "FastAssembly Ltd", "Quality Parts LLC", "Superior Manufacturing",
    "PrecisionWorks Inc", "Elite Systems Corp", "Advanced Components Inc",
    "ProManufacturing LLC", "TechSolutions Group", "Innovative Parts Co",
    "Premier Industries", "Dynamic Systems Ltd", "Quantum Manufacturing",
    "Apex Engineering", "Titan Products Inc", "Vanguard Systems",
    "Omega Manufacturing", "Fusion Industries", "Stellar Components Ltd",
    "Nexus Engineering", "Cascade Manufacturing", "Horizon Technologies",
    "Summit Parts Corp", "Velocity Industries",
]

warehouses = ["San Francisco", "London", "Tokyo"]
statuses = ["Delivered", "Shipped", "Processing", "Backordered"]

orders = []
order_id = 1

for month in range(1, 13):
    num_orders = random.randint(8, 12)
    for _ in range(num_orders):
        day = random.randint(1, 28)
        hour = random.randint(8, 17)
        minute = random.randint(0, 59)
        order_date = f"2025-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00"
        order_datetime = datetime(2025, month, day, hour, minute)
        delivery_days = random.randint(7, 14)
        expected_delivery = order_datetime + timedelta(days=delivery_days)

        if month <= 8:
            status = random.choices(statuses, weights=[70, 20, 5, 5])[0]
        elif month <= 10:
            status = random.choices(statuses, weights=[40, 40, 15, 5])[0]
        else:
            status = random.choices(statuses, weights=[10, 30, 40, 20])[0]

        num_items = random.randint(1, 3)
        order_products = random.sample(products, num_items)

        items = []
        total_value = 0
        primary_category = None
        for product in order_products:
            quantity = random.randint(50, 1000)
            item_value = quantity * product['price']
            total_value += item_value
            if primary_category is None:
                primary_category = product['category']
            items.append({
                'sku': product['sku'],
                'name': product['name'],
                'quantity': quantity,
                'unit_price': product['price'],
            })

        order = {
            'id': str(order_id),
            'order_number': f"ORD-2025-{order_id:04d}",
            'customer': random.choice(customers),
            'items': items,
            'status': status,
            'warehouse': random.choice(warehouses),
            'category': primary_category,
            'order_date': order_date,
            'expected_delivery': expected_delivery.strftime("%Y-%m-%dT%H:%M:%S"),
            'total_value': round(total_value, 2),
        }
        if status == 'Delivered' and month <= 10:
            actual_delivery = order_datetime + timedelta(days=random.randint(6, delivery_days + 2))
            order['actual_delivery'] = actual_delivery.strftime("%Y-%m-%dT%H:%M:%S")

        orders.append(order)
        order_id += 1

with open(os.path.join(DATA_DIR, 'orders.json'), 'w') as f:
    json.dump(orders, f, indent=2)

print(f"Generated {len(orders)} orders across 12 months of 2025")

from collections import defaultdict
orders_per_month = defaultdict(int)
for order in orders:
    orders_per_month[order['order_date'][5:7]] += 1

print("\nOrders per month:")
for month in sorted(orders_per_month.keys()):
    print(f"  {month}: {orders_per_month[month]} orders")
