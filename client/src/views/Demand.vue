<template>
  <div class="demand">
    <div class="page-header">
      <h2>{{ t("demand.title") }}</h2>
      <p>{{ t("demand.description") }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t("common.loading") }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="demand-trend-cards">
        <div class="trend-card increasing-card">
          <div class="trend-header">
            <div class="trend-icon">↑</div>
            <div>
              <div class="trend-label">{{ t("demand.increasingDemand") }}</div>
              <div class="trend-count">
                {{
                  t("demand.itemsCount", {
                    count: getForecastsByTrend("increasing").length,
                  })
                }}
              </div>
            </div>
          </div>
          <div class="trend-items">
            <div
              v-for="item in getForecastsByTrend('increasing').slice(0, 5)"
              :key="item.id"
              class="trend-item"
            >
              <span class="item-name">{{ item.item_name }}</span>
              <span class="item-change">{{ getChangePercent(item) }}</span>
            </div>
            <div
              v-if="getForecastsByTrend('increasing').length > 5"
              class="more-items"
            >
              +{{ getForecastsByTrend("increasing").length - 5 }}
              {{ t("demand.more") }}
            </div>
          </div>
        </div>

        <div class="trend-card stable-card">
          <div class="trend-header">
            <div class="trend-icon">→</div>
            <div>
              <div class="trend-label">{{ t("demand.stableDemand") }}</div>
              <div class="trend-count">
                {{
                  t("demand.itemsCount", {
                    count: getForecastsByTrend("stable").length,
                  })
                }}
              </div>
            </div>
          </div>
          <div class="trend-items">
            <div
              v-for="item in getForecastsByTrend('stable').slice(0, 5)"
              :key="item.id"
              class="trend-item"
            >
              <span class="item-name">{{ item.item_name }}</span>
              <span class="item-change neutral">{{
                getChangePercent(item)
              }}</span>
            </div>
            <div
              v-if="getForecastsByTrend('stable').length > 5"
              class="more-items"
            >
              +{{ getForecastsByTrend("stable").length - 5 }}
              {{ t("demand.more") }}
            </div>
          </div>
        </div>

        <div class="trend-card decreasing-card">
          <div class="trend-header">
            <div class="trend-icon">↓</div>
            <div>
              <div class="trend-label">{{ t("demand.decreasingDemand") }}</div>
              <div class="trend-count">
                {{
                  t("demand.itemsCount", {
                    count: getForecastsByTrend("decreasing").length,
                  })
                }}
              </div>
            </div>
          </div>
          <div class="trend-items">
            <div
              v-for="item in getForecastsByTrend('decreasing').slice(0, 5)"
              :key="item.id"
              class="trend-item"
            >
              <span class="item-name">{{ item.item_name }}</span>
              <span class="item-change">{{ getChangePercent(item) }}</span>
            </div>
            <div
              v-if="getForecastsByTrend('decreasing').length > 5"
              class="more-items"
            >
              +{{ getForecastsByTrend("decreasing").length - 5 }}
              {{ t("demand.more") }}
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("demand.demandForecasts") }}</h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t("demand.table.sku") }}</th>
                <th>{{ t("demand.table.itemName") }}</th>
                <th>{{ t("demand.table.currentDemand") }}</th>
                <th>{{ t("demand.table.forecastedDemand") }}</th>
                <th>{{ t("demand.table.change") }}</th>
                <th>{{ t("demand.table.trend") }}</th>
                <th>{{ t("demand.table.period") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="forecast in forecasts" :key="forecast.id">
                <td>
                  <strong>{{ forecast.item_sku }}</strong>
                </td>
                <td>{{ forecast.item_name }}</td>
                <td>{{ forecast.current_demand }}</td>
                <td>
                  <strong>{{ forecast.forecasted_demand }}</strong>
                </td>
                <td>
                  <span :style="{ color: getChangeColor(forecast) }">
                    {{ getChangePercent(forecast) }}
                  </span>
                </td>
                <td>
                  <span :class="['badge', forecast.trend]">
                    {{ t(`trends.${forecast.trend}`) }}
                  </span>
                </td>
                <td>{{ translatePeriod(forecast.period) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import { api } from "../api";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";

export default {
  name: "Demand",
  setup() {
    const { t, currentLocale } = useI18n();
    const loading = ref(true);
    const error = ref(null);
    const forecasts = ref([]);

    const { selectedLocation, selectedCategory, getCurrentFilters } =
      useFilters();

    let inflight = null;
    const loadForecasts = async () => {
      inflight?.abort();
      const controller = new AbortController();
      inflight = controller;
      loading.value = true;
      error.value = null;
      try {
        forecasts.value = await api.getDemandForecasts(getCurrentFilters(), {
          signal: controller.signal,
        });
      } catch (err) {
        if (err?.code === "CANCELED") return;
        error.value = err?.message || "Failed to load demand forecasts";
      } finally {
        loading.value = false;
      }
    };

    watch([selectedLocation, selectedCategory], () => {
      loadForecasts();
    });

    const getForecastsByTrend = (trend) =>
      forecasts.value.filter((f) => f.trend === trend);

    const getChangePercent = (forecast) => {
      if (forecast.current_demand === 0) return "—";
      const pct = (
        ((forecast.forecasted_demand - forecast.current_demand) /
          forecast.current_demand) *
        100
      ).toFixed(1);
      const num = parseFloat(pct);
      if (!isFinite(num)) return "—";
      return num > 0 ? `+${pct}%` : `${pct}%`;
    };

    const getChangeColor = (forecast) => {
      if (forecast.current_demand === 0) return "var(--chart-1)";
      const change = forecast.forecasted_demand - forecast.current_demand;
      const changePercent = Math.abs((change / forecast.current_demand) * 100);
      if (changePercent <= 2) return "var(--chart-1)";
      if (change > 0) return "var(--success)";
      if (change < 0) return "var(--danger)";
      return "var(--chart-1)";
    };

    const translatePeriod = (period) => {
      if (currentLocale.value === "ja") {
        return period
          .replace(/Next\s+/i, "次の")
          .replace(/\s+months/i, "か月")
          .replace(/\s+month/i, "か月")
          .replace(/\s+days/i, "日間")
          .replace(/\s+day/i, "日")
          .replace("Q1", "第1四半期")
          .replace("Q2", "第2四半期")
          .replace("Q3", "第3四半期")
          .replace("Q4", "第4四半期");
      }
      return period;
    };

    onMounted(loadForecasts);

    return {
      t,
      loading,
      error,
      forecasts,
      getForecastsByTrend,
      getChangePercent,
      getChangeColor,
      translatePeriod,
    };
  },
};
</script>

<style scoped>
.demand-trend-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-7);
}

.trend-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-xs);
  transition: border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}

