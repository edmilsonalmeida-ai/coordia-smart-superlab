# Fluxo de Integração Completo

## Componentes adicionados

- `adaptador_planilha.py` — CSV → eventos
- `fluxo_completo.py` — evento → recomendação → decisão humana + feedback

## Exemplo rápido

```python
from integracao.fluxo_completo import FluxoCoordIA

fluxo = FluxoCoordIA()
eventos = [{"tipo": "frequencia", "valor": 0.5, "aluno_id": "A1", "fonte": "sintetico"}]
recs = fluxo.processar(eventos)

# Coordenador decide
fluxo.decidir(0, "aceito", "coordenador", "Contato realizado")
print(fluxo.resumo())
```

Advisory + decisão humana separados.
