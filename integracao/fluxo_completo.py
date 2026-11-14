"""
Fluxo completo: evento → recomendação → decisão humana.
"""

from typing import Dict, List
from integracao.conector import ConectorCoordIA
from agents.decisao_humana import registrar_decisao
from agents.feedback import registrar_feedback
from agents.log_persistente import LogPersistente

class FluxoCoordIA:
    def __init__(self):
        self.conector = ConectorCoordIA()
        self.pendentes = []
        self._indices_decididos = set()
        self._log_decisoes = LogPersistente("decisoes.jsonl")

    def processar(self, eventos: List[Dict]) -> List[Dict]:
        recs = self.conector.processar_lote(eventos)
        self.pendentes.extend(recs)
        return recs

    def decidir(self, indice: int, decisao: str, responsavel: str, observacao: str = "") -> Dict:
        """Registra somente decisões humanas explícitas, válidas e ainda não registradas."""
        if type(indice) is not int or indice < 0 or indice >= len(self.pendentes):
            return {"erro": "índice inválido"}
        if indice in self._indices_decididos:
            return {"erro": "decisão já registrada"}
        if decisao not in ("aceito", "rejeitado", "modificado", "em_revisao"):
            return {"erro": "decisão inválida"}
        if not isinstance(responsavel, str) or not responsavel.strip() or responsavel.strip().lower() == "sistema":
            return {"erro": "responsável humano não identificado"}
        if not isinstance(observacao, str):
            return {"erro": "observação inválida"}

        # Índice local não divulga matrícula/identificador de estudante no recibo.
        resultado = registrar_decisao(
            recomendacao_id=f"local-{indice}",
            decisao=decisao,
            responsavel=responsavel.strip(),
            observacao=observacao
        )
        # Uma falha de persistência impede marcar o índice como decidido.
        self._log_decisoes.registrar(resultado)
        self._indices_decididos.add(indice)
        util = "util" if decisao == "aceito" else "nao_util"
        registrar_feedback(f"local-{indice}", util, observacao)
        return resultado

    def resumo(self) -> Dict:
        return {
            "pendentes": len(self.pendentes),
            "modo": self.conector.modo,
            "status": self.conector.status()
        }
