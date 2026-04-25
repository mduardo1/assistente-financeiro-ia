from flask import Blueprint, jsonify, request

from app.services.auth_service import AuthService
from app.services.parser_service import ParserService
from app.services.transaction_service import TransactionService


webhook_bp = Blueprint("webhook", __name__, url_prefix="/webhooks")


@webhook_bp.post("/whatsapp")
def whatsapp():
    payload = request.get_json(silent=True) or request.form.to_dict()
    message = payload.get("message", "")
    email = payload.get("email")
    whatsapp_number = payload.get("whatsapp")

    user = AuthService().get_user_by_contact(email=email, whatsapp=whatsapp_number)
    if user is None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Usuário não encontrado para o webhook.",
                }
            ),
            404,
        )

    try:
        parsed = ParserService().parse_message(message)
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

    success, service_message = TransactionService().create_transaction(
        user_id=user.id,
        form_data=parsed,
        source="whatsapp_webhook",
    )

    if not success:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": service_message,
                }
            ),
            400,
        )

    return (
        jsonify(
            {
                "status": "success",
                "message": "Webhook processado com sucesso.",
                "transaction": parsed,
            }
        ),
        201,
    )
