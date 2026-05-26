---
name: saas-redesign
description: Redesigns a Vue 3 + Composition API application's UI into a modern SaaS-style interface — converts top navigation bars into a vertical left sidebar, introduces a CSS-variable design token system, and applies consistent spacing/typography to produce a polished professional look. Use this skill whenever the user wants to "modernize", "redesign", "polish", "refresh", "give a SaaS look to", "move the nav to the sidebar", or "improve the layout" of a Vue 3 frontend, even if they don't say the word "SaaS" outright. Layout + tokens only — does not rewrite component logic, routing, or data flow.
---

# SaaS Redesign for Vue 3

Transform a Vue 3 (Composition API) application's chrome from a top-nav layout into a modern SaaS layout with a vertical left sidebar, driven by a CSS-variable design token system. The goal is a layout-and-styling pass that feels deliberate and consistent — not a rewrite of business logic.

## When to use

Trigger this skill when the user wants the frontend to feel more like a polished SaaS product. Common phrasings:

- "Redesign the UI", "modernize the layout", "give it a SaaS look"
- "Move the navigation to the left/sidebar"
- "Apply a design system", "use design tokens", "make spacing consistent"
- "It looks dated / amateur / clunky"

If the user only wants to tweak one screen, don't trigger this — this skill makes a coordinated, app-wide change.

## What this skill does and does not touch

**Touches:**

- `App.vue` shell (template + global `<style>`)
- Top-level layout structure (sidebar + main content)
- CSS in any view/component that uses hardcoded colors or spacing the skill is tokenizing
- `FilterBar.vue` placement (moved into main content area if it was a separate bar)

**Does not touch:**

- Component setup() logic, refs, computed properties, lifecycle hooks
- Router configuration, API calls, composables, data fetching
- Vue templates, except for `App.vue`'s shell and class renames forced by CSS changes
- Tests, build config, package.json

If you find yourself editing `script` blocks for reasons other than `App.vue`'s nav state (e.g., `sidebarCollapsed` ref), stop — that's out of scope.

## Workflow

### Step 1 — Read the current state

Before changing anything, build a quick model of the app:

1. Read `client/src/App.vue` end-to-end. Note the top-nav structure: logo, nav links, any extras (profile menu, language switcher, search, etc.).
2. List view files in `client/src/views/` and skim each one's `<style>` block (or any global styles in `App.vue`) to identify hardcoded values that will recur in the tokenization pass.
3. Note if there is a `FilterBar` or similar sub-header — it needs to be re-placed under the new layout.

You're not exhaustively cataloguing — you want enough context to know which hardcoded colors and spacings are common enough to be worth turning into tokens. Five minutes of reading saves an hour of cleanup.

### Step 2 — Install the design tokens

Add a `:root` block at the top of `App.vue`'s global `<style>` (or create one if the styles are scoped). The exact token set lives in `references/design-tokens.md` — read that file before writing tokens, because it includes naming rationale and the full canonical list.

The token system has five families:

- **Color** (`--color-*`) — surfaces, text, borders, accent, semantic (success/warning/danger/info)
- **Spacing** (`--space-*`) — a 4px scale from `--space-1` (4px) to `--space-8` (64px)
- **Radius** (`--radius-*`) — sm / md / lg
- **Shadow** (`--shadow-*`) — sm / md
- **Typography** (`--font-size-*`, `--font-weight-*`, `--line-height-*`)

**Preserve the existing color palette where possible.** If the app already uses slate/gray (e.g., `#0f172a`, `#64748b`, `#e2e8f0`), make those the values of the tokens — don't redesign the palette. The user wants consistency, not a new look from scratch.

### Step 3 — Build the sidebar

Replace the top-nav in `App.vue` with a vertical sidebar. The full template (HTML + CSS) is in `references/sidebar-template.md` — adapt it to the app's actual nav items. Key structural points:

