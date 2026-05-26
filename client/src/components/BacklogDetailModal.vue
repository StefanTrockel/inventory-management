<template>
  <BaseModal
    :is-open="isOpen && !!backlogItem"
    title="Inventory Shortage Details"
    @close="$emit('close')"
  >
    <template v-if="backlogItem">
      <div class="shortage-header">
        <div class="shortage-icon">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <path
              d="M24 8L24 28M24 34L24 36"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
            />
            <circle
              cx="24"
              cy="24"
              r="18"
              stroke="currentColor"
              stroke-width="3"
            />
          </svg>
        </div>
        <div class="shortage-title-section">
          <h4 class="item-name">
            {{ translateProductName(backlogItem.item_name) }}
          </h4>
          <div class="item-sku">SKU: {{ backlogItem.item_sku }}</div>
        </div>
        <span class="priority-badge" :class="backlogItem.priority">
          {{ backlogItem.priority }} Priority
        </span>
      </div>

      <div class="shortage-summary">
        <div class="summary-card danger">
          <div class="summary-label">Shortage Amount</div>
          <div class="summary-value">{{ shortage }} units</div>
        </div>
        <div class="summary-card warning">
          <div class="summary-label">Days Delayed</div>
          <div class="summary-value">{{ backlogItem.days_delayed }} days</div>
        </div>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">Order ID</div>
          <div class="info-value order-id">{{ backlogItem.order_id }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Item SKU</div>
          <div class="info-value sku">{{ backlogItem.item_sku }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">Quantity Needed</div>
          <div class="info-value">{{ backlogItem.quantity_needed }} units</div>
        </div>

        <div class="info-item">
          <div class="info-label">Quantity Available</div>
          <div class="info-value">
            {{ backlogItem.quantity_available }} units
          </div>
        </div>

        <div class="info-item">
          <div class="info-label">Expected Date</div>
          <div class="info-value">
            {{ formatDate(backlogItem.expected_date) }}
          </div>
        </div>

        <div class="info-item">
          <div class="info-label">Status</div>
          <div class="info-value">
            <span class="badge danger">Backordered</span>
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
import BaseModal from "./BaseModal.vue";

const { translateProductName } = useI18n();

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  backlogItem: {
    type: Object,
    default: null,
  },
});

defineEmits(["close"]);

const shortage = computed(() => {
  if (!props.backlogItem) return 0;
  return (
    props.backlogItem.quantity_needed - props.backlogItem.quantity_available
  );
});

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};
</script>

<style scoped>
.shortage-header {
  display: flex;
  align-items: center;
  gap: var(--space-5);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border);
  margin-bottom: var(--space-6);
}

.shortage-icon {
  width: 56px;
  height: 56px;
  background: var(--danger);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.shortage-title-section {
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

.priority-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

.priority-badge.high {
  background: var(--danger-bg);
  color: var(--danger-text);
}

.priority-badge.medium {
  background: var(--warning-bg);
  color: var(--warning-text);
}

.priority-badge.low {
  background: var(--info-bg);
  color: var(--info-text);
}

.shortage-summary {
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

.summary-card.danger {
  border-color: var(--danger);
  background: var(--danger-bg);
}

.summary-card.warning {
  border-color: var(--warning);
  background: var(--warning-bg);
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

.summary-card.danger .summary-value {
  color: var(--danger-text);
}

.summary-card.warning .summary-value {
  color: var(--warning-text);
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

.info-value.order-id,
.info-value.sku {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--accent);
  white-space: nowrap;
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
