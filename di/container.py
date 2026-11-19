"""
Container de injeção de dependência leve.
Registra e resolve dependências sem frameworks externos.
"""

from typing import Any, Callable, Dict, Type

class Container:
    def __init__(self):
        self._registros: Dict[str, Any] = {}
        self._fabricas: Dict[str, Callable] = {}

    def registrar(self, nome: str, instancia: Any):
        """Registra uma instância pronta."""
        self._registros[nome] = instancia
        return self

    def registrar_fabrica(self, nome: str, fabrica: Callable):
        """Registra uma fábrica (chamada na resolução)."""
        self._fabricas[nome] = fabrica
        return self

    def resolver(self, nome: str) -> Any:
        """Resolve uma dependência."""
        if nome in self._registros:
            return self._registros[nome]
        if nome in self._fabricas:
            instancia = self._fabricas[nome](self)
            self._registros[nome] = instancia  # cache
            return instancia
        raise KeyError(f"Dependência '{nome}' não registrada")

    def tem(self, nome: str) -> bool:
        return nome in self._registros or nome in self._fabricas

    def listar(self) -> list:
        return list(set(self._registros.keys()) | set(self._fabricas.keys()))

# Container global
container = Container()
