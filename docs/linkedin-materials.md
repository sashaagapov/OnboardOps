# OnboardOps — LinkedIn materials

## Suggested post

I have been working on **OnboardOps**, a personal project built around a simulated client-onboarding workflow.

The goal was to apply and reinforce technical knowledge by connecting the parts of a small system end to end: a FastAPI backend with SQLite storage, a React and TypeScript operations console, REST API validation and tests, Postman checks, and local n8n automation.

The application supports client tasks, three task statuses, deadlines, overdue-task detection, onboarding progress, and a seven-metric operations summary. The n8n workflow retrieves that summary daily, can send a Telegram alert when overdue work exists, and writes a date-based daily snapshot to Google Sheets.

Building it made the interactions between UI state, API contracts, persistence, testing, and automation much more concrete. The project uses synthetic onboarding data; it is a technical implementation rather than a production service.

GitHub: https://github.com/sashaagapov/OnboardOps

## LinkedIn Projects-section description

Personal project for a simulated client-onboarding workflow. Built a FastAPI and SQLite backend, React/TypeScript operations console, tested REST API, and local n8n automation for overdue alerts and date-based Google Sheets reporting.

## Compact CV entry

**OnboardOps — Personal Project**
Built a simulated client-onboarding system using FastAPI, SQLite, React, and TypeScript. Implemented task management, deadline and progress reporting, automated API tests, and local n8n automation for Telegram overdue alerts and daily Google Sheets upserts.

## Visual order for a LinkedIn post

1. Authentic Operations Console screenshot using synthetic data.
2. `docs/architecture.svg` to explain the frontend, API, database, and automation flow.
3. `docs/automation-workflow.svg` to show triggers, summary request, condition, Telegram branch, and Google Sheets upsert.

Do not include the sanitized workflow JSON itself, private local database files, Google Sheets screenshots containing account data, or Telegram configuration.
