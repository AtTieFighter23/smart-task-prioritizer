from config import create_app, db
from models import User, Project, Task

app = create_app("development")

DEMO_USERNAME = "demo_user"
DEMO_PASSWORD = "password123"

with app.app_context():
    Task.query.delete()
    Project.query.delete()
    User.query.delete()

    demo_user = User(username=DEMO_USERNAME)
    demo_user.password = DEMO_PASSWORD  # hashes via the model's password setter
    db.session.add(demo_user)
    db.session.commit()

    demo_project = Project(
        name="Demo Project",
        description="Seeded for manual testing",
        user_id=demo_user.id,
    )
    db.session.add(demo_project)
    db.session.commit()

    print(f"Seeded User id={demo_user.id}, Project id={demo_project.id}")
    print(f"Login with username='{DEMO_USERNAME}' password='{DEMO_PASSWORD}'")
