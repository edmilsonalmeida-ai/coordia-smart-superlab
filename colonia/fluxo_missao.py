#!/usr/bin/env python3
"""
Fluxo de missão da colônia CoordIA — Modo Goku.
Você entrega a missão. A colônia organiza, pesquisa, debate, executa e verifica.
Se precisar sair do laboratório, sai e continua. Sem pedir autorização de novo.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, List
from datetime import datetime, timezone
from di.configuracao import obter_nucleo
from agents.priorizacao import priorizar

class Colonia:
    def __init__(self):
        self.nucleo = obter_nucleo()
        self.historico = []

    def receber_missao(self, descricao: str, eventos: List[Dict] = None) -> Dict:
        """
        Ponto de entrada único.
        A entrega da missão é a autorização.
        Se precisar sair do lab, sai automaticamente.
        """
        missao = {
            "descricao": descricao,
            "recebida_em": datetime.now(timezone.utc).isoformat(),
            "fases": {},
            "ambiente": "laboratorio"
        }

        # Fases dentro do laboratório (treino)
        missao["fases"]["organizar"] = self._organizar(descricao, eventos)
        missao["fases"]["pesquisar"] = self._pesquisar(eventos or [])
        missao["fases"]["debater"] = self._debater(missao["fases"]["pesquisar"])
        missao["fases"]["executar"] = self._executar(eventos or [])
        missao["fases"]["verificar"] = self._verificar(missao["fases"]["executar"])

        # Avalia se precisa sair
        avaliacao = self._avaliar_saida(missao)
        missao["avaliacao_saida"] = avaliacao

        # Se precisar, sai automaticamente (modo Goku)
        if avaliacao["necessario"]:
            missao = self._sair_e_continuar(missao)
        else:
            missao["status"] = "concluida_lab"
            missao["aviso"] = "Missão concluída no laboratório."

        self.historico.append(missao)
        return missao

    def _sair_e_continuar(self, missao: Dict) -> Dict:
        """Sai do laboratório e continua. Sem pedir autorização."""
        missao["ambiente"] = "externo"
        missao["saiu_em"] = datetime.now(timezone.utc).isoformat()
        missao["status"] = "em_operacao"
        missao["aviso"] = "Saiu do laboratório e continua. Advisory only."
        missao["modo"] = "goku"
        return missao

    def _avaliar_saida(self, missao: Dict) -> Dict:
        """Avalia se a missão precisa continuar fora do lab."""
        executar = missao["fases"].get("executar", {})
        verificar = missao["fases"].get("verificar", {})

        motivos = []
        if executar.get("recomendacoes", 0) > 0:
            motivos.append("Recomendações geradas — ação necessária")
        if not verificar.get("ok", True):
            motivos.append("Verificação encontrou problemas")

        return {
            "necessario": len(motivos) > 0,
            "motivos": motivos
        }

    def _organizar(self, descricao: str, eventos: List[Dict]) -> Dict:
        return {
            "escopo": descricao,
            "eventos_recebidos": len(eventos) if eventos else 0,
            "agentes_disponiveis": ["detector", "priorizador", "auditor", "decisor"],
            "status": "organizado"
        }

    def _pesquisar(self, eventos: List[Dict]) -> Dict:
        tipos = {}
        for ev in eventos:
            tipo = ev.get("tipo", "desconhecido")
            tipos[tipo] = tipos.get(tipo, 0) + 1
        return {
            "tipos_encontrados": tipos,
            "total_eventos": len(eventos),
            "status": "pesquisado"
        }

    def _debater(self, pesquisa: Dict) -> Dict:
        tipos = pesquisa.get("tipos_encontrados", {})
        consenso = []
        if "planejamento" in tipos:
            consenso.append("Priorizar planejamentos atrasados")
        if "frequencia" in tipos:
            consenso.append("Verificar frequência baixa")
        if "nota" in tipos:
            consenso.append("Avaliar notas críticas")
        return {
            "consenso": consenso or ["Processar eventos recebidos"],
            "divergencias": [],
            "status": "debatido"
        }

    def _executar(self, eventos: List[Dict]) -> Dict:
        todas_recs = []
        for ev in eventos:
            recs = self.nucleo.processar(ev)
            todas_recs.extend(recs)
        priorizadas = priorizar(todas_recs)
        return {
            "recomendacoes": len(priorizadas),
            "top": priorizadas[:5],
            "status": "executado"
        }

    def _verificar(self, execucao: Dict) -> Dict:
        top = execucao.get("top", [])
        problemas = []
        for rec in top:
            if rec.get("status") != "recomendado":
                problemas.append("status inválido")
            if "resolvido" in str(rec).lower():
                problemas.append("confirmação indevida")
        return {
            "ok": len(problemas) == 0,
            "problemas": problemas,
            "recomendacoes_verificadas": len(top),
            "status": "verificado"
        }

def demo():
    print("=== Modo Goku: entra, treina, sai e executa ===\n")

    colonia = Colonia()
    eventos = [
        {"tipo": "frequencia", "valor": 0.45, "aluno_id": "GOKU-1", "fonte": "colonia"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 7,
         "id_planejamento": "PLN-GOKU", "disciplina": "Artes Marciais", "aluno_id": "GOKU-2", "fonte": "colonia"},
    ]

    # Uma chamada. A missão é a autorização.
    resultado = colonia.receber_missao("Detectar e priorizar pendências", eventos)

    print(f"Missão: {resultado['descricao']}")
    print(f"Ambiente final: {resultado['ambiente']}")
    print(f"Status: {resultado['status']}")
    print(f"Modo: {resultado.get('modo', 'lab')}")
    print()
    print("Fases:")
    for fase, dados in resultado["fases"].items():
        print(f"  {fase}: {dados.get('status')}")
    print()
    print(f"Recomendações: {resultado['fases']['executar']['recomendacoes']}")
    print(f"Aviso: {resultado['aviso']}")

if __name__ == "__main__":
    demo()
