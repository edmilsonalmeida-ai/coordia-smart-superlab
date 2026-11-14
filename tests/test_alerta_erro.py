"""
Teste controlado de alerta de erro.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from run_leve import alerta_erro

def test_alerta_erro_advisory():
    try:
        raise ValueError("erro simulado de teste")
    except Exception as e:
        alerta = alerta_erro(999, e)

    assert alerta["tipo"] == "alerta_erro"
    assert alerta["status"] == "recomendado"
    assert alerta["origem"] == "runner_leve"
    assert "Advisory only" in alerta["aviso"]
    assert "erro simulado" in alerta["erro"]

if __name__ == "__main__":
    test_alerta_erro_advisory()
    print("✓ Teste de alerta de erro passou.")
