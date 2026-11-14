"""
Motor de priorização leve.
Ordena recomendações por risco, urgência e impacto estimado.
Advisory only.
"""

from typing import List, Dict

def calcular_prioridade(rec: Dict) -> float:
    risco = float(rec.get("risco", 0.5))
    # Fatores simples e determinísticos
    fator_tipo = {
        "pendencia_frequencia": 1.2,
        "alerta_planejamento": 1.1,
        "pendencia_prazo": 1.3,
        "alerta_erro": 1.5,
        "risco_evasao": 1.4,
    }.get(rec.get("tipo", ""), 1.0)
    return round(min(1.0, risco * fator_tipo), 2)

def priorizar(recomendacoes: List[Dict]) -> List[Dict]:
    for rec in recomendacoes:
        rec["prioridade"] = calcular_prioridade(rec)
        rec["status"] = "recomendado"  # garante advisory
    return sorted(recomendacoes, key=lambda r: r.get("prioridade", 0), reverse=True)
