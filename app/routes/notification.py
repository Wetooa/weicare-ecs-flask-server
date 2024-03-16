from flask import Blueprint, jsonify, request
from app.models import NotificationType, User, Notification, db

notification_bp = Blueprint("notification", __name__)


@notification_bp.route("/notification/<int:user_id>", methods=["GET"])
def get_user_notifications(user_id):
    user = User.query.get_or_404(user_id)
    notifications_list = []

    for notification in user.notifications:
        notification_data = {
            "id": notification.id,
            "user_id": user.id,
            "title": notification.title,
            "message": notification.message,
            "type": notification.type.value,  # Convert enum to string value
            "is_read": notification.is_read,
            "created_at": notification.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Format datetime
        }
        notifications_list.append(notification_data)

    return jsonify(notifications_list)


@notification_bp.route("/notification/<int:user_id>", methods=["POST"])
def create_notification(user_id):
    user = User.query.get_or_404(user_id)

    r = request.get_json()

    new_notification = Notification(
        user_id=user.id,
        title=r.get("title"),
        message=r.get("message"),
        type=NotificationType(r.get("type")),
    )

    db.session.add(new_notification)
    db.session.commit()

    return jsonify({"message": "Notification created successfully"}), 201


@notification_bp.route("/notification/<int:notification_id>", methods=["PUT"])
def mark_notification_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)

    if not notification.is_read:
        notification.is_read = True
        db.session.commit()
        return jsonify({"message": "Notification marked as read"}), 200
    else:
        return jsonify({"message": "Notification is already marked as read"}), 200
