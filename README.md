# Assistente Financeiro IA

Plataforma financeira em Flask com experiência mais próxima de produto SaaS, parser financeiro local, camada opcional com OpenAI e consultas inteligentes iniciais no dashboard.

## Visão do produto

O projeto evolui o conceito de assistente financeiro para algo mais próximo de um produto digital real:

- autenticação;
- painel com visão executiva;
- cadastro manual e por mensagem;
- consultas financeiras rápidas;
- preparação para IA e WhatsApp.

## Funcionalidades atuais

- cadastro e login de usuário;
- sessão autenticada;
- dashboard financeiro com resumos;
- gráfico de entradas vs saídas;
- gráfico de gastos por categoria;
- parser financeiro por mensagem;
- fallback local para interpretação;
- camada opcional de IA com OpenAI;
- cadastro manual de entradas e saídas;
- filtros em movimentações;
- rota fake de webhook para WhatsApp;
- consultas financeiras locais no dashboard;
- páginas institucionais do produto.

## Funcionalidades com IA

Quando habilitado, o sistema tenta usar a OpenAI para extrair JSON estruturado da mensagem financeira. Se a API não estiver configurada ou a resposta vier inválida, o sistema usa automaticamente o parser local como fallback.

## Como configurar a OpenAI

Copie o `.env.example` para `.env` e configure:

```env
OPENAI_API_KEY=
USE_OPENAI_PARSER=false
```

## Como rodar sem IA

Deixe:

```env
USE_OPENAI_PARSER=false
```

Depois:

```bash
pip install -r requirements.txt
python run.py
```

## Como rodar com IA

Configure no `.env`:

```env
OPENAI_API_KEY=sua_chave_aqui
USE_OPENAI_PARSER=true
```

Depois:

```bash
pip install -r requirements.txt
python run.py
```

## Como testar

```bash
python -m pytest tests
```

## Parser financeiro

Exemplos suportados:

- `gastei 50 no mercado`
- `paguei 120 de internet`
- `comprei 30 em frutas`
- `recebi 300 de cliente`
- `ganhei 1000 da venda do iphone`
- `vendi 500 em móveis`

## Rotas principais

- `/auth/login`
- `/auth/register`
- `/dashboard/`
- `/dashboard/query`
- `/transactions/`
- `/transactions/parse`
- `/webhooks/whatsapp`
- `/sobre`
- `/como-funciona`
- `/proximos-recursos`

## Estrutura do projeto

```text
assistente-financeiro-ia/
├── app/
│   ├── config.py
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
├── docs/
├── tests/
├── run.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Estratégia de branches

- `main`: somente versão estável
- `develop`: integração principal
- `feature/professional-improvements`: melhorias profissionais
- `feature/product-ai`: evolução para produto + IA

## Próximos passos

- integração real com WhatsApp Business API;
- respostas automáticas no webhook;
- perguntas financeiras mais avançadas;
- edição e exclusão de lançamentos;
- planos SaaS completos por perfil;
- remoção segura da pasta `src/` em branch dedicada após revisão final.
