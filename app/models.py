from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
# from config.config import app_config
from flask import g, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    BadSignature, SignatureExpired
# import random
# import string
from app import app

db = SQLAlchemy(app)
# SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                      for x in range(32))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    psw_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.psw_hash = self.hash_password(password)

    def __repr__(self):
        return "<{} {}>".format(self.username, self.psw_hash)


    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password ,self.psw_hash)

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in=6000)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'], expires_in=6000)
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        user = data['id']
        return user


class Bucketlist(db.Model):

    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship("Item", backref=db.backref("bucketlists"))

    def get_url(self):
        return url_for('app.get_specific_bucketlist', id=self.id,
                       _external=True)

    def return_data(self):
        items = Item.query.filter_by(bucketlist_id=self.id).all()
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.return_data() for item in items],
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'created_by': self.created_by
        }


class Item(db.Model):
    '''Method to create tables for the items'''
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)

    def get_url(self):
        return url_for(
            'app.get_item',
            item_id=self.id,
            id=self.bucketlist_id,
            _external=True
        )

    def return_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'done': self.done,
        }
