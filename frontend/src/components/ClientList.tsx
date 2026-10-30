import type { Client } from "../types";

type ClientListProps = {
  clients: Client[];
  selectedClient: string | null;
  onSelect: (clientName: string) => void;
  isLoading: boolean;
};

export function ClientList({ clients, selectedClient, onSelect, isLoading }: ClientListProps) {
  if (isLoading) {
    return (
      <div className="client-skeleton" aria-label="Loading clients" aria-busy="true">
        {Array.from({ length: 4 }, (_, i) => (
          <div className="client-skeleton__item" key={i} />
        ))}
      </div>
    );
  }

  if (clients.length === 0) {
    return <p className="panel-message">No clients yet. Create one to get started.</p>;
  }

  return (
    <ul className="client-list" aria-label="Clients">
      {clients.map((client) => {
        const isSelected = selectedClient === client.name;
        return (
          <li key={client.name}>
            <button
              className={`client-row${isSelected ? " client-row--selected" : ""}`}
              type="button"
              onClick={() => onSelect(client.name)}
              aria-pressed={isSelected}
            >
              <div className="client-row__top">
                <span className="client-row__name">{client.name}</span>
                <span className="client-row__pct">{client.progress_percent}%</span>
              </div>
              <div className="progress-bar" role="progressbar" aria-valuenow={client.progress_percent} aria-valuemin={0} aria-valuemax={100}>
                <div
                  className="progress-bar__fill"
                  style={{ width: `${client.progress_percent}%` }}
                />
              </div>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