.trend-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-md);
}

.increasing-card {
  border-left: 4px solid var(--success);
}

.stable-card {
  border-left: 4px solid var(--accent);
}

.decreasing-card {
  border-left: 4px solid var(--danger);
}

.trend-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-faint);
}

.trend-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  font-size: 1.5rem;
  font-weight: 700;
  flex-shrink: 0;
}

.increasing-card .trend-icon {
  background: var(--success-bg);
  color: var(--success-text);
}

.stable-card .trend-icon {
  background: var(--accent-subtle);
  color: var(--accent);
}

.decreasing-card .trend-icon {
  background: var(--danger-bg);
  color: var(--danger-text);
}

.trend-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.trend-count {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-strong);
  margin-top: var(--space-1);
  letter-spacing: -0.02em;
  font-feature-settings: 'tnum' 1;
}

.trend-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.trend-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) var(--space-3);
  background: var(--bg-subtle);
  border-radius: var(--radius-sm);
  transition: background var(--dur-fast) var(--ease);
}

.trend-item:hover {
  background: var(--bg-hover);
}

.item-name {
  font-size: 0.875rem;
  color: var(--text-primary);
  font-weight: 500;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: var(--space-4);
}

.item-change {
  font-size: 0.813rem;
  font-weight: 700;
  flex-shrink: 0;
  font-feature-settings: 'tnum' 1;
}

.increasing-card .item-change {
  color: var(--success-text);
}

.stable-card .item-change {
  color: var(--accent);
}

.decreasing-card .item-change {
  color: var(--danger-text);
}

.item-change.neutral {
  color: var(--text-muted);
}

.more-items {
  font-size: 0.813rem;
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
  padding: var(--space-2);
}

/* SKU mono in table */
:deep(td:first-child strong) {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
}
</style>
