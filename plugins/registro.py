"""
Registro de plugins do CoordIA SMART.
Permite adicionar detectores e ações sem alterar o núcleo.
"""

from typing import Callable, Dict, List

class RegistroPlugins:
    def __init__(self):
        self.detectores: Dict[str, Callable] = {}
        self.acoes: Dict[str, Callable] = {}

    def registrar_detector(self, nome: str, funcao: Callable):
        """Registra um detector."""
        self.detectores[nome] = funcao
        return self

    def registrar_acao(self, nome: str, funcao: Callable):
        """Registra uma ação do orquestrador."""
        self.acoes[nome] = funcao
        return self

    def listar_detectores(self) -> List[str]:
        return list(self.detectores.keys())

    def listar_acoes(self) -> List[str]:
        return list(self.acoes.keys())

    def obter_detectores(self) -> List[Callable]:
        return list(self.detectores.values())

    def executar_acao(self, nome: str, *args, **kwargs):
        if nome not in self.acoes:
            return {"erro": f"ação '{nome}' não encontrada"}
        return self.acoes[nome](*args, **kwargs)

# Instância global
registro = RegistroPlugins()
