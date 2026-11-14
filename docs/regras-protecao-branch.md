# Regras de Proteção de Branch — Recomendação

**Repositório:** edmilsonalmeida-ai/coordia-smart-superlab  
**Branch alvo:** `main`

## Status atual
Nenhuma regra de proteção está ativa (comportamento padrão de repositório novo).

## Recomendação para a próxima fase

Configurar em **Settings → Branches → Add branch protection rule**:

| Regra | Valor sugerido | Motivo |
|-------|----------------|--------|
| Branch name pattern | `main` | Proteger a linha principal |
| Require a pull request before merging | Ativado | Evitar push direto |
| Require approvals | 1 | Revisão humana mínima |
| Require status checks to pass | Ativado | Exigir CI verde |
| Status checks | `CI COORDIA SMART` | O workflow que já existe |
| Require branches to be up to date | Ativado | Evitar merge desatualizado |
| Include administrators | Opcional | Você decide |
| Allow force pushes | Desativado | Proteção extra |
| Allow deletions | Desativado | Evitar exclusão acidental |

## Como configurar (manual)

1. Acesse https://github.com/edmilsonalmeida-ai/coordia-smart-superlab/settings/branches
2. Clique em **Add rule**
3. Preencha conforme a tabela acima
4. Salve

## Observação

A configuração de branch protection **não pode ser feita via API** com as ferramentas atualmente conectadas.  
Deve ser feita manualmente na interface do GitHub.

Depois de configurada, o merge do PR da branch de laboratório exigirá CI verde.
