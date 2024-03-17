from app import db
from flask import jsonify
from flask import Blueprint
from app.models import HeartClassificationType, User, HealthData
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
            "heart_status": h.heart_status,
            "created_at": h.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime
        }
        health_data_list.append(health_data)

    return jsonify(health_data_list)


# FIX: fake pa muna, simply creates dummy data
@health_data_bp.route("/health_data/<int:user_id>", methods=["POST"])
def add_user_health_data(user_id):
    user = User.query.get_or_404(user_id)

    troponin_level = randint(0, 30)
    heart_rate = randint(60, 100)

    systolic = randint(100, 140)
    diastolic = randint(60, 100)
    blood_pressure = f"{systolic}/{diastolic}"

    heart_status = "healthy"
    if troponin_level > 18:
        heart_status = "myocardial_infarction"
    elif systolic > 120 and diastolic < 80:
        heart_status = "elevated_bp"
    elif heart_rate > 90:
        # TODO: change into smth that makes more sense
        heart_status = "arrhythmia"

    classification = HeartClassificationType.GOOD
    if heart_status == "elevated_bp" or heart_status == "arrhythmia":
        classification = HeartClassificationType.RISK
    if heart_status == "myocardial_infarction":
        classification = HeartClassificationType.DANGER

    # TODO: do something here like maybe make model anaylze currently added data alongside previous data
    # TODO: contact people if heart status is bad

    new_health_data = HealthData(
        user_id=user.id,
        troponin_level=troponin_level,
        heart_rate=heart_rate,
        blood_pressure=blood_pressure,
        heart_status=heart_status,
        classification=classification,
    )

    db.session.add(new_health_data)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Health data added successfully",
                "health_data": new_health_data,
            }
        ),
        201,
    )
