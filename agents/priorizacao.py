"""
Motor de priorização — versão explorada.
Combina risco, tipo, urgência e impacto.
Advisory only.
"""

from typing import List, Dict

FATORES_TIPO = {
    "alerta_erro": 1.6,
    "risco_evasao": 1.5,
    "pendencia_prazo": 1.4,
    "pendencia_frequencia": 1.3,
    "tarefa_atrasada": 1.25,
    "alerta_planejamento": 1.2,
    "baixa_participacao": 1.1,
    "pendencia_nota": 1.15,
    "pendencia_documento": 1.05,
}

def calcular_prioridade(rec: Dict) -> float:
    risco = float(rec.get("risco", 0.5))
    tipo = rec.get("tipo", "")
    fator_tipo = FATORES_TIPO.get(tipo, 1.0)

    # Urgência explícita (dias)
    dias = rec.get("dias_atraso") or rec.get("dias_restantes") or 0
    try:
        dias = float(dias)
    except (TypeError, ValueError):
        dias = 0
    fator_urgencia = min(1.5, 1.0 + abs(dias) * 0.03)

    # Impacto estimado (se presente)
    impacto = float(rec.get("impacto", 1.0))

    score = risco * fator_tipo * fator_urgencia * impacto
    return round(min(1.0, score), 2)

def priorizar(recomendacoes: List[Dict]) -> List[Dict]:
    for rec in recomendacoes:
        rec["prioridade"] = calcular_prioridade(rec)
        rec["status"] = "recomendado"
        rec["fatores"] = {
            "tipo": FATORES_TIPO.get(rec.get("tipo", ""), 1.0),
            "risco_base": rec.get("risco", 0.5)
        }
    return sorted(recomendacoes, key=lambda r: r.get("prioridade", 0), reverse=True)

def explicar_prioridade(rec: Dict) -> str:
    """Gera explicação legível da prioridade."""
    return (
        f"Prioridade {rec.get('prioridade', 0):.2f} = "
        f"risco {rec.get('risco', 0.5)} × "
        f"tipo {FATORES_TIPO.get(rec.get('tipo', ''), 1.0)}"
    )
