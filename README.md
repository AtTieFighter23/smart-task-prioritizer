# Smart Task Prioritizer

A full-stack productivity application that helps users cut through task-list overwhelm. Users organize tasks under projects, and can request an AI-generated priority ranking — with a short rationale for each task — based on due dates and a user-set priority level.

## Problem

Flat to-do lists treat every task as equally urgent. This app removes the daily guesswork of deciding what to work on next by combining due dates, user judgment, and AI-assisted reasoning into a single ranked view.

## Tech Stack

**Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-RESTful, Marshmallow
**Frontend:** React (Vite), React Router
**Database:** SQLite (dev) via SQLAlchemy ORM
**AI Integration:** Google Gemini API for task prioritization and rationale generation

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

### Prerequisites

- Python 3.11+ (this project uses `pyenv` to pin `3.11.9`)
- Node.js and npm
- A free Google Gemini API key ([aistudio.google.com](https://aistudio.google.com) → Get API key)

### Backend (`server/`)

```bash
cd server
pipenv install
pipenv shell
cp .env.example .env
```

Open `.env` and set your real key:

```
GEMINI_API_KEY=your-actual-key-here
```

Set up the database:

```bash
export FLASK_APP=app.py
flask db upgrade
python seed.py
```

Run the server:

```bash
python app.py
```

The API runs at `http://localhost:5555`.

### Frontend (`client/`)

In a separate terminal:

```bash
cd client
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

### Usage

1. Add a project from the sidebar.
2. Open it and add a few tasks, each with a due date and priority level (low/medium/high).
3. Click **Prioritize tasks** to get an AI-ranked order with a short rationale for each task.

## Notes

- This build has no authentication — all projects belong to a single seeded demo user. Auth is planned for a future iteration of this project.
- The Gemini free tier has daily request limits per model; if prioritization fails with a quota error, it resets at midnight Pacific Time.

## Author

AtTieFighter23