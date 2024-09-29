"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Ingredient, Cocktail, Dish, Favorite, Pairing
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import logging
# El módulo logging en Python se utiliza para registrar mensajes sobre eventos que ocurren durante la ejecución de un programa
# Configurar logging en el nivel DEBUG
logging.basicConfig(level=logging.DEBUG)
# DEBUG: Información detallada, útil para diagnosticar problemas.
# INFO: Mensajes informativos que resaltan el progreso normal de la aplicación.
# WARNING: Indica que algo inesperado ocurrió, o que hay algún problema en el futuro (ej. uso de una función obsoleta).
# ERROR: Indica un error que impide que una función realice su tarea.
# CRITICAL: Un error grave, indicando que la aplicación puede no ser capaz de continuar.

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# endpoints sobre usuarios
@api.route("/users", methods = ["GET"])
def get_users():
    users = User.query.all()
    return jsonify ([user.serialize() for user in users])


@api.route("/user/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    # obtiene todos los usuarios o da error
    user = User.query.get_or_404(user_id)
    # devuelve una lista con todos los usuarios
    return jsonify (user.serialize())


@api.route ("/new-user", methods = ["POST"])
def create_user():
    # obtiene la data
    data = request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    # obtiene contraseña
    password = data.get("password")
    if not password:
        return jsonify({"error": "Password is required"}), 400
    # seguridad
    hashed_password = generate_password_hash (password)
    # nuevo usuario
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
    # obtiene la data
    data =request.json
    if not data:
        return jsonify ({"error" : "No imput data provided"}), 400
    # obtiene el usuario por el id
    user = User.query.get(user_id)
    if not user:
        return jsonify ({"error" : "User not found"}), 404
    # para actualizar
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
    # obtiene el usuario
    user = User.query.get(user_id)
    # si no se encuentra
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        # elimina
        db.session.delete(user) 
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User deleted successfully"}), 200

# endpoints ingredientes
@api.route ("/ingredients", methods = ["GET"])
def get_ingredients():
    # obtiene todos los ingredientes
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.serialize() for ingredient in ingredients])


@api.route ("/ingredient/<int:Ingredient_id>", methods =["GET"])
def get_ingredient(Ingredient_id):
    # obtiene el ingrediente por el id o da error
    ingredient = Ingredient.query.get_or_404(Ingredient_id)
    return jsonify (ingredient.serialize())


@api.route ("/ingredient", methods = ["POST"])
def create_ingredient():
    # obtiene la data
    data = request.json
    if not data:  # si no hay data
        return jsonify ({"Error" : "Not imput data provided"}), 404
    ingredient = data.get
    if not ingredient:
        return jsonify ({"Error" : "Ingredient is required"})
    # nuevo ingrediente
    new_ingredient = Ingredient (
        name = data.get ("name"),
        type = data.get("type")
    )
    db.session.add(new_ingredient)
    db.session.commit()

    return jsonify(new_ingredient.serialize())

@api.route("/update-ingredient/<int:Ingredient_id>", methods=["PUT"]) 
def update_ingredient(Ingredient_id):
    # obtiene la data
    data = request.json
    if not data:
        return jsonify ({"Error" : "not input data provided"}), 400
    # busca el ingrediente por el id
    ingredient = Ingredient.query.get(Ingredient_id)
    if not ingredient:
        return jsonify ({"Error" : "Ingredient not found"}), 404
    # actualiza ingrediente
    ingredient.name = data.get( "name", Ingredient.name)
    try:
        db.session.commit()
    except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}), 500
   

    return jsonify ({"msg" : "Ingredient updated succesfuly"}), 200

@api.route("/delete-ingredient/<int:Ingredient_id>", methods = ["DELETE"])
def delete_ingredient(Ingredient_id):
    # busca el ingrediente por el id
    ingredient = Ingredient.query.get(Ingredient_id)
    if not ingredient:
        # si no lo encuentra
        return jsonify ({"Error" : " Ingredient not found"}), 404
    
    try:
        # elimina ingrediente
        db.session.delete (ingredient)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify ({"msg" : "Ingredient delete succesfuly"})
                                                                
