"""
Agentes especializados para orquestração.
Cada um tem uma responsabilidade clara.
"""

from typing import List, Dict

class AgenteDetector:
    """Foca apenas na detecção."""
    def executar(self, eventos: List[Dict]) -> Dict:
        from agents.nucleo import Nucleo
        from agents.detectores import DETECTORES_PADRAO
        from agents.detectores_extras import DETECTORES_EXTRAS
        from prototype.alertas_planejamento import detector_planejamento
        nucleo = Nucleo(DETECTORES_PADRAO + DETECTORES_EXTRAS + [detector_planejamento])
        recs = []
        for ev in eventos:
            recs.extend(nucleo.processar(ev))
        return {"agente": "detector", "recomendacoes": recs}

class AgentePriorizador:
    """Foca apenas na priorização."""
    def executar(self, recomendacoes: List[Dict]) -> Dict:
        from agents.priorizacao import priorizar
        priorizadas = priorizar(recomendacoes)
        return {"agente": "priorizador", "recomendacoes": priorizadas}

class AgenteAuditor:
    """Verifica advisory e proveniência."""
    def executar(self, recomendacoes: List[Dict]) -> Dict:
        problemas = []
        for rec in recomendacoes:
            if rec.get("status") != "recomendado":
                problemas.append("status inválido")
            if "resolvido" in str(rec).lower() or "executado" in str(rec).lower():
                problemas.append("confirmação indevida")
        return {
            "agente": "auditor",
            "ok": len(problemas) == 0,
            "problemas": problemas
        }

class AgenteDecisor:
    """Prepara a decisão humana (não decide)."""
    def executar(self, recomendacoes: List[Dict]) -> Dict:
        return {
            "agente": "decisor",
            "pendentes": len(recomendacoes),
            "aviso": "Aguardando decisão humana",
            "top": recomendacoes[:3]
        }
