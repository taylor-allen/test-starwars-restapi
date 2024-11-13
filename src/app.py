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
from models import db, People, User, Planets, Favorites

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/people", methods=["GET"])
def get_all_people():
    all_people = People.query.all()
    people_serialize = [people.serialize() for people in all_people]
    return jsonify(people_serialize), 200


@app.route("/people/<int:person_id>", methods=["GET"])
def get_each_person(person_id):
    person = People.query.filter_by(id=person_id).first()

    return jsonify(person.serialize()), 200


@app.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    users_serialize = [user.serialize() for user in all_users]
    return jsonify(users_serialize), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_each_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    return jsonify(user.serialize()), 200


@app.route("/planets", methods=["GET"])
def get_all_planets():
    all_planets = Planets.query.all()
    planets_serialize = [planets.serialize() for planets in all_planets]
    return jsonify(planets_serialize), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_each_planets(planet_id):
    planets = Planets.query.filter_by(id=planet_id).first()

    return jsonify(planets.serialize()), 200


@app.route("/users/<int:id>/favorites", methods=["GET"])
def get_user_favorites(id):
    all_favorites = Favorites.query.filter_by(user_id=id)
    favorites_serialize = [favorites.serialize() for favorites in all_favorites]
    return jsonify(favorites_serialize()), 200


@app.route("/users/<int:user_id>/favorites/planets/<int:planet_id>", methods=["POST"])
def post_favorite_planet(user_id, planet_id):
    favorite = Favorites(user_id=user_id, planet_id=planet_id, person_id="NULL")
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200


@app.route("/users/<int:user_id>/favorites/people/<int:person_id>", methods=["POST"])
def post_favorite_person(user_id, person_id):
    favorite = Favorites(user_id=user_id, person_id=person_id, planet_id="NULL")
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200


@app.route(
    "/users/<int:user_id>/favorites/planets/<int:planets_id>", methods=["DELETE"]
)
def delete_favorite_planet(user_id, planet_id):
    planet = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    db.session.delete(planet)
    db.session.commit()
    return jsonify("You deleted a favorite planet")


@app.route("/users/<int:user_id>/favorites/people/<int:person_id>", methods=["DELETE"])
def delete_favorite_person(user_id, person_id):
    person = Favorites.query.filter_by(user_id=user_id, person_id=person_id).first()
    db.session.delete(person)
    db.session.commit()
    return jsonify("You deleted a favorite person")


# example


@app.route("/people", methods=["POST"])
def post_people():
    data = request.get_json()
    people = People(name=data["name"], homeworld=data["homeworld"])
    db.session.add(people)
    db.session.commit()
    return jsonify(people.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
