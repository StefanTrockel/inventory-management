"""Tests for orders, reports, tasks and purchase-order endpoints."""


class TestOrdersEndpoint:
    def test_get_all_orders(self, client):
        response = client.get("/api/orders")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        for field in ["id", "order_number", "customer", "items", "status", "order_date", "total_value"]:
            assert field in first

    def test_order_ids_are_unique(self, client):
        data = client.get("/api/orders").json()
        ids = [o["id"] for o in data]
        assert len(ids) == len(set(ids)), "Order ids must be unique"

    def test_get_order_by_id(self, client):
        data = client.get("/api/orders").json()
        target = data[0]["id"]
        response = client.get(f"/api/orders/{target}")
        assert response.status_code == 200
        assert response.json()["id"] == target

    def test_get_nonexistent_order(self, client):
        response = client.get("/api/orders/999999")
        assert response.status_code == 404

    def test_filter_by_warehouse(self, client):
        data = client.get("/api/orders?warehouse=Tokyo").json()
        assert all(o["warehouse"] == "Tokyo" for o in data)

    def test_filter_by_status(self, client):
        data = client.get("/api/orders?status=Delivered").json()
        assert all(o["status"].lower() == "delivered" for o in data)

    def test_filter_by_month_exact(self, client):
        data = client.get("/api/orders?month=2025-01").json()
        assert all(o["order_date"].startswith("2025-01") for o in data)

    def test_filter_by_month_does_not_substring_match(self, client):
        """Regression: a bare '01' must NOT match months by substring."""
        response = client.get("/api/orders?month=01")
        assert response.status_code == 400

    def test_filter_by_month_rejects_unknown_quarter(self, client):
        response = client.get("/api/orders?month=Q5-2025")
        # Q5 matches the regex shape Q[1-4] only for 1-4, so Q5 is a 400.
        assert response.status_code == 400

    def test_filter_by_valid_quarter(self, client):
        data = client.get("/api/orders?month=Q1-2025").json()
        assert all(o["order_date"][:7] in ["2025-01", "2025-02", "2025-03"] for o in data)


class TestReportsEndpoints:
    def test_quarterly_always_returns_four_quarters(self, client):
        data = client.get("/api/reports/quarterly").json()
        quarters = {q["quarter"] for q in data}
        assert quarters == {"Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025"}

    def test_quarterly_always_has_fulfillment_rate(self, client):
        data = client.get("/api/reports/quarterly").json()
        for q in data:
            assert "fulfillment_rate" in q
            assert "avg_order_value" in q
            assert isinstance(q["fulfillment_rate"], (int, float))

    def test_monthly_trends_structure(self, client):
        data = client.get("/api/reports/monthly-trends").json()
        assert isinstance(data, list)
        for m in data:
            for field in ["month", "order_count", "revenue", "delivered_count"]:
                assert field in m


class TestTasksEndpoints:
    def test_get_tasks(self, client):
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_toggle_delete_task(self, client):
        created = client.post("/api/tasks", json={"title": "Test task", "priority": "high"})
        assert created.status_code == 201
        task = created.json()
        assert task["title"] == "Test task"
        assert task["status"] == "pending"

        toggled = client.patch(f"/api/tasks/{task['id']}")
        assert toggled.status_code == 200
        assert toggled.json()["status"] == "completed"

        deleted = client.delete(f"/api/tasks/{task['id']}")
        assert deleted.status_code == 204

        missing = client.delete(f"/api/tasks/{task['id']}")
        assert missing.status_code == 404


class TestPurchaseOrderEndpoints:
    def test_get_seeded_purchase_order(self, client):
        # backlog item "2" is seeded with a PO in purchase_orders.json
        response = client.get("/api/purchase-orders/2")
        assert response.status_code == 200
        assert response.json()["backlog_item_id"] == "2"

    def test_get_missing_purchase_order(self, client):
        response = client.get("/api/purchase-orders/does-not-exist")
        assert response.status_code == 404

    def test_create_purchase_order(self, client):
        backlog = client.get("/api/backlog").json()
        # find a backlog item without a PO
        target = next((b for b in backlog if not b["has_purchase_order"]), None)
        assert target is not None
        payload = {
            "backlog_item_id": target["id"],
            "supplier_name": "Test Supplier",
            "quantity": 10,
            "unit_cost": 5.0,
            "expected_delivery_date": "2025-11-01",
        }
        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code == 201
        assert response.json()["backlog_item_id"] == target["id"]

    def test_create_purchase_order_unknown_backlog(self, client):
        payload = {
            "backlog_item_id": "nope",
            "supplier_name": "X",
            "quantity": 1,
            "unit_cost": 1.0,
            "expected_delivery_date": "2025-11-01",
        }
        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code == 404


class TestBacklogFilters:
    def test_backlog_warehouse_filter_matches_inventory(self, client):
        all_backlog = client.get("/api/backlog").json()
        assert len(all_backlog) > 0
        # Tokyo has SRV-301/SRV-302/PSU-508 backlog items
        tokyo = client.get("/api/backlog?warehouse=Tokyo").json()
        assert len(tokyo) <= len(all_backlog)
