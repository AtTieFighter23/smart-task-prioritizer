from config import ma
from models import Project, Task, PrioritizationRun


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        include_fk = True


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)

    class Meta:
        model = Project
        load_instance = True
        include_fk = True


class PrioritizationRunSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PrioritizationRun
        load_instance = True
        include_fk = True


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
prioritization_run_schema = PrioritizationRunSchema()
