from flask import jsonify, request
from app import app, auth
from app.models import User
from app.models import db


db.create_all()


@app.route("/auth/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    if username and password:
        if not User.query.filter_by(username=username).first():
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "created user"}), 201
        return jsonify({"message": "Username already exists."}), 401
    return jsonify({
                   "message": "You are required to pass username and password"
                   }), 401


@app.route("/auth/login", methods=["POST"])
def login():
    if not request.json['username'] or not request.json['password']:
        return jsonify({"message": "Need username and password to login"}), 401
    else:
        username = request.json.get("username")
        password = request.json.get("password")
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return jsonify({"message": "Username or password is invalid."
                            }), 406
        else:
            return jsonify({
                           'token': user.generate_auth_token().decode('utf-8')
                           })
