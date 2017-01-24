from flask import g, jsonify, request
from .models import User, Item
from . import app
from .models import db
from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme="Bearer")
db.create_all()

@app.route('/bucketlists/<int:id>/items', methods=['POST'])
def add_item(id):
    bucketlist = Bucketlist.query.get_or_404(id)
    item = Item(bucketlist_id=bucketlist)
    if not Item.query.filter_by(name=data['name'], bucketlist_id=data['bucketlist_id']):
        if len(data['name']) != 0:
            Item.name = data['name']
        else:
            return jsonify({"message":"Missing name."})
        if 'done' in data:
            Item.done = data['done']
    else:
        return jsonify({"message":"Item name already in use."})
    db.session.add(item)
    db.session.commit()
    return {}, 201, {'Location': item.get_url()}


@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['GET'])
def get_item(id, item_id):
    item = Item.query.filter_by(bucketlist_id=id, id=item_id).first_or_404()
    return jsonify(item.return_data())


@app.route('/bucketlists/<int:id>/items/<int:item_id>')
def update_item(id, item_id):
    item = Item.query.filter_by(bucketlist_id=id, id=item_id).first_or_404()
    if data['name']:
        if not Item.query.filter_by(name=data['name'], bucketlist_id=data['bucketlist_id']):
            if len(data['name']) != 0:
                Item.name = data['name']
            else:
                return jsonify({"message":"Missing name."})
            if 'done' in data:
                Item.done = data['done']
        else:
            return jsonify({"message":"Item name already in use."})
    db.session.add(item)
    db.session.commit()
    return {}


@app.route('/bucketlists/<int:id>/items/<int:item_id>')
def delete_item(id, item_id):
    item = Item.query.filter_by(bucketlist_id=id, id=item_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return {}