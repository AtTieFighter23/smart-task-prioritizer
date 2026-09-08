from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from config import db

VALID_PRIORITIES = ("low", "medium", "high")
VALID_STATUSES = ("not_started", "in_progress", "completed")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    projects = db.relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="projects")
    tasks = db.relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )
    prioritization_runs = db.relationship(
        "PrioritizationRun", back_populates="project", cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty.")
        return name

    def __repr__(self):
        return f"<Project {self.id}: {self.name}>"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    due_date = db.Column(db.Date)
    user_priority = db.Column(db.String, nullable=False, default="medium")
    status = db.Column(db.String, nullable=False, default="not_started")
    priority_rank = db.Column(db.Integer)  # set by the AI prioritization run
    ai_rationale = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    project = db.relationship("Project", back_populates="tasks")

    @validates("title")
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")
        return title

    @validates("user_priority")
    def validate_user_priority(self, key, value):
        if value not in VALID_PRIORITIES:
            raise ValueError(f"user_priority must be one of {VALID_PRIORITIES}.")
        return value

    @validates("status")
    def validate_status(self, key, value):
        if value not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}.")
        return value

    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"


class PrioritizationRun(db.Model):
    __tablename__ = "prioritization_runs"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    raw_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    project = db.relationship("Project", back_populates="prioritization_runs")

    def __repr__(self):
        return f"<PrioritizationRun {self.id} for Project {self.project_id}>"
    