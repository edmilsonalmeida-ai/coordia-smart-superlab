"""
Observabilidade do CoordIA SMART.
Métricas de execução e saúde do sistema.
"""

from typing import Dict
from datetime import datetime, timezone
from config import status_modo

class Observabilidade:
    def __init__(self):
        self.inicio = datetime.now(timezone.utc)
        self.eventos_processados = 0
        self.recomendacoes_geradas = 0
        self.erros = 0

    def registrar_evento(self):
        self.eventos_processados += 1

    def registrar_recomendacao(self, quantidade: int = 1):
        self.recomendacoes_geradas += quantidade

    def registrar_erro(self):
        self.erros += 1

    def saude(self) -> Dict:
        uptime = (datetime.now(timezone.utc) - self.inicio).total_seconds()
        return {
            "uptime_segundos": round(uptime, 1),
            "eventos_processados": self.eventos_processados,
            "recomendacoes_geradas": self.recomendacoes_geradas,
            "erros": self.erros,
            "taxa_erro": round(self.erros / max(1, self.eventos_processados), 3),
            "modo": status_modo()
        }

# Instância global
obs = Observabilidade()
