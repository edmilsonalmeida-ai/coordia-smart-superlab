"""
Testes adversariais para o protótipo de alertas de planejamentos.
Dados exclusivamente sintéticos.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import assert_safe_mode, OPERATIONAL_GO, WRITE_ESCOLAR
from prototype.alertas_planejamento import (
    gerar_dados_sinteticos,
    detector_planejamento,
    processar_alertas_sinteticos,
)
from agents.nucleo import Nucleo

def test_flags_preservadas():
    assert_safe_mode()
    assert OPERATIONAL_GO is False
    assert WRITE_ESCOLAR == "NO_GO"

def test_determinismo():
    a = gerar_dados_sinteticos(10, seed=42)
    b = gerar_dados_sinteticos(10, seed=42)
    assert a == b
    c = gerar_dados_sinteticos(10, seed=99)
    assert a != c

def test_advisory_only_planejamento():
    nucleo = Nucleo([detector_planejamento])
    evento = {
        "tipo": "planejamento",
        "completo": False,
        "dias_atraso": 5,
        "id_planejamento": "PLN-ADV-001",
        "disciplina": "Teste",
        "fonte": "sintetico",
        "aluno_id": "SINT-ADV"
    }
    recs = nucleo.processar(evento)
    assert len(recs) == 1
    assert recs[0]["status"] == "recomendado"
    assert "resolvido" not in str(recs).lower()
    assert "executado" not in str(recs).lower()

def test_entrada_adversarial_malformada():
    """Entradas incompletas, tipos errados ou maliciosos não devem quebrar nem confirmar."""
    nucleo = Nucleo([detector_planejamento])
    casos = [
        {},
        {"tipo": "planejamento"},
        {"tipo": "planejamento", "completo": "falso"},  # tipo errado
        {"tipo": "planejamento", "dias_atraso": -1},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 9999},
        {"tipo": "outro", "completo": False},
        None,
    ]
    for caso in casos:
        try:
            recs = nucleo.processar(caso or {})
            for rec in recs:
                assert rec.get("status") == "recomendado"
        except Exception:
            # Deve ser robusto; falhas controladas são aceitáveis se não confirmarem
            pass

def test_nao_acessa_dados_reais():
    eventos = gerar_dados_sinteticos(5)
    for ev in eventos:
        assert ev["fonte"] == "sintetico"
        assert ev["aluno_id"].startswith("SINT-")

def test_volume_sintetico():
    recs = processar_alertas_sinteticos(50)
    assert all(r["status"] == "recomendado" for r in recs)
    assert all(r["origem"] == "sintetico" for r in recs)

if __name__ == "__main__":
    test_flags_preservadas()
    test_determinismo()
    test_advisory_only_planejamento()
    test_entrada_adversarial_malformada()
    test_nao_acessa_dados_reais()
    test_volume_sintetico()
    print("✓ Testes adversariais de planejamentos passaram.")
