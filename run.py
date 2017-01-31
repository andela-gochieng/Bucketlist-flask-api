from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run()
