# COORDIA SMART — Superinvestigação Científica e Engenharia Autônoma

**Arquitetura leve, eficiente e extensível.**

## Fase atual (lab/coordia-smart-arquitetura-20261113)

Protótipo determinístico de alertas de planejamentos com dados exclusivamente sintéticos.

### Verificação rápida

```bash
python verificar_tudo.py
python -c "from prototype.cenarios_sinteticos import executar_todos_cenarios; print(executar_todos_cenarios())"
```

### Estrutura principal

- `agents/` — núcleo, detectores (5 papéis), log, decisão humana
- `prototype/` — alertas de planejamentos + cenários
- `tests/` — SuperTests + adversariais
- `.github/workflows/ci.yml` — CI
- `docs/` — revisões, recibos e resultados
- `config.py` — flags declaradas atualmente (OPERATIONAL_GO=true, WRITE_ESCOLAR=CONTROLADO); **isso não comprova autorização escolar nem operação real**

Advisory only. Extensível. Sem dependências obrigatórias.


## Câmara Extra — correções sob revisão

A branch `lab/camara-extra-p0-failclosed-20261114` propõe bloqueio de recomendações reprovadas, autenticação de API e testes sintéticos. A `main` permanece inalterada até revisão.

O log JSONL local é **append-only por convenção**, e não prova imutabilidade criptográfica, custódia externa ou revisão independente. Os quatro papéis do orquestrador são classes Python locais, **não quatro provedores/autônomos externos**.
