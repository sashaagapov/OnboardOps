# OnboardOps

OnboardOps is a FastAPI backend for managing client onboarding tasks. It stores tasks in SQLite and provides a REST API for task management, onboarding progress, deadlines, overdue work, and a multi-client overview.

## Tech stack

- Python 3
- FastAPI and Pydantic
- SQLite
- pytest with FastAPI `TestClient`

## Implemented API

- `GET /clients` — list clients with onboarding progress.
- `GET /clients/{client_name}/tasks` — list a client's tasks.
- `POST /tasks` — create a task. Returns `201`; a duplicate client/title pair returns `409`.
- `PATCH /clients/{client_name}/tasks/{title}` — update a task status.
- `DELETE /clients/{client_name}/tasks/{title}` — delete a task.
- `POST /clients/{client_name}/onboarding` — create the predefined onboarding tasks for a client.
- `GET /clients/{client_name}/progress` — return total, completed, and percentage progress.
- `GET /clients/{client_name}/overdue` — list incomplete tasks whose deadlines have passed.

Task statuses are validated as `pending` or `completed`. A task may include an optional ISO date deadline.

## Run locally

From the project directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
fastapi dev api.py
```

SQLite initializes automatically when FastAPI starts. The local database file, `onboardops.db`, is created in the current directory when needed.

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Tests

Run the test suite with:

```powershell
python -m pytest -q
```

The tests use isolated temporary SQLite databases and do not modify your local database.

## Next directions

Planned work includes a React and TypeScript frontend, then evaluation of PostgreSQL, Docker, automation, CI/CD, and deployment.
