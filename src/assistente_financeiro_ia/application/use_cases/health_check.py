from src.assistente_financeiro_ia.application.dto.health_status import HealthStatusDTO
from src.assistente_financeiro_ia.shared.config.settings import Settings


class HealthCheckUseCase:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def execute(self) -> HealthStatusDTO:
        return HealthStatusDTO(
            status="ok",
            service=self._settings.app_name,
            environment=self._settings.app_env,
        )