# endpoints cocktails
@api.route("/cocktails", methods = ["GET"])
def get_cocktails():
    # obtiene todos los cockteles
    cocktails = Cocktail.query.all()
    return jsonify ([cocktail.serialize() for cocktail in cocktails])



@api.route ("/cocktail/<int:Cocktail_id>", methods = ["GET"])
def get_cocktail(Cocktail_id):
    # obtiene el cocteles por el id
    cocktail = Cocktail.query.get_or_404(Cocktail_id)
    return jsonify (cocktail.serialize())


@api.route("/post-cocktail", methods =["POST"])
def create_cocktail():
    # busca la data
    data = request.json
    if not data:
        # si no la encuentra
        return jsonify({"Error" : "not input data provided"}), 400
    cocktail = data.get # busca el cocktel para crear
    if not cocktail: # si no lo encuentra
        return jsonify ({"Error" : "Cocktail is required"}), 404
    # nuevo coctel
    new_cocktail = Cocktail (
        name = data.get ("name"),
        preparation_steps = data.get ("preparation_steps"),
        flavor_profile = data.get ("flavor_profile")
    )
    db.session.add(new_cocktail)
    db.session.commit()
    return jsonify(new_cocktail.serialize())



@api.route("/update-cocktail/<int:Cocktail_id>", methods=["PUT"])
def update_cocktail(Cocktail_id):
    data = request.json
    if not data: ({"Error" : "not input data provided"}), 400
    # busca el coctel por el id
    cocktail = Cocktail.query.get (Cocktail_id)
    # si no lo encuentra
    if not cocktail: ({"Error": "Cocktail not found"}), 404
    # actualizacion coctel
    cocktail.name = data.get ("name", Cocktail.name)
    cocktail.preparation_steps = data.get ("preparation_steps", Cocktail.preparation_steps)
    cocktail.flavor_profile = data.get ("flavor_profile", Cocktail.flavor_profile)
    try:
        db.session.commit()
        return jsonify({"Success": "Cocktail updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error" : str(e)}), 500
    


@api.route("/delete-cocktail/<int:Cocktail_id>", methods=["DELETE"])
def delete_cocktail(Cocktail_id):
    # busca el coctel
    cocktail = Cocktail.query.get(Cocktail_id)
    if not cocktail:
        return jsonify({"Error" : "Cocktail not found"}), 404
    try:
        # elimina
        db.session.delete(cocktail)
        db.session.commit()
    except Exception as e:
        db.rollback()
        return jsonify ({"Error" : str(e)}), 500
    
    return jsonify ({"msg" : "Ingredient delete succesfuly"})


# endpoints platos
@api.route("/get-dishes", methods =["GET"])
def get_dishes():
    # obtiene todos los platos
    dishes = Dish.query.all()
    return jsonify ([dish.serialize()for dish in dishes])
    


@api.route("/get-dish/<int:Dish_id>", methods=["GET"])
def get_dish(Dish_id):
    # obtiene el plato por el id o da error
    dish = Dish.query.get_or_404(Dish_id)
    return jsonify (dish.serialize())


@api.route("/post-dish", methods=["POST"])
def post_dish():
    data= request.json
    if not data: ({"Error" : "not input data provided"})
    dish = data.get
    if not dish: ({"Error":"Dish is required"})
    # nuevo plato
    new_dish = Dish (
        name = data.get ("name"),
        preparation_steps = data.get ("preparation_steps"),
        flavor_profile = data.get ("flavor_profile")
    )
    db.session.add(new_dish)
    db.session.commit()
    return jsonify(new_dish.serialize())


@api.route("/update-dish/<int:Dish_id>", methods=["PUT"])
def update_dish(Dish_id):
    # convierte la data json
    data = request.json
    if not data: ({"Error" : "not input data provided"}), 400
    # busca el plato por el id
    dish = Dish.query.get (Dish_id)
    if not dish: ({"Error": "Dish not found"}), 404
    # actualizacion del plato
    dish.name = data.get ("name", Dish.name)
    dish.preparation_steps = data.get ("preparation_steps", Dish.preparation_steps)
    dish.flavor_profile = data.get ("flavor_profile", Dish.flavor_profile)
    try:
        db.session.commit()
        return jsonify({"Success": "Dish updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error" : str(e)}), 500
    


