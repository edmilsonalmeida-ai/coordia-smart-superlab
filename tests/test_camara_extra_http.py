"""Teste HTTP ponta a ponta local: sem conexões externas nem dados escolares."""
import json
import os
import sys
import tempfile
import threading
from pathlib import Path
from http.server import HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import integracao.api_integracao as api
from integracao.fluxo_completo import FluxoCoordIA


def executar_http_sintetico():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        servidor = None
        thread = None
        try:
            os.chdir(tmp)
            api.fluxo = FluxoCoordIA()
            servidor = HTTPServer(("127.0.0.1", 0), api.Handler)
            thread = threading.Thread(target=servidor.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
            thread.start()
            endpoint = "http://127.0.0.1:" + str(servidor.server_port)

            def post(rota, payload, token=None):
                cabecalhos = {"Content-Type": "application/json"}
                if token:
                    cabecalhos["Authorization"] = "Bearer " + token
                req = Request(endpoint + rota, data=json.dumps(payload).encode(), headers=cabecalhos, method="POST")
                try:
                    with urlopen(req, timeout=4) as res:
                        return res.status, json.load(res)
                except HTTPError as err:
                    return err.code, json.load(err)

            secret = "senha-testes-123456789012345678901234567890"
            with patch.dict(os.environ, {"COORDIA_API_TOKEN": ""}):
                code, _ = post("/processar", {"eventos": []})
                assert code == 503

            with patch.dict(os.environ, {"COORDIA_API_TOKEN": secret}):
                code, _ = post("/processar", {"eventos": []}, "token-errado")
                assert code == 401

                sint = {"tipo": "frequencia", "valor": 0.4, "fonte": "sintetico", "aluno_id": "SINT-001"}
                code, _ = post("/processar", {"eventos": [dict(sint, nome_estudante="PII-PROIBIDA")]}, secret)
                assert code == 422
                code, _ = post("/processar", {"eventos": [dict(sint, aluno_id="MATRICULA-REAL")]}, secret)
                assert code == 422

                code, dados = post("/processar", {"eventos": [sint]}, secret)
                assert code == 200 and dados["total"] >= 1
                assert all(rec["status"] == "recomendado" for rec in dados["recomendacoes"])

                code, _ = post("/decidir", {"indice": -1, "decisao": "aceito", "responsavel": "coordenador-teste"}, secret)
                assert code == 422
                code, _ = post("/decidir", {"indice": 0, "decisao": "aceito", "responsavel": "sistema"}, secret)
                assert code == 422
                code, decisao = post("/decidir", {"indice": 0, "decisao": "aceito", "responsavel": "coordenador-teste"}, secret)
                assert code == 200 and decisao["tipo"] == "decisao_humana"
                code, _ = post("/decidir", {"indice": 0, "decisao": "aceito", "responsavel": "coordenador-teste"}, secret)
                assert code == 422

                log = (Path(tmp) / "decisoes.jsonl").read_text(encoding="utf-8")
                assert log.count("\n") == 1
                assert "MATRICULA-REAL" not in log and "PII-PROIBIDA" not in log
                print("PASS HTTP: bloqueios, sintético, decisão humana e rejeição de duplicidade")
        finally:
            if servidor is not None:
                servidor.shutdown()
                servidor.server_close()
            if thread is not None:
                thread.join(timeout=2)
            os.chdir(cwd)


if __name__ == "__main__":
    executar_http_sintetico()
