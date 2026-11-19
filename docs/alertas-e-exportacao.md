# Alertas Configuráveis e Exportação

## Thresholds

```python
from alertas_config import definir_threshold, obter_threshold

definir_threshold("frequencia_minima", 0.8)
print(obter_threshold("frequencia_minima"))
```

## Exportação

```python
from exportar import exportar_recomendacoes

exportar_recomendacoes(recomendacoes, "json")
exportar_recomendacoes(recomendacoes, "csv")
```
