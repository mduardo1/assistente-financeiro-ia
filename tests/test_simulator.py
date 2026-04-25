def test_whatsapp_simulator_requires_login(client):
    response = client.get("/transactions/simulador-whatsapp")

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_whatsapp_simulator_saves_transaction(client):
    client.post(
        "/auth/register",
        data={
            "name": "Moyses",
            "email": "moyses@example.com",
            "password": "123456",
            "whatsapp": "11999999999",
        },
    )
    client.post(
        "/auth/login",
        data={"email": "moyses@example.com", "password": "123456"},
    )

    response = client.post(
        "/transactions/simulador-whatsapp",
        data={"message": "gastei 50 no mercado"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Movimentação salva".encode("utf-8") in response.data
