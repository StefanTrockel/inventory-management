import { onBeforeUnmount, watch } from "vue";

const FOCUSABLE = [
  "a[href]",
  "button:not([disabled])",
  "textarea:not([disabled])",
  'input:not([disabled]):not([type="hidden"])',
  "select:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(",");

export function useModal(isOpenRef, containerRef, onClose) {
  let previouslyFocused = null;

  const focusFirst = () => {
    const el = containerRef.value;
    if (!el) return;
    const target = el.querySelector(FOCUSABLE) || el;
    if (target && typeof target.focus === "function") target.focus();
  };

  const handleKeydown = (event) => {
    if (!isOpenRef.value) return;
    if (event.key === "Escape") {
      event.stopPropagation();
      onClose?.();
      return;
    }
    if (event.key === "Tab" && containerRef.value) {
      const focusables = Array.from(
        containerRef.value.querySelectorAll(FOCUSABLE),
      );
      if (focusables.length === 0) {
        event.preventDefault();
        return;
      }
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      const active = document.activeElement;
      if (event.shiftKey && active === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && active === last) {
        event.preventDefault();
        first.focus();
      }
    }
  };

  const stop = watch(
    isOpenRef,
    (open) => {
      if (open) {
        previouslyFocused = document.activeElement;
        document.addEventListener("keydown", handleKeydown, true);
        document.body.style.overflow = "hidden";
        setTimeout(focusFirst, 0);
      } else {
        document.removeEventListener("keydown", handleKeydown, true);
        document.body.style.overflow = "";
        if (
          previouslyFocused &&
          typeof previouslyFocused.focus === "function"
        ) {
          previouslyFocused.focus();
        }
        previouslyFocused = null;
      }
    },
    { immediate: true },
  );

  onBeforeUnmount(() => {
    document.removeEventListener("keydown", handleKeydown, true);
    document.body.style.overflow = "";
    stop();
  });
}
