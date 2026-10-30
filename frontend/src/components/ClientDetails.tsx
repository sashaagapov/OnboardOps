import type { ClientDetails as ClientDetailsData, Task, TaskStatus } from "../types";

type ClientDetailsProps = {
  clientName: string | null;
  details: ClientDetailsData | null;
  isLoading: boolean;
  error: string;
  updatingTaskId: number | null;
  onAddTask: () => void;
  onStatusChange: (task: Task, status: TaskStatus) => void;
};

function formatDueDate(dueDate: string | null) {
  if (!dueDate) return null;
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${dueDate}T00:00:00Z`));
}

function StatusBadge({ status }: { status: Task["status"] }) {
  const label = status === "in_progress" ? "In Progress" : status === "pending" ? "Pending" : "Completed";
  return (
    <span className={`status-badge status-badge--${status}`} aria-label={label}>
      {label}
    </span>
  );
}

export function ClientDetails({
  clientName,
  details,
  isLoading,
  error,
  updatingTaskId,
  onAddTask,
  onStatusChange,
}: ClientDetailsProps) {
  if (!clientName) {
    return (
      <p className="panel-message">
        Select a client from the list to view their onboarding tasks.
      </p>
    );
  }

  if (isLoading) {
    return (
      <p className="panel-message" aria-busy="true" aria-label={`Loading ${clientName}`}>
        Loading {clientName}&rsquo;s tasks&hellip;
      </p>
    );
  }

  if (error) {
    return <p className="panel-message panel-message--error">{error}</p>;
  }

  if (!details) {
    return null;
  }

  const overdueTaskIds = new Set(details.overdueTasks.map((task) => task.id));

  return (
    <section className="client-details" aria-live="polite">
      <header className="details-header">
        <div className="details-header__left">
          <p className="details-header__label">Selected client</p>
          <h2 className="details-header__name">{clientName}</h2>
        </div>
        <div className="details-header__meta">
          <div className="progress-readout">
            <strong className="progress-readout__pct">{details.progress.progress_percent}%</strong>
            <span className="progress-readout__sub">
              {details.progress.completed_tasks} of {details.progress.total_tasks} complete
            </span>
          </div>
          <button className="primary-button" type="button" onClick={onAddTask}>
            Add task
          </button>
        </div>
      </header>

      {details.tasks.length === 0 ? (
        <p className="panel-message">No tasks yet. Add a task to get started.</p>
      ) : (
        <div className="task-table-wrap">
          <table>
            <thead>
              <tr>
                <th scope="col">Task</th>
                <th scope="col">Status</th>
                <th scope="col">Due date</th>
                <th scope="col">Update status</th>
              </tr>
            </thead>
            <tbody>
              {details.tasks.map((task) => {
                const isOverdue = overdueTaskIds.has(task.id);
                const formatted = formatDueDate(task.due_date);
                return (
                  <tr className={isOverdue ? "task-row--overdue" : ""} key={task.id}>
                    <td>
                      <span className="task-title">{task.title}</span>
                      {isOverdue && (
                        <span className="overdue-badge" role="img" aria-label="Overdue">
                          ⚠ Overdue
                        </span>
                      )}
                    </td>
                    <td>
                      <StatusBadge status={task.status} />
                    </td>
                    <td>
                      {formatted ? (
                        <span className="due-date">{formatted}</span>
                      ) : (
                        <span className="due-date--unset">Not set</span>
                      )}
                    </td>
                    <td>
                      <select
                        aria-label={`Change status for ${task.title}`}
                        className="status-select"
                        disabled={updatingTaskId === task.id}
                        onChange={(event) =>
                          onStatusChange(task, event.target.value as TaskStatus)
                        }
                        value={task.status}
                      >
                        <option value="pending">Pending</option>
                        <option value="in_progress">In Progress</option>
                        <option value="completed">Completed</option>
                      </select>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
