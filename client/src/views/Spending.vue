<template>
  <div class="spending">
    <div class="page-header">
      <h2>{{ t("finance.title") }}</h2>
      <p>{{ t("finance.description") }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t("common.loading") }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <!-- Revenue & Financial KPIs -->
      <div class="stats-grid-finance">
        <div class="stat-card revenue-card">
          <div class="stat-label">{{ t("finance.totalRevenue") }}</div>
          <div class="stat-value">
            {{ formatCurrency(revenueMetrics.totalRevenue) }}
          </div>
          <div class="stat-change positive">
            <span class="change-icon">↑</span>
            {{ t("finance.fromOrders", { count: revenueMetrics.orderCount }) }}
          </div>
        </div>
        <div class="stat-card cost-card">
          <div class="stat-label">{{ t("finance.totalCosts") }}</div>
          <div class="stat-value">{{ formatCurrency(totalCosts) }}</div>
          <div class="stat-meta">{{ t("finance.costBreakdown") }}</div>
        </div>
        <div class="stat-card profit-card">
          <div class="stat-label">{{ t("finance.netProfit") }}</div>
          <div class="stat-value">{{ formatCurrency(netProfit) }}</div>
          <div class="stat-meta">
            {{ profitMargin }}% {{ t("finance.margin") }}
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t("finance.avgOrderValue") }}</div>
          <div class="stat-value">
            {{ formatCurrency(revenueMetrics.avgOrderValue) }}
          </div>
          <div class="stat-meta">{{ t("finance.perOrderRevenue") }}</div>
        </div>
      </div>

      <!-- Monthly Revenue vs Cost Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">{{ t("finance.revenueVsCosts.title") }}</h3>
          <div class="chart-legend">
            <span class="legend-item"
              ><span class="legend-dot revenue-color"></span
              >{{ t("finance.revenueVsCosts.revenue") }}</span
            >
            <span class="legend-item"
              ><span class="legend-dot cost-color"></span
              >{{ t("finance.revenueVsCosts.costs") }}</span
            >
          </div>
        </div>
        <div class="chart-container">
          <div class="bar-chart">
            <div class="y-axis">
              <span
                >{{ currencySymbol
                }}{{
                  Math.round(convertAmountForDisplay(maxRevenueValue))
                }}K</span
              >
              <span
                >{{ currencySymbol
                }}{{
                  Math.round(convertAmountForDisplay(maxRevenueValue * 0.75))
                }}K</span
              >
              <span
                >{{ currencySymbol
                }}{{
                  Math.round(convertAmountForDisplay(maxRevenueValue * 0.5))
                }}K</span
              >
              <span
                >{{ currencySymbol
                }}{{
                  Math.round(convertAmountForDisplay(maxRevenueValue * 0.25))
                }}K</span
              >
              <span>{{ currencySymbol }}0</span>
            </div>
            <div class="chart-area">
              <div
                v-for="month in monthlyRevenue"
                :key="month.month"
                class="bar-group-revenue"
              >
                <div class="revenue-bars">
                  <div
                    class="revenue-bar"
                    :style="{
                      height: getRevenueBarHeight(month.revenue) + '%',
                    }"
                    :title="`Revenue: ${formatCurrency(month.revenue)}`"
                  ></div>
                  <div
                    class="cost-bar"
                    :style="{ height: getRevenueBarHeight(month.costs) + '%' }"
                    :title="`Costs: ${formatCurrency(month.costs)}`"
                  ></div>
                </div>
                <span class="bar-label">{{ translateMonth(month.month) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Monthly Cost Flow Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">{{ t("finance.monthlyCostFlow.title") }}</h3>
          <div class="chart-legend">
            <span class="legend-item"
              ><span class="legend-dot procurement"></span
              >{{ t("finance.monthlyCostFlow.procurement") }}</span
            >
            <span class="legend-item"
              ><span class="legend-dot operational"></span
              >{{ t("finance.monthlyCostFlow.operational") }}</span
            >
            <span class="legend-item"
              ><span class="legend-dot labor"></span
              >{{ t("finance.monthlyCostFlow.labor") }}</span
            >
            <span class="legend-item"
              ><span class="legend-dot overhead"></span
              >{{ t("finance.monthlyCostFlow.overhead") }}</span
            >
          </div>
        </div>
        <div class="chart-container">
          <div class="bar-chart">
            <div class="y-axis">
              <span
                >{{ currencySymbol
                }}{{ Math.round(convertAmountForDisplay(25)) }}K</span
              >
              <span
                >{{ currencySymbol
                }}{{ Math.round(convertAmountForDisplay(20)) }}K</span
              >
              <span
                >{{ currencySymbol
                }}{{ Math.round(convertAmountForDisplay(15)) }}K</span
              >
              <span
                >{{ currencySymbol
                }}{{ Math.round(convertAmountForDisplay(10)) }}K</span
              >
              <span
                >{{ currencySymbol
                }}{{ Math.round(convertAmountForDisplay(5)) }}K</span
              >
              <span>{{ currencySymbol }}0</span>
            </div>
            <div class="chart-area">
              <div
                v-for="month in monthlySpending"
                :key="month.month"
                class="bar-group"
              >
                <div class="stacked-bar" @click="showCostDetail(month)">
                  <div
                    class="bar-segment procurement"
                    :style="{ height: getBarHeight(month.procurement) + '%' }"
                    :title="`Procurement: ${formatCurrency(month.procurement)}`"
                  ></div>
                  <div
                    class="bar-segment operational"
                    :style="{ height: getBarHeight(month.operational) + '%' }"
                    :title="`Operational: ${formatCurrency(month.operational)}`"
                  ></div>
                  <div
                    class="bar-segment labor"
                    :style="{ height: getBarHeight(month.labor) + '%' }"
                    :title="`Labor: ${formatCurrency(month.labor)}`"
                  ></div>
                  <div
                    class="bar-segment overhead"
                    :style="{ height: getBarHeight(month.overhead) + '%' }"
                    :title="`Overhead: ${formatCurrency(month.overhead)}`"
                  ></div>
                </div>
                <span class="bar-label">{{ translateMonth(month.month) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="two-column-grid">
        <!-- Category Spending Breakdown -->
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">
              {{ t("finance.categorySpending.title") }}
            </h3>
          </div>
          <div class="category-list">
            <div
              v-for="category in categorySpending"
              :key="category.category"
              class="category-item"
            >
              <div class="category-info">
                <div class="category-name">
                  {{ translateCategory(category.category) }}
                </div>
                <div class="category-amount">
                  {{ formatCurrency(category.amount) }}
                </div>
              </div>
              <div class="category-bar-container">
                <div
                  class="category-bar"
                  :style="{ width: category.percentage + '%' }"
                ></div>
              </div>
              <div class="category-meta">
                <span class="percentage"
                  >{{ category.percentage }}%
                  {{ t("finance.categorySpending.ofTotal") }}</span
                >
                <span
                  class="change"
                  :class="{
                    positive: category.change > 0,
                    negative: category.change < 0,
                  }"
                >
                  {{ category.change > 0 ? "+" : "" }}{{ category.change }}%
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Transactions -->
        <div class="card transactions-card">
          <div class="card-header">
            <h3 class="card-title">{{ t("finance.transactions.title") }}</h3>
          </div>
          <div class="transactions-table-container">
            <table class="transactions-table">
              <thead>
                <tr>
                  <th>{{ t("finance.transactions.id") }}</th>
                  <th>{{ t("finance.transactions.description") }}</th>
                  <th>{{ t("finance.transactions.vendor") }}</th>
                  <th>{{ t("finance.transactions.date") }}</th>
                  <th class="text-right">
                    {{ t("finance.transactions.amount") }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="transaction in recentTransactions"
                  :key="transaction.id"
                  class="clickable-row"
                  @click="handleTransactionClick(transaction)"
                >
                  <td class="transaction-id">
                    {{ transaction.id.toString().padStart(3, "0") }}
                  </td>
                  <td class="transaction-description">
                    {{ transaction.description }}
                  </td>
                  <td class="transaction-vendor">{{ transaction.vendor }}</td>
                  <td class="transaction-date">
                    {{ formatDateShort(transaction.date) }}
                  </td>
                  <td class="transaction-amount text-right">
                    {{ formatCurrency(transaction.amount) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <CostDetailModal
      :is-open="showCostModal"
      :cost-data="selectedCostData"
      @close="showCostModal = false"
    />
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from "vue";
import { api } from "../api";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";
import {
  formatCurrency as formatCurrencyUtil,
  convertAmount,
  currencySymbol as getCurrencySymbol,
} from "../utils/currency";
import { getYearMonthFromISO, parseISO } from "../utils/dates";
import CostDetailModal from "../components/CostDetailModal.vue";

export default {
  name: "Spending",
  components: {
    CostDetailModal,
  },
  setup() {
    const { t, currentCurrency } = useI18n();
    const loading = ref(true);
    const error = ref(null);
    const allMonthlySpending = ref([]);
    const allCategorySpending = ref([]);
    const allTransactions = ref([]);
    const summaryData = ref({});
    const allOrders = ref([]);

    // Modal state
    const showCostModal = ref(false);
    const selectedCostData = ref(null);

    // Use shared filters
    const {
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
      getCurrentFilters,
    } = useFilters();

    // Monthly spending chart always shows all months (not filtered)
    const monthlySpending = computed(() => {
      return allMonthlySpending.value;
    });

    // Filtered monthly spending for summary calculations only
    const filteredMonthlySpending = computed(() => {
      if (selectedPeriod.value === "all") {
        return allMonthlySpending.value;
      }

      // Extract month name from YYYY-MM format
      const monthMap = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
      };
      const selectedMonth = monthMap[selectedPeriod.value.split("-")[1]];
      return allMonthlySpending.value.filter((m) => m.month === selectedMonth);
    });

    const categorySpending = computed(() => {
      return allCategorySpending.value;
    });

    const recentTransactions = computed(() => {
      if (selectedPeriod.value === "all") {
        return allTransactions.value;
      }
      // Filter transactions by selected month
      return allTransactions.value.filter((t) => {
        const transactionMonth = getYearMonthFromISO(t.date);
        return transactionMonth === selectedPeriod.value;
      });
    });

    const summary = computed(() => {
      // Recalculate summary based on filteredMonthlySpending (not the chart data)
      if (filteredMonthlySpending.value.length === 0) {
        return summaryData.value;
      }

      const totals = filteredMonthlySpending.value.reduce(
        (acc, month) => ({
          procurement: acc.procurement + month.procurement,
          operational: acc.operational + month.operational,
          labor: acc.labor + month.labor,
          overhead: acc.overhead + month.overhead,
        }),
        { procurement: 0, operational: 0, labor: 0, overhead: 0 },
      );

      return {
        total_procurement_cost: totals.procurement,
        total_operational_cost: totals.operational,
        total_labor_cost: totals.labor,
        total_overhead: totals.overhead,
        procurement_change: summaryData.value.procurement_change || 0,
        operational_change: summaryData.value.operational_change || 0,
        labor_change: summaryData.value.labor_change || 0,
        overhead_change: summaryData.value.overhead_change || 0,
      };
    });

    // Filtered orders based on selected period
    const filteredOrders = computed(() => {
      if (selectedPeriod.value === "all") {
        return allOrders.value;
      }

      // Filter orders by selected month
      return allOrders.value.filter((order) => {
        const orderMonth = getYearMonthFromISO(order.order_date);
        return orderMonth === selectedPeriod.value;
      });
    });

    // Revenue metrics from filtered orders
    const revenueMetrics = computed(() => {
      const totalRevenue = filteredOrders.value.reduce(
        (sum, order) => sum + (order.total_value || 0),
        0,
      );
      const orderCount = filteredOrders.value.length;
      const avgOrderValue = orderCount > 0 ? totalRevenue / orderCount : 0;

      return {
        totalRevenue,
        orderCount,
        avgOrderValue,
        revenueGrowth: 15.3, // Placeholder - could calculate from historical data
      };
    });

    // Total costs from summary
    const totalCosts = computed(() => {
      return (
        summary.value.total_procurement_cost +
        summary.value.total_operational_cost +
        summary.value.total_labor_cost +
        summary.value.total_overhead
      );
    });

    // Net profit
    const netProfit = computed(() => {
      return revenueMetrics.value.totalRevenue - totalCosts.value;
    });

    // Profit margin percentage
    const profitMargin = computed(() => {
      if (revenueMetrics.value.totalRevenue === 0) return 0;
      return (
        (netProfit.value / revenueMetrics.value.totalRevenue) *
        100
      ).toFixed(1);
    });

    // Monthly revenue data for chart
    const monthlyRevenue = computed(() => {
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

      // Initialize all months
      const revenueByMonth = monthNames.map((month) => ({
        month,
        revenue: 0,
        costs: 0,
      }));

      allOrders.value.forEach((order) => {
        const orderDate = parseISO(order.order_date);
        if (!orderDate) return;
        const monthIndex = orderDate.getMonth();
        if (monthIndex >= 0 && monthIndex < 12) {
          revenueByMonth[monthIndex].revenue += order.total_value || 0;
        }
      });

      // Add costs from spending data
      allMonthlySpending.value.forEach((spending) => {
        const monthIndex = monthNames.indexOf(spending.month);
        if (monthIndex >= 0) {
          revenueByMonth[monthIndex].costs =
            spending.procurement +
            spending.operational +
            spending.labor +
            spending.overhead;
        }
      });

      return revenueByMonth;
    });

    const maxRevenueValue = computed(() => {
      if (monthlyRevenue.value.length === 0) return 0;
      const maxRevenue = Math.max(
        ...monthlyRevenue.value.map((m) => m.revenue),
      );
      const maxCost = Math.max(...monthlyRevenue.value.map((m) => m.costs));
      const max = Math.max(maxRevenue, maxCost);
      return max > 0 ? Math.ceil(max / 1000) : 0;
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
        const [
          summaryRes,
          monthlyRes,
          categoryRes,
          transactionsRes,
          ordersRes,
        ] = await Promise.all([
          api.getSpendingSummary({ signal }),
          api.getMonthlySpending({ signal }),
          api.getCategorySpending({ signal }),
          api.getTransactions(filters, { signal }),
          api.getOrders(filters, { signal }),
        ]);

        summaryData.value = summaryRes;
        allMonthlySpending.value = monthlyRes;
        allCategorySpending.value = categoryRes;
        allTransactions.value = transactionsRes;
        allOrders.value = ordersRes;
      } catch (err) {
        if (err?.code !== "CANCELED") {
          error.value = "Failed to load financial data: " + err.message;
        }
      } finally {
        loading.value = false;
      }
    };

    watch(
      [selectedPeriod, selectedLocation, selectedCategory, selectedStatus],
      loadData,
    );

    const formatCurrency = (value) => {
      return formatCurrencyUtil(value, currentCurrency.value);
    };

    const currencySymbol = computed(() =>
      getCurrencySymbol(currentCurrency.value),
    );

    const getBarHeight = (value) => {
      const maxValue = 25000;
      return (value / maxValue) * 100;
    };

    const getRevenueBarHeight = (value) => {
      const maxValue = maxRevenueValue.value * 1000;
      if (maxValue <= 0) return 0;
      return ((value || 0) / maxValue) * 100;
    };

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      });
    };

    const formatDateShort = (dateString) => {
      const date = new Date(dateString);
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const day = date.getDate().toString().padStart(2, "0");
      const year = date.getFullYear().toString().slice(-2);
      return `${month}/${day}/${year}`;
    };

    const translateMonth = (month) => {
      const monthMap = {
        Jan: t("months.jan"),
        Feb: t("months.feb"),
        Mar: t("months.mar"),
        Apr: t("months.apr"),
        May: t("months.may"),
        Jun: t("months.jun"),
        Jul: t("months.jul"),
        Aug: t("months.aug"),
        Sep: t("months.sep"),
        Oct: t("months.oct"),
        Nov: t("months.nov"),
        Dec: t("months.dec"),
      };
      return monthMap[month] || month;
    };

    const translateCategory = (category) => {
      // First try spending categories
      const spendingCategoryMap = {
        "Raw Materials": t("spendingCategories.rawMaterials"),
        Components: t("spendingCategories.components"),
        Equipment: t("spendingCategories.equipment"),
        Consumables: t("spendingCategories.consumables"),
      };

      // Then try product categories
      const productCategoryMap = {
        "Circuit Boards": t("categories.circuitBoards"),
        Sensors: t("categories.sensors"),
        Actuators: t("categories.actuators"),
        Controllers: t("categories.controllers"),
        "Power Supplies": t("categories.powerSupplies"),
      };

      return (
        spendingCategoryMap[category] ||
        productCategoryMap[category] ||
        category
      );
    };

    const handleTransactionClick = (transaction) => {
      alert(
        `Transaction Details:\n\nID: ${transaction.id}\nDescription: ${transaction.description}\nVendor: ${transaction.vendor}\nDate: ${formatDateShort(transaction.date)}\nAmount: ${formatCurrencyUtil(transaction.amount, currentCurrency.value)}`,
      );
    };

    const showCostDetail = (monthData) => {
      selectedCostData.value = monthData;
      showCostModal.value = true;
    };

    onMounted(loadData);

    const convertAmountForDisplay = (usdKValue) =>
      convertAmount(usdKValue * 1000, currentCurrency.value) / 1000;

    return {
      t,
      loading,
      error,
      summary,
      monthlySpending,
      categorySpending,
      recentTransactions,
      revenueMetrics,
      totalCosts,
      netProfit,
      profitMargin,
      monthlyRevenue,
      maxRevenueValue,
      formatCurrency,
      currencySymbol,
      getBarHeight,
      getRevenueBarHeight,
      formatDate,
      formatDateShort,
      translateMonth,
      translateCategory,
      handleTransactionClick,
      showCostModal,
      selectedCostData,
      showCostDetail,
      convertAmountForDisplay,
      Math,
    };
  },
};
</script>

<style scoped>
.stat-change {
  margin-top: var(--space-3);
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive {
  color: var(--success-text);
}

.stat-change.negative {
  color: var(--danger-text);
}

.change-icon {
  font-weight: 700;
  font-size: 1rem;
}

.chart-card {
  margin-bottom: var(--space-7);
}

.chart-legend {
  display: flex;
  gap: var(--space-6);
  font-size: 0.875rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--text-secondary);
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: var(--radius-full);
}

.legend-dot.procurement {
  background: var(--chart-1);
}
.legend-dot.operational {
  background: var(--chart-6);
}
.legend-dot.labor {
  background: var(--chart-2);
}
.legend-dot.overhead {
  background: var(--chart-3);
}
.legend-dot.revenue-color {
  background: var(--text-strong);
}
.legend-dot.cost-color {
  background: var(--chart-4);
}

.stats-grid-finance {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-7);
}

.revenue-card {
  border-left: 4px solid var(--text-strong);
}

.cost-card {
  border-left: 4px solid var(--danger);
}

.profit-card {
  border-left: 4px solid var(--accent);
}

.stat-meta {
  margin-top: var(--space-2);
  font-size: 0.813rem;
  color: var(--text-muted);
}

.bar-group-revenue {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
}

.revenue-bars {
  width: 100%;
  max-width: 80px;
  display: flex;
  gap: 6px;
  justify-content: center;
  align-items: flex-end;
  height: 100%;
  padding-bottom: 2rem;
}

.revenue-bar,
.cost-bar {
  width: 50%;
  max-width: 30px;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  transition: all var(--dur) var(--ease);
  cursor: pointer;
  min-height: 4px;
}

.revenue-bar {
  background: var(--chart-1);
}

.cost-bar {
  background: var(--chart-4);
}

.revenue-bar:hover,
.cost-bar:hover {
  opacity: 0.8;
  transform: scaleY(1.05);
}

.chart-container {
  padding: var(--space-6) 0;
}

.bar-chart {
  display: flex;
  gap: var(--space-6);
  height: 350px;
}

.y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-right: var(--space-4);
  font-size: 0.6875rem;
  color: var(--chart-axis);
  border-right: 1px solid var(--chart-grid);
}

