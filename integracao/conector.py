"""
Conector base para CoordIA / Comandantes General.
Modo controlado. Sem dados reais por padrão.
"""

from typing import List, Dict
from config import OPERATIONAL_GO, MODO_SINTETICO, ativar_modo_operacional
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from agents.detectores_extras import DETECTORES_EXTRAS
from prototype.alertas_planejamento import detector_planejamento

class ConectorCoordIA:
    def __init__(self):
    self.nucleo = Nucleo(
            DETECTORES_PADRAO + DETECTORES_EXTRAS + [detector_planejamento]
        )
        self.modo = "sintetico" if MODO_SINTETICO else "operacional"

    def processar_lote(self, eventos: List[Dict]) -> List[Dict]:
        """Processa um lote de eventos e retorna recomendações priorizadas."""
        todas = []
        for evento in eventos:
            evento.setdefault("fonte", self.modo)
            recs = self.nucleo.processar(evento)
            todas.extend(recs)
        return todas

    def ativar_operacional(self, confirmacao: str):
        """Ativa modo operacional somente com confirmação explícita."""
        resultado = ativar_modo_operacional(confirmacao)
        self.modo = "operacional"
        return resultado

    def status(self) -> Dict:
        return {
            "modo": self.modo,
            "operational_go": OPERATIONAL_GO,
            "aviso": "Advisory only — decisão humana obrigatória"
        }
