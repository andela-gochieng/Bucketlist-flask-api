from flask import Flask
from flask_testing import TestCase
from app import app, db
from config.config import app_config
from app.models import User, Bucketlist, Item

app.config.from_object(app_config['testing'])


class BaseTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app_config['TESTING'] = True
        return app  

    def setUp(self):
    
        user1 = User(username='Kenyan',
                     password='kicc123')
        bucketlist1 = Bucketlist(name='Restaurants to visit',
                                 created_by=1)
        item1 = Item(name='Larder',
                     bucketlist_id=1)
        item2 = Item(name='About Thyme',
                     bucketlist_id=1)

        if __name__ == "__main__":
            db.create_all()

        db.session.add(user1)
        db.session.add(bucketlist1)
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()


def tearDown(self):

    db.session.remove()
    db.drop_all()
