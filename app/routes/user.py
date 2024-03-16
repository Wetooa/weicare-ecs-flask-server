from flask import jsonify, request
from flask import Blueprint
from app.models import User, Contact, HealthData

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
def get_all_users():
    users = User.query.all()

    users_list = []

    for u in users:
        user_data = {
            "id": u.id,
            "firstname": u.firstname,
            "lastname": u.lastname,
            "age": u.age,
            "sex": u.sex.value,
            "address": u.address,
            "weight": u.weight,
            "height": u.height,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime
        }
        users_list.append(user_data)

    return jsonify(users_list)


@user_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)

    user_data = {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "age": user.age,
        "sex": user.sex.value,
        "address": user.address,
        "weight": user.weight,
        "height": user.height,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime
    }

    return jsonify(user_data)
