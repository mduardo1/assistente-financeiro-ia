# Assistente Financeiro IA

Plataforma financeira em Flask com experiência de produto SaaS, parser local, integração opcional com OpenAI, simulador WhatsApp e base preparada para WhatsApp Business API.

## Visão do produto

O Assistente Financeiro IA evolui de um painel financeiro para um produto digital mais completo:

- autenticação;
- dashboard executivo;
- parser financeiro local;
- fallback para IA;
- consultas em linguagem natural;
- preparação para WhatsApp.

## Funcionalidades atuais

- cadastro e login de usuário;
- dashboard com indicadores e gráficos;
- lançamentos manuais;
- parser por mensagem;
- fallback local seguro;
- consultas financeiras locais;
- filtros de transações;
- simulador WhatsApp;
- webhook preparado para verificação e recebimento de payload JSON;
- páginas SaaS de produto.

## Como rodar sem IA

No `.env`:

```env
USE_OPENAI_PARSER=false
OPENAI_API_KEY=
```

Depois:

```bash
pip install -r requirements.txt
python run.py
```

## Como rodar com IA

No `.env`:

```env
USE_OPENAI_PARSER=true
OPENAI_API_KEY=sua_chave
```

Depois:

```bash
pip install -r requirements.txt
python run.py
```

## Como configurar `.env`

Use o `.env.example` como base. O `.env` não deve ser versionado.

Variáveis principais:

```env
OPENAI_API_KEY=
USE_OPENAI_PARSER=false
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
```

## Como funciona o fallback

Se a OpenAI estiver desativada, sem chave ou retornar um JSON inválido, o sistema usa automaticamente o parser local atual. Isso evita quebrar o fluxo principal.

## Como testar o simulador WhatsApp

1. Faça login.
2. Acesse `/transactions/simulador-whatsapp`.
3. Digite uma mensagem como:
   - `gastei 50 no mercado`
   - `recebi 300 de cliente`
4. O sistema salva a movimentação e responde em formato de conversa.

## Como o webhook está preparado

Rotas:

- `GET /webhook/whatsapp`
- `POST /webhook/whatsapp`
- `POST /webhooks/whatsapp`

O `GET` já responde ao fluxo de verificação com `hub.mode`, `hub.verify_token` e `hub.challenge`.

O `POST` já aceita:

- payload simples com `message`
- payload JSON em estilo Meta/WhatsApp Business Platform

## Rotas principais

- `/auth/login`
- `/auth/register`
- `/dashboard/`
- `/dashboard/ask`
- `/transactions/`
- `/transactions/parse`
- `/transactions/simulador-whatsapp`
- `/webhook/whatsapp`
- `/webhooks/whatsapp`
- `/sobre`
- `/como-funciona`
- `/proximos-recursos`

## Próximos passos

- envio real de mensagens pela WhatsApp Business API;
- interpretação de perguntas mais complexas;
- histórico persistente do chat;
- relatórios e exportação;
- planos SaaS completos e billing.

## Estratégia de branches

- `main`: versão estável
- `develop`: integração principal
- `feature/professional-improvements`: UX/UI e base profissional
- `feature/product-ai`: produto, IA e WhatsApp
