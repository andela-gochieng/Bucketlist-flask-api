from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    BadSignature, SignatureExpired
from app import app
from run import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    psw_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.psw_hash = self.hash_password(password)

    def hash_password(self, password):
        '''Encrypt the password given and returns
        a hashed version for storage.'''

        return pwd_context.encrypt(password)

    def verify_password(self, password):
        '''Compares the password given when the user logs in with the password
        hash stored in the database.'''

        return pwd_context.verify(password, self.psw_hash)

    def generate_auth_token(self):
        '''Generates a token once the password has been verified.'''
        s = Serializer(app.config['SECRET_KEY'], expires_in=6000)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        '''Verifies that the token provided with each request is valid before
        the request is serviced'''
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
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship("Item", backref=db.backref("bucketlists"))


    def return_data(self):
        '''Displays the details of each bucketlist when the 'GET' method is
        used'''

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

    def return_data(self):
        '''Displays the details of each item when the 'GET' method is
        used'''

        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'done': self.done,
        }
