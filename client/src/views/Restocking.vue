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
  padding: 1.25rem 0 0.5rem;
}

.slider-section {
  margin-bottom: 1.25rem;
}

.slider-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.budget-slider {
  width: 100%;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: #e2e8f0;
  border-radius: 3px;
  outline: none;
  cursor: pointer;
  accent-color: #2563eb;
}

.budget-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 0 0 2px #2563eb, 0 2px 6px rgba(37, 99, 235, 0.3);
  transition: box-shadow 0.2s;
}

.budget-slider::-webkit-slider-thumb:hover {
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2), 0 2px 8px rgba(37, 99, 235, 0.4);
}

.budget-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 0 0 2px #2563eb;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #94a3b8;
}

.budget-display {
  margin-bottom: 1.25rem;
}

.budget-amount {
  font-size: 2rem;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: -0.025em;
  margin-bottom: 0.25rem;
}

.budget-spend-line {
  font-size: 0.875rem;
  color: #64748b;
}

.budget-spend-line strong {
  color: #0f172a;
}

.budget-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.stat-tile {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.875rem 1rem;
  text-align: center;
}

.stat-tile-value {
  font-size: 1.375rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.stat-tile-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 0.25rem;
}

.empty-state {
  padding: 3rem 1.5rem;
  text-align: center;
  color: #64748b;
  font-size: 0.938rem;
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 0 0;
  margin-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.action-bar-left {
  flex: 1;
}

.btn-primary {
  padding: 0.625rem 1.5rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  white-space: nowrap;
}

.btn-primary:hover:not(:disabled) {
  background: #1d4ed8;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.btn-primary:disabled {
  background: #cbd5e1;
  color: #94a3b8;
  cursor: not-allowed;
  box-shadow: none;
}

.success-message {
  font-size: 0.875rem;
  color: #065f46;
  background: #d1fae5;
  border: 1px solid #a7f3d0;
  border-radius: 6px;
  padding: 0.5rem 0.875rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.orders-link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

.orders-link:hover {
  text-decoration: underline;
}

.submit-error {
  font-size: 0.875rem;
  color: #991b1b;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  padding: 0.5rem 0.875rem;
}
</style>
