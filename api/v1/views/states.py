#!/usr/bin/python3
"""
Create a new view for State objects 
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.state import State


@app_views.route("/state/")
def states_view():
    """return all states"""
    list = [storage.all(State).to_dict()]
    return jsonify(list)
    

@app_views.route("/states/<state_id>",  methods=['GET'])
def state_view(state_id):
    """return state objects"""  
    x = storage.get(State.id)
    if x == None:
        abort(400)
    obj = x.to_dict()
    return jsonify(obj)