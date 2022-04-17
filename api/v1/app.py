#!/usr/bin/python3
"""
first endpoint (route) will be to 
return the status of your API
"""


from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """
     Registers a function to be called 
    when the application context ends. 
    """
    storage.close()

if __name__ == "__main__":
    if os.getenv('HBNB_API_HOST') and os.getenv('HBNB_API_PORT'):
        app.run(host=os.getenv('HBNB_API_HOST'),
                port=os.getenv('HBNB_API_PORT'), threaded=True)
    else:
        app.run(threaded=True)