from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define SQLAlchemy models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    age = db.Column(db.String)
    sex = db.Column(db.Enum("male", "female"))
    address = db.Column(db.String)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    contact_info = db.Column(db.ARRAY(db.Integer))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("health_data", lazy=True))
    troponin_level = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    blood_pressure = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Dummy route to query data from the server
@app.route("/", methods=["GET"])
def get_dummy_data():
    users = User.query.all()
    health_data = HealthData.query.all()

    return (users, health_data)


if __name__ == "__main__":
    app.run(debug=True)
