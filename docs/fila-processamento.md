# Fila de Processamento

## Uso

```python
from fila import FilaProcessamento
from di.configuracao import obter_nucleo

fila = FilaProcessamento()
fila.adicionar_lote(eventos)

nucleo = obter_nucleo()
resultados = fila.processar_todos(nucleo)

print(f"Processados: {fila.total_processados()}")
```

## Métodos

- `adicionar(evento)` — adiciona um evento
- `adicionar_lote(eventos)` — adiciona vários
- `processar_proximo(nucleo)` — processa o próximo
- `processar_todos(nucleo)` — processa a fila inteira
- `pendentes()` — quantidade na fila
