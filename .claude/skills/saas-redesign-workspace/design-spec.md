# Design Spec — "Operations Console"

A refined, light, Linear/Stripe-inspired SaaS aesthetic for the Catalyst Components inventory app. This is the single source of truth. Implement it precisely. The character comes from restraint, hairline borders, generous whitespace, tabular numerics, and a confident indigo accent — NOT from heavy color or ornament.

## Non-negotiables

- **Do not** touch `setup()` logic, refs, computed, lifecycle, routing, or API calls. Layout + CSS + template chrome only.
- **Do not** use the old cliché purple gradient (`#667eea` → `#764ba2`) anywhere. Replace those chart/accent usages with the indigo accent below.
- Keep all routes/nav items 1:1. Don't rename routes.
- Use the exact token names below so the `:root` block (App.vue) and `var()` refs (views) align.

## Typography

Loaded via Google Fonts in `index.html` (handled separately):

- **Manrope** — all UI text, headings, labels, stat values. Distinctive geometric humanist sans, refined, very SaaS. Use weight contrast (400/500/600/700/800) for hierarchy.
- **IBM Plex Mono** — SKUs, order IDs, and other machine codes only. This is a deliberate Stripe-style touch: monospace for identifiers. Do NOT use mono for currency/large numbers.

```css
--font-sans:
  "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-mono: "IBM Plex Mono", "SF Mono", ui-monospace, monospace;
```

- Body uses `--font-sans`.
- Numeric values (stat values, table figures, currency) get `font-feature-settings: 'tnum' 1, 'cv11' 1;` for tabular alignment.
- Headings: tighter letter-spacing (`-0.02em` to `-0.03em`), weight 700–800.
- Uppercase micro-labels (stat labels, table headers, section labels): `font-size: 0.6875rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted);`

## Color tokens (`:root`)

```css
:root {
  /* Canvas & surfaces */
  --bg-app: #fafbfc; /* page canvas — barely-there cool gray */
  --bg-surface: #ffffff; /* cards, sidebar, modals */
  --bg-subtle: #f6f7f9; /* table headers, inset wells, hover fills */
  --bg-hover: #f1f3f5; /* row/nav hover */

  /* Text */
  --text-strong: #0b0f19; /* headings, primary values */
  --text-primary: #1f2733; /* body */
  --text-secondary: #5b6573; /* secondary body, table cells */
  --text-muted: #8a93a2; /* labels, captions, icons-resting */
  --text-inverse: #ffffff;

  /* Borders — hairline, low contrast */
  --border: #e9ebef; /* default dividers, card borders */
  --border-strong: #d7dbe0; /* hover/focus borders */
  --border-faint: #f0f2f4; /* internal table row lines */

  /* Accent — refined indigo (NOT generic #2563eb, NOT purple gradient) */
  --accent: #4f46e5;
  --accent-hover: #4338ca;
  --accent-press: #3730a3;
  --accent-subtle: #eef2ff; /* active-nav tint, focus ring bg */
  --accent-ring: rgba(79, 70, 229, 0.18);

  /* Semantic */
  --success: #0f9d6b;
  --success-bg: #e7f7f0;
  --success-text: #096c4a;
  --warning: #d97706;
  --warning-bg: #fef3e2;
  --warning-text: #92510a;
  --danger: #e11d48;
  --danger-bg: #fdeaee;
  --danger-text: #9f1239;
  --info: #4f46e5;
  --info-bg: #eef2ff;
  --info-text: #3730a3;

  /* Data-viz palette (cohesive with accent) */
  --chart-1: #4f46e5; /* indigo (primary series / accent) */
  --chart-2: #0f9d6b; /* emerald */
  --chart-3: #f59e0b; /* amber */
  --chart-4: #e11d48; /* rose */
  --chart-5: #0ea5e9; /* sky */
  --chart-6: #8b5cf6; /* violet */
  --chart-grid: #eceef1; /* hairline gridlines */
  --chart-axis: #aab2bd; /* axis labels */

  /* Spacing — 4px scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 32px;
  --space-8: 48px;
  --space-9: 64px;

  /* Radius — modern, slightly generous */
  --radius-sm: 7px; /* controls, badges */
  --radius-md: 10px; /* inputs, small cards */
  --radius-lg: 14px; /* cards, panels */
  --radius-xl: 18px; /* feature panels */
  --radius-full: 999px;

  /* Shadows — barely-there, layered. Refined look leans on borders, not shadow. */
  --shadow-xs: 0 1px 2px rgba(13, 18, 28, 0.04);
  --shadow-sm:
    0 1px 3px rgba(13, 18, 28, 0.06), 0 1px 2px rgba(13, 18, 28, 0.04);
  --shadow-md:
    0 4px 12px rgba(13, 18, 28, 0.07), 0 2px 4px rgba(13, 18, 28, 0.04);
  --shadow-lg:
    0 12px 28px rgba(13, 18, 28, 0.1), 0 4px 10px rgba(13, 18, 28, 0.05);

  /* Layout */
  --sidebar-width: 248px;
  --content-max: 1560px;

  /* Motion */
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --dur-fast: 120ms;
  --dur: 180ms;
}
```

