#!/usr/bin/env python3
"""
Interface de decisão do CoordIA SMART.
Permite ao coordenador revisar e decidir sobre recomendações.
"""

from typing import List, Dict
from datetime import datetime, timezone
import json
from pathlib import Path

class InterfaceDecisao:
    def __init__(self):
        self.pendentes: List[Dict] = []
        self.decididas: List[Dict] = []
        self.arquivo = Path("decisoes.jsonl")

    def carregar_recomendacoes(self, recomendacoes: List[Dict]):
        """Carrega recomendações para decisão."""
        for i, rec in enumerate(recomendacoes):
            self.pendentes.append({
                "indice": i,
                "recomendacao": rec,
                "status": "pendente"
            })

    def listar_pendentes(self) -> List[Dict]:
        return [p for p in self.pendentes if p["status"] == "pendente"]

    def decidir(self, indice: int, decisao: str, responsavel: str, observacao: str = "") -> Dict:
        """Registra decisão humana."""
        if indice >= len(self.pendentes):
            return {"erro": "índice inválido"}

        item = self.pendentes[indice]
        if item["status"] != "pendente":
            return {"erro": "já decidido"}

        item["status"] = "decidido"
        item["decisao"] = {
            "tipo": decisao,
            "responsavel": responsavel,
            "observacao": observacao,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.decididas.append(item)
        self._persistir(item)
        return {"status": "decidido", "decisao": decisao}

    def _persistir(self, item: Dict):
        with self.arquivo.open("a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def resumo(self) -> Dict:
        return {
            "pendentes": len(self.listar_pendentes()),
            "decididas": len(self.decididas),
            "aceitas": sum(1 for d in self.decididas if d.get("decisao", {}).get("tipo") == "aceito"),
            "rejeitadas": sum(1 for d in self.decididas if d.get("decisao", {}).get("tipo") == "rejeitado")
        }

def demo():
    interface = InterfaceDecisao()
    recs = [
        {"tipo": "pendencia_frequencia", "recomendacao": "Verificar ausências", "prioridade": 0.8},
        {"tipo": "alerta_planejamento", "recomendacao": "Revisar planejamento", "prioridade": 0.9},
    ]
    interface.carregar_recomendacoes(recs)
    print(f"Pendentes: {len(interface.listar_pendentes())}")

    interface.decidir(0, "aceito", "coordenador", "Contato realizado")
    interface.decidir(1, "rejeitado", "coordenador", "Já resolvido")

    print(f"Resumo: {interface.resumo()}")

if __name__ == "__main__":
    demo()
