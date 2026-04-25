from flask import Blueprint, current_app, jsonify


health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/health")
def healthcheck():
    container = current_app.config["CONTAINER"]
    result = container.health_check_use_case.execute()

    return (
        jsonify(
            {
                "status": result.status,
                "service": result.service,
                "environment": result.environment,
            }
        ),
        200,
    )
