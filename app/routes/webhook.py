from flask import Blueprint, current_app, jsonify, request

from app.services.auth_service import AuthService
from app.services.message_transaction_service import MessageTransactionService


webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.get("/webhook/whatsapp")
def whatsapp_verify():
    hub_mode = request.args.get("hub.mode")
    hub_verify_token = request.args.get("hub.verify_token")
    hub_challenge = request.args.get("hub.challenge", "")
    expected_token = current_app.config.get("WHATSAPP_VERIFY_TOKEN", "")

    if hub_mode == "subscribe" and hub_verify_token and hub_verify_token == expected_token:
        return hub_challenge, 200

    return "Token de verificação inválido.", 403


@webhook_bp.post("/webhook/whatsapp")
@webhook_bp.post("/webhooks/whatsapp")
def whatsapp():
    payload = request.get_json(silent=True) or request.form.to_dict()
    extracted_message = _extract_whatsapp_message(payload)

    if not extracted_message:
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Webhook recebido e registrado, sem mensagem de texto processável.",
                    "payload_received": True,
                }
            ),
            200,
        )

    email = payload.get("email")
    whatsapp_number = payload.get("whatsapp") or _extract_sender_phone(payload)
    user = AuthService().get_user_by_contact(email=email, whatsapp=whatsapp_number)

    if user is None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Usuário não encontrado para o webhook.",
                    "message_text": extracted_message,
                }
            ),
            404,
        )

    try:
        saved = MessageTransactionService().parse_and_save(
            user_id=user.id,
            message=extracted_message,
            source="whatsapp_webhook",
        )
    except ValueError as error:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": str(error),
                }
            ),
            400,
        )

    return (
        jsonify(
            {
                "status": "success",
                "message": "Webhook processado com sucesso.",
                "transaction": saved.parsed_data,
                "note": "Estrutura pronta para WhatsApp Business API. O vínculo real do número do usuário pode ser feito aqui.",
            }
        ),
        201,
    )


def _extract_whatsapp_message(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return None

    direct_message = payload.get("message")
    if isinstance(direct_message, str) and direct_message.strip():
        return direct_message.strip()

    entries = payload.get("entry")
    if not isinstance(entries, list):
        return None

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        changes = entry.get("changes")
        if not isinstance(changes, list):
            continue
        for change in changes:
            if not isinstance(change, dict):
                continue
            value = change.get("value")
            if not isinstance(value, dict):
                continue
            messages = value.get("messages")
            if not isinstance(messages, list):
                continue
            for message in messages:
                if not isinstance(message, dict):
                    continue
                text_block = message.get("text")
                if isinstance(text_block, dict):
                    body = text_block.get("body")
                    if isinstance(body, str) and body.strip():
                        return body.strip()

    return None


def _extract_sender_phone(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return None

    entries = payload.get("entry")
    if not isinstance(entries, list):
        return None

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        changes = entry.get("changes")
        if not isinstance(changes, list):
            continue
        for change in changes:
            if not isinstance(change, dict):
                continue
            value = change.get("value")
            if not isinstance(value, dict):
                continue
            contacts = value.get("contacts")
            if isinstance(contacts, list):
                for contact in contacts:
                    if isinstance(contact, dict):
                        wa_id = contact.get("wa_id")
                        if isinstance(wa_id, str) and wa_id.strip():
                            return wa_id.strip()
            messages = value.get("messages")
            if isinstance(messages, list):
                for message in messages:
                    if isinstance(message, dict):
                        sender = message.get("from")
                        if isinstance(sender, str) and sender.strip():
                            return sender.strip()

    return None
