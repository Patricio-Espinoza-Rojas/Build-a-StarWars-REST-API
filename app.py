from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Characters, Planets, User , favorite_character , favorite_planet , favorite_vehicle

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JSON_SORT_KEYS'] = False
 
db.init_app(app)
Migrate(app,db)
CORS(app)

@app.route('/', methods=['GET'])
def root():
    return jsonify({"msg" : "API REST FLASK"},200)

@app.route('/people', methods=['GET'])
def get_people():
    characters = Characters.query.all()
    characters = list(map(lambda character: character.serialize(),characters))

    return jsonify(characters),200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id):
    character = Characters.query.get(id)
    return jsonify(character.serialize()),200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.serialize(),planets))
    return jsonify(planets),200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planets.query.get(id)
    return jsonify(planet.serialize()),200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(),users))
    return jsonify(users),200

@app.route('/users/favorites', methods=['GET'])
def get_users_with_favorites():
    users = User.query.all()
    users = list(map(lambda user: user.serialize_with_favorites(),users))
    return jsonify(users),200

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST','DELETE'])
def post_favorite_planet(user_id,planet_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        planets = Planets.query.get(planet_id)

        user.favorite_planet.append(planets)

        user.save()

    if request.method == 'DELETE':
        user = User.query.get(user_id)
        fav_planet = user.favorite_planet
        fav_planet_filtered = filter(lambda planet: planet != Planets.query.get(planet_id),fav_planet)
        user.favorite_planet = list(fav_planet_filtered)
        user.save()

    return jsonify({"user" : user.serialize_with_favorites()}) , 200

@app.route('/users/<int:user_id>/favorite/people/<int:character_id>', methods=['POST','DELETE'])
def post_favorite_character(user_id,character_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        characters = Characters.query.get(character_id)

        user.favorite_character.append(characters)
        user.save()
    
    if request.method == 'DELETE':
        user = User.query.get(user_id)
        fav_character = user.favorite_character
        fav_character_filtered = filter(lambda character: character != Characters.query.get(character_id),fav_character)
        user.favorite_character = list(fav_character_filtered)
        user.save()
    
    return jsonify({"user" : user.serialize_with_favorites()}),200

if __name__ == '__main__':
    app.run()