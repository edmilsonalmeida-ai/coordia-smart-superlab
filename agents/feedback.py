"""
Feedback loop leve.
Registra resultado de decisões humanas para ajuste futuro de regras.
Não altera automaticamente o comportamento (apenas registra).
"""

from typing import Dict
from agents.log_persistente import LogPersistente

def registrar_feedback(recomendacao_id: str, resultado: str, observacao: str = "") -> Dict:
    """
    resultado: "util" | "nao_util" | "falso_positivo" | "falso_negativo"
    """
    entrada = {
        "tipo": "feedback",
        "recomendacao_id": recomendacao_id,
        "resultado": resultado,
        "observacao": observacao,
        "aviso": "Registro apenas — não altera regras automaticamente"
    }
    log = LogPersistente("feedback.jsonl")
    log.registrar(entrada)
    return entrada
