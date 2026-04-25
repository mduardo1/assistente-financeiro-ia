from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "assistente-financeiro-ia"
    app_env: str = "development"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_env=os.getenv("APP_ENV", cls.app_env),
        )
