# Integração OpenAI

## Objetivo

Interpretar mensagens financeiras com OpenAI de forma opcional e segura.

## Configuração

```env
OPENAI_API_KEY=
USE_OPENAI_PARSER=false
```

## Estratégia

- usar Structured Outputs;
- validar o JSON retornado;
- cair no parser local se a IA falhar;
- nunca salvar chave no código.

## Fallback

Se:

- `USE_OPENAI_PARSER=false`
- `OPENAI_API_KEY` estiver vazia
- a resposta da IA vier inválida
- ocorrer erro na chamada

então o sistema usa `ParserService`.
