# app/upload.py
from flask import Blueprint, request, redirect, url_for, flash, current_app
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models import ReservaInformatica
import os
from .routes import main_bp

def get_drive_service():
    credentials_path = current_app.config['GOOGLE_CREDENTIALS_PATH']
    scopes = ['https://www.googleapis.com/auth/drive.file']
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=scopes
    )
    return build('drive', 'v3', credentials=credentials)

def obtener_o_crear_carpeta_mes(mes_año, parent_id):
    drive_service = get_drive_service()
    query = (
        f"name = '{mes_año}' and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"'{parent_id}' in parents and trashed = false"
    )
    resultados = drive_service.files().list(q=query, fields="files(id, name)").execute()
    carpetas = resultados.get('files', [])
    if carpetas:
        return carpetas[0]['id']
    else:
        metadata = {
            'name': mes_año,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        carpeta = drive_service.files().create(body=metadata, fields='id').execute()
        return carpeta['id']

@main_bp.route('/subir-hoja/<int:reserva_id>', methods=['POST'])
def subir_hoja(reserva_id):
    reserva = ReservaInformatica.query.get_or_404(reserva_id)
    archivo = request.files['archivo']
    drive_service = get_drive_service()

    if archivo:
        mes_año = reserva.fecha.strftime('%Y-%m')
        nombre_archivo = f"{reserva.usuario.nombre}_{reserva.fecha.strftime('%Y-%m-%d')}.pdf"
        carpeta_mes_id = obtener_o_crear_carpeta_mes(mes_año, current_app.config['FOLDER_ID'])

        filename = secure_filename(nombre_archivo)
        filepath = os.path.join('uploads', filename)
        archivo.save(filepath)

        file_metadata = {
            'name': nombre_archivo,
            'parents': [carpeta_mes_id]
        }
        media = MediaFileUpload(filepath, mimetype='application/pdf')
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        os.remove(filepath)
        flash('Archivo subido correctamente a Google Drive', 'success')
    else:
        flash('No se ha seleccionado ningún archivo', 'danger')

    return redirect(url_for('main.ver_reserva', reserva_id=reserva_id))