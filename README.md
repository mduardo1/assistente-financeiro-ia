# Assistente Financeiro IA

Sistema web financeiro em Flask para registrar entradas e saídas manualmente e, em seguida, evoluir para captura por mensagens no estilo:

- `gastei 50 no mercado`
- `recebi 300 de cliente`
- `paguei 120 de internet`
- `vendi 500 em móveis`

## Objetivo do sistema

Entregar uma base inicial simples, profissional e organizada para um assistente financeiro inspirado na experiência de produtos como o Porquim, com foco em:

- autenticação de usuários;
- dashboard financeiro;
- cadastro manual de movimentações;
- parser de mensagens financeiras;
- preparação para integração com WhatsApp.

## Tecnologias usadas

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- Jinja2

## Como instalar

```bash
pip install -r requirements.txt
```

Para rodar testes localmente:

```bash
pip install -r requirements-dev.txt
pytest
```

## Como rodar

```bash
python run.py
```

## Como acessar no navegador

Abra:

```text
http://127.0.0.1:5000
```

## Estrutura de pastas

```text
assistente-financeiro-ia/
├── app/
│   ├── __init__.py
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
├── README.md
└── .gitignore
```

## Funcionalidades

- cadastro de usuário;
- login com sessão;
- logout;
- senha com hash seguro;
- dashboard financeiro;
- cadastro manual de entradas;
- cadastro manual de saídas;
- listagem de movimentações;
- cálculo de saldo total;
- cálculo de entradas e saídas;
- gastos por categoria;
- parser simples de mensagens financeiras;
- rota fake de webhook para WhatsApp.

## Fluxo do sistema

1. O usuário cria uma conta.
2. Faz login no sistema.
3. Cadastra movimentações manualmente ou por mensagem.
4. Os dados são salvos no SQLite.
5. O dashboard mostra saldo, totais e categorias.

## Fluxo do WhatsApp

1. Uma mensagem chega ao webhook fake.
2. O sistema localiza o usuário por `whatsapp` ou `email`.
3. O parser interpreta tipo, valor e categoria.
4. A movimentação é salva com origem `whatsapp_webhook`.
5. O dashboard passa a refletir esse lançamento.

## Como testar o parser

Pelo painel web:

1. Faça login.
2. Acesse `Movimentações`.
3. Use o bloco `Lançar por mensagem`.
4. Teste frases como:

- `gastei 50 no mercado`
- `recebi 300 de cliente`
- `paguei 120 de internet`
- `vendi 500 em moveis`

Pela rota fake do webhook:

```bash
curl -X POST http://127.0.0.1:5000/webhooks/whatsapp \
  -H "Content-Type: application/json" \
  -d "{\"whatsapp\":\"11999999999\",\"message\":\"recebi 300 de cliente\"}"
```

## Estratégia de branches

- `main`: somente versão estável.
- `develop`: integração do desenvolvimento.
- `feature/auth`: login, cadastro, logout e sessão.
- `feature/dashboard`: visão consolidada do financeiro.
- `feature/transactions`: cadastro e listagem de movimentações.
- `feature/ai-parser`: interpretação das mensagens financeiras.
- `feature/whatsapp-webhook`: rota fake para WhatsApp.
- `feature/docs-readme`: documentação do projeto.

## Fluxo sugerido de Pull Request

Para cada feature:

1. Criar a branch a partir de `develop`.
2. Implementar a feature com commits pequenos.
3. Publicar a branch no GitHub.
4. Abrir Pull Request para `develop`.
5. Após validação, fazer merge.

Exemplo:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/auth
git push -u origin feature/auth
```

## Arquitetura

Resumo:

- `routes`: entrada HTTP e respostas HTML/JSON;
- `services`: regras de negócio;
- `models`: estruturas de dados;
- `database`: conexão e schema SQLite;
- `templates`: interface com Jinja2;
- `static`: CSS e JavaScript.

Documentação detalhada:

- [Arquitetura](docs/architecture.md)
- [Estratégia de Branches](docs/branch-strategy.md)

## Próximos passos

- integração real com WhatsApp Business API;
- classificação automática mais inteligente;
- filtros por período;
- relatórios mensais;
- exportação de dados;
- edição e exclusão de lançamentos;
- multiusuário com perfis e permissões.

## Observação sobre a base atual

Há uma estrutura anterior em `src/` preservada no repositório para não remover conteúdo já existente sem necessidade. A aplicação principal desta entrega roda pela estrutura em `app/` e pelo arquivo `run.py`.
