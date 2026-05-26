<template>
  <div class="filters-bar">
    <div class="filters-container">
      <div class="filters-grid">
        <div v-if="show.period" class="filter-group">
          <label>{{ t("filters.timePeriod") }}</label>
          <select v-model="selectedPeriod" class="filter-select">
            <option value="all">{{ t("filters.allMonths") }}</option>
            <option value="2025-01">{{ t("months.january") }}</option>
            <option value="2025-02">{{ t("months.february") }}</option>
            <option value="2025-03">{{ t("months.march") }}</option>
            <option value="2025-04">{{ t("months.april") }}</option>
            <option value="2025-05">{{ t("months.may") }}</option>
            <option value="2025-06">{{ t("months.june") }}</option>
            <option value="2025-07">{{ t("months.july") }}</option>
            <option value="2025-08">{{ t("months.august") }}</option>
            <option value="2025-09">{{ t("months.september") }}</option>
            <option value="2025-10">{{ t("months.october") }}</option>
            <option value="2025-11">{{ t("months.november") }}</option>
            <option value="2025-12">{{ t("months.december") }}</option>
          </select>
        </div>

        <div v-if="show.location" class="filter-group">
          <label>{{ t("filters.location") }}</label>
          <select v-model="selectedLocation" class="filter-select">
            <option value="all">{{ t("filters.all") }}</option>
            <option value="San Francisco">
              {{ t("warehouses.sanFrancisco") }}
            </option>
            <option value="London">{{ t("warehouses.london") }}</option>
            <option value="Tokyo">{{ t("warehouses.tokyo") }}</option>
          </select>
        </div>

        <div v-if="show.category" class="filter-group">
          <label>{{ t("filters.category") }}</label>
          <select v-model="selectedCategory" class="filter-select">
            <option value="all">{{ t("filters.all") }}</option>
            <option value="circuit boards">
              {{ t("categories.circuitBoards") }}
            </option>
            <option value="sensors">{{ t("categories.sensors") }}</option>
            <option value="actuators">{{ t("categories.actuators") }}</option>
            <option value="controllers">
              {{ t("categories.controllers") }}
            </option>
            <option value="power supplies">
              {{ t("categories.powerSupplies") }}
            </option>
          </select>
        </div>

        <div v-if="show.status" class="filter-group">
          <label>{{ t("filters.orderStatus") }}</label>
          <select v-model="selectedStatus" class="filter-select">
            <option value="all">{{ t("filters.all") }}</option>
            <option value="delivered">{{ t("status.delivered") }}</option>
            <option value="shipped">{{ t("status.shipped") }}</option>
            <option value="processing">{{ t("status.processing") }}</option>
            <option value="backordered">{{ t("status.backordered") }}</option>
          </select>
        </div>
      </div>

      <button
        v-if="anyShown"
        class="reset-filters-btn"
        @click="resetRelevant"
        :disabled="!relevantActive"
        title="Reset filters"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";

const ROUTE_FILTERS = {
  "/": ["period", "location", "category", "status"],
  "/inventory": ["location", "category"],
  "/orders": ["period", "location", "category", "status"],
  "/spending": ["period", "location", "category"],
  "/demand": ["location", "category"],
  "/reports": ["location", "category", "status"],
  "/backlog": ["location", "category"],
};

export default {
  name: "FilterBar",
  setup() {
    const route = useRoute();
    const {
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
    } = useFilters();
    const { t } = useI18n();

    const relevantKeys = computed(
      () => ROUTE_FILTERS[route.path] || ROUTE_FILTERS["/"],
    );

    const show = computed(() => ({
      period: relevantKeys.value.includes("period"),
      location: relevantKeys.value.includes("location"),
      category: relevantKeys.value.includes("category"),
      status: relevantKeys.value.includes("status"),
    }));

    const anyShown = computed(() => Object.values(show.value).some(Boolean));

    const relevantActive = computed(
      () =>
        (show.value.period && selectedPeriod.value !== "all") ||
        (show.value.location && selectedLocation.value !== "all") ||
        (show.value.category && selectedCategory.value !== "all") ||
        (show.value.status && selectedStatus.value !== "all"),
    );

    const resetRelevant = () => {
      if (show.value.period) selectedPeriod.value = "all";
      if (show.value.location) selectedLocation.value = "all";
      if (show.value.category) selectedCategory.value = "all";
      if (show.value.status) selectedStatus.value = "all";
    };

    return {
      t,
      show,
      anyShown,
      relevantActive,
      resetRelevant,
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
    };
  },
};
</script>

<style scoped>
.filters-bar {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 20;
}

.filters-container {
  padding: var(--space-4) var(--space-8);
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.filters-grid {
  display: flex;
  align-items: center;
  gap: var(--space-5);
  flex: 1;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.filter-group label {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
  white-space: nowrap;
}

.filter-select {
  padding: 8px 32px 8px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
  background-color: var(--bg-surface);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M2.5 4.5L6 8L9.5 4.5' stroke='%238a93a2' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  cursor: pointer;
  transition: border-color var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease);
  min-width: 140px;
}

.filter-select:hover {
  border-color: var(--border-strong);
}

.filter-select:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-ring);
}

.reset-filters-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-muted);
  cursor: pointer;
  transition: background var(--dur-fast) var(--ease), border-color var(--dur-fast) var(--ease), color var(--dur-fast) var(--ease);
  flex-shrink: 0;
}

.reset-filters-btn:hover:not(:disabled) {
  background: var(--bg-hover);
  border-color: var(--border-strong);
  color: var(--text-strong);
}

.reset-filters-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.reset-filters-btn svg {
  width: 18px;
  height: 18px;
}
</style>
