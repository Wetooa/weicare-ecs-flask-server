from app import db
from flask import jsonify, request
from flask import Blueprint
from app.models import User, HealthData
from random import randint

health_data_bp = Blueprint("health_data", __name__)


@health_data_bp.route("/health_data/<int:user_id>", methods=["GET"])
def get_user_health_data(user_id):
    user = User.query.get_or_404(user_id)
    health_data_list = []

    for h in user.health_data:
        health_data = {
            "user_id": user.id,
            "troponin_level": h.troponin_level,
            "heart_rate": h.heart_rate,
            "blood_pressure": h.blood_pressure,
            "created_at": h.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime
        }
        health_data_list.append(health_data)

    return jsonify(health_data_list)


# fake pa muna, simply creates dummy data


@health_data_bp.route("/health_data/<int:user_id>", methods=["POST"])
def add_user_health_data(user_id):
    user = User.query.get_or_404(user_id)

    [troponin_level, heart_rate, blood_pressure] = request.args.lists()

    troponin_level = randint(0, 20)
    heart_rate = randint(60, 100)
    blood_pressure = str(randint(100, 140) + randint(70, 90))

    new_health_data = HealthData(
        user_id=user.id,
        troponin_level=troponin_level,
        heart_rate=heart_rate,
        blood_pressure=blood_pressure,
    )

    # do something here like maybe make model anaylze currently added data alongside previous data

    db.session.add(new_health_data)
    db.session.commit()

    return jsonify({"message": "Health data added successfully"}), 201
