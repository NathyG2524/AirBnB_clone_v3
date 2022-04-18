#!/usr/bin/python3
"""
Create a new view for User objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import make_response, request, abort, jsonify
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def user_states_view():
    """return all users"""
    list = []
    for value in storage.all(User).values():
        list.append(value.to_dict())
    return jsonify(list)


@app_views.route("/users/<user_id>",  methods=['GET'])
def user_state_view(user_id):
    """return user objects"""
    x = storage.get(User, user_id)
    if x is None:
        abort(404)
    obj = x.to_dict()
    return jsonify(obj)


@app_views.route("/users/<user_id>", methods=['GET', 'DELETE'])
def user_delete_views(user_id):
    """Delete user object with the given user_id"""
    x = storage.get(User, user_id)
    if not x:
        abort(404)
    x.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=['POST'])
def user_state_post():
    """create a new user"""
    if not request.get_json():
        return ("Not a JSON", 400)
    if 'email' not in request.get_json():
        return ("Missing email\n", 400)
    if 'password' not in request.get_json():
        return ("Missing password\n", 400)
    new_data = request.get_json()
    new_state = User(**new_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def user_state_put(user_id):
    """update a user with a user_id"""
    x = storage.get(User, user_id)
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
