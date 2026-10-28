
import { useEffect, useState } from "react";

type Client = {
  name: string;
  progress_percent: number;
};

function App() {
  const [clients, setClients] = useState<Client[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadClients() {
      try {
        const response = await fetch("/api/clients");

        if (!response.ok) {
          throw new Error("Failed to fetch clients");
        }

        const data = await response.json();
        setClients(data.clients);
      } catch {
        setError("Could not connect to the backend");
      }
    }

    loadClients();
  }, []);

  return (
    <main>
      <h1>OnboardOps</h1>
      <p>Client Onboarding Dashboard</p>

      <h2>Clients</h2>

      {error && <p>{error}</p>}

      {clients.length === 0 && !error && <p>No clients found.</p>}

      {clients.map((client) => (
        <div key={client.name}>
          <h3>{client.name}</h3>
          <p>Progress: {client.progress_percent}%</p>
        </div>
      ))}
    </main>
  );
}

export default App;
