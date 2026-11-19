"""
Controle de idempotência do CoordIA SMART.
Evita reprocessamento de eventos já processados.
"""

import hashlib
import json
from typing import Dict, Set
from pathlib import Path

class Idempotencia:
    def __init__(self, arquivo: str = "processados.json"):
        self.arquivo = Path(arquivo)
        self.processados: Set[str] = set()
        self._carregar()

    def _chave(self, evento: Dict) -> str:
        """Gera chave única para o evento."""
        dados = json.dumps(evento, sort_keys=True, default=str)
        return hashlib.sha256(dados.encode()).hexdigest()[:16]

    def _carregar(self):
        if self.arquivo.exists():
            try:
                dados = json.loads(self.arquivo.read_text())
                self.processados = set(dados.get("processados", []))
            except Exception:
                pass

    def _salvar(self):
        self.arquivo.write_text(json.dumps({"processados": list(self.processados)}))

    def ja_processado(self, evento: Dict) -> bool:
        """Verifica se evento já foi processado."""
        return self._chave(evento) in self.processados

    def marcar_processado(self, evento: Dict):
        """Marca evento como processado."""
        self.processados.add(self._chave(evento))
        self._salvar()

    def filtrar_novos(self, eventos: list) -> list:
        """Retorna apenas eventos não processados."""
        return [e for e in eventos if not self.ja_processado(e)]

    def limpar(self):
        """Limpa histórico de processados."""
        self.processados.clear()
        self._salvar()

# Instância global
idempotencia = Idempotencia()
