import { useCallback, useEffect, useState } from "react";
import { createTask, getClientDetails, getClients, getOperationsSummary, updateTaskStatus } from "./api";
import { ClientDetails } from "./components/ClientDetails";
import { ClientList } from "./components/ClientList";
import { MetricCard } from "./components/MetricCard";
import { TaskForm, type NewTaskValues } from "./components/TaskForm";
import type { Client, ClientDetails as ClientDetailsData, OperationsSummary, Task, TaskStatus } from "./types";
import "./App.css";

const metrics = (summary: OperationsSummary) => [
  { label: "Total tasks", value: summary.total_tasks },
  { label: "Completed", value: summary.completed_tasks, tone: "success" as const },
  { label: "Pending", value: summary.pending_tasks },
  { label: "In progress", value: summary.in_progress_tasks, tone: "progress" as const },
  { label: "Completion rate", value: `${summary.completion_rate}%` },
  { label: "Overdue", value: summary.overdue_tasks, tone: "warning" as const },
  { label: "Clients", value: summary.unique_clients },
];

function App() {
  const [clients, setClients] = useState<Client[]>([]);
  const [summary, setSummary] = useState<OperationsSummary | null>(null);
  const [selectedClient, setSelectedClient] = useState<string | null>(null);
  const [clientDetails, setClientDetails] = useState<ClientDetailsData | null>(null);
  const [overviewError, setOverviewError] = useState("");
  const [detailsError, setDetailsError] = useState("");
  const [notice, setNotice] = useState("");
  const [activeForm, setActiveForm] = useState<"client" | "task" | null>(null);
  const [creationError, setCreationError] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [isOverviewLoading, setIsOverviewLoading] = useState(true);
  const [isDetailsLoading, setIsDetailsLoading] = useState(false);
  const [updatingTaskId, setUpdatingTaskId] = useState<number | null>(null);

  const loadOverview = useCallback(async () => {
    setIsOverviewLoading(true);
    setOverviewError("");
    try {
      const [nextSummary, nextClients] = await Promise.all([getOperationsSummary(), getClients()]);
      setSummary(nextSummary);
      setClients(nextClients);
    } catch {
      setOverviewError("Could not load operations data. Check that the FastAPI server is running.");
    } finally {
      setIsOverviewLoading(false);
    }
  }, []);

  const loadClientDetails = useCallback(async (clientName: string) => {
    setIsDetailsLoading(true);
    setDetailsError("");
    try {
      setClientDetails(await getClientDetails(clientName));
    } catch {
      setDetailsError("Could not load this client's task details.");
      setClientDetails(null);
    } finally {
      setIsDetailsLoading(false);
    }
  }, []);

  useEffect(() => {
    void Promise.resolve().then(loadOverview);
  }, [loadOverview]);

  function selectClient(clientName: string) {
    setSelectedClient(clientName);
    setNotice("");
    setActiveForm(null);
    void loadClientDetails(clientName);
  }

  function openForm(mode: "client" | "task") {
    setCreationError("");
    setNotice("");
    setActiveForm(mode);
  }

  function closeForm() {
    if (!isCreating) {
      setActiveForm(null);
      setCreationError("");
    }
  }

  async function createNewTask({ client, title, dueDate }: NewTaskValues) {
    if (!client || !title) {
      setCreationError("Client name and task title are required.");
      return;
    }
    setIsCreating(true);
    setCreationError("");
    try {
      await createTask({ client, title, ...(dueDate ? { due_date: dueDate } : {}) });
      setSelectedClient(client);
      await Promise.all([loadOverview(), loadClientDetails(client)]);
      setNotice(`"${title}" was created for ${client}.`);
      setActiveForm(null);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Task could not be created.";
      setCreationError(message);
    } finally {
      setIsCreating(false);
    }
  }

  async function changeTaskStatus(task: Task, status: TaskStatus) {
    if (!selectedClient) return;
    setUpdatingTaskId(task.id);
    setNotice("");
    setDetailsError("");
    try {
      await updateTaskStatus(selectedClient, task.title, status);
      await Promise.all([loadClientDetails(selectedClient), loadOverview()]);
      setNotice(`"${task.title}" marked ${status.replace("_", " ")}.`);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Task status could not be updated.";
      setDetailsError(message);
    } finally {
      setUpdatingTaskId(null);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="product-name">OnboardOps</p>
          <h1>Operations Console</h1>
        </div>
        <div className="topbar-actions">
          <button className="primary-button" type="button" onClick={() => openForm("client")}>
            New client
          </button>
        </div>
      </header>

      {overviewError ? (
        <div className="app-error" role="alert">
          <p>{overviewError}</p>
          <button type="button" onClick={() => void loadOverview()}>
            Try again
          </button>
        </div>
      ) : (
        <>
          <section className="metrics" aria-label="Operations summary">
            {isOverviewLoading || !summary
              ? Array.from({ length: 7 }, (_, index) => (
                  <div className="metric-card metric-card--loading" key={index} aria-hidden="true" />
                ))
              : metrics(summary).map((metric) => <MetricCard key={metric.label} {...metric} />)}
          </section>

          {activeForm && (
            <TaskForm
              clientName={activeForm === "task" ? selectedClient ?? undefined : undefined}
              error={creationError}
              isSubmitting={isCreating}
              onCancel={closeForm}
              onSubmit={createNewTask}
            />
          )}

          <section className="workspace" aria-label="Client task workspace">
            <aside className="clients-panel">
              <div className="panel-heading">
                <div>
                  <p className="panel-heading__label">Portfolio</p>
                  <h2>Clients</h2>
                </div>
                {!isOverviewLoading && (
                  <span className="client-count" aria-label={`${clients.length} clients`}>
                    {clients.length}
                  </span>
                )}
              </div>
              <ClientList
                clients={clients}
                selectedClient={selectedClient}
                onSelect={selectClient}
                isLoading={isOverviewLoading}
              />
            </aside>

            <section className="details-panel" aria-label="Client task details">
              {notice && <p className="notice" role="status">{notice}</p>}
              <ClientDetails
                clientName={selectedClient}
                details={clientDetails}
                isLoading={isDetailsLoading}
                error={detailsError}
                updatingTaskId={updatingTaskId}
                onAddTask={() => openForm("task")}
                onStatusChange={changeTaskStatus}
              />
            </section>
          </section>
        </>
      )}
    </main>
  );
}

export default App;
