"""Contraprovas independentes do fluxo P0 — dados exclusivamente sintéticos.

Executar: python tests/test_camara_extra_failclosed.py
Nenhuma conexão escolar, deploy ou provedor externo.
"""
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentes.especializados import AgenteAuditor
from orquestrador_agentes import OrquestradorAgentes
from integracao.fluxo_completo import FluxoCoordIA
from integracao.api_integracao import Handler


def test_auditor_rejeita_proveniencia_ausente():
    rec = {"tipo": "pendencia", "recomendacao": "Revisar", "status": "recomendado",
           "prioridade": 0.7, "origem": "desconhecida"}
    resultado = AgenteAuditor().executar([rec])
    assert not resultado["ok"]
    assert any("origem" in p for p in resultado["problemas"])


def test_orquestrador_bloqueia_falha_e_nao_chama_decisor():
    orch = OrquestradorAgentes()
    rec = {"tipo": "pendencia", "recomendacao": "Revisar", "status": "executado",
           "prioridade": 0.5, "origem": "sintetico"}
    orch.detector.executar = lambda eventos: {"recomendacoes": [rec]}
    orch.priorizador.executar = lambda recs: {"recomendacoes": recs}
    def nunca_decidir(recs):
        raise AssertionError("Decisor acionado após auditoria reprovada")
    orch.decisor.executar = nunca_decidir
    resultado = orch.executar_fluxo([{"tipo": "teste", "fonte": "sintetico"}])
    assert resultado["bloqueado"] is True
    assert resultado["auditoria_ok"] is False
    assert resultado["top"] == []
    assert resultado["pendentes_decisao"] == 0


def test_orquestrador_advisory_aceito():
    orch = OrquestradorAgentes()
    rec = {"tipo": "pendencia", "recomendacao": "Verificar", "status": "recomendado",
           "prioridade": 0.5, "origem": "sintetico"}
    orch.detector.executar = lambda eventos: {"recomendacoes": [rec]}
    orch.priorizador.executar = lambda recs: {"recomendacoes": recs}
    resultado = orch.executar_fluxo([{"tipo": "teste", "fonte": "sintetico"}])
    assert resultado["bloqueado"] is False
    assert resultado["auditoria_ok"] is True
    assert resultado["pendentes_decisao"] == 1


def test_decisao_humana_validada_registrada_uma_vez():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        try:
            os.chdir(tmp)
            fluxo = FluxoCoordIA()
            fluxo.pendentes = [{"tipo": "pendencia", "status": "recomendado",
                                "origem": "sintetico"}]
            for idx in (-1, True, 1, "0", None):
                assert fluxo.decidir(idx, "aceito", "coordenador-teste").get("erro")
            assert fluxo.decidir(0, "autorizar_escrita", "coordenador-teste").get("erro")
            assert fluxo.decidir(0, "aceito", "sistema").get("erro")
            assert fluxo.decidir(0, "aceito", "").get("erro")
            resultado = fluxo.decidir(0, "aceito", "coordenador-teste", "apenas teste")
            assert resultado["decisao"] == "aceito"
            assert resultado["recomendacao_id"] == "local-0"
            assert fluxo.decidir(0, "rejeitado", "coordenador-teste").get("erro")
            log = (Path(tmp) / "decisoes.jsonl").read_text(encoding="utf-8")
            assert log.count("\n") == 1 and '"decisao": "aceito"' in log
        finally:
            os.chdir(cwd)


def test_api_falha_fechado_sem_token():
    class FakeHandler:
        def __init__(self, header):
            self.headers = {"Authorization": header}
            self.status = None
        def _json(self, status, data):
            self.status = status

    with patch.dict(os.environ, {"COORDIA_API_TOKEN": ""}):
        fake = FakeHandler("")
        assert Handler._autorizar(fake) is False
        assert fake.status == 503

    secret = "somente-teste-00000000000000000000000000000"
    with patch.dict(os.environ, {"COORDIA_API_TOKEN": secret}):
        fake = FakeHandler("Bearer errado")
        assert Handler._autorizar(fake) is False
        assert fake.status == 401
        fake = FakeHandler("Bearer " + secret)
        assert Handler._autorizar(fake) is True
        assert fake.status is None


if __name__ == "__main__":
    tests = [
        test_auditor_rejeita_proveniencia_ausente,
        test_orquestrador_bloqueia_falha_e_nao_chama_decisor,
        test_orquestrador_advisory_aceito,
        test_decisao_humana_validada_registrada_uma_vez,
        test_api_falha_fechado_sem_token,
    ]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("PASS: cinco grupos de contraprovas sintéticas P0.")
