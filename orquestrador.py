#!/usr/bin/env python3
"""
Orquestrador CoordIA — versão expandida.
Reconhece pedidos em português com ou sem acentos.
"""

import sys
import unicodedata
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from typing import Dict, List
from missoes.missao_001_pendencias import Missao001
from agents.priorizacao import definir_peso, obter_pesos, resetar_pesos
from config import status_modo
from orquestrador_agentes import OrquestradorAgentes

def normalizar(texto: str) -> str:
    caracteres = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in caracteres if not unicodedata.combining(c))

class Orquestrador:
    def __init__(self):
        self.missao = Missao001()
        self.agentes = OrquestradorAgentes()
        self.historico = []

    def pedir(self, pedido: str, eventos: List[Dict] = None) -> Dict:
        pedido_norm = normalizar(pedido)
        acoes = []
        resultado = {"pedido": pedido, "acoes": [], "status_modo": status_modo()}

        # Missão / detecção
        if any(k in pedido_norm for k in ["pendencia", "prioriz", "missao", "detect", "alerta", "conferir"]):
            if eventos:
                res = self.missao.executar(eventos)
                resultado["missao"] = res
                acoes.append("missao_001_executada")
            else:
                acoes.append("missao_001_pronta")

        # Fluxo de agentes
        if any(k in pedido_norm for k in ["agente", "fluxo", "orquestr"]):
            if eventos:
                resultado["agentes"] = self.agentes.executar_fluxo(eventos)
                acoes.append("fluxo_agentes_executado")

        # Pesos
        if any(k in pedido_norm for k in ["peso", "priorizacao", "ajustar"]):
            if "frequencia" in pedido_norm:
                definir_peso("pendencia_frequencia", 1.8)
                acoes.append("peso_frequencia_ajustado")
            if "reset" in pedido_norm or "padrao" in pedido_norm:
                resetar_pesos()
                acoes.append("pesos_resetados")
            resultado["pesos"] = obter_pesos()

        # Status
        if any(k in pedido_norm for k in ["status", "painel", "como esta", "situacao"]):
            resultado["status"] = self.missao.relatorio()
            acoes.append("status_consultado")

        # Testes
        if any(k in pedido_norm for k in ["teste", "verificar", "supertest"]):
            acoes.append("verificacao_sugerida")

        # Treinamento
        if any(k in pedido_norm for k in ["treinar", "colonia", "ensinar"]):
            acoes.append("treinamento_disponivel")

        resultado["acoes"] = acoes
        resultado["aviso"] = "Advisory only — decisão humana obrigatória"
        self.historico.append(resultado)
        return resultado

    def resumo(self) -> Dict:
        return {
            "pedidos_processados": len(self.historico),
            "ultimo_pedido": self.historico[-1]["pedido"] if self.historico else None,
            "modo": status_modo()
        }
