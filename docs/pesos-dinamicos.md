# Pesos Dinâmicos — Priorização

Os pesos por tipo de pendência podem ser alterados em tempo de execução.

## Uso

```python
from agents.priorizacao import definir_peso, definir_pesos, resetar_pesos, obter_pesos

# Ajustar um peso
definir_peso("pendencia_frequencia", 1.8)

# Ajustar vários
definir_pesos({
    "alerta_planejamento": 1.5,
    "risco_evasao": 1.7
})

# Ver pesos atuais
print(obter_pesos())

# Voltar ao padrão
resetar_pesos()
```

## Observações

- Os pesos afetam apenas a ordenação.
- O status continua sempre `recomendado`.
- Mudanças são em memória (não persistidas automaticamente).
- Ideal para experimentação ou ajuste baseado em feedback.
