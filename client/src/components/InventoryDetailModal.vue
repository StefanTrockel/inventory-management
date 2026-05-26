<template>
  <BaseModal
    :is-open="isOpen && !!inventoryItem"
    title="Inventory Item Details"
    @close="$emit('close')"
  >
    <template v-if="inventoryItem">
      <div class="item-header">
        <div class="item-icon" :class="getStockIconClass()">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <rect
              x="8"
              y="12"
              width="32"
              height="28"
              rx="2"
              stroke="currentColor"
              stroke-width="2.5"
            />
            <path
              d="M16 8V16M32 8V16M8 20H40"
              stroke="currentColor"
              stroke-width="2.5"
              stroke-linecap="round"
            />
            <path
              d="M16 28H32M16 34H24"
              stroke="currentColor"
              stroke-width="2.5"
              stroke-linecap="round"
            />
          </svg>
        </div>
        <div class="item-title-section">
          <h4 class="item-name">
            {{ translateProductName(inventoryItem.name) }}
          </h4>
          <div class="item-sku">SKU: {{ inventoryItem.sku }}</div>
        </div>
        <span class="stock-badge" :class="getStockStatusClass()">
          {{ getStockStatus() }}
        </span>
      </div>

      <div class="stock-summary">
        <div class="summary-card primary">
          <div class="summary-label">Quantity on Hand</div>
          <div class="summary-value">
            {{ inventoryItem.quantity_on_hand }} units
          </div>
        </div>
        <div class="summary-card" :class="getSummaryCardClass()">
          <div class="summary-label">Stock Level</div>
          <div class="summary-value">{{ stockPercentage }}%</div>
          <div class="summary-subtitle">vs. reorder point</div>
        </div>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">Category</div>
          <div class="info-value">{{ inventoryItem.category }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Location</div>
          <div class="info-value">{{ inventoryItem.location }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Reorder Point</div>
          <div class="info-value">{{ inventoryItem.reorder_point }} units</div>
        </div>

        <div class="info-item">
          <div class="info-label">Units Remaining</div>
          <div class="info-value">
            <span
              :style="{
                color:
                  inventoryItem.quantity_on_hand <= inventoryItem.reorder_point
                    ? 'var(--danger)'
                    : 'var(--success)',
              }"
            >
              {{
                inventoryItem.quantity_on_hand - inventoryItem.reorder_point
              }}
              units
            </span>
          </div>
        </div>

        <div class="info-item">
          <div class="info-label">Unit Cost</div>
          <div class="info-value">
            {{
              formatCurrencyWithDecimals(
                inventoryItem.unit_cost,
                currentCurrency,
                2,
              )
            }}
          </div>
        </div>

        <div class="info-item">
          <div class="info-label">Total Value</div>
          <div class="info-value total-value">
            {{ formatCurrencyWithDecimals(totalValue, currentCurrency, 2) }}
          </div>
        </div>

        <div class="info-item">
          <div class="info-label">Warehouse</div>
          <div class="info-value">
            {{ translateWarehouse(inventoryItem.location) }}
          </div>
        </div>

        <div class="info-item">
          <div class="info-label">Status</div>
          <div class="info-value">
            <span :class="['badge', getStockStatusClass()]">
              {{ getStockStatus() }}
            </span>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <button class="btn-secondary" @click="$emit('close')">Close</button>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "../composables/useI18n";
import { formatCurrencyWithDecimals } from "../utils/currency";
import BaseModal from "./BaseModal.vue";

const { currentCurrency, translateProductName, translateWarehouse } = useI18n();

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  inventoryItem: {
    type: Object,
    default: null,
  },
});

defineEmits(["close"]);

const totalValue = computed(() => {
  if (!props.inventoryItem) return 0;
  return props.inventoryItem.quantity_on_hand * props.inventoryItem.unit_cost;
});

const stockPercentage = computed(() => {
  if (!props.inventoryItem || props.inventoryItem.reorder_point === 0) return 0;
  return Math.round(
    (props.inventoryItem.quantity_on_hand / props.inventoryItem.reorder_point) *
      100,
  );
});

const getStockStatus = () => {
  if (!props.inventoryItem) return "Unknown";
  if (
    props.inventoryItem.quantity_on_hand <= props.inventoryItem.reorder_point
  ) {
    return "Low Stock";
  } else if (
    props.inventoryItem.quantity_on_hand <=
    props.inventoryItem.reorder_point * 1.5
  ) {
    return "Adequate";
  } else {
    return "In Stock";
  }
};

const getStockStatusClass = () => {
  const status = getStockStatus();
  if (status === "Low Stock") return "danger";
  if (status === "Adequate") return "warning";
  return "success";
};

const getStockIconClass = () => {
  const status = getStockStatus();
  if (status === "Low Stock") return "danger-icon";
  if (status === "Adequate") return "warning-icon";
  return "success-icon";
};

const getSummaryCardClass = () => {
  const status = getStockStatus();
  if (status === "Low Stock") return "danger-card";
  if (status === "Adequate") return "warning-card";
  return "success-card";
};
</script>

<style scoped>
.item-header {
  display: flex;
  align-items: center;
  gap: var(--space-5);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border);
  margin-bottom: var(--space-6);
}

.item-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.item-icon.success-icon {
  background: var(--success);
}

.item-icon.warning-icon {
  background: var(--warning);
}

.item-icon.danger-icon {
  background: var(--danger);
}

.item-title-section {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-strong);
  margin: 0 0 var(--space-2) 0;
  letter-spacing: -0.02em;
}

.item-sku {
  font-size: 0.8125rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
  white-space: nowrap;
}

.stock-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

.stock-badge.success {
  background: var(--success-bg);
  color: var(--success-text);
}

.stock-badge.warning {
  background: var(--warning-bg);
  color: var(--warning-text);
}

.stock-badge.danger {
  background: var(--danger-bg);
  color: var(--danger-text);
}

.stock-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-7);
}

.summary-card {
  padding: var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid;
}

.summary-card.primary {
  border-color: var(--accent-ring);
  background: var(--accent-subtle);
}

.summary-card.success-card {
  border-color: var(--success);
  background: var(--success-bg);
}

.summary-card.warning-card {
  border-color: var(--warning);
  background: var(--warning-bg);
}

.summary-card.danger-card {
  border-color: var(--danger);
  background: var(--danger-bg);
}

.summary-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: var(--space-2);
}

.summary-value {
  font-size: 1.875rem;
  font-weight: 800;
  color: var(--text-strong);
  font-feature-settings: 'tnum' 1;
}

.summary-subtitle {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: var(--space-1);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-6);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.info-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
}

.info-value {
  font-size: 0.938rem;
  color: var(--text-primary);
  font-weight: 500;
}

.info-value.total-value {
  font-size: 1.125rem;
  color: var(--accent);
  font-weight: 700;
  font-feature-settings: 'tnum' 1;
}

.btn-secondary {
  padding: var(--space-3) var(--space-5);
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-weight: 500;
  font-size: 0.875rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--dur-fast) var(--ease);
  font-family: var(--font-sans);
}

.btn-secondary:hover {
  background: var(--bg-hover);
  border-color: var(--border-strong);
}
</style>
