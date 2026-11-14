"""
Contrato de dados para integração com CoordIA / Comandantes General.
Define o formato mínimo que qualquer conector deve fornecer.
"""

from typing import TypedDict, Optional, List

class EventoEscolar(TypedDict, total=False):
    tipo: str
    aluno_id: str
    turma_id: Optional[str]
    disciplina: Optional[str]
    valor: Optional[float]
    dias_atraso: Optional[int]
    dias_restantes: Optional[int]
    completo: Optional[bool]
    fonte: str
    ts: str
    metadados: Optional[dict]

class Recomendacao(TypedDict):
    tipo: str
    recomendacao: str
    origem: str
    risco: float
    prioridade: float
    status: str
    aluno_id: Optional[str]
    aviso: str

def validar_evento(evento: dict) -> bool:
    return "tipo" in evento and "fonte" in evento
