from flask import Blueprint
from app.models import (
    User,
    HealthData,
    Contact,
    Device,
    Notification,
    SexType,
    NotificationType,
    db,
)

seed_bp = Blueprint("seed", __name__)


@seed_bp.route("/add_dummy_data", methods=["POST"])
def add_dummy_data():
    add_dummy_users()
    add_dummy_health_data()
    add_dummy_contacts()
    add_dummy_devices()
    add_dummy_notifications()
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
        blood_pressure="120/80",
    )

    health_data2 = HealthData(
        user_id=2,  # Assuming user2 has ID 2
        troponin_level=15,
        heart_rate=65,
        blood_pressure="130/85",
    )

    db.session.add(health_data1)
    db.session.add(health_data2)
    db.session.commit()


def add_dummy_contacts():
    contact1 = Contact(
        firstname="Alice",
        lastname="Johnson",
        age=28,
        address="789 Oak St",
        number="987654321",
        user_id=1,  # Assuming user1 has ID 1
    )

    contact2 = Contact(
        firstname="Bob",
        lastname="Williams",
        age=35,
        address="321 Pine St",
        number="123456789",
        user_id=2,  # Assuming user2 has ID 2
    )

    db.session.add(contact1)
    db.session.add(contact2)
    db.session.commit()


def add_dummy_devices():
    device1 = Device(
        name="Smartwatch",
        is_active=True,
        user_id=1,  # Assuming user1 has ID 1
    )

    device2 = Device(
        name="Fitness Tracker",
        is_active=False,
        user_id=2,  # Assuming user2 has ID 2
    )

    db.session.add(device1)
    db.session.add(device2)
    db.session.commit()


def add_dummy_notifications():
    notification1 = Notification(
        user_id=1,  # Assuming user1 has ID 1
        title="Good News!",
        message="Your recent health checkup results look great!",
        type=NotificationType.GOOD,
    )

    notification2 = Notification(
        user_id=1,  # Assuming user2 has ID 2
        title="Risk Alert",
        message="Please consult your doctor regarding your blood pressure.",
        type=NotificationType.RISK,
    )

    notification2 = Notification(
        user_id=3,  # Assuming user2 has ID 2
        title="Danger Danger Zone",
        message="U are in danger my guy!!! Call the ambulance",
        type=NotificationType.DANGER,
    )

    db.session.add(notification1)
    db.session.add(notification2)
    db.session.commit()
