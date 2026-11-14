"""
Detectores extras — potencialização.
Advisory only.
"""

from typing import Dict

def detector_participacao(evento: Dict):
    if evento.get("tipo") == "participacao" and evento.get("valor", 1.0) < 0.4:
        return {
            "tipo": "baixa_participacao",
            "recomendacao": f"Estimular participação do aluno {evento.get('aluno_id')}",
            "origem": evento.get("fonte", "sintetico"),
            "risco": 0.6,
            "status": "recomendado"
        }
    return None

def detector_tarefa_atrasada(evento: Dict):
    if evento.get("tipo") == "tarefa" and evento.get("dias_atraso", 0) > 3:
        return {
            "tipo": "tarefa_atrasada",
            "recomendacao": f"Cobrar tarefa atrasada ({evento.get('dias_atraso')} dias)",
            "origem": evento.get("fonte", "sintetico"),
            "risco": min(1.0, 0.5 + evento.get("dias_atraso", 0) * 0.05),
            "status": "recomendado"
        }
    return None

DETECTORES_EXTRAS = [detector_participacao, detector_tarefa_atrasada]
