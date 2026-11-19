"""
Cofre de credenciais do CoordIA SMART.
Armazena credenciais de forma segura para uso pelos agentes.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timezone

class Cofre:
    def __init__(self, arquivo: str = ".cofre.json"):
        self.arquivo = Path(arquivo)
        self.credenciais: Dict[str, Dict] = {}
        self._carregar()

    def _carregar(self):
        if self.arquivo.exists():
            try:
                self.credenciais = json.loads(self.arquivo.read_text())
            except Exception:
                self.credenciais = {}

    def _salvar(self):
        self.arquivo.write_text(json.dumps(self.credenciais, indent=2))

    def _hash(self, valor: str) -> str:
        return hashlib.sha256(valor.encode()).hexdigest()

    def depositar(self, servico: str, usuario: str, senha: str, extras: Dict = None) -> Dict:
        """Deposita credenciais de um serviço."""
        self.credenciais[servico] = {
            "usuario": usuario,
            "senha_hash": self._hash(senha),
            "senha": senha,  # Em produção, criptografar
            "extras": extras or {},
            "depositado_em": datetime.now(timezone.utc).isoformat()
        }
        self._salvar()
        return {"status": "depositado", "servico": servico}

    def obter(self, servico: str) -> Optional[Dict]:
        """Obtém credenciais de um serviço."""
        return self.credenciais.get(servico)

    def listar(self) -> list:
        """Lista serviços com credenciais."""
        return list(self.credenciais.keys())

    def remover(self, servico: str) -> bool:
        if servico in self.credenciais:
            del self.credenciais[servico]
            self._salvar()
            return True
        return False

    def tem(self, servico: str) -> bool:
        return servico in self.credenciais

# Instância global
cofre = Cofre()
