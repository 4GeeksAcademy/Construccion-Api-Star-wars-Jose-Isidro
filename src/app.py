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
from models import db, User, People, Planet , Favorite ,People_favorite ,Planet_favorite
#from models import Person

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

@app.route('/users', methods=['GET'])
def get_users():
    all_user = User.query.all()
    all_user = list(map(lambda x: x.serialize(), all_user))

    return jsonify(all_user), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    all_favorite = Favorite.query.all()
    result = []
    for i in all_favorite:
        result.append(i.serialize())
    return jsonify(result), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))

    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    person = People.query.get(people_id)

    return jsonify(person), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id)

    return jsonify(planet), 200

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def post_planet(planet_id):

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"msg": "Planeta no existe"}), 404
    # puse este "user_id" porque aun no tengo token
    user_id = 1

    new_fav = Planet_favorite(
        user_id=user_id,
        planeta_id=planet_id
    )

    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 201

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def post_person(people_id):

    people = People.query.get(people_id)

    if not people:
        return jsonify({"msg": "Personaje no existe"}), 404
    # puse este "user_id" porque aun no tengo token
    user_id = 1

    new_fav = People_favorite(
        user_id=user_id,
        people_id=people_id
    )

    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 201

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet_favorite(planet_id):
    # puse este "user_id" porque aun no tengo token
    user_id = 1

    planeta = Planet_favorite.query.filter_by(user_id = user_id , planeta_id = planet_id).first()

    if not planeta:
        return jsonify({"msg": "Planet not exit"}),404
    
    db.session.delete(planeta)
    db.session.commit()

    return jsonify({"msg" : "planeta eliminado de favoritos"}),200

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_people_favorite(people_id):
    # puse este "user_id" porque aun no tengo token
    user_id = 1

    person = People_favorite.query.filter_by(user_id = user_id , person_id = people_id).first()

    if not person:
        return jsonify({"msg": "Personaje not exit"}),404
    
    db.session.delete(person)
    db.session.commit()

    return jsonify({"msg" : "personaje eliminado de favoritos"}),200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
