# COORDIA SMART — Superinvestigação Científica e Engenharia Autônoma

**Arquitetura leve, eficiente e extensível.**

## Ideia central

Núcleo mínimo que gera recomendações advisory com proveniência.  
Tudo o mais é plugável. Nenhum agente confirma trabalho concluído.

## Uso rápido

```bash
# Demonstração completa
python run_completo.py

# SuperTests
python tests/supertest_nucleo.py
python tests/supertest_completo.py

# API HTTP mínima
python api/server.py
# Depois: curl -X POST http://127.0.0.1:8080/recomendacao -d '{"tipo":"frequencia","valor":0.6,"fonte":"api"}'
```

## Estrutura

| Caminho | Função |
|---------|---------|
| `agents/nucleo.py` | Núcleo (advisory, log em memória) |
| `agents/detectores.py` | Detectores plugáveis |
| `agents/log_persistente.py` | Log append-only (JSONL) |
| `adapters/exemplo_planilha.py` | Adapter CSV |
| `integracoes/webhook_exemplo.py` | Notificação webhook |
| `api/server.py` | API HTTP (stdlib) |
| `run.py` / `run_completo.py` | Runners |
| `tests/` | SuperTests |
| `architecture/LEVE.md` | Design e regras de extensão |
| `docs/` | Análises SMART/FMDS e melhor caminho |

## Princípios

- Advisory only
- Proveniência obrigatória
- Zero dependências obrigatórias
- Extensão = novo arquivo (sem alterar o núcleo)

Contribuição concreta ao SuperLAB.
