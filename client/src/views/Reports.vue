<template>
  <div class="reports">
    <div class="page-header">
      <h2>{{ t("reports.title") }}</h2>
      <p>{{ t("reports.description") }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t("common.loading") }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <!-- Quarterly Performance -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("reports.quarterly") }}</h3>
        </div>
        <div class="table-container">
          <table class="reports-table">
            <thead>
              <tr>
                <th>{{ t("reports.quarter") }}</th>
                <th>{{ t("reports.orders") }}</th>
                <th>{{ t("reports.revenue") }}</th>
                <th>{{ t("reports.avgOrderValue") }}</th>
                <th>{{ t("reports.fulfillmentRate") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="q in quarterlyData" :key="q.quarter">
                <td>
                  <strong>{{ q.quarter }}</strong>
                </td>
                <td>{{ q.total_orders }}</td>
                <td>{{ formatCurrency(q.total_revenue) }}</td>
                <td>{{ formatCurrency(q.avg_order_value) }}</td>
                <td>
                  <span :class="getFulfillmentClass(q.fulfillment_rate)">
                    {{ q.fulfillment_rate }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Monthly Revenue Trend -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("reports.monthlyTrend") }}</h3>
        </div>
        <div class="chart-container">
          <div class="bar-chart">
            <div
              v-for="month in monthlyData"
              :key="month.month"
              class="bar-wrapper"
            >
              <div class="bar-container">
                <div
                  class="bar"
                  :style="{ height: getBarHeight(month.revenue) + 'px' }"
                  :title="formatCurrency(month.revenue)"
                ></div>
              </div>
              <div class="bar-label">{{ formatMonthLabel(month.month) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Month-over-Month Analysis -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("reports.monthOverMonth") }}</h3>
        </div>
        <div class="table-container">
          <table class="reports-table">
            <thead>
              <tr>
                <th>{{ t("reports.month") }}</th>
                <th>{{ t("reports.orders") }}</th>
                <th>{{ t("reports.revenue") }}</th>
                <th>Change</th>
                <th>{{ t("reports.growth") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(month, index) in monthlyData" :key="month.month">
                <td>
                  <strong>{{ formatMonthLabel(month.month) }}</strong>
                </td>
                <td>{{ month.order_count }}</td>
                <td>{{ formatCurrency(month.revenue) }}</td>
                <td>
                  <span
                    v-if="index > 0"
                    :class="
                      getChangeClass(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    "
                  >
                    {{
                      getChangeValue(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    }}
                  </span>
                  <span v-else>-</span>
                </td>
                <td>
                  <span
                    v-if="index > 0"
                    :class="
                      getChangeClass(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    "
                  >
                    {{
                      getGrowthRate(
                        month.revenue,
                        monthlyData[index - 1].revenue,
                      )
                    }}
                  </span>
                  <span v-else>-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Summary Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">{{ t("reports.totalRevenueYtd") }}</div>
          <div class="stat-value">{{ formatCurrency(totalRevenue) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Avg Monthly Revenue</div>
          <div class="stat-value">{{ formatCurrency(avgMonthlyRevenue) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Total Orders (YTD)</div>
          <div class="stat-value">{{ totalOrders }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t("reports.bestQuarter") }}</div>
          <div class="stat-value">{{ bestQuarter }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import { api } from "../api";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";
import { formatCurrency as formatCurrencyUtil } from "../utils/currency";

export default {
  name: "Reports",
  setup() {
    const { t, currentCurrency } = useI18n();
    const {
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
      getCurrentFilters,
    } = useFilters();

    const loading = ref(false);
    const error = ref(null);
    const quarterlyData = ref([]);
    const monthlyData = ref([]);

    const totalRevenue = computed(() => {
      return monthlyData.value.reduce((sum, m) => sum + (m.revenue || 0), 0);
    });

    const avgMonthlyRevenue = computed(() => {
      if (monthlyData.value.length === 0) return 0;
      return totalRevenue.value / monthlyData.value.length;
    });

    const totalOrders = computed(() => {
      return monthlyData.value.reduce(
        (sum, m) => sum + (m.order_count || 0),
        0,
      );
    });

    const bestQuarter = computed(() => {
      let best = "";
      let bestRevenue = -Infinity;
      for (const q of quarterlyData.value) {
        if ((q.total_revenue || 0) > bestRevenue) {
          bestRevenue = q.total_revenue;
          best = q.quarter;
        }
      }
      return best;
    });

    const maxBarRevenue = computed(() => {
      if (monthlyData.value.length === 0) return 0;
      return Math.max(...monthlyData.value.map((m) => m.revenue || 0));
    });

    let abortController = null;

    const loadData = async () => {
      if (abortController) abortController.abort();
      abortController = new AbortController();
      const signal = abortController.signal;

      loading.value = true;
      error.value = null;

      try {
        const filters = getCurrentFilters();
        const [quarterly, monthly] = await Promise.all([
          api.getQuarterlyReports(filters, { signal }),
          api.getMonthlyTrends(filters, { signal }),
        ]);
        quarterlyData.value = quarterly;
        monthlyData.value = monthly;
      } catch (err) {
        if (err?.code !== "CANCELED") {
          error.value = "Failed to load reports: " + err.message;
        }
      } finally {
        loading.value = false;
      }
    };

    const formatCurrency = (value) =>
      formatCurrencyUtil(value, currentCurrency.value);

    const formatMonthLabel = (monthStr) => {
      if (!monthStr || typeof monthStr !== "string") return monthStr;
      const parts = monthStr.split("-");
      if (parts.length < 2) return monthStr;
      const monthNames = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ];
      const idx = parseInt(parts[1], 10) - 1;
      if (idx < 0 || idx > 11) return monthStr;
      return monthNames[idx] + " " + parts[0];
    };

    const getBarHeight = (revenue) => {
      const max = maxBarRevenue.value;
      if (max <= 0) return 0;
      return ((revenue || 0) / max) * 200;
    };

    const getFulfillmentClass = (rate) => {
      if (rate >= 90) return "badge success";
      if (rate >= 75) return "badge warning";
      return "badge danger";
    };

    const getChangeValue = (current, previous) => {
      const change = (current || 0) - (previous || 0);
      if (change > 0) return "+" + formatCurrency(change);
      if (change < 0) return "-" + formatCurrency(Math.abs(change));
      return formatCurrency(0);
    };

    const getChangeClass = (current, previous) => {
      const change = (current || 0) - (previous || 0);
      if (change > 0) return "positive-change";
      if (change < 0) return "negative-change";
      return "";
    };

    const getGrowthRate = (current, previous) => {
      if (!previous) return "N/A";
      const rate = (((current || 0) - previous) / previous) * 100;
      return (rate > 0 ? "+" : "") + rate.toFixed(1) + "%";
    };

    watch(
      [selectedPeriod, selectedLocation, selectedCategory, selectedStatus],
      loadData,
    );

    onMounted(loadData);

    return {
      t,
      loading,
      error,
      quarterlyData,
      monthlyData,
      totalRevenue,
      avgMonthlyRevenue,
      totalOrders,
      bestQuarter,
      formatCurrency,
      formatMonthLabel,
      getBarHeight,
      getFulfillmentClass,
      getChangeValue,
      getChangeClass,
      getGrowthRate,
    };
  },
};
</script>

<style scoped>
.reports {
  padding: 0;
}

.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-6);
  box-shadow: var(--shadow-xs);
}

.card-header {
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-strong);
  margin: 0;
  letter-spacing: -0.01em;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.reports-table th {
  background: var(--bg-subtle);
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-bottom: 1px solid var(--border);
}

.reports-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-faint);
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.reports-table tr:hover {
  background: var(--bg-subtle);
}

/* Quarter identifier — mono */
.reports-table td:first-child strong {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--text-primary);
  white-space: nowrap;
}

/* Month label — mono */
.reports-table tbody td:first-child strong {
  font-family: var(--font-mono);
}

/* Revenue figures — tabular */
.reports-table td:nth-child(3),
.reports-table td:nth-child(4) {
  font-feature-settings: 'tnum' 1;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-container {
  padding: var(--space-7) var(--space-4);
  min-height: 300px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 250px;
  gap: var(--space-2);
}

.bar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 80px;
}

.bar-container {
  height: 200px;
  display: flex;
  align-items: flex-end;
  width: 100%;
}

.bar {
  width: 100%;
  background: var(--chart-1);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  transition: all var(--dur) var(--ease);
  cursor: pointer;
}

.bar:hover {
  background: var(--accent-hover);
}

.bar-label {
  margin-top: 1.5rem;
  font-size: 0.6875rem;
  color: var(--chart-axis);
  text-align: center;
  transform: rotate(-45deg);
  white-space: nowrap;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-4);
  margin-top: var(--space-6);
}

.stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-6);
  box-shadow: var(--shadow-xs);
  border-left: 4px solid var(--accent);
}

.stat-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: var(--space-2);
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 800;
  color: var(--text-strong);
  letter-spacing: -0.03em;
  font-feature-settings: 'tnum' 1;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.badge.success {
  background: var(--success-bg);
  color: var(--success-text);
}

.badge.warning {
  background: var(--warning-bg);
  color: var(--warning-text);
}

.badge.danger {
  background: var(--danger-bg);
  color: var(--danger-text);
}

.positive-change {
  color: var(--success-text);
  font-weight: 600;
  font-feature-settings: 'tnum' 1;
}

.negative-change {
  color: var(--danger-text);
  font-weight: 600;
  font-feature-settings: 'tnum' 1;
}

.loading {
  text-align: center;
  padding: var(--space-8);
  color: var(--text-muted);
}

.error {
  background: var(--danger-bg);
  color: var(--danger-text);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  margin: var(--space-4) 0;
}
</style>
