# Orquestrador CoordIA

Você pede. Ele encaminha e aciona.

## Uso

```python
from orquestrador import Orquestrador

orch = Orquestrador()
resultado = orch.pedir("Detectar pendências e priorizar", eventos)
print(resultado["acoes"])
```

## O que ele reconhece

| Palavras no pedido | Ação |
|--------------------|-------|
| pendência, priorizar, missão, detectar | Executa Missão 001 |
| peso, ajustar, frequência | Ajusta pesos dinâmicos |
| status, painel, situação | Consulta status |
| teste, verificar | Sugere verificação |
| treinar, colônia | Sugere treinamento |

## Princípio

Ele aciona, mas a decisão final continua humana.
