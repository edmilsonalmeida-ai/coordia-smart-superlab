"""
Fila de processamento do CoordIA SMART.
Processa eventos em lote de forma ordenada.
"""

from typing import List, Dict
from collections import deque

class FilaProcessamento:
    def __init__(self):
        self.fila = deque()
        self.processados = []

    def adicionar(self, evento: Dict):
        self.fila.append(evento)

    def adicionar_lote(self, eventos: List[Dict]):
        for ev in eventos:
            self.adicionar(ev)

    def processar_proximo(self, nucleo) -> Dict:
        if not self.fila:
            return None
        evento = self.fila.popleft()
        recs = nucleo.processar(evento)
        resultado = {"evento": evento, "recomendacoes": recs}
        self.processados.append(resultado)
        return resultado

    def processar_todos(self, nucleo) -> List[Dict]:
        resultados = []
        while self.fila:
            r = self.processar_proximo(nucleo)
            if r:
                resultados.append(r)
        return resultados

    def pendentes(self) -> int:
        return len(self.fila)

    def total_processados(self) -> int:
        return len(self.processados)
