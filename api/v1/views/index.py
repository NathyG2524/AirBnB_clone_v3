#!/usr/bin/python3
"""
create a route
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def index_status():
    """return json"""
    return jsonify(status="OK")
