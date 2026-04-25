from werkzeug.security import check_password_hash, generate_password_hash

from app.database.connection import get_db
from app.models.user import User


class AuthService:
    def register_user(self, form_data: dict[str, str]) -> tuple[bool, str]:
        name = form_data["name"]
        email = form_data["email"]
        password = form_data["password"]
        whatsapp = form_data["whatsapp"] or None

        if not name or not email or not password:
            return False, "Preencha nome, e-mail e senha."

        if len(password) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres."

        connection = get_db()
        existing_user = connection.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        if existing_user is not None:
            return False, "Já existe uma conta com este e-mail."

        password_hash = generate_password_hash(password)
        connection.execute(
            """
            INSERT INTO users (name, email, password_hash, whatsapp)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, password_hash, whatsapp),
        )
        connection.commit()
        return True, "Usuário criado com sucesso."

    def authenticate(self, email: str, password: str) -> User | None:
        if not email or not password:
            return None

        connection = get_db()
        row = connection.execute(
            """
            SELECT id, name, email, password_hash, whatsapp, created_at
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        if row is None:
            return None

        if not check_password_hash(row["password_hash"], password):
            return None

        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            whatsapp=row["whatsapp"],
            created_at=row["created_at"],
        )

    def get_user_by_contact(self, email: str | None = None, whatsapp: str | None = None) -> User | None:
        connection = get_db()

        if email:
            row = connection.execute(
                """
                SELECT id, name, email, password_hash, whatsapp, created_at
                FROM users
                WHERE email = ?
                """,
                (email.strip().lower(),),
            ).fetchone()
        elif whatsapp:
            row = connection.execute(
                """
                SELECT id, name, email, password_hash, whatsapp, created_at
                FROM users
                WHERE whatsapp = ?
                """,
                (whatsapp.strip(),),
            ).fetchone()
        else:
            return None

        if row is None:
            return None

        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            whatsapp=row["whatsapp"],
            created_at=row["created_at"],
        )
