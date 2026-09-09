from config import create_app, api
from models import User, Project, Task, PrioritizationRun  # noqa: F401 (needed for Flask-Migrate)
from resources import (
    ProjectListResource,
    ProjectResource,
    TaskListResource,
    TaskResource,
    PrioritizeResource,
)
from auth_resources import (
    SignupResource,
    LoginResource,
    LogoutResource,
    CheckSessionResource,
)

# IMPORTANT: resource registration must happen BEFORE create_app() is
# called, or routes will silently fail to register (confirmed gotcha
# from the Pagination lab).
api.add_resource(SignupResource, "/signup")
api.add_resource(LoginResource, "/login")
api.add_resource(LogoutResource, "/logout")
api.add_resource(CheckSessionResource, "/check_session")

api.add_resource(ProjectListResource, "/projects")
api.add_resource(ProjectResource, "/projects/<int:id>")
api.add_resource(TaskListResource, "/tasks")
api.add_resource(TaskResource, "/tasks/<int:id>")
api.add_resource(PrioritizeResource, "/projects/<int:id>/prioritize")

app = create_app("development")


@app.route("/")
def index():
    return {"message": "Smart Task Prioritizer API is running."}


if __name__ == "__main__":
    app.run(port=5555, debug=True)
