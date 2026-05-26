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
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-header {
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.reports-table th {
  background: #f8fafc;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  border-bottom: 2px solid #e2e8f0;
}

.reports-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.reports-table tr:hover {
  background: #f8fafc;
}

.chart-container {
  padding: 2rem 1rem;
  min-height: 300px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 250px;
  gap: 0.5rem;
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
  background: linear-gradient(to top, #3b82f6, #60a5fa);
  border-radius: 4px 4px 0 0;
  transition: all 0.3s;
  cursor: pointer;
}

.bar:hover {
  background: linear-gradient(to top, #2563eb, #3b82f6);
}

.bar-label {
  margin-top: 1.5rem;
  font-size: 0.75rem;
  color: #64748b;
  text-align: center;
  transform: rotate(-45deg);
  white-space: nowrap;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #3b82f6;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0f172a;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.badge.success {
  background: #dcfce7;
  color: #166534;
}

.badge.warning {
  background: #fef3c7;
  color: #92400e;
}

.badge.danger {
  background: #fee2e2;
  color: #991b1b;
}

.positive-change {
  color: #16a34a;
  font-weight: 600;
}

.negative-change {
  color: #dc2626;
  font-weight: 600;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.error {
  background: #fee2e2;
  color: #991b1b;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
}
</style>
