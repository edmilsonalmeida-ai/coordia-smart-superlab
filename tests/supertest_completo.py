"""
SuperTest completo — valida núcleo + detectores + persistência.
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from agents.log_persistente import LogPersistente

def test_fluxo_completo_com_persistencia():
    nucleo = Nucleo(DETECTORES_PADRAO)
    with tempfile.TemporaryDirectory() as tmp:
        log = LogPersistente(str(Path(tmp) / "audit.jsonl"))

        eventos = [
            {"tipo": "frequencia", "valor": 0.6, "fonte": "teste", "aluno_id": "X1"},
            {"tipo": "nota", "valor": 3.5, "fonte": "teste", "aluno_id": "X2"},
        ]

        for ev in eventos:
            recs = nucleo.processar(ev)
            for rec in recs:
                log.registrar({"evento": ev, "recomendacao": rec})

        salvos = log.ler_todos()
        assert len(salvos) == 2
        assert all(s["recomendacao"]["status"] == "recomendado" for s in salvos)
        assert salvos[0]["recomendacao"]["tipo"] == "pendencia_frequencia"

def test_nenhuma_confirmacao_automatica():
    nucleo = Nucleo(DETECTORES_PADRAO)
    recs = nucleo.processar({"tipo": "frequencia", "valor": 0.4, "fonte": "t"})
    for rec in recs:
        assert rec["status"] == "recomendado"
        assert "resolvido" not in rec.values()

if __name__ == "__main__":
    test_fluxo_completo_com_persistencia()
    test_nenhuma_confirmacao_automatica()
    print("✓ SuperTest completo passou.")
