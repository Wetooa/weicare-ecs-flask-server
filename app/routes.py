from flask import Blueprint, jsonify
from app.models import User, HealthData

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify(users)
