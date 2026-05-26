# Design Tokens

The canonical token set for the SaaS redesign. Drop this `:root` block into the global `<style>` block in `App.vue` (or wherever app-wide styles live).

## How to adapt the values

The token _names_ below are fixed — they're what every other CSS reference uses. The token _values_ should be tuned to the existing app's palette so the redesign feels like a polish, not a rebrand:

- If the app already uses a slate/gray scale (typical Tailwind-style `#0f172a` / `#64748b` / `#e2e8f0`), use those values as shown below.
- If the app uses a different palette (e.g., navy/teal, warm grays), substitute equivalents at the same lightness levels. The relationships matter more than the exact hexes.
- The accent color (`--color-accent`) should match the existing primary action color. If unclear, default to a desaturated blue (`#2563eb`).

## Canonical token block

```css
:root {
  /* Color — Surfaces */
  --color-bg-app: #f8fafc; /* page background */
  --color-bg-surface: #ffffff; /* cards, modals */
  --color-bg-sidebar: #ffffff; /* sidebar nav */
  --color-bg-hover: #f1f5f9; /* hover state for rows, links */
  --color-bg-subtle: #f8fafc; /* table headers, inset areas */

  /* Color — Text */
  --color-text-primary: #0f172a; /* headings, body emphasis */
  --color-text-secondary: #334155; /* body text */
  --color-text-muted: #64748b; /* labels, captions, subtext */
  --color-text-inverse: #ffffff; /* text on accent backgrounds */

  /* Color — Borders */
  --color-border: #e2e8f0; /* default dividers, card borders */
  --color-border-strong: #cbd5e1; /* hover/focus borders */

  /* Color — Accent (primary brand) */
  --color-accent: #2563eb;
  --color-accent-hover: #1d4ed8;
  --color-accent-subtle: #eff6ff; /* tinted active-state background */

  /* Color — Semantic */
  --color-success: #059669;
  --color-success-bg: #d1fae5;
  --color-success-text: #065f46;

  --color-warning: #ea580c;
  --color-warning-bg: #fed7aa;
  --color-warning-text: #92400e;

  --color-danger: #dc2626;
  --color-danger-bg: #fecaca;
  --color-danger-text: #991b1b;

  --color-info: #2563eb;
  --color-info-bg: #dbeafe;
  --color-info-text: #1e40af;

  /* Spacing — 4px scale */
  --space-1: 0.25rem; /*  4px */
  --space-2: 0.5rem; /*  8px */
  --space-3: 0.75rem; /* 12px */
  --space-4: 1rem; /* 16px */
  --space-5: 1.25rem; /* 20px */
  --space-6: 1.5rem; /* 24px */
  --space-7: 2rem; /* 32px */
  --space-8: 3rem; /* 48px */

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;

  /* Shadow */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.06);

  /* Typography */
  --font-size-xs: 0.75rem; /* 12px — labels, captions */
  --font-size-sm: 0.875rem; /* 14px — body small, table cells */
  --font-size-md: 0.938rem; /* 15px — body */
  --font-size-lg: 1.125rem; /* 18px — card titles */
  --font-size-xl: 1.375rem; /* 22px — section headings */
  --font-size-2xl: 1.875rem; /* 30px — page headings */
  --font-size-3xl: 2.25rem; /* 36px — stat values */

  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.2;
  --line-height-normal: 1.5;

  /* Layout */
  --sidebar-width: 240px;
  --content-max-width: 1600px;
}
```

## Common substitutions

When tokenizing existing styles, here's the mapping you'll apply most often:

| Hardcoded value             | Token                         |
| --------------------------- | ----------------------------- |
| `#f8fafc` (body bg)         | `var(--color-bg-app)`         |
| `#ffffff` / `white` (cards) | `var(--color-bg-surface)`     |
| `#f1f5f9` (hover bg)        | `var(--color-bg-hover)`       |
| `#0f172a` (heading text)    | `var(--color-text-primary)`   |
| `#334155` (body text)       | `var(--color-text-secondary)` |
| `#64748b` (muted text)      | `var(--color-text-muted)`     |
| `#e2e8f0` (borders)         | `var(--color-border)`         |
| `#cbd5e1` (hover borders)   | `var(--color-border-strong)`  |
| `#2563eb` (accent)          | `var(--color-accent)`         |
| `#eff6ff` (active bg)       | `var(--color-accent-subtle)`  |
| `0.25rem`                   | `var(--space-1)`              |
| `0.5rem`                    | `var(--space-2)`              |
| `0.75rem`                   | `var(--space-3)`              |
| `1rem`                      | `var(--space-4)`              |
| `1.25rem`                   | `var(--space-5)`              |
| `1.5rem`                    | `var(--space-6)`              |
| `2rem`                      | `var(--space-7)`              |
| `3rem`                      | `var(--space-8)`              |
| `6px` (radius)              | `var(--radius-sm)`            |
| `8px` (radius)              | `var(--radius-md)`            |
| `10px` (radius)             | `var(--radius-lg)`            |

## When _not_ to tokenize

- One-off layout values (e.g., a chart axis offset, an absolute-positioned icon). These aren't part of the design system.
- SVG fill/stroke colors inside chart components — they have their own semantic meaning (data series colors), not chrome colors.
- Values inside third-party component overrides — leave the integration boundary clean.

A token registry is only useful if every entry pulls its weight. Polluting it with one-offs makes future work harder.
