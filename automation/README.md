# n8n automation

`onboardops-daily-operations.json` is a sanitized n8n v2.45.7 export of
**OnboardOps — Daily Operations**. The source workflow is published in the
local Windows n8n instance. It contains a Manual Trigger, a daily Schedule
Trigger at 09:00 in `Europe/Kyiv`, an HTTP request to
`http://127.0.0.1:8000/operations/summary`, an `overdue_tasks > 0` condition,
a Telegram true branch, and a Google Sheets **Append or Update Row** node.

The committed export is deliberately inactive, so importing it cannot enable a
schedule unexpectedly. This does not change the published Windows workflow.

## Import on Windows or macOS

1. Install/run n8n v2.45.7 (or a compatible v2 release), then sign in locally.
2. In n8n, choose **Import from File** and select
   `automation/onboardops-daily-operations.json`.
3. In the Telegram node, privately create or select your Telegram credential,
   then enter the intended chat ID and message. These values and all credential
   bindings were removed from the committed export.
4. In the Google Sheets node, privately reconnect a Google Sheets OAuth2
   credential, select the target spreadsheet and sheet, then retain `date` as
   the matching column. The node uses **Append or Update Row**, so repeat runs
   update the existing row for a date instead of adding duplicates.
5. Start the FastAPI backend on the same machine before manually executing the
   workflow. Review it before activating the schedule.

The workflow uses `127.0.0.1`, so it works unchanged when n8n and FastAPI run
on the same Mac or Windows machine. For containers or separate hosts, update
the HTTP Request URL to a reachable backend address.

## Local backup and unfinished integrations

Local n8n databases, encryption configuration, OAuth/Telegram credentials,
Google account information, and runtime logs are private and are never tracked
in Git. n8n needs network access to Google only when authorizing or using the
Google Sheets node. Tableau dashboard work is not completed.
