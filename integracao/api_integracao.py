#!/usr/bin/env python3
"""
API mínima de integração CoordIA.
Endpoints:
  POST /processar   — recebe eventos, devolve recomendações
  POST /decidir     — registra decisão humana
  GET  /status      — status do conector
"""

import json
import os
import hmac
from http.server import HTTPServer, BaseHTTPRequestHandler
from integracao.fluxo_completo import FluxoCoordIA

fluxo = FluxoCoordIA()

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _autorizar(self):
        """Falha fechado se não houver token de serviço configurado."""
        segredo = os.environ.get("COORDIA_API_TOKEN", "")
        if len(segredo) < 32:
            self._json(503, {"erro": "API não configurada para alterações"})
            return False
        fornecido = self.headers.get("Authorization", "")
        if not hmac.compare_digest(fornecido, "Bearer " + segredo):
            self._json(401, {"erro": "autenticação obrigatória"})
            return False
        return True

    def do_GET(self):
        if self.path == "/status":
            self._json(200, fluxo.resumo())
        else:
            self._json(404, {"erro": "não encontrado"})

    def do_POST(self):
        if self.path not in ("/processar", "/decidir"):
            self._json(404, {"erro": "não encontrado"})
            return
        if not self._autorizar():
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._json(400, {"erro": "Content-Length inválido"})
            return
        if length <= 0 or length > 65536:
            self._json(413, {"erro": "corpo vazio ou maior que o permitido"})
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            self._json(400, {"erro": "JSON inválido"})
            return
        if not isinstance(payload, dict):
            self._json(400, {"erro": "objeto JSON obrigatório"})
            return

        if self.path == "/processar":
            eventos = payload.get("eventos", [])
            if not isinstance(eventos, list) or len(eventos) > 100:
                self._json(422, {"erro": "lote inválido"})
                return
            # Nenhum conector escolar real está autenticado nesta API mínima.
            if any(not isinstance(ev, dict) or ev.get("fonte") != "sintetico" for ev in eventos):
                self._json(422, {"erro": "somente eventos sintéticos comprovados neste endpoint"})
                return
            recs = fluxo.processar(eventos)
            self._json(200, {"recomendacoes": recs, "total": len(recs)})
        else:
            resultado = fluxo.decidir(
                payload.get("indice"),
                payload.get("decisao"),
                payload.get("responsavel"),
                payload.get("observacao", "")
            )
            self._json(422 if "erro" in resultado else 200, resultado)

    def log_message(self, format, *args):
        pass  # silencioso

def main(port=8080):
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"API de integração em http://127.0.0.1:{port}")
    print("Endpoints: GET /status | POST /processar | POST /decidir")
    server.serve_forever()

if __name__ == "__main__":
    main()
