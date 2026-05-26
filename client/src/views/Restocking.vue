<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <!-- Budget Card -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.budget.title') }}</h3>
        </div>

        <div class="budget-body">
          <div class="slider-section">
            <label class="slider-label">{{ t('restocking.budget.setBudget') }}</label>
            <input
              v-model.number="budget"
              type="range"
              min="0"
              max="500000"
              step="10000"
              class="budget-slider"
            />
            <div class="slider-labels">
              <span>$0</span>
              <span>$500,000</span>
            </div>
          </div>

          <div class="budget-display">
            <div class="budget-amount">{{ formatCurrency(budget, 0) }}</div>
            <div class="budget-spend-line">
              {{ t('restocking.budget.recommendedSpend') }}:
              <strong>{{ formatCurrency(totalRecommendedCost, 0) }}</strong>
              {{ t('restocking.budget.of') }}
              {{ formatCurrency(budget, 0) }}
              {{ t('restocking.budget.budget') }}
              <span v-if="budget > 0">({{ budgetUsagePercent }}%)</span>
            </div>
          </div>

          <div class="budget-stats">
            <div class="stat-tile">
              <div class="stat-tile-value">{{ recommendations.length }}</div>
              <div class="stat-tile-label">{{ t('restocking.summary.items') }}</div>
            </div>
            <div class="stat-tile">
              <div class="stat-tile-value">{{ totalUnits.toLocaleString() }}</div>
              <div class="stat-tile-label">{{ t('restocking.summary.units') }}</div>
            </div>
            <div class="stat-tile">
              <div class="stat-tile-value">{{ formatCurrency(totalRecommendedCost, 0) }}</div>
              <div class="stat-tile-label">{{ t('restocking.summary.cost') }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommendations Card -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendations.title') }}</h3>
        </div>

        <div v-if="recommendations.length === 0" class="empty-state">
          {{ t('restocking.recommendations.empty') }}
        </div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restocking.recommendations.sku') }}</th>
                <th>{{ t('restocking.recommendations.item') }}</th>
                <th>{{ t('restocking.recommendations.forecastedDemand') }}</th>
                <th>{{ t('restocking.recommendations.recommendedQty') }}</th>
                <th>{{ t('restocking.recommendations.unitCost') }}</th>
                <th>{{ t('restocking.recommendations.subtotal') }}</th>
                <th>{{ t('restocking.recommendations.leadTime') }}</th>
                <th>{{ t('restocking.recommendations.trend') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rec in recommendations" :key="rec.item_sku">
                <td><strong>{{ rec.item_sku }}</strong></td>
                <td>{{ translateProductName(rec.item_name) }}</td>
                <td>{{ rec.forecasted_demand.toLocaleString() }}</td>
                <td><strong>{{ rec.quantity.toLocaleString() }}</strong></td>
                <td>{{ formatCurrency(rec.unit_cost, 2) }}</td>
                <td><strong>{{ formatCurrency(rec.quantity * rec.unit_cost, 0) }}</strong></td>
                <td>{{ rec.lead_time_days }} {{ t('restocking.recommendations.days') }}</td>
                <td>
                  <span :class="['badge', rec.trend]">
                    {{ t(`trends.${rec.trend}`) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Action Bar -->
        <div class="action-bar">
          <div class="action-bar-left">
            <div v-if="orderSuccess" class="success-message">
              {{ t('restocking.success.submitted') }} — Order #{{ submittedOrderId }}
              &mdash; {{ t('restocking.success.expectedDelivery') }}: {{ expectedDeliveryDate }}
              &nbsp;
              <router-link to="/orders" class="orders-link">{{ t('restocking.success.viewOrders') }}</router-link>
            </div>
            <div v-if="submitError" class="submit-error">{{ t('restocking.error') }}</div>
          </div>
          <button
            class="btn-primary"
            :disabled="recommendations.length === 0 || submitting"
            @click="placeOrder"
          >
            {{ submitting ? t('restocking.submitting') : t('restocking.placeOrder') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'Restocking',
  setup() {
    const { t, translateProductName } = useI18n()

    const loading = ref(true)
    const error = ref(null)
    const forecasts = ref([])

    const budget = ref(100000)

    const submitting = ref(false)
    const submitError = ref(null)
    const orderSuccess = ref(false)
    const submittedOrderId = ref('')
    const expectedDeliveryDate = ref('')

    const loadForecasts = async () => {
      loading.value = true
      error.value = null
      try {
        forecasts.value = await api.getDemandForecasts()
      } catch (err) {
        error.value = 'Failed to load demand forecasts: ' + err.message
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    // Recommendation algorithm: sort by forecasted_demand descending, walk and fill budget
    const recommendations = computed(() => {
      if (budget.value <= 0 || forecasts.value.length === 0) return []

      const sorted = forecasts.value.slice().sort((a, b) => b.forecasted_demand - a.forecasted_demand)
      let remaining = budget.value
      const result = []

      for (const forecast of sorted) {
        if (remaining <= 0) break
        if (!forecast.unit_cost || forecast.unit_cost <= 0) continue

        let units = forecast.forecasted_demand
        if (units * forecast.unit_cost <= remaining) {
          // Full forecast fits
        } else {
          // Partial: as many as we can afford
          units = Math.floor(remaining / forecast.unit_cost)
        }

        if (units < 1) continue

        remaining -= units * forecast.unit_cost
        result.push({
          item_sku: forecast.item_sku,
          item_name: forecast.item_name,
          forecasted_demand: forecast.forecasted_demand,
          quantity: units,
          unit_cost: forecast.unit_cost,
          lead_time_days: forecast.lead_time_days,
          trend: forecast.trend
        })
      }

      return result
    })

    const totalRecommendedCost = computed(() => {
      return recommendations.value.reduce((sum, r) => sum + r.quantity * r.unit_cost, 0)
    })

    const totalUnits = computed(() => {
      return recommendations.value.reduce((sum, r) => sum + r.quantity, 0)
    })

    const budgetUsagePercent = computed(() => {
      if (budget.value <= 0) return 0
      return Math.round((totalRecommendedCost.value / budget.value) * 100)
    })

    const formatCurrency = (value, fractionDigits) => {
      return value.toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: fractionDigits,
        minimumFractionDigits: fractionDigits
      })
    }

    const placeOrder = async () => {
      if (recommendations.value.length === 0) return

      submitting.value = true
      submitError.value = null
      orderSuccess.value = false

      const items = recommendations.value.map(r => ({
        item_sku: r.item_sku,
        item_name: r.item_name,
        quantity: r.quantity,
        unit_cost: r.unit_cost,
        lead_time_days: r.lead_time_days
      }))

      try {
        const response = await api.submitRestockingOrder(items)
        const orderId = response.order_id || response.id || `RST-${Date.now()}`
        submittedOrderId.value = orderId

        // Expected delivery: max lead time from recommendations
        const maxLeadDays = Math.max(...recommendations.value.map(r => r.lead_time_days || 0))
        const deliveryDate = new Date()
        deliveryDate.setDate(deliveryDate.getDate() + maxLeadDays)
        expectedDeliveryDate.value = deliveryDate.toISOString().slice(0, 10)

        orderSuccess.value = true
      } catch (err) {
        submitError.value = err.message
        console.error(err)
      } finally {
        submitting.value = false
      }
    }

    onMounted(loadForecasts)

    return {
      t,
      translateProductName,
      loading,
      error,
      budget,
      recommendations,
      totalRecommendedCost,
      totalUnits,
      budgetUsagePercent,
      formatCurrency,
      submitting,
      submitError,
      orderSuccess,
      submittedOrderId,
      expectedDeliveryDate,
      placeOrder
    }
  }
}
</script>

<style scoped>
.budget-body {
  padding: var(--space-5) 0 var(--space-2);
}

.slider-section {
  margin-bottom: var(--space-5);
}

.slider-label {
  display: block;
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: var(--space-3);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.budget-slider {
  width: 100%;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: var(--border);
  border-radius: var(--radius-full);
  outline: none;
  cursor: pointer;
  accent-color: var(--accent);
}

.budget-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 0 0 2px var(--accent), var(--shadow-sm);
  transition: box-shadow var(--dur-fast) var(--ease);
}

.budget-slider::-webkit-slider-thumb:hover {
  box-shadow: 0 0 0 3px var(--accent-ring), var(--shadow-sm);
}

.budget-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 0 0 2px var(--accent);
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: var(--space-1);
  font-size: 0.75rem;
  color: var(--text-muted);
}

.budget-display {
  margin-bottom: var(--space-5);
}

.budget-amount {
  font-size: 2rem;
  font-weight: 800;
  color: var(--accent);
  letter-spacing: -0.03em;
  margin-bottom: var(--space-1);
  font-feature-settings: 'tnum' 1;
}

.budget-spend-line {
  font-size: 0.875rem;
  color: var(--text-muted);
}

.budget-spend-line strong {
  color: var(--text-primary);
  font-weight: 600;
}

.budget-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border);
}

.stat-tile {
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-4);
  text-align: center;
}

.stat-tile-value {
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-strong);
  letter-spacing: -0.025em;
  font-feature-settings: 'tnum' 1;
}

.stat-tile-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: var(--space-1);
}

