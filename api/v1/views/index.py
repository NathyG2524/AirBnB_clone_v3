#!/usr/bin/python3
"""
create a route
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def index_status():
    """return json"""
    return jsonify(status="OK")

@app_views.route('/stats')
def count_obj():
    """count objects"""
    return jsonify(all=storage.count())
