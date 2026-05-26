<template>
  <div class="app">
    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- Brand block -->
      <router-link to="/" class="sidebar-brand">
        <div class="brand-mark">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="16" width="8" height="8" rx="2" fill="var(--accent)" opacity="0.9"/>
            <rect x="10" y="10" width="8" height="8" rx="2" fill="var(--accent)" opacity="0.65"/>
            <rect x="16" y="4" width="8" height="8" rx="2" fill="var(--accent)" opacity="0.4"/>
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-name">{{ t('nav.companyName') }}</span>
          <span class="brand-subtitle">{{ t('nav.subtitle') }}</span>
        </div>
      </router-link>

      <!-- Nav -->
      <nav class="sidebar-nav">
        <div class="nav-section-label">Workspace</div>

        <router-link to="/" class="nav-item" exact>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="6" height="6" rx="1"/>
            <rect x="10" y="2" width="6" height="6" rx="1"/>
            <rect x="2" y="10" width="6" height="6" rx="1"/>
            <rect x="10" y="10" width="6" height="6" rx="1"/>
          </svg>
          {{ t('nav.overview') }}
        </router-link>

        <router-link to="/inventory" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 2L16 5.5V12.5L9 16L2 12.5V5.5L9 2Z"/>
            <path d="M9 2V16"/>
            <path d="M2 5.5L9 9L16 5.5"/>
          </svg>
          {{ t('nav.inventory') }}
        </router-link>

        <router-link to="/orders" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2H5C4.44772 2 4 2.44772 4 3V15C4 15.5523 4.44772 16 5 16H13C13.5523 16 14 15.5523 14 15V3C14 2.44772 13.5523 2 13 2Z"/>
            <path d="M7 6H11"/>
            <path d="M7 9H11"/>
            <path d="M7 12H9"/>
          </svg>
          {{ t('nav.orders') }}
        </router-link>

        <router-link to="/restocking" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 9a6 6 0 0 1-6 6c-2.21 0-4.14-1.19-5.2-2.97"/>
            <path d="M3 9a6 6 0 0 1 6-6c2.21 0 4.14 1.19 5.2 2.97"/>
            <polyline points="1,11.5 3,9 5,11.5"/>
            <polyline points="17,6.5 15,9 13,6.5"/>
          </svg>
          {{ t('nav.restocking') }}
        </router-link>

        <div class="nav-section-label nav-section-label--spaced">Insights</div>

        <router-link to="/demand" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="2,13 6,9 9,11 14,5"/>
            <polyline points="11,5 14,5 14,8"/>
          </svg>
          {{ t('nav.demandForecast') }}
        </router-link>

        <router-link to="/spending" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="9" r="7"/>
            <path d="M9 5.5V9"/>
            <path d="M6.5 7.5C6.5 6.67 7.17 6 8 6H10C10.83 6 11.5 6.67 11.5 7.5C11.5 8.33 10.83 9 10 9H8C7.17 9 6.5 9.67 6.5 10.5C6.5 11.33 7.17 12 8 12H11.5"/>
            <path d="M9 12V12.5"/>
          </svg>
          {{ t('nav.finance') }}
        </router-link>

        <router-link to="/reports" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="14" height="14" rx="2"/>
            <path d="M6 10V13"/>
            <path d="M9 7V13"/>
            <path d="M12 5V13"/>
          </svg>
          {{ t('nav.reports') }}
        </router-link>

        <router-link to="/backlog" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="9" r="7"/>
            <polyline points="9,5 9,9 12,11"/>
          </svg>
          {{ t('nav.backlog') }}
        </router-link>
      </nav>

      <!-- Footer -->
      <div class="sidebar-footer">
        <div class="sidebar-divider"></div>
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>

    <!-- Main area -->
    <div class="main-area">
      <FilterBar />
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { api } from "./api";
import { useAuth } from "./composables/useAuth";
import { useI18n } from "./composables/useI18n";
import FilterBar from "./components/FilterBar.vue";
import ProfileMenu from "./components/ProfileMenu.vue";
import ProfileDetailsModal from "./components/ProfileDetailsModal.vue";
import TasksModal from "./components/TasksModal.vue";
import LanguageSwitcher from "./components/LanguageSwitcher.vue";

