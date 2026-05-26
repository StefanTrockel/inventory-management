# Sidebar Template

The HTML structure and CSS for the vertical left sidebar. Adapt — don't copy verbatim — to fit the app's actual nav items, branding, and any existing affordances (profile menu, language switcher, etc.) that need to live in the chrome.

## Layout philosophy

The app shell becomes a **two-column flex row**:

```
┌──────────┬──────────────────────────────────┐
│          │                                  │
│ Sidebar  │  Main content                    │
│ (240px)  │  (fills remaining width)         │
│          │                                  │
│  Logo    │  ┌─ FilterBar (if present) ─┐    │
│          │  │                          │    │
│  Nav     │  └──────────────────────────┘    │
│  links   │                                  │
│          │  ┌─ <router-view />          ─┐  │
│          │  │                            │  │
│  ──────  │  │                            │  │
│  User /  │  │                            │  │
│  Locale  │  └────────────────────────────┘  │
└──────────┴──────────────────────────────────┘
```

The sidebar is sticky/fixed-height (`100vh`) and **does not scroll with the page** — the main content area scrolls independently. The user/locale affordances live at the bottom of the sidebar via `margin-top: auto` on a flex column.

## App.vue template

Replace the existing `<header class="top-nav">...</header>` and surrounding structure with this layout. The `router-link` calls stay identical — only the wrapping and styling change.

```vue
<template>
  <div class="app">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <h1 class="brand-name">{{ t("nav.companyName") }}</h1>
        <span class="brand-subtitle">{{ t("nav.subtitle") }}</span>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item">
          {{ t("nav.overview") }}
        </router-link>
        <router-link to="/inventory" class="nav-item">
          {{ t("nav.inventory") }}
        </router-link>
        <router-link to="/orders" class="nav-item">
          {{ t("nav.orders") }}
        </router-link>
        <router-link to="/spending" class="nav-item">
          {{ t("nav.finance") }}
        </router-link>
        <router-link to="/demand" class="nav-item">
          {{ t("nav.demandForecast") }}
        </router-link>
        <router-link to="/reports" class="nav-item"> Reports </router-link>
      </nav>

      <div class="sidebar-footer">
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>

    <div class="main-area">
      <FilterBar />
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <!-- Modals stay outside the layout flow -->
    <ProfileDetailsModal ... />
    <TasksModal ... />
  </div>
</template>
```

**Note on active state:** Vue Router automatically adds `router-link-active` and `router-link-exact-active` classes. The CSS below targets `.router-link-exact-active` so the active styling appears without any binding logic. The previous `:class="{ active: $route.path === '/' }"` is no longer needed and should be removed.

## CSS for the shell

Replace the existing `.top-nav`, `.nav-container`, `.logo`, `.nav-tabs`, and `.main-content` rules with these. Keep everything else (cards, badges, tables) — those are tokenized separately.

```css
.app {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg-app);
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  background: var(--color-bg-sidebar);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
}

.sidebar-brand {
  padding: var(--space-6) var(--space-5) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.brand-name {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  letter-spacing: -0.025em;
  line-height: var(--line-height-tight);
}

.brand-subtitle {
  display: block;
  margin-top: var(--space-1);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-regular);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: var(--space-4) var(--space-3);
  gap: var(--space-1);
  flex: 1;
  overflow-y: auto;
}

.nav-item {
  display: block;
  padding: var(--space-3) var(--space-4);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
  border-radius: var(--radius-sm);
  transition:
    background 0.15s ease,
    color 0.15s ease;
  border-left: 3px solid transparent;
  margin-left: -3px;
}

.nav-item:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.nav-item.router-link-exact-active {
  color: var(--color-accent);
  background: var(--color-accent-subtle);
  border-left-color: var(--color-accent);
  font-weight: var(--font-weight-semibold);
}

.sidebar-footer {
  padding: var(--space-4) var(--space-3);
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

/* Main area */
.main-area {
  flex: 1;
  min-width: 0; /* prevents flex children from forcing horizontal scroll */
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: var(--space-6) var(--space-7);
  max-width: var(--content-max-width);
  width: 100%;
  margin: 0 auto;
}
```

## Adaptation notes

- **If the sidebar has more than ~8 items**, group them with `<div class="nav-section">` blocks separated by a heading or subtle divider. Don't let the nav scroll if you can avoid it.
- **If the brand area should also be clickable** (link to home), wrap `.sidebar-brand` in a `<router-link to="/">` and reset its text-decoration.
- **For dark mode**, the same token names work — just override the values inside `@media (prefers-color-scheme: dark)` or a `.dark` class. Don't introduce a separate token set.
- **Mobile**: This template assumes a desktop SaaS context. If responsive is in scope, add a `@media (max-width: 768px)` rule that collapses the sidebar to an icon rail or hides it behind a hamburger — but only if the user asked for it. Don't preemptively add complexity.

## Removing the old top-nav styles

After applying the new shell, delete these rules from the existing styles (they're now dead code):

- `.top-nav`, `.nav-container`, `.logo`, `.logo h1`, `.subtitle`
- `.nav-tabs`, `.nav-tabs a`, `.nav-tabs a:hover`, `.nav-tabs a.active`, `.nav-tabs a.active::after`

Leave the rest of the global styles in place — they're tokenized in the next step, not replaced.
