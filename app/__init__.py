from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.app_context().push()

    db.init_app(app)

    from app.routes import main_bp
    from app.seed import dummy_data_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(dummy_data_bp)

    with app.app_context():
        db.create_all()

    return app
