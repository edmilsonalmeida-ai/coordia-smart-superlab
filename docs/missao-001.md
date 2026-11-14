# Missão 001 — Detecção e Priorização de Pendências

**Primeira missão real do CoordIA SMART.**

## Objetivo

Detectar pendências escolares, priorizá-las e encaminhá-las para decisão humana.

## Escopo

- Frequência
- Planejamentos
- Notas
- Tarefas atrasadas
- Participação

## Como executar

```python
from missoes.missao_001_pendencias import Missao001

missao = Missao001()
resultado = missao.executar(eventos)
missao.registrar_decisao(0, "aceito", "coordenador", "Ação tomada")
```

## Modo

Operacional ativo. Advisory only. Decisão humana obrigatória.
