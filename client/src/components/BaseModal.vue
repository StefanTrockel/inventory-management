<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="base-modal-overlay"
        @click.self="$emit('close')"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="titleId"
      >
        <div
          ref="containerEl"
          class="base-modal-container"
          :class="containerClass"
          tabindex="-1"
        >
          <header v-if="$slots.header || title" class="base-modal-header">
            <slot name="header">
              <h2 :id="titleId" class="base-modal-title">{{ title }}</h2>
            </slot>
            <button
              v-if="showClose"
              class="base-modal-close"
              type="button"
              :aria-label="closeLabel"
              @click="$emit('close')"
            >
              ×
            </button>
          </header>
          <div class="base-modal-body" :class="bodyClass">
            <slot />
          </div>
          <footer v-if="$slots.footer" class="base-modal-footer">
            <slot name="footer" />
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
import { ref, toRef, computed } from "vue";
import { useModal } from "../composables/useModal";

let nextId = 0;

export default {
  name: "BaseModal",
  props: {
    isOpen: { type: Boolean, required: true },
    title: { type: String, default: "" },
    showClose: { type: Boolean, default: true },
    closeLabel: { type: String, default: "Close" },
    containerClass: { type: String, default: "" },
    bodyClass: { type: String, default: "" },
  },
  emits: ["close"],
  setup(props, { emit }) {
    const containerEl = ref(null);
    const titleId = computed(() => `base-modal-title-${++nextId}`);
    useModal(toRef(props, "isOpen"), containerEl, () => emit("close"));
    return { containerEl, titleId };
  },
};
</script>

<style scoped>
.base-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(11, 15, 25, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-4);
}

.base-modal-container {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  max-width: 640px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.base-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--border);
}

.base-modal-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-strong);
  margin: 0;
  letter-spacing: -0.02em;
}

.base-modal-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: background var(--dur-fast) var(--ease), color var(--dur-fast) var(--ease);
}

.base-modal-close:hover {
  background: var(--bg-hover);
  color: var(--text-strong);
}

.base-modal-body {
  padding: var(--space-6);
  overflow-y: auto;
  flex: 1;
}

.base-modal-footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--border);
  background: var(--bg-subtle);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity var(--dur) var(--ease);
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
