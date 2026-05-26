<template>
  <BaseModal
    :is-open="isOpen"
    :title="t('tasks.title')"
    container-class="tasks-modal-container"
    @close="$emit('close')"
  >
    <div class="task-form">
      <div class="form-row">
        <div class="form-group flex-1">
          <label for="task-title">{{ t("tasks.taskTitle") }}</label>
          <input
            id="task-title"
            v-model="newTask.title"
            type="text"
            :placeholder="t('tasks.taskTitlePlaceholder')"
            class="task-input"
            @keyup.enter="handleAddTask"
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="task-priority">{{ t("tasks.priority") }}</label>
          <select
            id="task-priority"
            v-model="newTask.priority"
            class="task-select"
          >
            <option value="high">{{ t("priority.high") }}</option>
            <option value="medium">{{ t("priority.medium") }}</option>
            <option value="low">{{ t("priority.low") }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="task-due-date">{{ t("tasks.dueDate") }}</label>
          <input
            id="task-due-date"
            v-model="newTask.dueDate"
            type="date"
            class="task-input"
          />
        </div>

        <div class="form-group-btn">
          <button
            @click="handleAddTask"
            class="task-add-btn"
            :disabled="!newTask.title.trim() || !newTask.dueDate"
          >
            {{ t("tasks.addTask") }}
          </button>
        </div>
      </div>
    </div>

    <div class="tasks-divider"></div>

    <div v-if="sortedTasks.length === 0" class="no-tasks">
      {{ t("tasks.noTasks") }}
    </div>

    <div v-else class="tasks-list">
      <div
        v-for="task in sortedTasks"
        :key="task.id"
        class="task-item"
        :class="[
          `priority-${task.priority}`,
          { completed: task.status === 'completed' },
        ]"
      >
        <div class="task-header">
          <div class="task-check-title">
            <input
              type="checkbox"
              :checked="task.status === 'completed'"
              @change="$emit('toggle-task', task)"
              class="task-checkbox"
            />
            <span class="task-title" @click="$emit('toggle-task', task)">{{
              task.title
            }}</span>
          </div>
          <button
            @click="$emit('delete-task', task)"
            class="task-delete-btn"
            title="Delete task"
          >
            ×
          </button>
        </div>

        <div class="task-footer">
          <span class="priority-badge" :class="task.priority">
            {{ translatePriority(task.priority) }}
          </span>
          <div class="task-due-date">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <rect
                x="2"
                y="3"
                width="10"
                height="9"
                rx="1"
                stroke="currentColor"
                stroke-width="1.2"
              />
              <path
                d="M4.5 1.5V4.5M9.5 1.5V4.5M2 6H12"
                stroke="currentColor"
                stroke-width="1.2"
                stroke-linecap="round"
              />
            </svg>
            {{ formatDueDate(task.dueDate) }}
          </div>
          <span
            class="status-badge"
            :class="getStatusClass(task.dueDate, task.status)"
          >
            {{ getStatusText(task.dueDate, task.status) }}
          </span>
        </div>
      </div>
    </div>

    <template #footer>
      <button class="btn-secondary" @click="$emit('close')">
        {{ t("profileDetails.close") }}
      </button>
    </template>
  </BaseModal>
</template>

<script>
import { ref, computed } from "vue";
import { useI18n } from "../composables/useI18n";
import { diffCalendarDays, formatDateShort } from "../utils/dates";
import BaseModal from "./BaseModal.vue";

