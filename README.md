# COORDIA SMART — Superinvestigação Científica e Engenharia Autônoma

**Arquitetura leve, eficiente e extensível.**

## Ideia central

Núcleo mínimo que gera recomendações advisory com proveniência.  
Tudo o mais (detectores, fontes, notificações, armazenamento) é plugável.

> A capacidade de antecipar cresce junto com a capacidade de provar o que foi feito.

## Começar rápido

```python
from agents.nucleo import Nucleo, detector_frequencia

nucleo = Nucleo([detector_frequencia])
recs = nucleo.processar({
    "tipo": "frequencia",
    "valor": 0.68,
    "fonte": "sistema_escolar",
    "ts": "2026-11-13T21:00:00Z"
})
print(recs)
print(nucleo.exportar_log())
```

## Arquitetura

Veja [`architecture/LEVE.md`](architecture/LEVE.md) — núcleo simples + regras de extensão.

## Princípios

- Advisory only (nenhum agente confirma trabalho concluído)
- Funções puras e interfaces mínimas
- Zero dependências obrigatórias
- Adaptação = novo adapter ou detector (sem mudar o núcleo)
- Log imutável com proveniência

## Estrutura

- `agents/nucleo.py` — núcleo executável e leve
- `architecture/LEVE.md` — design e regras de extensão
- `docs/` — análise SMART/FMDS e mapeamento

Contribuição concreta ao SuperLAB: simples hoje, adaptável sempre.
