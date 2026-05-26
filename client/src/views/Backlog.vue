<template>
  <div class="backlog">
    <div class="page-header">
      <h2>{{ t("backlog.title") }}</h2>
      <p>{{ t("backlog.description") }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t("backlog.loading") }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="stats-grid">
        <div class="stat-card danger">
          <div class="stat-label">{{ t("backlog.high") }}</div>
          <div class="stat-value">
            {{ getBacklogByPriority("high").length }}
          </div>
        </div>
        <div class="stat-card warning">
          <div class="stat-label">{{ t("backlog.medium") }}</div>
          <div class="stat-value">
            {{ getBacklogByPriority("medium").length }}
          </div>
        </div>
        <div class="stat-card info">
          <div class="stat-label">{{ t("backlog.low") }}</div>
          <div class="stat-value">{{ getBacklogByPriority("low").length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t("backlog.table.itemName") }}</div>
          <div class="stat-value">{{ backlogItems.length }}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t("backlog.title") }}</h3>
        </div>
        <div v-if="backlogItems.length === 0" class="empty-state">
          <p>{{ t("backlog.empty") }}</p>
        </div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t("backlog.table.sku") }}</th>
                <th>{{ t("backlog.table.itemName") }}</th>
                <th>{{ t("backlog.table.quantityNeeded") }}</th>
                <th>{{ t("backlog.table.quantityAvailable") }}</th>
                <th>{{ t("backlog.table.shortage") }}</th>
                <th>{{ t("backlog.table.daysDelayed") }}</th>
                <th>{{ t("backlog.table.priority") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in backlogItems" :key="item.id">
                <td>
                  <strong>{{ item.item_sku }}</strong>
                </td>
                <td>{{ item.item_name }}</td>
                <td>{{ item.quantity_needed }}</td>
                <td>{{ item.quantity_available }}</td>
                <td>
                  <span class="badge danger">
                    {{ item.quantity_needed - item.quantity_available }}
                    {{ t("backlog.unitsShort") }}
                  </span>
                </td>
                <td>
                  <span
                    :style="{
                      color: item.days_delayed > 7 ? '#ef4444' : '#f59e0b',
                    }"
                  >
                    {{ item.days_delayed }} {{ t("backlog.days") }}
                  </span>
                </td>
                <td>
                  <span
                    :class="[
                      'badge',
                      item.priority ? item.priority.toLowerCase() : '',
                    ]"
                  >
                    {{
                      t(
                        `priority.${item.priority ? item.priority.toLowerCase() : "low"}`,
                      )
                    }}
                  </span>
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
import { ref, onMounted, watch } from "vue";
import { api } from "../api";
import { useFilters } from "../composables/useFilters";
import { useI18n } from "../composables/useI18n";

export default {
  name: "Backlog",
  setup() {
    const { t } = useI18n();
    const loading = ref(true);
    const error = ref(null);
    const backlogItems = ref([]);

    const { selectedLocation, selectedCategory, getCurrentFilters } =
      useFilters();

    let inflight = null;
    const loadBacklog = async () => {
      inflight?.abort();
      const controller = new AbortController();
      inflight = controller;
      loading.value = true;
      error.value = null;
      try {
        backlogItems.value = await api.getBacklog(getCurrentFilters(), {
          signal: controller.signal,
        });
      } catch (err) {
        if (err?.code === "CANCELED") return;
        error.value = err?.message || "Failed to load backlog";
      } finally {
        loading.value = false;
      }
    };

    const getBacklogByPriority = (priority) => {
      return backlogItems.value.filter(
        (item) => (item.priority || "").toLowerCase() === priority,
      );
    };

    watch([selectedLocation, selectedCategory], () => {
      loadBacklog();
    });

    onMounted(loadBacklog);

    return {
      t,
      loading,
      error,
      backlogItems,
      getBacklogByPriority,
    };
  },
};
</script>

<style scoped>
.empty-state {
  padding: 3rem;
  text-align: center;
  color: #10b981;
  font-size: 1.125rem;
  font-weight: 600;
}
</style>
