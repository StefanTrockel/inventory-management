import os
import re
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mock_data import (
    inventory_items,
    orders,
    demand_forecasts,
    backlog_items,
    spending_summary,
    monthly_spending,
    category_spending,
    recent_transactions,
    purchase_orders,
    submitted_orders,
    tasks,
)

app = FastAPI(title="Factory Inventory Management System")

QUARTER_MAP = {
    'Q1-2025': ['2025-01', '2025-02', '2025-03'],
    'Q2-2025': ['2025-04', '2025-05', '2025-06'],
    'Q3-2025': ['2025-07', '2025-08', '2025-09'],
    'Q4-2025': ['2025-10', '2025-11', '2025-12'],
}

MONTH_TO_QUARTER = {m: q for q, ms in QUARTER_MAP.items() for m in ms}

MONTH_RE = re.compile(r'^(\d{4}-\d{2}|Q[1-4]-\d{4}|all)$')


def _quarter_months(month: str) -> Optional[List[str]]:
    return QUARTER_MAP.get(month)


def filter_by_month(items: list, month: Optional[str]) -> list:
    if not month or month == 'all':
        return items
    if not MONTH_RE.match(month):
        raise HTTPException(status_code=400, detail=f"Invalid month parameter: {month!r}")
    if month.startswith('Q'):
        quarter_months = _quarter_months(month)
        if not quarter_months:
            return []
        return [item for item in items if item.get('order_date', '')[:7] in quarter_months]
    return [item for item in items if item.get('order_date', '').startswith(month)]


def apply_filters(items: list, warehouse: Optional[str] = None, category: Optional[str] = None,
                  status: Optional[str] = None) -> list:
    filtered = items
    if warehouse and warehouse != 'all':
        filtered = [item for item in filtered if item.get('warehouse') == warehouse]
    if category and category != 'all':
        filtered = [item for item in filtered if item.get('category', '').lower() == category.lower()]
    if status and status != 'all':
        filtered = [item for item in filtered if item.get('status', '').lower() == status.lower()]
    return filtered


def _filter_backlog_by_warehouse_category(items: list, warehouse: Optional[str], category: Optional[str]) -> list:
    if not (warehouse and warehouse != 'all') and not (category and category != 'all'):
        return items
    inventory_by_sku = {inv['sku']: inv for inv in inventory_items}
    result = []
    for item in items:
        inv = inventory_by_sku.get(item.get('item_sku'))
        if inv is None:
            continue
        if warehouse and warehouse != 'all' and inv.get('warehouse') != warehouse:
            continue
        if category and category != 'all' and inv.get('category', '').lower() != category.lower():
            continue
        result.append(item)
    return result


