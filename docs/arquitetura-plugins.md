# Arquitetura de Plugins

## Conceito

Detectores e ações podem ser adicionados sem alterar o núcleo.

## Como criar um plugin

```python
from plugins.registro import registro

def meu_detector(evento):
    if evento.get("tipo") == "meu_tipo":
        return {"tipo": "meu_alerta", "recomendacao": "...", "status": "recomendado", "risco": 0.7}
    return None

registro.registrar_detector("meu_detector", meu_detector)
```

## Como usar

```python
import plugins.detectores_plugin  # auto-registro
from plugins.registro import registro
from agents.nucleo import Nucleo

nucleo = Nucleo(registro.obter_detectores())
```

## Plugins incluídos

- `atraso_grave` — atraso >15 dias
- `nota_critica` — nota <3

A arquitetura é aberta. Novos plugins são apenas módulos que se registram.
