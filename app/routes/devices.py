from flask import jsonify, request
from flask import Blueprint
from app.models import User, Contact, HealthData

devices_bp = Blueprint("devices", __name__)


@devices_bp.route("/device/<int:user_id>", methods=["GET"])
def get_user_devices(user_id):
    user = User.query.get_or_404(user_id)
    devices_list = []

    for h in user.devices:
        devices_data = {
            "id": h.id,
            "user_id": user.id,
            "name": h.name,
            "is_active": h.is_active,
            "created_at": h.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime
        }
        devices_list.append(devices_data)

    return jsonify(devices_list)
