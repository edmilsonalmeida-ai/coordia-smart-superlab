# Monitoramento de Desempenho

## Uso básico

```python
from monitor import monitor

inicio = monitor.iniciar_operacao()
# ... operação ...
monitor.finalizar_operacao(inicio, sucesso=True, recs=3)

print(monitor.metricas())
print(monitor.resumo())
```

## Decorator

```python
from monitor import monitorar

@monitorar
def processar(evento):
    return nucleo.processar(evento)
```

## Dashboard

```bash
python dashboard.py
```

## Métricas

- uptime
- eventos processados
- recomendações geradas
- tempo médio e máximo
- eventos por segundo
- taxa de erro
