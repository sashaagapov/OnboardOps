# OnboardOps

OnboardOps is a small Python project for managing client onboarding tasks. It includes a FastAPI API to create, list, update the status of, and delete tasks stored in a local SQLite database. A separate script generates a fixed set of sample onboarding tasks.

## Run locally

From the project directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python database.py
fastapi dev api.py
```

The database initialization creates `onboardops.db` in the current directory. The API documentation is available at `http://127.0.0.1:8000/docs` while the server is running.

To run the sample script after initializing the database:

```powershell
python main.py
```
