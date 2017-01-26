from flask import g, jsonify, request
from .models import User, Bucketlist
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


@app.route('/bucketlists', methods=['POST'])
@auth.login_required
def create_bucketlist():
    name = request.json.get('name')
    if not db.session.query(Bucketlist).filter_by(
            name=name, created_by=g.user.id).all():
        if len(name) == 0:
            return jsonify({"message": "Missing name."}), 401
    else:
        return jsonify({"message": "Bucketlist name already exists."}), 401
    db.session.add(Bucketlist(created_by=g.user.id, name=name))
    db.session.commit()
    return jsonify({"message": "Bucketlist created."}), 201


@app.route('/bucketlists/<int:id>', methods=['GET'])
@auth.login_required
def get_specific_bucketlist(id):
    bucketlist = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()
    if bucketlist:
        return jsonify(bucketlist.return_data()), 200
    return jsonify({"message": "Bucketlist not found"}), 404


@app.route('/bucketlists/', methods=['GET'])
@auth.login_required
def get_all_bucketlists():
    bucketlists = db.session.query(Bucketlist).filter_by(
            created_by=g.user.id).all()
    if not bucketlists:
        return jsonify({"message": "Bucketlist not found"}), 404
    if request.args.get('q') and request.args.get('limit'):
        bucketlists = db.session.query(Bucketlist).filter_by(
            created_by=g.user.id,
            name=request.args.get('q').limit(request.args.get('limit'))).all()
    if request.args.get('q'):
        print(request.args)
        bucketlists = db.session.query(Bucketlist).filter_by(
            created_by=g.user.id, name=request.args.get('q')).all()
    if request.args.get('limit'):
        bucketlists = db.session.query(Bucketlist).filter_by(
            created_by=g.user.id.limit(request.args.get('limit'))).all()
    elif not request.args.get('q') and not request.args.get('limit'):
        bucketlists = db.session.query(Bucketlist).filter_by(
            created_by=g.user.id).all()
    
    list_bucketlists = []
    for item in bucketlists:
        list_bucketlists.append(item.return_data())
    return jsonify(list_bucketlists), 200


@app.route('/bucketlists/<int:id>', methods=['PUT'])
@auth.login_required
def edit_existing_bucketlist(id):
    name = request.json.get("name")
    if len(name) == 0:
        return jsonify({"message": "Missing name."}), 406
    bl = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()
    if not bl:
        return jsonify({"message": "Bucketlist not found."}), 404
    bl.name = name
    db.session.commit()
    return jsonify({"message": "Bucketlist name updated."}), 202


@app.route('/bucketlists/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_existing_bucketlist(id):
    bucketlist = db.session.query(Bucketlist).filter_by(
        created_by=g.user.id, id=id).first()
    if bucketlist:
        db.session.delete(bucketlist)
        db.session.commit()
        return jsonify({"message": "Bucketlist deleted"})
    return jsonify({"message": "Bucketlist not found"}), 404


@app.errorhandler(405)
def custom_error(e):
    res = jsonify({
        'status': 405,
        'error': 'method not supported',
        'message': 'the method is not supported'
    })
    res.status_code = 405
    return res
