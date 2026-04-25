def test_create_transaction_registers_income(client):
    client.post(
        "/auth/register",
        data={
            "name": "Moyses",
            "email": "moyses@example.com",
            "password": "123456",
            "whatsapp": "",
        },
    )
    client.post(
        "/auth/login",
        data={"email": "moyses@example.com", "password": "123456"},
    )

    response = client.post(
        "/transactions/",
        data={
            "type": "income",
            "description": "Venda de movel",
            "category": "moveis",
            "amount": "500",
            "transaction_date": "2026-04-25",
        },
    )

    assert response.status_code == 200
    assert "Movimentação registrada com sucesso".encode("utf-8") in response.data
    assert b"Venda de movel" in response.data
    assert b"R$ 500.00" in response.data
