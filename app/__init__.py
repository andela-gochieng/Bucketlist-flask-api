from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
# from app.models import User, Bucketlist, Item
from config.config import app_config


app = Flask(__name__)
app.config.from_object(app_config['development'])

from . import models
from . import auth
from . import items
from . import bucketlists

if __name__ == "__main__":
    db.create_all()