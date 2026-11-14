"""
Persistência simples de log (append-only em arquivo JSONL).
Zero dependências externas.
"""

import json
from pathlib import Path
from typing import Dict, Any

class LogPersistente:
    def __init__(self, caminho: str = "auditoria.jsonl"):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

    def registrar(self, entrada: Dict[str, Any]) -> None:
        with self.caminho.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

    def ler_todos(self) -> list:
        if not self.caminho.exists():
            return []
        with self.caminho.open(encoding="utf-8") as f:
            return [json.loads(linha) for linha in f if linha.strip()]
