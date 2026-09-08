import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt

load_dotenv()  # pulls ANTHROPIC_API_KEY (and anything else) from .env into os.environ

# Shared extension instances (module-level, matching the app-factory pattern).
# IMPORTANT: any api.add_resource(...) calls must happen BEFORE create_app()
# is invoked in app.py, or routes will silently fail to register.
db = SQLAlchemy()
migrate = Migrate()
api = Api()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app(env="development"):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    CORS(app, supports_credentials=True)

    return app
