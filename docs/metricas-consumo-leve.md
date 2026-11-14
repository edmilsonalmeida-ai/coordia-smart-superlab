# Métricas de Consumo — Modo Leve

**Processo:** `python -u run_leve.py`  
**Data da medição:** 2026-11-13 ~21:58 -04  
**Ambiente:** sandbox

## Resumo

| Métrica | Valor |
|---------|-------|
| CPU % | 0.0 % |
| Memória RSS | ~13.6 MB |
| Memória VSZ | ~17.8 MB |
| Threads | 1 |
| Load average | 0.00 |
| Context switches | muito baixo |
| CPU time acumulado | ~0.02 s após minutos de execução |

## Observações

- Consumo praticamente nulo de CPU (processo dorme 10 s entre ciclos).
- Memória estável, sem crescimento.
- Adequado para deixar rodando continuamente sem impacto.
- Flags de segurança mantidas.

O modo leve cumpre o objetivo de eficiência extrema.
