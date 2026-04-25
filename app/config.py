from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DATABASE_PATH = BASE_DIR / "app" / "database" / "assistente_financeiro_ia.db"
    APP_NAME = "Assistente Financeiro IA"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    USE_OPENAI_PARSER = os.getenv("USE_OPENAI_PARSER", "false").lower() == "true"
    WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
