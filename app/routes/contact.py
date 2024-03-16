from app import db
from app.models import Contact, HealthData, User
from flask import Blueprint
from flask import jsonify, request

contact_bp = Blueprint("contact_bp", __name__)


@contact_bp.route("/contact/<int:user_id>", methods=["GET"])
def get_user_contacts(user_id):
    user = User.query.get_or_404(user_id)

    contacts_list = []

    for contact in user.contacts:
        contact_data = {
            "id": contact.id,
            "firstname": contact.firstname,
            "lastname": contact.lastname,
            "age": contact.age,
            "address": contact.address,
            "number": contact.number,
        }
        contacts_list.append(contact_data)

    return jsonify(contacts_list)


@contact_bp.route("/contacts/<int:user_id>", methods=["POST"])
def add_contact(user_id):
    user = User.query.get_or_404(user_id)
    [firstname, lastname, age, address, number] = request.args.lists()

    new_contact = Contact(
        user_id=user.id,
        firstname=firstname,
        lastname=lastname,
        age=age,
        address=address,
        number=number,
    )

    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contact added successfully"}), 201