## App shell layout

Root `.app` becomes a flex row: `sidebar | main-area`. Sidebar is `position: sticky; top: 0; height: 100vh`, does not scroll with content. Main area scrolls independently and contains the FilterBar (sticky at top of content) then `<router-view>`.

```
┌────────────┬─────────────────────────────────────┐
│ ◳ Brand    │ [FilterBar — sticky]                 │
│            │─────────────────────────────────────│
│ WORKSPACE  │  Page header                         │
│ ▦ Overview │  KPI cards (staggered fade-in)       │
│ ▣ Inventory│  Content cards                       │
│ ⎘ Orders   │                                      │
│            │                                      │
│ INSIGHTS   │                                      │
│ $ Finance  │                                      │
│ ↗ Demand   │                                      │
│ ▤ Reports  │                                      │
│ ─────────  │                                      │
│ 🌐 English │                                      │
│ 👤 Profile │                                      │
└────────────┴─────────────────────────────────────┘
```

### Sidebar structure (App.vue template)

Keep using `t()` for the existing labels. Group nav with section labels. Each nav item = icon + label.

- **Brand block** (top): a small inline-SVG logo mark in accent + company name (`t('nav.companyName')`) in weight 800, and `t('nav.subtitle')` as a tiny muted line under it. Wrap in `<router-link to="/">`.
- **Section "WORKSPACE"**: Overview (`/`), Inventory (`/inventory`), Orders (`/orders`).
- **Section "INSIGHTS"**: Finance (`/spending`), Demand Forecast (`/demand`), Reports (`/reports`).
- **Footer** (bottom, `margin-top:auto`): hairline divider, then `<LanguageSwitcher />` and `<ProfileMenu />`.

### Icons

Use inline `<svg>` line icons, 18×18, `stroke="currentColor" stroke-width="1.75" fill="none" stroke-linecap="round" stroke-linejoin="round"`, so they inherit nav text color. Suggested icons (use simple Lucide-style paths):

- Overview → layout-grid (2×2 squares)
- Inventory → package/box
- Orders → clipboard-list or shopping-cart
- Finance → wallet or dollar-sign
- Demand Forecast → trending-up
- Reports → bar-chart / file-text
- Brand mark → stacked layers / cube glyph in accent

Active nav item (`.router-link-exact-active`): `background: var(--accent-subtle); color: var(--accent);` icon inherits accent; weight 600; a `3px` accent bar on the left via `box-shadow: inset 3px 0 0 var(--accent)` OR border-left. Resting nav: `color: var(--text-secondary)`, icon `--text-muted`. Hover: `background: var(--bg-hover); color: var(--text-strong)`.

### Shell CSS essentials

```css
body {
  font-family: var(--font-sans);
  background: var(--bg-app);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
}
.app {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  background: var(--bg-surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
}
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4) var(--space-3);
}
.nav-section-label {
  /* uppercase micro-label */
  padding: var(--space-4) var(--space-3) var(--space-2);
}
.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-3);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition:
    background var(--dur-fast) var(--ease),
    color var(--dur-fast) var(--ease);
}
.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-strong);
}
.nav-item.router-link-exact-active {
  background: var(--accent-subtle);
  color: var(--accent);
  font-weight: 600;
  box-shadow: inset 3px 0 0 var(--accent);
}
.main-area {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  width: 100%;
  max-width: var(--content-max);
  margin: 0 auto;
  padding: var(--space-7) var(--space-8);
}
```

Remove old `.top-nav`, `.nav-container`, `.logo`, `.nav-tabs`, `.subtitle` rules.

## Components

### Cards (`.card`, content panels)

