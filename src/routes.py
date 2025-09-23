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