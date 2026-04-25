from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DATABASE_PATH = BASE_DIR / "app" / "database" / "assistente_financeiro_ia.db"
    APP_NAME = "Assistente Financeiro IA"
