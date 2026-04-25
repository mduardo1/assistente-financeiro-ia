from src.assistente_financeiro_ia.bootstrap import create_app
from src.assistente_financeiro_ia.shared.config.settings import Settings


def test_health_route_returns_ok():
    app = create_app(Settings(app_name="assistente-financeiro-ia", app_env="test"))
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "service": "assistente-financeiro-ia",
        "environment": "test",
    }
