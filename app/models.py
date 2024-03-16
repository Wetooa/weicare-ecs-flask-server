from app import db
from datetime import datetime
from dataclasses import dataclass
import enum


class SexType(enum.Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    age = db.Column(db.Integer)
    sex = db.Column(db.Enum(SexType))
    address = db.Column(db.String)

    weight = db.Column(db.Float)
    height = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


@dataclass
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    age = db.Column(db.Integer)
    address = db.Column(db.String)
    number = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("contacts", lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super(Contact, self).__init__(**kwargs)


@dataclass
class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    is_active = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("devices", lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super(Devices, self).__init__(**kwargs)


@dataclass
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("health_data", lazy=True))

    troponin_level = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    blood_pressure = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super(HealthData, self).__init__(**kwargs)
