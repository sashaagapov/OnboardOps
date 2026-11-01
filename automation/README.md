# n8n automation

`onboardops-daily-operations.json` is a sanitized n8n v2.45.7 export of
**OnboardOps — Daily Operations**. It contains a Manual Trigger, a daily
Schedule Trigger at 09:00 in `Europe/Kyiv`, an HTTP request to
`http://127.0.0.1:8000/operations/summary`, an `overdue_tasks > 0` condition,
and a Telegram true branch. The workflow is exported inactive and has not been
published for scheduled execution.

## Import on Windows or macOS

1. Install/run n8n v2.45.7 (or a compatible v2 release), then sign in locally.
2. In n8n, choose **Import from File** and select
   `automation/onboardops-daily-operations.json`.
3. In the Telegram node, privately create or select your Telegram credential,
   then enter the intended chat ID and message. These values and all credential
   bindings were removed from the committed export.
4. Start the FastAPI backend on the same machine before manually executing the
   workflow. Review it before activating the schedule.

The workflow uses `127.0.0.1`, so it works unchanged when n8n and FastAPI run
on the same Mac or Windows machine. For containers or separate hosts, update
the HTTP Request URL to a reachable backend address.

## Local backup and unfinished integrations

Local n8n databases, encryption configuration, credentials, and runtime logs
are private and are never tracked in Git. Google Sheets integration is not
implemented. Tableau dashboard work is not completed.
