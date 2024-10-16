"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Character, Planet

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/user/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user1 = User(username=username, password=password)
    db.session.add(user1)
    db.session.commit()

    response_body = {
        "msg": f"Hello, created user {username}"
    }
    return jsonify(response_body), 200

@app.route('/favorites', methods=['POST'])
def create_fave():
    category = request.json.get('category')

    if category == 'character':
        char = Character.query.filter_by(name=request.json.get('name')).first()
        if not char:
            char = Character(
                name=request.json.get('name'),
                gender=request.json.get('gender'),
                eye_color=request.json.get('eye_color'),
                hair_color=request.json.get('hair_color')
            )
            db.session.add(char)

        fave = Favorites(
            name=request.json.get('name'),
            category=category,
            user_id=request.json.get('user_id'),
            character_id=char.id
        )

    elif category == 'planet':
        planet = Planet.query.filter_by(name=request.json.get('name')).first()
        if not planet:
            planet = Planet(
                name=request.json.get('name'),
                climate=request.json.get('climate'),
                mass=request.json.get('mass'),
                population=request.json.get('population'),
                gravity=request.json.get('gravity'),
                terrain=request.json.get('terrain')
            )
            db.session.add(planet)

        fave = Favorites(
            name=request.json.get('name'),
            category=category,
            user_id=request.json.get('user_id'),
            planet_id=planet.id
        )

    db.session.add(fave)
    db.session.commit()

    response_body = {
        "msg": "Favorite has been created successfully"
    }
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if user_id is None:
        return jsonify({"message": "Please provide user ID"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
        return jsonify({"message": "Favorite planet removed"}), 200
    return jsonify({"message": "Planet is not in favorites"}), 404

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if user_id is None:
        return jsonify({"message": "Please provide user ID"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"message": "Character not found"}), 404
    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()
        return jsonify({"message": "Favorite character removed"}), 200
    return jsonify({"message": "Character is not in favorites"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
