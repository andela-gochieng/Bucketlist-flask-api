from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import User, Bucketlist, Item
from config.config import app_config


app = Flask(__name__)
app.config.from_object(app_config['development'])
db = SQLAlchemy(app)

if __name__ == "__main__":
    db.create_all()