export default {
  name: "App",
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher,
  },
  setup() {
    const {
      currentUser,
      addUserTask,
      removeUserTask,
      toggleUserTask,
      hasUserTask,
    } = useAuth();
    const { t } = useI18n();
    const showProfileDetails = ref(false);
    const showTasks = ref(false);
    const apiTasks = ref([]);

    const tasks = computed(() => {
      const userTasks = currentUser.value.tasks.map((task) => ({
        ...task,
        source: task.source || "mock",
      }));
      const api = apiTasks.value.map((task) => ({ ...task, source: "api" }));
      return [...userTasks, ...api];
    });

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks();
      } catch (err) {
        if (err?.status !== 404) {
          console.error("Failed to load tasks:", err);
        }
      }
    };

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData);
        apiTasks.value.unshift(newTask);
      } catch (err) {
        if (err?.status === 404) {
          addUserTask(taskData);
        } else {
          console.error("Failed to add task:", err);
        }
      }
    };

    const deleteTask = async (task) => {
      const id = typeof task === "object" ? task.id : task;
      const source =
        typeof task === "object"
          ? task.source
          : hasUserTask(id)
            ? "mock"
            : "api";
      if (source === "mock") {
        removeUserTask(id);
        return;
      }
      try {
        await api.deleteTask(id);
        apiTasks.value = apiTasks.value.filter((t) => t.id !== id);
      } catch (err) {
        console.error("Failed to delete task:", err);
      }
    };

    const toggleTask = async (task) => {
      const id = typeof task === "object" ? task.id : task;
      const source =
        typeof task === "object"
          ? task.source
          : hasUserTask(id)
            ? "mock"
            : "api";
      if (source === "mock") {
        toggleUserTask(id);
        return;
      }
      try {
        const updated = await api.toggleTask(id);
        const index = apiTasks.value.findIndex((t) => t.id === id);
        if (index !== -1) apiTasks.value[index] = updated;
      } catch (err) {
        console.error("Failed to toggle task:", err);
      }
    };

    onMounted(loadTasks);

    return {
      t,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask,
    };
  },
};
</script>

<style>
/* ─── Reset ─────────────────────────────────────────────── */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ─── Design tokens ──────────────────────────────────────── */
:root {
  /* Canvas & surfaces */
  --bg-app: #fafbfc;
  --bg-surface: #ffffff;
  --bg-subtle: #f6f7f9;
  --bg-hover: #f1f3f5;

  /* Text */
  --text-strong: #0b0f19;
  --text-primary: #1f2733;
  --text-secondary: #5b6573;
  --text-muted: #8a93a2;
  --text-inverse: #ffffff;

  /* Borders */
  --border: #e9ebef;
  --border-strong: #d7dbe0;
  --border-faint: #f0f2f4;

  /* Accent — refined indigo */
  --accent: #4f46e5;
  --accent-hover: #4338ca;
  --accent-press: #3730a3;
  --accent-subtle: #eef2ff;
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

  /* Data-viz palette */
  --chart-1: #4f46e5;
  --chart-2: #0f9d6b;
  --chart-3: #f59e0b;
  --chart-4: #e11d48;
  --chart-5: #0ea5e9;
  --chart-6: #8b5cf6;
  --chart-grid: #eceef1;
  --chart-axis: #aab2bd;

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

  /* Radius */
  --radius-sm: 7px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 18px;
  --radius-full: 999px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(13, 18, 28, 0.04);
  --shadow-sm: 0 1px 3px rgba(13, 18, 28, 0.06), 0 1px 2px rgba(13, 18, 28, 0.04);
  --shadow-md: 0 4px 12px rgba(13, 18, 28, 0.07), 0 2px 4px rgba(13, 18, 28, 0.04);
  --shadow-lg: 0 12px 28px rgba(13, 18, 28, 0.10), 0 4px 10px rgba(13, 18, 28, 0.05);

  /* Layout */
  --sidebar-width: 248px;
  --content-max: 1560px;

  /* Typography */
  --font-sans: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'IBM Plex Mono', 'SF Mono', ui-monospace, monospace;

  /* Motion */
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --dur-fast: 120ms;
  --dur: 180ms;
}

/* ─── Base ───────────────────────────────────────────────── */
body {
  font-family: var(--font-sans);
  background: var(--bg-app);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ─── App shell ──────────────────────────────────────────── */
.app {
  display: flex;
  min-height: 100vh;
}

/* ─── Sidebar ────────────────────────────────────────────── */
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
  overflow: hidden;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-5) var(--space-4);
  text-decoration: none;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  transition: background var(--dur-fast) var(--ease);
}

