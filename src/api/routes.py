"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route("/users", methods = ["GET"])
def get_users():
    users = User.query.all()
    return jsonify ([user.serialize() for user in users])


@api.route("/user/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify (user.serialize())


@api.route ("/user", methods = ["POST"])
def create_user():
    data = request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    new_user = User (
        name = data.get ("name"),
        username = data.get ("username"),
        email = data.get ("email"),
        password = data.get ("password")  # pendiente hasear contraseña
    )
    db.session.add (new_user)
    db.session.commit()
    return jsonify (new_user.serialize()), 200