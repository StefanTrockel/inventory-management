import { ref, computed } from "vue";
import { useI18n } from "./useI18n";
import { resetFilters as resetFiltersFn } from "./useFilters";

const baseUserData = {
  id: 1,
  email: "john.doe@catalystcomponents.com",
  phone: "+1 (111) 111-1111",
  avatar: null,
  joinDate: "2022-03-15",
};

const defaultTasks = [
  {
    id: 1,
    titleKey: "tasks.defaults.reviewQ4",
    priority: "high",
    dueDate: "2025-10-08",
    status: "pending",
  },
  {
    id: 2,
    titleKey: "tasks.defaults.approveTokyo",
    priority: "medium",
    dueDate: "2025-10-06",
    status: "pending",
  },
  {
    id: 3,
    titleKey: "tasks.defaults.updateReorderPoints",
    priority: "medium",
    dueDate: "2025-10-10",
    status: "pending",
  },
  {
    id: 4,
    titleKey: "tasks.defaults.reviewMonthlySpending",
    priority: "low",
    dueDate: "2025-10-15",
    status: "pending",
  },
];

const userTasks = ref(defaultTasks.map((t) => ({ ...t, source: "mock" })));

const isAuthenticated = ref(true);

const { currentLocale, t } = useI18n();

const currentUser = computed(() => {
  const isJapanese = currentLocale.value === "ja";
  return {
    ...baseUserData,
    name: isJapanese ? "田中 太郎" : "John Doe",
    jobTitle: isJapanese ? "オペレーションマネージャー" : "Operations Manager",
    department: isJapanese
      ? "サプライチェーン運営部"
      : "Supply Chain Operations",
    location: isJapanese ? "サンフランシスコ" : "San Francisco",
    tasks: userTasks.value.map((task) => ({
      ...task,
      title: task.titleKey ? t(task.titleKey) : task.title,
    })),
  };
});

export function useAuth() {
  const logout = () => {
    isAuthenticated.value = false;
    resetFiltersFn();
    try {
      localStorage.removeItem("auth-token");
    } catch {
      // ignore
    }
    console.log("Logout: state cleared");
  };

  const getInitials = (name) => {
    if (!name) return "";
    return name
      .split(" ")
      .map((n) => n[0])
      .filter(Boolean)
      .join("")
      .toUpperCase();
  };

  const addUserTask = (task) => {
    const id =
      task.id ??
      Math.max(0, ...userTasks.value.map((t) => Number(t.id) || 0)) + 1;
    userTasks.value.unshift({ source: "mock", ...task, id });
  };

  const removeUserTask = (taskId) => {
    userTasks.value = userTasks.value.filter((task) => task.id !== taskId);
  };

  const toggleUserTask = (taskId) => {
    const task = userTasks.value.find((t) => t.id === taskId);
    if (task) {
      task.status = task.status === "pending" ? "completed" : "pending";
    }
  };

  const hasUserTask = (taskId) => userTasks.value.some((t) => t.id === taskId);

  return {
    currentUser,
    isAuthenticated,
    logout,
    getInitials,
    addUserTask,
    removeUserTask,
    toggleUserTask,
    hasUserTask,
  };
}
