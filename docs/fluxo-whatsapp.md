# Fluxo WhatsApp

## Estado atual

O projeto já possui uma rota fake de webhook em:

```text
/webhooks/whatsapp
```

Ela serve como ponto de entrada para futuras integrações reais.

## Fluxo atual

1. O webhook recebe um JSON com `message` e `whatsapp` ou `email`.
2. O sistema identifica o usuário pelo contato informado.
3. O `ParserService` interpreta a frase.
4. O `TransactionService` valida e salva a movimentação.
5. A transação fica registrada com origem `whatsapp_webhook`.

## Exemplos

```json
{
  "whatsapp": "11999999999",
  "message": "recebi 300 de cliente"
}
```

```json
{
  "email": "moyses@example.com",
  "message": "paguei 120 de internet"
}
```

## Evolução futura

Os próximos passos naturais para esse fluxo são:

- assinatura e validação do webhook;
- integração com WhatsApp Business API;
- resposta automática ao usuário;
- consultas financeiras por texto;
- confirmação de lançamento por mensagem.
