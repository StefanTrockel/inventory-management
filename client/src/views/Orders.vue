<template>
  <div class="orders">
    <div class="page-header">
      <h2>{{ t("orders.title") }}</h2>
      <p>{{ t("orders.description") }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t("common.loading") }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-if="submittedOrders.length > 0" class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('orders.submittedOrders.title') }} ({{ submittedOrders.length }})</h3>
        </div>
        <div class="table-container">
          <table class="submitted-orders-table">
            <thead>
              <tr>
                <th class="scol-order-number">{{ t('orders.submittedOrders.orderNumber') }}</th>
                <th class="scol-items">{{ t('orders.submittedOrders.items') }}</th>
                <th class="scol-date">{{ t('orders.submittedOrders.submittedDate') }}</th>
                <th class="scol-date">{{ t('orders.submittedOrders.expectedDelivery') }}</th>
                <th class="scol-lead-time">{{ t('orders.submittedOrders.leadTime') }}</th>
                <th class="scol-value">{{ t('orders.submittedOrders.totalValue') }}</th>
                <th class="scol-status">{{ t('orders.submittedOrders.status') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in submittedOrders" :key="order.id">
                <td class="scol-order-number"><strong>{{ order.order_number }}</strong></td>
                <td class="scol-items">
                  <details class="items-details">
                    <summary class="items-summary">
                      {{ t('orders.itemsCount', { count: order.items.length }) }}
                    </summary>
                    <div class="items-dropdown">
                      <div v-for="item in order.items" :key="item.item_sku" class="item-entry">
                        <span class="item-name">{{ item.item_name }}</span>
                        <span class="item-meta">{{ t('orders.quantity') }}: {{ item.quantity }} @ {{ currencySymbol }}{{ item.unit_cost }} &mdash; {{ t('orders.submittedOrders.leadTime') }}: {{ item.lead_time_days }} {{ t('orders.submittedOrders.days') }}</span>
                      </div>
                    </div>
                  </details>
                </td>
                <td class="scol-date">{{ formatDate(order.submitted_date) }}</td>
                <td class="scol-date">{{ formatDate(order.expected_delivery) }}</td>
                <td class="scol-lead-time">{{ order.max_lead_time_days }} {{ t('orders.submittedOrders.days') }}</td>
                <td class="scol-value"><strong>{{ currencySymbol }}{{ order.total_value.toLocaleString() }}</strong></td>
                <td class="scol-status">
                  <span class="badge info">{{ t('orders.submittedOrders.submitted') }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="selectedStatus === 'all'" class="stats-grid">
        <div class="stat-card success">
          <div class="stat-label">{{ t("status.delivered") }}</div>
          <div class="stat-value">
            {{ getOrdersByStatus("Delivered").length }}
          </div>
        </div>
        <div class="stat-card info">
          <div class="stat-label">{{ t("status.shipped") }}</div>
          <div class="stat-value">
            {{ getOrdersByStatus("Shipped").length }}
          </div>
        </div>
        <div class="stat-card warning">
          <div class="stat-label">{{ t("status.processing") }}</div>
          <div class="stat-value">
            {{ getOrdersByStatus("Processing").length }}
          </div>
        </div>
        <div class="stat-card danger">
          <div class="stat-label">{{ t("status.backordered") }}</div>
          <div class="stat-value">
            {{ getOrdersByStatus("Backordered").length }}
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            {{ t("orders.allOrders") }} ({{ orders.length }})
          </h3>
        </div>
        <div class="table-container">
          <table class="orders-table">
            <thead>
              <tr>
                <th class="col-order-number">
                  {{ t("orders.table.orderNumber") }}
                </th>
                <th class="col-customer">{{ t("orders.table.customer") }}</th>
                <th class="col-items">{{ t("orders.table.items") }}</th>
                <th class="col-status">{{ t("orders.table.status") }}</th>
                <th class="col-date">{{ t("orders.table.orderDate") }}</th>
                <th class="col-date">
                  {{ t("orders.table.expectedDelivery") }}
                </th>
                <th class="col-value">{{ t("orders.table.totalValue") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td class="col-order-number">
                  <strong>{{ order.order_number }}</strong>
                </td>
                <td class="col-customer">
                  {{ translateCustomerName(order.customer) }}
                </td>
                <td class="col-items">
                  <details class="items-details">
                    <summary class="items-summary">
                      {{
                        t("orders.itemsCount", { count: order.items.length })
                      }}
                    </summary>
                    <div class="items-dropdown">
                      <div
                        v-for="item in order.items"
                        :key="item.sku || item.name"
                        class="item-entry"
                      >
                        <span class="item-name">{{
                          translateProductName(item.name)
                        }}</span>
                        <span class="item-meta"
                          >{{ t("orders.quantity") }}: {{ item.quantity }} @
                          {{ currencySymbol }}{{ item.unit_price }}</span
                        >
                      </div>
                    </div>
                  </details>
                </td>
                <td class="col-status">
                  <span :class="['badge', getOrderStatusClass(order.status)]">
                    {{ t(`status.${order.status.toLowerCase()}`) }}
                  </span>
                </td>
                <td class="col-date">{{ formatDate(order.order_date) }}</td>
                <td class="col-date">
                  {{ formatDate(order.expected_delivery) }}
                </td>
                <td class="col-value">
                  <strong
                    >{{ currencySymbol
                    }}{{ order.total_value.toLocaleString() }}</strong
                  >
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from "vue";
import { api } from "../api";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";
import { formatDateShort } from "../utils/dates";
import { compareISO } from "../utils/dates";

export default {
  name: "Orders",
  setup() {
    const {
      t,
      currentLocale,
      currentCurrency,
      translateProductName,
      translateCustomerName,
    } = useI18n();

    const currencySymbol = computed(() =>
      currentCurrency.value === "JPY" ? "¥" : "$",
    );

    const loading = ref(true);
    const error = ref(null);
    const orders = ref([]);
    const submittedOrders = ref([]);

    const {
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
      getCurrentFilters,
    } = useFilters();

    let inflight = null;
    const loadOrders = async () => {
      inflight?.abort();
      const controller = new AbortController();
      inflight = controller;
      loading.value = true;
      error.value = null;
      try {
        const [fetchedOrders, fetchedSubmitted] = await Promise.all([
          api.getOrders(getCurrentFilters(), { signal: controller.signal }),
          api.getSubmittedOrders({ signal: controller.signal }),
        ]);
        if (controller.signal.aborted) return;
        orders.value = fetchedOrders
          .slice()
          .sort((a, b) => compareISO(a.order_date, b.order_date));
        submittedOrders.value = fetchedSubmitted
          .slice()
          .sort((a, b) => compareISO(b.submitted_date, a.submitted_date));
      } catch (err) {
        if (err?.code === "CANCELED") return;
        error.value = err?.message || "Failed to load orders";
      } finally {
        loading.value = false;
      }
    };

    watch(
      [selectedPeriod, selectedLocation, selectedCategory, selectedStatus],
      () => {
        loadOrders();
      },
    );

    const getOrdersByStatus = (status) =>
      orders.value.filter((o) => o.status === status);

    const getOrderStatusClass = (status) => {
      const statusMap = {
        Delivered: "success",
        Shipped: "info",
        Processing: "warning",
        Backordered: "danger",
      };
      return statusMap[status] || "info";
    };

    const formatDate = (dateString) =>
      formatDateShort(dateString, currentLocale.value);

    onMounted(loadOrders);

    return {
      t,
      loading,
      error,
      orders,
      submittedOrders,
      selectedStatus,
      getOrdersByStatus,
      getOrderStatusClass,
      formatDate,
      currencySymbol,
      translateProductName,
      translateCustomerName,
    };
  },
};
</script>

<style scoped>
.submitted-orders-table {
  table-layout: fixed;
  width: 100%;
}

.scol-order-number {
  width: 170px;
}

.scol-items {
  width: 180px;
}

.scol-date {
  width: 130px;
}

.scol-lead-time {
  width: 110px;
}

.scol-value {
  width: 120px;
}

.scol-status {
  width: 110px;
}

.orders-table {
  table-layout: fixed;
  width: 100%;
}

.col-order-number {
  width: 130px;
}

.col-customer {
  width: 180px;
}

.col-items {
  width: 200px;
}

.col-status {
  width: 130px;
}

.col-date {
  width: 140px;
}

.col-value {
  width: 120px;
}

/* Order number / submitted order number — mono identifiers */
.scol-order-number strong,
.col-order-number strong {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.items-details {
  position: relative;
}

.items-summary {
  cursor: pointer;
  color: var(--accent);
  font-weight: 500;
  list-style: none;
  user-select: none;
  display: inline-block;
  font-size: 0.875rem;
  transition: color var(--dur-fast) var(--ease);
}

.items-summary::-webkit-details-marker {
  display: none;
}

.items-summary::before {
  content: "▶";
  display: inline-block;
  margin-right: 0.375rem;
  font-size: 0.75rem;
  transition: transform var(--dur-fast) var(--ease);
}

.items-details[open] .items-summary::before {
  transform: rotate(90deg);
}

.items-summary:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

.items-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: var(--space-2);
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  padding: var(--space-3);
  z-index: 10;
  min-width: 300px;
  max-width: 400px;
}

.item-entry {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: var(--space-2);
  border-bottom: 1px solid var(--border-faint);
}

.item-entry:last-child {
  border-bottom: none;
}

.item-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
}

.item-meta {
  font-size: 0.813rem;
  color: var(--text-secondary);
}
</style>
