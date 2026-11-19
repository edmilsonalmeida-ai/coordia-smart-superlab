# Simulação de Cenários

## Uso

```python
from simulacao import simular_cenario, comparar_cenarios

# Cenário único
resultado = simular_cenario(eventos, {"pendencia_frequencia": 1.8})

# Comparar cenários
cenarios = [
    {"nome": "padrao", "pesos": None},
    {"nome": "agressivo", "pesos": {"alerta_erro": 2.0}},
]
resultados = comparar_cenarios(eventos, cenarios)
```

## Objetivo

Testar diferentes configurações de pesos antes de aplicar em produção.
