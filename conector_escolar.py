"""
Conector escolar do CoordIA SMART.
Estrutura para integração com sistemas reais.
"""

from typing import Dict, List, Protocol
from abc import abstractmethod

class FonteEscolar(Protocol):
    """Interface para fontes de dados escolares."""

    @abstractmethod
    def obter_frequencias(self, turma_id: str = None) -> List[Dict]:
        """Retorna dados de frequência."""
        ...

    @abstractmethod
    def obter_notas(self, turma_id: str = None) -> List[Dict]:
        """Retorna dados de notas."""
        ...

    @abstractmethod
    def obter_planejamentos(self, turma_id: str = None) -> List[Dict]:
        """Retorna dados de planejamentos."""
        ...

class ConectorEscolar:
    """Conector que adapta qualquer fonte para o formato CoordIA."""

    def __init__(self, fonte: FonteEscolar = None):
        self.fonte = fonte

    def definir_fonte(self, fonte: FonteEscolar):
        self.fonte = fonte

    def coletar_eventos(self, turma_id: str = None) -> List[Dict]:
        """Coleta todos os eventos da fonte."""
        if not self.fonte:
            return []

        eventos = []

        # Frequências
        for freq in self.fonte.obter_frequencias(turma_id):
            eventos.append({
                "tipo": "frequencia",
                "aluno_id": freq.get("aluno_id"),
                "valor": freq.get("percentual", 1.0),
                "fonte": "escolar"
            })

        # Notas
        for nota in self.fonte.obter_notas(turma_id):
            eventos.append({
                "tipo": "nota",
                "aluno_id": nota.get("aluno_id"),
                "valor": nota.get("nota"),
                "disciplina": nota.get("disciplina"),
                "fonte": "escolar"
            })

        # Planejamentos
        for plan in self.fonte.obter_planejamentos(turma_id):
            eventos.append({
                "tipo": "planejamento",
                "aluno_id": plan.get("aluno_id"),
                "completo": plan.get("completo", True),
                "dias_atraso": plan.get("dias_atraso", 0),
                "disciplina": plan.get("disciplina"),
                "id_planejamento": plan.get("id"),
                "fonte": "escolar"
            })

        return eventos

class FonteSimulada:
    """Fonte simulada para testes."""

    def obter_frequencias(self, turma_id: str = None) -> List[Dict]:
        return [
            {"aluno_id": "ALU-001", "percentual": 0.65},
            {"aluno_id": "ALU-002", "percentual": 0.90},
        ]

    def obter_notas(self, turma_id: str = None) -> List[Dict]:
        return [
            {"aluno_id": "ALU-001", "nota": 4.5, "disciplina": "Matemática"},
            {"aluno_id": "ALU-003", "nota": 7.0, "disciplina": "Português"},
        ]

    def obter_planejamentos(self, turma_id: str = None) -> List[Dict]:
        return [
            {"id": "PLN-001", "aluno_id": "ALU-002", "completo": False, "dias_atraso": 5, "disciplina": "História"},
        ]
