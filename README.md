# OnboardOps

OnboardOps is a client-onboarding task manager. Its FastAPI backend stores tasks in SQLite and provides a REST API for task management, onboarding progress, deadlines, overdue work, and a multi-client overview. A React and TypeScript frontend is available in `frontend/`.

## Tech stack

- Python 3
- FastAPI and Pydantic
- SQLite
- pytest with FastAPI `TestClient`
- React and TypeScript (frontend)

## Implemented API

- `GET /clients` — list clients with onboarding progress.
- `GET /clients/{client_name}/tasks` — list a client's tasks.
- `POST /tasks` — create a task. Returns `201`; a duplicate client/title pair returns `409`.
- `PATCH /clients/{client_name}/tasks/{title}` — update a task status.
- `DELETE /clients/{client_name}/tasks/{title}` — delete a task.
- `POST /clients/{client_name}/onboarding` — create the predefined onboarding tasks for a client.
- `GET /clients/{client_name}/progress` — return total, completed, and percentage progress.
- `GET /clients/{client_name}/overdue` — list incomplete tasks whose deadlines have passed.
- `GET /operations/summary` — return a cross-client operations snapshot: `total_tasks`, `completed_tasks`, `pending_tasks`, `in_progress_tasks`, `completion_rate`, `overdue_tasks`, and `unique_clients`.

Task statuses are validated as `pending`, `in_progress`, or `completed`. Completion rate counts only completed tasks. A task may include an optional ISO date deadline; overdue tasks are pending or in-progress tasks whose deadline has passed.

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

Operations Summary coverage is included in `test_api.py`. Run that module on its own with:

```powershell
python -m pytest -q test_api.py
```

## API testing with Postman

The importable collection is at [postman/OnboardOps.postman_collection.json](postman/OnboardOps.postman_collection.json). It contains 20 ordered requests and 42 assertions covering client listing, onboarding, task creation and retrieval, status updates, deletion, validation errors, duplicates, progress, overdue tasks, idempotency, and cleanup.

1. Start the API with `fastapi dev api.py`; the collection defaults to `http://127.0.0.1:8000`.
2. Import `postman/OnboardOps.postman_collection.json` into Postman.
3. Run the full collection once in its listed order, starting with request `00` and without a data file.

The collection uses the `baseUrl` variable and creates a unique `PostmanQA_*` client in its first pre-request script. It only uses that synthetic client and the final requests remove its tasks, so repeated full runs are safe against a local development database. Do not point the collection at production or real customer data. Python tests remain separate and can be run with `python -m pytest -q`.

## Next directions

Next steps include further frontend development, then evaluation of PostgreSQL, Docker, automation, CI/CD, and deployment.
