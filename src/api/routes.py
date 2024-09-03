"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Ingredient
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash

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


@api.route ("/new-user", methods = ["POST"])
def create_user():
    print(request.method) 
    data = request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    password = data.get("password")
    if not password:
        return jsonify({"error": "Password is required"}), 400
    hashed_password = generate_password_hash (password)
    new_user = User (
        name = data.get ("name"),
        username = data.get ("username"),
        email = data.get ("email"),
        password = hashed_password  
    )
    db.session.add (new_user)
    db.session.commit()
    return jsonify (new_user.serialize()), 200


@api.route ("/user/<int:user_id>", methods =["PUT"])
def update_user (user_id):
    data =request.json
    if not data:
        return jsonify ({"error" : "No imput data provided"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify ({"error" : "User not found"}), 404
    
    user.name = data.get ("name", User.name)
    user.username = data.get ("username", User.username)
    user.email = data.get ("email", User.email)

    new_password = data.get ("password")
    if new_password:
        User.password = generate_password_hash (new_password)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}), 500
        
        return jsonify ({"msg" : "User updated succesfuly"}), 200
    


@api.route("/delete-user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    print(request.method)  

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user) 
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User deleted successfully"}), 200


@api.route ("/ingredients", methods = ["GET"])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.serialize() for ingredient in ingredients])


@api.route ("/ingredient/<int:Ingredient_id>", methods =["GET"])
def get_ingredient(Ingredient_id):
    print(request.method) 
    ingredient = Ingredient.query.get_or_404(Ingredient_id)
    return jsonify (ingredient.serialize())


@api.route ("/ingredient", methods = ["POST"])
def create_ingredient():
    data = request.json
    if not data:
        return jsonify ({"Error" : "Not imput data provider"}), 404
    ingredient = data.get
    if not ingredient:
        return jsonify ({"Error" : "Ingredient is required"})
    new_ingredient = Ingredient (
        name = data.get ("name")
    )
    db.session.add(new_ingredient)
    db.session.commit()

    return jsonify(new_ingredient.serialize())
