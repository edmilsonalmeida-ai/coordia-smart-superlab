# Revisão dos Cinco Papéis Existentes

**Data:** 2026-11-13  
**Contexto:** Fase de protótipo de alertas de planejamentos.

## Os cinco detectores (papéis)

| Papel | Arquivo | Função | Status | Observação |
|-------|---------|---------|--------|-----------|
| Detector Frequência | detectores.py | Alerta baixa frequência | Advisory | Mantido, plugável |
| Detector Notas | detectores.py | Alerta notas baixas | Advisory | Mantido |
| Detector Prazo | detectores.py | Alerta prazos curtos | Advisory | Mantido |
| Detector Evasão | detectores.py | Risco combinado | Advisory | Mantido |
| Detector Documentos | detectores.py | Documentos não entregues | Advisory | Mantido |

## Revisão

- Todos permanecem **advisory only** (status sempre inicia como "recomendado").
- Nenhum escreve em sistemas escolares (WRITE_ESCOLAR=NO_GO).
- Extensíveis via `Nucleo.adicionar_detector`.
- Novo papel adicionado nesta fase: `detector_planejamento` (protótipo sintético), sem alterar os cinco existentes.
- Recomendação: manter os cinco como base; novos papéis entram como plugins.

## Pendências reais

- Integração com fonte real de planejamentos (ainda bloqueada por WRITE_ESCOLAR=NO_GO).
- Definição formal de thresholds por disciplina.
- UI de revisão humana para os alertas.
