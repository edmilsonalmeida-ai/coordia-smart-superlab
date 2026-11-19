#!/usr/bin/env python3
"""
Dashboard web do CoordIA SMART.
Interface simples para visualização e decisão.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs
from config import status_modo
from monitor import monitor
from interface_decisao import InterfaceDecisao

interface = InterfaceDecisao()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CoordIA SMART</title>
    <style>
        body { font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 20px; }
        .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .alta { border-left: 4px solid #e74c3c; }
        .media { border-left: 4px solid #f39c12; }
        .baixa { border-left: 4px solid #27ae60; }
        button { padding: 8px 16px; margin: 5px; cursor: pointer; }
        .aceitar { background: #27ae60; color: white; border: none; }
        .rejeitar { background: #e74c3c; color: white; border: none; }
    </style>
</head>
<body>
    <h1>CoordIA SMART</h1>
    <div class="card">
        <h3>Status</h3>
        <p>Modo: {modo}</p>
        <p>Eventos processados: {eventos}</p>
        <p>Pendentes de decisão: {pendentes}</p>
    </div>
    <h2>Recomendações Pendentes</h2>
    {recomendacoes}
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self._dashboard()
        elif self.path == "/api/status":
            self._json({"status": status_modo(), "metricas": monitor.metricas()})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/decidir":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            resultado = interface.decidir(
                body.get("indice", 0),
                body.get("decisao", "rejeitado"),
                body.get("responsavel", "web"),
                body.get("observacao", "")
            )
            self._json(resultado)
        else:
            self.send_error(404)

    def _dashboard(self):
        status = status_modo()
        metricas = monitor.metricas()
        pendentes = interface.listar_pendentes()

        recs_html = ""
        for p in pendentes[:10]:
            rec = p.get("recomendacao", {})
            prio = rec.get("prioridade", 0)
            classe = "alta" if prio >= 0.8 else "media" if prio >= 0.5 else "baixa"
            recs_html += f"""
            <div class="card {classe}">
                <strong>[{prio:.2f}] {rec.get('tipo', 'N/A')}</strong>
                <p>{rec.get('recomendacao', '')[:100]}</p>
                <button class="aceitar" onclick="decidir({p['indice']}, 'aceito')">Aceitar</button>
                <button class="rejeitar" onclick="decidir({p['indice']}, 'rejeitado')">Rejeitar</button>
            </div>
            """

        html = HTML_TEMPLATE.format(
            modo=status.get("aviso", "N/A"),
            eventos=metricas.get("eventos_processados", 0),
            pendentes=len(pendentes),
            recomendacoes=recs_html or "<p>Nenhuma pendência.</p>"
        )
        html += """
        <script>
        function decidir(indice, decisao) {
            fetch('/api/decidir', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({indice, decisao, responsavel: 'dashboard'})
            }).then(() => location.reload());
        }
        </script>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def _json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

def main(port=8080):
    print(f"Dashboard em http://127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()

if __name__ == "__main__":
    main()
