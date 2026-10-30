export type TaskStatus = "pending" | "in_progress" | "completed";

export type Client = {
  name: string;
  progress_percent: number;
};

export type Task = {
  id: number;
  title: string;
  status: TaskStatus;
  due_date: string | null;
};

export type Progress = {
  client: string;
  total_tasks: number;
  completed_tasks: number;
  progress_percent: number;
};

export type OperationsSummary = {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  in_progress_tasks: number;
  completion_rate: number;
  overdue_tasks: number;
  unique_clients: number;
};

export type ClientDetails = {
  tasks: Task[];
  progress: Progress;
  overdueTasks: Task[];
};
