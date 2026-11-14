"""
Teste mestre — cobre todas as possibilidades implementadas.
Somente dados sintéticos. Advisory only.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import assert_safe_mode, OPERATIONAL_GO, WRITE_ESCOLAR
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from prototype.alertas_planejamento import detector_planejamento, processar_alertas_sinteticos
from prototype.cenarios_sinteticos import executar_todos_cenarios
from agents.log_persistente import LogPersistente
from agents.decisao_humana import registrar_decisao
import tempfile
from pathlib import Path

def test_flags():
    assert_safe_mode()
    assert OPERATIONAL_GO is False
    assert WRITE_ESCOLAR == "NO_GO"

def test_todos_detectores():
    nucleo = Nucleo(DETECTORES_PADRAO)
    casos = [
        {"tipo": "frequencia", "valor": 0.6, "fonte": "sintetico", "aluno_id": "T1"},
        {"tipo": "nota", "valor": 3.0, "fonte": "sintetico", "aluno_id": "T2"},
        {"tipo": "prazo", "dias_restantes": 1, "fonte": "sintetico", "aluno_id": "T3"},
        {"frequencia": 0.6, "nota_media": 4.0, "pendencias_abertas": 4, "fonte": "sintetico", "aluno_id": "T4"},
        {"tipo": "documento", "entregue": False, "nome_documento": "hist", "fonte": "sintetico", "aluno_id": "T5"},
    ]
    for caso in casos:
        recs = nucleo.processar(caso)
        for rec in recs:
            assert rec["status"] == "recomendado"
            assert "resolvido" not in str(rec).lower()

def test_planejamento_e_cenarios():
    recs = processar_alertas_sinteticos(30)
    assert all(r["status"] == "recomendado" for r in recs)
    assert all(r["origem"] == "sintetico" for r in recs)

    resultados = executar_todos_cenarios()
    assert len(resultados) == 3
    for r in resultados:
        assert r["status_todos_recomendado"]
        assert r["origem_sintetico"]

def test_decisao_humana_separada():
    decisao = registrar_decisao(
        recomendacao_id="master-001",
        decisao="aceito",
        responsavel="coordenador",
        observacao="teste mestre"
    )
    assert decisao["tipo"] == "decisao_humana"
    assert "Ação humana" in decisao["aviso"]
    assert decisao["decisao"] == "aceito"

def test_log_e_persistencia():
    with tempfile.TemporaryDirectory() as tmp:
        log = LogPersistente(str(Path(tmp) / "master.jsonl"))
        nucleo = Nucleo([detector_planejamento])
        evento = {
            "tipo": "planejamento",
            "completo": False,
            "dias_atraso": 2,
            "fonte": "sintetico",
            "id_planejamento": "MASTER-PLN",
            "disciplina": "Teste",
            "aluno_id": "SINT-MASTER"
        }
        recs = nucleo.processar(evento)
        for rec in recs:
            log.registrar({"evento": evento, "recomendacao": rec})
        salvos = log.ler_todos()
        assert len(salvos) >= 1
        assert salvos[0]["recomendacao"]["status"] == "recomendado"

def test_sem_escrita_escolar():
    # Garante que nenhum detector ou núcleo tenta escrever em sistema real
    nucleo = Nucleo(DETECTORES_PADRAO + [detector_planejamento])
    evento = {"tipo": "frequencia", "valor": 0.5, "fonte": "sintetico"}
    recs = nucleo.processar(evento)
    for rec in recs:
        assert rec.get("status") != "resolvido"
        assert rec.get("status") != "executado"
        assert "WRITE" not in str(rec)

if __name__ == "__main__":
    test_flags()
    test_todos_detectores()
    test_planejamento_e_cenarios()
    test_decisao_humana_separada()
    test_log_e_persistencia()
    test_sem_escrita_escolar()
    print("✓ Teste mestre (todas as possibilidades atuais) passou.")
