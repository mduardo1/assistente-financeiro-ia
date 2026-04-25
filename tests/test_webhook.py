def test_whatsapp_webhook_creates_transaction(client):
    client.post(
        "/auth/register",
        data={
            "name": "Moyses",
            "email": "moyses@example.com",
            "password": "123456",
            "whatsapp": "11999999999",
        },
    )

    response = client.post(
        "/webhooks/whatsapp",
        json={
            "whatsapp": "11999999999",
            "message": "recebi 300 de cliente",
        },
    )

    payload = response.get_json()

    assert response.status_code == 201
    assert payload["status"] == "success"
    assert payload["transaction"]["type"] == "income"
    assert payload["transaction"]["category"] == "cliente"
