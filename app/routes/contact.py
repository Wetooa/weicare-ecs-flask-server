from app import db
from app.models import Contact, User
from flask import Blueprint
from flask import jsonify, request

contact_bp = Blueprint("contact", __name__)


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


@contact_bp.route("/contact/<int:user_id>", methods=["POST"])
def add_contact(user_id):
    user = User.query.get_or_404(user_id)
    c = request.get_json()

    new_contact = Contact(
        user_id=user.id,
        firstname=c.get("firstname"),
        lastname=c.get("lastname"),
        age=c.get("age"),
        address=c.get("address"),
        number=c.get("number"),
    )

    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contact added successfully"}), 201


@contact_bp.route("/contact/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    contact = Contact.query.filter_by(id=contact_id).first()
    c = request.get_json()

    if contact:
        contact.firstname = c.get("firstname")
        contact.lastname = c.get("lastname")
        contact.age = c.get("age")
        contact.address = c.get("address")
        contact.number = c.get("number")

        db.session.commit()
        return jsonify({"message": "Contact updated successfully"}), 200
    else:
        return jsonify({"error": "Contact not found"}), 404


@contact_bp.route("/contact/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    contact = Contact.query.filter_by(id=contact_id).first()
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully"}), 200
    else:
        return jsonify({"error": "Contact not found"}), 404
