import { useState, type FormEvent } from "react";

export type NewTaskValues = {
  client: string;
  title: string;
  dueDate: string;
};

type TaskFormProps = {
  clientName?: string;
  isSubmitting: boolean;
  error: string;
  onCancel: () => void;
  onSubmit: (values: NewTaskValues) => void;
};

export function TaskForm({ clientName, isSubmitting, error, onCancel, onSubmit }: TaskFormProps) {
  const [client, setClient] = useState(clientName ?? "");
  const [title, setTitle] = useState("");
  const [dueDate, setDueDate] = useState("");
  const isNewClient = !clientName;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit({ client: client.trim(), title: title.trim(), dueDate });
  }

  return (
    <section className="creation-panel" aria-labelledby="task-form-title">
      <div className="creation-panel__header">
        <div>
          <p className="creation-panel__title">{isNewClient ? "New client" : "New task"}</p>
          <h2 id="task-form-title">
            {isNewClient ? "Create client & first task" : `Add task — ${clientName}`}
          </h2>
        </div>
        <button className="text-button" type="button" onClick={onCancel} disabled={isSubmitting} aria-label="Close form">
          ✕
        </button>
      </div>

      <form className="task-form" onSubmit={handleSubmit}>
        {isNewClient && (
          <label>
            Client name
            <input
              autoComplete="organization"
              disabled={isSubmitting}
              onChange={(event) => setClient(event.target.value)}
              placeholder="e.g. Acme Corp"
              required
              value={client}
            />
          </label>
        )}
        <label>
          Task title
          <input
            autoFocus
            disabled={isSubmitting}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="e.g. Complete KYC verification"
            required
            value={title}
          />
        </label>
        <label>
          Due date <span className="optional">Optional</span>
          <input
            disabled={isSubmitting}
            onChange={(event) => setDueDate(event.target.value)}
            type="date"
            value={dueDate}
          />
        </label>
        <p className="form-note">Tasks are created with Pending status.</p>
        {error && (
          <p className="form-error" role="alert">
            {error}
          </p>
        )}
        <div className="form-actions">
          <button className="text-button" disabled={isSubmitting} type="button" onClick={onCancel}>
            Cancel
          </button>
          <button className="primary-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Creating…" : isNewClient ? "Create client" : "Add task"}
          </button>
        </div>
      </form>
    </section>
  );
}
