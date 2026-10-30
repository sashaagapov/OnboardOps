import type {
  Client,
  ClientDetails,
  OperationsSummary,
  Progress,
  Task,
  TaskStatus,
} from "./types";

type ClientsResponse = { clients: Client[] };
type TasksResponse = { client: string; tasks: Task[] };

export type CreateTaskInput = {
  client: string;
  title: string;
  due_date?: string;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, options);

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    const detail = typeof payload?.detail === "string" ? payload.detail : "Request failed";
    throw new Error(detail);
  }

  return response.json() as Promise<T>;
}

export async function getClients(): Promise<Client[]> {
  const response = await request<ClientsResponse>("/clients");
  return response.clients;
}

export function getOperationsSummary(): Promise<OperationsSummary> {
  return request<OperationsSummary>("/operations/summary");
}

export function createTask(task: CreateTaskInput): Promise<Omit<Task, "id">> {
  return request<Omit<Task, "id">>("/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...task, status: "pending" }),
  });
}

export async function getClientDetails(clientName: string): Promise<ClientDetails> {
  const encodedClient = encodeURIComponent(clientName);
  const [tasksResponse, progress, overdueTasks] = await Promise.all([
    request<TasksResponse>(`/clients/${encodedClient}/tasks`),
    request<Progress>(`/clients/${encodedClient}/progress`),
    request<Task[]>(`/clients/${encodedClient}/overdue`),
  ]);

  return { tasks: tasksResponse.tasks, progress, overdueTasks };
}

export function updateTaskStatus(
  clientName: string,
  title: string,
  status: TaskStatus,
): Promise<{ updated: boolean }> {
  return request<{ updated: boolean }>(
    `/clients/${encodeURIComponent(clientName)}/tasks/${encodeURIComponent(title)}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    },
  );
}
