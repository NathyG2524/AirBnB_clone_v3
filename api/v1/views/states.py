#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import make_response, request, abort, jsonify
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def states_view():
    """return all states"""
    list = []
    for value in storage.all(State).values():
        list.append(value.to_dict())
    return jsonify(list)


@app_views.route("/states/<state_id>",  methods=['GET'])
def state_view(state_id):
    """return state objects"""
    x = storage.get(State, state_id)
    if x is None:
        abort(404)
    obj = x.to_dict()
    return jsonify(obj)


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE'])
def delete_views(state_id):
    """Delete state object with the given state_id"""
    x = storage.get(State, state_id)
    if not x:
        abort(404)
    x.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", methods=['POST'])
def state_post():
    """create a new state"""
    if not request.get_json():
        return ("Not a JSON", 400)
    if 'name' not in request.get_json():
        return ("Missing name", 400)
    new_data = request.get_json()
    new_state = State(**new_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def state_put(state_id):
    """update a state with a state_id"""
    x = storage.get(State, state_id)
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
