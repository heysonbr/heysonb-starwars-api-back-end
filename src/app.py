from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites_people, Favorites_planets
import os

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    all_user = list(map(lambda x: x.serialize(), user))
    return jsonify(all_user), 200

@app.route('/users/<int:id>', methods=['GET'])    
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.get_json()
    user = User(username=request_body["username"], email=request_body["email"], password=request_body["password"], is_active=True, favorites_people=[], favorites_planets=[])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/people', methods=['GET'])
def handle_people():
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    return jsonify(all_people), 200

@app.route('/people', methods=['POST'])
def create_people():
    request_body = request.get_json()
    people = People(name=request_body["name"], birth_year=request_body["birth_year"], height=request_body["height"], mass=request_body["mass"], hair_color=request_body["hair_color"],gender=request_body["gender"])
    db.session.add(people)
    db.session.commit()
    return jsonify(people.serialize()), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_single_people(id):
    people = People.query.get(id)
    if people is None:
        raise APIException("People not found", status_code=404)
    return jsonify(people.serialize()), 200

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):
    people = People.query.get(id)
    if people is None:
        raise APIException("People not found", status_code=404)
    db.session.delete(people)
    db.session.commit()
    return jsonify(people.serialize()), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planets.query.get(id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    request_body = request.get_json()
    planet = Planets(name=request_body["name"],terrain=request_body["terrain"], gravity=request_body["gravity"], population=request_body["population"], rotation_period=request_body["rotation_period"], orbital_period=request_body["orbital_period"], diameter=request_body["diameter"], surface_water=request_body["surface_water"])
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planets.query.get(id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    db.session.delete(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 200

# @app.route('/users/favorites', methods=['GET'])
# def list_favorites():
#     favorite = Favorites.query.all()
#     all_favorites = list(map(lambda x: x.serialize(), favorite))
#     return jsonify(all_favorites), 200

@app.route('/users/<int:id>/favorites/', methods=['GET'])    
def get_user_favorites(id):
    user = User.query.get(id)
    if user is None:
        raise APIException("User not found", status_code=404)
    return jsonify(user.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')

    # Verifica si el planeta y el usuario existen
    planet = Planets.query.get(planet_id)
    user = User.query.get(user_id)
    if planet is None or user is None:
        raise APIException("Planet or User not found", status_code=404)

    favorite_planet = Favorites_planets(planet_id=planet_id, user_id=user_id)
    db.session.add(favorite_planet)
    db.session.commit()
    return jsonify(favorite_planet.serialize()), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id')
    favorite_people = Favorites_people(people_id=people_id, user_id=user_id)
    db.session.add(favorite_people)
    db.session.commit()
    return jsonify(favorite_people.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    del_fav_planet = Favorites_planets.query.filter_by(planet_id=planet_id, user_id=user_id).first()
    if del_fav_planet is None:
        raise APIException("Planet not found", status_code=404)
    else:
        db.session.delete(del_fav_planet)
        db.session.commit()
        return jsonify({"msg": f"Personaje {planet_id} eliminado de favoritos"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.json.get('user_id')
    del_fav_people = Favorites_people.query.filter_by(people_id=people_id, user_id=user_id).first()
    if del_fav_people is None:
    
       
        db.session.delete(del_fav_people)
        db.session.commit()
        return jsonify({"msg": f"Personaje {people_id} eliminado de favoritos"}), 200
    else:
        raise APIException("Personaje no encontrado", status_code=404)
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)