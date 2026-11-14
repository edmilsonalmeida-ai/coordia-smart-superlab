#!/usr/bin/env python3
"""
Resumo inteligente do log de auditoria.
Agrupa por tipo e prioridade.
"""

import json
from pathlib import Path
from collections import defaultdict

def gerar(caminho: str = "auditoria.jsonl"):
    p = Path(caminho)
    if not p.exists():
        return {"total": 0, "por_tipo": {}, "alta_prioridade": []}

    por_tipo = defaultdict(int)
    alta = []
    total = 0

    with p.open(encoding="utf-8") as f:
        for linha in f:
            if not linha.strip():
                continue
            total += 1
            try:
                entrada = json.loads(linha)
                rec = entrada.get("recomendacao", {})
                tipo = rec.get("tipo", "desconhecido")
                por_tipo[tipo] += 1
                if rec.get("prioridade", 0) >= 0.8:
                    alta.append({
                        "tipo": tipo,
                        "prioridade": rec.get("prioridade"),
                        "recomendacao": rec.get("recomendacao", "")[:80]
                    })
            except Exception:
                pass

    return {
        "total": total,
        "por_tipo": dict(por_tipo),
        "alta_prioridade": alta[:10],
        "advisory": True
    }

if __name__ == "__main__":
    print(json.dumps(gerar(), ensure_ascii=False, indent=2))
