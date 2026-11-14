# Fluxo Completo — Recomendação + Decisão Humana

## Separação clara

1. **IA** gera recomendação (`status: "recomendado"`).
2. **Humano** registra decisão (`aceito` / `rejeitado` / `modificado`).
3. Ambos ficam no log, distintos e imutáveis.

## Exemplo via CLI

```bash
# 1. Gerar recomendação
python cli.py detectar '{"tipo":"frequencia","valor":0.62,"fonte":"cli","aluno_id":"A999"}'

# 2. Registrar decisão humana
python cli.py decidir rec-001 aceito "coordenador.silva" "Contato realizado"
```

## Exemplo em código

```python
from agents.decisao_humana import registrar_decisao

decisao = registrar_decisao(
    recomendacao_id="abc123",
    decisao="aceito",
    responsavel="equipe.pedagogica",
    observacao="Intervenção agendada"
)
```

Isso garante que recomendação de IA nunca se confunde com trabalho concluído.
