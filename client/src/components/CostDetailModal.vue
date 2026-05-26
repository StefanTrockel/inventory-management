<template>
  <BaseModal
    :is-open="isOpen && !!costData"
    :title="costData ? costData.month + ' Cost Breakdown' : ''"
    @close="$emit('close')"
  >
    <template v-if="costData">
      <div class="cost-summary">
        <div class="summary-card total">
          <div class="summary-label">Total Costs</div>
          <div class="summary-value">
            {{ formatCurrency(totalCosts, currentCurrency) }}
          </div>
        </div>
      </div>

      <div class="cost-breakdown">
        <div class="cost-item procurement">
          <div class="cost-header">
            <div class="cost-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect
                  x="4"
                  y="6"
                  width="16"
                  height="14"
                  rx="2"
                  stroke="currentColor"
                  stroke-width="2"
                />
                <path
                  d="M8 6V4M16 6V4M4 10H20"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </div>
            <div class="cost-info">
              <div class="cost-name">Procurement</div>
              <div class="cost-amount">
                {{ formatCurrency(costData.procurement, currentCurrency) }}
              </div>
            </div>
          </div>
          <div class="cost-percentage">
            {{ getProcurementPercentage() }}% of total
          </div>
        </div>

        <div class="cost-item operational">
          <div class="cost-header">
            <div class="cost-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle
                  cx="12"
                  cy="12"
                  r="8"
                  stroke="currentColor"
                  stroke-width="2"
                />
                <path
                  d="M12 8V12L15 15"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </div>
            <div class="cost-info">
              <div class="cost-name">Operational</div>
              <div class="cost-amount">
                {{ formatCurrency(costData.operational, currentCurrency) }}
              </div>
            </div>
          </div>
          <div class="cost-percentage">
            {{ getOperationalPercentage() }}% of total
          </div>
        </div>

        <div class="cost-item labor">
          <div class="cost-header">
            <div class="cost-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle
                  cx="12"
                  cy="8"
                  r="4"
                  stroke="currentColor"
                  stroke-width="2"
                />
                <path
                  d="M6 20C6 16.6863 8.68629 14 12 14C15.3137 14 18 16.6863 18 20"
                  stroke="currentColor"
                  stroke-width="2"
                />
              </svg>
            </div>
            <div class="cost-info">
              <div class="cost-name">Labor</div>
              <div class="cost-amount">
                {{ formatCurrency(costData.labor, currentCurrency) }}
              </div>
            </div>
          </div>
          <div class="cost-percentage">
            {{ getLaborPercentage() }}% of total
          </div>
        </div>

        <div class="cost-item overhead">
          <div class="cost-header">
            <div class="cost-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path
                  d="M3 12L5 10M5 10L12 3L19 10M5 10V20C5 20.5523 5.44772 21 6 21H9M19 10L21 12M19 10V20C19 20.5523 18.5523 21 18 21H15M9 21C9 21 9 18 9 16C9 14 10 14 12 14C14 14 15 14 15 16C15 18 15 21 15 21M9 21H15"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </div>
            <div class="cost-info">
              <div class="cost-name">Overhead</div>
              <div class="cost-amount">
                {{ formatCurrency(costData.overhead, currentCurrency) }}
              </div>
            </div>
          </div>
          <div class="cost-percentage">
            {{ getOverheadPercentage() }}% of total
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
import { formatCurrency } from "../utils/currency";
import BaseModal from "./BaseModal.vue";

const { currentCurrency } = useI18n();

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  costData: {
    type: Object,
    default: null,
  },
});

defineEmits(["close"]);

const totalCosts = computed(() => {
  if (!props.costData) return 0;
  return (
    props.costData.procurement +
    props.costData.operational +
    props.costData.labor +
    props.costData.overhead
  );
});

const getProcurementPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0;
  return ((props.costData.procurement / totalCosts.value) * 100).toFixed(1);
};

const getOperationalPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0;
  return ((props.costData.operational / totalCosts.value) * 100).toFixed(1);
};

const getLaborPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0;
  return ((props.costData.labor / totalCosts.value) * 100).toFixed(1);
};

const getOverheadPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0;
  return ((props.costData.overhead / totalCosts.value) * 100).toFixed(1);
};
</script>

<style scoped>
.cost-summary {
  margin-bottom: var(--space-7);
}

.summary-card {
  padding: var(--space-6);
  border-radius: var(--radius-lg);
  text-align: center;
}

.summary-card.total {
  background: var(--accent);
  color: var(--text-inverse);
}

.summary-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  opacity: 0.85;
  margin-bottom: var(--space-2);
}

.summary-value {
  font-size: 2.25rem;
  font-weight: 800;
  font-feature-settings: 'tnum' 1;
}

.cost-breakdown {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.cost-item {
  padding: var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid;
}

.cost-item.procurement {
  border-color: var(--accent-ring);
  background: var(--accent-subtle);
}

.cost-item.operational {
  border-color: rgba(139, 92, 246, 0.25);
  background: #f5f3ff;
}

.cost-item.labor {
  border-color: rgba(15, 157, 107, 0.25);
  background: var(--success-bg);
}

.cost-item.overhead {
  border-color: rgba(245, 158, 11, 0.25);
  background: var(--warning-bg);
}

.cost-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-2);
}

.cost-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.cost-item.procurement .cost-icon {
  background: var(--chart-1);
  color: white;
}

.cost-item.operational .cost-icon {
  background: var(--chart-6);
  color: white;
}

.cost-item.labor .cost-icon {
  background: var(--chart-2);
  color: white;
}

.cost-item.overhead .cost-icon {
  background: var(--chart-3);
  color: white;
}

.cost-info {
  flex: 1;
}

.cost-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.938rem;
  margin-bottom: var(--space-1);
}

.cost-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-strong);
  font-feature-settings: 'tnum' 1;
}

.cost-percentage {
  font-size: 0.813rem;
  color: var(--text-muted);
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
