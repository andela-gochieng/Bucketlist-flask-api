from flask import g, jsonify, request
from .models import User, Item
from . import app
from .models import db
from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme="Bearer")
db.create_all()

@auth.verify_token
def verify_token(token):
    if not token:
        return False
    user_id = User.verify_auth_token(token=token)
    if not user_id:
        return False
    g.user = db.session.query(User).filter_by(id=user_id).first()
    return True


@app.route('/bucketlists/<int:id>/items', methods=['POST'])
@auth.login_required
def add_item(id):
    name = request.json.get('name')
    if not db.session.query(Item).filter_by(name=name, bucketlist_id=id).first():
        if len(name) == 0:
            return jsonify({"message": "Missing name."}), 401
        db.session.add(Item(bucketlist_id=id,name=name))
        db.session.commit()
        return jsonify({"message":"Item created."}), 201

    else:
        return jsonify({"message": "Item name already exists."}), 401



@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['GET'])
@auth.login_required
def get_item(id, item_id):
    item = db.session.query(Item).get(item_id)
    return jsonify(item.return_data()), 200

@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(id, item_id):
    name = request.json.get("name")
    if len(name)==0:
        return jsonify({"message": "Missing name."})
    bl = db.session.query(Item).filter_by(id=item_id, bucketlist_id=id).first()
    if not bl:
        return jsonify({"message":"Item not found."})
    bl.name = name               
    db.session.commit()
    return jsonify({"message":"Item name updated."}), 200


@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(id, item_id):
    item = db.session.query(Item).get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message":"Item deleted"})
    return jsonify({"message":"Item not found"})