.chart-area {
  flex: 1;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  gap: var(--space-2);
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
}

.stacked-bar {
  width: 100%;
  max-width: 60px;
  display: flex;
  flex-direction: column-reverse;
  align-items: stretch;
  height: 100%;
  padding-bottom: 2rem;
  cursor: pointer;
  transition: opacity var(--dur-fast) var(--ease);
}

.stacked-bar:hover {
  opacity: 0.85;
}

.bar-segment {
  width: 100%;
  transition: all var(--dur) var(--ease);
  cursor: pointer;
  display: block;
}

.bar-segment:first-child {
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
}

.bar-segment:last-child {
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.bar-segment.procurement {
  background: var(--chart-1);
}
.bar-segment.operational {
  background: var(--chart-6);
}
.bar-segment.labor {
  background: var(--chart-2);
}
.bar-segment.overhead {
  background: var(--chart-3);
}

.bar-segment:hover {
  opacity: 0.8;
}

.bar-label {
  margin-top: var(--space-2);
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--chart-axis);
}

.two-column-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: var(--space-7);
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.category-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.category-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-name {
  font-weight: 600;
  color: var(--text-primary);
}

.category-amount {
  font-weight: 700;
  color: var(--accent);
  font-size: 1.125rem;
  font-feature-settings: 'tnum' 1;
}

