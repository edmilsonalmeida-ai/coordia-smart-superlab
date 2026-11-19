# Proteção de Branch

## Configuração manual no GitHub

1. Acesse: https://github.com/edmilsonalmeida-ai/coordia-smart-superlab/settings/branches
2. Clique em "Add branch protection rule"
3. Branch name pattern: `main`
4. Marque:
   - [x] Require a pull request before merging
   - [x] Require approvals (1)
   - [x] Require status checks to pass
   - [x] Require branches to be up to date
5. Salve

## Por que é manual

A API do GitHub não permite configurar proteção de branch via token padrão. Requer permissões de admin e configuração pela interface.

## Verificação

Após configurar, tentativas de push direto para `main` serão bloqueadas.
