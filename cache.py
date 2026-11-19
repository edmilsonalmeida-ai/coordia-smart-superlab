"""
Cache leve do CoordIA SMART.
Evita reprocessamento de eventos idênticos.
"""

import hashlib
import json
from typing import Dict, Any, Optional

class Cache:
    def __init__(self, max_itens: int = 1000):
        self.cache: Dict[str, Any] = {}
        self.max_itens = max_itens
        self.hits = 0
        self.misses = 0

    def _chave(self, evento: Dict) -> str:
        serializado = json.dumps(evento, sort_keys=True, default=str)
        return hashlib.md5(serializado.encode()).hexdigest()

    def obter(self, evento: Dict) -> Optional[Any]:
        chave = self._chave(evento)
        if chave in self.cache:
            self.hits += 1
            return self.cache[chave]
        self.misses += 1
        return None

    def guardar(self, evento: Dict, resultado: Any):
        if len(self.cache) >= self.max_itens:
            # Remove o mais antigo
            primeira = next(iter(self.cache))
            del self.cache[primeira]
        self.cache[self._chave(evento)] = resultado

    def estatisticas(self) -> Dict:
        total = self.hits + self.misses
        return {
            "hits": self.hits,
            "misses": self.misses,
            "taxa_hit": round(self.hits / total, 2) if total > 0 else 0,
            "itens": len(self.cache)
        }

    def limpar(self):
        self.cache.clear()
        self.hits = 0
        self.misses = 0
