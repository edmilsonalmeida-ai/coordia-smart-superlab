#!/usr/bin/env python3
"""
Missão 001 — Primeira missão real do CoordIA SMART
Foco: detectar, priorizar e encaminhar pendências escolares.
Modo operacional ativo. Advisory + decisão humana.
"""

from typing import List, Dict
from integracao.fluxo_completo import FluxoCoordIA
from datetime import datetime, timezone

class Missao001:
    """Primeira missão operacional: pendências escolares."""

    def __init__(self):
        self.fluxo = FluxoCoordIA()
        self.id = "MISSAO-001"
        self.nome = "Detecção e Priorização de Pendências"
        self.iniciada_em = datetime.now(timezone.utc).isoformat()

    def executar(self, eventos: List[Dict]) -> Dict:
        """Executa a missão sobre um lote de eventos."""
        recomendacoes = self.fluxo.processar(eventos)
        return {
            "missao": self.id,
            "nome": self.nome,
            "iniciada_em": self.iniciada_em,
            "eventos_processados": len(eventos),
            "recomendacoes": len(recomendacoes),
            "top_prioridades": recomendacoes[:5],
            "status": "executada",
            "modo": self.fluxo.conector.modo,
            "aviso": "Advisory only — decisão humana obrigatória"
        }

    def registrar_decisao(self, indice: int, decisao: str, responsavel: str, observacao: str = ""):
        return self.fluxo.decidir(indice, decisao, responsavel, observacao)

    def relatorio(self) -> Dict:
        return {
            "missao": self.id,
            "nome": self.nome,
            "resumo": self.fluxo.resumo(),
            "operational_go": True
        }

def demo():
    """Demonstração da missão com dados de exemplo."""
    missao = Missao001()
    eventos = [
        {"tipo": "frequencia", "valor": 0.48, "aluno_id": "ALU-101", "fonte": "operacional"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 8,
         "id_planejamento": "PLN-201", "disciplina": "Matemática", "aluno_id": "ALU-102", "fonte": "operacional"},
        {"tipo": "nota", "valor": 3.2, "aluno_id": "ALU-103", "fonte": "operacional"},
        {"tipo": "tarefa", "dias_atraso": 5, "aluno_id": "ALU-104", "fonte": "operacional"},
        {"tipo": "participacao", "valor": 0.25, "aluno_id": "ALU-105", "fonte": "operacional"},
    ]
    resultado = missao.executar(eventos)
    print(f"Missão {resultado['missao']}: {resultado['nome']}")
    print(f"Eventos: {resultado['eventos_processados']} | Recomendações: {resultado['recomendacoes']}")
    print("Top prioridades:")
    for rec in resultado["top_prioridades"]:
        print(f"  [{rec.get('prioridade', 0):.2f}] {rec['tipo']}: {rec['recomendacao'][:60]}")
    return resultado

if __name__ == "__main__":
    demo()
