from flask import Blueprint, request, jsonify
import requests

whatsapp_bp = Blueprint("whatsapp", __name__)

WHATSAPP_VERIFY_TOKEN = "whatsapp_webhook_verification_2025"

@whatsapp_bp.route("/webhook/whatsapp", methods=["GET"])
def verify():
    if (
        request.args.get("hub.mode") == "subscribe"
        and request.args.get("hub.verify_token") == WHATSAPP_VERIFY_TOKEN
    ):
        return request.args.get("hub.challenge"), 200
    return "Forbidden", 403


@whatsapp_bp.route("/webhook/whatsapp", methods=["POST"])
def dummy():
    return "OK", 200



def enviar_sustitucion_whatsapp(telefono, sustitucion):
    PHONE_NUMBER_ID = "971299449400630"
    ACCESS_TOKEN = "EAAhbe78U2pMBQUz1wHYftC1p7zQSabJ4WKQWdRd34eEBMe4d6AjMfhc14ZA0DtZBHiZCBjwMzfJaxYiYgR4lhm07qIMzlZBkaBKLWYFhZCGk4tu0rPz4hdXgkQsDUF5UaygpiMEnbiJOj0g74DLFepjZBPGhKBEYGByoAhoBHb67htxtsZBBZCf0uxnUSaw27gZDZD"

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "template",
        "template": {
            "name": "sustituciones",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": sustitucion.sustituto.nombre
                        },
                        {
                            "type": "text",
                            "text": sustitucion.grupo.nombre
                        },
                        {
                            "type": "text",
                            "text": sustitucion.fecha.strftime("%d/%m/%Y")
                        },
                        {
                            "type": "text",
                            "text": f"{sustitucion.hora_inicio} - {sustitucion.hora_fin}"
                        },
                        {
                            "type": "text",
                            "text": sustitucion.sustituido.nombre
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.json()

def enviar_amonestacion_whatsapp(telefono, amonestacion, fecha_madrid):
    """
    Envía una amonestación por WhatsApp usando plantilla oficial.
    Sustituye directamente al envío por SMS.
    """

    PHONE_NUMBER_ID = "971299449400630"
    ACCESS_TOKEN = "EAAhbe78U2pMBQUz1wHYftC1p7zQSabJ4WKQWdRd34eEBMe4d6AjMfhc14ZA0DtZBHiZCBjwMzfJaxYiYgR4lhm07qIMzlZBkaBKLWYFhZCGk4tu0rPz4hdXgkQsDUF5UaygpiMEnbiJOj0g74DLFepjZBPGhKBEYGByoAhoBHb67htxtsZBBZCf0uxnUSaw27gZDZD"

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": 626188229,
        "type": "template",
        "template": {
            "name": "amonestacion",      # nombre EXACTO de la plantilla
            "language": {
                "code": "es"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": f"{amonestacion.alumno.nombre}"
                        },
                        {
                            "type": "text",
                            "text": f"{amonestacion.alumno.grupo_id.nombre}"
                        },
                        {
                            "type": "text",
                            "text": amonestacion.motivo
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    return {
        "ok": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.text
    }