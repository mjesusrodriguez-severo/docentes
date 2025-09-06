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
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    GOOGLE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials', 'google_service_account.json')
    #PARA PRODUCCION
    GOOGLE_CREDENTIALS_BASE64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
    FOLDER_ID = '19RcNZyhqlPJnmGdAcbB-K6NE8T-XX7NL'

    CARPETA_SUSTITUCIONES_RAIZ_ID = "15wiaXSjf8Pw1_ngP9msLdxlHXfai6q9J"

    ESENDEX_USER = os.getenv("ESENDEX_USER")
    ESENDEX_PASSWORD = os.getenv("ESENDEX_PASSWORD")
    ESENDEX_ACCOUNT_REF = os.getenv("ESENDEX_ACCOUNT_REF")
    ESENDEX_REMITENTE = "SeveroOchoa"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'absentismo')
    ALLOWED_EXTENSIONS = {'csv'}