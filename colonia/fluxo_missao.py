#!/usr/bin/env python3
"""
Fluxo de missão da colônia CoordIA.
Você entrega a missão. A colônia organiza, pesquisa, debate, executa e verifica.
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
        """Ponto de entrada: recebe a missão e coordena o fluxo."""
        missao = {
            "descricao": descricao,
            "recebida_em": datetime.now(timezone.utc).isoformat(),
            "fases": {}
        }

        # Fase 1: Organizar
        missao["fases"]["organizar"] = self._organizar(descricao, eventos)

        # Fase 2: Pesquisar
        missao["fases"]["pesquisar"] = self._pesquisar(eventos or [])

        # Fase 3: Debater
        missao["fases"]["debater"] = self._debater(missao["fases"]["pesquisar"])

        # Fase 4: Executar
        missao["fases"]["executar"] = self._executar(eventos or [])

        # Fase 5: Verificar
        missao["fases"]["verificar"] = self._verificar(missao["fases"]["executar"])

        missao["status"] = "concluida_lab"
        missao["aviso"] = "Verificação em laboratório. Continuação externa requer autorização."
        self.historico.append(missao)
        return missao

    def _organizar(self, descricao: str, eventos: List[Dict]) -> Dict:
        """Organiza o trabalho: identifica escopo e recursos."""
        return {
            "escopo": descricao,
            "eventos_recebidos": len(eventos) if eventos else 0,
            "agentes_disponiveis": ["detector", "priorizador", "auditor", "decisor"],
            "status": "organizado"
        }

    def _pesquisar(self, eventos: List[Dict]) -> Dict:
        """Pesquisa: analisa os eventos e identifica padrões."""
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
        """Debate: agentes discutem prioridades e abordagens."""
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
        """Executa: processa eventos e gera recomendações."""
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
        """Verifica: valida advisory e proveniência."""
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
    colonia = Colonia()
    eventos = [
        {"tipo": "frequencia", "valor": 0.45, "aluno_id": "COL-1", "fonte": "colonia"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 7,
         "id_planejamento": "PLN-COL", "disciplina": "Geografia", "aluno_id": "COL-2", "fonte": "colonia"},
        {"tipo": "nota", "valor": 3.5, "aluno_id": "COL-3", "fonte": "colonia"},
    ]

    resultado = colonia.receber_missao("Detectar e priorizar pendências escolares", eventos)

    print(f"Missão: {resultado['descricao']}")
    print(f"Status: {resultado['status']}")
    print()
    for fase, dados in resultado["fases"].items():
        print(f"  {fase}: {dados.get('status', 'ok')}")
    print()
    print(f"Verificação OK: {resultado['fases']['verificar']['ok']}")
    print(f"Recomendações: {resultado['fases']['executar']['recomendacoes']}")

if __name__ == "__main__":
    demo()
