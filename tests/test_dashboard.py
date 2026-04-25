def test_dashboard_displays_financial_summary(client):
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
    client.post(
        "/transactions/",
        data={
            "type": "income",
            "description": "Recebimento de cliente",
            "category": "cliente",
            "amount": "300",
            "transaction_date": "2026-04-25",
        },
    )
    client.post(
        "/transactions/",
        data={
            "type": "expense",
            "description": "Pagamento de internet",
            "category": "internet",
            "amount": "120",
            "transaction_date": "2026-04-25",
        },
    )

    response = client.get("/dashboard/")

    assert response.status_code == 200
    assert "R$ 180.00".encode("utf-8") in response.data
    assert "internet".encode("utf-8") in response.data
    assert b"expensesChart" in response.data