@api.route("/delete-dish/<int:Dish_id>", methods=["DELETE"])
def delete_dish(Dish_id):
    # obtiene plato por id
    dish = Dish.query.get(Dish_id)
    if not dish:
        return jsonify({"Error" : "Dish not found"}), 404
    try:
        # elimina
        db.session.delete(dish)
        db.session.commit()
    except Exception as e:
        db.rollback()
        return jsonify ({"Error" : str(e)}), 500
    
    return jsonify ({"msg" : "Dish delete succesfuly"})


# endpoints favoritos
@api.route("/get-favourites", methods =["GET"])
def get_favourites():
    # obtiene todos los favoritos
    favorites = Favorite.query.all
    return jsonify ([favorite.serialize() for favorite in favorites])


@api.route("/get-favorite/<int:favorite_id>", methods=["GET"])
def get_favorite(favorite_id):
    # obtiene el favorito por el id o da error
    favorite = Favorite.query.get_or_404 (favorite_id)
    return jsonify (favorite.serialize())


@api.route("/post-favorite", methods=["POST"])
def create_favorite():
    # convierte la data a json
    data = request.json
    if not data:
        return {"Error": "No input data provided"}, 400
# necesario
    user_id = data.get('user_id')
    cocktail_id = data.get('cocktail_id')
    dish_id = data.get('dish_id')
# si no encuentra ningun id asociado a ningun plato o cocktel
    if not user_id or (not cocktail_id and not dish_id):
        return {"Error": "User ID and either Cocktail ID or Dish ID are required"}, 400
# si encuentra un id de plato y de cocktel
    if cocktail_id and dish_id:
        return {"Error": "You can only favorite either a dish or a cocktail, not both"}, 400

    # Crear el favorito
    new_favorite = Favorite(
        user_id=user_id,
        cocktail_id=cocktail_id,
        dish_id=dish_id
    )

    try:
        db.session.add(new_favorite)
        db.session.commit()
        return new_favorite.serialize(), 201
    except Exception as e:
        db.session.rollback()
        # Agregar el logging del error
        logging.exception("Error occurred during favorite creation")
        # Devolver el mensaje de error exacto
        return {"Error": str(e)}, 500
    


@api.route("/update-favorite/<int:fav_id>", methods=["PUT"])
def update_favorite(fav_id):
    data = request.json
    if not data:
        return {"Error": "No input data provided"}, 400

    # Obtener los nuevos valores de cocktail_id y dish_id
    cocktail_id = data.get('cocktail_id')
    dish_id = data.get('dish_id')

    # Verificar si al menos uno de los IDs se proporciona
    if not cocktail_id and not dish_id:
        return {"Error": "Either Cocktail ID or Dish ID is required"}, 400

    # Buscar el favorito existente
    favorite = Favorite.query.get(fav_id)
    if not favorite:
        return {"Error": "Favorite not found"}, 404

    # Actualizar los campos según los datos proporcionados
    if cocktail_id is not None:
        favorite.cocktail_id = cocktail_id
    if dish_id is not None:
        favorite.dish_id = dish_id

    try:
        db.session.commit()
        return favorite.serialize(), 200
    except Exception as e:
        db.session.rollback()
        # Log the error for debugging
        logging.error("Error committing to the database: %s", str(e))
        return {"Error": str(e)}, 500



@api.route("/delete-favorite/<int:favorite_id>", methods=["DELETE"])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        return {"Error": "Favorite not found"}, 404

    try:
              # elimina
        db.session.delete(favorite)
        db.session.commit()
    except Exception as e:
        db.rollback()
        return jsonify ({"Error" : str(e)}), 500
    
    return jsonify ({"msg" : "Favorite delete succesfuly"})




@api.route("/get-pairings", methods =["GET"])
def get_pairings():
    pairings = Pairing.query.all()
    return jsonify([pairing.serialize() for pairing in pairings])


@api.route("/get-pairing/<int:pairing_id>")
def get_pairing(pairing_id):
    