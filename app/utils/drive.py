from datetime import datetime

from flask import current_app
from googleapiclient.http import MediaFileUpload

from .google_auth import build_drive_service
from googleapiclient.errors import HttpError

def subir_archivo_a_drive(drive_service, file_path, nombre_usuario, carpeta_raiz_id):
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.strftime("%Y-%m")         # Ej: "2025-08"
    fecha_nombre = fecha_actual.strftime("%d-%m-%Y")    # Ej: "22-08-2025"

    # Buscar si la subcarpeta del mes ya existe
    query = (
        f"'{carpeta_raiz_id}' in parents and "
        f"name='{mes_actual}' and "
        f"mimeType='application/vnd.google-apps.folder' and trashed = false"
    )
    respuesta = drive_service.files().list(
        q=query,
        fields="files(id, name)",
        supportsAllDrives=True
    ).execute()
    carpetas = respuesta.get('files', [])

    if carpetas:
        carpeta_mes_id = carpetas[0]['id']
    else:
        # Crear la carpeta del mes si no existe
        file_metadata = {
            'name': mes_actual,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [carpeta_raiz_id]
        }
        carpeta = drive_service.files().create(
            body=file_metadata,
            fields='id',
            supportsAllDrives=True  # ✅ necesario aquí también
        ).execute()
        carpeta_mes_id = carpeta.get('id')

    # Subir el archivo a esa subcarpeta
    file_metadata = {
        'name': f'{nombre_usuario} - {fecha_nombre}.pdf',
        'parents': [carpeta_mes_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    archivo = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()

    archivo_id = archivo.get('id')

    permiso = {
        'type': 'anyone',
        'role': 'reader'
    }

    drive_service.permissions().create(
        fileId=archivo_id,
        body=permiso,
        supportsAllDrives=True
    ).execute()

    return archivo.get('id')

def obtener_o_crear_carpeta(nombre_carpeta, id_padre, service):
    """
    Busca una carpeta con el nombre dado dentro de otra (id_padre).
    Si no existe, la crea. Compatible con unidades compartidas.
    """
    query = (
        f"'{id_padre}' in parents and "
        f"name = '{nombre_carpeta}' and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"trashed = false"
    )

    try:
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        files = response.get('files', [])
        if files:
            return files[0]['id']

        # Si no existe, crearla
        file_metadata = {
            'name': nombre_carpeta,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [id_padre]
        }

        folder = service.files().create(
            body=file_metadata,
            fields='id',
            supportsAllDrives=True
        ).execute()

        return folder.get('id')

    except HttpError as error:
        raise Exception(f"Error al acceder a Drive: {error}")

def crear_carpeta_sustitucion(email_sustituido, fecha, hora, grupo_id):
    """
    Crea carpeta por mes y día dentro de la carpeta de sustituciones.
    Devuelve el ID de la carpeta del día.
    """
    service = build_drive_service()
    raiz_sustituciones = current_app.config.get("CARPETA_SUSTITUCIONES_RAIZ_ID")

    mes = fecha.strftime("%Y-%m")
    dia = fecha.strftime("%Y-%m-%d")

    carpeta_mes_id = obtener_o_crear_carpeta(mes, raiz_sustituciones, service)
    carpeta_dia_id = obtener_o_crear_carpeta(dia, carpeta_mes_id, service)

    return carpeta_dia_id

