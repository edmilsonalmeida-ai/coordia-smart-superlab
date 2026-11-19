#!/usr/bin/env python3
"""
Histórico de missões executadas.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

ARQUIVO = Path("historico_missoes.jsonl")

def registrar(missao_id: str, resultado: dict):
    entrada = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "missao": missao_id,
        "eventos": resultado.get("eventos_processados", 0),
        "recomendacoes": resultado.get("recomendacoes", 0),
        "modo": resultado.get("modo", "desconhecido")
    }
    with ARQUIVO.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
    return entrada

def listar(limite: int = 10):
    if not ARQUIVO.exists():
        return []
    linhas = ARQUIVO.read_text(encoding="utf-8").strip().split("\n")
    entradas = []
    for linha in linhas[-limite:]:
        if linha.strip():
            try:
                entradas.append(json.loads(linha))
            except Exception:
                pass
    return entradas

if __name__ == "__main__":
    print("Histórico de missões:")
    for e in listar():
        print(f"  {e['ts'][:19]} | {e['missao']} | {e['recomendacoes']} recs")
