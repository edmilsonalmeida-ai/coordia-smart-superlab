# Orquestração de Agentes

## Agentes especializados

| Agente | Responsabilidade |
|--------|------------------|
| Detector | Gera recomendações a partir dos eventos |
| Priorizador | Ordena por prioridade |
| Auditor | Verifica advisory e proveniência |
| Decisor | Prepara para decisão humana (não decide) |

## Fluxo

```
eventos → Detector → Priorizador → Auditor → Decisor → humano
```

## Uso

```python
from orquestrador_agentes import OrquestradorAgentes

orch = OrquestradorAgentes()
resultado = orch.executar_fluxo(eventos)
```

Cada agente tem uma única responsabilidade. O orquestrador coordena.
