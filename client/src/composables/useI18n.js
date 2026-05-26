import { ref, computed } from "vue";
import en from "../locales/en";
import ja from "../locales/ja";

const translations = {
  en,
  ja,
};

function readStoredLocale() {
  try {
    const stored = localStorage.getItem("app-locale");
    return translations[stored] ? stored : "en";
  } catch {
    return "en";
  }
}

const currentLocale = ref(readStoredLocale());

const currentCurrency = computed(() =>
  currentLocale.value === "ja" ? "JPY" : "USD",
);

function resolve(localeKey, keys) {
  let value = translations[localeKey];
  for (const k of keys) {
    if (value && typeof value === "object") {
      value = value[k];
    } else {
      return undefined;
    }
  }
  return typeof value === "string" ? value : undefined;
}

function replacePlaceholders(text, params) {
  return text.replace(/\{(\w+)\}/g, (match, key) =>
    params[key] !== undefined ? params[key] : match,
  );
}

export function useI18n() {
  const t = (key, params = {}) => {
    const keys = key.split(".");
    const primary = resolve(currentLocale.value, keys);
    if (primary !== undefined) return replacePlaceholders(primary, params);
    if (currentLocale.value !== "en") {
      const fallback = resolve("en", keys);
      if (fallback !== undefined) return replacePlaceholders(fallback, params);
    }
    return key;
  };

  const setLocale = (locale) => {
    if (translations[locale]) {
      currentLocale.value = locale;
      try {
        localStorage.setItem("app-locale", locale);
      } catch {
        // ignore (private mode etc.)
      }
    }
  };

  const availableLocales = computed(() => Object.keys(translations));

  const localeName = computed(() => {
    const names = { en: "English", ja: "日本語" };
    return names[currentLocale.value] || currentLocale.value;
  });

  const translateProductName = (productName) => {
    const map = translations[currentLocale.value]?.productNames;
    return (map && map[productName]) || productName;
  };

  const translateCustomerName = (customerName) => {
    const map = translations[currentLocale.value]?.customerNames;
    return (map && map[customerName]) || customerName;
  };

  const translateWarehouse = (warehouseName) => {
    if (currentLocale.value === "ja") {
      const cityMap = {
        "San Francisco": "サンフランシスコ",
        London: "ロンドン",
        Tokyo: "東京",
      };
      if (cityMap[warehouseName]) return cityMap[warehouseName];
      if (warehouseName && warehouseName.startsWith("Warehouse ")) {
        return warehouseName.replace("Warehouse ", "倉庫");
      }
    }
    return warehouseName;
  };

  return {
    t,
    setLocale,
    currentLocale: computed(() => currentLocale.value),
    currentCurrency,
    availableLocales,
    localeName,
    translateProductName,
    translateCustomerName,
    translateWarehouse,
  };
}
