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

All five PNGs are square (1200 × 1200 px) and share the Operations Console's restrained navy, blue, green, and amber palette. Editable SVG sources are retained alongside the assets. The console image is an authentic capture from the running React app using synthetic records created through the real API.

1. [Cover](linkedin/01-cover.png) — the personal-project context and implemented stack. [Editable SVG](linkedin/01-cover.svg).
2. [Operations Console](linkedin/02-console.png) — real UI with seven KPI cards, client progress, task statuses, deadlines, and `Demo:` data. [Editable SVG](linkedin/02-console.svg); [unframed capture](operations-console.png).
3. [Architecture](linkedin/03-architecture.png) — interactive application flow and n8n's independent call to the same API. [Editable SVG](architecture.svg).
4. [Automation](linkedin/04-automation.png) — manual/daily triggers, summary request, and parallel Telegram and Google Sheets branches. [Editable SVG](automation-workflow.svg).
5. [Task Lifecycle & KPI Logic](linkedin/05-metrics.png) — a typical status progression, the seven KPI relationships, and no invented results. The arrows do not restrict API status changes. [Editable SVG](operational-metrics.svg).

Do not include the sanitized workflow JSON itself, private local database files, Google Sheets screenshots containing account data, or Telegram configuration.
