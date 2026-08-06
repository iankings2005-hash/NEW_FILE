from flask import Flask
from extensions import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import Expense

with app.app_context():
    db.create_all()

import routes

if __name__ == "__main__":
    app.run(debug=True)