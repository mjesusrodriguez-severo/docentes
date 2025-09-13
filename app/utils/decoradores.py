# decoradores.py
from functools import wraps
from flask_login import current_user
from flask import abort, flash, redirect, url_for


def rol_requerido(*roles_permitidos):
    def decorador(f):
        @wraps(f)
        def funcion_envuelta(*args, **kwargs):
            if current_user.rol not in roles_permitidos:
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for("main.index"))
            return f(*args, **kwargs)
        return funcion_envuelta
    return decorador