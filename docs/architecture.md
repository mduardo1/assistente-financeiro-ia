# Arquitetura

## Visão geral

O projeto segue uma organização inspirada em Clean Architecture, separando responsabilidades para manter o crescimento sustentável do sistema.

## Camadas

### `app/routes`

Responsável pela interface HTTP.

- recebe requests;
- valida fluxo de navegação;
- chama os serviços;
- retorna HTML ou JSON.

### `app/services`

Responsável pelas regras de negócio da aplicação.

- autenticação;
- parser financeiro;
- cadastro e listagem de transações;
- consolidação do dashboard.

### `app/models`

Modelos simples para representar os dados da aplicação.

### `app/database`

Responsável pela infraestrutura SQLite.

- conexão;
- inicialização do banco;
- schema SQL.

### `app/templates`

Camada de apresentação com Jinja2.

### `app/static`

Arquivos estáticos do front-end.

## Fluxo principal

1. O usuário cria conta ou faz login.
2. A sessão é persistida no Flask.
3. O usuário registra movimentações manualmente ou por mensagem.
4. Os serviços salvam os dados no SQLite.
5. O dashboard consolida saldo, entradas, saídas e categorias.
6. O webhook fake simula a futura integração com WhatsApp.

## Banco de dados

### `users`

- `id`
- `name`
- `email`
- `password_hash`
- `whatsapp`
- `created_at`

### `transactions`

- `id`
- `user_id`
- `type`
- `description`
- `category`
- `amount`
- `source`
- `transaction_date`
- `created_at`

## Parser financeiro

O parser atual funciona por regras simples:

- identifica palavras de entrada e saída;
- extrai o primeiro valor numérico encontrado;
- usa preposições como `no`, `na`, `de`, `do`, `da` e `em` para inferir a categoria;
- salva a mensagem original como descrição.

## Crescimento futuro

O sistema já está preparado para evoluir com:

- integração real com WhatsApp;
- categorias inteligentes;
- relatórios mensais;
- filtros;
- múltiplas fontes de entrada;
- APIs externas e automações.
