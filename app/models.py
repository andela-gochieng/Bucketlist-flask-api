from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from config.config import app_config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
import string

db = SQLAlchemy()
SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in range(32))


class User(db.Model):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self, password):
        self.psw_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.psw_hash)

    def generate_auth_token(self, expiration=300):
        s = Serializer(app_config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app_config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        user = data['id']
        return user

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    psw_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User(logged_in='%s')>" % (
            self.created_by)


class Bucketlist(db.Model):

    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship("Item", backref=db.backref("bucketlists"))

    def __repr__(self):
        return "<Bucketlist(created_by='%s', created_on='%s')>" % (
            self.created_by, self.date_created)


class Item(db.Model):
    '''Method to create tables for the items'''
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Item(name='%s', created_on='%s')>" % (self.name,
                                                       self.date_created)
