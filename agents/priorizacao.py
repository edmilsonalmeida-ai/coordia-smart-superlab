"""
Motor de priorização com pesos dinâmicos.
Pesos podem ser ajustados em tempo de execução.
Advisory only.
"""

from typing import List, Dict
import copy

# Pesos padrão (podem ser sobrescritos)
PESOS_PADRAO = {
    "alerta_erro": 1.6,
    "risco_evasao": 1.5,
    "pendencia_prazo": 1.4,
    "pendencia_frequencia": 1.3,
    "tarefa_atrasada": 1.25,
    "alerta_planejamento": 1.2,
    "baixa_participacao": 1.1,
    "pendencia_nota": 1.15,
    "pendencia_documento": 1.05,
}

# Estado global de pesos dinâmicos
_pesos_ativos = copy.deepcopy(PESOS_PADRAO)

def definir_peso(tipo: str, peso: float):
    """Define ou atualiza o peso de um tipo em tempo de execução."""
    _pesos_ativos[tipo] = float(peso)

def definir_pesos(novos: Dict[str, float]):
    """Substitui vários pesos de uma vez."""
    _pesos_ativos.update({k: float(v) for k, v in novos.items()})

def resetar_pesos():
    """Volta aos pesos padrão."""
    global _pesos_ativos
    _pesos_ativos = copy.deepcopy(PESOS_PADRAO)

def obter_pesos() -> Dict[str, float]:
    return copy.deepcopy(_pesos_ativos)

def calcular_prioridade(rec: Dict) -> float:
    risco = float(rec.get("risco", 0.5))
    tipo = rec.get("tipo", "")
    fator_tipo = _pesos_ativos.get(tipo, 1.0)

    dias = rec.get("dias_atraso") or rec.get("dias_restantes") or 0
    try:
        dias = float(dias)
    except (TypeError, ValueError):
        dias = 0
    fator_urgencia = min(1.5, 1.0 + abs(dias) * 0.03)

    impacto = float(rec.get("impacto", 1.0))
    score = risco * fator_tipo * fator_urgencia * impacto
    return round(min(1.0, score), 2)

def priorizar(recomendacoes: List[Dict]) -> List[Dict]:
    for rec in recomendacoes:
        rec["prioridade"] = calcular_prioridade(rec)
        rec["status"] = "recomendado"
        rec["peso_tipo"] = _pesos_ativos.get(rec.get("tipo", ""), 1.0)
    return sorted(recomendacoes, key=lambda r: r.get("prioridade", 0), reverse=True)

def explicar_prioridade(rec: Dict) -> str:
    return (
        f"Prioridade {rec.get('prioridade', 0):.2f} = "
        f"risco {rec.get('risco', 0.5)} × "
        f"peso {rec.get('peso_tipo', 1.0)}"
    )