- App root becomes a flex row: `sidebar | main`
- Sidebar is fixed width (240px default), full viewport height, scrollable if nav overflows
- Logo/brand sits at the top of the sidebar (replaces the horizontal logo + subtitle)
- Nav links stack vertically, with active state shown by a left border accent + tinted background
- Any "user/profile/settings" affordances move to the bottom of the sidebar
- The main content area scrolls independently — sidebar stays put

Existing nav links should map one-to-one. Don't rename routes, don't reorder. Use the existing `router-link` calls, just restyled and re-positioned.

### Step 4 — Re-place the FilterBar (if present)

If the app has a global `FilterBar` (or any sub-header) that previously sat below the top-nav, it now lives inside the main content area, above `<router-view />`. It should sit flush at the top of the content scroll area, with the same horizontal padding as the rest of the page. Treat it as part of the page content, not part of the app chrome.

### Step 5 — Tokenize global styles

Now go through the global styles in `App.vue` (the shared classes — `.page-header`, `.card`, `.stat-card`, `.badge`, `.table-container`, etc.) and replace hardcoded colors and spacings with token references.

Replacement strategy:

- Map each unique hardcoded color in the file to its token (most will land on `--color-bg-app`, `--color-bg-surface`, `--color-border`, `--color-text-primary`, `--color-text-secondary`, `--color-text-muted`, `--color-accent`).
- Map each unique spacing value (`0.25rem`, `0.5rem`, `0.75rem`, `1rem`, `1.25rem`, `1.5rem`, `2rem`, `2.5rem`, `3rem`) to its closest `--space-*` token. Snap to the scale — don't preserve oddities like `0.313rem`. Consistency is the whole point.
- Border radius values (`6px`, `8px`, `10px`) collapse to `--radius-sm`, `--radius-md`, `--radius-lg`.

### Step 6 — Tokenize view-level styles

For each `.vue` file in `client/src/views/` (and any components with scoped styles that contain the same hardcoded values), apply the same substitution. Focus only on values that map cleanly to a token. Don't refactor layout, don't restructure SVG charts, don't change class names. If a value is one-off and doesn't have a clean token match, leave it alone — forcing a token where one doesn't fit makes the system worse, not better.

### Step 7 — Verify

After the changes:

1. Start the dev server (`cd client && npm run dev`) and open `http://localhost:3000`.
2. Click through every route. Confirm: sidebar renders, active state shows on the current route, content fills the rest of the viewport, filter bar (if present) sits at the top of the content, no horizontal scroll on a normal laptop viewport.
3. Take a screenshot of at least 2-3 routes for the user to review.
4. Note in your final message: which tokens were introduced, what mapped to what, anything left as-is and why.

If anything is broken — content overflowing, sidebar overlapping content, route highlight not working — fix it before reporting done. A half-redesigned app is worse than the original.

## Design principles to keep in mind

These aren't checklists — they're the _why_ behind the rules above. When you hit an ambiguous case, fall back to these.

- **Consistency beats novelty.** A SaaS look isn't about being clever; it's about the same spacing, the same border, the same hover state every time. If something has to be unique, it should be unique for a reason.
- **Breathing room.** Tight, dense layouts read as amateur. Default to generous padding inside cards (`--space-4` minimum), comfortable line-heights, and clear separation between sections.
- **Quiet color, loud hierarchy.** Backgrounds and borders should be muted; type weight and size should do most of the visual work. The accent color is for one or two things per screen — the active nav item, primary actions — not decoration.
- **One source of truth.** All shared values come from `:root`. If you find yourself writing `color: #64748b` for the third time, that's a token waiting to be used (or to exist).

## Output

When done, give the user:

1. A one-paragraph summary of what changed (sidebar added, N tokens introduced, M files touched).
2. Screenshots of at least 2 routes if you ran the dev server.
3. A bullet list of any visual decisions that might warrant review (e.g., "kept the existing slate palette rather than rebranding", "left chart colors as-is — they don't fit the token system cleanly").

Don't write a long retrospective — keep it tight.
