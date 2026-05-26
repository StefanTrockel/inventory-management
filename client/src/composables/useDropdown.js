import { ref, onBeforeUnmount } from "vue";

export function useDropdown() {
  const isOpen = ref(false);
  const containerEl = ref(null);

  const handleDocumentMousedown = (event) => {
    if (!containerEl.value) return;
    if (!containerEl.value.contains(event.target)) {
      isOpen.value = false;
    }
  };

  const handleKeydown = (event) => {
    if (event.key === "Escape") {
      isOpen.value = false;
    }
  };

  const open = () => {
    if (isOpen.value) return;
    isOpen.value = true;
    document.addEventListener("mousedown", handleDocumentMousedown, true);
    document.addEventListener("keydown", handleKeydown, true);
  };

  const close = () => {
    if (!isOpen.value) return;
    isOpen.value = false;
    document.removeEventListener("mousedown", handleDocumentMousedown, true);
    document.removeEventListener("keydown", handleKeydown, true);
  };

  const toggle = () => {
    if (isOpen.value) close();
    else open();
  };

  onBeforeUnmount(() => {
    document.removeEventListener("mousedown", handleDocumentMousedown, true);
    document.removeEventListener("keydown", handleKeydown, true);
  });

  return { isOpen, containerEl, open, close, toggle };
}
