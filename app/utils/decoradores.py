# decoradores.py
from functools import wraps
from flask_login import current_user
from flask import abort

def rol_requerido(rol):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol != rol:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return wrapper