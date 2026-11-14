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
    """Valida invariantes mínimos antes de expor recomendações à decisão humana.

    A origem declarada não é prova criptográfica da fonte: essa verificação cabe
    ao conector autorizado e a uma auditoria de proveniência separada.
    """
    def executar(self, recomendacoes: List[Dict]) -> Dict:
        problemas = []
        for indice, rec in enumerate(recomendacoes):
            if not isinstance(rec, dict):
                problemas.append(f"recomendacao_{indice}: formato inválido")
                continue
            if rec.get("status") != "recomendado":
                problemas.append(f"recomendacao_{indice}: status inválido")
            if not isinstance(rec.get("tipo"), str) or not rec["tipo"].strip():
                problemas.append(f"recomendacao_{indice}: tipo ausente")
            if not isinstance(rec.get("recomendacao"), str) or not rec["recomendacao"].strip():
                problemas.append(f"recomendacao_{indice}: orientação ausente")
            if not isinstance(rec.get("origem"), str) or rec["origem"].strip().lower() in ("", "desconhecida"):
                problemas.append(f"recomendacao_{indice}: origem não declarada")
            score = rec.get("prioridade")
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
                problemas.append(f"recomendacao_{indice}: prioridade inválida")
            if any(chave in rec for chave in ("decisao", "resolvido", "executado", "concluido", "aprovado")):
                problemas.append(f"recomendacao_{indice}: campos de execução ou decisão indevidos")
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
