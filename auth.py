"""
Autenticação básica do CoordIA SMART.
Controle de acesso para coordenadores.
"""

import hashlib
from typing import Dict, Optional
from datetime import datetime, timezone

class Auth:
    def __init__(self):
        self.usuarios: Dict[str, Dict] = {}
        self.sessoes: Dict[str, Dict] = {}

    def registrar(self, usuario: str, senha: str, papel: str = "coordenador") -> Dict:
        """Registra um usuário."""
        if usuario in self.usuarios:
            return {"erro": "usuário já existe"}
        self.usuarios[usuario] = {
            "senha_hash": hashlib.sha256(senha.encode()).hexdigest(),
            "papel": papel,
            "criado_em": datetime.now(timezone.utc).isoformat()
        }
        return {"status": "registrado", "usuario": usuario, "papel": papel}

    def login(self, usuario: str, senha: str) -> Optional[str]:
        """Autentica e retorna token de sessão."""
        if usuario not in self.usuarios:
            return None
        hash_senha = hashlib.sha256(senha.encode()).hexdigest()
        if self.usuarios[usuario]["senha_hash"] != hash_senha:
            return None
        token = hashlib.sha256(f"{usuario}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        self.sessoes[token] = {
            "usuario": usuario,
            "papel": self.usuarios[usuario]["papel"],
            "inicio": datetime.now(timezone.utc).isoformat()
        }
        return token

    def validar(self, token: str) -> Optional[Dict]:
        """Valida token e retorna dados da sessão."""
        return self.sessoes.get(token)

    def logout(self, token: str) -> bool:
        if token in self.sessoes:
            del self.sessoes[token]
            return True
        return False

# Instância global
auth = Auth()