.empty-state {
  padding: var(--space-8) var(--space-6);
  text-align: center;
  color: var(--text-muted);
  font-size: 0.938rem;
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-4) 0 0;
  margin-top: var(--space-4);
  border-top: 1px solid var(--border);
}

.action-bar-left {
  flex: 1;
}

.btn-primary {
  padding: var(--space-3) var(--space-6);
  background: var(--accent);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  font-family: var(--font-sans);
  transition: background var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease);
  white-space: nowrap;
}

.btn-primary:hover:not(:disabled) {
  background: var(--accent-hover);
  box-shadow: var(--shadow-sm);
}

.btn-primary:disabled {
  background: var(--border-strong);
  color: var(--text-muted);
  cursor: not-allowed;
  box-shadow: none;
}

.success-message {
  font-size: 0.875rem;
  color: var(--success-text);
  background: var(--success-bg);
  border: 1px solid var(--success);
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-4);
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.orders-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
}

.orders-link:hover {
  text-decoration: underline;
}

.submit-error {
  font-size: 0.875rem;
  color: var(--danger-text);
  background: var(--danger-bg);
  border: 1px solid var(--danger);
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-4);
}

/* SKU mono in table */
.table-container td:first-child strong {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--text-primary);
  white-space: nowrap;
}
</style>
