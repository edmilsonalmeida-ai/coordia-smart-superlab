"""
SuperTest — COORDIA SMART (núcleo potencializado)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.nucleo import Nucleo
from agents.detectores import detector_frequencia

def test_advisory_only():
    nucleo = Nucleo([detector_frequencia])
    evento = {"tipo": "frequencia", "valor": 0.6, "fonte": "teste"}
    recs = nucleo.processar(evento)
    assert len(recs) == 1
    assert recs[0]["status"] == "recomendado"
    assert "resolvido" not in str(recs[0]).lower()

def test_priorizacao():
    nucleo = Nucleo([detector_frequencia])
    evento = {"tipo": "frequencia", "valor": 0.4, "fonte": "teste"}
    recs = nucleo.processar(evento)
    assert "prioridade" in recs[0]
    assert recs[0]["prioridade"] > 0

def test_extensibilidade():
    def detector_custom(evento):
        if evento.get("tipo") == "custom":
            return {"tipo": "custom", "recomendacao": "ok", "origem": "teste", "risco": 0.5}
        return None

    nucleo = Nucleo([detector_frequencia, detector_custom])
    recs = nucleo.processar({"tipo": "custom", "fonte": "teste"})
    assert len(recs) == 1
    assert recs[0]["tipo"] == "custom"

if __name__ == "__main__":
    test_advisory_only()
    test_priorizacao()
    test_extensibilidade()
    print("✓ SuperTest passou: núcleo potencializado, advisory e extensível.")
