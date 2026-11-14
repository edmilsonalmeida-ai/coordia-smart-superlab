#!/usr/bin/env python3
"""
CLI simples — COORDIA SMART
Uso:
  python cli.py detectar '{"tipo":"frequencia","valor":0.6,"fonte":"cli"}'
  python cli.py decidir <id> aceito "coordenador" "Observação"
"""

import json
import sys
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from agents.decisao_humana import registrar_decisao
from agents.log_persistente import LogPersistente

nucleo = Nucleo(DETECTORES_PADRAO)
log = LogPersistente("auditoria_cli.jsonl")

def cmd_detectar(evento_json: str):
    evento = json.loads(evento_json)
    recs = nucleo.processar(evento)
    for rec in recs:
        log.registrar({"evento": evento, "recomendacao": rec})
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    if not recs:
        print("Nenhuma recomendação.")

def cmd_decidir(rec_id: str, decisao: str, responsavel: str, obs: str = ""):
    entrada = registrar_decisao(rec_id, decisao, responsavel, obs)
    log.registrar(entrada)
    print(json.dumps(entrada, ensure_ascii=False, indent=2))

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "detectar" and len(sys.argv) >= 3:
        cmd_detectar(sys.argv[2])
    elif cmd == "decidir" and len(sys.argv) >= 5:
        cmd_decidir(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
