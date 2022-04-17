#!/usr/bin/python3
"""
create a route
"""

from api.v1.views import app_views

@app_views.route('/status')
def index():
    """return json"""
    return { "status" : "OK" }