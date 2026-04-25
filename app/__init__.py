from flask import Flask

from app.config import Config
from app.database.connection import close_db, init_app as init_database
from app.routes.auth import auth_bp
from app.routes.core import core_bp
from app.routes.dashboard import dashboard_bp
from app.routes.transactions import transactions_bp


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config.from_object(config_class)

    init_database(app)
    app.teardown_appcontext(close_db)

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)

    return app
