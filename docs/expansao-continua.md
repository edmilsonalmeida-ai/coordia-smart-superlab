# Expansão Contínua — 13/11/2026

## Adicionado

- Detectores extras: participação e tarefa atrasada
- Resumo inteligente do log (agrupa por tipo e destaca alta prioridade)
- Feedback já integrado no fluxo anterior

## Como usar

```python
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from agents.detectores_extras import DETECTORES_EXTRAS

nucleo = Nucleo(DETECTORES_PADRAO + DETECTORES_EXTRAS)
```

```bash
python resumo_inteligente.py
```

Modo sintético e advisory preservados.
