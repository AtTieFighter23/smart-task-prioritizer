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

    # Frontend (:5173) and backend (:5555) are different ports, which browsers
    # treat as different origins — these settings let the session cookie
    # travel cross-origin. Modern browsers treat http://localhost as secure
    # enough for this even without HTTPS.
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    # Wildcard origins ("*") are rejected by browsers when credentials are
    # involved, so the frontend's exact origin must be named explicitly.
    # Both hostnames are listed since browsers treat localhost and 127.0.0.1
    # as different origins even though they're the same machine.
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    )

    return app