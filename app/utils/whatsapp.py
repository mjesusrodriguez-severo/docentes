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



def enviar_whatsapp(telefono, mensaje):
    PHONE_NUMBER_ID = "707135885826193"
    ACCESS_TOKEN = "EAARS3psBzZAMBQR2RtdD9ISDqqKRTJV6DPZAtFxRToZBZBjbeQUUITHHvkU5tTnXi48htGYcY7ZAtdW1YZA5nHTHhcuQZB5SYdAANB9vNcdznqrkrMepnnq1yqZC4fxKsywT2XnzO71Jh1slCVWY7kebqSjy052R8SlxTTDN1yUZCGzerMvJpJ9Q8aDOIHmAUtFhk8WgE0dZBIhdENArQylBoFo7ZAwPhSZBVRR195YAzGmFZAbs5jqPVphrYtiNbZCckGNrl9L8MqLGmrKaLLLsflYVAd0nSILwj0yQkEYAZDZD"

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": "34675151146",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code, response.text


@whatsapp_bp.route("/test/whatsapp", methods=["GET"])
def test_whatsapp():
    telefono = request.args.get("telefono")

    if not telefono:
        return jsonify(error="Falta parámetro 'telefono'"), 400

    status, response = enviar_whatsapp(
        telefono=telefono,
        mensaje="✅ Mensaje de prueba enviado desde PRODUCCIÓN"
    )

    return jsonify(
        status=status,
        whatsapp_response=response
    )
