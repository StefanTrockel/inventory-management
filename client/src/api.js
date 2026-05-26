import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export class ApiError extends Error {
  constructor(message, { status, code, cause } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status ?? null;
    this.code = code ?? null;
    if (cause) this.cause = cause;
  }
}

const client = axios.create({ baseURL: API_BASE_URL });

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isCancel(error)) {
      throw new ApiError("Request canceled", {
        code: "CANCELED",
        cause: error,
      });
    }
    const status = error.response?.status ?? null;
    const detail = error.response?.data?.detail;
    const message =
      detail ||
      (status ? `Request failed with status ${status}` : "Network error");
    throw new ApiError(message, { status, code: error.code, cause: error });
  },
);

function appendFilters(params, filters, allowed) {
  if (!filters) return;
  for (const key of allowed) {
    const value = filters[key];
    if (
      value !== undefined &&
      value !== null &&
      value !== "" &&
      value !== "all"
    ) {
      params.append(key, value);
    }
  }
}

async function get(path, { params, signal } = {}) {
  const qs = params && params.toString() ? `?${params.toString()}` : "";
  const response = await client.get(`${path}${qs}`, { signal });
  return response.data;
}

export const api = {
  async getInventory(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, ["warehouse", "category"]);
    return get("/inventory", { params, signal });
  },

  async getInventoryItem(id, { signal } = {}) {
    return get(`/inventory/${id}`, { signal });
  },

  async getOrders(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, [
      "warehouse",
      "category",
      "status",
      "month",
    ]);
    return get("/orders", { params, signal });
  },

  async getOrder(id, { signal } = {}) {
    return get(`/orders/${id}`, { signal });
  },

  async getDemandForecasts(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, ["warehouse", "category"]);
    return get("/demand", { params, signal });
  },

  async getBacklog(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, ["warehouse", "category"]);
    return get("/backlog", { params, signal });
  },

  async getDashboardSummary(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, [
      "warehouse",
      "category",
      "status",
      "month",
    ]);
    return get("/dashboard/summary", { params, signal });
  },

  async getSpendingSummary({ signal } = {}) {
    return get("/spending/summary", { signal });
  },

  async getMonthlySpending({ signal } = {}) {
    return get("/spending/monthly", { signal });
  },

  async getCategorySpending({ signal } = {}) {
    return get("/spending/categories", { signal });
  },

  async getTransactions(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, ["warehouse", "category"]);
    return get("/spending/transactions", { params, signal });
  },

  async getQuarterlyReports(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, [
      "warehouse",
      "category",
      "status",
      "month",
    ]);
    return get("/reports/quarterly", { params, signal });
  },

  async getMonthlyTrends(filters = {}, { signal } = {}) {
    const params = new URLSearchParams();
    appendFilters(params, filters, [
      "warehouse",
      "category",
      "status",
      "month",
    ]);
    return get("/reports/monthly-trends", { params, signal });
  },

  async getTasks({ signal } = {}) {
    return get("/tasks", { signal });
  },

  async createTask(taskData) {
    const response = await client.post("/tasks", taskData);
    return response.data;
  },

  async deleteTask(taskId) {
    const response = await client.delete(`/tasks/${taskId}`);
    return response.data;
  },

  async toggleTask(taskId) {
    const response = await client.patch(`/tasks/${taskId}`);
    return response.data;
  },

  async createPurchaseOrder(purchaseOrderData) {
    const response = await client.post("/purchase-orders", purchaseOrderData);
    return response.data;
  },

  async getPurchaseOrderByBacklogItem(backlogItemId, { signal } = {}) {
    return get(`/purchase-orders/${backlogItemId}`, { signal })
  },

  async getSubmittedOrders({ signal } = {}) {
    return get('/orders/submitted', { signal })
  },

  async submitRestockingOrder(items) {
    const response = await client.post('/orders/submit', { items })
    return response.data
  }
}
