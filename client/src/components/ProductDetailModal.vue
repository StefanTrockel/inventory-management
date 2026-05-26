<template>
  <BaseModal
    :is-open="isOpen && !!product"
    title="Product Details"
    @close="$emit('close')"
  >
    <template v-if="product">
      <div class="product-header">
        <div class="product-icon">
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
          </svg>
        </div>
        <div class="product-title-section">
          <h4 class="product-name">{{ translateProductName(product.name) }}</h4>
          <div class="product-sku">SKU: {{ product.sku }}</div>
        </div>
        <span
          class="stock-badge"
          :class="getStockBadgeClass(product.stockLevel)"
        >
          {{ product.stockLevel }}
        </span>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">Category</div>
          <div class="info-value">{{ product.category }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Warehouse</div>
          <div class="info-value">{{ product.warehouse }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Units Ordered</div>
          <div class="info-value">{{ product.unitsOrdered }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Total Revenue</div>
          <div class="info-value">
            {{ formatCurrency(product.revenue, currentCurrency) }}
          </div>
        </div>

        <div class="info-item">
          <div class="info-label">Current Stock</div>
          <div class="info-value">{{ product.quantityOnHand }} units</div>
        </div>

        <div class="info-item">
          <div class="info-label">Reorder Point</div>
          <div class="info-value">{{ product.reorderPoint }} units</div>
        </div>

        <div class="info-item">
          <div class="info-label">First Order Date</div>
          <div class="info-value">{{ formatDate(product.firstOrderDate) }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Stock Status</div>
          <div class="info-value">
            <span :class="['badge', getStockBadgeClass(product.stockLevel)]">
              {{ product.stockLevel }}
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
import { useI18n } from "../composables/useI18n";
import { formatCurrency } from "../utils/currency";
import BaseModal from "./BaseModal.vue";

const { currentCurrency, translateProductName } = useI18n();

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  product: {
    type: Object,
    default: null,
  },
});

defineEmits(["close"]);

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const getStockBadgeClass = (stockLevel) => {
  if (stockLevel === "In Stock") return "success";
  if (stockLevel === "Low Stock") return "warning";
  if (stockLevel === "Out of Stock") return "danger";
  return "info";
};
</script>

<style scoped>
.product-header {
  display: flex;
  align-items: center;
  gap: var(--space-5);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border);
  margin-bottom: var(--space-7);
}

.product-icon {
  width: 56px;
  height: 56px;
  background: var(--accent);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.product-title-section {
  flex: 1;
  min-width: 0;
}

.product-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-strong);
  margin: 0 0 var(--space-2) 0;
  letter-spacing: -0.02em;
}

.product-sku {
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
