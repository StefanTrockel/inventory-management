const ISO_DATE_RE = /^\d{4}-\d{2}-\d{2}/;

export function parseISO(value) {
  if (!value || typeof value !== "string") return null;
  const d = new Date(value);
  return Number.isFinite(d.getTime()) ? d : null;
}

export function getYearMonthFromISO(value) {
  if (!value || typeof value !== "string") return null;
  return ISO_DATE_RE.test(value) ? value.slice(0, 7) : null;
}

export function getMonthFromISO(value) {
  if (!value || typeof value !== "string" || !ISO_DATE_RE.test(value))
    return null;
  const m = parseInt(value.slice(5, 7), 10);
  return Number.isFinite(m) ? m - 1 : null;
}

export function compareISO(a, b) {
  const sa = typeof a === "string" ? a : "";
  const sb = typeof b === "string" ? b : "";
  if (sa < sb) return -1;
  if (sa > sb) return 1;
  return 0;
}

export function diffCalendarDays(from, to) {
  const a = from instanceof Date ? from : parseISO(from);
  const b = to instanceof Date ? to : parseISO(to);
  if (!a || !b) return null;
  const utcA = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
  const utcB = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());
  return Math.round((utcB - utcA) / 86400000);
}

export function formatDateShort(value, locale = "en") {
  const d = parseISO(value);
  if (!d) return "—";
  const bcp47 = locale === "ja" ? "ja-JP" : "en-US";
  return d.toLocaleDateString(bcp47, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function formatYearMonth(value, locale = "en") {
  const ym =
    getYearMonthFromISO(value) || (typeof value === "string" ? value : null);
  if (!ym) return "—";
  const [y, m] = ym.split("-").map((n) => parseInt(n, 10));
  if (!Number.isFinite(y) || !Number.isFinite(m)) return "—";
  const d = new Date(Date.UTC(y, m - 1, 1));
  const bcp47 = locale === "ja" ? "ja-JP" : "en-US";
  return d.toLocaleDateString(bcp47, {
    year: "numeric",
    month: "short",
    timeZone: "UTC",
  });
}
