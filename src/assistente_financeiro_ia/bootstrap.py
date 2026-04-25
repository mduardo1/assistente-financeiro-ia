from flask import Flask

from src.assistente_financeiro_ia.presentation.http.routes.health import health_blueprint
from src.assistente_financeiro_ia.shared.config.settings import Settings
from src.assistente_financeiro_ia.shared.container import Container


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    container = Container.build(settings)

    app = Flask(__name__)
    app.config["APP_NAME"] = settings.app_name
    app.config["APP_ENV"] = settings.app_env
    app.config["CONTAINER"] = container

    app.register_blueprint(health_blueprint)

    return app
