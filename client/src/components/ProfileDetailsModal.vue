<template>
  <BaseModal
    :is-open="isOpen"
    :title="t('profileDetails.title')"
    @close="$emit('close')"
  >
    <div class="profile-section">
      <div class="avatar-section">
        <div class="avatar-xl">
          {{ getInitials(currentUser.name) }}
        </div>
        <h4 class="profile-name">{{ currentUser.name }}</h4>
        <p class="profile-job-title">{{ currentUser.jobTitle }}</p>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">{{ t("profileDetails.email") }}</div>
          <div class="info-value">{{ currentUser.email }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">{{ t("profileDetails.department") }}</div>
          <div class="info-value">{{ currentUser.department }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">{{ t("profileDetails.location") }}</div>
          <div class="info-value">{{ currentUser.location }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">{{ t("profileDetails.phone") }}</div>
          <div class="info-value">{{ currentUser.phone }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">{{ t("profileDetails.joinDate") }}</div>
          <div class="info-value">{{ formatDate(currentUser.joinDate) }}</div>
        </div>

        <div class="info-item">
          <div class="info-label">{{ t("profileDetails.employeeId") }}</div>
          <div class="info-value">
            CC-{{ currentUser.id.toString().padStart(5, "0") }}
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button class="btn-secondary" @click="$emit('close')">
        {{ t("profileDetails.close") }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { useAuth } from "../composables/useAuth";
import { useI18n } from "../composables/useI18n";
import BaseModal from "./BaseModal.vue";

const { currentUser, getInitials } = useAuth();
const { t, currentLocale } = useI18n();

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["close"]);

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const locale = currentLocale.value === "ja" ? "ja-JP" : "en-US";
  return date.toLocaleDateString(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};
</script>

<style scoped>
.profile-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-7);
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border);
}

.avatar-xl {
  width: 88px;
  height: 88px;
  border-radius: var(--radius-full);
  background: var(--accent);
  color: var(--text-inverse);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.75rem;
  letter-spacing: 0.025em;
  box-shadow: 0 4px 12px var(--accent-ring);
}

.profile-name {
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-strong);
  margin: 0;
  letter-spacing: -0.02em;
}

.profile-job-title {
  font-size: 0.938rem;
  color: var(--text-muted);
  margin: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
