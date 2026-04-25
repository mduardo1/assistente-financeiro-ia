from dataclasses import dataclass


@dataclass(frozen=True)
class HealthStatusDTO:
    status: str
    service: str
    environment: str
