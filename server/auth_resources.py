from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import db
from models import User
from schemas import user_schema


class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get("username") or not data.get("password"):
            return {"error": "username and password are required."}, 400

        user = User(username=data["username"])
        try:
            user.password = data["password"]  # hashes via the model's setter
            db.session.add(user)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except IntegrityError:
            db.session.rollback()
            return {"error": "Username is already taken."}, 400

        session["user_id"] = user.id
        return user_schema.dump(user), 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get("username") or not data.get("password"):
            return {"error": "username and password are required."}, 400

        user = User.query.filter_by(username=data["username"]).first()
        if not user or not user.authenticate(data["password"]):
            return {"error": "Invalid username or password."}, 401

        session["user_id"] = user.id
        return user_schema.dump(user), 200


class LogoutResource(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSessionResource(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Not logged in."}, 401

        user = User.query.get(user_id)
        if not user:
            return {"error": "Not logged in."}, 401

        return user_schema.dump(user), 200
