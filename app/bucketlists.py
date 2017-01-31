from flask import g, jsonify, url_for, request
from app.models import User, Bucketlist
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


@app.route('/bucketlists/', methods=['POST'])
@auth.login_required
def create_bucketlist():
    '''Creates a buckelist by providing a unique name of the bucketlist to be
    created'''

    name = request.json.get('name')
    if not Bucketlist.query.filter_by(
            name=name, created_by=g.user.id).all():
        if not name:
            return jsonify({"message": "Missing name."}), 400
    else:
        return jsonify({"message": "Bucketlist name already exists."}), 400
    db.session.add(Bucketlist(created_by=g.user.id, name=name))
    db.session.commit()
    return jsonify({"message": "Bucketlist created."}), 201


@app.route('/bucketlists/<int:id>', methods=['GET'])
@auth.login_required
def get_specific_bucketlist(id):
    '''Enables viewing of one buckelist specified by the ID number'''

    bucketlist = Bucketlist.query.filter_by(
        id=id, created_by=g.user.id).first()
    if bucketlist:
        return jsonify(bucketlist.return_data()), 200
    return jsonify({"message": "Bucketlist not found"}), 404


@app.route('/bucketlists/', methods=['GET'])
@auth.login_required
def get_all_bucketlists():
    '''Enables viewing of all the buckelists belonging to the current user.
    Shows the details of each buckelist and its subsequent items '''

    try:
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 20)
        search_name = request.args.get('q', '')
    except:
        return jsonify({"error": "limit and page must be integers"}), 400
    bucketlists = Bucketlist.query.filter_by(
        created_by=g.user.id).filter(
        Bucketlist.name.like('%{}%'.format(search_name))).paginate(
        page=page, per_page=limit)

    if bucketlists.has_prev:
        previous_url = url_for(
            request.endpoint,
            page=bucketlists.prev_num,
            limit=limit,
            _external=True
        )
    else:
        previous_url = None
    if bucketlists.has_next:
        next_url = url_for(
            request.endpoint,
            page=bucketlists.next_num,
            limit=limit,
            _external=True
        )
    else:
        next_url = None
    first_url = url_for(request.endpoint, page=1, limit=limit, _external=True)
    last_url = url_for(
        request.endpoint, page=bucketlists.pages, limit=limit, _external=True)

    page_info = {
        "page": page,
        "limit": limit,
        "total": bucketlists.total,
        "pages": bucketlists.pages,
        "previous": previous_url,
        "next": next_url,
        "first_url": first_url,
        "last_url": last_url
    }
    list_bucketlists = [item.return_data() for item in bucketlists.items]
    return jsonify({"bucketlists": list_bucketlists, "page_meta": page_info}), 200


@app.route('/bucketlists/<int:id>', methods=['PUT'])
@auth.login_required
def edit_existing_bucketlist(id):
    '''Allows the change of the name of the buckelist but the name must not
    already exist.'''

    name = request.json.get("name")
    if not name:
        return jsonify({"message": "Missing name."}), 400
    bucketlist = Bucketlist.query.filter_by(
        id=id, created_by=g.user.id).first()
    if not bucketlist:
        return jsonify({"message": "Bucketlist not found."}), 404
    bucketlist.name = name
    db.session.commit()
    return jsonify({"message": "Bucketlist name updated."}), 202


@app.route('/bucketlists/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_existing_bucketlist(id):
    '''Permanently removes the bucketlist from the list of bucketlists created
    by the current user'''

    bucketlist = Bucketlist.query.filter_by(
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


@app.errorhandler(405)
def internal_server_error(e):
    res = jsonify({
        'status': 500,
        'error': 'internal_server_error',
        'message': 'internal_server_error'
    })
    res.status_code = 405
    return res
