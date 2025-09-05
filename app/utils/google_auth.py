import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app

def build_drive_service():
    credentials_path = current_app.config['GOOGLE_CREDENTIALS_PATH']
    scopes = ['https://www.googleapis.com/auth/drive.file']
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=scopes
    )
    return build('drive', 'v3', credentials=credentials)