from flask import Blueprint, jsonify

from app.models import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
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
