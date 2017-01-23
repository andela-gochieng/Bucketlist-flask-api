from flask import jsonify, g, current_app
from .models import User
from flask_httpauth import HTTPTokenAuth
from .models import db
from . import app

auth = HTTPTokenAuth()
# auth_token = HTTPBasicAuth()

@app.route("/", methods=["GET"])
def index():
    return "sdsd"