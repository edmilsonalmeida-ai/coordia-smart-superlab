# Alertas Automáticos de Falhas

## Uso

```python
from alertas_falha import alerta_falha
from monitor import monitor

# Verifica métricas e gera alertas
alertas = alerta_falha.verificar(monitor.metricas())

# Lista alertas recentes
print(alerta_falha.listar())
```

## Thresholds padrão

| Threshold | Valor |
|-----------|-------|
| taxa_erro_max | 10% |
| tempo_max_ms | 1000ms |
| erros_consecutivos | 3 |

## Ajustar thresholds

```python
alerta_falha.definir_threshold("taxa_erro_max", 0.05)
```

## Callbacks

```python
def meu_callback(alerta):
    # Enviar notificação, registrar em log, etc.
    pass

alerta_falha.registrar_callback(meu_callback)
```

## Severidades

- `medio` — atenção
- `alto` — ação recomendada
- `critico` — ação imediata
