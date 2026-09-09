from datetime import datetime

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ai import get_priority_ranking
from config import db
from models import Project, Task, PrioritizationRun
from schemas import project_schema, projects_schema, task_schema, tasks_schema


def parse_due_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def require_login():
    """Returns (user_id, None) if logged in, or (None, (body, status)) if not.
    Callers should `return error` immediately when error is not None."""
    user_id = session.get("user_id")
    if not user_id:
        return None, ({"error": "Not authenticated."}, 401)
    return user_id, None


class ProjectListResource(Resource):
    def get(self):
        user_id, error = require_login()
        if error:
            return error
        projects = Project.query.filter_by(user_id=user_id).all()
        return projects_schema.dump(projects), 200

    def post(self):
        user_id, error = require_login()
        if error:
            return error

        data = request.get_json()
        if not data or "name" not in data:
            return {"error": "name is required."}, 400
        try:
            project = Project(
                name=data["name"],
                description=data.get("description"),
                user_id=user_id,  # always the logged-in user, never client-supplied
            )
            db.session.add(project)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        return project_schema.dump(project), 201


class ProjectResource(Resource):
    def get(self, id):
        user_id, error = require_login()
        if error:
            return error

        project = Project.query.get(id)
        if not project:
            return {"error": "Project not found."}, 404
        if project.user_id != user_id:
            return {"error": "Forbidden."}, 403
        return project_schema.dump(project), 200

    def patch(self, id):
        user_id, error = require_login()
        if error:
            return error

        project = Project.query.get(id)
        if not project:
            return {"error": "Project not found."}, 404
        if project.user_id != user_id:
            return {"error": "Forbidden."}, 403

        data = request.get_json() or {}
        try:
            for attr in ("name", "description"):
                if attr in data:
                    setattr(project, attr, data[attr])
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        return project_schema.dump(project), 200

    def delete(self, id):
        user_id, error = require_login()
        if error:
            return error

        project = Project.query.get(id)
        if not project:
            return {"error": "Project not found."}, 404
        if project.user_id != user_id:
            return {"error": "Forbidden."}, 403

        db.session.delete(project)
        db.session.commit()
        return {}, 204


class TaskListResource(Resource):
    def get(self):
        user_id, error = require_login()
        if error:
            return error
        tasks = Task.query.join(Project).filter(Project.user_id == user_id).all()
        return tasks_schema.dump(tasks), 200

    def post(self):
        user_id, error = require_login()
        if error:
            return error

        data = request.get_json()
        if not data or "title" not in data or "project_id" not in data:
            return {"error": "title and project_id are required."}, 400

        project = Project.query.get(data["project_id"])
        if not project or project.user_id != user_id:
            return {"error": "Invalid project_id."}, 400

        try:
            task = Task(
                title=data["title"],
                description=data.get("description"),
                due_date=parse_due_date(data.get("due_date")),
                user_priority=data.get("user_priority", "medium"),
                status=data.get("status", "not_started"),
                project_id=project.id,
            )
            db.session.add(task)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        return task_schema.dump(task), 201


class TaskResource(Resource):
    def get(self, id):
        user_id, error = require_login()
        if error:
            return error

        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found."}, 404
        if task.project.user_id != user_id:
            return {"error": "Forbidden."}, 403
        return task_schema.dump(task), 200

    def patch(self, id):
        user_id, error = require_login()
        if error:
            return error

        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found."}, 404
        if task.project.user_id != user_id:
            return {"error": "Forbidden."}, 403

        data = request.get_json() or {}
        try:
            if "due_date" in data:
                task.due_date = parse_due_date(data["due_date"])
            for attr in ("title", "description", "user_priority", "status"):
                if attr in data:
                    setattr(task, attr, data[attr])
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        return task_schema.dump(task), 200

    def delete(self, id):
        user_id, error = require_login()
        if error:
            return error

        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found."}, 404
        if task.project.user_id != user_id:
            return {"error": "Forbidden."}, 403

        db.session.delete(task)
        db.session.commit()
        return {}, 204


class PrioritizeResource(Resource):
    def post(self, id):
        user_id, error = require_login()
        if error:
            return error

        project = Project.query.get(id)
        if not project:
            return {"error": "Project not found."}, 404
        if project.user_id != user_id:
            return {"error": "Forbidden."}, 403

        open_tasks = [t for t in project.tasks if t.status != "completed"]
        if not open_tasks:
            return {"error": "No open tasks to prioritize."}, 400

        try:
            ranking, raw_response = get_priority_ranking(open_tasks)
        except RuntimeError as e:
            return {"error": str(e)}, 502

        tasks_by_id = {t.id: t for t in open_tasks}
        for entry in ranking:
            task = tasks_by_id.get(entry.get("task_id"))
            if task:
                task.priority_rank = entry.get("rank")
                task.ai_rationale = entry.get("rationale")

        run = PrioritizationRun(project_id=project.id, raw_response=raw_response)
        db.session.add(run)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to save prioritization results: {e}"}, 500

        return tasks_schema.dump(open_tasks), 200
