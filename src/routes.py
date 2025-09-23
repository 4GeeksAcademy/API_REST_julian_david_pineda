"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, User, Planets, People, Favorite
from utils import generate_sitemap, APIException
from flask_cors import CORS


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


"""__________________________ User Endpoints_____________________________"""

@api.route('/users', methods=['GET'])
def get_all_user():
    try: 
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    try:
        user_id = request.args.get('user_id', 1, type=int)

        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        favorites_data = []

        for favorite in favorites:
            fav_info = favorite.serialize()

            if favorite.people_id:
                person = People.query.get(favorite.people_id)
                if person:
                    fav_info['details'] = person.serialize()
            elif favorite.planet_id:
                planet = Planets.query.get(favorite.planet_id)
                if planet:
                    fav_info['details'] = planet.serialize()
            
            favorites_data.append(fav_info)
        return jsonify(favorites_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""__________________________ People Endpoints_____________________________"""

@api.route('/people', methods=['GET'])
def get_all_people():
    try:
        people = People.query.all()
        return jsonify([person.serialize() for person in people]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    try:
        person = People.query.get(people_id)
        if person is None:
            return jsonify({"error": "Person not found"}), 404
        return jsonify(person.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""__________________________ Planets Endpoints_____________________________"""

@api.route('/planet', methods=['GET'])
def get_all_planets():
    try: 
        planet = Planets.query.all()
        return jsonify([place.serialize() for place in planet]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    try:
        planet = Planets.query.get(planet_id)
        if planet is None:
            return jsonify({"Error": "Planet no found"}), 404
        return jsonify(planet.serialize()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""__________________________ Favorites Endpoints_____________________________"""

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):

    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 1)

        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        planet = Planets.query.get(planet_id)
        if planet is None:
            return jsonify({"Error": "Planet not found"}), 404
        
        existing = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if existing:
            return jsonify({"error": "Planet already in favorites"}), 400
        
        favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            "message": "Planet add to favorites successfully",
            "favorite": favorite.serialize()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 1)
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        person = People.query.get(people_id)
        if person is None:
            return jsonify({"error": "People not found"}), 404
        existing = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if existing:
            return jsonify({"error": "People already in favorites"}), 400
        
        favorite = Favorite(user_id=user_id, people_id=people_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            "message": "People add to favorites successfully",
            "favorite": favorite.serialize()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    try:
        user_id = request.args.get('user_id', 1, type=int)

        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if favorite is None:
            return jsonify({"error": "Favorite planet not found"}), 404
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Planet removed from favorites successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    try:
        user_id = request.args.get('user_id', 1, type=int)

        favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if favorite is None:
            return jsonify({"error": "Favorite people not found"}), 404
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "People removed from favorites successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
