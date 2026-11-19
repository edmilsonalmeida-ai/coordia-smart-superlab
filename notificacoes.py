"""
Sistema de notificações do CoordIA SMART.
Prepara alertas para envio (e-mail, webhook, etc).
"""

from typing import Dict, List
from datetime import datetime, timezone
import json
from pathlib import Path

class Notificacoes:
    def __init__(self):
        self.fila: List[Dict] = []
        self.enviadas: List[Dict] = []
        self.arquivo = Path("notificacoes.jsonl")

    def criar(self, tipo: str, destinatario: str, mensagem: str, prioridade: str = "normal") -> Dict:
        """Cria uma notificação."""
        notificacao = {
            "id": len(self.fila) + len(self.enviadas),
            "tipo": tipo,
            "destinatario": destinatario,
            "mensagem": mensagem,
            "prioridade": prioridade,
            "criada_em": datetime.now(timezone.utc).isoformat(),
            "status": "pendente"
        }
        self.fila.append(notificacao)
        return notificacao

    def criar_alerta_prioridade(self, recomendacao: Dict, destinatario: str) -> Dict:
        """Cria notificação para alta prioridade."""
        return self.criar(
            tipo="alerta_prioridade",
            destinatario=destinatario,
            mensagem=f"[{recomendacao.get('prioridade', 0):.2f}] {recomendacao.get('tipo')}: {recomendacao.get('recomendacao', '')[:100]}",
            prioridade="alta" if recomendacao.get("prioridade", 0) >= 0.8 else "normal"
        )

    def marcar_enviada(self, notificacao_id: int) -> bool:
        """Marca notificação como enviada."""
        for n in self.fila:
            if n["id"] == notificacao_id:
                n["status"] = "enviada"
                n["enviada_em"] = datetime.now(timezone.utc).isoformat()
                self.enviadas.append(n)
                self.fila.remove(n)
                self._persistir(n)
                return True
        return False

    def pendentes(self) -> List[Dict]:
        return [n for n in self.fila if n["status"] == "pendente"]

    def _persistir(self, notificacao: Dict):
        with self.arquivo.open("a", encoding="utf-8") as f:
            f.write(json.dumps(notificacao, ensure_ascii=False) + "\n")

# Instância global
notificacoes = Notificacoes()
