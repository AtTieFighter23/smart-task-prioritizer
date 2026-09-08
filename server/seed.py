from config import create_app, db
from models import User, Project, Task

app = create_app("development")

with app.app_context():
    Task.query.delete()
    Project.query.delete()
    User.query.delete()

    demo_user = User(username="demo_user", password_hash="placeholder")
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
