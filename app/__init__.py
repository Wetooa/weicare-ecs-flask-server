from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
import os


load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.app_context().push()

    db.init_app(app)

    from app.routes.user import user_bp
    from app.routes.contact import contact_bp
    from app.routes.health_data import health_data_bp
    from app.routes.device import device_bp
    from app.routes.notification import notification_bp

    from app.routes.seed import seed_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(health_data_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(seed_bp)

    CORS(app)

    with app.app_context():
        db.create_all()

    return app
