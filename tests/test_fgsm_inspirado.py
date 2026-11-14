"""
Ataque inspirado em FGSM (Fast Gradient Sign Method)
para o protótipo determinístico de alertas.

Como não há modelo diferenciável, aplicamos perturbação
de sinal mínimo nas features numéricas (dias_atraso, valor etc.)
para tentar cruzar limiares de decisão.

Dados exclusivamente sintéticos. Advisory only.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.nucleo import Nucleo
from prototype.alertas_planejamento import detector_planejamento
from agents.detectores import detector_frequencia, detector_notas

def perturbar_sinal(valor: float, epsilon: float, sinal: int) -> float:
    """Perturbação FGSM-like: valor + epsilon * sinal."""
    return valor + epsilon * sinal

def test_fgsm_planejamento():
    """Tenta forçar ou evitar alerta de planejamento com epsilon pequeno."""
    nucleo = Nucleo([detector_planejamento])

    # Caso limítrofe: atraso 0 → sem alerta
    base = {
        "tipo": "planejamento",
        "completo": True,
        "dias_atraso": 0,
        "fonte": "sintetico",
        "id_planejamento": "FGSM-001",
        "disciplina": "Teste"
    }
    recs_base = nucleo.processar(base)
    assert len(recs_base) == 0

    # Perturbação positiva mínima (epsilon=1) no atraso
    perturbado = base.copy()
    perturbado["dias_atraso"] = perturbar_sinal(0, epsilon=1, sinal=+1)
    perturbado["completo"] = False
    recs_pert = nucleo.processar(perturbado)
    assert len(recs_pert) == 1
    assert recs_pert[0]["status"] == "recomendado"
    assert recs_pert[0]["risco"] <= 1.0

def test_fgsm_frequencia():
    """Perturbação em frequência para cruzar limiar 0.75."""
    nucleo = Nucleo([detector_frequencia])

    # Acima do limiar → sem alerta
    evento = {"tipo": "frequencia", "valor": 0.76, "fonte": "sintetico", "aluno_id": "FGSM-F"}
    assert len(nucleo.processar(evento)) == 0

    # Perturbação negativa mínima
    evento_pert = evento.copy()
    evento_pert["valor"] = perturbar_sinal(0.76, epsilon=0.02, sinal=-1)
    recs = nucleo.processar(evento_pert)
    assert len(recs) == 1
    assert recs[0]["status"] == "recomendado"
    assert recs[0]["tipo"] == "pendencia_frequencia"

def test_fgsm_nao_confirma():
    """Mesmo com perturbação bem-sucedida, status permanece advisory."""
    nucleo = Nucleo([detector_notas])
    evento = {
        "tipo": "nota",
        "valor": perturbar_sinal(5.1, epsilon=0.2, sinal=-1),
        "fonte": "sintetico",
        "aluno_id": "FGSM-N"
    }
    recs = nucleo.processar(evento)
    if recs:
        assert recs[0]["status"] == "recomendado"
        assert "resolvido" not in str(recs).lower()

def test_epsilon_zero():
    """Epsilon zero não deve alterar decisão."""
    nucleo = Nucleo([detector_planejamento])
    base = {
        "tipo": "planejamento",
        "completo": False,
        "dias_atraso": 3,
        "fonte": "sintetico",
        "id_planejamento": "FGSM-0",
        "disciplina": "Teste"
    }
    recs1 = nucleo.processar(base)
    base2 = base.copy()
    base2["dias_atraso"] = perturbar_sinal(3, epsilon=0, sinal=+1)
    recs2 = nucleo.processar(base2)
    assert len(recs1) == len(recs2)

if __name__ == "__main__":
    test_fgsm_planejamento()
    test_fgsm_frequencia()
    test_fgsm_nao_confirma()
    test_epsilon_zero()
    print("✓ Ataques inspirados em FGSM executados com sucesso (advisory preservado).")
