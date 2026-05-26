const USD_TO_JPY = 150;

function coerceFinite(amount) {
  const n = Number(amount);
  return Number.isFinite(n) ? n : 0;
}

export function formatCurrency(amount, currency = "USD") {
  const n = coerceFinite(amount);
  if (currency === "JPY") {
    const yenAmount = Math.round(n * USD_TO_JPY);
    return `¥${yenAmount.toLocaleString("ja-JP")}`;
  }
  return `$${n.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
}

export function formatCurrencyWithDecimals(
  amount,
  currency = "USD",
  decimals = 0,
) {
  const n = coerceFinite(amount);
  if (currency === "JPY") {
    const yenAmount = n * USD_TO_JPY;
    return `¥${yenAmount.toLocaleString("ja-JP", { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}`;
  }
  return `$${n.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}`;
}

export function convertAmount(amount, currency = "USD") {
  const n = coerceFinite(amount);
  if (currency === "JPY") {
    return Math.round(n * USD_TO_JPY);
  }
  return n;
}

export function currencySymbol(currency = "USD") {
  return currency === "JPY" ? "¥" : "$";
}
