# WhatsApp Business API

## Estado atual

O projeto ainda não envia mensagens reais, mas já está preparado para:

- verificar webhook;
- receber payload JSON;
- extrair texto da mensagem;
- salvar a movimentação usando a mesma lógica do sistema.

## Variáveis de ambiente

```env
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
```

## Rotas preparadas

- `GET /webhook/whatsapp`
- `POST /webhook/whatsapp`
- `POST /webhooks/whatsapp`

## Próximo passo

Integrar o envio ativo de mensagens pela Cloud API da Meta usando `WHATSAPP_ACCESS_TOKEN` e `WHATSAPP_PHONE_NUMBER_ID`.
