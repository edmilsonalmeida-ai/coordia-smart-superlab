"""
Thresholds por disciplina do CoordIA SMART.
Regras diferentes para cada disciplina.
"""

from typing import Dict

THRESHOLDS_DISCIPLINA = {
    "Matemática": {"nota_minima": 5.0, "frequencia_minima": 0.75},
    "Português": {"nota_minima": 5.0, "frequencia_minima": 0.75},
    "História": {"nota_minima": 5.0, "frequencia_minima": 0.70},
    "Geografia": {"nota_minima": 5.0, "frequencia_minima": 0.70},
    "Ciências": {"nota_minima": 5.0, "frequencia_minima": 0.75},
    "Educação Física": {"nota_minima": 6.0, "frequencia_minima": 0.80},
    "Artes": {"nota_minima": 6.0, "frequencia_minima": 0.70},
    "_padrao": {"nota_minima": 5.0, "frequencia_minima": 0.75},
}

def obter_threshold(disciplina: str, campo: str) -> float:
    """Obtém threshold para disciplina e campo."""
    config = THRESHOLDS_DISCIPLINA.get(disciplina, THRESHOLDS_DISCIPLINA["_padrao"])
    return config.get(campo, THRESHOLDS_DISCIPLINA["_padrao"].get(campo, 0))

def definir_threshold(disciplina: str, campo: str, valor: float):
    """Define threshold para disciplina."""
    if disciplina not in THRESHOLDS_DISCIPLINA:
        THRESHOLDS_DISCIPLINA[disciplina] = dict(THRESHOLDS_DISCIPLINA["_padrao"])
    THRESHOLDS_DISCIPLINA[disciplina][campo] = valor

def listar_disciplinas() -> list:
    return [d for d in THRESHOLDS_DISCIPLINA.keys() if d != "_padrao"]
