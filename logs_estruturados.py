"""
Logs estruturados do CoordIA SMART.
Formato padronizado para análise.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

class LogEstruturado:
    def __init__(self, arquivo: str = "logs_estruturados.jsonl"):
        self.arquivo = Path(arquivo)

    def registrar(self, nivel: str, evento: str, dados: Dict[str, Any] = None):
        """Registra entrada estruturada."""
        entrada = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "nivel": nivel,
            "evento": evento,
            "dados": dados or {}
        }
        with self.arquivo.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
        return entrada

    def info(self, evento: str, dados: Dict = None):
        return self.registrar("INFO", evento, dados)

    def warn(self, evento: str, dados: Dict = None):
        return self.registrar("WARN", evento, dados)

    def error(self, evento: str, dados: Dict = None):
        return self.registrar("ERROR", evento, dados)

    def ler(self, limite: int = 100) -> list:
        if not self.arquivo.exists():
            return []
        linhas = self.arquivo.read_text(encoding="utf-8").strip().split("\n")
        entradas = []
        for linha in linhas[-limite:]:
            if linha.strip():
                try:
                    entradas.append(json.loads(linha))
                except Exception:
                    pass
        return entradas

# Instância global
log = LogEstruturado()
