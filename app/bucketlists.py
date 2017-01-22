from flask import g, jsonify, request
from models import User, BucketList
from app import app, db


@app.route('/bucketlists/', methods=['POST'])
def create_bucketlist():
    user = User.query.get_or_404(g.user.id)
    bucketlist = Bucketlist(created_by=user.id)
    if not Bucketlist.query.filter_by(name=data['name'], created_by=g.user.id):
        if len(data['name']) != 0:
            Bucketlist.name = data['name']
        else:
            return'Missing name.'
    else:
        return 'Bucketlist name already exists.'
    db.session.add(bucketlist)
    db.session.commit()
    return {}, 201, {'Location': bucketlist.get_url()}


@app.route('/bucketlists/<int:id>', methods=['GET'])
def get_specific_bucketlist():
    return Bucketlist.query.get_or_404(id)


@app.route('/bucketlists/', methods=['GET'])
def get_all_bucketlists():
    return Bucketlist.query.filter_by(created_by=g.user.id)


@app.route('/bucketlists/<int:id>', methods=['PUT'])
def edit_existing_bucketlist():
    bucketlist = Bucketlist.query.get_or_404(id)
    if data['name']:
        if not Bucketlist.query.filter_by(name=data['name'], created_by=g.user.id):
            if len(data['name']) != 0:
                Bucketlist.name = data['name']
            else:
                return'Missing name.'
    else:
        return 'Bucketlist name already exists.'
    db.session.add(bucketlist)
    db.session.commit()
    return {}



def delete_existing_bucketlist():
    bucketlist = Bucketlist.query.get_or_404(id)
    db.session.delete(bucketlist)
    db.session.commit()
    return {}

