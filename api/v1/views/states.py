#!/usr/bin/python3
"""
Create a new view for State objects 
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.state import State


@app_views.route("/states/")
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
    if x == None:
        abort(400)
    obj = x.to_dict()
    return jsonify(obj)
