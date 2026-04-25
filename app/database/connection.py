from pathlib import Path
import sqlite3

from flask import Flask, current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE_PATH"])
        database_path.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        g.db = connection

    return g.db


def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)

    if connection is not None:
        connection.close()


def init_db() -> None:
    connection = get_db()
    schema_path = Path(__file__).resolve().parent / "schema.sql"
    connection.executescript(schema_path.read_text(encoding="utf-8"))
    connection.commit()


def init_app(app: Flask) -> None:
    with app.app_context():
        init_db()
