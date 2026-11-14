"""
Fluxo completo: evento → recomendação → decisão humana.
"""

from typing import Dict, List
from integracao.conector import ConectorCoordIA
from agents.decisao_humana import registrar_decisao
from agents.feedback import registrar_feedback

class FluxoCoordIA:
    def __init__(self):
        self.conector = ConectorCoordIA()
        self.pendentes = []

    def processar(self, eventos: List[Dict]) -> List[Dict]:
        recs = self.conector.processar_lote(eventos)
        self.pendentes.extend(recs)
        return recs

    def decidir(self, indice: int, decisao: str, responsavel: str, observacao: str = "") -> Dict:
        """Registra decisão humana sobre uma recomendação pendente."""
        if indice >= len(self.pendentes):
            return {"erro": "índice inválido"}
        rec = self.pendentes[indice]
        resultado = registrar_decisao(
            recomendacao_id=rec.get("id_planejamento") or rec.get("aluno_id") or str(indice),
            decisao=decisao,
            responsavel=responsavel,
            observacao=observacao
        )
        # Feedback opcional
        util = "util" if decisao == "aceito" else "nao_util"
        registrar_feedback(str(indice), util, observacao)
        return resultado

    def resumo(self) -> Dict:
        return {
            "pendentes": len(self.pendentes),
            "modo": self.conector.modo,
            "status": self.conector.status()
        }
