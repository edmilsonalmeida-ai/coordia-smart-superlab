# COORDIA SMART — Superinvestigação Científica e Engenharia Autônoma

**Arquitetura leve, eficiente e extensível.**

## Ideia central

Núcleo mínimo que gera recomendações advisory com proveniência.  
Tudo o mais (detectores, fontes, notificações, armazenamento) é plugável.

> A capacidade de antecipar cresce junto com a capacidade de provar o que foi feito.

## Começar rápido

```bash
python run.py
```

Ou use diretamente:

```python
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO

nucleo = Nucleo(DETECTORES_PADRAO)
recs = nucleo.processar({
    "tipo": "frequencia",
    "valor": 0.68,
    "fonte": "sistema_escolar",
    "aluno_id": "A123"
})
print(recs)
print(nucleo.exportar_log())
```

## SuperTest

```bash
python tests/supertest_nucleo.py
```

## Arquitetura

Veja [`architecture/LEVE.md`](architecture/LEVE.md).

## Estrutura

- `agents/nucleo.py` — núcleo
- `agents/detectores.py` — detectores plugáveis (frequência, notas, prazo, evasão)
- `adapters/exemplo_planilha.py` — adapter CSV
- `run.py` — demonstração completa
- `tests/supertest_nucleo.py` — SuperTest
- `docs/` — análises e melhor caminho

Contribuição concreta ao SuperLAB.