export default {
  name: "TasksModal",
  components: { BaseModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    tasks: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["close", "add-task", "delete-task", "toggle-task"],
  setup(props, { emit }) {
    const { t, currentLocale } = useI18n();
    const newTask = ref({
      title: "",
      priority: "medium",
      dueDate: "",
    });

    const sortedTasks = computed(() => {
      return [...props.tasks];
    });

    const close = () => {
      emit("close");
    };

    const handleAddTask = () => {
      if (newTask.value.title.trim() && newTask.value.dueDate) {
        emit("add-task", {
          title: newTask.value.title.trim(),
          priority: newTask.value.priority,
          dueDate: newTask.value.dueDate,
        });
        newTask.value = {
          title: "",
          priority: "medium",
          dueDate: "",
        };
      }
    };

    const formatDueDate = (dateString) => {
      const today = new Date();
      const dueDate = new Date(dateString);
      const diffDays = diffCalendarDays(today, dueDate);

      if (diffDays === null) return "—";

      const isJapanese = currentLocale.value === "ja";

      if (diffDays === 0) return isJapanese ? "今日" : "today";
      if (diffDays === 1) return isJapanese ? "明日" : "tomorrow";
      if (diffDays === -1) return isJapanese ? "昨日" : "yesterday";
      if (diffDays < 0)
        return isJapanese
          ? `${Math.abs(diffDays)}日前`
          : `${Math.abs(diffDays)} days ago`;
      if (diffDays < 7)
        return isJapanese ? `${diffDays}日後` : `in ${diffDays} days`;

      return formatDateShort(dateString, currentLocale.value);
    };

    const getStatusClass = (dueDate, status) => {
      if (status === "completed") return "completed";

      const today = new Date();
      const diffDays = diffCalendarDays(today, new Date(dueDate));

      if (diffDays === null) return "upcoming";
      if (diffDays < 0) return "overdue";
      if (diffDays <= 1) return "urgent";
      return "upcoming";
    };

    const getStatusText = (dueDate, status) => {
      const isJapanese = currentLocale.value === "ja";

      if (status === "completed") return isJapanese ? "完了" : "Completed";

      const statusClass = getStatusClass(dueDate, status);
      if (statusClass === "overdue") return isJapanese ? "期限超過" : "Overdue";
      if (statusClass === "urgent")
        return isJapanese ? "もうすぐ期限" : "Due Soon";
      return isJapanese ? "予定" : "Upcoming";
    };

    const translatePriority = (priority) => {
      const priorityMap = {
        high: t("priority.high"),
        medium: t("priority.medium"),
        low: t("priority.low"),
      };
      return priorityMap[priority] || priority;
    };

    return {
      t,
      newTask,
      sortedTasks,
      close,
      handleAddTask,
      formatDueDate,
      getStatusClass,
      getStatusText,
      translatePriority,
    };
  },
};
</script>

<style>
.tasks-modal-container {
  max-width: 900px !important;
}
</style>

<style scoped>
.btn-secondary {
  padding: var(--space-3) var(--space-5);
  background: var(--bg-subtle);
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-weight: 600;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all var(--dur-fast) var(--ease);
}

.btn-secondary:hover {
  background: var(--bg-hover);
  border-color: var(--border-strong);
}

.task-form {
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  margin-bottom: var(--space-6);
}

.form-row {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  flex: 1;
}

.form-group.flex-1 {
  flex: 1;
}

.form-group-btn {
  display: flex;
  align-items: flex-end;
}

label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.task-input,
.task-select {
  padding: var(--space-3) var(--space-3);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-family: var(--font-sans);
  color: var(--text-primary);
  background: var(--bg-surface);
  transition: border-color var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease);
}

.task-input:focus,
.task-select:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-ring);
}

.task-select {
  cursor: pointer;
}

.task-add-btn {
  padding: var(--space-3) var(--space-6);
  background: var(--accent);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: background var(--dur-fast) var(--ease), transform var(--dur-fast) var(--ease);
  white-space: nowrap;
  height: fit-content;
}

.task-add-btn:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
}

.task-add-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.tasks-divider {
  height: 1px;
  background: var(--border);
  margin: var(--space-7) 0;
}

.no-tasks {
  text-align: center;
  padding: var(--space-8);
  color: var(--text-muted);
  font-size: 1rem;
  font-style: italic;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.task-item {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  transition: border-color var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease);
}

.task-item:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-xs);
}

.task-item.priority-high {
  border-left: 3px solid var(--danger);
}

.task-item.priority-medium {
  border-left: 3px solid var(--warning);
}

.task-item.priority-low {
  border-left: 3px solid var(--accent);
}

.task-item.completed {
  opacity: 0.6;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);
  gap: var(--space-4);
}

.task-check-title {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex: 1;
}

.task-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--accent);
  flex-shrink: 0;
}

.task-title {
  flex: 1;
  cursor: pointer;
  user-select: none;
  color: var(--text-primary);
  font-size: 0.938rem;
  font-weight: 600;
  line-height: 1.4;
}

.task-item.completed .task-title {
  text-decoration: line-through;
  color: var(--text-muted);
}

.task-delete-btn {
  width: 26px;
  height: 26px;
  background: var(--danger-bg);
  color: var(--danger-text);
  border: 1px solid var(--danger);
  border-radius: var(--radius-sm);
  font-size: 1.1rem;
  line-height: 1;
  cursor: pointer;
  transition: all var(--dur-fast) var(--ease);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  flex-shrink: 0;
}

.task-delete-btn:hover {
  background: var(--danger);
  color: white;
}

.task-footer {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.priority-badge {
  display: inline-flex;
  align-items: center;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  letter-spacing: 0.04em;
}

.priority-badge.high {
  background: var(--danger-bg);
  color: var(--danger-text);
}

.priority-badge.medium {
  background: var(--warning-bg);
  color: var(--warning-text);
}

.priority-badge.low {
  background: var(--info-bg);
  color: var(--info-text);
}

.task-due-date {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.813rem;
  color: var(--text-muted);
}

.task-due-date svg {
  color: var(--text-muted);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  margin-left: auto;
  letter-spacing: 0.02em;
}

.status-badge.overdue {
  background: var(--danger-bg);
  color: var(--danger-text);
}

.status-badge.urgent {
  background: var(--warning-bg);
  color: var(--warning-text);
}

.status-badge.upcoming {
  background: var(--info-bg);
  color: var(--info-text);
}

.status-badge.completed {
  background: var(--success-bg);
  color: var(--success-text);
}
</style>
