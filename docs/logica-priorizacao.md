# Lógica de Priorização — Explorada

## Fórmula

```
prioridade = min(1.0, risco × fator_tipo × fator_urgencia × impacto)
```

## Fatores

| Componente | Descrição |
|------------|-----------|
| risco | Valor base da recomendação (0–1) |
| fator_tipo | Multiplicador por tipo de pendência |
| fator_urgencia | Cresce com dias de atraso ou prazo |
| impacto | Fator opcional (padrão 1.0) |

## Fatores de tipo (atual)

- alerta_erro: 1.6
- risco_evasao: 1.5
- pendencia_prazo: 1.4
- pendencia_frequencia: 1.3
- tarefa_atrasada: 1.25
- alerta_planejamento: 1.2
- demais: 1.0–1.15

## Uso

```python
from agents.priorizacao import priorizar, explicar_prioridade
```

A priorização nunca altera o status advisory.
