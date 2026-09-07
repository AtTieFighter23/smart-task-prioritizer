# Smart Task Prioritizer

A full-stack productivity application that helps users cut through task-list overwhelm. Users organize tasks under projects, and can request an AI-generated priority ranking — with a short rationale for each task — based on due dates and a user-set priority level.

## Problem

Flat to-do lists treat every task as equally urgent. This app removes the daily guesswork of deciding what to work on next by combining due dates, user judgment, and AI-assisted reasoning into a single ranked view.

## Tech Stack

**Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow
**Frontend:** React (Vite), React Router
**Database:** SQLite (dev) via SQLAlchemy ORM
**AI Integration:** LLM API (Anthropic or OpenAI) for task prioritization and rationale generation

## Data Models

- **User** — has many Projects
- **Project** — belongs to User, has many Tasks
- **Task** — belongs to Project; includes `due_date`, `user_priority`, `status`, `priority_rank`, `ai_rationale`
- **PrioritizationRun** — belongs to Project; stores the raw AI response for each prioritization request

## Project Structure

- `server/` — Flask API
- `client/` — React frontend
- `README.md`

## Status

🚧 In active development.

## Setup

_Setup instructions will be added as the backend and frontend are scaffolded._

## Author

AtTieFighter23
