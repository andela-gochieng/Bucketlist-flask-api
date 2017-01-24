from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
# from app.models import User, Bucketlist, Item
from config.config import app_config


app = Flask(__name__)
app.config.from_object(app_config['development'])

from app import models
from app import auth
from app import items
from app import bucketlists

