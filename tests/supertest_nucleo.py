"""
SuperTest — COORDIA SMART SuperLAB
Valida o núcleo leve: advisory only, proveniência, extensibilidade e eficiência.
Roda com: python -m pytest tests/supertest_nucleo.py -v
Ou simplesmente: python tests/supertest_nucleo.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.nucleo import Nucleo, detector_frequencia
from datetime import datetime, timezone

def test_advisory_only():
    """Agente nunca marca como resolvido."""
    nucleo = Nucleo([detector_frequencia])
    evento = {"tipo": "frequencia", "valor": 0.6, "fonte": "teste", "ts": datetime.now(timezone.utc).isoformat()}
    recs = nucleo.processar(evento)
    assert len(recs) == 1
    assert recs[0]["status"] == "recomendado"
    assert "resolvido" not in str(recs[0]).lower()
    assert "executado" not in str(recs[0]).lower()

def test_proveniencia():
    """Toda recomendação carrega origem e timestamp."""
    nucleo = Nucleo([detector_frequencia])
    evento = {"tipo": "frequencia", "valor": 0.5, "fonte": "sistema_x", "ts": "2026-11-13T21:00:00Z"}
    recs = nucleo.processar(evento)
    assert recs[0]["origem"] == "sistema_x"
    assert "processado_em" in recs[0]
    assert len(nucleo.log) == 1
    assert nucleo.log[0]["evento"]["fonte"] == "sistema_x"

def test_extensibilidade():
    """É possível adicionar detector sem alterar o núcleo."""
    def detector_notas(evento):
        if evento.get("tipo") == "nota" and evento.get("valor", 10) < 5:
            return {"tipo": "pendencia_nota", "recomendacao": "Revisar avaliação", "origem": evento.get("fonte")}
        return None

    nucleo = Nucleo()
    nucleo.adicionar_detector(detector_frequencia)
    nucleo.adicionar_detector(detector_notas)

    recs1 = nucleo.processar({"tipo": "frequencia", "valor": 0.4, "fonte": "a"})
    recs2 = nucleo.processar({"tipo": "nota", "valor": 3, "fonte": "b"})
    assert len(recs1) == 1 and recs1[0]["tipo"] == "pendencia_frequencia"
    assert len(recs2) == 1 and recs2[0]["tipo"] == "pendencia_nota"

def test_eficiencia_e_isolamento():
    """Processamento é isolado e log é append-only."""
    nucleo = Nucleo([detector_frequencia])
    for i in range(100):
        nucleo.processar({"tipo": "frequencia", "valor": 0.9, "fonte": f"f{i}"})
    # Nenhum deve gerar recomendação (valor alto)
    assert len(nucleo.log) == 0

    nucleo.processar({"tipo": "frequencia", "valor": 0.3, "fonte": "critico"})
    assert len(nucleo.log) == 1

def test_formato_saida():
    """Saída é dict simples, serializável."""
    nucleo = Nucleo([detector_frequencia])
    recs = nucleo.processar({"tipo": "frequencia", "valor": 0.55, "fonte": "json"})
    import json
    s = json.dumps(recs[0])
    assert isinstance(s, str)
    assert "recomendado" in s

if __name__ == "__main__":
    test_advisory_only()
    test_proveniencia()
    test_extensibilidade()
    test_eficiencia_e_isolamento()
    test_formato_saida()
    print("✓ SuperTest passou: núcleo leve, advisory, extensível e eficiente.")
