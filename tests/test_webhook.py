def test_whatsapp_webhook_verification(client):
    response = client.get(
        "/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=test-verify-token&hub.challenge=12345"
    )

    assert response.status_code == 200
    assert response.data == b"12345"


def test_whatsapp_webhook_receives_meta_style_json(client):
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
        "/webhook/whatsapp",
        json={
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "from": "11999999999",
                                        "text": {
                                            "body": "recebi 300 de cliente"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        },
    )

    payload = response.get_json()

    assert response.status_code == 201
    assert payload["status"] == "success"
    assert payload["transaction"]["type"] == "income"
    assert payload["transaction"]["category"] == "cliente"
