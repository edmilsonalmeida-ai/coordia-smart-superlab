#!/usr/bin/env python3
"""
Métricas de missão do CoordIA SMART.
"""

from typing import List, Dict
from collections import Counter

def calcular_metricas(recomendacoes: List[Dict]) -> Dict:
    if not recomendacoes:
        return {"total": 0, "por_tipo": {}, "prioridade_media": 0}

    tipos = Counter(r.get("tipo", "desconhecido") for r in recomendacoes)
    prioridades = [r.get("prioridade", 0) for r in recomendacoes]

    return {
        "total": len(recomendacoes),
        "por_tipo": dict(tipos),
        "prioridade_media": round(sum(prioridades) / len(prioridades), 2),
        "prioridade_max": max(prioridades),
        "alta_prioridade": sum(1 for p in prioridades if p >= 0.8)
    }

def resumo_textual(metricas: Dict) -> str:
    return (
        f"Total: {metricas['total']} | "
        f"Média: {metricas['prioridade_media']} | "
        f"Alta: {metricas['alta_prioridade']}"
    )

if __name__ == "__main__":
    from missoes.missao_001_pendencias import Missao001
    missao = Missao001()
    eventos = [
        {"tipo": "frequencia", "valor": 0.4, "aluno_id": "M1", "fonte": "metrica"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 12,
         "id_planejamento": "PLN-M", "disciplina": "Biologia", "aluno_id": "M2", "fonte": "metrica"},
    ]
    resultado = missao.executar(eventos)
    metricas = calcular_metricas(resultado.get("top_prioridades", []))
    print(resumo_textual(metricas))
