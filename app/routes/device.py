from flask import jsonify, request
from flask import Blueprint
from app.models import User, Device, db
from datetime import datetime


device_bp = Blueprint("device", __name__)


@device_bp.route("/device/<int:user_id>", methods=["GET"])
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


@device_bp.route("/device/<int:user_id>", methods=["POST"])
def add_device(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    new_device = Device(
        user_id=user.id,
        name=data.get("name"),
        is_active=data.get("is_active"),
        created_at=datetime.now(),
    )

    db.session.add(new_device)
    db.session.commit()

    return jsonify({"message": "Device added successfully"}), 201


@device_bp.route("/device/<int:device_id>", methods=["PUT"])
def update_device(device_id):
    device = Device.query.filter_by(id=device_id).first()

    if not device:
        return jsonify({"error": "Device not found"}), 404

    data = request.get_json()
    device.name = data.get("name", device.name)
    device.is_active = data.get("is_active", device.is_active)

    db.session.commit()

    return jsonify({"message": "Device updated successfully"}), 200


@device_bp.route("/device/<int:device_id>", methods=["DELETE"])
def delete_device(device_id):
    device = Device.query.filter_by(id=device_id).first()

    if not device:
        return jsonify({"error": "Device not found"}), 404

    db.session.delete(device)
    db.session.commit()

    return jsonify({"message": "Device deleted successfully"}), 200
