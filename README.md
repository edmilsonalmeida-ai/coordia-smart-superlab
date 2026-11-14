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
- `config.py` — flags de segurança (OPERATIONAL_GO=false, WRITE_ESCOLAR=NO_GO)

Advisory only. Extensível. Sem dependências obrigatórias.
