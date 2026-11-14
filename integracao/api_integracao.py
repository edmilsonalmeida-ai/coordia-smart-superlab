#!/usr/bin/env python3
"""
API mínima de integração CoordIA.
Endpoints:
  POST /processar   — recebe eventos, devolve recomendações
  POST /decidir     — registra decisão humana
  GET  /status      — status do conector
"""

import json
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

    def do_GET(self):
        if self.path == "/status":
            self._json(200, fluxo.resumo())
        else:
            self._json(404, {"erro": "não encontrado"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw) if raw else {}
        except Exception:
            self._json(400, {"erro": "JSON inválido"})
            return

        if self.path == "/processar":
            eventos = payload.get("eventos", [])
            recs = fluxo.processar(eventos)
            self._json(200, {"recomendacoes": recs, "total": len(recs)})
        elif self.path == "/decidir":
            resultado = fluxo.decidir(
                payload.get("indice", 0),
                payload.get("decisao", "rejeitado"),
                payload.get("responsavel", "sistema"),
                payload.get("observacao", "")
            )
            self._json(200, resultado)
        else:
            self._json(404, {"erro": "não encontrado"})

    def log_message(self, format, *args):
        pass  # silencioso

def main(port=8080):
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"API de integração em http://127.0.0.1:{port}")
    print("Endpoints: GET /status | POST /processar | POST /decidir")
    server.serve_forever()

if __name__ == "__main__":
    main()
