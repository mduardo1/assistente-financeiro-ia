# Arquitetura

## Visão geral

O projeto usa uma organização limpa e prática para Flask, separando entrada HTTP, regras de negócio, persistência, templates e arquivos estáticos.

## Estrutura principal

### `app/routes`

Camada responsável por:

- receber requests;
- controlar autenticação e navegação;
- acionar os serviços;
- devolver HTML ou JSON.

### `app/services`

Camada de regras de negócio:

- autenticação;
- criação de transações;
- parser financeiro;
- consolidação do dashboard;
- base inicial para consultas financeiras futuras.

### `app/models`

Modelos simples para representar entidades da aplicação.

### `app/database`

Infraestrutura do SQLite:

- conexão;
- schema;
- inicialização do banco.

### `app/templates`

Camada de apresentação com Jinja2.

### `app/static`

Arquivos de CSS e JavaScript da interface.

## Fluxos principais

1. O usuário faz cadastro ou login.
2. A sessão é mantida pelo Flask.
3. As movimentações podem ser criadas manualmente ou por parser.
4. Os dados são persistidos no SQLite.
5. O dashboard consolida saldo, categorias e lançamentos recentes.
6. O webhook fake simula a evolução para o WhatsApp.

## Padrões aplicados

- Post/Redirect/Get nos POSTs de sucesso em transações;
- validação centralizada no service;
- parser desacoplado da rota;
- dados do gráfico preparados no backend e renderizados no frontend;
- base separada para futuras consultas financeiras por texto.

## Observação sobre `src/`

A pasta `src/` ainda existe no repositório, mas a aplicação ativa roda por `app/` e `run.py`.

Recomendação:

- manter `src/` preservada por enquanto, para evitar remoção insegura;
- remover em uma branch dedicada apenas depois de confirmar que não há uso indireto, documentação pendente ou dependência futura.
