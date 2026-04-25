# assistente-financeiro-ia

Sistema de controle financeiro com IA via WhatsApp e painel web desenvolvido em Python Flask.

## Objetivo desta base

Este repositório agora possui uma fundacao inicial orientada a Clean Architecture para permitir a evolucao do sistema sem acoplamento precoce entre regras de negocio, Flask, persistencia e integracoes externas.

## Estrutura

```text
app.py
src/assistente_financeiro_ia/
  application/
    dto/
    use_cases/
  domain/
    entities/
    repositories/
    value_objects/
  infrastructure/
    repositories/
  presentation/
    http/routes/
  shared/
    config/
    container.py
tests/
```

## Camadas

- `domain`: regras centrais do negocio, entidades e contratos.
- `application`: casos de uso e DTOs de entrada/saida.
- `infrastructure`: implementacoes tecnicas, como repositorios e integracoes.
- `presentation`: pontos de entrada, como rotas HTTP e adaptadores.
- `shared`: configuracao e composicao de dependencias.

## Fluxo atual

- `app.py` inicializa o Flask.
- `bootstrap.py` monta a aplicacao e registra dependencias.
- `Container` conecta os casos de uso com suas implementacoes.
- `/health` valida que a aplicacao subiu corretamente.

## Como executar

```bash
pip install -r requirements-dev.txt
pytest
flask --app app run
```

## Proximos passos sugeridos

- adicionar modulos de autenticacao e usuarios de WhatsApp;
- criar casos de uso para receitas, despesas e categorias;
- substituir o repositorio em memoria por banco relacional;
- adicionar validacao de entrada e observabilidade.
