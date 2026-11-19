# Infraestrutura

## Cache

```python
from cache import Cache

cache = Cache()
resultado = cache.obter(evento)
if resultado is None:
    resultado = processar(evento)
    cache.guardar(evento, resultado)
print(cache.estatisticas())
```

## Validação

```python
from validacao import validar_evento, validar_recomendacao, validar_lote

ok, erros = validar_evento(evento)
resultado = validar_lote(eventos)
```

## Observabilidade

```python
from observabilidade import obs

obs.registrar_evento()
obs.registrar_recomendacao(3)
print(obs.saude())
```
