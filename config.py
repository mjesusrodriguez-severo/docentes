import os
from dotenv import load_dotenv
from flask import current_app

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": "/etc/ssl/certs/ca-certificates.crt"
            }
        }
    }
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    OAUTHLIB_INSECURE_TRANSPORT = True  # Solo para desarrollo
    OAUTH_REDIRECT_URI = "http://localhost:5000/login/google/authorized"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mjesusrodriguez@severoochoa.es'
    MAIL_PASSWORD = 'ajab vpbz qrdj ywpn'
    MAIL_DEFAULT_SENDER = 'panel@severoochoa.es'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    GOOGLE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials', 'google_service_account.json')
    FOLDER_ID = '19RcNZyhqlPJnmGdAcbB-K6NE8T-XX7NL'

    CARPETA_SUSTITUCIONES_RAIZ_ID = "15wiaXSjf8Pw1_ngP9msLdxlHXfai6q9J"

    ESENDEX_USER = "manolojimenez86@gmail.com"
    ESENDEX_PASSWORD = "b072431a128749aca763"
    ESENDEX_ACCOUNT_REF = "EX0322259"
    ESENDEX_REMITENTE = "SeveroOchoa"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'absentismo')
    ALLOWED_EXTENSIONS = {'csv'}