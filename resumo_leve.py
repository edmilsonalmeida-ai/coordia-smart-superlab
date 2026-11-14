#!/usr/bin/env python3
"""
Resumo leve do log de auditoria.
Zero dependências.
"""

import json
from pathlib import Path
from collections import Counter

def gerar_resumo(caminho: str = "auditoria_leve.jsonl"):
    p = Path(caminho)
    if not p.exists():
        return {"erro": "log não encontrado"}

    tipos = Counter()
    total = 0
    with p.open(encoding="utf-8") as f:
        for linha in f:
            if not linha.strip():
                continue
            total += 1
            try:
                entrada = json.loads(linha)
                alerta = entrada.get("alerta") or entrada.get("alerta_erro") or {}
                tipos[alerta.get("tipo", "desconhecido")] += 1
            except Exception:
                tipos["parse_error"] += 1

    return {
        "total_entradas": total,
        "tipos": dict(tipos),
        "advisory": True,
        "origem": "sintetico"
    }

if __name__ == "__main__":
    print(json.dumps(gerar_resumo(), ensure_ascii=False, indent=2))
