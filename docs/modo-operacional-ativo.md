# Modo Operacional Ativo — 13/11/2026

**Autorização explícita concedida.**

## Flags atuais

| Flag | Valor |
|------|-------|
| OPERATIONAL_GO | `true` |
| MODO_SINTETICO | `false` |
| WRITE_ESCOLAR | `CONTROLADO` |

## O que muda

- O sistema pode operar com dados reais via conector auditado.
- Escrita escolar continua controlada (somente através do fluxo de integração).
- Advisory only permanece o padrão das recomendações.
- Log imutável e decisão humana continuam obrigatórios.

## Como verificar

```python
from config import status_modo
print(status_modo())
```

Modo operacional ativado com auditoria contínua.
