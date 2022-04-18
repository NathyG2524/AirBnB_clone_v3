#!usr/bin/python3
"""
create a new view for city objects
that handles all default RESTFul API
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.city import State


@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False)
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

@app_views.route('/api/v1/cities/<city_id>')
def city_id_route(city_id):
    """retrieves the list of all City objects of a state"""
    x = storage.get(City, city_id)
    if x is None:
        abort(404)
    obj = x.to_dic()
    return obj
