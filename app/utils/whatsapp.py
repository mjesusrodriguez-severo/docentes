from flask import Blueprint, request

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

