# Métricas e Relatórios

## Relatório automático

```bash
python relatorio_automatico.py
```

## Métricas de missão

```python
from metricas_missao import calcular_metricas, resumo_textual

metricas = calcular_metricas(recomendacoes)
print(resumo_textual(metricas))
```

## Campos

- total de recomendações
- distribuição por tipo
- prioridade média e máxima
- quantidade de alta prioridade (≥0.8)