.category-bar-container {
  width: 100%;
  height: 6px;
  background: var(--bg-subtle);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.category-bar {
  height: 100%;
  background: var(--accent);
  border-radius: var(--radius-full);
  transition: width 0.6s var(--ease);
}

.category-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.813rem;
}

.percentage {
  color: var(--text-muted);
}

.change {
  font-weight: 600;
}

.change.positive {
  color: var(--success-text);
}

.change.negative {
  color: var(--danger-text);
}

.transactions-card {
  display: flex;
  flex-direction: column;
}

.transactions-table-container {
  overflow-y: auto;
  max-height: 400px;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
}

.transactions-table thead {
  position: sticky;
  top: 0;
  background: var(--bg-subtle);
  z-index: 1;
}

.transactions-table th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.6875rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-bottom: 1px solid var(--border);
}

.transactions-table th.text-right {
  text-align: right;
}

.transactions-table td {
  padding: var(--space-4) var(--space-4);
  border-bottom: 1px solid var(--border-faint);
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.transactions-table tbody tr {
  cursor: pointer;
  transition: background-color var(--dur-fast) var(--ease);
}

.transactions-table tbody tr:hover {
  background: var(--bg-subtle);
}

.transactions-table tbody tr.clickable-row:hover {
  background: var(--bg-hover);
}

.transaction-id {
  color: var(--text-primary);
  font-weight: 500;
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  white-space: nowrap;
}

.transaction-description {
  color: var(--text-primary);
  font-weight: 500;
}

.transaction-vendor {
  color: var(--text-secondary);
}

.transaction-date {
  color: var(--text-secondary);
  font-size: 0.813rem;
}

.transaction-amount {
  font-weight: 700;
  color: var(--text-strong);
  font-feature-settings: 'tnum' 1;
}

.text-right {
  text-align: right;
}
</style>
