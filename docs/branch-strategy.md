# Estratégia de Branches

## Branches principais

- `main`: apenas versões estáveis.
- `develop`: branch principal de desenvolvimento.

## Feature branches

- `feature/auth`
- `feature/dashboard`
- `feature/transactions`
- `feature/ai-parser`
- `feature/whatsapp-webhook`
- `feature/docs-readme`

## Fluxo recomendado

1. Atualizar `develop`.
2. Criar uma branch de feature a partir de `develop`.
3. Fazer commits pequenos e objetivos.
4. Abrir Pull Request da feature para `develop`.
5. Revisar, testar e fazer merge.
6. Promover `develop` para `main` somente quando a versão estiver estável.

## Comandos úteis

```bash
git checkout develop
git pull origin develop
git checkout -b feature/nome-da-feature

git add .
git commit -m "feat(nome): descreve a entrega"

git checkout develop
git merge feature/nome-da-feature

git push origin feature/nome-da-feature
```
