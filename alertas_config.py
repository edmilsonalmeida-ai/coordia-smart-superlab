"""
Configuração de alertas do CoordIA SMART.
Thresholds ajustáveis por tipo.
"""

from typing import Dict

THRESHOLDS_PADRAO = {
    "frequencia_minima": 0.75,
    "nota_minima": 5.0,
    "dias_atraso_alerta": 3,
    "dias_atraso_grave": 15,
    "participacao_minima": 0.4,
}

_thresholds = dict(THRESHOLDS_PADRAO)

def definir_threshold(nome: str, valor: float):
    _thresholds[nome] = valor

def obter_threshold(nome: str) -> float:
    return _thresholds.get(nome, 0)

def obter_todos() -> Dict[str, float]:
    return dict(_thresholds)

def resetar():
    global _thresholds
    _thresholds = dict(THRESHOLDS_PADRAO)
