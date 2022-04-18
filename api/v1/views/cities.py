#!/usr/bin/python3
"""
create a new view for city objects
that handles all default RESTFul API
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def city_route(state_id):
    """view a city"""
    x = storage.get(State, state_id)
    y = storage.all(City)
    if x is None:
        abort(404)
    list = []
    for cities in y.values():
        if cities.state_id == state_id:
            list.append(cities.to_dict())
    return jsonify(list)


@app_views.route('/cities/<city_id>')
def city_id_route(city_id):
    """retrieves the list of all City objects of a state"""
    x = storage.get(City, city_id)
    if x is None:
        abort(404)
    obj = x.to_dict()
    return jsonify(obj)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    x = storage.get(City, city_id)
    if x is None:
        abort(404)
    x.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Creates a city"""
    x = storage.get(State, state_id)
    if not x:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON", 400)
    if 'name' not in request.get_json():
        return ("Missing name", 400)
    new_data = request.get_json()
    new_data['state_id'] = state_id
    new_city = City(**new_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """updates a city"""
    x = storage.get(City, city_id)
    if x is None:
        abort(404)
    if not request.get_json():
        return ("Not a JSON", 404)
    new_data = request.get_json()
    for key, value in new_data.items():
        setattr(x, key, value)
    x.save()
    return jsonify(x.to_dict()), 200
