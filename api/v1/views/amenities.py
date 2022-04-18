#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import make_response, request, abort, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def amenity_view():
    """return all amenities"""
    list = []
    for value in storage.all(Amenity).values():
        list.append(value.to_dict())
    return jsonify(list)


@app_views.route("/amenities/<amenity_id>",  methods=['GET'])
def amenity_view_id(amenity_id):
    """return amenity objects"""
    x = storage.get(Amenity, amenity_id)
    if x is None:
        abort(404)
    obj = x.to_dict()
    return jsonify(obj)


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE'])
def delete_amenity_views(amenity_id):
    """Delete amenity object with the given amenity_id"""
    x = storage.get(Amenity, amenity_id)
    if not x:
        abort(404)
    x.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/", methods=['POST'])
def amenity_post():
    """create a new amenity"""
    if not request.get_json():
        return ("Not a JSON", 400)
    if 'name' not in request.get_json():
        return ("Missing name", 400)
    new_data = request.get_json()
    new_state = Amenity(**new_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def amenity_put(amenity_id):
    """update a amenity with a amenity_id"""
    x = storage.get(Amenity, amenity_id)
    if x is None:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return make_response("Not a JSON", 400)
    new_data = request.get_json()
    for key, value in new_data.items():
        setattr(x, key, value)
        x.save()
        obj = x.to_dict()
        return jsonify(obj), 200
