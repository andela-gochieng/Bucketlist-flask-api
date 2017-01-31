from flask import g, jsonify, request
from app.models import User, Bucketlist, Item
from app import app
from app.models import db
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
    g.user = User.query.filter_by(id=user_id).first()
    return True


@app.route('/bucketlists/<int:id>/items/', methods=['POST'])
@auth.login_required
def add_item(id):
    '''Creates an item by providing a unique name of the item to be
    created and the ID of the bucketlist'''

    name = request.json.get('name')
    if Bucketlist.query.filter_by(id=id, created_by=g.user.id).first():
        if not Item.query.filter_by(name=name, bucketlist_id=id).first():
            if len(name) == 0:
                return jsonify({"message": "Missing name."}), 400
            db.session.add(Item(bucketlist_id=id, name=name))
            db.session.commit()
            return jsonify({"message": "Item created."}), 201

        else:
            return jsonify({"message": "Item name already exists."}), 400
    return jsonify({'message': 'Bucketlist not found'}), 404


@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['GET'])
@auth.login_required
def get_item(id, item_id):
    '''Enables viewing of one item specified by the ID number'''

    if not Bucketlist.query.filter_by(created_by=g.user.id,id=id).first():
        return jsonify({"message": "Bucketlist does not exist"})
    item = Item.query.filter_by(bucketlist_id=id,id=item_id).first()
    if item:
        return jsonify(item.return_data()), 200
    return jsonify({"message": "Item not found"}), 404


@app.route('/bucketlists/<int:id>/items/', methods=['GET'])
@auth.login_required
def get_all_items(id):
    '''Enables viewing of all the buckelists belonging to the current user.
    Shows the details of each buckelist and its subsequent items '''

    if not Bucketlist.query.filter_by(created_by=g.user.id,id=id).first():
        return jsonify({"message": "Bucketlist does not exist"})
    items = db.session.query(Item).filter_by(bucketlist_id=id).all()
    list_items = []
    for n in items:
        list_items.append(n.return_data())
    return jsonify(list_items), 200


@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(id, item_id):
    '''Allows the change of the name of the item but the name must not
    already exist. The done status can also be changed to true of false'''

    if not Bucketlist.query.filter_by(created_by=g.user.id,id=id).first():
        return jsonify({"message": "Bucketlist does not exist"}), 404
    name = request.json.get("name")
    done = request.json.get("done")
    item = Item.query.filter_by(id=item_id, bucketlist_id=id).first()
    name_msg = ''
    if not item:
        return jsonify({"message": "Item not found."}), 404
    if name:
        if Item.query.filter_by(name=name, bucketlist_id=id).first():
            return jsonify({"message": "Item name already exists."}), 401
        item.name = name
        db.session.commit()
        name_msg = 'Item name updated'
    if done:
        if done.lower() == "true":
            item.done = True
        else:
            item.done = False
        db.session.commit()
        return jsonify({"message": "Done status updated."}), 202
    if name_msg:
        return jsonify({'message': name_msg})
    if  not name and not done:
        return jsonify({"message": "Missing parameter."}), 400


@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(id, item_id):
    '''Permanently removes the item from the list of items in the specified 
    buckelist'''

    if Bucketlist.query.filter_by(id=id, created_by=g.user.id).first():
        item = Item.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Item deleted"}), 200
        return jsonify({"message": "Item not found"}), 404
    return jsonify({'message': "Bucketlist not found"}), 404
