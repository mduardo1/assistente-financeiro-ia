from src.assistente_financeiro_ia.application.use_cases.health_check import (
    HealthCheckUseCase,
)
from src.assistente_financeiro_ia.shared.config.settings import Settings


def test_health_check_use_case_returns_application_metadata():
    settings = Settings(app_name="assistente-financeiro-ia", app_env="test")

    result = HealthCheckUseCase(settings=settings).execute()

    assert result.status == "ok"
    assert result.service == "assistente-financeiro-ia"
    assert result.environment == "test"
