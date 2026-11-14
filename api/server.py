#!/usr/bin/env python3
"""
API HTTP mínima — COORDIA SMART
Usa apenas a biblioteca padrão (http.server).
Advisory only.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from agents.log_persistente import LogPersistente

nucleo = Nucleo(DETECTORES_PADRAO)
log = LogPersistente("auditoria_api.jsonl")

class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/recomendacao":
            self._send(404, {"erro": "rota não encontrada"})
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            evento = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send(400, {"erro": "JSON inválido"})
            return

        recs = nucleo.processar(evento)
        for rec in recs:
            log.registrar({"evento": evento, "recomendacao": rec})

        self._send(200, {
            "recomendacoes": recs,
            "aviso": "Advisory only — requer ação humana",
            "total": len(recs)
        })

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok", "detectores": len(nucleo.detectores)})
        elif self.path == "/log":
            self._send(200, {"entradas": log.ler_todos()[-20:]})  # últimas 20
        else:
            self._send(404, {"erro": "rota não encontrada"})

    def log_message(self, format, *args):
        return  # silencioso

def main(port: int = 8080):
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"COORDIA SMART API rodando em http://127.0.0.1:{port}")
    print("POST /recomendacao  |  GET /health  |  GET /log")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")
        server.server_close()

if __name__ == "__main__":
    main()
