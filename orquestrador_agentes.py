#!/usr/bin/env python3
"""
Orquestrador de agentes especializados.
Coordena detector → priorizador → auditor → decisor.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from typing import List, Dict
from agentes.especializados import (
    AgenteDetector, AgentePriorizador, AgenteAuditor, AgenteDecisor
)

class OrquestradorAgentes:
    def __init__(self):
        self.detector = AgenteDetector()
        self.priorizador = AgentePriorizador()
        self.auditor = AgenteAuditor()
        self.decisor = AgenteDecisor()

    def executar_fluxo(self, eventos: List[Dict]) -> Dict:
        """Executa o fluxo completo de agentes."""
        # 1. Detectar
        det = self.detector.executar(eventos)
        recs = det["recomendacoes"]

        # 2. Priorizar
        pri = self.priorizador.executar(recs)
        priorizadas = pri["recomendacoes"]

        # 3. Auditar
        aud = self.auditor.executar(priorizadas)

        # Sem aprovação do auditor, nenhuma recomendação vai ao decisor.
        if not aud["ok"]:
            return {
                "fluxo": "detector → priorizador → auditor (BLOQUEADO)",
                "eventos": len(eventos),
                "recomendacoes": len(priorizadas),
                "auditoria_ok": False,
                "bloqueado": True,
                "problemas_auditoria": aud["problemas"],
                "pendentes_decisao": 0,
                "top": [],
                "aviso": "Fail-closed: auditoria reprovada, sem encaminhamento"
            }

        # 4. Preparar decisão humana somente após a auditoria.
        dec = self.decisor.executar(priorizadas)
        return {
            "fluxo": "detector → priorizador → auditor → decisor",
            "eventos": len(eventos),
            "recomendacoes": len(priorizadas),
            "auditoria_ok": True,
            "bloqueado": False,
            "problemas_auditoria": [],
            "pendentes_decisao": dec["pendentes"],
            "top": dec["top"],
            "aviso": "Advisory only — decisão humana obrigatória"
        }

def demo():
    orch = OrquestradorAgentes()
    eventos = [
        {"tipo": "frequencia", "valor": 0.45, "aluno_id": "A1", "fonte": "orq"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 7,
         "id_planejamento": "PLN-ORQ", "disciplina": "História", "aluno_id": "A2", "fonte": "orq"},
        {"tipo": "tarefa", "dias_atraso": 4, "aluno_id": "A3", "fonte": "orq"},
    ]
    resultado = orch.executar_fluxo(eventos)
    print("Fluxo:", resultado["fluxo"])
    print(f"Eventos: {resultado['eventos']} | Recomendações: {resultado['recomendacoes']}")
    print(f"Auditoria OK: {resultado['auditoria_ok']}")
    print(f"Pendentes de decisão: {resultado['pendentes_decisao']}")
    print("Top:")
    for t in resultado["top"]:
        print(f"  [{t.get('prioridade', 0):.2f}] {t['tipo']}")

if __name__ == "__main__":
    demo()
