#!/usr/bin/env python3
"""
Fluxo de missão da colônia CoordIA.
Você entrega a missão. A colônia organiza, pesquisa, debate, executa e verifica.
Se precisar, sai do laboratório com autorização.
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
        self.fora_do_lab = False

    def receber_missao(self, descricao: str, eventos: List[Dict] = None) -> Dict:
        """Ponto de entrada: recebe a missão e coordena o fluxo."""
        missao = {
            "descricao": descricao,
            "recebida_em": datetime.now(timezone.utc).isoformat(),
            "fases": {},
            "ambiente": "laboratorio"
        }

        # Fases dentro do laboratório
        missao["fases"]["organizar"] = self._organizar(descricao, eventos)
        missao["fases"]["pesquisar"] = self._pesquisar(eventos or [])
        missao["fases"]["debater"] = self._debater(missao["fases"]["pesquisar"])
        missao["fases"]["executar"] = self._executar(eventos or [])
        missao["fases"]["verificar"] = self._verificar(missao["fases"]["executar"])

        # Avalia se precisa sair do lab
        missao["precisa_sair"] = self._avaliar_saida(missao)

        missao["status"] = "concluida_lab"
        missao["aviso"] = "Verificação em laboratório concluída."
        self.historico.append(missao)
        return missao

    def sair_do_laboratorio(self, missao: Dict, autorizacao: str) -> Dict:
        """Sai do laboratório com autorização explícita."""
        if autorizacao != "AUTORIZADO-SAIR":
            return {"erro": "Autorização inválida", "status": "bloqueado"}

        self.fora_do_lab = True
        missao["ambiente"] = "externo"
        missao["saiu_em"] = datetime.now(timezone.utc).isoformat()
        missao["status"] = "em_operacao_externa"
        missao["aviso"] = "Operação externa. Advisory only. Decisão humana obrigatória."
        return missao

    def _avaliar_saida(self, missao: Dict) -> Dict:
        """Avalia se a missão precisa continuar fora do lab."""
        verificar = missao["fases"].get("verificar", {})
        executar = missao["fases"].get("executar", {})

        motivos = []
        if executar.get("recomendacoes", 0) > 0:
            motivos.append("Recomendações geradas requerem ação humana")
        if not verificar.get("ok", True):
            motivos.append("Verificação encontrou problemas")

        return {
            "necessario": len(motivos) > 0,
            "motivos": motivos,
            "autorizacao_requerida": "AUTORIZADO-SAIR"
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
    colonia = Colonia()
    eventos = [
        {"tipo": "frequencia", "valor": 0.45, "aluno_id": "COL-1", "fonte": "colonia"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 7,
         "id_planejamento": "PLN-COL", "disciplina": "Geografia", "aluno_id": "COL-2", "fonte": "colonia"},
    ]

    # Fluxo no laboratório
    resultado = colonia.receber_missao("Detectar pendências", eventos)
    print(f"Missão: {resultado['descricao']}")
    print(f"Ambiente: {resultado['ambiente']}")
    print(f"Precisa sair: {resultado['precisa_sair']['necessario']}")
    print(f"Motivos: {resultado['precisa_sair']['motivos']}")

    # Saída controlada
    if resultado["precisa_sair"]["necessario"]:
        print("\nSolicitando saída do laboratório...")
        resultado = colonia.sair_do_laboratorio(resultado, "AUTORIZADO-SAIR")
        print(f"Ambiente: {resultado['ambiente']}")
        print(f"Status: {resultado['status']}")

if __name__ == "__main__":
    demo()
