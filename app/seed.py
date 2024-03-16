from app import db
from flask import Blueprint
from app.models import SexType, User, HealthData


dummy_data_bp = Blueprint("dummy_data", __name__)


@dummy_data_bp.route("/add_dummy_data", methods=["GET"])
def add_dummy_data():
    add_dummy_users()
    add_dummy_health_data()
    return "Dummy data added successfully"


def add_dummy_users():
    user1 = User(
        firstname="John",
        lastname="Doe",
        age=30,
        sex=SexType.MALE,
        address="123 Main St",
        weight=75.5,
        height=180.0,
    )

    user2 = User(
        firstname="Jane",
        lastname="Smith",
        age=25,
        sex=SexType.FEMALE,
        address="456 Elm St",
        weight=60.0,
        height=165.0,
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


def add_dummy_health_data():
    health_data1 = HealthData(
        user_id=1,  # Assuming user1 has ID 1
        troponin_level=10,
        heart_rate=70,
        blood_pressure=120,
    )

    health_data2 = HealthData(
        user_id=2,  # Assuming user2 has ID 2
        troponin_level=15,
        heart_rate=65,
        blood_pressure=130,
    )

    db.session.add(health_data1)
    db.session.add(health_data2)
    db.session.commit()
