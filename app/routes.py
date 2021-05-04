from app import db
from app.models.planet import Planet
from flask import request, Blueprint, make_response, jsonify

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("/<planet_id>", methods=["GET", "PUT", "DELETE"])
def handle_planets(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return make_response("", 404)
    if request.method == "GET":
        return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "size": planet.size
    }
    elif request.method == "PUT":
        form_data = request.get_json()
        planet.name = form_data["name"]
        planet.description =form_data["description"] 
        planet.size = form_data["size"] 
        db.session.commit()
        return make_response(f"planet #{planet.id} successfully updated")
    elif request.method == "DELETE":
        db.session.delete(planet)
        db.session.commit()
        return make_response(f"planet #{planet.id} successfully deleted")

@planets_bp.route("", methods=["GET", "POST"])
def view_planets():
    if request.method == "POST":
        request_body = request.get_json()
        new_planet = Planet(name=request_body['name'],
            description=request_body['description'],
            size=request_body['size'])
        db.session.add(new_planet)
        db.session.commit()
        return make_response(f"Your planet {new_planet.name} was created! It's {new_planet.size} big and it's {new_planet.description}.", 201)
    if request.method == "GET":
        planets = Planet.query.all()
        planets_response = []
        for planet in planets:
            planets_response.append({
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "size": planet.size
            })
        return jsonify(planets_response)