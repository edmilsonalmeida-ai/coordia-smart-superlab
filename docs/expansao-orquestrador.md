# Expansão do Orquestrador — 18/11/2026

## Novas intenções reconhecidas

| Palavras | Ação |
|----------|-------|
| agente, fluxo, orquestr | Executa fluxo de agentes especializados |
| reset, padrao (com peso) | Reseta pesos para o padrão |
| conferir | Aciona missão |

## Uso

```python
from orquestrador import Orquestrador

orch = Orquestrador()
orch.pedir("Executar fluxo de agentes", eventos)
orch.pedir("Resetar pesos")
orch.pedir("Conferir pendências", eventos)
```
