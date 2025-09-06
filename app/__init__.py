import base64
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import configure_mappers
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Solo reconstruir el archivo de credenciales si no estamos en desarrollo
    if os.getenv("FLASK_ENV") != "development":
        encoded_credentials = os.getenv("GOOGLE_CREDENTIALS_BASE64")
        credentials_path = app.config["GOOGLE_CREDENTIALS_PATH"]

        if encoded_credentials and not os.path.exists(credentials_path):
            os.makedirs(os.path.dirname(credentials_path), exist_ok=True)
            with open(credentials_path, "wb") as f:
                f.write(base64.b64decode(encoded_credentials))
            print("✅ Credenciales de Google reconstruidas en producción.")
        elif not encoded_credentials:
            print("⚠️ GOOGLE_CREDENTIALS_BASE64 no está definido.")

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        configure_mappers()

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.auth import auth_bp
    from .routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app