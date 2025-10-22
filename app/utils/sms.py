try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

import requests
from requests.auth import HTTPBasicAuth
from flask import current_app, url_for


def enviar_sms_esendex(telefono, mensaje):
    """
    Envia un SMS usando Esendex API en formato XML.
    """

    xml_data = f"""
    <messages>
        <accountreference>{current_app.config['ESENDEX_ACCOUNT_REF']}</accountreference>
        <message>
            <to>{telefono}</to>
            <from>SeveroOchoa</from>
            <body>{mensaje}</body>
            <type>SMS</type>
        </message>
    </messages>
    """.strip()

    headers = {"Content-Type": "text/xml"}

    response = requests.post(
        "https://api.esendex.com/v1.0/messagedispatcher",
        headers=headers,
        data=xml_data.encode("utf-8"),
        auth=HTTPBasicAuth(current_app.config['ESENDEX_USER'], current_app.config['ESENDEX_PASSWORD'])
    )

    return response.status_code in [200, 201], response.text

def enviar_sms_sustitucion(telefono, sustitucion):
    """
    Envia un SMS informando de una sustitución y solicitando confirmación de lectura.
    """
    mensaje = (
        f"Jefatura de estudios:\n"
        f"Grupo {sustitucion.grupo.nombre}, {sustitucion.fecha.strftime('%d/%m/%Y')} a las {sustitucion.hora}.\n"
        f"Confirma lectura: {url_for('main.confirmar_sustitucion', sustitucion_id=sustitucion.id, _external=True)}"
    )
    return enviar_sms_esendex(telefono, mensaje)

def enviar_sms_amonestacion_utils(telefono, amonestacion):
    """
    Envía un SMS informando de una amonestación registrada al alumno.
    """
    # Convertir la hora UTC (guardada en la BD) a hora española
    fecha_madrid = amonestacion.fecha.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Madrid"))
    print("Fecha original (UTC):", amonestacion.fecha)
    print("Fecha convertida (Madrid):", fecha_madrid)
    mensaje = (
        f"Jefatura de estudios:\n"
        f"Amonestación a {amonestacion.alumno.nombre} {amonestacion.alumno.apellidos}, "
        f"{fecha_madrid.strftime('%d/%m/%Y')} a las {fecha_madrid.strftime('%H:%M')}.\n"
        f"Profesor/a: {amonestacion.profesor.nombre}. \n"
        f"Motivo: {amonestacion.motivo}\n"
        f"Descripción: {amonestacion.descripcion}\n"
    )
    return enviar_sms_esendex(telefono, mensaje)
