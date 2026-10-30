# n8n automation

The local n8n workflow **OnboardOps — Daily Operations** is stored in the local
n8n instance. It retrieves `GET http://127.0.0.1:8000/operations/summary` and
uses `overdue_tasks > 0` to select a branch. The workflow is inactive; no
schedule or external notification is enabled.

## Restore

Start the local n8n instance, sign in with the existing local n8n account, and
open **OnboardOps — Daily Operations** from the workflow list. Its persistent
state is backed up outside this repository; restore that private backup before
starting n8n if recovery is needed.

## Export status

An importable JSON export is not included in this commit. At checkpoint time,
the local n8n UI and REST API required an authenticated session, so the workflow
could not be exported without credentials. No authentication was bypassed and
no credentials, encryption configuration, or n8n database files are tracked in
Git.

## Incomplete integrations

- Telegram credentials and bot token are not configured.
- Google Sheets is not connected.
- Tableau integration is not implemented.
