# Assistente Financeiro IA

Sistema financeiro web em Flask para registrar entradas e saídas, interpretar mensagens financeiras e preparar a evolução futura para atendimento via WhatsApp.

## Descrição do projeto

O Assistente Financeiro IA foi estruturado como uma base profissional para controle financeiro pessoal ou de pequenos negócios. O projeto já entrega autenticação, dashboard, parser por mensagem, persistência em SQLite e uma organização clara para crescer com segurança.

## Funcionalidades atuais

- cadastro de usuário;
- login com sessão;
- logout;
- senha com hash seguro;
- dashboard financeiro;
- cards de saldo, entradas e saídas;
- gráfico de gastos por categoria com Chart.js;
- estados vazios amigáveis;
- cadastro manual de entradas;
- cadastro manual de saídas;
- listagem de movimentações;
- parser financeiro por mensagem;
- rota fake de webhook para WhatsApp;
- base inicial para futuras consultas financeiras por texto;
- testes automatizados cobrindo fluxos principais.

## Melhorias implementadas nesta etapa

- UX/UI renovada com layout mais moderno, melhor espaçamento e responsividade;
- mensagens flash mais elegantes e legíveis;
- loading visual nos botões de login, cadastro, parser e nova movimentação;
- Post/Redirect/Get nas operações de sucesso em transações;
- validação monetária com suporte a vírgula e ponto;
- bloqueio de valores negativos e inválidos;
- parser financeiro com cobertura para mais palavras-chave;
- gráfico real de categorias usando dados do backend;
- documentação expandida;
- testes adicionais para parser e validações.

## Tecnologias usadas

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- Jinja2
- Chart.js
- Pytest

## Como instalar

```bash
pip install -r requirements.txt
```

Para desenvolvimento e testes:

```bash
pip install -r requirements-dev.txt
```

## Como rodar

```bash
python run.py
```

## Como acessar no navegador

```text
http://127.0.0.1:5000
```

## Como testar

```bash
python -m pytest tests
```

## Como usar o parser

No painel de movimentações, use o bloco "Lançar por mensagem" com frases como:

- `gastei 50 no mercado`
- `paguei 120 de internet`
- `comprei 30 em frutas`
- `recebi 300 de cliente`
- `ganhei 1000 da venda do iphone`
- `vendi 500 em móveis`

## Estrutura do projeto

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
├── requirements-dev.txt
├── README.md
└── .gitignore
```

## Estratégia de branches

- `main`: somente versão estável;
- `develop`: integração de desenvolvimento;
- `feature/professional-improvements`: melhorias profissionais desta etapa;
- demais features podem continuar segmentadas por domínio ou tela.

## Fluxo do sistema

1. O usuário cria conta ou faz login.
2. A sessão é mantida pelo Flask.
3. O usuário registra movimentações manualmente ou por texto.
4. O SQLite persiste os dados.
5. O dashboard consolida saldo, categorias e atividade recente.

## Próximos passos

- consultas financeiras por texto;
- integração real com WhatsApp Business API;
- filtros por período;
- edição e exclusão de lançamentos;
- exportação de dados;
- limpeza segura da pasta `src/` em branch dedicada, após confirmação final.

## Observação sobre `src/`

A pasta `src/` continua no repositório, mas a aplicação em uso roda por `app/` e `run.py`. A recomendação é remover `src/` apenas depois de uma revisão final em branch separada, para não apagar nada sem necessidade.

## Documentação complementar

- [Arquitetura](docs/arquitetura.md)
- [Fluxo WhatsApp](docs/fluxo-whatsapp.md)
- [Melhorias Futuras](docs/melhorias-futuras.md)
