#!/usr/bin/python3
"""
Main API app
"""
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/medflow/api/v1")
CORS(app, resorces={"*": {'origins': "0.0.0.0"}})

@app.errorhandler(400)
def bad_request(error):
    err_message = {'error': error.description}
    return make_response(jsonify(err_message), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'unauthorized'}), 401)

@app.errorhandler(404)
def not_found(error):
    err_message = {'error': 'not found'}
    return make_response(jsonify(err_message), 404)

@app.teardown_appcontext
def refresh(exception):
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)