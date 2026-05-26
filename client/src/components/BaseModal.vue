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
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.base-modal-container {
  background: #ffffff;
  border-radius: 12px;
  max-width: 640px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.base-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.base-modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.base-modal-close {
  background: transparent;
  border: none;
  font-size: 1.75rem;
  line-height: 1;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.base-modal-close:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.base-modal-body {
  padding: 1.25rem 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.base-modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.18s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
