"""
Detectores plugáveis — COORDIA SMART
Todos advisory. Nenhum altera status final.
"""

from typing import Dict, Any

def detector_frequencia(evento: Dict) -> Dict | None:
    if evento.get("tipo") == "frequencia" and float(evento.get("valor", 1.0)) < 0.75:
        return {
            "tipo": "pendencia_frequencia",
            "recomendacao": "Verificar ausências e contato com responsável",
            "origem": evento.get("fonte", "desconhecida"),
            "risco": round(1.0 - float(evento["valor"]), 2),
            "aluno_id": evento.get("aluno_id")
        }
    return None

def detector_notas(evento: Dict) -> Dict | None:
    if evento.get("tipo") == "nota" and float(evento.get("valor", 10)) < 5.0:
        return {
            "tipo": "pendencia_nota",
            "recomendacao": "Revisar avaliação e propor recuperação",
            "origem": evento.get("fonte", "desconhecida"),
            "risco": round((5.0 - float(evento["valor"])) / 5.0, 2),
            "aluno_id": evento.get("aluno_id")
        }
    return None

def detector_prazo(evento: Dict) -> Dict | None:
    if evento.get("tipo") == "prazo" and evento.get("dias_restantes", 999) <= 3:
        return {
            "tipo": "pendencia_prazo",
            "recomendacao": "Encaminhar lembrete urgente de entrega",
            "origem": evento.get("fonte", "desconhecida"),
            "risco": 0.8 if evento.get("dias_restantes", 0) <= 1 else 0.5,
            "aluno_id": evento.get("aluno_id")
        }
    return None

def detector_evasao(evento: Dict) -> Dict | None:
    sinais = 0
    if evento.get("frequencia", 1.0) < 0.7:
        sinais += 1
    if evento.get("nota_media", 10) < 5:
        sinais += 1
    if evento.get("pendencias_abertas", 0) >= 3:
        sinais += 1
    if sinais >= 2:
        return {
            "tipo": "risco_evasao",
            "recomendacao": "Acionar equipe pedagógica para intervenção",
            "origem": evento.get("fonte", "desconhecida"),
            "risco": round(sinais / 3.0, 2),
            "aluno_id": evento.get("aluno_id")
        }
    return None

DETECTORES_PADRAO = [
    detector_frequencia,
    detector_notas,
    detector_prazo,
    detector_evasao
]
