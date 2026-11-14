# Status do Modo Leve — em execução

**Runner:** `run_leve.py`  
**Modo:** sintético, advisory, baixo consumo  
**Flags:** OPERATIONAL_GO=false | WRITE_ESCOLAR=NO_GO

## Comportamento observado

- Ciclos a cada ~10 segundos
- ~2 alertas por ciclo (lote de 5 eventos)
- Log append-only crescendo de forma controlada
- Zero impacto de recursos

## Como parar

Interromper o processo com Ctrl+C ou kill do processo Python.

Tudo continua leve e seguro.
