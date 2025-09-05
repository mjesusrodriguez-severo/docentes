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