_allowed_origins_env = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
_allowed_origins = [o.strip() for o in _allowed_origins_env.split(',') if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InventoryItem(BaseModel):
    id: str
    sku: str
    name: str
    category: str
    warehouse: str
    quantity_on_hand: int
    reorder_point: int
    unit_cost: float
    location: str
    last_updated: str


class Order(BaseModel):
    id: str
    order_number: str
    customer: str
    items: List[dict]
    status: str
    order_date: str
    expected_delivery: str
    total_value: float
    actual_delivery: Optional[str] = None
    warehouse: Optional[str] = None
    category: Optional[str] = None


class DemandForecast(BaseModel):
    id: str
    item_sku: str
    item_name: str
    current_demand: int
    forecasted_demand: int
    trend: str
    period: str
    unit_cost: Optional[float] = None
    lead_time_days: Optional[int] = None


class SubmittedOrderItem(BaseModel):
    item_sku: str
    item_name: str
    quantity: int
    unit_cost: float
    lead_time_days: int


class SubmittedOrder(BaseModel):
    id: str
    order_number: str
    items: List[SubmittedOrderItem]
    total_value: float
    submitted_date: str
    expected_delivery: str
    max_lead_time_days: int
    status: str


class CreateSubmittedOrderRequest(BaseModel):
    items: List[SubmittedOrderItem]


class BacklogItem(BaseModel):
    id: str
    order_id: str
    item_sku: str
    item_name: str
    quantity_needed: int
    quantity_available: int
    days_delayed: int
    priority: str
    has_purchase_order: Optional[bool] = False
    purchase_order_id: Optional[str] = None


class PurchaseOrder(BaseModel):
    id: str
    backlog_item_id: str
    supplier_name: str
    quantity: int
    unit_cost: float
    expected_delivery_date: str
    status: str
    created_date: str
    notes: Optional[str] = None


class CreatePurchaseOrderRequest(BaseModel):
    backlog_item_id: str
    supplier_name: str
    quantity: int
    unit_cost: float
    expected_delivery_date: str
    notes: Optional[str] = None


class Task(BaseModel):
    id: int
    title: str
    priority: str
    dueDate: str
    status: str


class CreateTaskRequest(BaseModel):
    title: str
    priority: str = "medium"
    dueDate: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Factory Inventory Management System API", "version": "1.0.0"}


@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(warehouse: Optional[str] = None, category: Optional[str] = None):
    return apply_filters(inventory_items, warehouse, category)


@app.get("/api/inventory/{item_id}", response_model=InventoryItem)
def get_inventory_item(item_id: str):
    item = next((it for it in inventory_items if it["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/api/orders", response_model=List[Order])
def get_orders(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    month: Optional[str] = None,
):
    filtered = apply_filters(orders, warehouse, category, status)
    filtered = filter_by_month(filtered, month)
    return filtered


@app.get("/api/orders/submitted", response_model=List[SubmittedOrder])
def get_submitted_orders():
    """Get all restocking orders submitted via the Restocking tab."""
    return submitted_orders


@app.post("/api/orders/submit", response_model=SubmittedOrder, status_code=201)
def submit_restocking_order(payload: CreateSubmittedOrderRequest):
    """Submit a new restocking order built from demand-forecast recommendations."""
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item.")

    submitted_at = datetime.now()
    max_lead = max(item.lead_time_days for item in payload.items)
    expected_delivery = submitted_at + timedelta(days=max_lead)
    total_value = sum(item.quantity * item.unit_cost for item in payload.items)

    next_seq = len(submitted_orders) + 1
    new_order = {
        "id": f"sub-{int(submitted_at.timestamp())}-{next_seq}",
        "order_number": f"RST-{submitted_at.strftime('%Y%m%d')}-{next_seq:03d}",
        "items": [item.model_dump() for item in payload.items],
        "total_value": round(total_value, 2),
        "submitted_date": submitted_at.strftime("%Y-%m-%d"),
        "expected_delivery": expected_delivery.strftime("%Y-%m-%d"),
        "max_lead_time_days": max_lead,
        "status": "Submitted",
    }
    submitted_orders.insert(0, new_order)
    return new_order


@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/api/demand", response_model=List[DemandForecast])
def get_demand_forecasts(warehouse: Optional[str] = None, category: Optional[str] = None):
    if not (warehouse and warehouse != 'all') and not (category and category != 'all'):
        return demand_forecasts
    inventory_by_sku = {inv['sku']: inv for inv in inventory_items}
    result = []
    for forecast in demand_forecasts:
        inv = inventory_by_sku.get(forecast.get('item_sku'))
        if inv is None:
            continue
        if warehouse and warehouse != 'all' and inv.get('warehouse') != warehouse:
            continue
        if category and category != 'all' and inv.get('category', '').lower() != category.lower():
            continue
        result.append(forecast)
    return result


@app.get("/api/backlog", response_model=List[BacklogItem])
def get_backlog(warehouse: Optional[str] = None, category: Optional[str] = None):
    filtered = _filter_backlog_by_warehouse_category(backlog_items, warehouse, category)
    po_by_backlog = {po["backlog_item_id"]: po for po in purchase_orders}
    result = []
    for item in filtered:
        item_dict = dict(item)
        po = po_by_backlog.get(item["id"])
        item_dict["has_purchase_order"] = po is not None
        item_dict["purchase_order_id"] = po["id"] if po else None
        result.append(item_dict)
    return result


@app.get("/api/dashboard/summary")
def get_dashboard_summary(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    month: Optional[str] = None,
):
    filtered_inventory = apply_filters(inventory_items, warehouse, category)
    filtered_orders = apply_filters(orders, warehouse, category, status)
    filtered_orders = filter_by_month(filtered_orders, month)
    filtered_backlog = _filter_backlog_by_warehouse_category(backlog_items, warehouse, category)

    total_inventory_value = sum(item["quantity_on_hand"] * item["unit_cost"] for item in filtered_inventory)
    low_stock_items = len([item for item in filtered_inventory if item["quantity_on_hand"] <= item["reorder_point"]])
    pending_orders = len([o for o in filtered_orders if o["status"] in ["Processing", "Backordered"]])
    total_backlog_items = len(filtered_backlog)

    return {
        "total_inventory_value": round(total_inventory_value, 2),
        "low_stock_items": low_stock_items,
        "pending_orders": pending_orders,
        "total_backlog_items": total_backlog_items,
        "total_orders_value": sum(o["total_value"] for o in filtered_orders),
    }


@app.get("/api/spending/summary")
def get_spending_summary():
    return spending_summary


@app.get("/api/spending/monthly")
def get_monthly_spending():
    return monthly_spending


@app.get("/api/spending/categories")
def get_category_spending():
    return category_spending


@app.get("/api/spending/transactions")
def get_recent_transactions(warehouse: Optional[str] = None, category: Optional[str] = None):
    return apply_filters(recent_transactions, warehouse, category)


def _quarter_for_date(order_date: str) -> Optional[str]:
    if not order_date:
        return None
    return MONTH_TO_QUARTER.get(order_date[:7])


@app.get("/api/reports/quarterly")
def get_quarterly_reports(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
):
    filtered = apply_filters(orders, warehouse, category, status)

    quarters = {
        q: {
            'quarter': q,
            'total_orders': 0,
            'total_revenue': 0.0,
            'delivered_orders': 0,
            'avg_order_value': 0.0,
            'fulfillment_rate': 0.0,
        }
        for q in QUARTER_MAP
    }

    for order in filtered:
        quarter = _quarter_for_date(order.get('order_date', ''))
        if not quarter:
            continue
        bucket = quarters[quarter]
        bucket['total_orders'] += 1
        bucket['total_revenue'] += order.get('total_value', 0) or 0
        if order.get('status') == 'Delivered':
            bucket['delivered_orders'] += 1

    for data in quarters.values():
        if data['total_orders']:
            data['avg_order_value'] = round(data['total_revenue'] / data['total_orders'], 2)
            data['fulfillment_rate'] = round((data['delivered_orders'] / data['total_orders']) * 100, 1)
        data['total_revenue'] = round(data['total_revenue'], 2)

    return sorted(quarters.values(), key=lambda x: x['quarter'])


@app.get("/api/reports/monthly-trends")
def get_monthly_trends(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
):
    filtered = apply_filters(orders, warehouse, category, status)
    months: dict = {}
    for order in filtered:
        order_date = order.get('order_date', '')
        if len(order_date) < 7:
            continue
        month = order_date[:7]
        bucket = months.setdefault(month, {
            'month': month,
            'order_count': 0,
            'revenue': 0.0,
            'delivered_count': 0,
        })
        bucket['order_count'] += 1
        bucket['revenue'] += order.get('total_value', 0) or 0
        if order.get('status') == 'Delivered':
            bucket['delivered_count'] += 1

    for bucket in months.values():
        bucket['revenue'] = round(bucket['revenue'], 2)

    return sorted(months.values(), key=lambda x: x['month'])


@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return tasks


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(payload: CreateTaskRequest):
    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {
        "id": next_id,
        "title": payload.title,
        "priority": payload.priority,
        "dueDate": payload.dueDate or datetime.utcnow().strftime('%Y-%m-%d'),
        "status": "pending",
    }
    tasks.append(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/api/tasks/{task_id}", response_model=Task)
def toggle_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed" if task["status"] != "completed" else "pending"
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/api/purchase-orders", response_model=PurchaseOrder, status_code=201)
def create_purchase_order(payload: CreatePurchaseOrderRequest):
    if not any(b["id"] == payload.backlog_item_id for b in backlog_items):
        raise HTTPException(status_code=404, detail="Backlog item not found")
    if any(po["backlog_item_id"] == payload.backlog_item_id for po in purchase_orders):
        raise HTTPException(status_code=409, detail="Purchase order already exists for this backlog item")
    new_id = f"PO-{len(purchase_orders) + 1:04d}"
    po = {
        "id": new_id,
        "backlog_item_id": payload.backlog_item_id,
        "supplier_name": payload.supplier_name,
        "quantity": payload.quantity,
        "unit_cost": payload.unit_cost,
        "expected_delivery_date": payload.expected_delivery_date,
        "status": "Pending",
        "created_date": datetime.utcnow().strftime('%Y-%m-%d'),
        "notes": payload.notes,
    }
    purchase_orders.append(po)
    return po


@app.get("/api/purchase-orders/{backlog_item_id}", response_model=PurchaseOrder)
def get_purchase_order_by_backlog_item(backlog_item_id: str):
    po = next((p for p in purchase_orders if p["backlog_item_id"] == backlog_item_id), None)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
