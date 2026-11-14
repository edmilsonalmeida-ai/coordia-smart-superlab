# Potencialização do Núcleo — 13/11/2026

Autorização concedida. Decisão: potencializar mantendo segurança.

## O que foi adicionado

- **Priorização inteligente** (`agents/priorizacao.py`)
  - Ordena por risco × fator de tipo
  - Garante status `recomendado`

- **Feedback loop** (`agents/feedback.py`)
  - Registra utilidade das recomendações
  - Não altera regras automaticamente

- **Núcleo atualizado**
  - Trata erros de detectores
  - Aplica priorização
  - Enriquece com timestamp e aviso

## Princípios mantidos

- Modo sintético como padrão
- Advisory only
- Proveniência e log imutável
- Controle humano

Pronto para expansão incremental.