.sidebar-brand:hover {
  background: var(--bg-hover);
}

.brand-mark {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.brand-name {
  font-size: 0.9375rem;
  font-weight: 800;
  color: var(--text-strong);
  letter-spacing: -0.02em;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.brand-subtitle {
  font-size: 0.6875rem;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-3) var(--space-3);
}

.nav-section-label {
  padding: var(--space-4) var(--space-3) var(--space-2);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.nav-section-label--spaced {
  margin-top: var(--space-3);
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
  transition: background var(--dur-fast) var(--ease), color var(--dur-fast) var(--ease);
  margin-bottom: 2px;
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

.sidebar-footer {
  flex-shrink: 0;
  padding: var(--space-3) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.sidebar-divider {
  height: 1px;
  background: var(--border);
  margin-bottom: var(--space-2);
}

/* ─── Main area ──────────────────────────────────────────── */
.main-area {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  height: 100vh;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: var(--content-max);
  margin: 0 auto;
  padding: var(--space-7) var(--space-8);
}

/* ─── Page header ────────────────────────────────────────── */
.page-header {
  margin-bottom: var(--space-6);
}

.page-header h2 {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-strong);
  margin-bottom: var(--space-1);
  letter-spacing: -0.03em;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 0.9375rem;
}

/* ─── Stats grid ─────────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

/* ─── Stat cards ─────────────────────────────────────────── */
@keyframes fadeRise {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .stat-card {
    animation: none !important;
    transform: none !important;
  }
}

.stat-card {
  background: var(--bg-surface);
  padding: var(--space-5) var(--space-6);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-xs);
  transition: border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease), transform var(--dur) var(--ease);
  animation: fadeRise 360ms var(--ease) both;
}

.stat-card:nth-child(1) { animation-delay: 0ms; }
.stat-card:nth-child(2) { animation-delay: 40ms; }
.stat-card:nth-child(3) { animation-delay: 80ms; }
.stat-card:nth-child(4) { animation-delay: 120ms; }
.stat-card:nth-child(5) { animation-delay: 160ms; }
.stat-card:nth-child(6) { animation-delay: 200ms; }

.stat-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.stat-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: var(--space-3);
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-strong);
  letter-spacing: -0.03em;
  font-feature-settings: 'tnum' 1, 'cv11' 1;
}

.stat-card.warning .stat-value { color: var(--warning); }
.stat-card.success .stat-value { color: var(--success); }
.stat-card.danger  .stat-value { color: var(--danger); }
.stat-card.info    .stat-value { color: var(--info); }

/* ─── Cards ──────────────────────────────────────────────── */
.card {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-xs);
  margin-bottom: var(--space-5);
  transition: border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-strong);
  letter-spacing: -0.01em;
}

/* ─── Tables ─────────────────────────────────────────────── */
.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--bg-subtle);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-faint);
  color: var(--text-secondary);
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color var(--dur-fast) var(--ease);
}

tbody tr:hover {
  background: var(--bg-subtle);
}

/* ─── Badges ─────────────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.badge.success    { background: var(--success-bg); color: var(--success-text); }
.badge.warning    { background: var(--warning-bg); color: var(--warning-text); }
.badge.danger     { background: var(--danger-bg);  color: var(--danger-text); }
.badge.info       { background: var(--info-bg);    color: var(--info-text); }
.badge.increasing { background: var(--success-bg); color: var(--success-text); }
.badge.decreasing { background: var(--danger-bg);  color: var(--danger-text); }
.badge.stable     { background: var(--info-bg);    color: var(--info-text); }
.badge.high       { background: var(--danger-bg);  color: var(--danger-text); }
.badge.medium     { background: var(--warning-bg); color: var(--warning-text); }
.badge.low        { background: var(--info-bg);    color: var(--info-text); }

/* ─── States ─────────────────────────────────────────────── */
.loading {
  text-align: center;
  padding: var(--space-8);
  color: var(--text-muted);
  font-size: 0.9375rem;
}

.error {
  background: var(--danger-bg);
  border: 1px solid var(--danger);
  color: var(--danger-text);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  margin: var(--space-4) 0;
  font-size: 0.9375rem;
}
</style>