- `background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-xs); padding: var(--space-6);`
- Hover (on interactive cards only): `border-color: var(--border-strong); box-shadow: var(--shadow-md); transform: translateY(-1px);` with transition.
- `.card-header`: bottom hairline `1px solid var(--border)`, padding-bottom `var(--space-4)`, margin-bottom `var(--space-5)`. Title weight 700, `--text-strong`, letter-spacing -0.01em.

### Stat cards (`.stat-card`)

- Same surface treatment, `--radius-lg`, padding `var(--space-5) var(--space-6)`.
- Label: uppercase micro-label.
- Value: `font-size: 2rem; font-weight: 800; color: var(--text-strong); letter-spacing: -0.03em;` tabular numerals.
- Goal/progress bar: track `height:6px; border-radius:var(--radius-full); background:var(--bg-subtle);` fill in `--accent` (or semantic). Delta text in semantic color, small.
- Staggered entrance: cards fade+rise on load via `@keyframes` + `animation-delay` increments (e.g., 40ms steps). Respect `@media (prefers-reduced-motion: reduce)` → no transform/animation.
- Semantic variants keep their accent only on the value or a small dot, not the whole card.

### Tables

- Header row: `background: var(--bg-subtle);` th = uppercase micro-label, padding `var(--space-3) var(--space-4)`.
- td: padding `var(--space-4)`, `font-size: 0.875rem; color: var(--text-secondary);` row divider `1px solid var(--border-faint)`.
- Row hover: `background: var(--bg-subtle);` clickable rows show `cursor:pointer`.
- SKUs / IDs: wrap in `--font-mono`, `font-size: 0.8125rem; color: var(--text-primary);`.
- Emphasized figures (quantity, total value): weight 600, `--text-strong`, tabular.

### Badges / status pills

- `display:inline-flex; align-items:center; gap:6px; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; letter-spacing: 0.02em;` Capitalize (not all-caps) for a softer modern look — e.g., "In Stock", "Low Stock".
- Optional leading dot (6px circle) in the semantic color.
- Map existing classes: `.success` → success bg/text, `.warning` → warning, `.danger` → danger, `.info` → info; `.increasing`→success, `.decreasing`→danger, `.stable`→info; `.high`→danger, `.medium`→warning, `.low`→info.

### FilterBar

- Container: `background: var(--bg-surface); border-bottom: 1px solid var(--border);` sticky `top:0; z-index:20;` padding `var(--space-4) var(--space-8);` `backdrop-filter: blur(8px); background: rgba(255,255,255,0.85);` for a refined glass effect.
- Filter label: uppercase micro-label.
- Selects & search input: `background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 8px 12px; font: inherit; font-size: 0.875rem; color: var(--text-primary);` Custom chevron for selects (inline SVG background or a wrapper). Focus: `border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ring); outline: none;`
- Search input: leading magnifier icon in `--text-muted`, clear button on the right.

### Charts (SVG)

- Replace hardcoded chart hexes with the `--chart-*` tokens (use `var()` in inline styles where possible, or update the literal hexes to the new values).
  - blue `#3b82f6` → `--chart-1` (#4f46e5)
  - green `#10b981` → `--chart-2` (#0f9d6b)
  - amber `#f59e0b` → `--chart-3` (#f59e0b)
  - red `#ef4444` → `--chart-4` (#e11d48)
  - purple gradient `#667eea/#764ba2` → solid `--chart-1` or an indigo→sky gradient `#4f46e5 → #0ea5e9`
  - violet `#8b5cf6` → `--chart-6`
- Gridlines: `stroke: var(--chart-grid); stroke-width: 1;`
- Axis labels: `--font-sans`, `font-size: 11px; fill: var(--chart-axis);`
- Donut/line/bar fills/strokes use the cohesive palette in series order (chart-1, chart-2, ...).
- Keep chart geometry/data binding untouched — only colors, gridline strokes, label fills.

## Motion (restrained)

- Page content: one staggered fade-rise of the top cards on mount via CSS animation + `animation-delay`. Subtle (8–12px rise, 300–400ms).
- Hover transitions on cards/nav/rows: `var(--dur)`/`var(--dur-fast)` with `var(--ease)`.
- Honor `@media (prefers-reduced-motion: reduce)`.

## Definition of done

- Sidebar with brand mark, two section labels, icon nav, active state, footer affordances.
- All shared components (cards, stat cards, tables, badges, filter bar) refined per above.
- Charts recolored to the cohesive palette; no purple gradient remains.
- SKUs/IDs in mono. Numbers tabular.
- No console errors; all routes render; no horizontal scroll at 1440px.
- Business logic untouched.
