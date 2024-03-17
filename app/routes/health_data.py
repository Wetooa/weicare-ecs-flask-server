import datetime
from app import db
from flask import jsonify
from flask import Blueprint
from app.models import HeartClassificationType, User, HealthData
from random import randint

health_data_bp = Blueprint("health_data", __name__)


@health_data_bp.route("/health_data/<int:user_id>/recent", methods=["GET"])
def get_recent_user_health_data(user_id):
    user = User.query.get_or_404(user_id)
    data = (
        HealthData.query.filter_by(user_id=user_id)
        .order_by(HealthData.created_at.asc())
        .first()
    )

    if not data:
        return jsonify({"message": "No data found..."})

    health_data = {
        "user_id": user.id,
        "troponin_level": data.troponin_level,
        "heart_rate": data.heart_rate,
        "blood_pressure": data.blood_pressure,
        "heart_status": data.heart_status,
        "classification": data.classification.value,
        "created_at": data.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }

    return jsonify(health_data)


@health_data_bp.route("/health_data/<int:user_id>", methods=["GET"])
def get_user_health_data(user_id):
    data = HealthData.query.filter_by(user_id=user_id).order_by(
        HealthData.created_at.asc()
    )
    health_data_list = []

    for h in data:
        health_data = {
            "user_id": h.user_id,
            "troponin_level": h.troponin_level,
            "heart_rate": h.heart_rate,
            "blood_pressure": h.blood_pressure,
            "heart_status": h.heart_status,
            "classification": h.classification.value,
            "created_at": h.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f"),
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

    serializable_data = {
        "user_id": user.id,
        "troponin_level": new_health_data.troponin_level,
        "heart_rate": new_health_data.heart_rate,
        "blood_pressure": new_health_data.blood_pressure,
        "heart_status": new_health_data.heart_status,
        "classification": new_health_data.classification.value,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }

    db.session.add(new_health_data)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Health data added successfully",
                "health_data": serializable_data,
            }
        ),
        201,
    )
