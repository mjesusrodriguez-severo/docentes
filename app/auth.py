import os
from flask import Blueprint, redirect, url_for, session, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user, logout_user, current_user
from app.models import Usuario
from app import db, login_manager

auth_bp = Blueprint('auth', __name__)

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_to="auth.login_callback"  # 👈 ESTA ES LA CLAVE
)

@auth_bp.record_once
def setup_blueprint(state):
    app = state.app
    app.register_blueprint(google_bp, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@auth_bp.route("/login")
def login():
    next_url = request.args.get("next")

    if not google.authorized:
        # Guarda `next` en sesión si viene una URL de redirección
        if next_url:
            session['next_url'] = next_url
        return redirect(url_for("google.login"))

    # Ya está autorizado: redirige a `next` o al dashboard
    return redirect(session.pop('next_url', url_for("main.dashboard")))

@auth_bp.route("/auth/callback")
def login_callback():
    if not google.authorized:
        print("❌ No autorizado con Google")
        return "No autorizado con Google", 403

    resp = google.get("/oauth2/v2/userinfo")
    print("📩 Respuesta de Google:", resp.status_code, resp.text)

    if not resp.ok:
        return f"Error al obtener datos del usuario: {resp.text}", 403

    user_info = resp.json()
    print("✅ Datos de usuario recibidos:", user_info)

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        print("❌ No se recibió el email del usuario.")
        return "Error: no se recibió el email del usuario", 403

    # Guardar en base de datos
    user = Usuario.query.filter_by(email=email).first()
    if not user:
        user = Usuario(email=email, nombre=name, rol="docente")
        db.session.add(user)
        db.session.commit()
        print("📝 Usuario creado:", email)
    else:
        print("📂 Usuario ya existente:", email)

    login_user(user)
    print("🔓 Login exitoso:", email)

    return redirect(url_for("main.dashboard"))

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))