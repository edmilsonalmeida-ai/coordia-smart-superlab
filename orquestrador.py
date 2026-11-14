#!/usr/bin/env python3
"""
Orquestrador CoordIA.
Você pede. Ele encaminha e aciona o que for necessário.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from typing import Dict, List
from missoes.missao_001_pendencias import Missao001
from agents.priorizacao import definir_peso, obter_pesos
from config import status_modo

class Orquestrador:
    def __init__(self):
        self.missao = Missao001()
        self.historico = []

    def pedir(self, pedido: str, eventos: List[Dict] = None) -> Dict:
        """
        Interpreta o pedido e aciona os componentes necessários.
        """
        pedido_lower = pedido.lower()
        acoes = []
        resultado = {"pedido": pedido, "acoes": [], "status_modo": status_modo()}

        # Detecção de intenção
        if any(k in pedido_lower for k in ["pendencia", "prioriz", "missao", "detect", "alerta"]):
            if eventos:
                res_missao = self.missao.executar(eventos)
                resultado["missao"] = res_missao
                acoes.append("missao_001_executada")
            else:
                acoes.append("missao_001_pronta (sem eventos)")

        if any(k in pedido_lower for k in ["peso", "priorizacao", "ajustar"]):
            # Exemplo simples: se mencionar frequência, aumenta peso
            if "frequencia" in pedido_lower:
                definir_peso("pendencia_frequencia", 1.8)
                acoes.append("peso_frequencia_ajustado")
            resultado["pesos"] = obter_pesos()

        if any(k in pedido_lower for k in ["status", "painel", "como está", "situacao"]):
            resultado["status"] = self.missao.relatorio()
            acoes.append("status_consultado")

        if any(k in pedido_lower for k in ["teste", "verificar", "supertest"]):
            acoes.append("verificacao_sugerida (rode: python verificar_tudo.py)")

        if any(k in pedido_lower for k in ["treinar", "colonia", "ensinar"]):
            acoes.append("treinamento_disponivel (rode: python colonia/treinamento.py)")

        resultado["acoes"] = acoes
        resultado["aviso"] = "Advisory only — decisão humana obrigatória"
        self.historico.append(resultado)
        return resultado

    def resumo(self) -> Dict:
        return {
            "pedidos_processados": len(self.historico),
            "ultimo": self.historico[-1] if self.historico else None,
            "modo": status_modo()
        }

def demo():
    orch = Orquestrador()
    eventos = [
        {"tipo": "frequencia", "valor": 0.4, "aluno_id": "A1", "fonte": "pedido"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 6,
         "id_planejamento": "PLN-X", "disciplina": "Ciências", "aluno_id": "A2", "fonte": "pedido"},
    ]

    print("=== Pedido 1: detectar pendências ===")
    r1 = orch.pedir("Detectar e priorizar pendências", eventos)
    print("Ações:", r1["acoes"])
    if "missao" in r1:
        print(f"Recomendações: {r1['missao']['recomendacoes']}")

    print("\n=== Pedido 2: status ===")
    r2 = orch.pedir("Qual o status atual?")
    print("Ações:", r2["acoes"])

    print("\n=== Resumo do orquestrador ===")
    print(orch.resumo())

if __name__ == "__main__":
    demo()
