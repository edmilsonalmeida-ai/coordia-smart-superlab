#!/usr/bin/env python3
"""
Exportação de dados do CoordIA SMART.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict

def exportar_json(dados: List[Dict], caminho: str):
    Path(caminho).write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return caminho

def exportar_csv(dados: List[Dict], caminho: str):
    if not dados:
        return None
    campos = list(dados[0].keys())
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)
    return caminho

def exportar_recomendacoes(recomendacoes: List[Dict], formato: str = "json"):
    if formato == "csv":
        return exportar_csv(recomendacoes, "recomendacoes.csv")
    return exportar_json(recomendacoes, "recomendacoes.json")

if __name__ == "__main__":
    from missoes.missao_001_pendencias import Missao001
    missao = Missao001()
    eventos = [{"tipo": "frequencia", "valor": 0.5, "aluno_id": "E1", "fonte": "export"}]
    resultado = missao.executar(eventos)
    recs = resultado.get("top_prioridades", [])
    caminho = exportar_recomendacoes(recs, "json")
    print(f"Exportado: {caminho}")
