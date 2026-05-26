import { ref, computed } from "vue";

const selectedPeriod = ref("all");
const selectedLocation = ref("all");
const selectedCategory = ref("all");
const selectedStatus = ref("all");

export const FILTER_KEYS = ["period", "location", "category", "status"];

export function resetFilters() {
  selectedPeriod.value = "all";
  selectedLocation.value = "all";
  selectedCategory.value = "all";
  selectedStatus.value = "all";
}

export function useFilters() {
  const hasActiveFilters = computed(
    () =>
      selectedPeriod.value !== "all" ||
      selectedLocation.value !== "all" ||
      selectedCategory.value !== "all" ||
      selectedStatus.value !== "all",
  );

  const getCurrentFilters = () => {
    const filters = {};
    if (selectedLocation.value !== "all")
      filters.warehouse = selectedLocation.value;
    if (selectedCategory.value !== "all")
      filters.category = selectedCategory.value;
    if (selectedStatus.value !== "all") filters.status = selectedStatus.value;
    if (selectedPeriod.value !== "all") filters.month = selectedPeriod.value;
    return filters;
  };

  return {
    selectedPeriod,
    selectedLocation,
    selectedCategory,
    selectedStatus,
    hasActiveFilters,
    resetFilters,
    getCurrentFilters,
  };
}
