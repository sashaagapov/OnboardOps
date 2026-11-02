# OnboardOps — Personal Project

OnboardOps is an end-to-end personal project built to apply and strengthen technical knowledge through hands-on software development, API integration, workflow automation, and operational reporting.

It models a simulated client-onboarding workflow: tasks can be created and managed for each client, progress and overdue work are visible in a React console, and a local n8n workflow can send an overdue alert and record a daily operations snapshot.

## Architecture

![OnboardOps architecture](docs/architecture.svg)

The backend is the source of truth for tasks and the operations summary. The frontend and n8n consume the same REST API; SQLite remains local to the development environment.

## What is implemented

- React + TypeScript Operations Console for browsing clients, reviewing tasks, creating a client/first task, adding tasks, and updating task status.
- FastAPI REST API backed by automatically initialized SQLite storage.
- Three task states: `pending`, `in_progress`, and `completed`.
- Optional deadlines, overdue-task detection, onboarding progress, and seven cross-client operational metrics.
- Python test suite using pytest and FastAPI `TestClient` with isolated temporary databases.
- Postman collection for ordered API checks, validation, duplicate handling, progress, overdue behavior, and cleanup.
- A local n8n workflow with manual and scheduled triggers, a summary request, an overdue condition, Telegram notification, and a date-based Google Sheets upsert.

## Operations Console

The console is designed around the current operational workflow:

- Seven KPI cards: total, completed, pending, in progress, completion rate, overdue, and client count.
- Client list with individual completion progress.
- Per-client task table with due dates, overdue indicators, and status controls.
- Simple, validated forms for creating a new client with its first task or adding a task to an existing client.
- Loading, empty, success, validation, duplicate-task, and API-error states.

## Backend and REST API

| Area | Endpoints |
| --- | --- |
| Tasks | `POST /tasks`, `PATCH /clients/{client_name}/tasks/{title}`, `DELETE /clients/{client_name}/tasks/{title}` |
| Clients | `GET /clients`, `GET /clients/{client_name}/tasks` |
| Onboarding | `POST /clients/{client_name}/onboarding`, `GET /clients/{client_name}/progress`, `GET /clients/{client_name}/overdue` |
| Reporting | `GET /operations/summary` |

`POST /tasks` returns `201`; duplicate client/title pairs return `409`; missing task updates/deletions return `404`; task status validation returns `422` for unsupported values.

## Automation and reporting

![n8n workflow configuration](docs/automation-workflow.svg)

The committed n8n workflow export is sanitized and intentionally inactive for safe import. The locally published workflow runs daily at 09:00 in `Europe/Kyiv` and also supports manual execution.

- It requests `GET /operations/summary` from the local FastAPI service.
- The Telegram branch runs when `overdue_tasks > 0`.
- Google Sheets uses **Append or Update Row**, matching on `date`, so a repeated daily run updates the same date rather than creating a duplicate.

See [automation/README.md](automation/README.md) for import steps, credential rebinding, and local runtime requirements. Telegram credentials, Google OAuth credentials, chat IDs, message content, and spreadsheet identifiers are intentionally excluded from Git.

## Tech stack

- Python, FastAPI, Pydantic, SQLite, pytest
- React, TypeScript, Vite, ESLint
- Postman
- n8n 2.45.7 (local automation)
- Telegram and Google Sheets integrations configured locally in n8n

## Testing and validation

The Python suite currently contains **37 passing tests**. It covers onboarding generation, SQLite operations, duplicate protection, task updates/deletions, status validation, client isolation, progress, deadlines, overdue calculations, operations summary metrics, and FastAPI responses.

```powershell
python -m pytest -q
```

Frontend checks:

```powershell
cd frontend
npm run lint
npm run build
```

The repository also includes [the Postman collection](postman/OnboardOps.postman_collection.json) used for API checks. It uses synthetic `PostmanQA_*` data and cleans it up at the end of a complete run.

## Run locally

SQLite initializes automatically when FastAPI starts and creates `onboardops.db` in the current directory when necessary. The database is local-only and is not committed.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
fastapi dev api.py
```

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

### macOS (Terminal)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
fastapi dev api.py
```

In a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open the FastAPI documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Vite proxies `/api` requests to `http://127.0.0.1:8000`.

### Optional synthetic demo data

With the API running, create a disposable example client using the existing onboarding contract:

```bash
curl -X POST http://127.0.0.1:8000/clients/DemoClient/onboarding
```

This is idempotent and does not require private data. Delete demo tasks through the API or console when finished.

## Current status and limitations

The project is a local development implementation for a simulated scenario. It does not include authentication, multi-user access, deployment, cloud database infrastructure, CI/CD, or a completed Tableau dashboard. n8n credentials and runtime data stay local; importing the sanitized workflow requires privately reconnecting Telegram and Google Sheets credentials.

## Repository metadata

Suggested GitHub description: **Personal project for simulated client onboarding: FastAPI, React, SQLite, n8n automation, Telegram alerts, and Google Sheets reporting.**

Suggested topics: `fastapi`, `react`, `typescript`, `sqlite`, `python`, `n8n`, `automation`, `postman`, `google-sheets`, `telegram`.
