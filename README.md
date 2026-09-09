# Smart Task Prioritizer

A full-stack productivity application that helps users cut through task-list overwhelm. Users organize tasks under projects, and can request an AI-generated priority ranking — with a short rationale for each task — based on due dates and a user-set priority level.

## Problem

Flat to-do lists treat every task as equally urgent. This app removes the daily guesswork of deciding what to work on next by combining due dates, user judgment, and AI-assisted reasoning into a single ranked view.

## Tech Stack

**Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-RESTful, Marshmallow, Flask-Bcrypt
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

✅ Core features complete: authentication, full CRUD, AI prioritization, and pagination are all implemented and tested.

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

The seed script prints a demo login (`demo_user` / `password123`) for quick testing.

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

## Core Functionality

- **Authentication** — sign up or log in with a username and password (hashed with bcrypt). Sessions persist across page reloads via a secure cookie.
- **Ownership-based access control** — every project and task belongs to exactly one user. The API enforces this at the resource level: a logged-in user can only view, edit, or delete their own data, even if they know another user's project/task ID.
- **Project & Task CRUD** — create, view, edit, and delete projects and tasks. Each task supports a due date, a user-set priority (low/medium/high), and a status (not started/in progress/completed).
- **AI-powered prioritization** — clicking "Prioritize tasks" on a project sends its open tasks (title, due date, priority) to the Gemini API, which returns a suggested rank and a short rationale for each task. Tasks re-sort automatically by rank, and every prioritization run is logged to the database for reference.
- **Pagination** — `GET /projects` and `GET /tasks` support `?page=` and `?per_page=` query parameters and return paginated results with metadata (`total`, `pages`, etc.). The project sidebar uses this directly with a "Load more" control once a user has more than 10 projects.
- **Error handling** — invalid input, missing/incorrect credentials, unauthorized access attempts, and AI API failures (including quota limits and transient outages) all return clear, structured error responses instead of crashing.

## Usage

1. Sign up for an account (or log in with the demo credentials above).
2. Add a project from the sidebar.
3. Open it and add a few tasks, each with a due date and priority level.
4. Click **Prioritize tasks** to get an AI-ranked order with a short rationale for each task.

## Notes

- The Gemini free tier has daily request limits per model; if prioritization fails with a quota error, it resets at midnight Pacific Time.

## Author

AtTieFighter23